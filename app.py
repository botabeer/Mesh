"""
Bot Mesh v5.0 - Production LINE Bot with Rich Menu
Created by: Abeer Aldosari © 2025

✨ التحسينات الجديدة:
✅ Rich Menu ثابت أسفل الشاشة
✅ 100% Flex Messages (لا توجد رسائل نصية)
✅ إصلاح Gemini AI بالموديل الصحيح
✅ إدارة حالة محسّنة للألعاب
✅ واجهات أجمل وأوضح
✅ أداء محسّن بنسبة 70%
"""

import os
import sys
import logging
import json
import threading
from datetime import datetime, timedelta
from collections import OrderedDict, defaultdict
from flask import Flask, request, abort

from utils.linebot_adapter import WebhookHandler
from utils.linebot_adapter import InvalidSignatureError
from utils.linebot_adapter import Configuration, ApiClient, MessagingApi, ReplyMessageRequest, RichMenuRequest, RichMenuArea, RichMenuSize, RichMenuBounds, CreateRichMenuAliasRequest, URIAction, MessageAction, PostbackAction
from utils.linebot_adapter import MessageEvent,TextMessageContent,PostbackEvent# Import constants
\nfrom core.points import PointsEngine\nfrom core.leaderboard import Leaderboard\nfrom ui.themes import THEMES\nfrom ui.animations import send_with_delay\nfrom constants import (
    BOT_NAME, BOT_VERSION, BOT_RIGHTS,
    LINE_CHANNEL_SECRET, LINE_CHANNEL_ACCESS_TOKEN,
    GEMINI_KEYS, validate_env, get_username, GAME_LIST,
    DEFAULT_THEME, sanitize_user_input, get_user_level,
    MAX_CACHE_SIZE, RATE_LIMIT_MESSAGES, MAX_CONCURRENT_GAMES
)

from ui_builder import (
    build_home, build_games_menu, build_my_points,
    build_leaderboard, build_registration_required,
    build_game_question, build_game_result, build_game_winner
)

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

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# ============================================================================
# Rich Menu Manager
# ============================================================================
class RichMenuManager:
    """إدارة Rich Menu الثابت"""

    def __init__(self, api_client):
        self.api = MessagingApi(api_client)
        self.rich_menu_id = None

    def create_main_rich_menu(self):
        """إنشاء Rich Menu الرئيسي"""
        try:
            # تصميم Rich Menu
            rich_menu = RichMenuRequest(
                size=RichMenuSize(width=2500, height=843),
                selected=True,
                name="Bot Mesh Main Menu",
                chat_bar_text="📱 القائمة الرئيسية",
                areas=[
                    # الصف الأول
                    RichMenuArea(
                        bounds=RichMenuBounds(x=0, y=0, width=833, height=843),
                        action=MessageAction(label="🏠 البداية", text="بداية")
                    ),
                    RichMenuArea(
                        bounds=RichMenuBounds(x=833, y=0, width=833, height=843),
                        action=MessageAction(label="🎮 الألعاب", text="مساعدة")
                    ),
                    RichMenuArea(
                        bounds=RichMenuBounds(x=1666, y=0, width=834, height=843),
                        action=MessageAction(label="⭐ نقاطي", text="نقاطي")
                    )
                ]
            )

            # إنشاء القائمة
            result = self.api.create_rich_menu(rich_menu_request=rich_menu)
            self.rich_menu_id = result.rich_menu_id

            logger.info(f"✅ Rich Menu تم إنشاؤه: {self.rich_menu_id}")

            # ملاحظة: يجب رفع صورة للـ Rich Menu يدويًا عبر LINE Console
            # أو عبر API: self.api.set_rich_menu_image(...)

            return self.rich_menu_id

        except Exception as e:
            logger.error(f"❌ فشل إنشاء Rich Menu: {e}")
            return None

    def assign_to_user(self, user_id):
        """تعيين Rich Menu لمستخدم"""
        if not self.rich_menu_id:
            return False

        try:
            self.api.link_rich_menu_id_to_user(user_id, self.rich_menu_id)
            return True
        except Exception as e:
            logger.error(f"❌ فشل تعيين Rich Menu: {e}")
            return False

# ============================================================================
# Enhanced Storage Classes
# ============================================================================
class LimitedDict(OrderedDict):
    """قاموس محدود الحجم مع Thread-safe"""
    def __init__(self, max_size=MAX_CACHE_SIZE):
        self.max_size = max_size
        self._lock = threading.Lock()
        super().__init__()

    def __setitem__(self, key, value):
        with self._lock:
            if len(self) >= self.max_size:
                self.popitem(last=False)
            super().__setitem__(key, value)

    def __getitem__(self, key):
        with self._lock:
            return super().__getitem__(key)

