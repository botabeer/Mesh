from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, QuickReply, QuickReplyButton, MessageAction, FlexSendMessage
import os
from datetime import datetime, timedelta
import sqlite3
from collections import defaultdict
import threading
import time
import re
import logging

# إعداد السجلات
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# استيراد الألعاب
GAMES_LOADED = {}
try:
    from games.iq_game import IQGame
    GAMES_LOADED['IQGame'] = IQGame
except: logger.warning("⚠️ IQGame غير متاح")

try:
    from games.word_color_game import WordColorGame
    GAMES_LOADED['WordColorGame'] = WordColorGame
except: logger.warning("⚠️ WordColorGame غير متاح")

try:
    from games.chain_words_game import ChainWordsGame
    GAMES_LOADED['ChainWordsGame'] = ChainWordsGame
except: logger.warning("⚠️ ChainWordsGame غير متاح")

try:
    from games.scramble_word_game import ScrambleWordGame
    GAMES_LOADED['ScrambleWordGame'] = ScrambleWordGame
except: logger.warning("⚠️ ScrambleWordGame غير متاح")

try:
    from games.letters_words_game import LettersWordsGame
    GAMES_LOADED['LettersWordsGame'] = LettersWordsGame
except: logger.warning("⚠️ LettersWordsGame غير متاح")

try:
    from games.fast_typing_game import FastTypingGame
    GAMES_LOADED['FastTypingGame'] = FastTypingGame
except: logger.warning("⚠️ FastTypingGame غير متاح")

try:
    from games.human_animal_plant_game import HumanAnimalPlantGame
    GAMES_LOADED['HumanAnimalPlantGame'] = HumanAnimalPlantGame
except: logger.warning("⚠️ HumanAnimalPlantGame غير متاح")

try:
    from games.guess_game import GuessGame
    GAMES_LOADED['GuessGame'] = GuessGame
except: logger.warning("⚠️ GuessGame غير متاح")

try:
    from games.compatibility_game import CompatibilityGame
    GAMES_LOADED['CompatibilityGame'] = CompatibilityGame
except: logger.warning("⚠️ CompatibilityGame غير متاح")

try:
    from games.math_game import MathGame
    GAMES_LOADED['MathGame'] = MathGame
except: logger.warning("⚠️ MathGame غير متاح")

try:
    from games.memory_game import MemoryGame
    GAMES_LOADED['MemoryGame'] = MemoryGame
except: logger.warning("⚠️ MemoryGame غير متاح")

try:
    from games.riddle_game import RiddleGame
    GAMES_LOADED['RiddleGame'] = RiddleGame
except: logger.warning("⚠️ RiddleGame غير متاح")

try:
    from games.opposite_game import OppositeGame
    GAMES_LOADED['OppositeGame'] = OppositeGame
except: logger.warning("⚠️ OppositeGame غير متاح")

try:
    from games.emoji_game import EmojiGame
    GAMES_LOADED['EmojiGame'] = EmojiGame
except: logger.warning("⚠️ EmojiGame غير متاح")

try:
    from games.song_game import SongGame
    GAMES_LOADED['SongGame'] = SongGame
except: logger.warning("⚠️ SongGame غير متاح")

logger.info(f"✅ تم تحميل {len(GAMES_LOADED)} لعبة")

app = Flask(__name__)

# إعدادات LINE Bot
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', 'YOUR_TOKEN')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET', 'YOUR_SECRET')

if LINE_CHANNEL_ACCESS_TOKEN == 'YOUR_TOKEN':
    logger.warning("⚠️ LINE_CHANNEL_ACCESS_TOKEN غير محدد")
if LINE_CHANNEL_SECRET == 'YOUR_SECRET':
    logger.warning("⚠️ LINE_CHANNEL_SECRET غير محدد")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# إعدادات Gemini AI
GEMINI_API_KEYS = [k for k in [os.getenv(f'GEMINI_API_KEY_{i}', '') for i in range(1, 4)] if k]
current_gemini_key_index = 0
USE_AI = bool(GEMINI_API_KEYS)

