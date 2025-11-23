"""
Bot Mesh - Enhanced Silent Bot (All-in-One)
Created by: Abeer Aldosari © 2025
بوت صامت - يرد فقط على المسجلين والأوامر
"""
import os
import logging
import sqlite3
from datetime import datetime
from flask import Flask, request, abort, jsonify

# LINE SDK v3
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi,
    ReplyMessageRequest, TextMessage, FlexMessage, FlexContainer
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent, FollowEvent, MentionEvent

# ==================== Configuration ====================
LINE_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', '')
LINE_SECRET = os.getenv('LINE_CHANNEL_SECRET', '')
DB_PATH = os.getenv('DB_PATH', 'data/game.db')

# 9 Themes - Professional 3D Colors
THEMES = {
    'white': {'bg': '#E0E5EC', 'card': '#D1D9E6', 'primary': '#667EEA', 'text': '#1A202C', 'text2': '#4A5568', 'name': 'أبيض'},
    'black': {'bg': '#0F0F1A', 'card': '#1A1A2E', 'primary': '#00D9FF', 'text': '#F7FAFC', 'text2': '#CBD5E0', 'name': 'أسود'},
    'gray': {'bg': '#2D3748', 'card': '#4A5568', 'primary': '#68D391', 'text': '#F7FAFC', 'text2': '#E2E8F0', 'name': 'رمادي'},
    'blue': {'bg': '#1E3A8A', 'card': '#1E40AF', 'primary': '#60A5FA', 'text': '#F0F9FF', 'text2': '#BFDBFE', 'name': 'أزرق'},
    'green': {'bg': '#14532D', 'card': '#166534', 'primary': '#4ADE80', 'text': '#F0FDF4', 'text2': '#BBF7D0', 'name': 'أخضر'},
    'pink': {'bg': '#FFF1F2', 'card': '#FFE4E6', 'primary': '#EC4899', 'text': '#831843', 'text2': '#9F1239', 'name': 'وردي'},
    'orange': {'bg': '#431407', 'card': '#7C2D12', 'primary': '#FB923C', 'text': '#FFF7ED', 'text2': '#FDBA74', 'name': 'برتقالي'},
    'purple': {'bg': '#3B0764', 'card': '#581C87', 'primary': '#C084FC', 'text': '#FAF5FF', 'text2': '#E9D5FF', 'name': 'بنفسجي'},
    'brown': {'bg': '#1C0A00', 'card': '#44403C', 'primary': '#A78BFA', 'text': '#FAFAF9', 'text2': '#D6D3D1', 'name': 'بني'}
}

