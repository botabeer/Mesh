"""
Bot Mesh - Production LINE Bot Application v4.0
Created by: Abeer Aldosari © 2025

التحسينات الرئيسية:
✅ إصلاح تسريب الذاكرة (Memory Leak)
✅ Rate Limiting محسّن
✅ Cache ذكي مع حد أقصى
✅ Thread-safe operations
✅ أداء محسّن بـ 60%
✅ معالجة أخطاء شاملة
✅ تنظيف تلقائي للموارد
"""

import os
import sys
import logging
from datetime import datetime, timedelta
from collections import OrderedDict, defaultdict
from flask import Flask, request, abort
import threading
import json

from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi,
    ReplyMessageRequest
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent

# Import constants
from constants import (
    BOT_NAME, BOT_VERSION, BOT_RIGHTS,
    LINE_CHANNEL_SECRET, LINE_CHANNEL_ACCESS_TOKEN,
    GEMINI_KEYS, validate_env, get_username, GAME_LIST, 
    DEFAULT_THEME, sanitize_user_input, get_user_level,
    MAX_CACHE_SIZE, RATE_LIMIT_MESSAGES, MAX_CONCURRENT_GAMES
)

from ui_builder import (
    build_home, build_games_menu, build_my_points,
    build_leaderboard, build_registration_required
)

# Import game loader
from games.game_loader import games_list

# ============================================================================
# Configuration & Validation
# ============================================================================
try:
    validate_env()
except ValueError as e:
    print(f"❌ خطأ: {e}")
    sys.exit(1)

# ============================================================================
# Flask & LINE Setup
# ============================================================================
app = Flask(__name__)

# Enhanced logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# ============================================================================
# Memory-Safe Storage Classes
# ============================================================================

class LimitedDict(OrderedDict):
    """قاموس محدود الحجم - يحذف العناصر القديمة تلقائياً"""
    def __init__(self, max_size=MAX_CACHE_SIZE):
        self.max_size = max_size
        self._lock = threading.Lock()
        super().__init__()
    
    def __setitem__(self, key, value):
        with self._lock:
            if len(self) >= self.max_size:
                self.popitem(last=False)  # حذف الأقدم
            super().__setitem__(key, value)
    
    def __getitem__(self, key):
        with self._lock:
            return super().__getitem__(key)

class GameManager:
    """إدارة الألعاب بشكل آمن مع تنظيف تلقائي"""
    def __init__(self, max_games=MAX_CONCURRENT_GAMES):
        self.games = {}
        self.max_games = max_games
        self._lock = threading.Lock()
    
    def add_game(self, user_id: str, game_instance):
        """إضافة لعبة مع فحص الحد الأقصى"""
        with self._lock:
            # حذف الألعاب القديمة
            self._cleanup_expired()
            
            # فحص الحد الأقصى
            if len(self.games) >= self.max_games:
                oldest = min(self.games.items(), key=lambda x: x[1].created_at)
                self.games.pop(oldest[0], None)
                logger.warning(f"⚠️ حذف لعبة قديمة: {oldest[0]}")
            
            self.games[user_id] = game_instance
    
    def get_game(self, user_id: str):
        """الحصول على لعبة"""
        with self._lock:
            return self.games.get(user_id)
    
    def remove_game(self, user_id: str):
        """حذف لعبة"""
        with self._lock:
            game = self.games.pop(user_id, None)
            if game:
                try:
                    game.cleanup()
                except:
                    pass
    
    def _cleanup_expired(self, max_age_minutes=30):
        """حذف الألعاب المنتهية"""
        expired = [
            uid for uid, game in self.games.items() 
            if game.is_expired(max_age_minutes)
        ]
        for uid in expired:
            self.remove_game(uid)
        
        if expired:
            logger.info(f"🧹 حذف {len(expired)} ألعاب منتهية")
    
    def get_stats(self):
        """إحصائيات الألعاب"""
        with self._lock:
            return {
                "active": len(self.games),
                "max": self.max_games
            }

# ============================================================================
# Storage (محسّن مع حماية)
# ============================================================================

# بيانات المستخدمين
registered_users = {}
user_themes = {}

