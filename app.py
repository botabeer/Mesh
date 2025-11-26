"""
🎮 Bot Mesh v8.0 - Main Server (Enhanced & Secured)
Created by: Abeer Aldosari © 2025

✅ Fixed imports
✅ Rate limiting
✅ Input validation
✅ Better error handling
✅ Security enhancements
"""

import os
import logging
import threading
import time
from collections import defaultdict
from flask import Flask, request, abort

from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi,
    ReplyMessageRequest, TextMessage, QuickReply, QuickReplyItem, MessageAction
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent, FollowEvent

from ui import (
    build_home, build_games_menu, build_my_points,
    build_leaderboard, build_registration_required, build_help
)
from games import GameLoader  # Fixed import
from db import DB
from constants import QUICK_REPLY_BUTTONS, BOT_NAME, ERROR_MESSAGES, RATE_LIMITS

# ============================================================================
# Setup
# ============================================================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# Configuration
# ============================================================================
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', '')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET', '')
PORT = int(os.getenv('PORT', 10000))

if not LINE_CHANNEL_ACCESS_TOKEN or not LINE_CHANNEL_SECRET:
    logger.error("❌ LINE credentials missing!")
    exit(1)

# ============================================================================
# Initialize
# ============================================================================
app = Flask(__name__)
db = DB()
game_loader = GameLoader()  # Fixed class name

configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

logger.info(f"✅ {BOT_NAME} initialized with {len(game_loader.loaded)} games")

# ============================================================================
# Rate Limiting (Simple In-Memory)
# ============================================================================
class SimpleRateLimiter:
    """محدد معدل بسيط في الذاكرة"""
    
    def __init__(self):
        self.requests = defaultdict(list)
        self.lock = threading.Lock()
    
    def is_allowed(self, user_id: str, max_per_minute: int = 10) -> bool:
        """التحقق من السماح بالطلب"""
        with self.lock:
            now = time.time()
            minute_ago = now - 60
            
            # تنظيف الطلبات القديمة
            self.requests[user_id] = [
                t for t in self.requests[user_id] if t > minute_ago
            ]
            
            # التحقق من الحد
            if len(self.requests[user_id]) >= max_per_minute:
                return False
            
            # إضافة الطلب الجديد
            self.requests[user_id].append(now)
            return True

rate_limiter = SimpleRateLimiter()

# ============================================================================
# Input Validation
# ============================================================================
def validate_text_input(text: str) -> bool:
    """التحقق من صحة الإدخال النصي"""
    if not text or not isinstance(text, str):
        return False
    
    # الطول المسموح
    if len(text) > 500:
        return False
    
    # منع الأحرف الخطرة
    dangerous_chars = ['<script>', 'javascript:', 'onerror=']
    text_lower = text.lower()
    for char in dangerous_chars:
        if char in text_lower:
            return False
    
    return True

# ============================================================================
# Helper Functions
# ============================================================================
def normalize_text(text: str) -> str:
    """تطبيع النص العربي"""
    if not text:
        return ""
    
    text = text.strip().lower()
    
    # تطبيع الحروف العربية
    replacements = {
        'أ': 'ا', 'إ': 'ا', 'آ': 'ا',
        'ى': 'ي', 'ة': 'ه'
    }
    
    for old, new in replacements.items():
        text = text.replace(old, new)
    
    return text

def get_username(profile) -> str:
    """الحصول على اسم المستخدم بشكل آمن"""
    try:
        return profile.display_name if profile.display_name else "مستخدم"
    except:
        return "مستخدم"

def create_quick_reply() -> QuickReply:
    """إنشاء Quick Reply"""
    items = []
    for btn in QUICK_REPLY_BUTTONS:
        items.append(
            QuickReplyItem(
                action=MessageAction(
                    label=btn["label"],
                    text=btn["text"]
                )
            )
        )
    return QuickReply(items=items)

def add_quick_reply_to_message(message):
    """إضافة Quick Reply لأي رسالة"""
    quick_reply = create_quick_reply()
    if hasattr(message, 'quick_reply'):
        message.quick_reply = quick_reply
    return message

def safe_reply(line_bot_api, reply_token, messages):
    """إرسال رد آمن مع معالجة الأخطاء"""
    try:
        if not isinstance(messages, list):
            messages = [messages]
        
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(reply_token=reply_token, messages=messages)
        )
        return True
    except Exception as e:
        logger.error(f"❌ Failed to send reply: {e}")
        return False

