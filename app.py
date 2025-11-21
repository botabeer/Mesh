from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage, QuickReply, QuickReplyButton, MessageAction
import os
from datetime import datetime, timedelta
import sqlite3
from collections import defaultdict
import threading
import time
import logging
import json

# إعداد السجلات
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# استيراد الألعاب
GAMES_LOADED = {}
game_imports = [
    ('games.iq_game', 'IQGame'),
    ('games.word_color_game', 'WordColorGame'),
    ('games.chain_words_game', 'ChainWordsGame'),
    ('games.scramble_word_game', 'ScrambleWordGame'),
    ('games.letters_words_game', 'LettersWordsGame'),
    ('games.fast_typing_game', 'FastTypingGame'),
    ('games.human_animal_plant_game', 'HumanAnimalPlantGame'),
    ('games.guess_game', 'GuessGame'),
    ('games.compatibility_game', 'CompatibilityGame'),
    ('games.math_game', 'MathGame'),
    ('games.memory_game', 'MemoryGame'),
    ('games.riddle_game', 'RiddleGame'),
    ('games.opposite_game', 'OppositeGame'),
    ('games.emoji_game', 'EmojiGame'),
    ('games.song_game', 'SongGame')
]

for module_name, class_name in game_imports:
    try:
        module = __import__(module_name, fromlist=[class_name])
        GAMES_LOADED[class_name] = getattr(module, class_name)
    except:
        logger.warning(f"⚠️ {class_name} غير متاح")

logger.info(f"✅ تم تحميل {len(GAMES_LOADED)} لعبة")

app = Flask(__name__)

# إعدادات LINE Bot
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', 'YOUR_TOKEN')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET', 'YOUR_SECRET')
BOT_NAME = os.getenv('BOT_MESH', 'Bot Mesh')  # اسم البوت للمنشن

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# إعدادات Gemini AI
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
# 🎮 نظام إدارة اللاعبين والألعاب
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
                'game': game_obj,
                'type': game_type,
                'created_at': datetime.now()
            }
    
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

# قاعدة البيانات
DB_NAME = 'game_scores.db'

def get_db_connection():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    try:
        conn = get_db_connection()
        c = conn.cursor()
        
        # جدول المستخدمين
        c.execute('''CREATE TABLE IF NOT EXISTS users
                     (user_id TEXT PRIMARY KEY, 
                      display_name TEXT, 
                      line_display_name TEXT,
                      total_points INTEGER DEFAULT 0,
                      games_played INTEGER DEFAULT 0, 
                      wins INTEGER DEFAULT 0, 
                      last_played TEXT,
                      registered_at TEXT DEFAULT CURRENT_TIMESTAMP,
                      last_updated TEXT DEFAULT CURRENT_TIMESTAMP)''')
        
        # جدول سجل الألعاب
        c.execute('''CREATE TABLE IF NOT EXISTS game_history
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                      user_id TEXT, 
                      game_type TEXT,
                      points INTEGER, 
                      won INTEGER, 
                      played_at TEXT DEFAULT CURRENT_TIMESTAMP,
                      FOREIGN KEY (user_id) REFERENCES users(user_id))''')
        
        # جدول تتبع تحديث الأسماء
        c.execute('''CREATE TABLE IF NOT EXISTS name_updates
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      user_id TEXT,
                      old_name TEXT,
                      new_name TEXT,
                      updated_at TEXT DEFAULT CURRENT_TIMESTAMP)''')
        
        c.execute('CREATE INDEX IF NOT EXISTS idx_user_points ON users(total_points DESC)')
        c.execute('CREATE INDEX IF NOT EXISTS idx_game_history_user ON game_history(user_id, played_at)')
        
        conn.commit()
        conn.close()
        logger.info("✅ قاعدة البيانات جاهزة")
    except Exception as e:
        logger.error(f"❌ خطأ في قاعدة البيانات: {e}")

