"""
Bot Mesh - Professional Gaming Bot
تصميم Neumorphism Soft احترافي
Created by: Abeer Aldosari © 2025
"""
from flask import Flask, request, abort, jsonify
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage
import os, sqlite3, threading, time, logging, signal, importlib
from datetime import datetime, timedelta
from contextlib import contextmanager
from collections import defaultdict

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ============================================
# 🎮 Dynamic Games Loading
# ============================================
GAMES_FOLDER = "games"

def snake_to_camel(name):
    return "".join(word.capitalize() for word in name.split("_"))

def load_games():
    games = {}
    if not os.path.exists(GAMES_FOLDER):
        logger.warning(f"⚠️ {GAMES_FOLDER} folder not found")
        return games
    
    logger.info(f"🔍 Loading games from {GAMES_FOLDER}")
    for filename in os.listdir(GAMES_FOLDER):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = filename[:-3]
            class_name = snake_to_camel(module_name)
            try:
                module = importlib.import_module(f"{GAMES_FOLDER}.{module_name}")
                game_class = getattr(module, class_name, None)
                if game_class:
                    games[class_name] = game_class
                    logger.info(f"✅ {class_name}")
            except Exception as e:
                logger.debug(f"⚠️ {class_name}: {e}")
    
    logger.info(f"📊 {len(games)} games loaded")
    return games

GAMES_LOADED = load_games()

GAME_MAP = {
    'ذكاء': {'class': 'IQGame', 'emoji': '🧠', 'name': 'اختبار الذكاء', 'color': '#A3B1C6'},
    'لون': {'class': 'WordColorGame', 'emoji': '🎨', 'name': 'لعبة الألوان', 'color': '#C3AED6'},
    'سلسلة': {'class': 'ChainWordsGame', 'emoji': '⛓️', 'name': 'سلسلة الكلمات', 'color': '#8FC7D6'},
    'ترتيب': {'class': 'ScrambleWordGame', 'emoji': '🔤', 'name': 'ترتيب الحروف', 'color': '#A8D5BA'},
    'تكوين': {'class': 'LettersWordsGame', 'emoji': '✍️', 'name': 'تكوين الكلمات', 'color': '#D4A5A5'},
    'أسرع': {'class': 'FastTypingGame', 'emoji': '⚡', 'name': 'الكتابة السريعة', 'color': '#FFB6C1'},
    'لعبة': {'class': 'HumanAnimalPlantGame', 'emoji': '🎯', 'name': 'إنسان حيوان نبات', 'color': '#B0C4DE'},
    'خمن': {'class': 'GuessGame', 'emoji': '🤔', 'name': 'خمن الرقم', 'color': '#D8BFD8'},
    'توافق': {'class': 'CompatibilityGame', 'emoji': '💖', 'name': 'نسبة التوافق', 'color': '#FFB3BA'},
    'رياضيات': {'class': 'MathGame', 'emoji': '🔢', 'name': 'الرياضيات', 'color': '#A3B1C6'},
    'ذاكرة': {'class': 'MemoryGame', 'emoji': '🧩', 'name': 'اختبار الذاكرة', 'color': '#BAE1FF'},
    'لغز': {'class': 'RiddleGame', 'emoji': '🎭', 'name': 'حل الألغاز', 'color': '#FFDFBA'},
    'ضد': {'class': 'OppositeGame', 'emoji': '↔️', 'name': 'الأضداد', 'color': '#BAFFC9'},
    'إيموجي': {'class': 'EmojiGame', 'emoji': '😀', 'name': 'خمن الإيموجي', 'color': '#FFE5B4'},
    'أغنية': {'class': 'SongGame', 'emoji': '🎵', 'name': 'خمن الأغنية', 'color': '#E0BBE4'}
}

AVAILABLE_GAMES = {k: v for k, v in GAME_MAP.items() if v['class'] in GAMES_LOADED}

# ============================================
# ⚙️ Configuration
# ============================================
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', 'YOUR_TOKEN')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET', 'YOUR_SECRET')
DB_NAME = 'game_scores.db'

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
# 📊 Metrics
# ============================================
class Metrics:
    def __init__(self):
        self.requests = 0
        self.games_started = 0
        self.lock = threading.Lock()
    
    def increment(self, metric):
        with self.lock:
            setattr(self, metric, getattr(self, metric) + 1)

metrics = Metrics()