# ==================== Logging ====================
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ==================== Database ====================
class Database:
    def __init__(self, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            uid TEXT PRIMARY KEY,
            name TEXT,
            points INTEGER DEFAULT 0,
            games INTEGER DEFAULT 0,
            wins INTEGER DEFAULT 0,
            theme TEXT DEFAULT 'white',
            registered BOOLEAN DEFAULT 0,
            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        self.conn.commit()

    def get_user(self, uid):
        self.cursor.execute("SELECT * FROM users WHERE uid=?", (uid,))
        row = self.cursor.fetchone()
        if row:
            return {'uid': row[0], 'name': row[1], 'points': row[2], 'games': row[3], 
                    'wins': row[4], 'theme': row[5], 'registered': bool(row[6]), 
                    'joined_at': row[7], 'last_active': row[8]}
        return None

    def add_or_update_user(self, uid, name, registered=False):
        self.cursor.execute("""
        INSERT INTO users(uid, name, registered) VALUES(?, ?, ?)
        ON CONFLICT(uid) DO UPDATE SET name=excluded.name, last_active=CURRENT_TIMESTAMP
        """, (uid, name, registered))
        self.conn.commit()

    def register_user(self, uid):
        self.cursor.execute("UPDATE users SET registered=1 WHERE uid=?", (uid,))
        self.conn.commit()

    def unregister_user(self, uid):
        self.cursor.execute("UPDATE users SET registered=0 WHERE uid=?", (uid,))
        self.conn.commit()

    def is_registered(self, uid):
        user = self.get_user(uid)
        return user and user['registered']

    def update_points(self, uid, points=0, won=False):
        user = self.get_user(uid)
        if user:
            new_points = user['points'] + points
            new_games = user['games'] + 1
            new_wins = user['wins'] + (1 if won else 0)
            self.cursor.execute("""
            UPDATE users SET points=?, games=?, wins=?, last_active=CURRENT_TIMESTAMP
            WHERE uid=?
            """, (new_points, new_games, new_wins, uid))
            self.conn.commit()

    def update_theme(self, uid, theme):
        self.cursor.execute("UPDATE users SET theme=?, last_active=CURRENT_TIMESTAMP WHERE uid=?", (theme, uid))
        self.conn.commit()

    def get_leaderboard(self, limit=10):
        self.cursor.execute("SELECT name, points, games, wins FROM users WHERE registered=1 ORDER BY points DESC LIMIT ?", (limit,))
        return [{'name': r[0], 'points': r[1], 'games': r[2], 'wins': r[3]} for r in self.cursor.fetchall()]

# ==================== Game Manager ====================
class GameManager:
    def __init__(self):
        self.active_games = {}

    def start_game(self, gid, game, game_type):
        self.active_games[gid] = {"game": game, "type": game_type}

    def get_game(self, gid):
        return self.active_games.get(gid)

    def end_game(self, gid):
        self.active_games.pop(gid, None)

# ==================== Flask & LINE ====================
app = Flask(__name__)
configuration = Configuration(access_token=LINE_TOKEN)
handler = WebhookHandler(LINE_SECRET)
db = Database(DB_PATH)
gm = GameManager()

# Game imports will be added here
GAMES = {}

# ==================== Helper Functions ====================
def get_name(uid):
    try:
        with ApiClient(configuration) as api_client:
            line_api = MessagingApi(api_client)
            profile = line_api.get_profile(uid)
            return profile.display_name
    except:
        return 'لاعب'

def get_theme(uid):
    user = db.get_user(uid)
    return user.get('theme', 'white') if user else 'white'

def send_flex(reply_token, content, alt='رسالة'):
    try:
        with ApiClient(configuration) as api_client:
            line_api = MessagingApi(api_client)
            line_api.reply_message(ReplyMessageRequest(
                replyToken=reply_token,
                messages=[FlexMessage(altText=alt, contents=FlexContainer.from_dict(content))]
            ))
            return True
    except Exception as e:
        logger.error(f'Error: {e}')
    return False

def send_text(reply_token, text):
    try:
        with ApiClient(configuration) as api_client:
            line_api = MessagingApi(api_client)
            line_api.reply_message(ReplyMessageRequest(
                replyToken=reply_token,
                messages=[TextMessage(text=text)]
            ))
            return True
    except Exception as e:
        logger.error(f'Error: {e}')
    return False

# ==================== Flex Builders ====================
def create_main_menu(uid):
    """القائمة الرئيسية - 12 لعبة بدون إيموجي"""
    theme = THEMES.get(get_theme(uid), THEMES['white'])
    user = db.get_user(uid)
    name = user['name'] if user else 'لاعب'
    is_registered = db.is_registered(uid)
    
    games = [
        ('ذكاء', 'ذكاء'), ('لون', 'لون'), ('رياضيات', 'رياضيات'),
        ('أسرع', 'أسرع'), ('ترتيب', 'ترتيب'), ('ضد', 'ضد'),
        ('تكوين', 'تكوين'), ('أغنية', 'أغنية'), ('لعبة', 'لعبة'),
        ('سلسلة', 'سلسلة'), ('خمن', 'خمن'), ('توافق', 'توافق')
    ]
    
    game_buttons = []
    for i in range(0, 12, 3):
        row = {
            "type": "box",
            "layout": "horizontal",
            "contents": [],
            "spacing": "sm",
            "margin": "sm"
        }
        for label, cmd in games[i:i+3]:
            row["contents"].append({
                "type": "button",
                "action": {"type": "message", "label": label, "text": cmd},
                "style": "secondary",
                "color": theme['card'],
                "height": "sm",
                "flex": 1
            })
        game_buttons.append(row)
    
    status_color = theme['primary'] if is_registered else theme['text2']
    status_text = "مسجل" if is_registered else "غير مسجل"
    
    return {
        "type": "bubble",
        "size": "mega",
        "styles": {"body": {"backgroundColor": theme['bg']}},
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "Bot Mesh",
                    "weight": "bold",
                    "size": "xxl",
                    "color": theme['primary'],
                    "align": "center"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {"type": "text", "text": name, "size": "sm", "color": theme['text'], "flex": 2},
                        {"type": "text", "text": status_text, "size": "sm", "color": status_color, "align": "end", "weight": "bold", "flex": 1}
                    ],
                    "margin": "md"
                },
                {
                    "type": "separator",
                    "margin": "lg"
                },
                {
                    "type": "text",
                    "text": "اختر لعبتك",
                    "size": "lg",
                    "color": theme['text'],
                    "weight": "bold",
                    "align": "center",
                    "margin": "lg"
                }
            ] + game_buttons + [
                {
                    "type": "separator",
                    "margin": "lg"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {"type": "button", "action": {"type": "message", "label": "نقاطي", "text": "نقاطي"}, "style": "primary", "color": theme['primary'], "height": "sm"},
                        {"type": "button", "action": {"type": "message", "label": "صدارة", "text": "صدارة"}, "style": "primary", "color": theme['primary'], "height": "sm"}
                    ],
                    "spacing": "sm",
                    "margin": "md"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {"type": "button", "action": {"type": "message", "label": "ثيم", "text": "ثيم"}, "style": "secondary", "color": theme['card'], "height": "sm"},
                        {"type": "button", "action": {"type": "message", "label": "انسحب", "text": "انسحب"}, "style": "secondary", "color": "#F59E0B", "height": "sm"},
                        {"type": "button", "action": {"type": "message", "label": "إيقاف", "text": "إيقاف"}, "style": "secondary", "color": "#EF4444", "height": "sm"}
                    ],
                    "spacing": "sm",
                    "margin": "sm"
                }
            ],
            "paddingAll": "20px"
        }
    }

