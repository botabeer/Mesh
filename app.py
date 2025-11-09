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
import re
import logging

# استيراد الألعاب
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

# إعداد Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# إعدادات LINE Bot
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', 'YOUR_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET', 'YOUR_CHANNEL_SECRET')

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

# إعدادات قاعدة البيانات
DB_PATH = os.getenv('DB_PATH', 'game_scores.db')

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
        logger.info(f"تم التبديل إلى المفتاح رقم {current_gemini_key_index + 1}")
        return True
    return False

# تخزين الألعاب النشطة واللاعبين
active_games = {}
registered_players = set()
user_message_count = defaultdict(lambda: {'count': 0, 'reset_time': datetime.now()})
ai_conversations = {}  # تخزين محادثات الذكاء الاصطناعي

# فئة أساسية للألعاب مع نظام 10 أسئلة
class BaseGameWithRounds:
    """فئة أساسية للألعاب مع نظام الجولات"""
    def __init__(self, max_rounds=10):
        self.max_rounds = max_rounds
        self.current_round = 0
        self.scores = defaultdict(int)  # {user_id: score}
        self.player_names = {}  # {user_id: display_name}
    
    def add_score(self, user_id, display_name, points):
        """إضافة نقاط للاعب"""
        self.scores[user_id] += points
        self.player_names[user_id] = display_name
    
    def increment_round(self):
        """زيادة رقم الجولة"""
        self.current_round += 1
    
    def is_game_over(self):
        """التحقق من انتهاء اللعبة"""
        return self.current_round >= self.max_rounds
    
    def get_winner_message(self):
        """الحصول على رسالة الفائز"""
        if not self.scores:
            return {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "انتهت اللعبة",
                            "weight": "bold",
                            "size": "xl",
                            "align": "center",
                            "color": "#1a1a1a"
                        },
                        {
                            "type": "text",
                            "text": "لم يشارك أحد",
                            "size": "sm",
                            "color": "#666666",
                            "align": "center",
                            "margin": "md"
                        }
                    ],
                    "backgroundColor": "#ffffff",
                    "paddingAll": "24px"
                }
            }
        
        # ترتيب اللاعبين حسب النقاط
        sorted_players = sorted(self.scores.items(), key=lambda x: x[1], reverse=True)
        
        # بناء محتوى الرسالة
        contents = [
            {
                "type": "text",
                "text": "انتهت اللعبة",
                "weight": "bold",
                "size": "xl",
                "align": "center",
                "color": "#1a1a1a"
            },
            {
                "type": "text",
                "text": f"{self.max_rounds} جولات",
                "size": "sm",
                "color": "#666666",
                "align": "center",
                "margin": "sm"
            },
            {
                "type": "separator",
                "margin": "xl",
                "color": "#e0e0e0"
            }
        ]
        
        # إضافة اللاعبين
        for i, (user_id, score) in enumerate(sorted_players[:10], 1):
            rank_color = "#1a1a1a" if i <= 3 else "#666666"
            rank_text = "01" if i == 1 else "02" if i == 2 else "03" if i == 3 else f"{i:02d}"
            player_name = self.player_names.get(user_id, "لاعب")
            
            # إضافة علامة للفائز
            if i == 1:
                player_name = f"{player_name} 👑"
            
            contents.append({
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": rank_text,
                        "size": "sm",
                        "color": rank_color,
                        "flex": 0,
                        "weight": "bold"
                    },
                    {
                        "type": "text",
                        "text": player_name,
                        "size": "sm",
                        "color": "#333333",
                        "flex": 1,
                        "margin": "md"
                    },
                    {
                        "type": "text",
                        "text": str(score),
                        "size": "sm",
                        "color": rank_color,
                        "align": "end",
                        "weight": "bold"
                    }
                ],
                "margin": "lg" if i == 1 else "md"
            })
        
        return {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": contents,
                "backgroundColor": "#ffffff",
                "paddingAll": "24px"
            }
        }

# دالة تطبيع النص
def normalize_text(text):
    """تطبيع النص للمقارنة"""
    text = text.strip().lower()
    text = re.sub(r'^ال', '', text)
    text = text.replace('أ', 'ا').replace('إ', 'ا').replace('آ', 'ا')
    text = text.replace('ة', 'ه')
    text = text.replace('ى', 'ي')
    text = re.sub(r'[\u064B-\u065F]', '', text)
    return text

