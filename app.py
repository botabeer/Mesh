"""
app.py - LINE Games Bot - Modern Neumorphism Design
بوت ألعاب احترافي بتصميم عصري
"""

from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    FlexSendMessage
)
import os
import logging
from datetime import datetime
import sqlite3
from collections import defaultdict
import threading
import time

# ===================================
# إعداد السجلات
# ===================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# ===================================
# إعدادات LINE Bot
# ===================================
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', 'YOUR_TOKEN')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET', 'YOUR_SECRET')

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# ===================================
# تخزين البيانات
# ===================================
active_games = {}
registered_players = set()
user_scores = defaultdict(int)

# ===================================
# قاعدة البيانات
# ===================================
DB_NAME = 'game_scores.db'

def init_db():
    """إنشاء قاعدة البيانات"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (user_id TEXT PRIMARY KEY,
                  display_name TEXT,
                  total_points INTEGER DEFAULT 0,
                  games_played INTEGER DEFAULT 0,
                  wins INTEGER DEFAULT 0,
                  last_played TEXT)''')
    conn.commit()
    conn.close()

init_db()

def update_user_score(user_id, display_name, points, won=False):
    """تحديث نقاط المستخدم"""
    conn = sqlite3.connect(DB_NAME)
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
        c.execute('''INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)''',
                  (user_id, display_name, points, 1, 1 if won else 0,
                   datetime.now().isoformat()))
    
    conn.commit()
    conn.close()

def get_leaderboard(limit=5):
    """الحصول على لوحة الصدارة"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''SELECT display_name, total_points FROM users 
                 ORDER BY total_points DESC LIMIT ?''', (limit,))
    leaders = c.fetchall()
    conn.close()
    return leaders

# ===================================
# تصاميم Flex Messages - Neumorphism
# ===================================

class FlexDesign:
    """تصاميم Neumorphism الحديثة"""
    
    # الألوان
    BG = '#E0E5EC'
    TEXT_PRIMARY = '#4A5568'
    TEXT_SECONDARY = '#A3B1C6'
    ACCENT = '#667eea'
    
    @staticmethod
    def main_menu():
        """القائمة الرئيسية"""
        return {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "Neumorphism Soft 🎮",
                        "weight": "bold",
                        "size": "xl",
                        "align": "center",
                        "color": FlexDesign.TEXT_PRIMARY
                    },
                    {
                        "type": "text",
                        "text": "تأثير 3D - عمق ناعم",
                        "size": "sm",
                        "align": "center",
                        "color": FlexDesign.TEXT_SECONDARY,
                        "margin": "sm"
                    },
                    {
                        "type": "separator",
                        "margin": "xl",
                        "color": "#ddd"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            FlexDesign._game_button("🔤", "تكوين الكلمات", "letters"),
                            FlexDesign._game_button("⚡", "أسرع إجابة", "fast"),
                            FlexDesign._game_button("🔀", "ترتيب الحروف", "scramble"),
                            FlexDesign._game_button("🔗", "سلسلة الكلمات", "chain"),
                            FlexDesign._game_button("🧠", "أسئلة ذكاء", "iq")
                        ],
                        "spacing": "md",
                        "margin": "xl"
                    },
                    {
                        "type": "separator",
                        "margin": "xl",
                        "color": "#ddd"
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": "🏆 الصدارة",
                                    "text": "الصدارة"
                                },
                                "style": "secondary",
                                "height": "sm"
                            },
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": "👥 انضم",
                                    "text": "انضم"
                                },
                                "style": "primary",
                                "height": "sm",
                                "color": FlexDesign.ACCENT
                            }
                        ],
                        "spacing": "sm",
                        "margin": "xl"
                    }
                ],
                "backgroundColor": FlexDesign.BG,
                "paddingAll": "24px"
            }
        }
    
    @staticmethod
    def _game_button(emoji, name, game_id):
        """زر لعبة"""
        return {
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "text",
                    "text": emoji,
                    "size": "xl",
                    "flex": 0
                },
                {
                    "type": "text",
                    "text": name,
                    "size": "md",
                    "color": FlexDesign.TEXT_PRIMARY,
                    "flex": 1,
                    "margin": "md",
                    "weight": "bold"
                },
                {
                    "type": "button",
                    "action": {
                        "type": "message",
                        "label": "▶",
                        "text": game_id
                    },
                    "style": "primary",
                    "height": "sm",
                    "flex": 0,
                    "color": FlexDesign.ACCENT
                }
            ],
            "spacing": "md",
            "paddingAll": "12px",
            "cornerRadius": "16px",
            "backgroundColor": FlexDesign.BG
        }
    
    @staticmethod
    def game_screen(game_name, question, letters=None, round_num=1, total_rounds=5):
        """شاشة اللعبة"""
        contents = [
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": f"■ {game_name}",
                        "weight": "bold",
                        "size": "lg",
                        "color": FlexDesign.TEXT_PRIMARY,
                        "flex": 1
                    },
                    {
                        "type": "text",
                        "text": f"سؤال {round_num}/{total_rounds}",
                        "size": "sm",
                        "color": FlexDesign.TEXT_SECONDARY,
                        "align": "end"
                    }
                ]
            },
            {
                "type": "separator",
                "margin": "lg",
                "color": "#ddd"
            }
        ]
        
        # الحروف إذا كانت موجودة
        if letters:
            letter_boxes = []
            for letter in letters:
                letter_boxes.append({
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": letter,
                            "size": "xxl",
                            "color": FlexDesign.ACCENT,
                            "align": "center",
                            "weight": "bold"
                        }
                    ],
                    "width": "60px",
                    "height": "60px",
                    "backgroundColor": FlexDesign.BG,
                    "cornerRadius": "16px",
                    "justifyContent": "center"
                })
            
            contents.append({
                "type": "box",
                "layout": "horizontal",
                "contents": letter_boxes,
                "spacing": "sm",
                "margin": "xl",
                "justifyContent": "center",
                "paddingAll": "20px",
                "cornerRadius": "20px",
                "backgroundColor": FlexDesign.BG
            })
        
        # السؤال
        contents.append({
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": question,
                    "size": "md",
                    "color": FlexDesign.TEXT_PRIMARY,
                    "align": "center",
                    "wrap": True
                }
            ],
            "paddingAll": "20px",
            "cornerRadius": "16px",
            "backgroundColor": FlexDesign.BG,
            "margin": "lg"
        })
        
        # الأزرار
        contents.append({
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "button",
                    "action": {
                        "type": "message",
                        "label": "الحل",
                        "text": "الحل"
                    },
                    "style": "secondary",
                    "height": "sm"
                },
                {
                    "type": "button",
                    "action": {
                        "type": "message",
                        "label": "تلميح",
                        "text": "تلميح"
                    },
                    "style": "primary",
                    "height": "sm",
                    "color": FlexDesign.ACCENT
                }
            ],
            "spacing": "sm",
            "margin": "xl"
        })
        
        return {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": contents,
                "backgroundColor": FlexDesign.BG,
                "paddingAll": "24px"
            }
        }
    
    @staticmethod
    def correct_answer(player_name, points):
        """إجابة صحيحة"""
        return {
            "type": "bubble",
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
                                "text": "✓",
                                "size": "4xl",
                                "color": FlexDesign.ACCENT,
                                "align": "center",
                                "weight": "bold"
                            }
                        ],
                        "width": "80px",
                        "height": "80px",
                        "backgroundColor": FlexDesign.BG,
                        "cornerRadius": "full",
                        "justifyContent": "center",
                        "offsetStart": "50%",
                        "position": "relative"
                    },
                    {
                        "type": "text",
                        "text": "إجابة صحيحة!",
                        "weight": "bold",
                        "size": "xl",
                        "color": FlexDesign.TEXT_PRIMARY,
                        "align": "center",
                        "margin": "xl"
                    },
                    {
                        "type": "text",
                        "text": player_name,
                        "size": "md",
                        "color": FlexDesign.TEXT_SECONDARY,
                        "align": "center",
                        "margin": "sm"
                    },
                    {
                        "type": "separator",
                        "margin": "xl",
                        "color": "#ddd"
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": "النقاط",
                                "size": "sm",
                                "color": FlexDesign.TEXT_SECONDARY,
                                "flex": 1
                            },
                            {
                                "type": "text",
                                "text": f"+{points}",
                                "size": "xxl",
                                "color": FlexDesign.ACCENT,
                                "flex": 1,
                                "align": "end",
                                "weight": "bold"
                            }
                        ],
                        "margin": "xl"
                    }
                ],
                "backgroundColor": FlexDesign.BG,
                "paddingAll": "28px"
            }
        }
    
    @staticmethod
    def leaderboard(leaders):
        """لوحة الصدارة"""
        players_list = []
        for i, (name, score) in enumerate(leaders, 1):
            is_top = (i <= 3)
            players_list.append({
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": str(i),
                        "size": "sm",
                        "color": FlexDesign.ACCENT if is_top else FlexDesign.TEXT_PRIMARY,
                        "align": "center",
                        "weight": "bold",
                        "flex": 0
                    },
                    {
                        "type": "text",
                        "text": name,
                        "size": "md" if is_top else "sm",
                        "color": FlexDesign.TEXT_PRIMARY,
                        "flex": 3,
                        "margin": "md",
                        "weight": "bold" if is_top else "regular"
                    },
                    {
                        "type": "text",
                        "text": f"{score} نقطة",
                        "size": "md" if is_top else "sm",
                        "color": FlexDesign.ACCENT if is_top else FlexDesign.TEXT_SECONDARY,
                        "flex": 2,
                        "align": "end",
                        "weight": "bold" if is_top else "regular"
                    }
                ],
                "spacing": "md",
                "paddingAll": "12px",
                "backgroundColor": FlexDesign.BG,
                "cornerRadius": "12px",
                "margin": "sm" if i > 1 else "none"
            })
        
        return {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "🏆 لوحة الصدارة",
                        "weight": "bold",
                        "size": "xl",
                        "color": FlexDesign.TEXT_PRIMARY,
                        "align": "center"
                    },
                    {
                        "type": "separator",
                        "margin": "lg",
                        "color": "#ddd"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": players_list,
                        "margin": "lg"
                    }
                ],
                "backgroundColor": FlexDesign.BG,
                "paddingAll": "24px"
            }
        }

# ===================================
# الألعاب
# ===================================

class LettersGame:
    """لعبة تكوين الكلمات"""
    
    def __init__(self):
        self.letters = ['ق', 'ي', 'ر', 'ل', 'ر', 'ل']
        self.valid_words = ['قرر', 'ليرة', 'رير']
        self.found_words = []
        self.round = 1
        self.max_rounds = 5
    
    def start(self):
        return FlexDesign.game_screen(
            "لعبة تكوين الكلمات",
            "كوّن 3 كلمات من هذه الحروف\nاكتب كلمة واحدة في كل رسالة",
            self.letters,
            self.round,
            self.max_rounds
        )
    
    def check_answer(self, answer):
        answer = answer.strip()
        if answer in self.valid_words and answer not in self.found_words:
            self.found_words.append(answer)
            return True, 10
        return False, 0

class FastGame:
    """لعبة أسرع إجابة"""
    
    def __init__(self):
        self.question = "اكتب كلمة تبدأ بحرف 'ع'"
        self.correct_answers = ['عمر', 'علي', 'عائشة', 'عبد']
        self.answered = False
    
    def start(self):
        return FlexDesign.game_screen(
            "لعبة أسرع إجابة",
            self.question,
            None,
            1,
            5
        )
    
    def check_answer(self, answer):
        if not self.answered and answer in self.correct_answers:
            self.answered = True
            return True, 20
        return False, 0

# ===================================
# Routes
# ===================================

@app.route("/", methods=['GET'])
def home():
    """الصفحة الرئيسية"""
    return """
    <html>
        <head>
            <title>LINE Games Bot 🎮</title>
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body {
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    min-height: 100vh;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }
                .card {
                    background: rgba(255, 255, 255, 0.1);
                    backdrop-filter: blur(10px);
                    border-radius: 30px;
                    padding: 60px 40px;
                    max-width: 600px;
                    text-align: center;
                    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
                }
                h1 { font-size: 4em; margin-bottom: 10px; }
                h2 { font-size: 2em; margin-bottom: 10px; }
                p { font-size: 1.2em; opacity: 0.9; margin-bottom: 30px; }
                .stats {
                    display: grid;
                    grid-template-columns: repeat(3, 1fr);
                    gap: 20px;
                    margin-top: 30px;
                }
                .stat {
                    background: rgba(255, 255, 255, 0.2);
                    padding: 20px;
                    border-radius: 20px;
                }
                .stat-value {
                    font-size: 2.5em;
                    font-weight: bold;
                    margin-bottom: 5px;
                }
                .stat-label {
                    font-size: 0.9em;
                    opacity: 0.8;
                }
            </style>
        </head>
        <body>
            <div class="card">
                <h1>🎮</h1>
                <h2>LINE Games Bot</h2>
                <p>بوت ألعاب احترافي بتصميم Neumorphism</p>
                
                <div class="stats">
                    <div class="stat">
                        <div class="stat-value">5</div>
                        <div class="stat-label">ألعاب</div>
                    </div>
                    <div class="stat">
                        <div class="stat-value">✓</div>
                        <div class="stat-label">يعمل</div>
                    </div>
                    <div class="stat">
                        <div class="stat-value">⚡</div>
                        <div class="stat-label">سريع</div>
                    </div>
                </div>
            </div>
        </body>
    </html>
    """

@app.route("/callback", methods=['POST'])
def callback():
    """معالج webhook"""
    signature = request.headers.get('X-Line-Signature', '')
    body = request.get_data(as_text=True)
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    """معالج الرسائل"""
    user_id = event.source.user_id
    text = event.message.text.strip()
    game_id = event.source.group_id if hasattr(event.source, 'group_id') else user_id
    
    # الحصول على اسم المستخدم
    try:
        profile = line_bot_api.get_profile(user_id)
        display_name = profile.display_name
    except:
        display_name = "مستخدم"
    
    # الأوامر الأساسية
    if text in ['البداية', 'start', 'ابدأ', 'القائمة', 'menu']:
        flex = FlexDesign.main_menu()
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(alt_text="القائمة الرئيسية", contents=flex)
        )
        return
    
    # الانضمام
    if text in ['انضم', 'join']:
        registered_players.add(user_id)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"✅ مرحباً بك {display_name}!\n\nتم تسجيلك بنجاح\nيمكنك الآن اللعب في جميع الألعاب")
        )
        return
    
    # الصدارة
    if text in ['الصدارة', 'leaderboard']:
        leaders = get_leaderboard()
        if leaders:
            flex = FlexDesign.leaderboard(leaders)
            line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage(alt_text="لوحة الصدارة", contents=flex)
            )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="لا توجد بيانات بعد\nابدأ اللعب لتظهر على اللوحة!")
            )
        return
    
    # بدء الألعاب
    if text == 'letters':
        game = LettersGame()
        active_games[game_id] = {
            'game': game,
            'type': 'letters'
        }
        flex = game.start()
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(alt_text="لعبة تكوين الكلمات", contents=flex)
        )
        return
    
    if text == 'fast':
        game = FastGame()
        active_games[game_id] = {
            'game': game,
            'type': 'fast'
        }
        flex = game.start()
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(alt_text="لعبة أسرع إجابة", contents=flex)
        )
        return
    
    # معالجة الإجابات
    if game_id in active_games:
        game_data = active_games[game_id]
        game = game_data['game']
        
        is_correct, points = game.check_answer(text)
        
        if is_correct:
            update_user_score(user_id, display_name, points)
            flex = FlexDesign.correct_answer(display_name, points)
            line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage(alt_text="إجابة صحيحة", contents=flex)
            )
        return

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"🚀 بدء الخادم على المنفذ {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
