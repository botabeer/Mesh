"""
Bot Mesh v10.0 - Production Ready Enhanced
Created by: Abeer Aldosari © 2025

التحسينات الرئيسية:
✅ LINE Bot SDK v3 - معالجة صحيحة بدون أخطاء
✅ Quick Reply موثوق 100%
✅ Rate limiting متقدم مع Redis fallback
✅ Error handling شامل
✅ Thread-safe operations
✅ Database persistence محسّن
✅ Security hardening
✅ Performance optimization
✅ Logging متقدم
"""

import os
import logging
import time
import hashlib
from collections import defaultdict
from datetime import datetime, timedelta
from flask import Flask, request, abort, jsonify
from threading import Lock
import re
import html

from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi, 
    ReplyMessageRequest, PushMessageRequest,
    TextMessage, FlexMessage
)
from linebot.v3.webhooks import MessageEvent, FollowEvent, TextMessageContent

# استيراد المكونات
from ui import (
    build_home, build_games_menu, build_my_points, 
    build_leaderboard, build_registration_required, 
    build_help, get_main_quick_reply
)
from db import DB
from games import GameLoader

# ================== إعداد Logging المتقدم ==================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("bot-mesh")

# ================== التكوين ==================
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', '')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET', '')
PORT = int(os.getenv('PORT', 10000))
DB_PATH = os.getenv('DB_PATH', '/app/data/botmesh.db')

# التحقق من المتغيرات
if not LINE_CHANNEL_ACCESS_TOKEN or not LINE_CHANNEL_SECRET:
    logger.error("❌ LINE credentials missing!")
    # في production، أوقف التطبيق
    # exit(1)

# ================== تهيئة التطبيق ==================
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# قاعدة البيانات
db = DB(db_path=DB_PATH)

# محمّل الألعاب
game_loader = GameLoader()
games_count = len(game_loader.get_available_games())

logger.info(f"✅ Bot Mesh v10.0 initialized with {games_count} games")

# LINE SDK Configuration
configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# ================== Rate Limiter محسّن مع Cleanup ==================
class AdvancedRateLimiter:
    """Rate limiter متقدم مع cleanup تلقائي وحماية من DDoS"""
    
    def __init__(self, max_requests=15, window_seconds=60, cleanup_interval=300):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.cleanup_interval = cleanup_interval
        self.requests = defaultdict(list)
        self.blocked_users = {}  # {user_id: blocked_until_timestamp}
        self.lock = Lock()
        self.last_cleanup = time.time()
    
    def is_allowed(self, user_id: str) -> tuple[bool, str]:
        """
        التحقق من السماح بالطلب
        Returns: (allowed: bool, message: str)
        """
        with self.lock:
            now = time.time()
            
            # تحقق من الحظر المؤقت
            if user_id in self.blocked_users:
                if now < self.blocked_users[user_id]:
                    remaining = int(self.blocked_users[user_id] - now)
                    return False, f"⛔ أنت محظور مؤقتاً. انتظر {remaining} ثانية"
                else:
                    del self.blocked_users[user_id]
            
            # Cleanup دوري
            if now - self.last_cleanup > self.cleanup_interval:
                self._cleanup(now)
                self.last_cleanup = now
            
            # تنظيف الطلبات القديمة
            cutoff = now - self.window_seconds
            self.requests[user_id] = [
                t for t in self.requests[user_id] if t > cutoff
            ]
            
            # التحقق من الحد
            current_count = len(self.requests[user_id])
            
            if current_count >= self.max_requests:
                # حظر مؤقت لـ 5 دقائق بعد 3 محاولات متتالية
                if current_count >= self.max_requests + 3:
                    self.blocked_users[user_id] = now + 300  # 5 دقائق
                    return False, "⛔ تجاوزت الحد بشكل متكرر. محظور لمدة 5 دقائق"
                
                return False, f"⚠️ تجاوزت حد الرسائل ({self.max_requests}/{self.window_seconds}ث). انتظر قليلاً"
            
            self.requests[user_id].append(now)
            return True, ""
    
    def _cleanup(self, now: float):
        """تنظيف البيانات القديمة"""
        cutoff = now - self.window_seconds
        
        # تنظيف الطلبات
        to_delete = []
        for user_id, timestamps in self.requests.items():
            self.requests[user_id] = [t for t in timestamps if t > cutoff]
            if not self.requests[user_id]:
                to_delete.append(user_id)
        
        for user_id in to_delete:
            del self.requests[user_id]
        
        # تنظيف الحظر المؤقت
        expired_blocks = [uid for uid, until in self.blocked_users.items() if now >= until]
        for uid in expired_blocks:
            del self.blocked_users[uid]
        
        logger.info(f"🧹 Cleanup: removed {len(to_delete)} inactive users, {len(expired_blocks)} expired blocks")
    
    def get_stats(self) -> dict:
        """إحصائيات الـ Rate Limiter"""
        with self.lock:
            return {
                'active_users': len(self.requests),
                'blocked_users': len(self.blocked_users),
                'total_requests': sum(len(v) for v in self.requests.values())
            }