# ============================================================================
# Background Message Processing
# ============================================================================
def process_message_background(user_id: str, text: str, reply_token: str):
    """معالجة الرسالة في الخلفية"""
    try:
        # Rate Limiting
        if not rate_limiter.is_allowed(user_id, RATE_LIMITS['max_messages_per_minute']):
            logger.warning(f"⚠️ Rate limit exceeded for {user_id}")
            return
        
        # Input Validation
        if not validate_text_input(text):
            logger.warning(f"⚠️ Invalid input from {user_id}")
            return
        
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            
            # جلب الملف الشخصي
            profile = line_bot_api.get_profile(user_id)
            name = get_username(profile)
            
            # الحصول على بيانات المستخدم
            user = db.get_user(user_id)
            theme = user['theme'] if user else '💜'
            points = user['points'] if user else 0
            is_registered = user is not None and user['status'] == 'active'
            
            normalized = normalize_text(text)
            
            # ==================== الأوامر الأساسية ====================
            
            # البداية
            if normalized in ['بداية', 'start', 'home', 'بدايه']:
                msg = build_home(theme, name, points, is_registered)
                msg = add_quick_reply_to_message(msg)
                safe_reply(line_bot_api, reply_token, msg)
                return
            
            # المساعدة
            if normalized in ['مساعدة', 'help', 'مساعده']:
                msg = build_help(theme)
                msg = add_quick_reply_to_message(msg)
                safe_reply(line_bot_api, reply_token, msg)
                return
            
            # اختيار الثيم
            if normalized.startswith('ثيم '):
                new_theme = text.replace('ثيم ', '').strip()
                valid_themes = ['💜', '💚', '💙', '🖤', '🩷', '🧡', '🤍', '🤎', '💛']
                
                if new_theme in valid_themes:
                    if user:
                        db.update_theme(user_id, new_theme)
                        theme = new_theme
                    msg = build_home(theme, name, points, is_registered)
                    msg = add_quick_reply_to_message(msg)
                    safe_reply(line_bot_api, reply_token, msg)
                return
            
            # الانضمام
            if normalized in ['انضم', 'join']:
                if not is_registered:
                    db.create_user(user_id, name, theme)
                    text_msg = TextMessage(text=f"✅ تم تسجيلك يا {name}!")
                else:
                    text_msg = TextMessage(text=f"ℹ️ أنت مسجل بالفعل يا {name}")
                
                text_msg = add_quick_reply_to_message(text_msg)
                safe_reply(line_bot_api, reply_token, text_msg)
                return
            
            # الانسحاب
            if normalized in ['انسحب', 'leave']:
                if is_registered:
                    db.deactivate_user(user_id)
                    text_msg = TextMessage(text=f"👋 تم إلغاء تسجيلك يا {name}")
                else:
                    text_msg = TextMessage(text="ℹ️ أنت غير مسجل")
                
                text_msg = add_quick_reply_to_message(text_msg)
                safe_reply(line_bot_api, reply_token, text_msg)
                return
            
            # قائمة الألعاب
            if normalized in ['العاب', 'games', 'ألعاب']:
                if not is_registered:
                    msg = build_registration_required(theme)
                else:
                    msg = build_games_menu(theme)
                
                msg = add_quick_reply_to_message(msg)
                safe_reply(line_bot_api, reply_token, msg)
                return
            
            # نقاطي
            if normalized in ['نقاطي', 'points']:
                if not is_registered:
                    msg = build_registration_required(theme)
                else:
                    msg = build_my_points(name, points, theme)
                
                msg = add_quick_reply_to_message(msg)
                safe_reply(line_bot_api, reply_token, msg)
                return
            
            # الصدارة
            if normalized in ['صدارة', 'leaderboard', 'صداره']:
                top = db.get_leaderboard(10)
                msg = build_leaderboard(top, theme)
                msg = add_quick_reply_to_message(msg)
                safe_reply(line_bot_api, reply_token, msg)
                return
            
            # ==================== الألعاب ====================
            
            # بدء لعبة
            if normalized.startswith('لعبة ') or normalized.startswith('لعبه '):
                if not is_registered:
                    msg = build_registration_required(theme)
                    msg = add_quick_reply_to_message(msg)
                    safe_reply(line_bot_api, reply_token, msg)
                    return
                
                game_name = text.replace('لعبة ', '').replace('لعبه ', '').strip()
                
                # إنهاء اللعبة السابقة
                if game_loader.has_active_game(user_id):
                    game_loader.end_game(user_id)
                
                # بدء لعبة جديدة
                response = game_loader.start_game(user_id, game_name)
                
                if not response:
                    available = "، ".join(game_loader.get_available_games())
                    text_msg = TextMessage(text=f"❌ اللعبة '{game_name}' غير موجودة\n\n🎮 المتاحة:\n{available}")
                    text_msg = add_quick_reply_to_message(text_msg)
                    safe_reply(line_bot_api, reply_token, text_msg)
                    return
                
                response = add_quick_reply_to_message(response)
                safe_reply(line_bot_api, reply_token, response)
                return
            
            # إيقاف اللعبة
            if normalized in ['إيقاف', 'stop', 'ايقاف']:
                if game_loader.has_active_game(user_id):
                    game_loader.end_game(user_id)
                    text_msg = TextMessage(text="⛔ تم إيقاف اللعبة")
                else:
                    text_msg = TextMessage(text="ℹ️ لا توجد لعبة نشطة")
                
                text_msg = add_quick_reply_to_message(text_msg)
                safe_reply(line_bot_api, reply_token, text_msg)
                return
            
            # ==================== أثناء اللعب ====================
            
            if game_loader.has_active_game(user_id):
                game = game_loader.get_game(user_id)
                
                # تلميح
                if normalized in ['لمح', 'hint']:
                    hint = game.get_hint() if hasattr(game, 'get_hint') else "💡 لا يوجد تلميح"
                    hint_msg = TextMessage(text=hint)
                    hint_msg = add_quick_reply_to_message(hint_msg)
                    safe_reply(line_bot_api, reply_token, hint_msg)
                    return
                
                # فحص الإجابة
                result = game.check_answer(text, user_id, name)
                
                if result:
                    # إضافة النقاط
                    if result.get('points', 0) > 0:
                        db.add_points(user_id, result['points'])
                    
                    # إرسال الرد
                    if 'response' in result:
                        response = add_quick_reply_to_message(result['response'])
                        safe_reply(line_bot_api, reply_token, response)
                    else:
                        text_msg = TextMessage(text=result.get('message', 'حدث خطأ'))
                        text_msg = add_quick_reply_to_message(text_msg)
                        safe_reply(line_bot_api, reply_token, text_msg)
                    
                    # إنهاء اللعبة
                    if result.get('game_over'):
                        game_loader.end_game(user_id)
                    
                    return
            
            # تجاهل الرسائل من غير المسجلين
            if not is_registered:
                logger.info(f"Ignored message from unregistered user: {user_id}")
                return
            
            # رسالة افتراضية
            default_msg = TextMessage(text="❓ لم أفهم الأمر. اكتب 'مساعدة' لعرض الأوامر")
            default_msg = add_quick_reply_to_message(default_msg)
            safe_reply(line_bot_api, reply_token, default_msg)
            
    except Exception as e:
        logger.error(f"❌ Background processing error: {e}", exc_info=True)