logger.info(f"🔑 عدد مفاتيح Gemini: {len(GEMINI_API_KEYS)}")

def get_gemini_api_key():
    return GEMINI_API_KEYS[current_gemini_key_index] if GEMINI_API_KEYS else None

def switch_gemini_key():
    global current_gemini_key_index
    if len(GEMINI_API_KEYS) > 1:
        current_gemini_key_index = (current_gemini_key_index + 1) % len(GEMINI_API_KEYS)
        logger.info(f"🔄 تبديل إلى مفتاح {current_gemini_key_index + 1}")
        return True
    return False

# متغيرات عامة
active_games = {}
registered_players = set()
user_message_count = defaultdict(lambda: {'count': 0, 'reset_time': datetime.now()})
games_lock = threading.Lock()
players_lock = threading.Lock()

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
        c.execute('''CREATE TABLE IF NOT EXISTS users
                     (user_id TEXT PRIMARY KEY, display_name TEXT, total_points INTEGER DEFAULT 0,
                      games_played INTEGER DEFAULT 0, wins INTEGER DEFAULT 0, last_played TEXT,
                      registered_at TEXT DEFAULT CURRENT_TIMESTAMP)''')
        c.execute('''CREATE TABLE IF NOT EXISTS game_history
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT, game_type TEXT,
                      points INTEGER, won INTEGER, played_at TEXT DEFAULT CURRENT_TIMESTAMP,
                      FOREIGN KEY (user_id) REFERENCES users(user_id))''')
        c.execute('CREATE INDEX IF NOT EXISTS idx_user_points ON users(total_points DESC)')
        c.execute('CREATE INDEX IF NOT EXISTS idx_game_history_user ON game_history(user_id, played_at)')
        conn.commit()
        conn.close()
        logger.info("✅ قاعدة البيانات جاهزة")
    except Exception as e:
        logger.error(f"❌ خطأ في قاعدة البيانات: {e}")

init_db()

def update_user_points(user_id, display_name, points, won=False, game_type=""):
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        user = c.fetchone()
        if user:
            c.execute('''UPDATE users SET total_points = ?, games_played = ?, wins = ?, 
                         last_played = ?, display_name = ? WHERE user_id = ?''',
                      (user['total_points'] + points, user['games_played'] + 1,
                       user['wins'] + (1 if won else 0), datetime.now().isoformat(), display_name, user_id))
        else:
            c.execute('''INSERT INTO users (user_id, display_name, total_points, games_played, wins, last_played)
                         VALUES (?, ?, ?, ?, ?, ?)''',
                      (user_id, display_name, points, 1, 1 if won else 0, datetime.now().isoformat()))
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
        c.execute('SELECT display_name, total_points, games_played, wins FROM users ORDER BY total_points DESC LIMIT ?', (limit,))
        leaders = c.fetchall()
        conn.close()
        return leaders
    except Exception as e:
        logger.error(f"❌ خطأ: {e}")
        return []

def check_rate_limit(user_id, max_messages=20, time_window=60):
    now = datetime.now()
    user_data = user_message_count[user_id]
    if now - user_data['reset_time'] > timedelta(seconds=time_window):
        user_data['count'] = 0
        user_data['reset_time'] = now
    if user_data['count'] >= max_messages:
        return False
    user_data['count'] += 1
    return True

def cleanup_old_games():
    while True:
        try:
            time.sleep(300)
            now = datetime.now()
            to_delete = []
            with games_lock:
                for game_id, game_data in active_games.items():
                    if now - game_data.get('created_at', now) > timedelta(minutes=10):
                        to_delete.append(game_id)
                for game_id in to_delete:
                    del active_games[game_id]
                    logger.info(f"🗑️ تنظيف لعبة: {game_id}")
        except Exception as e:
            logger.error(f"❌ خطأ في التنظيف: {e}")

threading.Thread(target=cleanup_old_games, daemon=True).start()