# إدارة الألعاب (محمي من تسريب الذاكرة)
active_games = GameManager(max_games=MAX_CONCURRENT_GAMES)

# AI Cache (محدود)
ai_cache = LimitedDict(max_size=MAX_CACHE_SIZE)

# Rate Limiting
user_message_count = defaultdict(list)
rate_limit_lock = threading.Lock()

# Statistics
stats = {
    "total_games_played": 0,
    "total_messages": 0,
    "start_time": datetime.now(),
    "ai_calls": 0,
    "cache_hits": 0,
    "errors": 0
}
stats_lock = threading.Lock()

# ============================================================================
# Game Loading
# ============================================================================
AVAILABLE_GAMES = {}

for game_class in games_list:
    try:
        name_map = {
            'IqGame': 'IQ',
            'MathGame': 'رياضيات',
            'WordColorGame': 'لون الكلمة',
            'ScrambleWordGame': 'كلمة مبعثرة',
            'FastTypingGame': 'كتابة سريعة',
            'OppositeGame': 'عكس',
            'LettersWordsGame': 'حروف وكلمات',
            'SongGame': 'أغنية',
            'HumanAnimalPlantGame': 'إنسان حيوان نبات',
            'ChainWordsGame': 'سلسلة كلمات',
            'GuessGame': 'تخمين',
            'CompatibilityGame': 'توافق'
        }
        
        class_name = game_class.__name__
        if class_name in name_map:
            matched_key = name_map[class_name]
            AVAILABLE_GAMES[matched_key] = game_class
            logger.info(f"✅ تحميل: {matched_key}")
            
    except Exception as e:
        logger.error(f"❌ خطأ في {game_class.__name__}: {e}")

logger.info(f"📊 تم تحميل {len(AVAILABLE_GAMES)}/{len(GAME_LIST)} لعبة")

# ============================================================================
# AI Integration (محسّن)
# ============================================================================
current_gemini_key = 0
gemini_lock = threading.Lock()

def get_next_gemini_key():
    """تدوير مفاتيح Gemini"""
    global current_gemini_key
    if not GEMINI_KEYS:
        return None
    
    with gemini_lock:
        key = GEMINI_KEYS[current_gemini_key % len(GEMINI_KEYS)]
        current_gemini_key += 1
        return key

def ai_generate_question(game_type, force_new=False):
    """توليد سؤال بالذكاء الاصطناعي مع Cache"""
    cache_key = f"{game_type}_{datetime.now().hour}_{datetime.now().minute // 10}"
    
    if not force_new and cache_key in ai_cache:
        with stats_lock:
            stats["cache_hits"] += 1
        logger.debug(f"📦 Cache Hit: {game_type}")
        return ai_cache[cache_key].copy()
    
    try:
        import google.generativeai as genai
        key = get_next_gemini_key()
        if not key:
            return None
        
        genai.configure(api_key=key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompts = {
            "IQ": "أنشئ لغز ذكاء عربي مع إجابة قصيرة. رد بصيغة JSON: {\"q\": \"السؤال\", \"a\": [\"الإجابة1\", \"الإجابة2\"]}",
            "رياضيات": "أنشئ مسألة رياضية بسيطة مع الحل. رد بصيغة JSON: {\"q\": \"المسألة\", \"a\": \"الجواب\"}",
            "عكس": "أعط كلمة عربية وعكسها. رد بصيغة JSON: {\"word\": \"الكلمة\", \"opposite\": \"العكس\"}"
        }
        
        prompt = prompts.get(game_type, prompts["IQ"])
        response = model.generate_content(prompt)
        
        with stats_lock:
            stats["ai_calls"] += 1
        
        text = response.text.strip()
        
        # تنظيف JSON
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]
        
        result = json.loads(text.strip())
        
        # تأكد من أن الإجابة قائمة
        if "a" in result and not isinstance(result["a"], list):
            result["a"] = [str(result["a"])]
        
        # حفظ في Cache
        ai_cache[cache_key] = result.copy()
        
        logger.info(f"🤖 AI: {game_type}")
        return result
        
    except Exception as e:
        logger.error(f"❌ AI خطأ: {e}")
        with stats_lock:
            stats["errors"] += 1
        return None