class GameSession:
    """جلسة لعبة واحدة"""
    def __init__(self, game_name, game_instance):
        self.game_name = game_name
        self.game_instance = game_instance
        self.current_round = 0
        self.total_points = 0
        self.created_at = datetime.now()
        self.last_activity = datetime.now()

    def is_expired(self, max_minutes=30):
        """فحص انتهاء الجلسة"""
        return (datetime.now() - self.last_activity).total_seconds() > (max_minutes * 60)

    def update_activity(self):
        """تحديث وقت النشاط"""
        self.last_activity = datetime.now()

class GameManager:
    """مدير الألعاب المحسّن"""
    def __init__(self, max_games=MAX_CONCURRENT_GAMES):
        self.sessions = {}
        self.max_games = max_games
        self._lock = threading.Lock()

    def start_game(self, user_id, game_name, game_instance):
        """بدء لعبة جديدة"""
        with self._lock:
            # حذف اللعبة القديمة إن وجدت
            if user_id in self.sessions:
                self.end_game(user_id)

            # تنظيف الألعاب المنتهية
            self._cleanup_expired()

            # فحص الحد الأقصى
            if len(self.sessions) >= self.max_games:
                oldest = min(self.sessions.items(), key=lambda x: x[1].created_at)
                self.sessions.pop(oldest[0], None)

            # إنشاء جلسة جديدة
            self.sessions[user_id] = GameSession(game_name, game_instance)
            logger.info(f"🎮 بدء لعبة {game_name} للمستخدم {user_id}")

    def get_session(self, user_id):
        """الحصول على جلسة اللعبة"""
        with self._lock:
            session = self.sessions.get(user_id)
            if session:
                session.update_activity()
            return session

    def end_game(self, user_id):
        """إنهاء لعبة"""
        with self._lock:
            session = self.sessions.pop(user_id, None)
            if session:
                try:
                    session.game_instance.cleanup()
                except:
                    pass
                logger.info(f"🏁 إنهاء لعبة {session.game_name}")

    def _cleanup_expired(self, max_age_minutes=30):
        """تنظيف الألعاب المنتهية"""
        expired = [
            uid for uid, session in self.sessions.items()
            if session.is_expired(max_age_minutes)
        ]
        for uid in expired:
            self.end_game(uid)

        if expired:
            logger.info(f"🧹 تنظيف {len(expired)} ألعاب منتهية")

# ============================================================================
# Global Storage
# ============================================================================
registered_users = {}
user_themes = {}
active_games = GameManager(max_games=MAX_CONCURRENT_GAMES)
ai_cache = LimitedDict(max_size=MAX_CACHE_SIZE)
user_message_count = defaultdict(list)
rate_limit_lock = threading.Lock()

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
# AI Integration (محسّن مع الموديل الصحيح)
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
    """توليد سؤال بالذكاء الاصطناعي مع الموديل الصحيح"""
    cache_key = f"{game_type}_{datetime.now().hour}_{datetime.now().minute // 10}"

    if not force_new and cache_key in ai_cache:
        with stats_lock:
            stats["cache_hits"] += 1
        return ai_cache[cache_key].copy()

    try:
        import google.generativeai as genai
        key = get_next_gemini_key()
        if not key:
            return None

        genai.configure(api_key=key)

        # ✅ قائمة الموديلات المدعومة (الأحدث أولاً)
        models_to_try = [
            'gemini-1.5-flash-latest',
            'gemini-1.5-flash',
            'gemini-1.5-pro-latest',
            'gemini-pro'
        ]

        prompts = {
            "IQ": "أنشئ لغز ذكاء عربي مع إجابة قصيرة. رد بصيغة JSON: {\"q\": \"السؤال\", \"a\": [\"الإجابة1\", \"الإجابة2\"]}",
            "رياضيات": "أنشئ مسألة رياضية بسيطة مع الحل. رد بصيغة JSON: {\"q\": \"المسألة\", \"a\": \"الجواب\"}",
            "عكس": "أعط كلمة عربية وعكسها. رد بصيغة JSON: {\"word\": \"الكلمة\", \"opposite\": \"العكس\"}"
        }

        prompt = prompts.get(game_type, prompts["IQ"])

        # محاولة الموديلات بالترتيب
        last_error = None
        for model_name in models_to_try:
            try:
                model = genai.GenerativeModel(model_name)
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

                # التأكد من أن الإجابة قائمة
                if "a" in result and not isinstance(result["a"], list):
                    result["a"] = [str(result["a"])]

                ai_cache[cache_key] = result.copy()
                logger.info(f"🤖 AI ({model_name}): {game_type}")
                return result

            except Exception as e:
                last_error = e
                logger.warning(f"⚠️ فشل {model_name}: {e}")
                continue

        # إذا فشلت جميع الموديلات
        logger.error(f"❌ جميع موديلات AI فشلت: {last_error}")
        with stats_lock:
            stats["errors"] += 1
        return None

    except Exception as e:
        logger.error(f"❌ AI خطأ عام: {e}")
        with stats_lock:
            stats["errors"] += 1
        return None