init_db()

def update_user_profile(user_id, current_line_name):
    """تحديث اسم المستخدم تلقائياً"""
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('SELECT display_name, line_display_name FROM users WHERE user_id = ?', (user_id,))
        user = c.fetchone()
        
        if user:
            old_name = user['line_display_name']
            if old_name != current_line_name:
                # تحديث الاسم
                c.execute('UPDATE users SET line_display_name = ?, last_updated = ? WHERE user_id = ?',
                         (current_line_name, datetime.now().isoformat(), user_id))
                
                # تسجيل التحديث
                c.execute('INSERT INTO name_updates (user_id, old_name, new_name) VALUES (?, ?, ?)',
                         (user_id, old_name, current_line_name))
                
                conn.commit()
                logger.info(f"🔄 تحديث اسم {user_id}: {old_name} → {current_line_name}")
        
        conn.close()
    except Exception as e:
        logger.error(f"❌ خطأ في تحديث الملف الشخصي: {e}")

def update_user_points(user_id, display_name, points, won=False, game_type=""):
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        user = c.fetchone()
        
        if user:
            c.execute('''UPDATE users SET total_points = ?, games_played = ?, wins = ?, 
                         last_played = ?, display_name = ?, last_updated = ? WHERE user_id = ?''',
                      (user['total_points'] + points, user['games_played'] + 1,
                       user['wins'] + (1 if won else 0), datetime.now().isoformat(), 
                       display_name, datetime.now().isoformat(), user_id))
        else:
            c.execute('''INSERT INTO users (user_id, display_name, line_display_name, total_points, 
                         games_played, wins, last_played) VALUES (?, ?, ?, ?, ?, ?, ?)''',
                      (user_id, display_name, display_name, points, 1, 1 if won else 0, 
                       datetime.now().isoformat()))
        
        if game_type:
            c.execute('INSERT INTO game_history (user_id, game_type, points, won) VALUES (?, ?, ?, ?)',
                      (user_id, game_type, points, 1 if won else 0))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        logger.error(f"❌ خطأ في تحديث النقاط: {e}")
        return False

def get_user_stats(user_id):
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        user = c.fetchone()
        conn.close()
        return user
    except Exception as e:
        logger.error(f"❌ خطأ: {e}")
        return None

def get_leaderboard(limit=10):
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('''SELECT display_name, total_points, games_played, wins 
                     FROM users ORDER BY total_points DESC LIMIT ?''', (limit,))
        leaders = c.fetchall()
        conn.close()
        return leaders
    except Exception as e:
        logger.error(f"❌ خطأ: {e}")
        return []

def cleanup_old_data():
    """حذف البيانات القديمة كل 24 ساعة"""
    while True:
        try:
            time.sleep(86400)  # 24 ساعة
            cutoff_date = (datetime.now() - timedelta(days=1)).isoformat()
            
            conn = get_db_connection()
            c = conn.cursor()
            
            # حذف سجلات الألعاب القديمة
            c.execute('DELETE FROM game_history WHERE played_at < ?', (cutoff_date,))
            
            # حذف تحديثات الأسماء القديمة
            c.execute('DELETE FROM name_updates WHERE updated_at < ?', (cutoff_date,))
            
            deleted_games = c.rowcount
            conn.commit()
            conn.close()
            
            logger.info(f"🗑️ تنظيف البيانات: حذف {deleted_games} سجل قديم")
        except Exception as e:
            logger.error(f"❌ خطأ في التنظيف: {e}")

# بدء التنظيف التلقائي
threading.Thread(target=cleanup_old_data, daemon=True).start()

def cleanup_old_games():
    """تنظيف الألعاب القديمة"""
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
                logger.info(f"🗑️ تنظيف لعبة قديمة: {game_id}")
        except Exception as e:
            logger.error(f"❌ خطأ في التنظيف: {e}")

threading.Thread(target=cleanup_old_games, daemon=True).start()