# قاعدة البيانات مع Context Manager
def init_db():
    """تهيئة قاعدة البيانات"""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS users
                         (user_id TEXT PRIMARY KEY, 
                          display_name TEXT,
                          total_points INTEGER DEFAULT 0,
                          games_played INTEGER DEFAULT 0,
                          wins INTEGER DEFAULT 0,
                          last_played TEXT,
                          join_date TEXT)''')
            
            # جدول لتتبع الألعاب
            c.execute('''CREATE TABLE IF NOT EXISTS game_history
                         (id INTEGER PRIMARY KEY AUTOINCREMENT,
                          user_id TEXT,
                          game_type TEXT,
                          points INTEGER,
                          won INTEGER,
                          play_date TEXT)''')
            conn.commit()
        logger.info("تم تهيئة قاعدة البيانات بنجاح")
    except Exception as e:
        logger.error(f"خطأ في تهيئة قاعدة البيانات: {e}")

init_db()

# دالة تحديث النقاط
def update_user_points(user_id, display_name, points, won=False, game_type=""):
    """تحديث نقاط المستخدم"""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
            user = c.fetchone()
            
            if user:
                new_points = user[2] + points
                new_games = user[3] + 1
                new_wins = user[4] + (1 if won else 0)
                c.execute('''UPDATE users SET total_points = ?, games_played = ?, 
                             wins = ?, last_played = ?, display_name = ?
                             WHERE user_id = ?''',
                          (new_points, new_games, new_wins, datetime.now().isoformat(), 
                           display_name, user_id))
            else:
                c.execute('''INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?)''',
                          (user_id, display_name, points, 1, 1 if won else 0, 
                           datetime.now().isoformat(), datetime.now().isoformat()))
            
            # إضافة سجل اللعبة
            c.execute('''INSERT INTO game_history (user_id, game_type, points, won, play_date)
                         VALUES (?, ?, ?, ?, ?)''',
                      (user_id, game_type, points, 1 if won else 0, datetime.now().isoformat()))
            conn.commit()
    except Exception as e:
        logger.error(f"خطأ في تحديث النقاط: {e}")

# دالة الحصول على إحصائيات المستخدم
def get_user_stats(user_id):
    """الحصول على إحصائيات المستخدم"""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
            return c.fetchone()
    except Exception as e:
        logger.error(f"خطأ في الحصول على الإحصائيات: {e}")
        return None

# دالة الصدارة
def get_leaderboard(limit=10):
    """الحصول على لوحة الصدارة"""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute('''SELECT display_name, total_points, games_played, wins 
                         FROM users ORDER BY total_points DESC LIMIT ?''', (limit,))
            return c.fetchall()
    except Exception as e:
        logger.error(f"خطأ في الحصول على الصدارة: {e}")
        return []

# حماية من السبام
def check_rate_limit(user_id):
    """التحقق من حد الرسائل"""
    now = datetime.now()
    user_data = user_message_count[user_id]
    
    if now - user_data['reset_time'] > timedelta(minutes=1):
        user_data['count'] = 0
        user_data['reset_time'] = now
    
    if user_data['count'] >= 30:  # زيادة الحد إلى 30
        return False
    
    user_data['count'] += 1
    return True

# تنظيف الألعاب القديمة
def cleanup_old_games():
    """تنظيف الألعاب غير النشطة"""
    while True:
        try:
            time.sleep(600)  # كل 10 دقائق
            now = datetime.now()
            to_delete = []
            
            for game_id, game_data in active_games.items():
                if now - game_data.get('created_at', now) > timedelta(minutes=10):
                    to_delete.append(game_id)
            
            for game_id in to_delete:
                del active_games[game_id]
                logger.info(f"تم حذف اللعبة: {game_id}")
        except Exception as e:
            logger.error(f"خطأ في التنظيف: {e}")

cleanup_thread = threading.Thread(target=cleanup_old_games, daemon=True)
cleanup_thread.start()

# الأزرار الثابتة - تصميم احترافي
def get_quick_reply():
    """الأزرار الرئيسية - الألعاب الأكثر استخداماً فقط"""
    return QuickReply(items=[
        QuickReplyButton(action=MessageAction(label="ذكاء", text="ذكاء")),
        QuickReplyButton(action=MessageAction(label="رياضيات", text="رياضيات")),
        QuickReplyButton(action=MessageAction(label="أسرع", text="أسرع")),
        QuickReplyButton(action=MessageAction(label="ترتيب", text="ترتيب الحروف")),
        QuickReplyButton(action=MessageAction(label="لغز", text="لغز")),
        QuickReplyButton(action=MessageAction(label="ذاكرة", text="ذاكرة")),
        QuickReplyButton(action=MessageAction(label="تكوين", text="تكوين كلمات")),
        QuickReplyButton(action=MessageAction(label="ضد", text="ضد")),
        QuickReplyButton(action=MessageAction(label="خمن", text="خمن")),
        QuickReplyButton(action=MessageAction(label="لمح", text="لمح")),
        QuickReplyButton(action=MessageAction(label="جاوب", text="جاوب")),
        QuickReplyButton(action=MessageAction(label="المزيد", text="المزيد"))
    ])

def get_more_quick_reply():
    """الأزرار الإضافية - ألعاب أخرى"""
    return QuickReply(items=[
        QuickReplyButton(action=MessageAction(label="سلسلة", text="سلسلة")),
        QuickReplyButton(action=MessageAction(label="لون", text="كلمة ولون")),
        QuickReplyButton(action=MessageAction(label="لعبة", text="لعبة")),
        QuickReplyButton(action=MessageAction(label="ايموجي", text="إيموجي")),
        QuickReplyButton(action=MessageAction(label="توافق", text="توافق")),
        QuickReplyButton(action=MessageAction(label="أغنية", text="أغنية")),
        QuickReplyButton(action=MessageAction(label="انضم", text="انضم")),
        QuickReplyButton(action=MessageAction(label="نقاطي", text="نقاطي")),
        QuickReplyButton(action=MessageAction(label="الصدارة", text="الصدارة")),
        QuickReplyButton(action=MessageAction(label="مساعدة", text="مساعدة")),
        QuickReplyButton(action=MessageAction(label="إيقاف", text="إيقاف")),
        QuickReplyButton(action=MessageAction(label="البداية", text="البداية"))
    ])

# رسالة الترحيب - تصميم أنيق بالأبيض والأسود
def get_welcome_message():
    """رسالة الترحيب الاحترافية"""
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
                            "type": "text",
                            "text": "مرحباً بك",
                            "weight": "bold",
                            "size": "xxl",
                            "align": "center",
                            "color": "#1a1a1a"
                        },
                        {
                            "type": "text",
                            "text": "منصة الألعاب التفاعلية",
                            "size": "sm",
                            "align": "center",
                            "color": "#666666",
                            "margin": "sm"
                        }
                    ],
                    "paddingBottom": "20px"
                },
                {
                    "type": "separator",
                    "color": "#e0e0e0"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "01",
                                    "size": "sm",
                                    "color": "#999999",
                                    "flex": 0,
                                    "weight": "bold"
                                },
                                {
                                    "type": "text",
                                    "text": "اضغط على 'انضم' للتسجيل",
                                    "size": "sm",
                                    "color": "#333333",
                                    "margin": "md",
                                    "wrap": True,
                                    "flex": 1
                                }
                            ],
                            "margin": "lg"
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "02",
                                    "size": "sm",
                                    "color": "#999999",
                                    "flex": 0,
                                    "weight": "bold"
                                },
                                {
                                    "type": "text",
                                    "text": "اختر لعبة من الأزرار أدناه",
                                    "size": "sm",
                                    "color": "#333333",
                                    "margin": "md",
                                    "wrap": True,
                                    "flex": 1
                                }
                            ],
                            "margin": "md"
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "03",
                                    "size": "sm",
                                    "color": "#999999",
                                    "flex": 0,
                                    "weight": "bold"
                                },
                                {
                                    "type": "text",
                                    "text": "ابدأ اللعب واجمع النقاط",
                                    "size": "sm",
                                    "color": "#333333",
                                    "margin": "md",
                                    "wrap": True,
                                    "flex": 1
                                }
                            ],
                            "margin": "md"
                        }
                    ],
                    "paddingTop": "20px",
                    "paddingBottom": "20px"
                },
                {
                    "type": "separator",
                    "color": "#e0e0e0"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "تم إنشاء هذا البوت بواسطة عبير الدوسري",
                            "size": "xs",
                            "color": "#999999",
                            "align": "center"
                        },
                        {
                            "type": "text",
                            "text": "نظام نقاط ولوحة صدارة",
                            "size": "xs",
                            "color": "#999999",
                            "align": "center",
                            "margin": "xs"
                        }
                    ],
                    "paddingTop": "20px"
                }
            ],
            "backgroundColor": "#ffffff",
            "paddingAll": "24px"
        }
    }

# رسالة المساعدة - تصميم احترافي
def get_help_message():
    """رسالة المساعدة"""
    return {
        "type": "bubble",
        "size": "mega",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "دليل الاستخدام",
                    "weight": "bold",
                    "size": "xl",
                    "align": "center",
                    "color": "#1a1a1a"
                },
                {
                    "type": "separator",
                    "margin": "xl",
                    "color": "#e0e0e0"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "الأوامر المتاحة",
                            "weight": "bold",
                            "size": "md",
                            "color": "#333333",
                            "margin": "lg"
                        },
                        {
                            "type": "text",
                            "text": "• انضم / انسحب - التسجيل\n• لمح - تلميح خفيف\n• جاوب - إظهار الإجابة الكاملة\n• نقاطي - إحصائياتك\n• الصدارة - أفضل اللاعبين\n• إيقاف - إنهاء اللعبة",
                            "size": "sm",
                            "color": "#666666",
                            "margin": "md",
                            "wrap": True
                        }
                    ]
                },
                {
                    "type": "separator",
                    "margin": "xl",
                    "color": "#e0e0e0"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "الألعاب المتاحة",
                            "weight": "bold",
                            "size": "md",
                            "color": "#333333",
                            "margin": "lg"
                        },
                        {
                            "type": "text",
                            "text": "الشائعة: ذكاء • رياضيات • أسرع • ترتيب\nلغز • ذاكرة • تكوين • ضد • خمن\n\nإضافية: سلسلة • لون • لعبة • ايموجي\nتوافق • أغنية (في قائمة المزيد)",
                            "size": "sm",
                            "color": "#666666",
                            "margin": "md",
                            "wrap": True
                        }
                    ]
                },
                {
                    "type": "separator",
                    "margin": "xl",
                    "color": "#e0e0e0"
                },
                {
                    "type": "text",
                    "text": "بعد الانضمام تُحسب إجاباتك تلقائياً",
                    "size": "xs",
                    "color": "#999999",
                    "align": "center",
                    "margin": "lg"
                }
            ],
            "backgroundColor": "#ffffff",
            "paddingAll": "24px"
        }
    }

# رسالة الإحصائيات - تصميم أنيق
def get_stats_message(stats, user_id):
    """رسالة الإحصائيات"""
    if not stats:
        return {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "لم تبدأ بعد",
                        "weight": "bold",
                        "size": "xl",
                        "align": "center",
                        "color": "#333333"
                    },
                    {
                        "type": "text",
                        "text": "اضغط 'انضم' للتسجيل والبدء",
                        "size": "sm",
                        "color": "#666666",
                        "align": "center",
                        "margin": "md",
                        "wrap": True
                    }
                ],
                "backgroundColor": "#ffffff",
                "paddingAll": "24px"
            }
        }
    
    status = "مسجل" if user_id in registered_players else "غير مسجل"
    win_rate = round((stats[4] / stats[3] * 100) if stats[3] > 0 else 0, 1)
    
    return {
        "type": "bubble",
        "size": "mega",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": stats[1],
                    "weight": "bold",
                    "size": "xl",
                    "align": "center",
                    "color": "#1a1a1a"
                },
                {
                    "type": "text",
                    "text": status,
                    "size": "sm",
                    "align": "center",
                    "color": "#666666",
                    "margin": "sm"
                },
                {
                    "type": "separator",
                    "margin": "xl",
                    "color": "#e0e0e0"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "النقاط الكلية",
                                    "size": "sm",
                                    "color": "#666666",
                                    "flex": 1
                                },
                                {
                                    "type": "text",
                                    "text": str(stats[2]),
                                    "size": "sm",
                                    "color": "#1a1a1a",
                                    "weight": "bold",
                                    "align": "end"
                                }
                            ],
                            "margin": "lg"
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "عدد الألعاب",
                                    "size": "sm",
                                    "color": "#666666",
                                    "flex": 1
                                },
                                {
                                    "type": "text",
                                    "text": str(stats[3]),
                                    "size": "sm",
                                    "color": "#1a1a1a",
                                    "weight": "bold",
                                    "align": "end"
                                }
                            ],
                            "margin": "md"
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "مرات الفوز",
                                    "size": "sm",
                                    "color": "#666666",
                                    "flex": 1
                                },
                                {
                                    "type": "text",
                                    "text": str(stats[4]),
                                    "size": "sm",
                                    "color": "#1a1a1a",
                                    "weight": "bold",
                                    "align": "end"
                                }
                            ],
                            "margin": "md"
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "نسبة الفوز",
                                    "size": "sm",
                                    "color": "#666666",
                                    "flex": 1
                                },
                                {
                                    "type": "text",
                                    "text": f"{win_rate}%",
                                    "size": "sm",
                                    "color": "#1a1a1a",
                                    "weight": "bold",
                                    "align": "end"
                                }
                            ],
                            "margin": "md"
                        }
                    ],
                    "paddingTop": "20px",
                    "paddingBottom": "20px"
                }
            ],
            "backgroundColor": "#ffffff",
            "paddingAll": "24px"
        }
    }

# رسالة الصدارة - تصميم راقي
def get_leaderboard_message(leaders):
    """رسالة لوحة الصدارة"""
    if not leaders:
        return {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "لوحة الصدارة",
                        "weight": "bold",
                        "size": "xl",
                        "align": "center",
                        "color": "#1a1a1a"
                    },
                    {
                        "type": "text",
                        "text": "لا توجد بيانات بعد",
                        "size": "sm",
                        "color": "#666666",
                        "align": "center",
                        "margin": "md"
                    }
                ],
                "backgroundColor": "#ffffff",
                "paddingAll": "24px"
            }
        }
    
    contents = [
        {
            "type": "text",
            "text": "لوحة الصدارة",
            "weight": "bold",
            "size": "xl",
            "align": "center",
            "color": "#1a1a1a"
        },
        {
            "type": "separator",
            "margin": "xl",
            "color": "#e0e0e0"
        }
    ]
    
    for i, leader in enumerate(leaders[:10], 1):
        rank_color = "#1a1a1a" if i <= 3 else "#666666"
        rank_text = "01" if i == 1 else "02" if i == 2 else "03" if i == 3 else f"{i:02d}"
        
        contents.append({
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "text",
                    "text": rank_text,
                    "size": "sm",
                    "color": rank_color,
                    "flex": 0,
                    "weight": "bold"
                },
                {
                    "type": "text",
                    "text": leader[0],
                    "size": "sm",
                    "color": "#333333",
                    "flex": 1,
                    "margin": "md"
                },
                {
                    "type": "text",
                    "text": str(leader[1]),
                    "size": "sm",
                    "color": rank_color,
                    "align": "end",
                    "weight": "bold"
                }
            ],
            "margin": "lg" if i == 1 else "md"
        })
    
    return {
        "type": "bubble",
        "size": "mega",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": contents,
            "backgroundColor": "#ffffff",
            "paddingAll": "24px"
        }
    }

# دالة الرد التلقائي باستخدام AI
async def get_ai_response(user_message, user_id):
    """الحصول على رد من Gemini AI"""
    if not USE_AI:
        return "عذراً، خدمة الذكاء الاصطناعي غير متوفرة حالياً"
    
    try:
        import google.generativeai as genai
        
        # الحصول على المحادثة السابقة
        if user_id not in ai_conversations:
            ai_conversations[user_id] = []
        
        # تحديد عدد الرسائل السابقة (آخر 10 رسائل)
        conversation_history = ai_conversations[user_id][-10:]
        
        # إعداد المفتاح
        api_key = get_gemini_api_key()
        genai.configure(api_key=api_key)
        
        # إعداد النموذج
        model = genai.GenerativeModel('gemini-pro')
        
        # بناء المحادثة
        prompt = "أنت مساعد ذكي ولطيف. أجب بشكل مختصر ومفيد.\n\n"
        for msg in conversation_history:
            prompt += f"{msg['role']}: {msg['content']}\n"
        prompt += f"المستخدم: {user_message}\nالمساعد:"
        
        # الحصول على الرد
        response = model.generate_content(prompt)
        ai_reply = response.text
        
        # حفظ المحادثة
        ai_conversations[user_id].append({"role": "المستخدم", "content": user_message})
        ai_conversations[user_id].append({"role": "المساعد", "content": ai_reply})
        
        # الاحتفاظ بآخر 20 رسالة فقط
        if len(ai_conversations[user_id]) > 20:
            ai_conversations[user_id] = ai_conversations[user_id][-20:]
        
        return ai_reply
        
    except Exception as e:
        logger.error(f"خطأ في AI: {e}")
        # محاولة التبديل للمفتاح التالي
        if switch_gemini_key():
            try:
                return await get_ai_response(user_message, user_id)
            except:
                pass
        return "عذراً، حدث خطأ في معالجة طلبك"

# دالة الحصول على اسم المستخدم
def get_display_name(user_id, fallback_name=""):
    """الحصول على اسم المستخدم أو استخدام الاسم البديل"""
    try:
        profile = line_bot_api.get_profile(user_id)
        return profile.display_name if profile.display_name else fallback_name if fallback_name else "لاعب"
    except Exception as e:
        logger.error(f"خطأ في الحصول على الاسم: {e}")
        return fallback_name if fallback_name else "لاعب"

@app.route("/callback", methods=['POST'])
def callback():
    """معالجة رسائل LINE"""
    signature = request.headers.get('X-Line-Signature', '')
    body = request.get_data(as_text=True)
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        logger.error("Invalid signature")
        abort(400)
    except Exception as e:
        logger.error(f"خطأ في callback: {e}")
    
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    """معالجة الرسائل النصية"""
    user_id = event.source.user_id
    text = event.message.text.strip()
    
    # التحقق من Rate Limit
    if not check_rate_limit(user_id):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text="عدد كبير من الرسائل، انتظر قليلاً",
                quick_reply=get_quick_reply()
            )
        )
        return
    
    # الحصول على اسم المستخدم - إذا لم يكن متاحاً، استخدم النص المكتوب
    display_name = get_display_name(user_id, text)
    
    # معرف اللعبة (Group أو User)
    if hasattr(event.source, 'group_id'):
        game_id = event.source.group_id
    elif hasattr(event.source, 'room_id'):
        game_id = event.source.room_id
    else:
        game_id = user_id
    
    # ===== الأوامر الرئيسية =====
    
    # البداية
    if text in ['البداية', 'ابدأ', 'start', 'قائمة', 'بداية']:
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(
                alt_text="مرحباً بك",
                contents=get_welcome_message(),
                quick_reply=get_quick_reply()
            )
        )
        return
    
    # المزيد
    elif text in ['المزيد', 'أكثر', 'more']:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text="خيارات إضافية",
                quick_reply=get_more_quick_reply()
            )
        )
        return
    
    # المساعدة
    elif text in ['مساعدة', 'help']:
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(
                alt_text="المساعدة",
                contents=get_help_message(),
                quick_reply=get_quick_reply()
            )
        )
        return
    
    # إحصائياتي
    elif text in ['نقاطي', 'احصائياتي', 'stats']:
        stats = get_user_stats(user_id)
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(
                alt_text="إحصائياتك",
                contents=get_stats_message(stats, user_id),
                quick_reply=get_quick_reply()
            )
        )
        return
    
    # لوحة الصدارة
    elif text in ['الصدارة', 'صدارة', 'leaderboard']:
        leaders = get_leaderboard()
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(
                alt_text="لوحة الصدارة",
                contents=get_leaderboard_message(leaders),
                quick_reply=get_quick_reply()
            )
        )
        return
    
    # إيقاف اللعبة
    elif text in ['إيقاف', 'ايقاف', 'stop']:
        if game_id in active_games:
            game_type = active_games[game_id].get('type', 'اللعبة')
            del active_games[game_id]
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(
                    text=f"تم إيقاف {game_type}",
                    quick_reply=get_quick_reply()
                )
            )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(
                    text="لا توجد لعبة نشطة",
                    quick_reply=get_quick_reply()
                )
            )
        return
    
    # ===== التسجيل والانسحاب =====
    
    # الانضمام
    elif text in ['انضم', 'join']:
        if user_id in registered_players:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(
                    text=f"أنت مسجل بالفعل يا {display_name}\n\nيمكنك اللعب في جميع الألعاب",
                    quick_reply=get_quick_reply()
                )
            )
        else:
            registered_players.add(user_id)
            
            # إضافته لجميع الألعاب النشطة
            for gid, game_data in active_games.items():
                if 'participants' not in game_data:
                    game_data['participants'] = set()
                game_data['participants'].add(user_id)
            
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(
                    text=f"تم تسجيلك يا {display_name}\n\nيمكنك الآن اللعب في جميع الألعاب\nإجاباتك ستُحسب تلقائياً",
                    quick_reply=get_quick_reply()
                )
            )
        return
    
    # الانسحاب
    elif text in ['انسحب', 'leave']:
        if user_id in registered_players:
            registered_players.remove(user_id)
            
            # إزالته من جميع الألعاب النشطة
            for gid, game_data in active_games.items():
                if 'participants' in game_data and user_id in game_data['participants']:
                    game_data['participants'].remove(user_id)
            
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(
                    text=f"تم انسحابك يا {display_name}\n\nيمكنك الانضمام مرة أخرى بكتابة 'انضم'",
                    quick_reply=get_quick_reply()
                )
            )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(
                    text="أنت غير مسجل\n\nاكتب 'انضم' للتسجيل",
                    quick_reply=get_quick_reply()
                )
            )
        return
    
    # ===== أمر لمح - طلب تلميح =====
    
    elif text in ['لمح', 'تلميح', 'hint']:
        if game_id not in active_games:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(
                    text="لا توجد لعبة نشطة\n\nابدأ لعبة أولاً",
                    quick_reply=get_quick_reply()
                )
            )
            return
        
        # الحصول على اللعبة الحالية
        game_data = active_games[game_id]
        game = game_data['game']
        
        # محاولة الحصول على تلميح
        try:
            if hasattr(game, 'get_hint'):
                hint = game.get_hint()
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(
                        text=f"💡 {hint}",
                        quick_reply=get_quick_reply()
                    )
                )
            else:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(
                        text="هذه اللعبة لا تدعم التلميحات",
                        quick_reply=get_quick_reply()
                    )
                )
        except Exception as e:
            logger.error(f"خطأ في لمح: {e}")
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(
                    text="حدث خطأ في الحصول على التلميح",
                    quick_reply=get_quick_reply()
                )
            )
        return
    
    # ===== أمر جاوب - طلب الحل الكامل =====
    
    elif text in ['جاوب', 'حل', 'الحل', 'answer']:
        if game_id not in active_games:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(
                    text="لا توجد لعبة نشطة\n\nابدأ لعبة أولاً",
                    quick_reply=get_quick_reply()
                )
            )
            return
        
        # الحصول على اللعبة الحالية
        game_data = active_games[game_id]
        game = game_data['game']
        
        # محاولة الحصول على الإجابة الكاملة
        try:
            if hasattr(game, 'get_answer'):
                answer = game.get_answer()
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(
                        text=f"✅ الإجابة:\n{answer}",
                        quick_reply=get_quick_reply()
                    )
                )
            else:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(
                        text="هذه اللعبة لا تدعم إظهار الإجابة",
                        quick_reply=get_quick_reply()
                    )
                )
        except Exception as e:
            logger.error(f"خطأ في جاوب: {e}")
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(
                    text="حدث خطأ في الحصول على الإجابة",
                    quick_reply=get_quick_reply()
                )
            )
        return
    
    # ===== بدء الألعاب =====
    
    elif text in ['ذكاء', 'iq']:
        game = IQGame(line_bot_api, use_ai=USE_AI, get_api_key=get_gemini_api_key, switch_key=switch_gemini_key)
        participants = registered_players.copy()
        participants.add(user_id)
        
        active_games[game_id] = {
            'game': game,
            'type': 'ذكاء',
            'created_at': datetime.now(),
            'participants': participants,
            'round_system': BaseGameWithRounds(max_rounds=10)
        }
        response = game.start_game()
        if hasattr(response, 'quick_reply') and response.quick_reply is None:
            response.quick_reply = get_quick_reply()
        line_bot_api.reply_message(event.reply_token, response)
        return
    
    elif text in ['كلمة ولون', 'لون', 'color']:
        game = WordColorGame(line_bot_api, use_ai=USE_AI, get_api_key=get_gemini_api_key, switch_key=switch_gemini_key)
        participants = registered_players.copy()
        participants.add(user_id)
        
        active_games[game_id] = {
            'game': game,
            'type': 'كلمة ولون',
            'created_at': datetime.now(),
            'participants': participants,
            'round_system': BaseGameWithRounds(max_rounds=10)
        }
        response = game.start_game()
        if hasattr(response, 'quick_reply') and response.quick_reply is None:
            response.quick_reply = get_quick_reply()
        line_bot_api.reply_message(event.reply_token, response)
        return
    
    elif text in ['سلسلة', 'chain']:
        game = ChainWordsGame(line_bot_api)
        participants = registered_players.copy()
        participants.add(user_id)
        
        active_games[game_id] = {
            'game': game,
            'type': 'سلسلة',
            'created_at': datetime.now(),
            'participants': participants,
            'round_system': BaseGameWithRounds(max_rounds=10)
        }
        response = game.start_game()
        if hasattr(response, 'quick_reply') and response.quick_reply is None:
            response.quick_reply = get_quick_reply()
        line_bot_api.reply_message(event.reply_token, response)
        return
    
    elif text in ['ترتيب الحروف', 'ترتيب', 'scramble']:
        game = ScrambleWordGame(line_bot_api)
        participants = registered_players.copy()
        participants.add(user_id)
        
        active_games[game_id] = {
            'game': game,
            'type': 'ترتيب',
            'created_at': datetime.now(),
            'participants': participants,
            'round_system': BaseGameWithRounds(max_rounds=10)
        }
        response = game.start_game()
        if hasattr(response, 'quick_reply') and response.quick_reply is None:
            response.quick_reply = get_quick_reply()
        line_bot_api.reply_message(event.reply_token, response)
        return
    
    elif text in ['تكوين كلمات', 'تكوين', 'letters']:
        game = LettersWordsGame(line_bot_api, use_ai=USE_AI, get_api_key=get_gemini_api_key, switch_key=switch_gemini_key)
        participants = registered_players.copy()
        participants.add(user_id)
        
        active_games[game_id] = {
            'game': game,
            'type': 'تكوين',
            'created_at': datetime.now(),
            'participants': participants,
            'round_system': BaseGameWithRounds(max_rounds=10)
        }
        response = game.start_game()
        if hasattr(response, 'quick_reply') and response.quick_reply is None:
            response.quick_reply = get_quick_reply()
        line_bot_api.reply_message(event.reply_token, response)
        return
    
    elif text in ['أسرع', 'fast']:
        game = FastTypingGame(line_bot_api)
        participants = registered_players.copy()
        participants.add(user_id)
        
        active_games[game_id] = {
            'game': game,
            'type': 'أسرع',
            'created_at': datetime.now(),
            'participants': participants,
            'round_system': BaseGameWithRounds(max_rounds=10)
        }
        response = game.start_game()
        if hasattr(response, 'quick_reply') and response.quick_reply is None:
            response.quick_reply = get_quick_reply()
        line_bot_api.reply_message(event.reply_token, response)
        return
    
    elif text in ['لعبة', 'game']:
        game = HumanAnimalPlantGame(line_bot_api, use_ai=USE_AI, get_api_key=get_gemini_api_key, switch_key=switch_gemini_key)
        participants = registered_players.copy()
        participants.add(user_id)
        
        active_games[game_id] = {
            'game': game,
            'type': 'لعبة',
            'created_at': datetime.now(),
            'participants': participants,
            'round_system': BaseGameWithRounds(max_rounds=10)
        }
        response = game.start_game()
        if hasattr(response, 'quick_reply') and response.quick_reply is None:
            response.quick_reply = get_quick_reply()
        line_bot_api.reply_message(event.reply_token, response)
        return
    
    elif text in ['خمن', 'guess']:
        game = GuessGame(line_bot_api)
        participants = registered_players.copy()
        participants.add(user_id)
        
        active_games[game_id] = {
            'game': game,
            'type': 'خمن',
            'created_at': datetime.now(),
            'participants': participants,
            'round_system': BaseGameWithRounds(max_rounds=10)
        }
        response = game.start_game()
        if hasattr(response, 'quick_reply') and response.quick_reply is None:
            response.quick_reply = get_quick_reply()
        line_bot_api.reply_message(event.reply_token, response)
        return
    
    elif text in ['توافق', 'compatibility']:
        game = CompatibilityGame(line_bot_api)
        participants = registered_players.copy()
        participants.add(user_id)
        
        active_games[game_id] = {
            'game': game,
            'type': 'توافق',
            'created_at': datetime.now(),
            'participants': participants,
            'round_system': BaseGameWithRounds(max_rounds=10)
        }
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text="لعبة التوافق\n\nاكتب اسمين مفصولين بمسافة\nمثال: ميش عبير",
                quick_reply=get_quick_reply()
            )
        )
        return
    
    elif text in ['رياضيات', 'math']:
        game = MathGame(line_bot_api)
        participants = registered_players.copy()
        participants.add(user_id)
        
        active_games[game_id] = {
            'game': game,
            'type': 'رياضيات',
            'created_at': datetime.now(),
            'participants': participants,
            'round_system': BaseGameWithRounds(max_rounds=10)
        }
        response = game.start_game()
        if hasattr(response, 'quick_reply') and response.quick_reply is None:
            response.quick_reply = get_quick_reply()
        line_bot_api.reply_message(event.reply_token, response)
        return
    
    elif text in ['ذاكرة', 'memory']:
        game = MemoryGame(line_bot_api)
        participants = registered_players.copy()
        participants.add(user_id)
        
        active_games[game_id] = {
            'game': game,
            'type': 'ذاكرة',
            'created_at': datetime.now(),
            'participants': participants,
            'round_system': BaseGameWithRounds(max_rounds=10)
        }
        response = game.start_game()
        if hasattr(response, 'quick_reply') and response.quick_reply is None:
            response.quick_reply = get_quick_reply()
        line_bot_api.reply_message(event.reply_token, response)
        return
    
    elif text in ['لغز', 'riddle']:
        game = RiddleGame(line_bot_api)
        participants = registered_players.copy()
        participants.add(user_id)
        
        active_games[game_id] = {
            'game': game,
            'type': 'لغز',
            'created_at': datetime.now(),
            'participants': participants,
            'round_system': BaseGameWithRounds(max_rounds=10)
        }
        response = game.start_game()
        if hasattr(response, 'quick_reply') and response.quick_reply is None:
            response.quick_reply = get_quick_reply()
        line_bot_api.reply_message(event.reply_token, response)
        return
    
    elif text in ['ضد', 'opposite']:
        game = OppositeGame(line_bot_api)
        participants = registered_players.copy()
        participants.add(user_id)
        
        active_games[game_id] = {
            'game': game,
            'type': 'ضد',
            'created_at': datetime.now(),
            'participants': participants,
            'round_system': BaseGameWithRounds(max_rounds=10)
        }
        response = game.start_game()
        if hasattr(response, 'quick_reply') and response.quick_reply is None:
            response.quick_reply = get_quick_reply()
        line_bot_api.reply_message(event.reply_token, response)
        return
    
    elif text in ['إيموجي', 'ايموجي', 'emoji']:
        game = EmojiGame(line_bot_api)
        participants = registered_players.copy()
        participants.add(user_id)
        
        active_games[game_id] = {
            'game': game,
            'type': 'ايموجي',
            'created_at': datetime.now(),
            'participants': participants,
            'round_system': BaseGameWithRounds(max_rounds=10)
        }
        response = game.start_game()
        if hasattr(response, 'quick_reply') and response.quick_reply is None:
            response.quick_reply = get_quick_reply()
        line_bot_api.reply_message(event.reply_token, response)
        return
    
    elif text in ['أغنية', 'اغنية', 'song']:
        game = SongGame(line_bot_api)
        participants = registered_players.copy()
        participants.add(user_id)
        
        active_games[game_id] = {
            'game': game,
            'type': 'أغنية',
            'created_at': datetime.now(),
            'participants': participants,
            'round_system': BaseGameWithRounds(max_rounds=10)
        }
        response = game.start_game()
        if hasattr(response, 'quick_reply') and response.quick_reply is None:
            response.quick_reply = get_quick_reply()
        line_bot_api.reply_message(event.reply_token, response)
        return
    
    # ===== معالجة إجابات الألعاب =====
    
    if game_id in active_games:
        game_data = active_games[game_id]
        
        # التحقق من المشاركة
        if user_id not in registered_players and 'participants' in game_data and user_id not in game_data['participants']:
            return
        
        game = game_data['game']
        round_system = game_data.get('round_system')
        
        result = game.check_answer(text, user_id, display_name)
        
        if result:
            points = result.get('points', 0)
            
            # إضافة النقاط لنظام الجولات
            if round_system and points > 0:
                round_system.add_score(user_id, display_name, points)
                round_system.increment_round()
                
                # التحقق من انتهاء اللعبة
                if round_system.is_game_over():
                    # حفظ النقاط النهائية لجميع اللاعبين
                    for player_id, player_score in round_system.scores.items():
                        player_name = round_system.player_names.get(player_id, "لاعب")
                        update_user_points(player_id, player_name, player_score, 
                                         player_id == max(round_system.scores, key=round_system.scores.get),
                                         game_data['type'])
                    
                    # حذف اللعبة
                    del active_games[game_id]
                    
                    # إرسال رسالة الفائز
                    line_bot_api.reply_message(
                        event.reply_token,
                        FlexSendMessage(
                            alt_text="انتهت اللعبة",
                            contents=round_system.get_winner_message(),
                            quick_reply=get_quick_reply()
                        )
                    )
                    return
                else:
                    # عرض الجولة الحالية
                    round_info = f"\n\nالجولة {round_system.current_round}/{round_system.max_rounds}"
                    if hasattr(result.get('response'), 'text'):
                        result['response'].text += round_info
            
            # الحفظ العادي للنقاط إذا لم يكن هناك نظام جولات
            elif points > 0:
                update_user_points(user_id, display_name, points, result.get('won', False), game_data['type'])
            
            if result.get('game_over', False) and not round_system:
                del active_games[game_id]
                response = TextSendMessage(
                    text=result.get('message', 'انتهت اللعبة'),
                    quick_reply=get_quick_reply()
                )
            else:
                response = result.get('response', TextSendMessage(text=result.get('message', '')))
                if hasattr(response, 'quick_reply') and response.quick_reply is None:
                    response.quick_reply = get_quick_reply()
            
            line_bot_api.reply_message(event.reply_token, response)
        return
    
    # ===== استخدام الذكاء الاصطناعي للرسائل العامة =====
    
    # إذا كان المستخدم مسجلاً وأرسل رسالة عادية، استخدم AI
    if user_id in registered_players and USE_AI and len(text) > 2:
        try:
            import asyncio
            # تشغيل دالة async
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            ai_response = loop.run_until_complete(get_ai_response(text, user_id))
            loop.close()
            
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(
                    text=ai_response,
                    quick_reply=get_quick_reply()
                )
            )
        except Exception as e:
            logger.error(f"خطأ في AI response: {e}")
    
    # تجاهل أي رسائل أخرى
    return

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"تشغيل البوت على المنفذ {port}")
    app.run(host='0.0.0.0', port=port)
