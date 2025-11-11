"""
LINE Bot - Game Server
الملف النهائي المحدث والمحسّن
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


# ====================
# Quick Reply
# ====================

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
        QuickReplyButton(action=MessageAction(label="✨ خمن", text="خمن")),
        QuickReplyButton(action=MessageAction(label="🖤 توافق", text="توافق")),
        QuickReplyButton(action=MessageAction(label="➕ رياضيات", text="رياضيات")),
        QuickReplyButton(action=MessageAction(label="🧩 ذاكرة", text="ذاكرة")),
        QuickReplyButton(action=MessageAction(label="❓ لغز", text="لغز")),
        QuickReplyButton(action=MessageAction(label="🎭 ضد", text="ضد"))
    ])


# ====================
# دوال الألعاب
# ====================

def start_game(game_id, game_class, game_type, user_id, event):
    """دالة موحدة لبدء الألعاب"""
    try:
        with games_lock:
            # إنشاء اللعبة
            if game_class in [IQGame, WordColorGame, LettersWordsGame, HumanAnimalPlantGame]:
                game = game_class(
                    line_bot_api, 
                    use_ai=USE_AI, 
                    get_api_key=get_gemini_api_key, 
                    switch_key=switch_gemini_key
                )
            else:
                game = game_class(line_bot_api)
            
            # إضافة المشاركين
            with players_lock:
                participants = registered_players.copy()
                participants.add(user_id)
            
            # تسجيل اللعبة النشطة
            active_games[game_id] = {
                'game': game,
                'type': game_type,
                'created_at': datetime.now(),
                'participants': participants
            }
        
        # بدء اللعبة
        response = game.start_game()
        
        # إضافة الأزرار السريعة إذا كان النص من نوع TextSendMessage
        if isinstance(response, TextSendMessage):
            response.quick_reply = get_quick_reply()
        
        return response
    
    except Exception as e:
        logger.error(f"❌ خطأ في بدء اللعبة {game_type} للمستخدم {user_id}: {e}")
        return TextSendMessage(
            text="⚠️ حدث خطأ أثناء بدء اللعبة. حاول مرة أخرى.",
            quick_reply=get_quick_reply()
        )