def get_user_profile_safe(user_id):
    try:
        profile = line_bot_api.get_profile(user_id)
        # تحديث الملف الشخصي تلقائياً
        update_user_profile(user_id, profile.display_name)
        return profile.display_name
    except Exception as e:
        logger.error(f"❌ خطأ في الملف الشخصي: {e}")
        return "مستخدم"

# ============================================
# 🎨 واجهات Neumorphism Soft
# ============================================

def create_main_menu():
    """القائمة الرئيسية بتصميم Neumorphism"""
    return {
        "type": "bubble",
        "size": "mega",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "image",
                            "url": "https://i.imgur.com/your-logo.png",  # ضع رابط شعارك
                            "size": "xs",
                            "aspectMode": "cover",
                            "aspectRatio": "1:1"
                        }
                    ],
                    "width": "60px",
                    "height": "60px",
                    "cornerRadius": "30px",
                    "backgroundColor": "#E0E5EC",
                    "offsetTop": "none",
                    "offsetStart": "none"
                },
                {
                    "type": "text",
                    "text": "Bot Mesh",
                    "weight": "bold",
                    "size": "xxl",
                    "color": "#7F8AB8",
                    "margin": "md"
                },
                {
                    "type": "text",
                    "text": "تأثير 3D - عمق ناعم",
                    "size": "sm",
                    "color": "#A3AED0",
                    "margin": "sm"
                },
                {
                    "type": "separator",
                    "margin": "xl",
                    "color": "#E0E5EC"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "button",
                            "action": {
                                "type": "message",
                                "label": "📝 انضم للعب",
                                "text": "انضم"
                            },
                            "style": "primary",
                            "color": "#7F8AB8",
                            "height": "sm"
                        },
                        {
                            "type": "button",
                            "action": {
                                "type": "message",
                                "label": "🎮 ابدأ اللعب",
                                "text": "ابدأ"
                            },
                            "style": "primary",
                            "color": "#6B7AA1",
                            "height": "sm",
                            "margin": "md"
                        },
                        {
                            "type": "button",
                            "action": {
                                "type": "message",
                                "label": "📊 نقاطي",
                                "text": "نقاطي"
                            },
                            "style": "secondary",
                            "height": "sm",
                            "margin": "md"
                        },
                        {
                            "type": "button",
                            "action": {
                                "type": "message",
                                "label": "🏆 الصدارة",
                                "text": "الصدارة"
                            },
                            "style": "secondary",
                            "height": "sm",
                            "margin": "md"
                        }
                    ],
                    "margin": "xl"
                }
            ],
            "paddingAll": "20px",
            "backgroundColor": "#E0E5EC"
        }
    }

