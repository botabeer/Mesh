"""
🎮 Bot Mesh v8.0 - Main Server
Created by: Abeer Aldosari © 2025

✅ Webhook Handler
✅ Background Processing
✅ Game Management
✅ User Management
"""

import os
import logging
import threading
from flask import Flask, request, abort

from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi,
    ReplyMessageRequest, TextMessage
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent, FollowEvent

from ui import (
    build_home, build_games_menu, build_my_points,
    build_leaderboard, build_registration_required
)
from games import GameLoader
from db import DB

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
game_loader = GameLoader()

configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

logger.info("✅ Bot Mesh initialized")

# ============================================================================
# Helper Functions
# ============================================================================
def normalize_text(text):
    """تطبيع النص العربي"""
    text = text.strip().lower()
    replacements = {
        'أ': 'ا', 'إ': 'ا', 'آ': 'ا',
        'ى': 'ي', 'ة': 'ه'
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text

def get_username(profile):
    """الحصول على اسم المستخدم"""
    return profile.display_name if profile.display_name else "مستخدم"

# ============================================================================
# Background Message Processing
# ============================================================================
def process_message_background(user_id, text, reply_token):
    """معالجة الرسالة في الخلفية"""
    try:
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
            if normalized in ['بداية', 'start', 'home']:
                msg = build_home(theme, name, points, is_registered)
                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(reply_token=reply_token, messages=[msg])
                )
                return
            
            # اختيار الثيم
            if normalized.startswith('ثيم '):
                new_theme = text.replace('ثيم ', '').strip()
                if new_theme in ['💜', '💙', '💚', '🖤', '🩷', '🧡']:
                    if user:
                        db.update_theme(user_id, new_theme)
                        theme = new_theme
                    msg = build_home(theme, name, points, is_registered)
                    line_bot_api.reply_message_with_http_info(
                        ReplyMessageRequest(reply_token=reply_token, messages=[msg])
                    )
                return
            
            # الانضمام
            if normalized in ['انضم', 'join']:
                if not is_registered:
                    db.create_user(user_id, name, theme)
                    text_msg = f"✅ تم تسجيلك يا {name}!"
                else:
                    text_msg = f"ℹ️ أنت مسجل بالفعل يا {name}"
                
                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(
                        reply_token=reply_token,
                        messages=[TextMessage(text=text_msg)]
                    )
                )
                return
            
            # الانسحاب
            if normalized in ['انسحب', 'leave']:
                if is_registered:
                    db.deactivate_user(user_id)
                    text_msg = f"👋 تم إلغاء تسجيلك يا {name}"
                else:
                    text_msg = "ℹ️ أنت غير مسجل"
                
                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(
                        reply_token=reply_token,
                        messages=[TextMessage(text=text_msg)]
                    )
                )
                return
            
            # قائمة الألعاب
            if normalized in ['مساعدة', 'help', 'العاب', 'games']:
                if not is_registered:
                    msg = build_registration_required(theme)
                else:
                    msg = build_games_menu(theme)
                
                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(reply_token=reply_token, messages=[msg])
                )
                return
            
            # نقاطي
            if normalized in ['نقاطي', 'points']:
                if not is_registered:
                    msg = build_registration_required(theme)
                else:
                    msg = build_my_points(name, points, theme)
                
                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(reply_token=reply_token, messages=[msg])
                )
                return
            
            # الصدارة
            if normalized in ['صدارة', 'leaderboard']:
                top = db.get_leaderboard(10)
                msg = build_leaderboard(top, theme)
                
                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(reply_token=reply_token, messages=[msg])
                )
                return
            
            # ==================== الألعاب ====================
            
            # بدء لعبة
            if normalized.startswith('لعبة '):
                if not is_registered:
                    msg = build_registration_required(theme)
                    line_bot_api.reply_message_with_http_info(
                        ReplyMessageRequest(reply_token=reply_token, messages=[msg])
                    )
                    return
                
                game_name = text.replace('لعبة ', '').strip()
                
                # إنهاء اللعبة السابقة
                if game_loader.has_active_game(user_id):
                    game_loader.end_game(user_id)
                
                # بدء لعبة جديدة
                response = game_loader.start_game(user_id, game_name)
                
                if not response:
                    available = "، ".join(game_loader.get_available_games())
                    text_msg = f"❌ اللعبة '{game_name}' غير موجودة\n\n🎮 المتاحة:\n{available}"
                    line_bot_api.reply_message_with_http_info(
                        ReplyMessageRequest(
                            reply_token=reply_token,
                            messages=[TextMessage(text=text_msg)]
                        )
                    )
                    return
                
                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(reply_token=reply_token, messages=[response])
                )
                return
            
            # إيقاف اللعبة
            if normalized in ['إيقاف', 'stop', 'ايقاف']:
                if game_loader.has_active_game(user_id):
                    game_loader.end_game(user_id)
                    text_msg = "⛔ تم إيقاف اللعبة"
                else:
                    text_msg = "ℹ️ لا توجد لعبة نشطة"
                
                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(
                        reply_token=reply_token,
                        messages=[TextMessage(text=text_msg)]
                    )
                )
                return
            
            # ==================== أثناء اللعب ====================
            
            if game_loader.has_active_game(user_id):
                game = game_loader.get_game(user_id)
                
                # تلميح
                if normalized in ['لمح', 'hint']:
                    hint = game.get_hint() if hasattr(game, 'get_hint') else "💡 لا يوجد تلميح"
                    line_bot_api.reply_message_with_http_info(
                        ReplyMessageRequest(
                            reply_token=reply_token,
                            messages=[TextMessage(text=hint)]
                        )
                    )
                    return
                
                # فحص الإجابة
                result = game.check_answer(text, user_id, name)
                
                if result:
                    # إضافة النقاط
                    if result.get('points', 0) > 0:
                        db.add_points(user_id, result['points'])
                    
                    # إرسال الرد
                    if 'response' in result:
                        line_bot_api.reply_message_with_http_info(
                            ReplyMessageRequest(
                                reply_token=reply_token,
                                messages=[result['response']]
                            )
                        )
                    else:
                        line_bot_api.reply_message_with_http_info(
                            ReplyMessageRequest(
                                reply_token=reply_token,
                                messages=[TextMessage(text=result.get('message', 'حدث خطأ'))]
                            )
                        )
                    
                    # إنهاء اللعبة
                    if result.get('game_over'):
                        game_loader.end_game(user_id)
                    
                    return
            
            # تجاهل الرسائل من غير المسجلين
            if not is_registered:
                logger.info(f"Ignored message from unregistered user: {user_id}")
                return
            
    except Exception as e:
        logger.error(f"Background processing error: {e}", exc_info=True)

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
                line_bot_api.push_message_with_http_info(
                    user_id,
                    [msg]
                )
                
            except Exception as e:
                logger.error(f"Follow error: {e}")
    
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
        "bot": "Bot Mesh v8.0",
        "games": len(game_loader.loaded),
        "users": db.get_total_users()
    }

@app.route("/health", methods=["GET"])
def health():
    """فحص الصحة"""
    return {"status": "healthy"}, 200

@app.route("/callback", methods=["POST"])
def callback():
    """LINE webhook"""
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        logger.error("Invalid signature")
        abort(400)
    except Exception as e:
        logger.error(f"Callback error: {e}", exc_info=True)
    
    return "OK"

# ============================================================================
# Startup
# ============================================================================
if __name__ == "__main__":
    logger.info(f"""
    ╔══════════════════════════════════╗
    ║   🎮 Bot Mesh v8.0 Starting     ║
    ║   Port: {PORT}                    ║
    ║   Games: {len(game_loader.loaded)}                   ║
    ╚══════════════════════════════════╝
    """)
    
    app.run(host="0.0.0.0", port=PORT, debug=False)