def create_theme_menu(uid):
    """قائمة الثيمات - 9 ثيمات"""
    current_theme = get_theme(uid)
    theme = THEMES.get(current_theme, THEMES['white'])
    
    theme_buttons = []
    theme_list = list(THEMES.keys())
    for i in range(0, 9, 3):
        row = {
            "type": "box",
            "layout": "horizontal",
            "contents": [],
            "spacing": "sm",
            "margin": "sm"
        }
        for key in theme_list[i:i+3]:
            t = THEMES[key]
            is_current = key == current_theme
            row["contents"].append({
                "type": "button",
                "action": {"type": "message", "label": f"{t['name']}", "text": f"ثيم:{key}"},
                "style": "primary" if is_current else "secondary",
                "color": t['primary'] if is_current else theme['card'],
                "height": "sm",
                "flex": 1
            })
        theme_buttons.append(row)
    
    return {
        "type": "bubble",
        "styles": {"body": {"backgroundColor": theme['bg']}},
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": "اختر الثيم", "weight": "bold", "size": "xl", "color": theme['primary'], "align": "center"},
                {"type": "text", "text": f"الحالي: {theme['name']}", "size": "sm", "color": theme['text2'], "align": "center", "margin": "sm"},
                {"type": "separator", "margin": "lg"}
            ] + theme_buttons + [
                {"type": "separator", "margin": "lg"},
                {"type": "button", "action": {"type": "message", "label": "رجوع", "text": "مساعدة"}, "style": "secondary", "margin": "md"}
            ],
            "paddingAll": "20px"
        }
    }

