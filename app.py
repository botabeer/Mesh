"""
LINE Gaming Bot - Enhanced, Beautiful & User-Friendly Version
تحسينات: أمان - أداء - جماليات - سهولة استخدام
"""
from flask import Flask, request, abort, jsonify
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage, QuickReply, QuickReplyButton, MessageAction
import os, sqlite3, threading, time, logging, signal, importlib
from datetime import datetime, timedelta
from functools import wraps
from contextlib import contextmanager
from collections import defaultdict
import random

# ============================================
# 🎨 Logging Configuration
# ============================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.handlers.RotatingFileHandler('bot.log', maxBytes=10*1024*1024, backupCount=5)
    ]
)
logger = logging.getLogger(__name__)

# ============================================
# 🎮 Dynamic Games Loading System
# ============================================
GAMES_FOLDER = "games"
GAMES_LOADED = {}

def snake_to_camel(name):
    """تحويل snake_case إلى CamelCase"""
    return "".join(word.capitalize() for word in name.split("_"))

def load_games_dynamically():
    """تحميل جميع الألعاب من مجلد games تلقائياً"""
    games_loaded = {}
    
    # التحقق من وجود المجلد
    if not os.path.exists(GAMES_FOLDER):
        logger.warning(f"⚠️ Games folder '{GAMES_FOLDER}' not found")
        return games_loaded
    
    logger.info(f"🔍 Scanning games folder: {GAMES_FOLDER}")
    
    # قراءة كل ملفات Python في مجلد الألعاب
    try:
        for filename in os.listdir(GAMES_FOLDER):
            if filename.endswith(".py") and filename != "__init__.py":
                module_name = filename[:-3]  # إزالة .py
                class_name = snake_to_camel(module_name)
                
                try:
                    module_path = f"{GAMES_FOLDER}.{module_name}"
                    module = importlib.import_module(module_path)
                    
                    # محاولة الحصول على الكلاس من الموديل
                    game_class = getattr(module, class_name, None)
                    
                    if game_class:
                        games_loaded[class_name] = game_class
                        logger.info(f"✅ {class_name} loaded successfully")
                    else:
                        logger.warning(f"⚠️ {class_name} not found in {filename}")
                        
                except ImportError as e:
                    logger.warning(f"⚠️ Import error for {class_name}: {e}")
                except Exception as e:
                    logger.error(f"❌ Error loading {class_name}: {e}")
    
    except Exception as e:
        logger.error(f"❌ Error reading games folder: {e}")
    
    logger.info(f"📊 Total games loaded: {len(games_loaded)}")
    return games_loaded

# تحميل الألعاب تلقائياً
GAMES_LOADED = load_games_dynamically()

# ============================================
# 🎯 Game Name Mapping (for Arabic commands)
# ============================================
GAME_NAME_MAP = {
    'ذكاء': 'IQGame',
    'لون': 'WordColorGame',
    'سلسلة': 'ChainWordsGame',
    'ترتيب': 'ScrambleWordGame',
    'تكوين': 'LettersWordsGame',
    'أسرع': 'FastTypingGame',
    'لعبة': 'HumanAnimalPlantGame',
    'خمن': 'GuessGame',
    'توافق': 'CompatibilityGame',
    'رياضيات': 'MathGame',
    'ذاكرة': 'MemoryGame',
    'لغز': 'RiddleGame',
    'ضد': 'OppositeGame',
    'إيموجي': 'EmojiGame',
    'أغنية': 'SongGame'
}

# خريطة الألعاب مع بياناتها الجمالية
GAMES_UI_DATA = [
    {"arabic": "ذكاء", "class": "IQGame", "emoji": "🧠", "desc": "اختبر ذكاءك", "color": "#8b5cf6"},
    {"arabic": "لون", "class": "WordColorGame", "emoji": "🎨", "desc": "كلمة ولون", "color": "#ec4899"},
    {"arabic": "سلسلة", "class": "ChainWordsGame", "emoji": "⛓️", "desc": "سلسلة الكلمات", "color": "#3b82f6"},
    {"arabic": "ترتيب", "class": "ScrambleWordGame", "emoji": "🔤", "desc": "رتب الحروف", "color": "#10b981"},
    {"arabic": "تكوين", "class": "LettersWordsGame", "emoji": "✍️", "desc": "كون كلمات", "color": "#f59e0b"},
    {"arabic": "أسرع", "class": "FastTypingGame", "emoji": "⚡", "desc": "اكتب بسرعة", "color": "#ef4444"},
    {"arabic": "لعبة", "class": "HumanAnimalPlantGame", "emoji": "🎯", "desc": "إنسان حيوان نبات", "color": "#06b6d4"},
    {"arabic": "خمن", "class": "GuessGame", "emoji": "🤔", "desc": "خمن الرقم", "color": "#6366f1"},
    {"arabic": "توافق", "class": "CompatibilityGame", "emoji": "💖", "desc": "نسبة التوافق", "color": "#f472b6"},
    {"arabic": "رياضيات", "class": "MathGame", "emoji": "🔢", "desc": "حل المسائل", "color": "#8b5cf6"},
    {"arabic": "ذاكرة", "class": "MemoryGame", "emoji": "🧩", "desc": "اختبر ذاكرتك", "color": "#14b8a6"},
    {"arabic": "لغز", "class": "RiddleGame", "emoji": "🎭", "desc": "حل الألغاز", "color": "#f97316"},
    {"arabic": "ضد", "class": "OppositeGame", "emoji": "↔️", "desc": "الأضداد", "color": "#a855f7"},
    {"arabic": "إيموجي", "class": "EmojiGame", "emoji": "😀", "desc": "خمن الإيموجي", "color": "#fbbf24"},
    {"arabic": "أغنية", "class": "SongGame", "emoji": "🎵", "desc": "خمن الأغنية", "color": "#ec4899"}
]

# تصفية الألعاب المتاحة فقط
AVAILABLE_GAMES_UI = [game for game in GAMES_UI_DATA if game["class"] in GAMES_LOADED]
logger.info(f"🎮 Available games for UI: {len(AVAILABLE_GAMES_UI)}")

# ============================================
# ⚙️ Configuration
# ============================================
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024

LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', 'YOUR_TOKEN')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET', 'YOUR_SECRET')
BOT_NAME = os.getenv('BOT_NAME', 'بوت الألعاب')
DB_NAME = os.getenv('DB_NAME', 'game_scores.db')

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

GEMINI_API_KEYS = [k for k in [os.getenv(f'GEMINI_API_KEY_{i}', '') for i in range(1, 4)] if k]
current_gemini_key_index = 0
USE_AI = bool(GEMINI_API_KEYS)

def get_gemini_api_key():
    return GEMINI_API_KEYS[current_gemini_key_index] if GEMINI_API_KEYS else None

def switch_gemini_key():
    global current_gemini_key_index
    if len(GEMINI_API_KEYS) > 1:
        current_gemini_key_index = (current_gemini_key_index + 1) % len(GEMINI_API_KEYS)
        return True
    return False