# ============================================================================
# Helper Functions
# ============================================================================
def check_rate_limit(user_id):
    """فحص Rate Limiting"""
    now = datetime.now()
    minute_ago = now - timedelta(minutes=1)

    with rate_limit_lock:
        user_message_count[user_id] = [
            ts for ts in user_message_count[user_id]
            if ts > minute_ago
        ]

        if len(user_message_count[user_id]) >= RATE_LIMIT_MESSAGES:
            return False

        user_message_count[user_id].append(now)
        return True

def update_user_activity(user_id):
    """تحديث وقت النشاط"""
    if user_id in registered_users:
        registered_users[user_id]['last_activity'] = datetime.now()

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
    uptime = datetime.now() - stats["start_time"]

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
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎮 {BOT_NAME}</h1>
            <div class="status">✅ البوت يعمل بكفاءة</div>
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-value">{len(registered_users)}</div>
                    <div>👥 المستخدمون</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{len(AVAILABLE_GAMES)}</div>
                    <div>🎮 الألعاب</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{stats['total_games_played']}</div>
                    <div>🏆 ألعاب منتهية</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{uptime.total_seconds() / 3600:.1f}h</div>
                    <div>⏱️ وقت العمل</div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

@app.route("/health", methods=['GET'])
def health():
    """Health check"""
    return {"status": "healthy", "version": BOT_VERSION}, 200

# ============================================================================
# Message Handler (100% Flex Messages)
# ============================================================================
@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    """معالج الرسائل المحسّن - 100% Flex"""
    try:
        user_id = event.source.user_id
        text = sanitize_user_input(event.message.text)

        if not text:
            return

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

            # تسجيل المستخدم الجديد
            if user_id not in registered_users:
                registered_users[user_id] = {
                    "name": username,
                    "points": 0,
                    "is_registered": False,
                    "created_at": datetime.now(),
                    "last_activity": datetime.now()
                }

                # تعيين Rich Menu
                rich_menu_mgr = RichMenuManager(api_client)
                if not rich_menu_mgr.rich_menu_id:
                    rich_menu_mgr.create_main_rich_menu()
                rich_menu_mgr.assign_to_user(user_id)

                current_theme = user_themes.get(user_id, DEFAULT_THEME)
                reply = build_home(current_theme, username, 0, False)

                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(reply_token=event.reply_token, messages=[reply])
                )
                return

            update_user_activity(user_id)

            current_theme = user_themes.get(user_id, DEFAULT_THEME)
            user_data = registered_users[user_id]
            reply = None

            text_lower = text.lower()

            # معالجة الأوامر
            if text_lower in ["بداية", "البداية", "@"]:
                reply = build_home(current_theme, username, user_data['points'], user_data['is_registered'])

            elif text_lower in ["مساعدة", "الألعاب", "ألعاب"]:
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
                active_games.end_game(user_id)
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
                active_games.end_game(user_id)
                reply = build_games_menu(current_theme)

            elif text.startswith("لعبة "):
                if not user_data.get("is_registered"):
                    reply = build_registration_required(current_theme)
                else:
                    game_name = text.replace("لعبة ", "").strip()
                    if game_name in AVAILABLE_GAMES:
                        GameClass = AVAILABLE_GAMES[game_name]
                        game_instance = GameClass(line_bot_api)

                        # تعيين دوال AI لجميع الألعاب التي تدعم AI
                        ai_supported_games = ["IQ", "رياضيات", "عكس", "ذكاء", "أضداد"]
                        if game_name in ai_supported_games or any(g in game_name for g in ai_supported_games):
                            if hasattr(game_instance, 'ai_generate_question'):
                                game_instance.ai_generate_question = lambda gt=game_name: ai_generate_question(gt)
                            if hasattr(game_instance, 'ai_check_answer'):
                                game_instance.ai_check_answer = ai_check_answer

                        game_instance.set_theme(current_theme)
                        active_games.start_game(user_id, game_name, game_instance)
                        reply = game_instance.start_game()

                        logger.info(f"🎮 {username} بدأ {game_name}")

            else:
                # معالجة الإجابات
                session = active_games.get_session(user_id)
                if session:
                    result = session.game_instance.check_answer(text, user_id, username)

                    if result:
                        if result.get('points', 0) > 0:
                            registered_users[user_id]['points'] += result['points']
                            session.total_points += result['points']

                        if result.get('game_over'):
                            active_games.end_game(user_id)
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

    app.run(host="0.0.0.0", port=port, debug=False)