def create_stats_flex(uid):
    """إحصائيات احترافية ثري دي"""
    theme = THEMES.get(get_theme(uid), THEMES['white'])
    user = db.get_user(uid)
    
    if not user:
        db.add_or_update_user(uid, get_name(uid), False)
        user = db.get_user(uid)
    
    is_registered = user['registered']
    win_rate = (user['wins'] / user['games'] * 100) if user['games'] > 0 else 0
    status_text = "مسجل" if is_registered else "غير مسجل"
    status_color = theme['primary'] if is_registered else "#EF4444"
    
    return {
        "type": "bubble",
        "size": "mega",
        "styles": {"body": {"backgroundColor": theme['bg']}},
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": "إحصائياتك", "weight": "bold", "size": "xxl", "color": theme['primary'], "align": "center"},
                {"type": "separator", "margin": "lg"},
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "box", "layout": "horizontal", "contents": [
                            {"type": "text", "text": "الاسم", "size": "md", "color": theme['text2'], "flex": 2},
                            {"type": "text", "text": user['name'], "size": "md", "color": theme['text'], "weight": "bold", "align": "end", "flex": 3}
                        ], "margin": "lg"},
                        {"type": "separator", "margin": "md"},
                        {"type": "box", "layout": "horizontal", "contents": [
                            {"type": "text", "text": "الحالة", "size": "md", "color": theme['text2'], "flex": 2},
                            {"type": "text", "text": status_text, "size": "md", "color": status_color, "weight": "bold", "align": "end", "flex": 3}
                        ], "margin": "md"},
                        {"type": "separator", "margin": "md"},
                        {"type": "box", "layout": "horizontal", "contents": [
                            {"type": "text", "text": "النقاط", "size": "md", "color": theme['text2'], "flex": 2},
                            {"type": "text", "text": str(user['points']), "size": "xl", "color": theme['primary'], "weight": "bold", "align": "end", "flex": 3}
                        ], "margin": "md"},
                        {"type": "separator", "margin": "md"},
                        {"type": "box", "layout": "horizontal", "contents": [
                            {"type": "text", "text": "الألعاب", "size": "md", "color": theme['text2'], "flex": 2},
                            {"type": "text", "text": str(user['games']), "size": "md", "color": theme['text'], "weight": "bold", "align": "end", "flex": 3}
                        ], "margin": "md"},
                        {"type": "separator", "margin": "md"},
                        {"type": "box", "layout": "horizontal", "contents": [
                            {"type": "text", "text": "الفوز", "size": "md", "color": theme['text2'], "flex": 2},
                            {"type": "text", "text": str(user['wins']), "size": "md", "color": theme['text'], "weight": "bold", "align": "end", "flex": 3}
                        ], "margin": "md"},
                        {"type": "separator", "margin": "md"},
                        {"type": "box", "layout": "horizontal", "contents": [
                            {"type": "text", "text": "نسبة الفوز", "size": "md", "color": theme['text2'], "flex": 2},
                            {"type": "text", "text": f"{win_rate:.1f}%", "size": "md", "color": theme['primary'], "weight": "bold", "align": "end", "flex": 3}
                        ], "margin": "md"}
                    ],
                    "backgroundColor": theme['card'],
                    "cornerRadius": "20px",
                    "paddingAll": "20px",
                    "margin": "lg"
                },
                {"type": "button", "action": {"type": "message", "label": "رجوع", "text": "مساعدة"}, "style": "secondary", "margin": "lg"}
            ],
            "paddingAll": "20px"
        }
    }

def create_leaderboard_flex(uid):
    """لوحة الصدارة"""
    theme = THEMES.get(get_theme(uid), THEMES['white'])
    leaders = db.get_leaderboard(10)
    
    contents = [
        {"type": "text", "text": "لوحة الصدارة", "weight": "bold", "size": "xl", "color": theme['primary'], "align": "center"},
        {"type": "separator", "margin": "lg"}
    ]
    
    if leaders:
        medals = ["المركز الأول", "المركز الثاني", "المركز الثالث"]
        for i, leader in enumerate(leaders):
            medal = medals[i] if i < 3 else f"المركز {i+1}"
            contents.append({
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {"type": "text", "text": f"{medal}", "size": "xs", "color": theme['text2'], "flex": 2},
                    {"type": "text", "text": leader['name'], "size": "sm", "color": theme['text'], "flex": 3},
                    {"type": "text", "text": str(leader['points']), "size": "sm", "color": theme['primary'], "weight": "bold", "align": "end", "flex": 1}
                ],
                "margin": "md"
            })
    else:
        contents.append({"type": "text", "text": "لا يوجد لاعبون مسجلون", "size": "md", "color": theme['text2'], "align": "center", "margin": "lg"})
    
    contents.append({"type": "button", "action": {"type": "message", "label": "رجوع", "text": "مساعدة"}, "style": "secondary", "margin": "lg"})
    
    return {
        "type": "bubble",
        "styles": {"body": {"backgroundColor": theme['bg']}},
        "body": {"type": "box", "layout": "vertical", "contents": contents, "paddingAll": "20px"}
    }