def create_games_carousel():
    """قائمة الألعاب بتصميم Neumorphism - Carousel"""
    games_data = [
        {"name": "ذكاء", "emoji": "🧠", "desc": "اختبر ذكاءك"},
        {"name": "لون", "emoji": "🎨", "desc": "كلمة ولون"},
        {"name": "سلسلة", "emoji": "⛓️", "desc": "سلسلة الكلمات"},
        {"name": "ترتيب", "emoji": "🔤", "desc": "رتب الحروف"},
        {"name": "تكوين", "emoji": "✍️", "desc": "كون كلمات"},
        {"name": "أسرع", "emoji": "⚡", "desc": "اكتب بسرعة"},
        {"name": "لعبة", "emoji": "🎯", "desc": "إنسان حيوان نبات"},
        {"name": "خمن", "emoji": "🤔", "desc": "خمن الرقم"},
        {"name": "رياضيات", "emoji": "🔢", "desc": "حل المسائل"},
        {"name": "ذاكرة", "emoji": "🧩", "desc": "اختبر ذاكرتك"},
        {"name": "لغز", "emoji": "🎭", "desc": "حل الألغاز"},
        {"name": "ضد", "emoji": "↔️", "desc": "الأضداد"},
        {"name": "أغنية", "emoji": "🎵", "desc": "خمن الأغنية"}
    ]
    
    bubbles = []
    for game in games_data:
        bubble = {
            "type": "bubble",
            "size": "micro",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": game["emoji"],
                        "size": "xxl",
                        "align": "center"
                    },
                    {
                        "type": "text",
                        "text": f"لعبة {game['name']}",
                        "weight": "bold",
                        "size": "sm",
                        "align": "center",
                        "margin": "md",
                        "color": "#7F8AB8"
                    },
                    {
                        "type": "text",
                        "text": game["desc"],
                        "size": "xs",
                        "align": "center",
                        "color": "#A3AED0",
                        "margin": "sm"
                    },
                    {
                        "type": "button",
                        "action": {
                            "type": "message",
                            "label": "العب",
                            "text": game["name"]
                        },
                        "style": "primary",
                        "color": "#7F8AB8",
                        "height": "sm",
                        "margin": "md"
                    }
                ],
                "paddingAll": "15px",
                "backgroundColor": "#E0E5EC"
            }
        }
        bubbles.append(bubble)
    
    return {
        "type": "carousel",
        "contents": bubbles
    }

def start_game(game_id, game_class, game_type, user_id, event):
    try:
        if game_class in [GAMES_LOADED.get('IQGame'), GAMES_LOADED.get('WordColorGame'), 
                          GAMES_LOADED.get('LettersWordsGame'), GAMES_LOADED.get('HumanAnimalPlantGame')]:
            game = game_class(line_bot_api, use_ai=USE_AI, get_api_key=get_gemini_api_key, switch_key=switch_gemini_key)
        else:
            game = game_class(line_bot_api)
        
        game_manager.create_game(game_id, game, game_type)
        
        response = game.start_game()
        line_bot_api.reply_message(event.reply_token, response)
        logger.info(f"🎮 بدأت لعبة {game_type}")
        return True
    except Exception as e:
        logger.error(f"❌ خطأ في بدء اللعبة: {e}")
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f"❌ خطأ في بدء {game_type}"))
        return False