# ============================================
# 💾 Database
# ============================================
class ConnectionPool:
    def __init__(self, db_name, max_conn=10):
        self.db_name = db_name
        self.pool = []
        self.max_conn = max_conn
        self.lock = threading.Lock()
    
    @contextmanager
    def get_connection(self):
        conn = None
        try:
            with self.lock:
                conn = self.pool.pop() if self.pool else sqlite3.connect(self.db_name, check_same_thread=False, timeout=10)
                conn.row_factory = sqlite3.Row
            yield conn
            conn.commit()
        except:
            if conn: conn.rollback()
            raise
        finally:
            if conn:
                with self.lock:
                    if len(self.pool) < self.max_conn:
                        self.pool.append(conn)
                    else:
                        conn.close()

db_pool = ConnectionPool(DB_NAME)

def init_db():
    with db_pool.get_connection() as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY, display_name TEXT,
            total_points INTEGER DEFAULT 0, games_played INTEGER DEFAULT 0,
            wins INTEGER DEFAULT 0, registered_at TEXT DEFAULT CURRENT_TIMESTAMP)''')
        c.execute('''CREATE TABLE IF NOT EXISTS game_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT,
            game_type TEXT, points INTEGER, won INTEGER,
            played_at TEXT DEFAULT CURRENT_TIMESTAMP)''')
        c.execute('CREATE INDEX IF NOT EXISTS idx_points ON users(total_points DESC)')

init_db()

def update_points(user_id, name, points, won=False, game_type=""):
    with db_pool.get_connection() as conn:
        c = conn.cursor()
        c.execute('''INSERT INTO users (user_id, display_name, total_points, games_played, wins)
                     VALUES (?, ?, ?, 1, ?) ON CONFLICT(user_id) DO UPDATE SET
                     total_points = total_points + ?, games_played = games_played + 1,
                     wins = wins + ?, display_name = ?''',
                  (user_id, name, points, 1 if won else 0, points, 1 if won else 0, name))
        if game_type:
            c.execute('INSERT INTO game_history (user_id, game_type, points, won) VALUES (?, ?, ?, ?)',
                     (user_id, game_type, points, 1 if won else 0))

def get_stats(user_id):
    with db_pool.get_connection() as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        return dict(c.fetchone()) if c.fetchone() else None

def get_leaderboard(limit=10):
    with db_pool.get_connection() as conn:
        c = conn.cursor()
        c.execute('SELECT display_name, total_points, games_played, wins FROM users ORDER BY total_points DESC LIMIT ?', (limit,))
        return [dict(r) for r in c.fetchall()]

def get_profile(user_id):
    try:
        return line_bot_api.get_profile(user_id).display_name
    except:
        return "لاعب"

# ============================================
# 🎮 Game Manager
# ============================================
class GameManager:
    def __init__(self):
        self.active_games = {}
        self.registered = set()
        self.lock = threading.Lock()
    
    def is_registered(self, uid):
        with self.lock:
            return uid in self.registered
    
    def register(self, uid):
        with self.lock:
            self.registered.add(uid)
    
    def unregister(self, uid):
        with self.lock:
            self.registered.discard(uid)
    
    def create_game(self, gid, game, gtype):
        with self.lock:
            self.active_games[gid] = {'game': game, 'type': gtype, 'created': datetime.now()}
    
    def get_game(self, gid):
        with self.lock:
            return self.active_games.get(gid)
    
    def end_game(self, gid):
        with self.lock:
            return self.active_games.pop(gid, None)
    
    def is_active(self, gid):
        with self.lock:
            return gid in self.active_games

game_manager = GameManager()

# ============================================
# 🎨 Neumorphism Design System
# ============================================
NEUMORPHIC_COLORS = {
    'bg': '#E0E5EC',
    'text_dark': '#A3B1C6',
    'text_light': '#FFFFFF',
    'shadow_dark': '#A3B1C6',
    'shadow_light': '#FFFFFF',
    'accent': '#DADE2C',
    'button': '#C3AED6'
}

def create_neumorphic_button(text, action_text, color='#C3AED6'):
    return {
        "type": "button",
        "action": {"type": "message", "label": text, "text": action_text},
        "style": "primary",
        "color": color,
        "height": "md",
        "margin": "md"
    }

def create_main_menu():
    return {
        "type": "bubble",
        "size": "mega",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": "Bot Mesh 🎮", "weight": "bold",
                 "size": "xxl", "color": "#A3B1C6", "align": "center"},
                {"type": "text", "text": "تأثير 3D - عمق ناعم", "size": "sm",
                 "color": "#A3B1C6", "align": "center", "margin": "sm"}
            ],
            "paddingAll": "20px",
            "backgroundColor": "#E0E5EC"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                create_neumorphic_button("📝 انضم للعب", "انضم", "#A3B1C6"),
                create_neumorphic_button("🎮 ابدأ اللعب", "ابدأ", "#C3AED6"),
                create_neumorphic_button("📊 نقاطي", "نقاطي", "#8FC7D6"),
                create_neumorphic_button("🏆 الصدارة", "الصدارة", "#A8D5BA"),
                create_neumorphic_button("❓ المساعدة", "مساعدة", "#D4A5A5")
            ],
            "paddingAll": "20px",
            "backgroundColor": "#E0E5EC",
            "spacing": "none"
        }
    }

def create_games_grid():
    if not AVAILABLE_GAMES:
        return {"type": "bubble", "body": {
            "type": "box", "layout": "vertical",
            "contents": [{"type": "text", "text": "⚠️ لا توجد ألعاب", "align": "center", "color": "#A3B1C6"}],
            "paddingAll": "30px", "backgroundColor": "#E0E5EC"
        }}
    
    bubbles = []
    for arabic, data in AVAILABLE_GAMES.items():
        bubbles.append({
            "type": "bubble",
            "size": "micro",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "box", "layout": "vertical",
                     "contents": [{"type": "text", "text": data['emoji'], "size": "5xl", "align": "center", "color": "#A3B1C6"}],
                     "paddingAll": "20px", "backgroundColor": "#E0E5EC",
                     "cornerRadius": "20px", "margin": "none"},
                    {"type": "text", "text": data['name'], "weight": "bold",
                     "size": "sm", "align": "center", "color": "#A3B1C6",
                     "margin": "md", "wrap": True},
                    {"type": "button",
                     "action": {"type": "message", "label": "▶️ العب", "text": arabic},
                     "style": "primary", "color": data['color'], "height": "sm", "margin": "md"}
                ],
                "paddingAll": "15px",
                "backgroundColor": "#E0E5EC",
                "spacing": "none"
            }
        })
    
    return {"type": "carousel", "contents": bubbles}

def create_stats_card(stats, uid):
    if not stats:
        return {
            "type": "bubble",
            "body": {
                "type": "box", "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "📊 إحصائياتك", "weight": "bold",
                     "size": "xl", "color": "#A3B1C6", "align": "center"},
                    {"type": "separator", "margin": "lg", "color": "#A3B1C6"},
                    {"type": "text", "text": "لم تلعب بعد", "align": "center",
                     "color": "#A3B1C6", "margin": "xl"},
                    create_neumorphic_button("🎮 ابدأ اللعب", "ابدأ", "#C3AED6")
                ],
                "paddingAll": "25px",
                "backgroundColor": "#E0E5EC"
            }
        }
    
    is_reg = "✅ مسجل" if game_manager.is_registered(uid) else "⚠️ غير مسجل"
    win_rate = (stats['wins'] / stats['games_played'] * 100) if stats['games_played'] > 0 else 0
    
    pts = stats['total_points']
    level = "🌱 مبتدئ" if pts < 100 else "⭐ متوسط" if pts < 500 else "🔥 محترف" if pts < 1000 else "👑 أسطوري"
    
    return {
        "type": "bubble",
        "size": "mega",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": level, "weight": "bold",
                 "size": "xxl", "color": "#A3B1C6", "align": "center"}
            ],
            "paddingAll": "20px",
            "backgroundColor": "#E0E5EC"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "box", "layout": "horizontal", "margin": "md",
                 "contents": [
                    {"type": "text", "text": "الحالة:", "size": "sm", "color": "#A3B1C6", "flex": 2},
                    {"type": "text", "text": is_reg, "size": "sm", "flex": 3, "align": "end", "weight": "bold", "color": "#A3B1C6"}
                ]},
                {"type": "separator", "margin": "lg", "color": "#A3B1C6"},
                {"type": "box", "layout": "horizontal", "margin": "lg", "spacing": "md",
                 "contents": [
                    {"type": "box", "layout": "vertical", "flex": 1,
                     "contents": [
                        {"type": "text", "text": "💰", "size": "xxl", "align": "center", "color": "#A3B1C6"},
                        {"type": "text", "text": str(pts), "size": "xl", "weight": "bold",
                         "align": "center", "color": "#A3B1C6"},
                        {"type": "text", "text": "نقطة", "size": "xs", "align": "center", "color": "#A3B1C6"}
                     ],
                     "backgroundColor": "#E0E5EC", "cornerRadius": "15px", "paddingAll": "15px"},
                    {"type": "box", "layout": "vertical", "flex": 1,
                     "contents": [
                        {"type": "text", "text": "🎮", "size": "xxl", "align": "center", "color": "#A3B1C6"},
                        {"type": "text", "text": str(stats['games_played']), "size": "xl", "weight": "bold",
                         "align": "center", "color": "#A3B1C6"},
                        {"type": "text", "text": "لعبة", "size": "xs", "align": "center", "color": "#A3B1C6"}
                     ],
                     "backgroundColor": "#E0E5EC", "cornerRadius": "15px", "paddingAll": "15px"}
                ]},
                {"type": "box", "layout": "horizontal", "margin": "md", "spacing": "md",
                 "contents": [
                    {"type": "box", "layout": "vertical", "flex": 1,
                     "contents": [
                        {"type": "text", "text": "🏆", "size": "xxl", "align": "center", "color": "#A3B1C6"},
                        {"type": "text", "text": str(stats['wins']), "size": "xl", "weight": "bold",
                         "align": "center", "color": "#A3B1C6"},
                        {"type": "text", "text": "فوز", "size": "xs", "align": "center", "color": "#A3B1C6"}
                     ],
                     "backgroundColor": "#E0E5EC", "cornerRadius": "15px", "paddingAll": "15px"},
                    {"type": "box", "layout": "vertical", "flex": 1,
                     "contents": [
                        {"type": "text", "text": "📈", "size": "xxl", "align": "center", "color": "#A3B1C6"},
                        {"type": "text", "text": f"{win_rate:.0f}%", "size": "xl", "weight": "bold",
                         "align": "center", "color": "#A3B1C6"},
                        {"type": "text", "text": "نسبة فوز", "size": "xs", "align": "center", "color": "#A3B1C6"}
                     ],
                     "backgroundColor": "#E0E5EC", "cornerRadius": "15px", "paddingAll": "15px"}
                ]},
                create_neumorphic_button("🎮 ابدأ لعبة", "ابدأ", "#C3AED6")
            ],
            "paddingAll": "20px",
            "backgroundColor": "#E0E5EC",
            "spacing": "none"
        }
    }

def create_leaderboard(leaders):
    if not leaders:
        return {"type": "bubble", "body": {
            "type": "box", "layout": "vertical",
            "contents": [{"type": "text", "text": "لا توجد بيانات", "align": "center", "color": "#A3B1C6"}],
            "paddingAll": "30px", "backgroundColor": "#E0E5EC"
        }}
    
    top3 = []
    medals = ["🥇", "🥈", "🥉"]
    for i, l in enumerate(leaders[:3]):
        top3.append({
            "type": "box", "layout": "horizontal",
            "contents": [
                {"type": "text", "text": medals[i], "size": "3xl", "flex": 0},
                {"type": "box", "layout": "vertical", "flex": 5,
                 "contents": [
                    {"type": "text", "text": l['display_name'], "weight": "bold",
                     "size": "md", "color": "#A3B1C6", "wrap": True},
                    {"type": "text", "text": f"⭐ {l['total_points']} | 🎮 {l['games_played']} | 🏆 {l['wins']}",
                     "size": "xs", "color": "#A3B1C6"}
                 ]}
            ],
            "backgroundColor": "#E0E5EC",
            "cornerRadius": "15px",
            "paddingAll": "15px",
            "margin": "md" if i > 0 else "none"
        })
    
    others = []
    for i, l in enumerate(leaders[3:], 4):
        others.append({
            "type": "box", "layout": "horizontal",
            "contents": [
                {"type": "text", "text": f"{i}", "size": "md", "weight": "bold",
                 "color": "#A3B1C6", "flex": 0},
                {"type": "text", "text": l['display_name'], "size": "sm",
                 "color": "#A3B1C6", "flex": 3, "wrap": True},
                {"type": "text", "text": f"{l['total_points']}⭐", "size": "sm",
                 "color": "#A3B1C6", "flex": 2, "align": "end", "weight": "bold"}
            ],
            "paddingAll": "12px",
            "margin": "sm"
        })
    
    return {
        "type": "bubble",
        "size": "mega",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": "🏆 لوحة الصدارة", "weight": "bold",
                 "size": "xxl", "color": "#A3B1C6", "align": "center"}
            ],
            "paddingAll": "20px",
            "backgroundColor": "#E0E5EC"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": top3 + others,
            "paddingAll": "20px",
            "backgroundColor": "#E0E5EC",
            "spacing": "none"
        }
    }

def create_help():
    return {
        "type": "bubble",
        "size": "mega",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": "❓ كيف ألعب؟", "weight": "bold",
                 "size": "xxl", "color": "#A3B1C6", "align": "center"}
            ],
            "paddingAll": "20px",
            "backgroundColor": "#E0E5EC"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": "خطوات سريعة:", "weight": "bold",
                 "size": "lg", "color": "#A3B1C6"},
                {"type": "box", "layout": "vertical", "margin": "lg", "spacing": "md",
                 "contents": [
                    {"type": "text", "text": "1️⃣ اكتب 'انضم' للتسجيل",
                     "size": "sm", "color": "#A3B1C6"},
                    {"type": "text", "text": "2️⃣ اكتب 'ابدأ' لعرض الألعاب",
                     "size": "sm", "color": "#A3B1C6"},
                    {"type": "text", "text": "3️⃣ اختر لعبة واستمتع!",
                     "size": "sm", "color": "#A3B1C6"}
                 ]},
                {"type": "separator", "margin": "xl", "color": "#A3B1C6"},
                {"type": "text", "text": "أوامر مفيدة:", "weight": "bold",
                 "size": "md", "color": "#A3B1C6", "margin": "xl"},
                {"type": "text", "text": "• نقاطي - عرض إحصائياتك\n• الصدارة - أفضل اللاعبين\n• إيقاف - إيقاف اللعبة",
                 "size": "sm", "color": "#A3B1C6", "margin": "md", "wrap": True},
                create_neumorphic_button("🎮 ابدأ الآن", "ابدأ", "#C3AED6")
            ],
            "paddingAll": "25px",
            "backgroundColor": "#E0E5EC",
            "spacing": "none"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text",
                 "text": "تم إنشاء هذا البوت بواسطة\nعبير الدوسري © 2025",
                 "size": "xxs",
                 "color": "#A3B1C6",
                 "align": "center",
                 "wrap": True}
            ],
            "paddingAll": "15px",
            "backgroundColor": "#E0E5EC"
        }
    }

# ============================================
# 🎯 Command Handler
# ============================================
class CommandHandler:
    def __init__(self, gm, api):
        self.gm = gm
        self.api = api
        self.cmds = {
            'مساعدة': self.help, 'help': self.help,
            'انضم': self.join, 'تسجيل': self.join,
            'انسحب': self.leave, 'خروج': self.leave,
            'ابدأ': self.start, 'start': self.start,
            'نقاطي': self.stats, 'احصائياتي': self.stats,
            'الصدارة': self.leaderboard,
            'إيقاف': self.stop, 'ايقاف': self.stop
        }
    
    def handle(self, event, uid, text, gid, name):
        handler = self.cmds.get(text)
        if handler:
            return handler(event, uid, gid, name)
        return False
    
    def help(self, event, *args):
        self.api.reply_message(event.reply_token,
            FlexSendMessage(alt_text="المساعدة", contents=create_help()))
        return True
    
    def join(self, event, uid, gid, name):
        if self.gm.is_registered(uid):
            self.api.reply_message(event.reply_token,
                TextSendMessage(text=f"✅ أنت مسجل بالفعل يا {name}\n\nاكتب 'ابدأ' للعب"))
        else:
            self.gm.register(uid)
            self.api.reply_message(event.reply_token,
                FlexSendMessage(alt_text="مرحباً", contents=create_main_menu()))
        return True
    
    def leave(self, event, uid, *args):
        if self.gm.is_registered(uid):
            self.gm.unregister(uid)
            self.api.reply_message(event.reply_token,
                TextSendMessage(text="👋 تم الانسحاب بنجاح"))
        else:
            self.api.reply_message(event.reply_token,
                TextSendMessage(text="❌ أنت غير مسجل"))
        return True
    
    def start(self, event, *args):
        if not AVAILABLE_GAMES:
            self.api.reply_message(event.reply_token,
                TextSendMessage(text="⚠️ لا توجد ألعاب متاحة حالياً"))
        else:
            self.api.reply_message(event.reply_token,
                FlexSendMessage(alt_text="اختر لعبة", contents=create_games_grid()))
        return True
    
    def stats(self, event, uid, *args):
        stats = get_stats(uid)
        self.api.reply_message(event.reply_token,
            FlexSendMessage(alt_text="إحصائياتك", contents=create_stats_card(stats, uid)))
        return True
    
    def leaderboard(self, event, *args):
        leaders = get_leaderboard()
        self.api.reply_message(event.reply_token,
            FlexSendMessage(alt_text="الصدارة", contents=create_leaderboard(leaders)))
        return True
    
    def stop(self, event, uid, gid, *args):
        if self.gm.is_active(gid):
            data = self.gm.get_game(gid)
            self.gm.end_game(gid)
            self.api.reply_message(event.reply_token,
                TextSendMessage(text=f"⏸️ تم إيقاف لعبة {data['type']}"))
        else:
            self.api.reply_message(event.reply_token,
                TextSendMessage(text="❌ لا توجد لعبة نشطة"))
        return True

cmd_handler = CommandHandler(game_manager, line_bot_api)

# ============================================
# 🎮 Game Functions
# ============================================
def start_game(gid, game_class, gtype, uid, event):
    try:
        ai_games = ['IQGame', 'WordColorGame', 'LettersWordsGame', 'HumanAnimalPlantGame']
        
        if game_class.__name__ in ai_games:
            game = game_class(line_bot_api, use_ai=USE_AI,
                            get_api_key=get_gemini_api_key, switch_key=switch_gemini_key)
        else:
            game = game_class(line_bot_api)
        
        game_manager.create_game(gid, game, gtype)
        response = game.start_game()
        line_bot_api.reply_message(event.reply_token, response)
        metrics.increment('games_started')
        logger.info(f"✅ Game started: {gtype}")
        return True
    except Exception as e:
        logger.error(f"❌ Game error: {e}")
        line_bot_api.reply_message(event.reply_token,
            TextSendMessage(text=f"❌ خطأ في بدء اللعبة"))
        return False

def handle_answer(event, uid, text, gid, name):
    data = game_manager.get_game(gid)
    if not data:
        return
    
    game = data['game']
    gtype = data['type']
    
    try:
        result = game.check_answer(text, uid, name)
        if result:
            points = result.get('points', 0)
            if points > 0:
                update_points(uid, name, points, result.get('won', False), gtype)
            
            if result.get('game_over', False):
                game_manager.end_game(gid)
            
            response = result.get('response', TextSendMessage(text=result.get('message', '')))
            line_bot_api.reply_message(event.reply_token, response)
    except Exception as e:
        logger.error(f"❌ Answer error: {e}")

# ============================================
# 🌐 Flask Routes
# ============================================
@app.route("/", methods=['GET'])
def home():
    return f'''<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Bot Mesh</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'Segoe UI',sans-serif;background:linear-gradient(135deg,#667eea,#764ba2);
color:#fff;min-height:100vh;display:flex;align-items:center;justify-content:center;padding:20px}}
.container{{background:rgba(255,255,255,0.1);backdrop-filter:blur(10px);padding:40px;
border-radius:20px;max-width:800px;width:100%;box-shadow:0 8px 32px rgba(31,38,135,0.37)}}
h1{{font-size:3em;margin-bottom:10px;text-align:center;animation:fadeIn 1s}}
.status{{text-align:center;font-size:1.2em;margin-bottom:30px;color:#4ade80}}
.stats{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:20px;margin:30px 0}}
.box{{background:rgba(255,255,255,0.2);border-radius:15px;padding:20px;text-align:center;
transition:transform 0.3s;animation:slideUp 0.5s}}
.box:hover{{transform:translateY(-5px)}}
.num{{font-size:2.5em;font-weight:bold;margin:10px 0}}
.label{{font-size:0.9em;opacity:0.9;text-transform:uppercase}}
@keyframes fadeIn{{from{{opacity:0}}to{{opacity:1}}}}
@keyframes slideUp{{from{{transform:translateY(20px);opacity:0}}to{{transform:translateY(0);opacity:1}}}}
</style></head><body>
<div class="container">
<h1>🎮 Bot Mesh</h1>
<p class="status">✅ Neumorphism Design Active</p>
<div class="stats">
<div class="box"><div class="num">{len(GAMES_LOADED)}</div><div class="label">Games</div></div>
<div class="box"><div class="num">{len(game_manager.registered)}</div><div class="label">Players</div></div>
<div class="box"><div class="num">{len(game_manager.active_games)}</div><div class="label">Active</div></div>
<div class="box"><div class="num">{metrics.requests}</div><div class="label">Requests</div></div>
</div>
<p style="text-align:center;margin-top:30px;opacity:0.8">Created by Abeer Aldosari © 2025</p>
</div></body></html>'''

@app.route("/health", methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'games': len(GAMES_LOADED)}), 200

@app.route("/callback", methods=['POST'])
def callback():
    sig = request.headers.get('X-Line-Signature')
    if not sig:
        abort(400)
    
    body = request.get_data(as_text=True)
    metrics.increment('requests')
    
    try:
        handler.handle(body, sig)
    except InvalidSignatureError:
        abort(400)
    except Exception as e:
        logger.error(f"❌ Callback error: {e}")
        abort(500)
    
    return 'OK'

# ============================================
# 📨 Message Handler
# ============================================
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    try:
        uid = event.source.user_id
        text = event.message.text.strip()
        gid = getattr(event.source, 'group_id', uid)
        name = get_profile(uid)
        
        logger.info(f"📨 {name}: {text}")
        
        # أوامر البوت فقط
        if cmd_handler.handle(event, uid, text, gid, name):
            return
        
        # بدء الألعاب (المسجلين فقط)
        if text in AVAILABLE_GAMES:
            if not game_manager.is_registered(uid):
                line_bot_api.reply_message(event.reply_token,
                    TextSendMessage(text="❌ يجب التسجيل أولاً\n\nاكتب 'انضم'"))
                return
            
            game_data = AVAILABLE_GAMES[text]
            game_class = GAMES_LOADED.get(game_data['class'])
            
            if not game_class:
                line_bot_api.reply_message(event.reply_token,
                    TextSendMessage(text=f"❌ اللعبة غير متاحة"))
                return
            
            # لعبة التوافق
            if text == 'توافق':
                game = game_class(line_bot_api)
                game_manager.create_game(gid, game, text)
                line_bot_api.reply_message(event.reply_token,
                    TextSendMessage(text="💖 لعبة التوافق!\n\nاكتب اسمين مفصولين بمسافة\nمثال: أحمد فاطمة"))
                return
            
            start_game(gid, game_class, text, uid, event)
            return
        
        # إجابات الألعاب (المسجلين فقط)
        if game_manager.is_active(gid):
            if not game_manager.is_registered(uid):
                return
            handle_answer(event, uid, text, gid, name)
            return
        
        # رسائل عامة - لا نرد
        logger.debug(f"🔇 Ignored: {text}")
        
    except Exception as e:
        logger.error(f"❌ Error: {e}", exc_info=True)

# ============================================
# 🚨 Error Handlers
# ============================================
@app.errorhandler(400)
def bad_request(e):
    return jsonify({'error': 'Bad Request'}), 400

@app.errorhandler(500)
def internal_error(e):
    return jsonify({'error': 'Internal Error'}), 500

# ============================================
# 🛑 Graceful Shutdown
# ============================================
def shutdown(signum, frame):
    logger.info("🛑 Shutting down...")
    with db_pool.lock:
        for conn in db_pool.pool:
            conn.close()
    exit(0)

signal.signal(signal.SIGTERM, shutdown)
signal.signal(signal.SIGINT, shutdown)

# ============================================
# 🚀 Entry Point
# ============================================
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    
    logger.info("=" * 60)
    logger.info("🎮 BOT MESH - Neumorphism Design")
    logger.info("=" * 60)
    logger.info(f"🌐 Port: {port}")
    logger.info(f"🎯 Games: {len(GAMES_LOADED)}")
    logger.info(f"✨ Available: {len(AVAILABLE_GAMES)}")
    logger.info(f"📊 Registered: {len(game_manager.registered)}")
    logger.info(f"🤖 AI: {'✅' if USE_AI else '❌'}")
    logger.info("=" * 60)
    logger.info("Created by: Abeer Aldosari © 2025")
    logger.info("=" * 60)
    
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