# ============================================
# 📊 Metrics & Monitoring
# ============================================
class Metrics:
    def __init__(self):
        self.requests = 0
        self.errors = 0
        self.games_started = 0
        self.db_queries = 0
        self.cache_hits = 0
        self.cache_misses = 0
        self.lock = threading.Lock()
        self.start_time = datetime.now()
    
    def increment(self, metric, value=1):
        with self.lock:
            setattr(self, metric, getattr(self, metric, 0) + value)
    
    def get_stats(self):
        with self.lock:
            uptime = (datetime.now() - self.start_time).total_seconds()
            return {
                'requests': self.requests, 'errors': self.errors,
                'games_started': self.games_started, 'db_queries': self.db_queries,
                'cache_hits': self.cache_hits, 'cache_misses': self.cache_misses,
                'uptime_seconds': uptime,
                'requests_per_second': self.requests / uptime if uptime > 0 else 0
            }

metrics = Metrics()

# ============================================
# 💾 Cache System
# ============================================
class TTLCache:
    def __init__(self, ttl_seconds=60, max_size=1000):
        self.cache = {}
        self.ttl = ttl_seconds
        self.max_size = max_size
        self.lock = threading.Lock()
    
    def get(self, key):
        with self.lock:
            if key in self.cache:
                value, timestamp = self.cache[key]
                if datetime.now() - timestamp < timedelta(seconds=self.ttl):
                    metrics.increment('cache_hits')
                    return value
                del self.cache[key]
            metrics.increment('cache_misses')
        return None
    
    def set(self, key, value):
        with self.lock:
            if len(self.cache) >= self.max_size:
                oldest = min(self.cache.items(), key=lambda x: x[1][1])
                del self.cache[oldest[0]]
            self.cache[key] = (value, datetime.now())
    
    def clear(self):
        with self.lock:
            self.cache.clear()

user_stats_cache = TTLCache(ttl_seconds=60)
leaderboard_cache = TTLCache(ttl_seconds=300)

# ============================================
# 🗄️ Database Connection Pool
# ============================================
class ConnectionPool:
    def __init__(self, db_name, max_connections=10):
        self.db_name = db_name
        self.pool = []
        self.max_connections = max_connections
        self.lock = threading.Lock()
    
    @contextmanager
    def get_connection(self):
        conn = None
        try:
            with self.lock:
                if self.pool:
                    conn = self.pool.pop()
                else:
                    conn = sqlite3.connect(self.db_name, check_same_thread=False, timeout=10)
                    conn.row_factory = sqlite3.Row
                    conn.execute('PRAGMA journal_mode=WAL')
            yield conn
            conn.commit()
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"❌ Database error: {e}")
            raise
        finally:
            if conn:
                with self.lock:
                    if len(self.pool) < self.max_connections:
                        self.pool.append(conn)
                    else:
                        conn.close()

db_pool = ConnectionPool(DB_NAME)

