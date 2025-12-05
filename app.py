import os, sys, logging, threading, time, traceback
from datetime import datetime, timedelta
from collections import defaultdict
from flask import Flask, request, abort, jsonify
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import Configuration, ApiClient, MessagingApi, ReplyMessageRequest, TextMessage
from linebot.v3.webhooks import MessageEvent, TextMessageContent
from constants import (BOT_NAME, BOT_VERSION, BOT_RIGHTS, LINE_CHANNEL_SECRET, LINE_CHANNEL_ACCESS_TOKEN, 
                       validate_env, GAME_LIST, DEFAULT_THEME, PRIVACY_SETTINGS, 
                       is_allowed_command, GAME_COMMANDS, get_game_class_name)
from ui_builder import (build_games_menu, build_my_points, build_leaderboard, build_registration_status, 
                        build_winner_announcement, build_help_window, build_theme_selector, build_enhanced_home, 
                        attach_quick_reply, build_error_message, build_game_stopped, build_team_game_end, 
                        build_unregister_confirmation, build_registration_required)
from database import get_database

try:
    validate_env()
except Exception as e:
    print(f"Configuration error: {e}")
    sys.exit(1)

app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s-%(levelname)s-%(message)s')
logger = logging.getLogger("botmesh")
configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)
db = get_database()

active_games = {}
game_timers = {}
session_meta = {}
team_mode_state = {}
RATE_LIMIT = {"max_requests": 30, "window_seconds": 60}
user_rate = defaultdict(list)
session_locks = {}
session_lock_main = threading.Lock()


class LRUCache:
    def __init__(self, capacity=1000):
        self.cache = {}
        self.capacity = capacity
        self.order = []
        self.lock = threading.Lock()
    
    def get(self, key):
        with self.lock:
            if key in self.cache:
                self.order.remove(key)
                self.order.append(key)
                return self.cache[key]
            return None
    
    def put(self, key, value):
        with self.lock:
            if key in self.cache:
                self.order.remove(key)
            elif len(self.cache) >= self.capacity:
                oldest = self.order.pop(0)
                del self.cache[oldest]
            self.cache[key] = value
            self.order.append(key)
    
    def remove(self, key):
        with self.lock:
            if key in self.cache:
                del self.cache[key]
                self.order.remove(key)


user_cache = LRUCache(capacity=1000)


def get_session_lock(game_id):
    with session_lock_main:
        if game_id not in session_locks:
            session_locks[game_id] = threading.Lock()
        return session_locks[game_id]


def is_rate_limited(user_id):
    now = datetime.utcnow()
    window = timedelta(seconds=RATE_LIMIT["window_seconds"])
    user_rate[user_id] = [t for t in user_rate[user_id] if now - t < window]
    if len(user_rate[user_id]) >= RATE_LIMIT["max_requests"]:
        logger.warning(f"Rate limit exceeded for user: {user_id}")
        return True
    user_rate[user_id].append(now)
    return False


AVAILABLE_GAMES = {}
try:
    from games.iq_game import IqGame
    from games.math_game import MathGame
    from games.word_color_game import WordColorGame
    from games.scramble_word_game import ScrambleWordGame
    from games.fast_typing_game import FastTypingGame
    from games.opposite_game import OppositeGame
    from games.letters_words_game import LettersWordsGame
    from games.song_game import SongGame
    from games.human_animal_plant_game import HumanAnimalPlantGame
    from games.chain_words_game import ChainWordsGame
    from games.guess_game import GuessGame
    from games.compatibility_game import CompatibilitySystem
    
    AVAILABLE_GAMES = {
        "ذكاء": IqGame,
        "رياضيات": MathGame,
        "لون": WordColorGame,
        "ترتيب": ScrambleWordGame,
        "أسرع": FastTypingGame,
        "ضد": OppositeGame,
        "تكوين": LettersWordsGame,
        "أغنيه": SongGame,
        "لعبة": HumanAnimalPlantGame,
        "سلسلة": ChainWordsGame,
        "خمن": GuessGame,
        "توافق": CompatibilitySystem
    }
    logger.info(f"Loaded {len(AVAILABLE_GAMES)} games successfully")