@app.route("/", methods=['GET'])
def home():
    return f'''
    <html>
        <head>
            <title>LINE Bot - بوت الألعاب</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    text-align: center;
                    padding: 50px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                }}
                .container {{
                    background: rgba(255, 255, 255, 0.1);
                    backdrop-filter: blur(10px);
                    padding: 40px;
                    border-radius: 20px;
                    max-width: 600px;
                    margin: 0 auto;
                    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
                }}
                h1 {{ font-size: 3em; margin-bottom: 10px; }}
                .stats {{ margin: 30px 0; }}
                .stat-box {{
                    display: inline-block;
                    margin: 10px 20px;
                    padding: 20px;
                    background: rgba(255, 255, 255, 0.2);
                    border-radius: 15px;
                }}
                .stat-number {{ font-size: 2em; font-weight: bold; }}
                .stat-label {{ font-size: 0.9em; opacity: 0.9; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1> Bot Mesh </h1>
                <p style="font-size: 1.2em; opacity: 0.9;">الخادم يعمل بنجاح</p>
                <div class="stats">
                    <div class="stat-box">
                        <div class="stat-number">{len(GAMES_LOADED)}</div>
                        <div class="stat-label">لعبة متاحة</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-number">{len(game_manager.registered_players)}</div>
                        <div class="stat-label">لاعب مسجل</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-number">{len(game_manager.active_games)}</div>
                        <div class="stat-label">لعبة نشطة</div>
                    </div>
                </div>
                <p style="margin-top: 30px; opacity: 0.8;">✨ تصميم Neumorphism Soft</p>
            </div>
        </body>
    </html>
    '''

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers.get('X-Line-Signature', '')
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    try:
        user_id = event.source.user_id
        text = event.message.text.strip()
        game_id = event.source.group_id if hasattr(event.source, 'group_id') else user_id
        display_name = get_user_profile_safe(user_id)
        
        logger.info(f"📨 {display_name}: {text}")
        
        # الأوامر المباشرة
        if text in ['مساعدة', 'help', 'المساعدة'] or f'@{BOT_NAME}' in text:
            menu = create_main_menu()
            line_bot_api.reply_message(event.reply_token, FlexSendMessage(alt_text="القائمة الرئيسية", contents=menu))
            return
        
        elif text in ['انضم', 'تسجيل', 'join']:
            if game_manager.is_registered(user_id):
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f"✅ أنت مسجل بالفعل يا {display_name}\n\nاكتب 'ابدأ' لاختيار لعبة"))
            else:
                game_manager.register_player(user_id)
                success_msg = {
                    "type": "bubble",
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {"type": "text", "text": "✅ تم التسجيل بنجاح!", "weight": "bold", "size": "xl", "color": "#7F8AB8", "align": "center"},
                            {"type": "text", "text": f"مرحباً {display_name}", "size": "md", "color": "#A3AED0", "align": "center", "margin": "md"},
                            {"type": "separator", "margin": "xl", "color": "#E0E5EC"},
                            {"type": "text", "text": "✨ إجاباتك ستُحسب تلقائياً\n\nاكتب 'ابدأ' لاختيار لعبة", "size": "sm", "color": "#7F8AB8", "align": "center", "wrap": True, "margin": "xl"}
                        ],
                        "paddingAll": "25px",
                        "backgroundColor": "#E0E5EC"
                    }
                }
                line_bot_api.reply_message(event.reply_token, FlexSendMessage(alt_text="تم التسجيل", contents=success_msg))
            return
        
        elif text in ['انسحب', 'خروج', 'leave']:
            if game_manager.is_registered(user_id):
                game_manager.unregister_player(user_id)
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f"👋 تم الانسحاب\n\nإجاباتك لن تُحسب بعد الآن"))
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text="❌ أنت غير مسجل"))
            return
        
        elif text in ['ابدأ', 'start', 'الألعاب']:
            games_carousel = create_games_carousel()
            line_bot_api.reply_message(event.reply_token, FlexSendMessage(alt_text="اختر لعبة", contents=games_carousel))
            return
        
        elif text == 'نقاطي':
            stats = get_user_stats(user_id)
            if stats:
                is_registered = "✅ مسجل" if game_manager.is_registered(user_id) else "❌ غير مسجل"
                win_rate = (stats['wins'] / stats['games_played'] * 100) if stats['games_played'] > 0 else 0
                
                stats_bubble = {
                    "type": "bubble",
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {"type": "text", "text": "📊 إحصائياتك", "weight": "bold", "size": "xl", "color": "#7F8AB8", "align": "center"},
                            {"type": "separator", "margin": "md", "color": "#E0E5EC"},
                            {"type": "box", "layout": "horizontal", "contents": [
                                {"type": "text", "text": "الحالة", "size": "sm", "color": "#A3AED0", "flex": 2},
                                {"type": "text", "text": is_registered, "size": "sm", "color": "#7F8AB8", "flex": 3, "align": "end", "weight": "bold"}
                            ], "margin": "md"},
                            {"type": "box", "layout": "horizontal", "contents": [
                                {"type": "text", "text": "💰 النقاط", "size": "sm", "color": "#A3AED0", "flex": 2},
                                {"type": "text", "text": str(stats['total_points']), "size": "xxl", "color": "#7F8AB8", "flex": 3, "align": "end", "weight": "bold"}
                            ], "margin": "md"},
                            {"type": "separator", "margin": "md", "color": "#E0E5EC"},
                            {"type": "box", "layout": "horizontal", "contents": [
                                {"type": "text", "text": "🎮 ألعاب", "size": "sm", "color": "#A3AED0", "flex": 2},
                                {"type": "text", "text": str(stats['games_played']), "size": "sm", "color": "#7F8AB8", "flex": 3, "align": "end"}
                            ], "margin": "md"},
                            {"type": "box", "layout": "horizontal", "contents": [
                                {"type": "text", "text": "🏆 فوز", "size": "sm", "color": "#A3AED0", "flex": 2},
                                {"type": "text", "text": str(stats['wins']), "size": "sm", "color": "#7F8AB8", "flex": 3, "align": "end"}
                            ], "margin": "sm"},
                            {"type": "box", "layout": "horizontal", "contents": [
                                {"type": "text", "text": "📈 نسبة الفوز", "size": "sm", "color": "#A3AED0", "flex": 2},
                                {"type": "text", "text": f"{win_rate:.1f}%", "size": "sm", "color": "#7F8AB8", "flex": 3, "align": "end"}
                            ], "margin": "sm"}
                        ],
                        "paddingAll": "20px",
                        "backgroundColor": "#E0E5EC"
                    }
                }
                line_bot_api.reply_message(event.reply_token, FlexSendMessage(alt_text="إحصائياتك", contents=stats_bubble))
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text="❌ لم تلعب بعد\n\nاكتب 'انضم' ثم 'ابدأ'"))
            return
        
        elif text == 'الصدارة':
            leaders = get_leaderboard()
            if leaders:
                players_content = []
                for i, leader in enumerate(leaders, 1):
                    medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}️⃣"
                    bg_color = "#7F8AB8" if i <= 3 else "#E0E5EC"
                    text_color = "#FFFFFF" if i <= 3 else "#7F8AB8"
                    
                    player_box = {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {"type": "text", "text": medal, "size": "sm", "flex": 0, "margin": "sm"},
                            {"type": "text", "text": leader['display_name'], "size": "sm", "color": text_color, "flex": 3, "weight": "bold" if i <= 3 else "regular"},
                            {"type": "text", "text": f"{leader['total_points']}⭐", "size": "sm", "color": text_color, "flex": 2, "align": "end", "weight": "bold" if i <= 3 else "regular"}
                        ],
                        "backgroundColor": bg_color,
                        "cornerRadius": "md",
                        "paddingAll": "12px",
                        "margin": "xs" if i > 1 else "none"
                    }
                    players_content.append(player_box)
                
                leaderboard = {
                    "type": "bubble",
                    "size": "mega",
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {"type": "text", "text": "🏆 لوحة الصدارة", "weight": "bold", "size": "xl", "color": "#7F8AB8", "align": "center"},
                            {"type": "separator", "margin": "md", "color": "#E0E5EC"}
                        ] + players_content,
                        "paddingAll": "20px",
                        "backgroundColor": "#E0E5EC"
                    }
                }
                line_bot_api.reply_message(event.reply_token, FlexSendMessage(alt_text="الصدارة", contents=leaderboard))
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text="❌ لا توجد بيانات"))
            return
        
        elif text in ['إيقاف', 'ايقاف', 'stop', 'توقف']:
            if game_manager.is_game_active(game_id):
                game_data = game_manager.get_game(game_id)
                game_type = game_data['type']
                game_manager.end_game(game_id)
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f"⏸️ تم إيقاف لعبة {game_type}\n\nاكتب 'ابدأ' للعب مرة أخرى"))
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text="❌ لا توجد لعبة نشطة"))
            return
        
        elif text in ['إعادة', 'اعادة', 'restart', 'مرة أخرى']:
            if game_manager.is_game_active(game_id):
                game_data = game_manager.get_game(game_id)
                game_type = game_data['type']
                game_manager.end_game(game_id)
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f"🔄 تم إعادة تعيين اللعبة\n\nاكتب '{game_type}' للبدء من جديد"))
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text="❌ لا توجد لعبة نشطة"))
            return
        
        # بدء الألعاب
        games_map = {
            'ذكاء': ('IQGame', 'ذكاء'),
            'لون': ('WordColorGame', 'لون'),
            'سلسلة': ('ChainWordsGame', 'سلسلة'),
            'ترتيب': ('ScrambleWordGame', 'ترتيب'),
            'تكوين': ('LettersWordsGame', 'تكوين'),
            'أسرع': ('FastTypingGame', 'أسرع'),
            'لعبة': ('HumanAnimalPlantGame', 'لعبة'),
            'خمن': ('GuessGame', 'خمن'),
            'توافق': ('CompatibilityGame', 'توافق'),
            'رياضيات': ('MathGame', 'رياضيات'),
            'ذاكرة': ('MemoryGame', 'ذاكرة'),
            'لغز': ('RiddleGame', 'لغز'),
            'ضد': ('OppositeGame', 'ضد'),
            'إيموجي': ('EmojiGame', 'إيموجي'),
            'أغنية': ('SongGame', 'أغنية')
        }
        
        if text in games_map:
            if not game_manager.is_registered(user_id):
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text="❌ يجب التسجيل أولاً\n\nاكتب 'انضم' للتسجيل"))
                return
            
            class_name, game_type = games_map[text]
            game_class = GAMES_LOADED.get(class_name)
            
            if not game_class:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f"❌ لعبة {game_type} غير متاحة حالياً"))
                return
            
            # لعبة التوافق حالة خاصة
            if text == 'توافق':
                game = game_class(line_bot_api)
                game_manager.create_game(game_id, game, 'توافق')
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text="💖 لعبة التوافق!\n\nاكتب اسمين مفصولين بمسافة\nمثال: أحمد فاطمة"))
                return
            
            start_game(game_id, game_class, game_type, user_id, event)
            return
        
        # معالجة إجابات الألعاب النشطة
        if game_manager.is_game_active(game_id):
            # التحقق من التسجيل
            if not game_manager.is_registered(user_id):
                logger.debug(f"🔇 إجابة من مستخدم غير مسجل: {user_id}")
                return
            
            game_data = game_manager.get_game(game_id)
            game = game_data['game']
            game_type = game_data['type']
            
            try:
                result = game.check_answer(text, user_id, display_name)
                if result:
                    points = result.get('points', 0)
                    if points > 0:
                        update_user_points(user_id, display_name, points, result.get('won', False), game_type)
                    
                    if result.get('game_over', False):
                        game_manager.end_game(game_id)
                        response = TextSendMessage(text=result.get('message', '🏁 انتهت اللعبة!\n\nاكتب "ابدأ" للعب مرة أخرى'))
                    else:
                        response = result.get('response', TextSendMessage(text=result.get('message', '')))
                    
                    line_bot_api.reply_message(event.reply_token, response)
                return
            except Exception as e:
                logger.error(f"❌ خطأ في معالجة الإجابة: {e}")
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text="❌ حدث خطأ. حاول مرة أخرى"))
                return
        
        # إذا لم يتطابق مع أي شيء، لا نرد (تجنب الإزعاج)
        logger.debug(f"🔇 رسالة عادية تم تجاهلها: {text}")
        
    except Exception as e:
        logger.error(f"❌ خطأ في معالجة الرسالة: {e}", exc_info=True)

@app.errorhandler(Exception)
def handle_error(error):
    logger.error(f"❌ خطأ غير متوقع: {error}", exc_info=True)
    return 'Internal Server Error', 500

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"🚀 بدء الخادم على المنفذ {port}")
    logger.info(f"🎮 الألعاب المحملة: {len(GAMES_LOADED)}")
    logger.info(f"📊 اللاعبون المسجلون: {len(game_manager.registered_players)}")
    logger.info(f"🎯 الألعاب النشطة: {len(game_manager.active_games)}")
    app.run(host='0.0.0.0', port=port, debug=False)