def init_db():
    try:
        with db_pool.get_connection() as conn:
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY, display_name TEXT NOT NULL,
                line_display_name TEXT, total_points INTEGER DEFAULT 0,
                games_played INTEGER DEFAULT 0, wins INTEGER DEFAULT 0,
                last_played TEXT, registered_at TEXT DEFAULT CURRENT_TIMESTAMP,
                last_updated TEXT DEFAULT CURRENT_TIMESTAMP)''')
            
            c.execute('''CREATE TABLE IF NOT EXISTS game_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT NOT NULL,
                game_type TEXT NOT NULL, points INTEGER NOT NULL,
                won INTEGER DEFAULT 0, played_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE)''')
            
            c.execute('''CREATE TABLE IF NOT EXISTS name_updates (
                id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT NOT NULL,
                old_name TEXT, new_name TEXT, updated_at TEXT DEFAULT CURRENT_TIMESTAMP)''')
            
            c.execute('CREATE INDEX IF NOT EXISTS idx_user_points ON users(total_points DESC)')
            c.execute('CREATE INDEX IF NOT EXISTS idx_game_history_user ON game_history(user_id, played_at)')
        
        logger.info("✅ Database ready")
    except Exception as e:
        logger.error(f"❌ Database init failed: {e}")
        raise

init_db()

# ============================================
# 🚦 Rate Limiting
# ============================================
class RateLimiter:
    def __init__(self, max_requests=100, window_seconds=60):
        self.max_requests = max_requests
        self.window = window_seconds
        self.requests = defaultdict(list)
        self.lock = threading.Lock()
    
    def is_allowed(self, key):
        now = time.time()
        with self.lock:
            self.requests[key] = [t for t in self.requests[key] if now - t < self.window]
            if len(self.requests[key]) >= self.max_requests:
                return False
            self.requests[key].append(now)
            return True

rate_limiter = RateLimiter()

# ============================================
# 🎮 Game Manager
# ============================================
class GameManager:
    def __init__(self):
        self.active_games = {}
        self.registered_players = set()
        self.lock = threading.Lock()
    
    def is_registered(self, user_id):
        with self.lock:
            return user_id in self.registered_players
    
    def register_player(self, user_id):
        with self.lock:
            self.registered_players.add(user_id)
    
    def unregister_player(self, user_id):
        with self.lock:
            self.registered_players.discard(user_id)
    
    def create_game(self, game_id, game_obj, game_type):
        with self.lock:
            self.active_games[game_id] = {
                'game': game_obj, 'type': game_type, 'created_at': datetime.now()
            }
            metrics.increment('games_started')
    
    def get_game(self, game_id):
        with self.lock:
            return self.active_games.get(game_id)
    
    def end_game(self, game_id):
        with self.lock:
            return self.active_games.pop(game_id, None)
    
    def is_game_active(self, game_id):
        with self.lock:
            return game_id in self.active_games

game_manager = GameManager()

# ============================================
# 💾 Database Operations
# ============================================
def update_user_profile(user_id, current_line_name):
    try:
        with db_pool.get_connection() as conn:
            c = conn.cursor()
            c.execute('SELECT line_display_name FROM users WHERE user_id = ?', (user_id,))
            metrics.increment('db_queries')
            user = c.fetchone()
            if user and user['line_display_name'] != current_line_name:
                c.execute('''UPDATE users SET line_display_name = ?, last_updated = ? 
                            WHERE user_id = ?''',
                         (current_line_name, datetime.now().isoformat(), user_id))
        return True
    except:
        return False

def update_user_points(user_id, display_name, points, won=False, game_type=""):
    try:
        with db_pool.get_connection() as conn:
            c = conn.cursor()
            metrics.increment('db_queries')
            c.execute('''INSERT INTO users (user_id, display_name, line_display_name, 
                         total_points, games_played, wins, last_played)
                         VALUES (?, ?, ?, ?, 1, ?, ?)
                         ON CONFLICT(user_id) DO UPDATE SET
                         total_points = total_points + excluded.total_points,
                         games_played = games_played + 1,
                         wins = wins + excluded.wins,
                         last_played = excluded.last_played,
                         display_name = excluded.display_name,
                         last_updated = CURRENT_TIMESTAMP''',
                      (user_id, display_name, display_name, points, 1 if won else 0, 
                       datetime.now().isoformat()))
            
            if game_type:
                c.execute('INSERT INTO game_history (user_id, game_type, points, won) VALUES (?, ?, ?, ?)',
                         (user_id, game_type, points, 1 if won else 0))
            
            user_stats_cache.clear()
            leaderboard_cache.clear()
        return True
    except Exception as e:
        logger.error(f"❌ Points update error: {e}")
        return False

def get_user_stats(user_id):
    cached = user_stats_cache.get(user_id)
    if cached:
        return cached
    
    try:
        with db_pool.get_connection() as conn:
            c = conn.cursor()
            c.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
            metrics.increment('db_queries')
            user = c.fetchone()
            if user:
                user_dict = dict(user)
                user_stats_cache.set(user_id, user_dict)
                return user_dict
        return None
    except:
        return None

def get_leaderboard(limit=10):
    limit = max(1, min(int(limit), 100))
    cache_key = f'leaderboard_{limit}'
    cached = leaderboard_cache.get(cache_key)
    if cached:
        return cached
    
    try:
        with db_pool.get_connection() as conn:
            c = conn.cursor()
            c.execute('''SELECT display_name, total_points, games_played, wins 
                        FROM users ORDER BY total_points DESC LIMIT ?''', (limit,))
            metrics.increment('db_queries')
            leaders = [dict(row) for row in c.fetchall()]
            leaderboard_cache.set(cache_key, leaders)
            return leaders
    except:
        return []

def get_user_profile_safe(user_id):
    try:
        profile = line_bot_api.get_profile(user_id)
        update_user_profile(user_id, profile.display_name)
        return profile.display_name
    except:
        return "لاعب"

# ============================================
# 🧹 Cleanup Tasks
# ============================================
def cleanup_old_games():
    while True:
        try:
            time.sleep(300)
            now = datetime.now()
            to_delete = []
            with game_manager.lock:
                for game_id, game_data in game_manager.active_games.items():
                    if now - game_data['created_at'] > timedelta(minutes=30):
                        to_delete.append(game_id)
            for game_id in to_delete:
                game_manager.end_game(game_id)
        except:
            pass

def cleanup_old_data():
    while True:
        try:
            time.sleep(86400)
            cutoff_date = (datetime.now() - timedelta(days=30)).isoformat()
            with db_pool.get_connection() as conn:
                c = conn.cursor()
                c.execute('DELETE FROM game_history WHERE played_at < ?', (cutoff_date,))
                c.execute('DELETE FROM name_updates WHERE updated_at < ?', (cutoff_date,))
        except:
            pass

threading.Thread(target=cleanup_old_games, daemon=True).start()
threading.Thread(target=cleanup_old_data, daemon=True).start()

# ============================================
# 🎨 Beautiful Flex Messages with Animations
# ============================================
def get_random_gradient():
    """توليد تدرجات عشوائية جميلة"""
    gradients = [
        ["#667eea", "#764ba2"], ["#f093fb", "#f5576c"], ["#4facfe", "#00f2fe"],
        ["#43e97b", "#38f9d7"], ["#fa709a", "#fee140"], ["#30cfd0", "#330867"],
        ["#a8edea", "#fed6e3"], ["#ff9a9e", "#fecfef"], ["#ffecd2", "#fcb69f"],
        ["#ff6e7f", "#bfe9ff"]
    ]
    return random.choice(gradients)

def create_welcome_bubble(display_name):
    """رسالة ترحيب جميلة بـ Animations"""
    colors = get_random_gradient()
    return {
        "type": "bubble", "size": "mega",
        "hero": {
            "type": "box", "layout": "vertical",
            "contents": [
                {"type": "box", "layout": "vertical",
                 "contents": [
                    {"type": "text", "text": "🎮", "size": "5xl", "align": "center", "color": "#ffffff"},
                 ],
                 "paddingAll": "30px"}
            ],
            "background": {
                "type": "linearGradient",
                "angle": "135deg",
                "startColor": colors[0],
                "endColor": colors[1]
            }
        },
        "body": {
            "type": "box", "layout": "vertical",
            "contents": [
                {"type": "text", "text": f"مرحباً {display_name}! 👋", 
                 "weight": "bold", "size": "xl", "color": "#1f2937", "wrap": True},
                {"type": "text", "text": "أهلاً بك في عالم الألعاب الممتع", 
                 "size": "sm", "color": "#6b7280", "wrap": True, "margin": "md"},
                {"type": "separator", "margin": "xl", "color": "#e5e7eb"},
                {"type": "box", "layout": "vertical", "margin": "xl", "spacing": "sm",
                 "contents": [
                    {"type": "box", "layout": "horizontal", "spacing": "sm",
                     "contents": [
                        {"type": "text", "text": "🎯", "flex": 0},
                        {"type": "text", "text": "+15 لعبة متنوعة", "size": "sm", "color": "#4b5563", "flex": 5}
                     ]},
                    {"type": "box", "layout": "horizontal", "spacing": "sm",
                     "contents": [
                        {"type": "text", "text": "⭐", "flex": 0},
                        {"type": "text", "text": "نظام نقاط وترتيب", "size": "sm", "color": "#4b5563", "flex": 5}
                     ]},
                    {"type": "box", "layout": "horizontal", "spacing": "sm",
                     "contents": [
                        {"type": "text", "text": "🏆", "flex": 0},
                        {"type": "text", "text": "منافسة مع الأصدقاء", "size": "sm", "color": "#4b5563", "flex": 5}
                     ]},
                    {"type": "box", "layout": "horizontal", "spacing": "sm",
                     "contents": [
                        {"type": "text", "text": "🤖", "flex": 0},
                        {"type": "text", "text": "ذكاء اصطناعي متقدم", "size": "sm", "color": "#4b5563", "flex": 5}
                     ]}
                 ]},
                {"type": "text", "text": "جاهز للبدء؟ 🚀", 
                 "weight": "bold", "size": "lg", "color": colors[0], 
                 "align": "center", "margin": "xl"}
            ],
            "paddingAll": "25px"
        },
        "footer": {
            "type": "box", "layout": "vertical", "spacing": "sm",
            "contents": [
                {"type": "button",
                 "action": {"type": "message", "label": "🎮 ابدأ اللعب", "text": "ابدأ"},
                 "style": "primary",
                 "color": colors[0],
                 "height": "md"},
                {"type": "button",
                 "action": {"type": "message", "label": "📊 نقاطي", "text": "نقاطي"},
                 "style": "link",
                 "height": "sm"}
            ],
            "paddingAll": "20px"
        }
    }

def create_main_menu():
    """القائمة الرئيسية المحسّنة"""
    colors = get_random_gradient()
    return {
        "type": "bubble", "size": "mega",
        "hero": {
            "type": "box", "layout": "vertical",
            "contents": [
                {"type": "text", "text": "🎮", "size": "5xl", "align": "center", "color": "#ffffff"}
            ],
            "paddingAll": "30px",
            "background": {
                "type": "linearGradient",
                "angle": "135deg",
                "startColor": colors[0],
                "endColor": colors[1]
            }
        },
        "body": {
            "type": "box", "layout": "vertical",
            "contents": [
                {"type": "text", "text": "القائمة الرئيسية", 
                 "weight": "bold", "size": "xxl", "color": "#1f2937", "align": "center"},
                {"type": "text", "text": "اختر ما تريد", 
                 "size": "sm", "color": "#6b7280", "align": "center", "margin": "sm"},
                {"type": "separator", "margin": "xl", "color": "#e5e7eb"},
                {"type": "box", "layout": "vertical", "margin": "xl", "spacing": "md",
                 "contents": [
                    {"type": "button",
                     "action": {"type": "message", "label": "🎮 ابدأ اللعب", "text": "ابدأ"},
                     "style": "primary", "color": colors[0], "height": "md"},
                    {"type": "button",
                     "action": {"type": "message", "label": "📊 إحصائياتي", "text": "نقاطي"},
                     "style": "primary", "color": colors[1], "height": "md"},
                    {"type": "button",
                     "action": {"type": "message", "label": "🏆 لوحة الصدارة", "text": "الصدارة"},
                     "style": "secondary", "height": "md"},
                    {"type": "button",
                     "action": {"type": "message", "label": "❓ المساعدة", "text": "مساعدة"},
                     "style": "link", "height": "sm"}
                 ]}
            ],
            "paddingAll": "25px"
        }
    }

def create_games_carousel():
    """قائمة ألعاب محسّنة مع الألعاب المتاحة فقط"""
    if not AVAILABLE_GAMES_UI:
        # إذا لم تكن هناك ألعاب متاحة
        return {
            "type": "bubble",
            "body": {
                "type": "box", "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "⚠️ لا توجد ألعاب متاحة حالياً", 
                     "weight": "bold", "size": "lg", "color": "#ef4444", "wrap": True, "align": "center"}
                ],
                "paddingAll": "30px"
            }
        }
    
    bubbles = []
    for game in AVAILABLE_GAMES_UI:
        bubbles.append({
            "type": "bubble", "size": "micro",
            "hero": {
                "type": "box", "layout": "vertical",
                "contents": [
                    {"type": "text", "text": game["emoji"], "size": "5xl", "align": "center", "color": "#ffffff"}
                ],
                "paddingAll": "20px",
                "background": {"type": "linearGradient", "angle": "135deg",
                              "startColor": game["color"], "endColor": game["color"] + "dd"}
            },
            "body": {
                "type": "box", "layout": "vertical",
                "contents": [
                    {"type": "text", "text": f"لعبة {game['arabic']}", 
                     "weight": "bold", "size": "md", "align": "center", "color": "#1f2937"},
                    {"type": "text", "text": game["desc"], 
                     "size": "xs", "align": "center", "color": "#6b7280", "margin": "sm", "wrap": True}
                ],
                "paddingAll": "15px"
            },
            "footer": {
                "type": "box", "layout": "vertical",
                "contents": [
                    {"type": "button",
                     "action": {"type": "message", "label": "▶️ العب", "text": game["arabic"]},
                     "style": "primary", "color": game["color"], "height": "sm"}
                ],
                "paddingAll": "12px"
            }
        })
    
    return {"type": "carousel", "contents": bubbles}

def create_stats_bubble(stats, user_id):
    """بطاقة إحصائيات جميلة"""
    is_registered = "✅ مسجل" if game_manager.is_registered(user_id) else "⚠️ غير مسجل"
    win_rate = (stats['wins'] / stats['games_played'] * 100) if stats['games_played'] > 0 else 0
    colors = get_random_gradient()
    
    # تحديد المستوى
    points = stats['total_points']
    if points < 100:
        level, level_emoji = "مبتدئ", "🌱"
    elif points < 500:
        level, level_emoji = "متوسط", "⭐"
    elif points < 1000:
        level, level_emoji = "محترف", "🔥"
    else:
        level, level_emoji = "أسطوري", "👑"
    
    return {
        "type": "bubble", "size": "mega",
        "hero": {
            "type": "box", "layout": "vertical",
            "contents": [
                {"type": "text", "text": level_emoji, "size": "5xl", "align": "center", "color": "#ffffff"},
                {"type": "text", "text": level, "size": "xl", "align": "center", 
                 "color": "#ffffff", "weight": "bold", "margin": "md"}
            ],
            "paddingAll": "30px",
            "background": {
                "type": "linearGradient",
                "angle": "135deg",
                "startColor": colors[0],
                "endColor": colors[1]
            }
        },
        "body": {
            "type": "box", "layout": "vertical",
            "contents": [
                {"type": "text", "text": "📊 إحصائياتك", 
                 "weight": "bold", "size": "xl", "color": "#1f2937", "align": "center"},
                {"type": "box", "layout": "horizontal", "margin": "md",
                 "contents": [
                    {"type": "text", "text": "الحالة:", "size": "sm", "color": "#6b7280", "flex": 2},
                    {"type": "text", "text": is_registered, "size": "sm", "flex": 3, 
                     "align": "end", "weight": "bold"}
                 ]},
                {"type": "separator", "margin": "lg", "color": "#e5e7eb"},
                {"type": "box", "layout": "vertical", "margin": "lg", "spacing": "lg",
                 "contents": [
                    {"type": "box", "layout": "horizontal",
                     "contents": [
                        {"type": "box", "layout": "vertical", "flex": 1,
                         "contents": [
                            {"type": "text", "text": "💰", "size": "xxl", "align": "center"},
                            {"type": "text", "text": str(stats['total_points']), 
                             "size": "xxl", "weight": "bold", "color": colors[0], "align": "center"},
                            {"type": "text", "text": "نقطة", "size": "xs", "color": "#6b7280", "align": "center"}
                         ],
                         "backgroundColor": "#f3f4f6", "cornerRadius": "lg", "paddingAll": "15px"},
                        {"type": "box", "layout": "vertical", "flex": 1,
                         "contents": [
                            {"type": "text", "text": "🎮", "size": "xxl", "align": "center"},
                            {"type": "text", "text": str(stats['games_played']), 
                             "size": "xxl", "weight": "bold", "color": colors[1], "align": "center"},
                            {"type": "text", "text": "لعبة", "size": "xs", "color": "#6b7280", "align": "center"}
                         ],
                         "backgroundColor": "#f3f4f6", "cornerRadius": "lg", "paddingAll": "15px"}
                     ], "spacing": "md"},
                    {"type": "box", "layout": "horizontal", "margin": "md",
                     "contents": [
                        {"type": "box", "layout": "vertical", "flex": 1,
                         "contents": [
                            {"type": "text", "text": "🏆", "size": "xxl", "align": "center"},
                            {"type": "text", "text": str(stats['wins']), 
                             "size": "xxl", "weight": "bold", "color": "#10b981", "align": "center"},
                            {"type": "text", "text": "فوز", "size": "xs", "color": "#6b7280", "align": "center"}
                         ],
                         "backgroundColor": "#f3f4f6", "cornerRadius": "lg", "paddingAll": "15px"},
                        {"type": "box", "layout": "vertical", "flex": 1,
                         "contents": [
                            {"type": "text", "text": "📈", "size": "xxl", "align": "center"},
                            {"type": "text", "text": f"{win_rate:.0f}%", 
                             "size": "xxl", "weight": "bold", "color": "#f59e0b", "align": "center"},
                            {"type": "text", "text": "نسبة فوز", "size": "xs", "color": "#6b7280", "align": "center"}
                         ],
                         "backgroundColor": "#f3f4f6", "cornerRadius": "lg", "paddingAll": "15px"}
                     ], "spacing": "md"}
                 ]}
            ],
            "paddingAll": "25px"
        },
        "footer": {
            "type": "box", "layout": "vertical",
            "contents": [
                {"type": "button",
                 "action": {"type": "message", "label": "🎮 ابدأ لعبة", "text": "ابدأ"},
                 "style": "primary", "color": colors[0], "height": "md"}
            ],
            "paddingAll": "20px"
        }
    }

def create_leaderboard_bubble(leaders):
    """لوحة صدارة محسّنة وجميلة"""
    colors = get_random_gradient()
    
    # أفضل 3 لاعبين
    top_3 = []
    medals = ["🥇", "🥈", "🥉"]
    medal_colors = ["#fbbf24", "#d1d5db", "#f97316"]
    
    for i, leader in enumerate(leaders[:3]):
        top_3.append({
            "type": "box", "layout": "horizontal",
            "contents": [
                {"type": "box", "layout": "vertical",
                 "contents": [
                    {"type": "text", "text": medals[i], "size": "3xl", "align": "center"}
                 ],
                 "flex": 0, "paddingAll": "15px"},
                {"type": "box", "layout": "vertical",
                 "contents": [
                    {"type": "text", "text": leader['display_name'], 
                     "weight": "bold", "size": "lg", "color": "#1f2937", "wrap": True},
                    {"type": "box", "layout": "horizontal", "spacing": "xs",
                     "contents": [
                        {"type": "text", "text": f"⭐ {leader['total_points']}", 
                         "size": "sm", "color": "#6b7280"},
                        {"type": "text", "text": f"🎮 {leader['games_played']}", 
                         "size": "sm", "color": "#6b7280"},
                        {"type": "text", "text": f"🏆 {leader['wins']}", 
                         "size": "sm", "color": "#6b7280"}
                     ]}
                 ],
                 "flex": 5, "justifyContent": "center"}
            ],
            "backgroundColor": medal_colors[i] + "20",
            "cornerRadius": "lg",
            "paddingAll": "15px",
            "margin": "md" if i > 0 else "none"
        })
    
    # باقي اللاعبين
    other_players = []
    for i, leader in enumerate(leaders[3:], 4):
        other_players.append({
            "type": "box", "layout": "horizontal",
            "contents": [
                {"type": "text", "text": f"{i}", "size": "lg", "weight": "bold", 
                 "color": "#9ca3af", "flex": 0, "align": "center"},
                {"type": "text", "text": leader['display_name'], 
                 "size": "md", "color": "#1f2937", "flex": 3, "wrap": True},
                {"type": "text", "text": f"{leader['total_points']}⭐", 
                 "size": "sm", "color": "#6b7280", "flex": 2, "align": "end", "weight": "bold"}
            ],
            "spacing": "md",
            "paddingAll": "12px",
            "margin": "sm"
        })
    
    return {
        "type": "bubble", "size": "mega",
        "hero": {
            "type": "box", "layout": "vertical",
            "contents": [
                {"type": "text", "text": "🏆", "size": "5xl", "align": "center", "color": "#ffffff"},
                {"type": "text", "text": "لوحة الصدارة", "size": "xl", "align": "center", 
                 "color": "#ffffff", "weight": "bold", "margin": "md"}
            ],
            "paddingAll": "30px",
            "background": {
                "type": "linearGradient",
                "angle": "135deg",
                "startColor": colors[0],
                "endColor": colors[1]
            }
        },
        "body": {
            "type": "box", "layout": "vertical",
            "contents": top_3 + other_players,
            "paddingAll": "20px"
        },
        "footer": {
            "type": "box", "layout": "vertical",
            "contents": [
                {"type": "button",
                 "action": {"type": "message", "label": "📊 نقاطي", "text": "نقاطي"},
                 "style": "link", "height": "sm"}
            ],
            "paddingAll": "15px"
        }
    }

def create_help_bubble():
    """بطاقة مساعدة شاملة"""
    colors = get_random_gradient()
    return {
        "type": "bubble", "size": "mega",
        "hero": {
            "type": "box", "layout": "vertical",
            "contents": [
                {"type": "text", "text": "❓", "size": "5xl", "align": "center", "color": "#ffffff"},
                {"type": "text", "text": "كيف ألعب؟", "size": "xl", "align": "center", 
                 "color": "#ffffff", "weight": "bold", "margin": "md"}
            ],
            "paddingAll": "30px",
            "background": {
                "type": "linearGradient",
                "angle": "135deg",
                "startColor": colors[0],
                "endColor": colors[1]
            }
        },
        "body": {
            "type": "box", "layout": "vertical",
            "contents": [
                {"type": "text", "text": "خطوات سريعة للبدء:", 
                 "weight": "bold", "size": "lg", "color": "#1f2937", "margin": "none"},
                {"type": "box", "layout": "vertical", "margin": "lg", "spacing": "md",
                 "contents": [
                    {"type": "box", "layout": "horizontal", "spacing": "sm",
                     "contents": [
                        {"type": "box", "layout": "vertical",
                         "contents": [{"type": "text", "text": "1", "size": "lg", "weight": "bold", 
                                      "color": "#ffffff", "align": "center"}],
                         "backgroundColor": colors[0], "cornerRadius": "30px",
                         "width": "35px", "height": "35px", "justifyContent": "center", "flex": 0},
                        {"type": "box", "layout": "vertical",
                         "contents": [
                            {"type": "text", "text": "اكتب 'انضم'", "weight": "bold", "size": "sm", "color": "#1f2937"},
                            {"type": "text", "text": "للتسجيل في البوت", "size": "xs", "color": "#6b7280"}
                         ], "flex": 5}
                     ]},
                    {"type": "box", "layout": "horizontal", "spacing": "sm",
                     "contents": [
                        {"type": "box", "layout": "vertical",
                         "contents": [{"type": "text", "text": "2", "size": "lg", "weight": "bold", 
                                      "color": "#ffffff", "align": "center"}],
                         "backgroundColor": colors[0], "cornerRadius": "30px",
                         "width": "35px", "height": "35px", "justifyContent": "center", "flex": 0},
                        {"type": "box", "layout": "vertical",
                         "contents": [
                            {"type": "text", "text": "اكتب 'ابدأ'", "weight": "bold", "size": "sm", "color": "#1f2937"},
                            {"type": "text", "text": "لعرض قائمة الألعاب", "size": "xs", "color": "#6b7280"}
                         ], "flex": 5}
                     ]},
                    {"type": "box", "layout": "horizontal", "spacing": "sm",
                     "contents": [
                        {"type": "box", "layout": "vertical",
                         "contents": [{"type": "text", "text": "3", "size": "lg", "weight": "bold", 
                                      "color": "#ffffff", "align": "center"}],
                         "backgroundColor": colors[0], "cornerRadius": "30px",
                         "width": "35px", "height": "35px", "justifyContent": "center", "flex": 0},
                        {"type": "box", "layout": "vertical",
                         "contents": [
                            {"type": "text", "text": "اختر لعبة", "weight": "bold", "size": "sm", "color": "#1f2937"},
                            {"type": "text", "text": "واستمتع باللعب!", "size": "xs", "color": "#6b7280"}
                         ], "flex": 5}
                     ]}
                 ]},
                {"type": "separator", "margin": "xl", "color": "#e5e7eb"},
                {"type": "text", "text": "أوامر مفيدة:", 
                 "weight": "bold", "size": "md", "color": "#1f2937", "margin": "xl"},
                {"type": "box", "layout": "vertical", "margin": "md", "spacing": "sm",
                 "contents": [
                    {"type": "text", "text": "• نقاطي - عرض إحصائياتك", "size": "sm", "color": "#4b5563"},
                    {"type": "text", "text": "• الصدارة - عرض أفضل اللاعبين", "size": "sm", "color": "#4b5563"},
                    {"type": "text", "text": "• إيقاف - إيقاف اللعبة الحالية", "size": "sm", "color": "#4b5563"},
                    {"type": "text", "text": "• انسحب - إلغاء التسجيل", "size": "sm", "color": "#4b5563"}
                 ]}
            ],
            "paddingAll": "25px"
        },
        "footer": {
            "type": "box", "layout": "vertical",
            "contents": [
                {"type": "button",
                 "action": {"type": "message", "label": "🎮 ابدأ الآن", "text": "ابدأ"},
                 "style": "primary", "color": colors[0], "height": "md"}
            ],
            "paddingAll": "20px"
        }
    }

# ============================================
# 🎯 Command Handler with Quick Replies
# ============================================
class CommandHandler:
    def __init__(self, game_mgr, bot_api):
        self.game_manager = game_mgr
        self.line_bot_api = bot_api
        self.commands = {
            'مساعدة': self.show_help, 'help': self.show_help, 'المساعدة': self.show_help,
            'انضم': self.join_game, 'تسجيل': self.join_game, 'join': self.join_game,
            'انسحب': self.leave_game, 'خروج': self.leave_game, 'leave': self.leave_game,
            'ابدأ': self.start_menu, 'start': self.start_menu, 'الألعاب': self.start_menu,
            'نقاطي': self.show_stats, 'احصائياتي': self.show_stats,
            'الصدارة': self.show_leaderboard,
            'إيقاف': self.stop_game, 'ايقاف': self.stop_game, 'stop': self.stop_game,
            'إعادة': self.restart_game, 'اعادة': self.restart_game
        }
    
    def handle(self, event, user_id, text, game_id, display_name):
        handler = self.commands.get(text)
        if handler:
            return handler(event, user_id, game_id, display_name)
        return False
    
    def show_help(self, event, *args):
        help_bubble = create_help_bubble()
        self.line_bot_api.reply_message(event.reply_token, 
            FlexSendMessage(alt_text="كيف ألعب؟", contents=help_bubble))
        return True
    
    def join_game(self, event, user_id, game_id, display_name):
        if self.game_manager.is_registered(user_id):
            quick_reply = QuickReply(items=[
                QuickReplyButton(action=MessageAction(label="🎮 ابدأ اللعب", text="ابدأ")),
                QuickReplyButton(action=MessageAction(label="📊 نقاطي", text="نقاطي")),
                QuickReplyButton(action=MessageAction(label="🏆 الصدارة", text="الصدارة"))
            ])
            self.line_bot_api.reply_message(event.reply_token,
                TextSendMessage(
                    text=f"✅ أنت مسجل بالفعل يا {display_name}!\n\nاختر من القائمة أدناه 👇",
                    quick_reply=quick_reply
                ))
        else:
            self.game_manager.register_player(user_id)
            welcome = create_welcome_bubble(display_name)
            self.line_bot_api.reply_message(event.reply_token,
                FlexSendMessage(alt_text="مرحباً بك!", contents=welcome))
        return True
    
    def leave_game(self, event, user_id, *args):
        if self.game_manager.is_registered(user_id):
            self.game_manager.unregister_player(user_id)
            quick_reply = QuickReply(items=[
                QuickReplyButton(action=MessageAction(label="🔄 انضم مجدداً", text="انضم"))
            ])
            self.line_bot_api.reply_message(event.reply_token,
                TextSendMessage(
                    text="👋 تم الانسحاب بنجاح\n\nسنفتقدك! يمكنك العودة في أي وقت",
                    quick_reply=quick_reply
                ))
        else:
            self.line_bot_api.reply_message(event.reply_token,
                TextSendMessage(text="❌ أنت غير مسجل\n\nاكتب 'انضم' للتسجيل"))
        return True
    
    def start_menu(self, event, *args):
        games_carousel = create_games_carousel()
        self.line_bot_api.reply_message(event.reply_token,
            FlexSendMessage(alt_text="اختر لعبتك المفضلة", contents=games_carousel))
        return True
    
    def show_stats(self, event, user_id, *args):
        stats = get_user_stats(user_id)
        if stats:
            stats_bubble = create_stats_bubble(stats, user_id)
            quick_reply = QuickReply(items=[
                QuickReplyButton(action=MessageAction(label="🎮 ابدأ لعبة", text="ابدأ")),
                QuickReplyButton(action=MessageAction(label="🏆 الصدارة", text="الصدارة"))
            ])
            self.line_bot_api.reply_message(event.reply_token,
                FlexSendMessage(alt_text="إحصائياتك", contents=stats_bubble,
                               quick_reply=quick_reply))
        else:
            quick_reply = QuickReply(items=[
                QuickReplyButton(action=MessageAction(label="📝 انضم للعب", text="انضم"))
            ])
            self.line_bot_api.reply_message(event.reply_token,
                TextSendMessage(
                    text="❌ لم تلعب بعد\n\nاكتب 'انضم' للبدء",
                    quick_reply=quick_reply
                ))
        return True
    
    def show_leaderboard(self, event, *args):
        leaders = get_leaderboard()
        if leaders:
            leaderboard = create_leaderboard_bubble(leaders)
            quick_reply = QuickReply(items=[
                QuickReplyButton(action=MessageAction(label="📊 نقاطي", text="نقاطي")),
                QuickReplyButton(action=MessageAction(label="🎮 ابدأ لعبة", text="ابدأ"))
            ])
            self.line_bot_api.reply_message(event.reply_token,
                FlexSendMessage(alt_text="لوحة الصدارة", contents=leaderboard,
                               quick_reply=quick_reply))
        else:
            self.line_bot_api.reply_message(event.reply_token,
                TextSendMessage(text="❌ لا توجد بيانات حالياً"))
        return True
    
    def stop_game(self, event, user_id, game_id, *args):
        if self.game_manager.is_game_active(game_id):
            game_data = self.game_manager.get_game(game_id)
            game_type = game_data['type']
            self.game_manager.end_game(game_id)
            quick_reply = QuickReply(items=[
                QuickReplyButton(action=MessageAction(label="🎮 ابدأ لعبة جديدة", text="ابدأ")),
                QuickReplyButton(action=MessageAction(label="📊 نقاطي", text="نقاطي"))
            ])
            self.line_bot_api.reply_message(event.reply_token,
                TextSendMessage(
                    text=f"⏸️ تم إيقاف لعبة {game_type}\n\nيمكنك بدء لعبة جديدة",
                    quick_reply=quick_reply
                ))
        else:
            self.line_bot_api.reply_message(event.reply_token,
                TextSendMessage(text="❌ لا توجد لعبة نشطة"))
        return True
    
    def restart_game(self, event, user_id, game_id, *args):
        if self.game_manager.is_game_active(game_id):
            game_data = self.game_manager.get_game(game_id)
            game_type = game_data['type']
            self.game_manager.end_game(game_id)
            quick_reply = QuickReply(items=[
                QuickReplyButton(action=MessageAction(label=f"🔄 {game_type}", text=game_type)),
                QuickReplyButton(action=MessageAction(label="🎮 اختر لعبة أخرى", text="ابدأ"))
            ])
            self.line_bot_api.reply_message(event.reply_token,
                TextSendMessage(
                    text=f"🔄 تم إعادة تعيين اللعبة\n\nجاهز للبدء من جديد؟",
                    quick_reply=quick_reply
                ))
        else:
            self.line_bot_api.reply_message(event.reply_token,
                TextSendMessage(text="❌ لا توجد لعبة نشطة"))
        return True

command_handler = CommandHandler(game_manager, line_bot_api)

# ============================================
# 🎮 Game Starter & Handler
# ============================================
def start_game(game_id, game_class, game_type, user_id, event):
    try:
        ai_games = ['IQGame', 'WordColorGame', 'LettersWordsGame', 'HumanAnimalPlantGame']
        
        if game_class.__name__ in ai_games:
            game = game_class(line_bot_api, use_ai=USE_AI,
                            get_api_key=get_gemini_api_key, switch_key=switch_gemini_key)
        else:
            game = game_class(line_bot_api)
        
        game_manager.create_game(game_id, game, game_type)
        response = game.start_game()
        
        # إضافة Quick Reply للعبة
        if hasattr(response, 'text'):
            quick_reply = QuickReply(items=[
                QuickReplyButton(action=MessageAction(label="⏸️ إيقاف", text="إيقاف")),
                QuickReplyButton(action=MessageAction(label="🔄 إعادة", text="إعادة"))
            ])
            response.quick_reply = quick_reply
        
        line_bot_api.reply_message(event.reply_token, response)
        logger.info(f"🎮 Game started: {game_type}")
        return True
    except Exception as e:
        logger.error(f"❌ Game start error: {e}")
        metrics.increment('errors')
        line_bot_api.reply_message(event.reply_token,
            TextSendMessage(text=f"❌ خطأ في بدء {game_type}"))
        return False

def handle_game_answer(event, user_id, text, game_id, display_name):
    game_data = game_manager.get_game(game_id)
    if not game_data:
        return
    
    game = game_data['game']
    game_type = game_data['type']
    
    try:
        result = game.check_answer(text, user_id, display_name)
        if result:
            points = result.get('points', 0)
            if points > 0:
                update_user_points(user_id, display_name, points,
                                 result.get('won', False), game_type)
            
            if result.get('game_over', False):
                game_manager.end_game(game_id)
                quick_reply = QuickReply(items=[
                    QuickReplyButton(action=MessageAction(label="🎮 لعبة جديدة", text="ابدأ")),
                    QuickReplyButton(action=MessageAction(label="📊 نقاطي", text="نقاطي"))
                ])
                response = TextSendMessage(
                    text=result.get('message', '🏁 انتهت اللعبة!\n\nجاهز لجولة أخرى؟'),
                    quick_reply=quick_reply
                )
            else:
                response = result.get('response', TextSendMessage(text=result.get('message', '')))
                # إضافة Quick Reply
                if hasattr(response, 'text'):
                    quick_reply = QuickReply(items=[
                        QuickReplyButton(action=MessageAction(label="⏸️ إيقاف", text="إيقاف"))
                    ])
                    response.quick_reply = quick_reply
            
            line_bot_api.reply_message(event.reply_token, response)
    except Exception as e:
        logger.error(f"❌ Answer error: {e}")
        metrics.increment('errors')
        line_bot_api.reply_message(event.reply_token,
            TextSendMessage(text="❌ حدث خطأ. حاول مرة أخرى"))

# ============================================
# 🌐 Flask Routes
# ============================================
@app.route("/", methods=['GET'])
def home():
    stats = metrics.get_stats()
    return f'''<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>LINE Gaming Bot</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'Segoe UI',sans-serif;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);