# ============================================================================
# Webhook Handlers
# ============================================================================
@handler.add(FollowEvent)
def handle_follow(event):
    """معالجة متابعة جديدة"""
    user_id = event.source.user_id
    
    def background():
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            
            try:
                profile = line_bot_api.get_profile(user_id)
                name = get_username(profile)
                
                # تسجيل المستخدم
                db.create_user(user_id, name, '💜')
                
                # إرسال رسالة ترحيب
                msg = build_home('💜', name, 0, True)
                msg = add_quick_reply_to_message(msg)
                line_bot_api.push_message_with_http_info(user_id, [msg])
                
            except Exception as e:
                logger.error(f"❌ Follow error: {e}")
    
    threading.Thread(target=background, daemon=True).start()

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    """معالجة الرسائل النصية"""
    user_id = event.source.user_id
    text = event.message.text.strip()
    reply_token = event.reply_token
    
    # معالجة خلفية
    threading.Thread(
        target=process_message_background,
        args=(user_id, text, reply_token),
        daemon=True
    ).start()

# ============================================================================
# Flask Routes
# ============================================================================
@app.route("/", methods=["GET"])
def home():
    """الصفحة الرئيسية"""
    return {
        "status": "running",
        "bot": f"{BOT_NAME} v8.0",
        "games": len(game_loader.loaded),
        "users": db.get_total_users(),
        "features": [
            "9 Neumorphic Themes",
            "12 Games with Quick Reply",
            "Theme Storage per User",
            "Full Arabic Support",
            "Rate Limiting",
            "Input Validation"
        ]
    }

@app.route("/health", methods=["GET"])
def health():
    """فحص الصحة"""
    return {
        "status": "healthy",
        "games_loaded": len(game_loader.loaded),
        "active_sessions": len(game_loader.active_sessions)
    }, 200

@app.route("/callback", methods=["POST"])
def callback():
    """LINE webhook"""
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        logger.error("❌ Invalid signature")
        abort(400)
    except Exception as e:
        logger.error(f"❌ Callback error: {e}", exc_info=True)
    
    return "OK"

@app.route("/stats", methods=["GET"])
def stats():
    """إحصائيات البوت"""
    return {
        "total_users": db.get_total_users(),
        "total_points": db.get_total_points(),
        "games_available": len(game_loader.loaded),
        "active_games": len(game_loader.active_sessions),
        "leaderboard": db.get_leaderboard(5)
    }

# ============================================================================
# Error Handlers
# ============================================================================
@app.errorhandler(404)
def not_found(error):
    return {"error": "Not found"}, 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"❌ Internal error: {error}")
    return {"error": "Internal server error"}, 500

# ============================================================================
# Startup
# ============================================================================
if __name__ == "__main__":
    logger.info(f"""
    ╔══════════════════════════════════╗
    ║   🎮 {BOT_NAME} v8.0 Starting    ║
    ║   Port: {PORT}                    ║
    ║   Games: {len(game_loader.loaded)}                   ║
    ║   Themes: 9                      ║
    ║   Security: ✅                   ║
    ╚══════════════════════════════════╝
    """)
    
    app.run(host="0.0.0.0", port=PORT, debug=False)