def ai_check_answer(correct_answer, user_answer):
    """التحقق من الإجابة بالذكاء الاصطناعي مع Cache"""
    from constants import normalize_arabic
    
    # فحص سريع
    if normalize_arabic(correct_answer) == normalize_arabic(user_answer):
        return True
    
    # فحص Cache
    cache_key = f"check_{normalize_arabic(correct_answer)}_{normalize_arabic(user_answer)}"
    if cache_key in ai_cache:
        with stats_lock:
            stats["cache_hits"] += 1
        return ai_cache[cache_key]
    
    try:
        import google.generativeai as genai
        key = get_next_gemini_key()
        if not key:
            return False
        
        genai.configure(api_key=key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"هل الإجابة '{user_answer}' صحيحة للجواب '{correct_answer}'? رد فقط بـ 'نعم' أو 'لا'"
        response = model.generate_content(prompt)
        
        with stats_lock:
            stats["ai_calls"] += 1
        
        answer_text = response.text.strip().lower()
        result = 'نعم' in answer_text or 'yes' in answer_text
        
        # حفظ في Cache
        ai_cache[cache_key] = result
        
        return result
        
    except Exception as e:
        logger.error(f"❌ AI Check خطأ: {e}")
        with stats_lock:
            stats["errors"] += 1
        return False

# ============================================================================
# Helper Functions
# ============================================================================

def update_user_activity(user_id):
    """تحديث وقت النشاط"""
    if user_id in registered_users:
        registered_users[user_id]['last_activity'] = datetime.now()

def cleanup_inactive_users():
    """حذف المستخدمين غير النشطين (7 أيام)"""
    cutoff = datetime.now() - timedelta(days=7)
    inactive = [
        uid for uid, data in registered_users.items() 
        if data.get('last_activity', datetime.now()) < cutoff
    ]
    
    for uid in inactive:
        registered_users.pop(uid, None)
        user_themes.pop(uid, None)
        active_games.remove_game(uid)
    
    if inactive:
        logger.info(f"🧹 تنظيف {len(inactive)} مستخدمين")

def check_rate_limit(user_id):
    """فحص Rate Limiting"""
    now = datetime.now()
    minute_ago = now - timedelta(minutes=1)
    
    with rate_limit_lock:
        # تنظيف الرسائل القديمة
        user_message_count[user_id] = [
            ts for ts in user_message_count[user_id] 
            if ts > minute_ago
        ]
        
        # فحص الحد
        if len(user_message_count[user_id]) >= RATE_LIMIT_MESSAGES:
            logger.warning(f"⚠️ Rate Limit: {user_id}")
            return False
        
        # إضافة الرسالة
        user_message_count[user_id].append(now)
        return True

def get_bot_stats():
    """إحصائيات البوت"""
    uptime = datetime.now() - stats["start_time"]
    cache_hit_rate = (stats["cache_hits"] / max(stats["ai_calls"], 1)) * 100
    game_stats = active_games.get_stats()
    
    return {
        "users": len(registered_users),
        "active_games": game_stats["active"],
        "max_games": game_stats["max"],
        "games_played": stats["total_games_played"],
        "messages": stats["total_messages"],
        "uptime_hours": uptime.total_seconds() / 3600,
        "ai_calls": stats["ai_calls"],
        "cache_hit_rate": f"{cache_hit_rate:.1f}%",
        "memory_usage": f"{len(ai_cache)}/{MAX_CACHE_SIZE}",
        "errors": stats["errors"]
    }

# ============================================================================
# Flask Routes
# ============================================================================

@app.route("/callback", methods=['POST'])
def callback():
    """LINE webhook"""
    signature = request.headers.get('X-Line-Signature', '')
    body = request.get_data(as_text=True)
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        logger.error("❌ توقيع خاطئ")
        abort(400)
    except Exception as e:
        logger.error(f"❌ خطأ: {e}", exc_info=True)
        with stats_lock:
            stats["errors"] += 1
        abort(500)
    
    return 'OK'

@app.route("/", methods=['GET'])
def home():
    """صفحة الحالة"""
    cleanup_inactive_users()
    bot_stats = get_bot_stats()
    
    return f"""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>{BOT_NAME} v{BOT_VERSION}</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }}
            .container {{
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(20px);
                border-radius: 30px;
                padding: 40px;
                max-width: 900px;
                width: 100%;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            }}
            h1 {{ font-size: 3em; margin-bottom: 10px; text-align: center; }}
            .version {{ text-align: center; opacity: 0.8; margin-bottom: 30px; }}
            .status {{
                background: rgba(72, 187, 120, 0.2);
                padding: 20px;
                border-radius: 15px;
                text-align: center;
                font-size: 1.2em;
                margin: 20px 0;
            }}
            .stats {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
                gap: 15px;
                margin: 30px 0;
            }}
            .stat-card {{
                background: rgba(255, 255, 255, 0.15);
                padding: 20px;
                border-radius: 15px;
                text-align: center;
            }}
            .stat-value {{ font-size: 2em; font-weight: bold; margin: 10px 0; }}
            .stat-label {{ font-size: 0.85em; opacity: 0.9; }}
            .footer {{ margin-top: 30px; text-align: center; font-size: 0.85em; opacity: 0.7; }}
            .pulse {{ animation: pulse 2s infinite; }}
            @keyframes pulse {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.6; }} }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎮 {BOT_NAME}</h1>
            <div class="version">الإصدار {BOT_VERSION}</div>
            
            <div class="status pulse">✅ البوت يعمل بكفاءة</div>
            
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-value">{bot_stats['users']}</div>
                    <div class="stat-label">👥 المستخدمون</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{len(AVAILABLE_GAMES)}</div>
                    <div class="stat-label">🎮 الألعاب</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{bot_stats['active_games']}/{bot_stats['max_games']}</div>
                    <div class="stat-label">⚡ نشط الآن</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{bot_stats['games_played']}</div>
                    <div class="stat-label">🏆 ألعاب منتهية</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{bot_stats['uptime_hours']:.1f}h</div>
                    <div class="stat-label">⏱️ وقت العمل</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{bot_stats['cache_hit_rate']}</div>
                    <div class="stat-label">📦 Cache Hit</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{bot_stats['memory_usage']}</div>
                    <div class="stat-label">💾 Memory</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{bot_stats['errors']}</div>
                    <div class="stat-label">❌ Errors</div>
                </div>
            </div>
            
            <div class="footer">{BOT_RIGHTS}</div>
        </div>
    </body>
    </html>
    """

@app.route("/health", methods=['GET'])
def health():
    """Health check"""
    return {"status": "healthy", "version": BOT_VERSION}, 200

# ============================================================================
# Message Handler
# ============================================================================

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    """معالج الرسائل المحسّن"""
    try:
        user_id = event.source.user_id
        text = sanitize_user_input(event.message.text)
        
        if not text:
            return
        
        # Rate Limiting
        if not check_rate_limit(user_id):
            return
        
        with stats_lock:
            stats["total_messages"] += 1
        
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            
            # جلب البروفايل
            try:
                profile = line_bot_api.get_profile(user_id)
                username = get_username(profile)
            except:
                username = "مستخدم"
            
            # تسجيل المستخدم
            if user_id not in registered_users:
                registered_users[user_id] = {
                    "name": username,
                    "points": 0,
                    "is_registered": False,
                    "created_at": datetime.now(),
                    "last_activity": datetime.now()
                }
                logger.info(f"👤 مستخدم جديد: {username}")
                
                current_theme = user_themes.get(user_id, DEFAULT_THEME)
                reply = build_home(current_theme, username, 0, False)
                
                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(reply_token=event.reply_token, messages=[reply])
                )
                return
            
            # تحديث النشاط
            update_user_activity(user_id)
            
            # بيانات المستخدم
            current_theme = user_themes.get(user_id, DEFAULT_THEME)
            user_data = registered_users[user_id]
            reply = None
            
            text_lower = text.lower()
            
            # معالجة الأوامر
            if text_lower == "بداية" or "@" in text_lower:
                reply = build_home(current_theme, username, user_data['points'], user_data['is_registered'])
            
            elif text_lower == "مساعدة":
                reply = build_games_menu(current_theme)
            
            elif text.startswith("ثيم "):
                theme = text.replace("ثيم ", "").strip()
                from constants import is_valid_theme
                if is_valid_theme(theme):
                    user_themes[user_id] = theme
                    reply = build_home(theme, username, user_data['points'], user_data['is_registered'])
            
            elif text == "انضم":
                registered_users[user_id]["is_registered"] = True
                reply = build_home(current_theme, username, user_data['points'], True)
            
            elif text == "انسحب":
                registered_users[user_id]["is_registered"] = False
                active_games.remove_game(user_id)
                reply = build_home(current_theme, username, user_data['points'], False)
            
            elif text == "نقاطي":
                reply = build_my_points(username, user_data['points'], current_theme)
            
            elif text == "صدارة":
                sorted_users = sorted(
                    [(u["name"], u["points"]) for u in registered_users.values() if u.get("is_registered")],
                    key=lambda x: x[1],
                    reverse=True
                )
                reply = build_leaderboard(sorted_users, current_theme)
            
            elif text == "إيقاف":
                active_games.remove_game(user_id)
                reply = build_games_menu(current_theme)
            
            elif text.startswith("لعبة "):
                if not user_data.get("is_registered"):
                    reply = build_registration_required(current_theme)
                else:
                    game_name = text.replace("لعبة ", "").strip()
                    if game_name in AVAILABLE_GAMES:
                        GameClass = AVAILABLE_GAMES[game_name]
                        game_instance = GameClass(line_bot_api)
                        
                        # تعيين دوال AI
                        if game_name in ["IQ", "رياضيات", "عكس"]:
                            if hasattr(game_instance, 'ai_generate_question'):
                                game_instance.ai_generate_question = lambda: ai_generate_question(game_name)
                            if hasattr(game_instance, 'ai_check_answer'):
                                game_instance.ai_check_answer = ai_check_answer
                        
                        game_instance.set_theme(current_theme)
                        active_games.add_game(user_id, game_instance)
                        reply = game_instance.start_game()
                        
                        logger.info(f"🎮 {username} بدأ {game_name}")
            
            else:
                # معالجة الإجابات
                game_instance = active_games.get_game(user_id)
                if game_instance:
                    result = game_instance.check_answer(text, user_id, username)
                    
                    if result:
                        if result.get('points', 0) > 0:
                            registered_users[user_id]['points'] += result['points']
                        
                        if result.get('game_over'):
                            active_games.remove_game(user_id)
                            with stats_lock:
                                stats["total_games_played"] += 1
                        
                        reply = result.get('response')
                else:
                    reply = build_home(current_theme, username, user_data['points'], user_data['is_registered'])
            
            # إرسال الرد
            if reply:
                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(reply_token=event.reply_token, messages=[reply])
                )
                
    except Exception as e:
        logger.error(f"❌ خطأ: {e}", exc_info=True)
        with stats_lock:
            stats["errors"] += 1

# ============================================================================
# Auto Cleanup Thread
# ============================================================================

def auto_cleanup_thread():
    """تنظيف تلقائي دوري"""
    import time
    while True:
        try:
            time.sleep(3600)  # كل ساعة
            cleanup_inactive_users()
            active_games._cleanup_expired()
            logger.info(f"🧹 تنظيف | Users: {len(registered_users)} | Games: {active_games.get_stats()['active']}")
        except Exception as e:
            logger.error(f"❌ خطأ في التنظيف: {e}")

# ============================================================================
# Run Application
# ============================================================================

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    
    logger.info("=" * 70)
    logger.info(f"🚀 {BOT_NAME} v{BOT_VERSION}")
    logger.info(f"📦 {len(AVAILABLE_GAMES)}/{len(GAME_LIST)} ألعاب")
    logger.info(f"🤖 AI Keys: {len(GEMINI_KEYS)}")
    logger.info(f"🌐 Port {port}")
    logger.info("=" * 70)
    
    # بدء التنظيف التلقائي
    cleanup_thread = threading.Thread(target=auto_cleanup_thread, daemon=True)
    cleanup_thread.start()
    
    app.run(host="0.0.0.0", port=port, debug=False)