except Exception as e:
    logger.error(f"Error loading games: {e}")
    logger.error(traceback.format_exc())


def ensure_session_meta(game_id):
    if game_id not in session_meta:
        session_meta[game_id] = {
            "session_id": None,
            "team_mode": False,
            "current_game_name": None,
            "session_type": "solo",
            "start_time": time.time()
        }
    return session_meta[game_id]


def launch_game_instance(game_id, owner_id, game_class_name, line_api, theme=None, team_mode=False, source_type="user"):
    if game_class_name not in AVAILABLE_GAMES:
        raise ValueError(f"Game not available: {game_class_name}")
    
    GameClass = AVAILABLE_GAMES[game_class_name]
    game_instance = GameClass(line_api)
    
    try:
        if hasattr(game_instance, 'set_theme') and theme:
            game_instance.set_theme(theme)
    except Exception as e:
        logger.error(f"Failed to set theme: {e}")
    
    try:
        if hasattr(game_instance, 'set_database'):
            game_instance.set_database(db)
        else:
            game_instance.db = db
    except Exception as e:
        logger.warning(f"Failed to link database: {e}")
    
    if team_mode:
        game_instance.team_mode = True
        game_instance.supports_hint = False
        game_instance.supports_reveal = False
        game_instance.session_type = "teams"
    else:
        game_instance.team_mode = False
        game_instance.session_type = "solo" if source_type == "user" else "group"
    
    active_games[game_id] = game_instance
    meta = ensure_session_meta(game_id)
    meta["current_game_name"] = game_class_name
    meta["team_mode"] = team_mode
    meta["session_type"] = game_instance.session_type
    
    if game_class_name != "توافق":
        session_id = db.create_game_session(
            owner_id, 
            game_class_name, 
            mode=game_instance.session_type, 
            team_mode=1 if team_mode else 0
        )
        meta["session_id"] = session_id
    
    logger.info(f"Launched game: {game_class_name} | Mode: {'teams' if team_mode else 'solo'}")
    return game_instance


def get_user_display_name(line_api, user_id):
    """
    الحصول على اسم المستخدم من LINE مع معالجة محسّنة للأخطاء
    """
    try:
        profile = line_api.get_profile(user_id)
        
        # محاولة الحصول على الاسم بطرق متعددة
        username = None
        
        # الطريقة 1: display_name attribute
        if hasattr(profile, 'display_name'):
            username = getattr(profile, 'display_name', None)
        
        # الطريقة 2: التحقق من الكائن كـ dictionary
        if not username and isinstance(profile, dict):
            username = profile.get('display_name') or profile.get('displayName')
        
        # الطريقة 3: محاولة تحويل الكائن لـ dict
        if not username:
            try:
                profile_dict = profile.to_dict() if hasattr(profile, 'to_dict') else vars(profile)
                username = profile_dict.get('display_name') or profile_dict.get('displayName')
            except:
                pass
        
        # التحقق من صحة الاسم
        if username:
            username = str(username).strip()
            # التحقق من أن الاسم ليس فارغاً أو مسافات فقط
            if username and len(username) > 0 and not username.isspace():
                logger.info(f"✓ Got username from LINE: {username[:20]}")
                return username[:50]  # حد أقصى 50 حرف
        
        logger.warning(f"⚠ LINE profile has no valid display_name for user: {user_id}")
        return "مستخدم"
        
    except AttributeError as e:
        logger.error(f"✗ AttributeError getting profile: {str(e)}")
        return "مستخدم"
    except Exception as e:
        logger.error(f"✗ Failed to get LINE profile: {type(e).__name__}: {str(e)[:100]}")
        return "مستخدم"