def get_quick_reply():
    return QuickReply(items=[
        QuickReplyButton(action=MessageAction(label="أسرع", text="أسرع")),
        QuickReplyButton(action=MessageAction(label="ذكاء", text="ذكاء")),
        QuickReplyButton(action=MessageAction(label="لون", text="كلمة ولون")),
        QuickReplyButton(action=MessageAction(label="أغنية", text="أغنية")),
        QuickReplyButton(action=MessageAction(label="سلسلة", text="سلسلة")),
        QuickReplyButton(action=MessageAction(label="ترتيب", text="ترتيب الحروف")),
        QuickReplyButton(action=MessageAction(label="تكوين", text="تكوين كلمات")),
        QuickReplyButton(action=MessageAction(label="لعبة", text="لعبة")),
        QuickReplyButton(action=MessageAction(label="خمن", text="خمن")),
        QuickReplyButton(action=MessageAction(label="ضد", text="ضد")),
        QuickReplyButton(action=MessageAction(label="ذاكرة", text="ذاكرة")),
        QuickReplyButton(action=MessageAction(label="لغز", text="لغز")),
        QuickReplyButton(action=MessageAction(label="رياضيات", text="رياضيات"))
    ])

def get_user_profile_safe(user_id):
    try:
        profile = line_bot_api.get_profile(user_id)
        return profile.display_name
    except Exception as e:
        logger.error(f"❌ خطأ في الملف الشخصي: {e}")
        return "مستخدم"

def start_game(game_id, game_class, game_type, user_id, event):
    try:
        with games_lock:
            if game_class in [IQGame, WordColorGame, LettersWordsGame, HumanAnimalPlantGame]:
                game = game_class(line_bot_api, use_ai=USE_AI, get_api_key=get_gemini_api_key, switch_key=switch_gemini_key)
            else:
                game = game_class(line_bot_api)
            with players_lock:
                participants = registered_players.copy()
                participants.add(user_id)
            active_games[game_id] = {'game': game, 'type': game_type, 'created_at': datetime.now(), 'participants': participants}
        response = game.start_game()
        line_bot_api.reply_message(event.reply_token, response)
        logger.info(f"🎮 بدأت لعبة {game_type}")
        return True
    except Exception as e:
        logger.error(f"❌ خطأ في بدء اللعبة: {e}")
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f"❌ خطأ في بدء {game_type}", quick_reply=get_quick_reply()))
        return False

