"""
LINE Bot - Game Server
الملف الرئيسي المحدث والمحسّن
"""

from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    QuickReply, QuickReplyButton, MessageAction,
    FlexSendMessage
)
import os
from datetime import datetime, timedelta
import sqlite3
from collections import defaultdict
import threading
import time
import logging

# الإعدادات والقوالب
from game_config import GameConfig
from flex_templates import FlexTemplates

# إعداد السجلات
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# استيراد الألعاب
try:
    from games.iq_game import IQGame
    from games.word_color_game import WordColorGame
    from games.chain_words_game import ChainWordsGame
    from games.scramble_word_game import ScrambleWordGame
    from games.letters_words_game import LettersWordsGame
    from games.fast_typing_game import FastTypingGame
    from games.human_animal_plant_game import HumanAnimalPlantGame
    from games.guess_game import GuessGame
    from games.compatibility_game import CompatibilityGame
    from games.math_game import MathGame
    from games.memory_game import MemoryGame
    from games.riddle_game import RiddleGame
    from games.opposite_game import OppositeGame
    from games.emoji_game import EmojiGame
    from games.song_game import SongGame
    logger.info("✅ تم استيراد جميع الألعاب بنجاح")
except Exception as e:
    logger.error(f"❌ خطأ في استيراد الألعاب: {e}")

app = Flask(__name__)

# إعدادات LINE Bot
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', 'YOUR_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET', 'YOUR_CHANNEL_SECRET')

if LINE_CHANNEL_ACCESS_TOKEN == 'YOUR_CHANNEL_ACCESS_TOKEN':
    logger.warning("⚠️ لم يتم تعيين LINE_CHANNEL_ACCESS_TOKEN")
if LINE_CHANNEL_SECRET == 'YOUR_CHANNEL_SECRET':
    logger.warning("⚠️ لم يتم تعيين LINE_CHANNEL_SECRET")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# إعدادات Gemini AI
GEMINI_API_KEYS = [
    os.getenv('GEMINI_API_KEY_1', ''),
    os.getenv('GEMINI_API_KEY_2', ''),
    os.getenv('GEMINI_API_KEY_3', '')
]
GEMINI_API_KEYS = [key for key in GEMINI_API_KEYS if key]
current_gemini_key_index = 0
USE_AI = bool(GEMINI_API_KEYS)

logger.info(f"🔑 عدد مفاتيح Gemini المتاحة: {len(GEMINI_API_KEYS)}")
logger.info(f"🤖 استخدام AI: {USE_AI}")


def get_gemini_api_key():
    """الحصول على مفتاح Gemini API الحالي"""
    global current_gemini_key_index
    if GEMINI_API_KEYS:
        return GEMINI_API_KEYS[current_gemini_key_index]
    return None


def switch_gemini_key():
    """التبديل إلى المفتاح التالي"""
    global current_gemini_key_index
    if len(GEMINI_API_KEYS) > 1:
        current_gemini_key_index = (current_gemini_key_index + 1) % len(GEMINI_API_KEYS)
        logger.info(f"🔄 تم التبديل إلى مفتاح Gemini رقم: {current_gemini_key_index + 1}")
        return True
    return False


# تخزين الألعاب النشطة واللاعبين
active_games = {}
registered_players = set()
user_message_count = defaultdict(lambda: {'count': 0, 'reset_time': datetime.now()})

# قفل thread-safe
games_lock = threading.Lock()
players_lock = threading.Lock()

# ====================
# قاعدة البيانات
# ====================