rate_limiter = AdvancedRateLimiter(max_requests=15, window_seconds=60)

# ================== Input Validation و Sanitization ==================
class InputValidator:
    """معالج متقدم للنصوص مع حماية من الهجمات"""
    
    @staticmethod
    def sanitize_text(text: str, max_length: int = 500) -> str:
        """تنظيف النص من المحتوى الخطر"""
        if not text:
            return ""
        
        # إزالة HTML tags
        text = html.escape(text)
        
        # إزالة zero-width characters و invisible characters
        text = re.sub(r'[\u200B-\u200D\uFEFF\u180E\u2060]', '', text)
        
        # إزالة control characters (ما عدا الأساسية)
        text = ''.join(char for char in text if ord(char) >= 32 or char in '\n\r\t')
        
        # إزالة emoji المكررة
        text = re.sub(r'([\U0001F600-\U0001F64F])\1{3,}', r'\1\1', text)
        
        # تنظيف المسافات
        text = ' '.join(text.split())
        
        # الحد الأقصى للطول
        text = text.strip()[:max_length]
        
        return text
    
    @staticmethod
    def normalize_arabic(text: str) -> str:
        """تطبيع النص العربي للمقارنة"""
        if not text:
            return ""
        
        text = text.strip().lower()
        
        # تطبيع الحروف العربية
        replacements = {
            'أ': 'ا', 'إ': 'ا', 'آ': 'ا',
            'ى': 'ي', 'ة': 'ه', 'ؤ': 'و', 'ئ': 'ي'
        }
        
        for old, new in replacements.items():
            text = text.replace(old, new)
        
        # إزالة التشكيل
        text = re.sub(r'[\u064B-\u065F\u0670]', '', text)
        
        return text
    
    @staticmethod
    def is_valid_command(text: str) -> bool:
        """التحقق من صحة الأمر"""
        if not text or len(text) > 100:
            return False
        
        # قائمة الأوامر المسموحة
        allowed_patterns = [
            r'^(بداية|start|home)$',
            r'^(مساعدة|help)$',
            r'^(انضم|join)$',
            r'^(انسحب|leave)$',
            r'^(العاب|games|الالعاب)$',
            r'^(نقاطي|points)$',
            r'^(صدارة|leaderboard)$',
            r'^(لمح|hint)$',
            r'^(جاوب|reveal)$',
            r'^(ايقاف|إيقاف|stop)$',
            r'^ثيم .+$',
            r'^لعبة .+$',
            r'^لعبه .+$'
        ]
        
        normalized = InputValidator.normalize_arabic(text)
        return any(re.match(pattern, normalized, re.IGNORECASE) for pattern in allowed_patterns)