color:#fff;min-height:100vh;display:flex;align-items:center;justify-content:center;padding:20px}}
.container{{background:rgba(255,255,255,0.1);backdrop-filter:blur(10px);padding:40px;
border-radius:20px;max-width:900px;width:100%;box-shadow:0 8px 32px rgba(31,38,135,0.37)}}
h1{{font-size:3em;margin-bottom:10px;text-align:center;animation:fadeIn 1s}}
.status{{text-align:center;font-size:1.2em;margin-bottom:30px;color:#4ade80}}
.stats{{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:20px;margin:30px 0}}
.stat-box{{background:rgba(255,255,255,0.2);border-radius:15px;padding:20px;text-align:center;
transition:transform 0.3s,box-shadow 0.3s;animation:slideUp 0.5s}}
.stat-box:hover{{transform:translateY(-5px);box-shadow:0 10px 25px rgba(0,0,0,0.2)}}
.stat-number{{font-size:2.5em;font-weight:bold;margin:10px 0}}
.stat-label{{font-size:0.9em;opacity:0.9;text-transform:uppercase}}
.badge{{display:inline-block;background:rgba(74,222,128,0.3);padding:5px 15px;
border-radius:20px;margin:5px;font-size:0.85em;animation:fadeIn 1.5s}}
@keyframes fadeIn{{from{{opacity:0}}to{{opacity:1}}}}
@keyframes slideUp{{from{{transform:translateY(20px);opacity:0}}to{{transform:translateY(0);opacity:1}}}}
</style></head><body>
<div class="container">
<h1>🎮 Gaming Bot</h1>
<p class="status">✅ Enhanced & Beautiful Version</p>
<div class="stats">
<div class="stat-box"><div class="stat-number">{len(GAMES_LOADED)}</div><div class="stat-label">Games</div></div>
<div class="stat-box"><div class="stat-number">{len(game_manager.registered_players)}</div><div class="stat-label">Players</div></div>
<div class="stat-box"><div class="stat-number">{len(game_manager.active_games)}</div><div class="stat-label">Active</div></div>
<div class="stat-box"><div class="stat-number">{stats['requests']}</div><div class="stat-label">Requests</div></div>
<div class="stat-box"><div class="stat-number">{stats['games_started']}</div><div class="stat-label">Games Started</div></div>
<div class="stat-box"><div class="stat-number">{stats['requests_per_second']:.2f}</div><div class="stat-label">RPS</div></div>
</div>
<div style="text-align:center;margin-top:20px">
<span class="badge">🔒 Secure</span><span class="badge">⚡ Fast</span>
<span class="badge">🎨 Beautiful</span><span class="badge">📊 Monitored</span>
</div>
<div style="text-align:center;margin-top:30px;opacity:0.8">
<p>⏱️ Uptime: {stats['uptime_seconds']/3600:.1f}h | Cache: {metrics.cache_hits}/{metrics.cache_hits+metrics.cache_misses}</p>
<p>✨ All Systems Operational</p>
</div></div></body></html>'''

@app.route("/health", methods=['GET'])
def health_check():
    try:
        with db_pool.get_connection() as conn:
            conn.execute('SELECT 1')
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'metrics': metrics.get_stats(),
            'games': {'active': len(game_manager.active_games), 'registered': len(game_manager.registered_players)}
        }), 200
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500

@app.route("/metrics", methods=['GET'])
def get_metrics():
    return jsonify({
        'metrics': metrics.get_stats(),
        'games': {'active': len(game_manager.active_games), 'registered': len(game_manager.registered_players)},
        'cache': {'user_stats': len(user_stats_cache.cache), 'leaderboard': len(leaderboard_cache.cache)}
    })

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers.get('X-Line-Signature')
    if not signature:
        logger.warning("⚠️ Missing signature")
        abort(400)
    
    body = request.get_data(as_text=True)
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    
    if not rate_limiter.is_allowed(client_ip):
        logger.warning(f"⚠️ Rate limit: {client_ip}")
        abort(429)
    
    metrics.increment('requests')
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        logger.warning("⚠️ Invalid signature")
        metrics.increment('errors')
        abort(400)
    except Exception as e:
        logger.error(f"❌ Callback error: {e}")
        metrics.increment('errors')
        abort(500)
    
    return 'OK'

# ============================================
# 📨 Message Handler
# ============================================
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    try:
        user_id = event.source.user_id
        text = event.message.text.strip()
        game_id = getattr(event.source, 'group_id', user_id)
        display_name = get_user_profile_safe(user_id)
        
        logger.info(f"📨 {display_name}: {text}")
        
        # فحص المنشن
        if f'@{BOT_NAME}' in text:
            text = text.replace(f'@{BOT_NAME}', '').strip() or 'مساعدة'
        
        # معالجة الأوامر
        if command_handler.handle(event, user_id, text, game_id, display_name):
            return
        
        # بدء الألعاب (باستخدام الخريطة الديناميكية)
        if text in GAME_NAME_MAP:
            if not game_manager.is_registered(user_id):
                quick_reply = QuickReply(items=[
                    QuickReplyButton(action=MessageAction(label="📝 انضم الآن", text="انضم"))
                ])
                line_bot_api.reply_message(event.reply_token,
                    TextSendMessage(
                        text="❌ يجب التسجيل أولاً\n\nانضم الآن واستمتع باللعب! 🎮",
                        quick_reply=quick_reply
                    ))
                return
            
            class_name = GAME_NAME_MAP[text]
            game_class = GAMES_LOADED.get(class_name)
            
            if not game_class:
                line_bot_api.reply_message(event.reply_token,
                    TextSendMessage(text=f"❌ لعبة {text} غير متاحة حالياً\n\nجرب لعبة أخرى"))
                return
            
            # لعبة التوافق - حالة خاصة
            if text == 'توافق':
                game = game_class(line_bot_api)
                game_manager.create_game(game_id, game, text)
                line_bot_api.reply_message(event.reply_token,
                    TextSendMessage(text="💖 لعبة التوافق!\n\nاكتب اسمين مفصولين بمسافة\nمثال: أحمد فاطمة"))
                return
            
            start_game(game_id, game_class, text, user_id, event)
            return
        
        # معالجة إجابات الألعاب النشطة
        if game_manager.is_game_active(game_id):
            if not game_manager.is_registered(user_id):
                logger.debug(f"🔇 Unregistered: {user_id}")
                return
            
            handle_game_answer(event, user_id, text, game_id, display_name)
            return
        
        # رسالة ترحيب للمستخدمين الجدد
        if text.lower() in ['hi', 'hello', 'مرحبا', 'السلام عليكم', 'هاي']:
            welcome = create_welcome_bubble(display_name)
            line_bot_api.reply_message(event.reply_token,
                FlexSendMessage(alt_text="مرحباً بك!", contents=welcome))
            return
        
        logger.debug(f"🔇 Ignored: {text}")
        
    except Exception as e:
        logger.error(f"❌ Handler error: {e}", exc_info=True)
        metrics.increment('errors')
        try:
            quick_reply = QuickReply(items=[
                QuickReplyButton(action=MessageAction(label="🏠 القائمة الرئيسية", text="مساعدة"))
            ])
            line_bot_api.reply_message(event.reply_token,
                TextSendMessage(
                    text="❌ حدث خطأ غير متوقع\n\nحاول مرة أخرى أو اتصل بالدعم",
                    quick_reply=quick_reply
                ))
        except:
            pass

# ============================================
# 🚨 Error Handlers
# ============================================
@app.errorhandler(400)
def bad_request(e):
    return jsonify({'error': 'Bad Request', 'message': str(e)}), 400

@app.errorhandler(429)
def rate_limit_exceeded(e):
    return jsonify({'error': 'Too Many Requests', 'message': 'Please slow down'}), 429

@app.errorhandler(500)
def internal_error(e):
    metrics.increment('errors')
    return jsonify({'error': 'Internal Server Error'}), 500

@app.errorhandler(Exception)
def handle_unexpected_error(error):
    logger.error(f"❌ Unexpected: {error}", exc_info=True)
    metrics.increment('errors')
    return jsonify({'error': 'Internal Server Error'}), 500

# ============================================
# 🛑 Graceful Shutdown
# ============================================
def graceful_shutdown(signum, frame):
    logger.info("🛑 Shutting down gracefully...")
    
    with game_manager.lock:
        logger.info(f"💾 {len(game_manager.active_games)} active games")
    
    with db_pool.lock:
        for conn in db_pool.pool:
            conn.close()
        logger.info("💾 Database connections closed")
    
    logger.info("✅ Shutdown complete")
    exit(0)

signal.signal(signal.SIGTERM, graceful_shutdown)
signal.signal(signal.SIGINT, graceful_shutdown)

# ============================================
# 🚀 Application Entry Point
# ============================================
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    logger.info("=" * 70)
    logger.info("🎮 LINE GAMING BOT - ENHANCED & BEAUTIFUL VERSION")
    logger.info("=" * 70)
    logger.info(f"🌐 Port: {port}")
    logger.info(f"🎯 Games: {len(GAMES_LOADED)}")
    logger.info(f"📊 Players: {len(game_manager.registered_players)}")
    logger.info(f"🎮 Active: {len(game_manager.active_games)}")
    logger.info(f"🤖 AI: {'✅' if USE_AI else '❌'}")
    logger.info(f"🔧 Debug: {'✅' if debug else '❌'}")
    logger.info("=" * 70)
    logger.info("✨ Features:")
    logger.info("  • Beautiful Neumorphism UI with Gradients")
    logger.info("  • Quick Reply Buttons for Easy Navigation")
    logger.info("  • Animated Flex Messages")
    logger.info("  • Smart Welcome Messages")
    logger.info("  • Level System (مبتدئ → أسطوري)")
    logger.info("  • Enhanced Leaderboard with Medals")
    logger.info("  • Comprehensive Help System")
    logger.info("  • Connection Pool & Caching")
    logger.info("  • Rate Limiting & Security")
    logger.info("=" * 70)
    
    app.run(host='0.0.0.0', port=port, debug=debug, threaded=True)