def get_db_connection():
    """إنشاء اتصال آمن بقاعدة البيانات"""
    conn = sqlite3.connect(GameConfig.DB_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """إنشاء جداول قاعدة البيانات"""
    try:
        conn = get_db_connection()
        c = conn.cursor()
        
        c.execute('''CREATE TABLE IF NOT EXISTS users
                     (user_id TEXT PRIMARY KEY, 
                      display_name TEXT,
                      total_points INTEGER DEFAULT 0,
                      games_played INTEGER DEFAULT 0,
                      wins INTEGER DEFAULT 0,
                      last_played TEXT,
                      registered_at TEXT DEFAULT CURRENT_TIMESTAMP)''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS game_history
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      user_id TEXT,
                      game_type TEXT,
                      points INTEGER,
                      won INTEGER,
                      played_at TEXT DEFAULT CURRENT_TIMESTAMP,
                      FOREIGN KEY (user_id) REFERENCES users(user_id))''')
        
        c.execute('''CREATE INDEX IF NOT EXISTS idx_user_points 
                     ON users(total_points DESC)''')
        c.execute('''CREATE INDEX IF NOT EXISTS idx_game_history_user 
                     ON game_history(user_id, played_at)''')
        
        conn.commit()
        conn.close()
        logger.info("✅ تم إنشاء قاعدة البيانات بنجاح")
    except Exception as e:
        logger.error(f"❌ خطأ في إنشاء قاعدة البيانات: {e}")


init_db()


def update_user_points(user_id, display_name, points, won=False, game_type=""):
    """تحديث نقاط المستخدم"""
    try:
        conn = get_db_connection()
        c = conn.cursor()
        
        c.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        user = c.fetchone()
        
        if user:
            new_points = max(0, user['total_points'] + points)  # تجنب النقاط السالبة
            new_games = user['games_played'] + 1
            new_wins = user['wins'] + (1 if won else 0)
            c.execute('''UPDATE users SET total_points = ?, games_played = ?, 
                         wins = ?, last_played = ?, display_name = ?
                         WHERE user_id = ?''',
                      (new_points, new_games, new_wins, datetime.now().isoformat(), 
                       display_name, user_id))
        else:
            c.execute('''INSERT INTO users (user_id, display_name, total_points, 
                         games_played, wins, last_played) VALUES (?, ?, ?, ?, ?, ?)''',
                      (user_id, display_name, max(0, points), 1, 1 if won else 0, 
                       datetime.now().isoformat()))
        
        if game_type:
            c.execute('''INSERT INTO game_history (user_id, game_type, points, won) 
                         VALUES (?, ?, ?, ?)''',
                      (user_id, game_type, points, 1 if won else 0))
        
        conn.commit()
        conn.close()
        logger.info(f"✅ تم تحديث نقاط {display_name}: {points:+d}")
        return True
    except Exception as e:
        logger.error(f"❌ خطأ في تحديث النقاط: {e}")
        return False


def get_user_stats(user_id):
    """الحصول على إحصائيات المستخدم"""
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        user = c.fetchone()
        conn.close()
        return user
    except Exception as e:
        logger.error(f"❌ خطأ في الحصول على الإحصائيات: {e}")
        return None


def get_leaderboard(limit=10):
    """الحصول على لوحة الصدارة"""
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('''SELECT display_name, total_points, games_played, wins 
                     FROM users ORDER BY total_points DESC LIMIT ?''', (limit,))
        leaders = c.fetchall()
        conn.close()
        return leaders
    except Exception as e:
        logger.error(f"❌ خطأ في الحصول على الصدارة: {e}")
        return []


def check_rate_limit(user_id):
    """فحص حد المعدل"""
    config = GameConfig.RATE_LIMIT
    now = datetime.now()
    user_data = user_message_count[user_id]
    
    if now - user_data['reset_time'] > timedelta(seconds=config['time_window']):
        user_data['count'] = 0
        user_data['reset_time'] = now
    
    if user_data['count'] >= config['max_messages']:
        logger.warning(f"⚠️ تجاوز حد الرسائل: {user_id}")
        return False
    
    user_data['count'] += 1
    return True


def cleanup_old_games():
    """تنظيف الألعاب القديمة"""
    while True:
        try:
            time.sleep(300)  # كل 5 دقائق
            now = datetime.now()
            to_delete = []
            
            with games_lock:
                for game_id, game_data in active_games.items():
                    if now - game_data.get('created_at', now) > timedelta(minutes=15):
                        to_delete.append(game_id)
                
                for game_id in to_delete:
                    del active_games[game_id]
                    logger.info(f"🗑️ تم حذف لعبة قديمة: {game_id}")
        except Exception as e:
            logger.error(f"❌ خطأ في التنظيف: {e}")


cleanup_thread = threading.Thread(target=cleanup_old_games, daemon=True)
cleanup_thread.start()


def get_quick_reply():
    """الأزرار الثابتة - ألعاب فقط"""
    return QuickReply(items=[
        QuickReplyButton(action=MessageAction(label="🎯 ذكاء", text="ذكاء")),
        QuickReplyButton(action=MessageAction(label="🎨 لون", text="لون")),
        QuickReplyButton(action=MessageAction(label="⛓️ سلسلة", text="سلسلة")),
        QuickReplyButton(action=MessageAction(label="🔤 ترتيب", text="ترتيب")),
        QuickReplyButton(action=MessageAction(label="✍️ تكوين", text="تكوين")),
        QuickReplyButton(action=MessageAction(label="⚡ أسرع", text="أسرع")),
        QuickReplyButton(action=MessageAction(label="🎲 لعبة", text="لعبة")),
        QuickReplyButton(action=MessageAction(label="🔮 خمن", text="خمن")),
        QuickReplyButton(action=MessageAction(label="💝 توافق", text="توافق")),
        QuickReplyButton(action=MessageAction(label="➕ رياضيات", text="رياضيات")),
        QuickReplyButton(action=MessageAction(label="🧩 ذاكرة", text="ذاكرة")),
        QuickReplyButton(action=MessageAction(label="❓ لغز", text="لغز")),
        QuickReplyButton(action=MessageAction(label="🎭 ضد", text="ضد"))
    ])


def get_user_profile_safe(user_id):
    """الحصول على معلومات المستخدم"""
    try:
        profile = line_bot_api.get_profile(user_id)
        return profile.display_name
    except Exception as e:
        logger.error(f"❌ خطأ في الحصول على الملف الشخصي: {e}")
        return "مستخدم"


def start_game(game_id, game_class, game_type, user_id, event):
    """دالة موحدة لبدء الألعاب"""
    try:
        with games_lock:
            # إنشاء اللعبة
            if game_class in [IQGame, WordColorGame, LettersWordsGame, HumanAnimalPlantGame]:
                game = game_class(line_bot_api, use_ai=USE_AI, 
                                get_api_key=get_gemini_api_key, 
                                switch_key=switch_gemini_key)
            else:
                game = game_class(line_bot_api)
            
            # إضافة المشاركين
            with players_lock:
                participants = registered_players.copy()
                participants.add(user_id)
            
            active_games[game_id] = {
                'game': game,
                'type': game_type,
                'created_at': datetime.now(),
                'participants': participants
            }
        
        # بدء اللعبة
        response = game.start_game()
        
        # إضافة الأزرار السريعة
        if isinstance(response, TextSendMessage):
            response.quick_reply = get_quick