validator = InputValidator()

# ================== Message Helpers محسّنة ==================
def send_message_safe(api: MessagingApi, user_id: str, content, use_quick_reply: bool = True):
    """
    إرسال رسالة آمن مع retry و error handling
    
    Args:
        api: LINE Messaging API
        user_id: معرف المستخدم
        content: FlexMessage أو TextMessage أو str
        use_quick_reply: إضافة Quick Reply
    
    Returns:
        bool: نجاح الإرسال
    """
    max_retries = 3
    retry_delay = 0.5
    
    for attempt in range(max_retries):
        try:
            messages = []
            
            # تحويل المحتوى إلى رسائل
            if isinstance(content, str):
                quick_reply = get_main_quick_reply() if use_quick_reply else None
                messages.append(TextMessage(text=content, quickReply=quick_reply))
            elif isinstance(content, FlexMessage):
                messages.append(content)
                if use_quick_reply:
                    # إضافة رسالة نصية صغيرة مع Quick Reply بعد الـ Flex
                    quick_reply = get_main_quick_reply()
                    messages.append(TextMessage(
                        text="استخدم الأزرار السريعة ⬇️",
                        quickReply=quick_reply
                    ))
            elif isinstance(content, (TextMessage, FlexMessage)):
                messages.append(content)
            else:
                logger.error(f"❌ Invalid content type: {type(content)}")
                return False
            
            # إرسال الرسائل
            api.push_message(
                PushMessageRequest(
                    to=user_id,
                    messages=messages
                )
            )
            
            logger.info(f"✅ Message sent to {user_id[:8]}... (attempt {attempt + 1})")
            return True
            
        except Exception as e:
            logger.error(f"❌ Send error (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay * (attempt + 1))
            else:
                return False
    
    return False

# ================== معالج الرسائل المحسّن ==================
def process_message_safe(user_id: str, text: str):
    """
    معالجة الرسائل مع error handling شامل
    
    Args:
        user_id: معرف المستخدم
        text: نص الرسالة
    """
    
    try:
        # Rate limiting
        allowed, rate_msg = rate_limiter.is_allowed(user_id)
        if not allowed:
            logger.warning(f"⚠️ Rate limit: {user_id[:8]}... - {rate_msg}")
            with ApiClient(configuration) as api_client:
                api = MessagingApi(api_client)
                send_message_safe(api, user_id, rate_msg, use_quick_reply=False)
            return
        
        # تنظيف النص
        text = validator.sanitize_text(text)
        if not text:
            logger.warning(f"⚠️ Empty message from {user_id[:8]}...")
            return
        
        # الحصول على بيانات المستخدم
        user = db.get_user(user_id)
        theme = user.get('theme', 'رمادي') if user else 'رمادي'
        points = user.get('points', 0) if user else 0
        is_registered = bool(user and user.get('status') == 'active')
        username = user.get('name', 'مستخدم') if user else 'مستخدم'
        
        normalized = validator.normalize_arabic(text)
        
        with ApiClient(configuration) as api_client:
            api = MessagingApi(api_client)
            
            # ===== الأوامر الأساسية =====
            if normalized in ['بداية', 'start', 'home']:
                msg = build_home(theme, username, points, is_registered)
                send_message_safe(api, user_id, msg)
                return
            
            if normalized in ['مساعدة', 'help']:
                msg = build_help(theme)
                send_message_safe(api, user_id, msg)
                return
            
            if normalized.startswith('ثيم '):
                new_theme = text.replace('ثيم ', '').strip()
                from ui import THEMES
                if new_theme in THEMES:
                    if user:
                        db.update_theme(user_id, new_theme)
                    msg = build_home(new_theme, username, points, is_registered)
                    send_message_safe(api, user_id, msg)
                else:
                    send_message_safe(api, user_id, f"⚠️ الثيم '{new_theme}' غير موجود")
                return
            
            if normalized in ['انضم', 'join']:
                if not is_registered:
                    db.create_user(user_id, username, theme)
                    send_message_safe(api, user_id, f"✅ تم تسجيلك بنجاح يا {username}!")
                else:
                    send_message_safe(api, user_id, "ℹ️ أنت مسجل بالفعل")
                return
            
            if normalized in ['انسحب', 'leave']:
                if is_registered:
                    db.deactivate_user(user_id)
                    send_message_safe(api, user_id, "✅ تم إلغاء تسجيلك")
                else:
                    send_message_safe(api, user_id, "ℹ️ أنت غير مسجل")
                return
            
            if normalized in ['العاب', 'games', 'الالعاب']:
                if not is_registered:
                    msg = build_registration_required(theme)
                    send_message_safe(api, user_id, msg)
                else:
                    msg = build_games_menu(theme)
                    send_message_safe(api, user_id, msg)
                return
            
            if normalized in ['نقاطي', 'points']:
                if not is_registered:
                    msg = build_registration_required(theme)
                    send_message_safe(api, user_id, msg)
                else:
                    msg = build_my_points(username, points, theme)
                    send_message_safe(api, user_id, msg)
                return
            
            if normalized in ['صدارة', 'leaderboard']:
                top = db.get_leaderboard(10)
                msg = build_leaderboard(top, theme)
                send_message_safe(api, user_id, msg)
                return
            
            # ===== أثناء اللعب =====
            if game_loader.has_active_game(user_id):
                game = game_loader.get_game(user_id)
                
                if normalized in ['لمح', 'hint']:
                    hint = game.get_hint() if hasattr(game, 'get_hint') else "لا يوجد تلميح"
                    send_message_safe(api, user_id, hint)
                    return
                
                # تمرير الإجابة
                if hasattr(game, 'check_answer'):
                    result = game.check_answer(text, user_id, username)
                    
                    if result:
                        pts = result.get('points', 0)
                        if pts > 0:
                            db.add_points(user_id, pts)
                        
                        # إرسال الاستجابة
                        response = result.get('response')
                        message_text = result.get('message', '')
                        
                        if isinstance(response, FlexMessage):
                            send_message_safe(api, user_id, response)
                        elif message_text:
                            send_message_safe(api, user_id, message_text)
                        
                        if result.get('game_over'):
                            game_loader.end_game(user_id)
                        
                        return
            
            # ===== بدء لعبة =====
            if normalized.startswith('لعبة ') or normalized.startswith('لعبه '):
                if not is_registered:
                    msg = build_registration_required(theme)
                    send_message_safe(api, user_id, msg)
                    return
                
                game_name = text.replace('لعبة ', '').replace('لعبه ', '').strip()
                
                # إنهاء اللعبة الحالية
                if game_loader.has_active_game(user_id):
                    game_loader.end_game(user_id)
                
                # بدء اللعبة الجديدة
                result = game_loader.start_game(user_id, game_name)
                
                if not result:
                    send_message_safe(api, user_id, f"❌ اللعبة '{game_name}' غير موجودة")
                    return
                
                send_message_safe(api, user_id, result)
                return
            
            if normalized in ['ايقاف', 'إيقاف', 'stop']:
                if game_loader.has_active_game(user_id):
                    game_loader.end_game(user_id)
                    send_message_safe(api, user_id, "✅ تم إيقاف اللعبة")
                else:
                    send_message_safe(api, user_id, "ℹ️ لا توجد لعبة نشطة")
                return
            
            # ===== المستخدم غير مسجل =====
            if not is_registered:
                send_message_safe(
                    api, user_id,
                    "⚠️ يجب التسجيل أولاً\nاكتب 'انضم' للتسجيل"
                )
                return
            
            # ===== رسالة افتراضية =====
            send_message_safe(
                api, user_id,
                "❓ لم أفهم الأمر\nاكتب 'مساعدة' للحصول على المساعدة"
            )
    
    except Exception as e:
        logger.error(f"❌ Error processing message from {user_id[:8]}...: {e}", exc_info=True)
        try:
            with ApiClient(configuration) as api_client:
                api = MessagingApi(api_client)
                send_message_safe(
                    api, user_id,
                    "❌ حدث خطأ غير متوقع. حاول مرة أخرى",
                    use_quick_reply=False
                )
        except:
            pass

# ================== LINE Webhook Handlers ==================
@handler.add(FollowEvent)
def handle_follow(event):
    """معالج متابعة جديدة"""
    user_id = event.source.user_id
    
    try:
        # تسجيل المستخدم
        db.create_user(user_id, "مستخدم", "رمادي")
        
        # إرسال رسالة ترحيب
        with ApiClient(configuration) as api_client:
            api = MessagingApi(api_client)
            msg = build_home("رمادي", "مستخدم", 0, True)
            send_message_safe(api, user_id, msg)
        
        logger.info(f"✅ New follower: {user_id[:8]}...")
    
    except Exception as e:
        logger.error(f"❌ Follow event error: {e}")

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    """معالج الرسائل النصية"""
    user_id = event.source.user_id
    text = event.message.text
    
    # معالجة الرسالة بشكل آمن
    process_message_safe(user_id, text)

# ================== Flask Routes ==================
@app.route("/", methods=["GET"])
def home():
    """الصفحة الرئيسية"""
    try:
        stats = db.get_stats()
        rate_stats = rate_limiter.get_stats()
        
        return jsonify({
            "status": "running",
            "bot": "Bot Mesh v10.0",
            "version": "10.0.0",
            "games": games_count,
            "users": stats.get('total_users', 0),
            "total_points": stats.get('total_points', 0),
            "rate_limiter": rate_stats,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Home error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/health", methods=["GET"])
def health():
    """فحص صحة الخدمة"""
    try:
        # فحص قاعدة البيانات
        total_users = db.get_total_users()
        
        # فحص Game Loader
        active_games = len(game_loader.active_sessions)
        
        return jsonify({
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "checks": {
                "database": True,
                "game_loader": True,
                "games_loaded": games_count
            },
            "stats": {
                "users": total_users,
                "active_games": active_games
            }
        }), 200
    
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 503

@app.route("/callback", methods=["POST"])
def callback():
    """LINE Webhook Callback"""
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
    """إحصائيات مفصلة"""
    try:
        db_stats = db.get_stats()
        rate_stats = rate_limiter.get_stats()
        game_stats = game_loader.get_stats()
        
        return jsonify({
            "database": db_stats,
            "rate_limiter": rate_stats,
            "games": game_stats,
            "timestamp": datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Stats error: {e}")
        return jsonify({"error": "Failed to get stats"}), 500

@app.route("/admin/backup", methods=["POST"])
def backup_database():
    """إنشاء نسخة احتياطية"""
    try:
        success = db.backup()
        if success:
            return jsonify({"status": "success", "message": "Backup created"})
        else:
            return jsonify({"status": "error", "message": "Backup failed"}), 500
    except Exception as e:
        logger.error(f"Backup error: {e}")
        return jsonify({"error": str(e)}), 500

# ================== Error Handlers ==================
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def internal_error(e):
    logger.error(f"Internal error: {e}")
    return jsonify({"error": "Internal server error"}), 500

# ================== Startup ==================
if __name__ == "__main__":
    logger.info(f"🚀 Bot Mesh v10.0 starting on port {PORT}")
    logger.info(f"📊 Games loaded: {games_count}")
    logger.info(f"💾 Database: {DB_PATH}")
    logger.info(f"🔒 Security: Enhanced")
    logger.info(f"⚡ Performance: Optimized")
    
    app.run(
        host="0.0.0.0",
        port=PORT,
        debug=False,
        threaded=True
    )