@app.route("/", methods=['GET'])
def home():
    return f'''<html><head><title>LINE Bot</title><style>body{{font-family:Arial;text-align:center;padding:50px;background:#f5f5f5}}h1{{color:#00B900}}.status{{background:white;padding:20px;border-radius:10px;margin:20px auto;max-width:600px}}</style></head><body><h1>🎮 LINE Bot Game Server</h1><div class="status"><h2>✅ الخادم يعمل</h2><p>البوت جاهز لاستقبال الرسائل</p><p><strong>الألعاب:</strong> 15 لعبة</p><p><strong>اللاعبون:</strong> {len(registered_players)}</p><p><strong>الألعاب النشطة:</strong> {len(active_games)}</p></div></body></html>'''

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers.get('X-Line-Signature', '')
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        logger.error("❌ توقيع غير صالح")
        abort(400)
    except Exception as e:
        logger.error(f"❌ خطأ: {e}")
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    try:
        user_id = event.source.user_id
        text = event.message.text.strip()
        
        if not check_rate_limit(user_id):
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="⚠️ كثير من الرسائل! انتظر دقيقة."))
            return
        
        display_name = get_user_profile_safe(user_id)
        game_id = event.source.group_id if hasattr(event.source, 'group_id') else user_id
        
        logger.info(f"📨 {display_name}: {text}")
        
        # الأوامر الأساسية
        if text in ['البداية', 'ابدأ', 'start', 'قائمة', 'البوت']:
            welcome = {
                "type": "bubble", "size": "mega",
                "header": {"type": "box", "layout": "vertical", "contents": [
                    {"type": "text", "text": "منصة الألعاب", "weight": "bold", "size": "xxl", "color": "#1a1a1a", "align": "center"},
                    {"type": "text", "text": f"مرحباً {display_name}", "size": "md", "color": "#6a6a6a", "align": "center", "margin": "sm"}
                ], "backgroundColor": "#ffffff", "paddingAll": "24px"},
                "body": {"type": "box", "layout": "vertical", "contents": [
                    {"type": "text", "text": "اضغط 'انضم' للتسجيل ثم اختر لعبة", "size": "sm", "color": "#4a4a4a", "align": "center", "wrap": True},
                    {"type": "text", "text": "15 لعبة متاحة", "size": "xs", "color": "#9a9a9a", "align": "center", "margin": "lg"}
                ], "backgroundColor": "#ffffff", "paddingAll": "20px"},
                "footer": {"type": "box", "layout": "horizontal", "contents": [
                    {"type": "button", "action": {"type": "message", "label": "انضم", "text": "انضم"}, "style": "primary", "color": "#2a2a2a"},
                    {"type": "button", "action": {"type": "message", "label": "مساعدة", "text": "مساعدة"}, "style": "secondary"}
                ], "spacing": "sm", "backgroundColor": "#f8f8f8", "paddingAll": "16px"}
            }
            line_bot_api.reply_message(event.reply_token, FlexSendMessage(alt_text="مرحباً", contents=welcome, quick_reply=get_quick_reply()))
            return
        
        elif text == 'نقاطي':
            stats = get_user_stats(user_id)
            if stats:
                status = "مسجل" if user_id in registered_players else "غير مسجل"
                win_rate = (stats['wins'] / stats['games_played'] * 100) if stats['games_played'] > 0 else 0
                stats_msg = {
                    "type": "bubble", "header": {"type": "box", "layout": "vertical", "contents": [
                        {"type": "text", "text": "إحصائياتك", "weight": "bold", "size": "xl", "color": "#1a1a1a", "align": "center"}
                    ], "backgroundColor": "#ffffff", "paddingAll": "20px"},
                    "body": {"type": "box", "layout": "vertical", "contents": [
                        {"type": "box", "layout": "horizontal", "contents": [
                            {"type": "text", "text": "الحالة", "size": "sm", "color": "#6a6a6a", "flex": 2},
                            {"type": "text", "text": status, "size": "sm", "color": "#2a2a2a", "flex": 3, "align": "end", "weight": "bold"}
                        ]},
                        {"type": "separator", "margin": "md", "color": "#e8e8e8"},
                        {"type": "box", "layout": "horizontal", "contents": [
                            {"type": "text", "text": "النقاط", "size": "sm", "color": "#6a6a6a", "flex": 2},
                            {"type": "text", "text": str(stats['total_points']), "size": "xl", "color": "#1a1a1a", "flex": 3, "align": "end", "weight": "bold"}
                        ], "margin": "md"},
                        {"type": "separator", "margin": "md", "color": "#e8e8e8"},
                        {"type": "box", "layout": "horizontal", "contents": [
                            {"type": "text", "text": "الألعاب", "size": "sm", "color": "#6a6a6a", "flex": 2},
                            {"type": "text", "text": str(stats['games_played']), "size": "sm", "color": "#2a2a2a", "flex": 3, "align": "end"}
                        ], "margin": "md"},
                        {"type": "box", "layout": "horizontal", "contents": [
                            {"type": "text", "text": "الفوز", "size": "sm", "color": "#6a6a6a", "flex": 2},
                            {"type": "text", "text": str(stats['wins']), "size": "sm", "color": "#2a2a2a", "flex": 3, "align": "end"}
                        ], "margin": "sm"},
                        {"type": "box", "layout": "horizontal", "contents": [
                            {"type": "text", "text": "نسبة الفوز", "size": "sm", "color": "#6a6a6a", "flex": 2},
                            {"type": "text", "text": f"{win_rate:.1f}%", "size": "sm", "color": "#2a2a2a", "flex": 3, "align": "end"}
                        ], "margin": "sm"}
                    ], "backgroundColor": "#ffffff", "paddingAll": "20px"}
                }
                line_bot_api.reply_message(event.reply_token, FlexSendMessage(alt_text="إحصائياتك", contents=stats_msg, quick_reply=get_quick_reply()))
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text="لم تلعب بعد\n\naكتب 'انضم' للتسجيل", quick_reply=get_quick_reply()))
            return
        
        elif text == 'الصدارة':
            leaders = get_leaderboard()
            if leaders:
                players_list = []
                for i, leader in enumerate(leaders, 1):
                    bg = "#4a4a4a" if i <= 3 else "#f5f5f5"
                    tc = "#ffffff" if i <= 3 else "#2a2a2a"
                    players_list.append({
                        "type": "box", "layout": "horizontal", "contents": [
                            {"type": "text", "text": str(i), "size": "sm", "color": tc, "align": "center", "weight": "bold", "flex": 0},
                            {"type": "text", "text": leader['display_name'], "size": "sm", "color": tc, "flex": 3, "margin": "md", "weight": "bold" if i <= 3 else "regular"},
                            {"type": "text", "text": str(leader['total_points']), "size": "sm", "color": tc, "flex": 1, "align": "end", "weight": "bold" if i <= 3 else "regular"}
                        ], "backgroundColor": bg, "cornerRadius": "md", "paddingAll": "12px", "margin": "xs" if i > 1 else "none"
                    })
                leaderboard = {
                    "type": "bubble", "size": "mega",
                    "header": {"type": "box", "layout": "vertical", "contents": [
                        {"type": "text", "text": "لوحة الصدارة", "weight": "bold", "size": "xl", "color": "#1a1a1a", "align": "center"}
                    ], "backgroundColor": "#ffffff", "paddingAll": "20px"},
                    "body": {"type": "box", "layout": "vertical", "contents": players_list, "backgroundColor": "#ffffff", "paddingAll": "20px"}
                }
                line_bot_api.reply_message(event.reply_token, FlexSendMessage(alt_text="الصدارة", contents=leaderboard, quick_reply=get_quick_reply()))
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text="لا توجد بيانات", quick_reply=get_quick_reply()))
            return
        
        elif text in ['إيقاف', 'ايقاف', 'stop']:
            with games_lock:
                if game_id in active_games:
                    game_type = active_games[game_id]['type']
                    del active_games[game_id]
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f"تم إيقاف {game_type}", quick_reply=get_quick_reply()))
                else:
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="لا توجد لعبة نشطة", quick_reply=get_quick_reply()))
            return
        
        elif text in ['انضم', 'تسجيل', 'join']:
            with players_lock:
                if user_id in registered_players:
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f"أنت مسجل بالفعل يا {display_name}", quick_reply=get_quick_reply()))
                else:
                    registered_players.add(user_id)
                    with games_lock:
                        for gid, game_data in active_games.items():
                            if 'participants' not in game_data:
                                game_data['participants'] = set()
                            game_data['participants'].add(user_id)
                    join_msg = {
                        "type": "bubble",
                        "body": {"type": "box", "layout": "vertical", "contents": [
                            {"type": "text", "text": "تم التسجيل بنجاح", "weight": "bold", "size": "xl", "color": "#1a1a1a", "align": "center"},
                            {"type": "text", "text": f"مرحباً {display_name}", "size": "md", "color": "#6a6a6a", "align": "center", "margin": "md"},
                            {"type": "separator", "margin": "xl", "color": "#e8e8e8"},
                            {"type": "text", "text": "يمكنك الآن اللعب في جميع الألعاب\n\nإجاباتك ستُحسب تلقائياً", "size": "sm", "color": "#4a4a4a", "align": "center", "wrap": True, "margin": "xl"}
                        ], "backgroundColor": "#ffffff", "paddingAll": "28px"}
                    }
                    line_bot_api.reply_message(event.reply_token, FlexSendMessage(alt_text="تم التسجيل", contents=join_msg, quick_reply=get_quick_reply()))
                    logger.info(f"✅ انضم: {display_name}")
            return
        
        elif text in ['انسحب', 'خروج', 'leave']:
            with players_lock:
                if user_id in registered_players:
                    registered_players.remove(user_id)
                    with games_lock:
                        for gid, game_data in active_games.items():
                            if 'participants' in game_data and user_id in game_data['participants']:
                                game_data['participants'].remove(user_id)
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f"تم انسحابك يا {display_name}", quick_reply=get_quick_reply()))
                else:
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="أنت غير مسجل", quick_reply=get_quick_reply()))
            return
        
        # بدء الألعاب
        games_map = {
            'ذكاء': (IQGame, 'ذكاء'), 'كلمة ولون': (WordColorGame, 'كلمة ولون'), 'لون': (WordColorGame, 'كلمة ولون'),
            'سلسلة': (ChainWordsGame, 'سلسلة'), 'ترتيب الحروف': (ScrambleWordGame, 'ترتيب'), 'ترتيب': (ScrambleWordGame, 'ترتيب'),
            'تكوين كلمات': (LettersWordsGame, 'تكوين'), 'تكوين': (LettersWordsGame, 'تكوين'), 'أسرع': (FastTypingGame, 'أسرع'),
            'لعبة': (HumanAnimalPlantGame, 'لعبة'), 'خمن': (GuessGame, 'خمن'), 'توافق': (CompatibilityGame, 'توافق'),
            'رياضيات': (MathGame, 'رياضيات'), 'ذاكرة': (MemoryGame, 'ذاكرة'), 'لغز': (RiddleGame, 'لغز'),
            'ضد': (OppositeGame, 'ضد'), 'إيموجي': (EmojiGame, 'إيموجي'), 'أغنية': (SongGame, 'أغنية')
        }
        
        if text in games_map:
            game_class, game_type = games_map[text]
            if text == 'توافق':
                with games_lock:
                    with players_lock:
                        participants = registered_players.copy()
                        participants.add(user_id)
                    game = CompatibilityGame(line_bot_api)
                    active_games[game_id] = {'game': game, 'type': 'توافق', 'created_at': datetime.now(), 'participants': participants}
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text="💖 لعبة التوافق!\n\nاكتب اسمين مفصولين بمسافة\nمثال: أحمد فاطمة", quick_reply=get_quick_reply()))
                return
            start_game(game_id, game_class, game_type, user_id, event)
            return
        
        # معالجة إجابات الألعاب النشطة
        if game_id in active_games:
            game_data = active_games[game_id]
            with players_lock:
                is_registered = user_id in registered_players
            if not is_registered and 'participants' in game_data and user_id not in game_data['participants']:
                return
            game = game_data['game']
            game_type = game_data['type']
            try:
                result = game.check_answer(text, user_id, display_name)
                if result:
                    points = result.get('points', 0)
                    if points > 0:
                        update_user_points(user_id, display_name, points, result.get('won', False), game_type)
                    if result.get('game_over', False):
                        with games_lock:
                            if game_id in active_games:
                                del active_games[game_id]
                        response = TextSendMessage(text=result.get('message', 'انتهت اللعبة'), quick_reply=get_quick_reply())
                    else:
                        response = result.get('response', TextSendMessage(text=result.get('message', '')))
                        if isinstance(response, TextSendMessage):
                            response.quick_reply = get_quick_reply()
                    line_bot_api.reply_message(event.reply_token, response)
                return
            except Exception as e:
                logger.error(f"❌ خطأ في معالجة الإجابة: {e}")
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text="❌ حدث خطأ. حاول مرة أخرى.", quick_reply=get_quick_reply()))
                return
    except Exception as e:
        logger.error(f"❌ خطأ في معالجة الرسالة: {e}")

@app.errorhandler(Exception)
def handle_error(error):
    logger.error(f"❌ خطأ غير متوقع: {error}", exc_info=True)
    return 'Internal Server Error', 500

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"🚀 بدء الخادم على المنفذ {port}")
    logger.info(f"📊 اللاعبون المسجلون: {len(registered_players)}")
    logger.info(f"🎮 الألعاب النشطة: {len(active_games)}")
    app.run(host='0.0.0.0', port=port, debug=False)