def get_user_data(line_api, user_id):
    """
    الحصول على بيانات المستخدم مع التحديث التلقائي للاسم
    """
    # التحقق من الكاش أولاً
    cached = user_cache.get(user_id)
    if cached:
        cache_time = cached.get('_cache_time', datetime.min)
        if datetime.utcnow() - cache_time < timedelta(minutes=PRIVACY_SETTINGS["cache_timeout_minutes"]):
            return cached
    
    # جلب من قاعدة البيانات
    user = db.get_user(user_id)
    
    if not user:
        # جلب الاسم من LINE للمستخدم الجديد
        username = get_user_display_name(line_api, user_id)
        db.create_user(user_id, username)
        user = db.get_user(user_id)
        logger.info(f"✓ New user created: {username[:20]}")
    else:
        # تحديث الاسم بشكل دوري (كل ساعة)
        last_update = user.get('last_activity', datetime.min)
        if isinstance(last_update, str):
            try:
                last_update = datetime.fromisoformat(last_update)
            except:
                last_update = datetime.min
        
        # تحديث الاسم إذا مر أكثر من ساعة
        if datetime.now() - last_update > timedelta(hours=1):
            fresh_username = get_user_display_name(line_api, user_id)
            if fresh_username != "مستخدم" and fresh_username != user.get('name'):
                # تحديث الاسم في قاعدة البيانات
                db.update_user_name(user_id, fresh_username)
                # تحديث وقت النشاط
                db.update_activity(user_id)
                
                # إزالة الكاش القديم
                user_cache.remove(user_id)
                
                # تحديث البيانات الحالية
                user['name'] = fresh_username
                user['last_activity'] = datetime.now()
                
                logger.info(f"✓ Updated username to: {fresh_username[:20]}")
    
    # تحديث الكاش
    user['_cache_time'] = datetime.utcnow()
    user_cache.put(user_id, user)
    return user


def handle_game_answer(game_id, result, user_id, meta):
    pts = result.get('points', 0)
    if pts > 0:
        if meta.get("team_mode"):
            team_name = result.get('team', 'team1')
            db.add_team_points(meta["session_id"], team_name, 1)
        else:
            db.add_points(user_id, 1)
            game_name = meta.get("current_game_name", "unknown")
            db.record_game_stat(user_id, game_name, 1, result.get('game_over', False))
    return pts


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        logger.warning("Invalid signature")
        abort(400)
    except Exception as e:
        logger.error(f"Handler error: {e}")
        logger.error(traceback.format_exc())
        abort(500)
    return "OK"


@app.route("/", methods=['GET'])
def status_page():
    stats = db.get_stats_summary()
    return f"""<html><head><title>{BOT_NAME}</title><style>body{{font-family:'Segoe UI',sans-serif;padding:40px;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);color:#fff;}}.container{{max-width:800px;margin:0 auto;background:rgba(255,255,255,0.95);padding:40px;border-radius:20px;box-shadow:0 20px 60px rgba(0,0,0,0.3);color:#333;}}h1{{color:#667eea;margin:0 0 10px;font-size:2.5em;}}.version{{color:#999;margin-bottom:30px;}}.stats{{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:20px;margin:30px 0;}}.stat-card{{background:#f8f9fa;padding:20px;border-radius:15px;text-align:center;border:2px solid #e9ecef;}}.stat-value{{font-size:2em;font-weight:bold;color:#667eea;margin:10px 0;}}.stat-label{{color:#666;font-size:0.9em;text-transform:uppercase;}}.footer{{margin-top:30px;padding-top:20px;border-top:2px solid #e9ecef;text-align:center;color:#999;font-size:0.85em;}}</style></head><body><div class="container"><h1>{BOT_NAME}</h1><div class="version">Version {BOT_VERSION}</div><div class="stats"><div class="stat-card"><div class="stat-label">Active Games</div><div class="stat-value">{len(active_games)}</div></div><div class="stat-card"><div class="stat-label">Available Games</div><div class="stat-value">{len(AVAILABLE_GAMES)}</div></div><div class="stat-card"><div class="stat-label">Total Users</div><div class="stat-value">{stats.get('total_users',0)}</div></div><div class="stat-card"><div class="stat-label">Registered Users</div><div class="stat-value">{stats.get('registered_users',0)}</div></div><div class="stat-card"><div class="stat-label">Total Sessions</div><div class="stat-value">{stats.get('total_sessions',0)}</div></div></div><div class="footer">{BOT_RIGHTS}</div></div></body></html>"""