# ==================== Routes ====================
@app.route('/')
def home():
    return jsonify({'name': 'Bot Mesh Silent', 'status': 'active', 'version': '4.0.0'})

@app.route('/callback', methods=['POST'])
def callback():
    signature = request.headers.get('X-Line-Signature')
    if not signature:
        abort(400)
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# ==================== Event Handlers ====================
@handler.add(FollowEvent)
def on_follow(event):
    uid = event.source.user_id
    name = get_name(uid)
    db.add_or_update_user(uid, name, False)
    send_flex(event.reply_token, create_main_menu(uid), 'مرحباً')

@handler.add(MessageEvent, message=TextMessageContent)
def on_message(event):
    uid = event.source.user_id
    txt = event.message.text.strip()
    gid = getattr(event.source, 'group_id', uid)
    name = get_name(uid)
    
    # تحديث/إضافة المستخدم في قاعدة البيانات
    if not db.get_user(uid):
        db.add_or_update_user(uid, name, False)
    
    is_registered = db.is_registered(uid)
    
    # التحقق من المنشن (Mention)
    if hasattr(event.message, 'mention') and event.message.mention:
        send_flex(event.reply_token, create_main_menu(uid), 'القائمة')
        return
    
    # الأوامر المتاحة للجميع
    if txt.lower() in ['بداية', 'start', 'مساعدة', 'help']:
        send_flex(event.reply_token, create_main_menu(uid), 'القائمة')
        return
    
    if txt.lower() in ['انضم', 'join']:
        db.register_user(uid)
        send_text(event.reply_token, 'تم التسجيل بنجاح')
        logger.info(f'User registered: {name}')
        return
    
    if txt == 'ثيم':
        send_flex(event.reply_token, create_theme_menu(uid), 'الثيمات')
        return
    
    if txt.startswith('ثيم:'):
        theme_key = txt.split(':')[1]
        if theme_key in THEMES:
            db.update_theme(uid, theme_key)
            send_text(event.reply_token, f"تم تغيير الثيم إلى {THEMES[theme_key]['name']}")
        return
    
    if txt.lower() in ['نقاطي', 'stats']:
        send_flex(event.reply_token, create_stats_flex(uid), 'إحصائياتك')
        return
    
    if txt.lower() in ['صدارة', 'leaderboard']:
        send_flex(event.reply_token, create_leaderboard_flex(uid), 'الصدارة')
        return
    
    # أمر الانسحاب
    if txt.lower() in ['انسحب', 'leave']:
        db.unregister_user(uid)
        send_text(event.reply_token, 'تم الانسحاب')
        logger.info(f'User unregistered: {name}')
        return
    
    # من هنا فصاعداً: فقط المسجلون
    if not is_registered:
        return  # صامت تماماً - لا يرد
    
    # إيقاف اللعبة
    if txt.lower() in ['إيقاف', 'stop']:
        if gm.get_game(gid):
            gm.end_game(gid)
            send_text(event.reply_token, 'تم إيقاف اللعبة')
        else:
            send_text(event.reply_token, 'لا توجد لعبة نشطة')
        return
    
    # بدء لعبة (سيتم إضافة منطق الألعاب هنا)
    # TODO: Add game logic here

# ==================== Run ====================
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    logger.info(f"Bot Mesh Silent v4.0 - Running on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
