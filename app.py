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
    ReplyMessageRequest, TextMessage, FlexMessage, FlexContainer,
    QuickReply, QuickReplyItem, MessageAction
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent, FollowEvent

# استيراد الألعاب من مجلد games
from games import *

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

# قائمة الألعاب المتاحة
GAMES = {
    'حساب': {'class': MathGame, 'name': 'حساب', 'emoji': '🧮', 'desc': 'حل المسائل الرياضية'},
    'كلمات': {'class': ScrambleWordGame, 'name': 'ترتيب الحروف', 'emoji': '🔤', 'desc': 'رتب الحروف لتكوين كلمة'},
    'تخمين': {'class': GuessGame, 'name': 'تخمين الكلمة', 'emoji': '🔮', 'desc': 'خمن الكلمة من الفئة'},
    'أسرع': {'class': FastTypingGame, 'name': 'كتابة سريعة', 'emoji': '⚡', 'desc': 'اكتب الجملة بسرعة'},
    'ذكاء': {'class': IqGame, 'name': 'أسئلة ذكاء', 'emoji': '🧠', 'desc': 'أسئلة ذكاء وألغاز'},
    'ألوان': {'class': WordColorGame, 'name': 'كلمة ولون', 'emoji': '🎨', 'desc': 'حدد لون الدائرة'},
    'سلسلة': {'class': ChainWordsGame, 'name': 'سلسلة كلمات', 'emoji': '🔗', 'desc': 'كون سلسلة من الكلمات'},
    'أغنية': {'class': SongGame, 'name': 'تخمين الأغنية', 'emoji': '🎵', 'desc': 'خمن المغني'},
    'ضد': {'class': OppositeGame, 'name': 'ضد الكلمة', 'emoji': '↔️', 'desc': 'اكتب عكس الكلمة'},
    'حروف': {'class': LettersWordsGame, 'name': 'تكوين كلمات', 'emoji': '📝', 'desc': 'كون كلمات من الحروف'},
    'لعبه': {'class': HumanAnimalPlantGame, 'name': 'إنسان حيوان نبات', 'emoji': '🌍', 'desc': 'إنسان حيوان نبات جماد بلاد'},
    'توافق': {'class': CompatibilityGame, 'name': 'التوافق', 'emoji': '💕', 'desc': 'احسب نسبة التوافق'}
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

# ==================== Helper Functions ====================
def get_quick_reply(is_registered=False):
    """إنشاء أزرار ثابتة للرد السريع"""
    items = [
        QuickReplyItem(action=MessageAction(label="🏠 القائمة", text="بداية")),
        QuickReplyItem(action=MessageAction(label="🎮 الألعاب", text="الألعاب")),
        QuickReplyItem(action=MessageAction(label="📊 نقاطي", text="نقاطي")),
        QuickReplyItem(action=MessageAction(label="🏆 الصدارة", text="صدارة")),
    ]
    
    if is_registered:
        items.extend([
            QuickReplyItem(action=MessageAction(label="🎨 الثيمات", text="ثيم")),
            QuickReplyItem(action=MessageAction(label="⏹️ إيقاف", text="إيقاف")),
        ])
    else:
        items.append(QuickReplyItem(action=MessageAction(label="✅ انضم", text="انضم")))
    
    return QuickReply(items=items)

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

def send_flex(reply_token, content, alt='رسالة', uid=None):
    try:
        with ApiClient(configuration) as api_client:
            line_api = MessagingApi(api_client)
            is_registered = db.is_registered(uid) if uid else False
            line_api.reply_message(ReplyMessageRequest(
                replyToken=reply_token,
                messages=[FlexMessage(
                    altText=alt, 
                    contents=FlexContainer.from_dict(content),
                    quickReply=get_quick_reply(is_registered)
                )]
            ))
            return True
    except Exception as e:
        logger.error(f'Error: {e}')
    return False

def send_text(reply_token, text, uid=None):
    try:
        with ApiClient(configuration) as api_client:
            line_api = MessagingApi(api_client)
            is_registered = db.is_registered(uid) if uid else False
            line_api.reply_message(ReplyMessageRequest(
                replyToken=reply_token,
                messages=[TextMessage(text=text, quickReply=get_quick_reply(is_registered))]
            ))
            return True
    except Exception as e:
        logger.error(f'Error: {e}')
    return False

def create_main_menu(uid):
    theme = THEMES[get_theme(uid)]
    user = db.get_user(uid)
    is_registered = user and user['registered']
    
    return {
        "type": "bubble",
        "styles": {"body": {"backgroundColor": theme['bg']}},
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": "🎮 Bot Mesh", "weight": "bold", "size": "xxl", "color": theme['primary']},
                {"type": "text", "text": "Enhanced Silent Bot", "size": "sm", "color": theme['text2'], "margin": "md"},
                {"type": "separator", "margin": "xl"},
                {"type": "text", "text": "الحالة", "weight": "bold", "size": "lg", "color": theme['text'], "margin": "xl"},
                {"type": "text", "text": f"{'✅ مسجل' if is_registered else '❌ غير مسجل'}", "color": theme['text2'], "margin": "sm"},
                {"type": "separator", "margin": "xl"},
                {"type": "text", "text": "الأوامر المتاحة:", "weight": "bold", "color": theme['text'], "margin": "xl"},
                {"type": "text", "text": "• انضم - للتسجيل", "size": "sm", "color": theme['text2'], "margin": "md"},
                {"type": "text", "text": "• الألعاب - قائمة الألعاب", "size": "sm", "color": theme['text2']},
                {"type": "text", "text": "• نقاطي - الإحصائيات", "size": "sm", "color": theme['text2']},
                {"type": "text", "text": "• صدارة - لوحة الصدارة", "size": "sm", "color": theme['text2']},
                {"type": "text", "text": "• ثيم - تغيير الثيم", "size": "sm", "color": theme['text2']},
            ]
        }
    }

def create_games_menu(uid):
    theme = THEMES[get_theme(uid)]
    contents = [
        {"type": "text", "text": "🎮 قائمة الألعاب", "weight": "bold", "size": "xl", "color": theme['primary']},
        {"type": "separator", "margin": "xl"}
    ]
    
    for key, game in GAMES.items():
        contents.append({
            "type": "text",
            "text": f"{game['emoji']} {game['name']} - {key}",
            "size": "sm",
            "color": theme['text2'],
            "margin": "md"
        })
        contents.append({
            "type": "text",
            "text": f"   {game['desc']}",
            "size": "xs",
            "color": theme['text2'],
            "margin": "xs"
        })
    
    return {
        "type": "bubble",
        "styles": {"body": {"backgroundColor": theme['bg']}},
        "body": {"type": "box", "layout": "vertical", "contents": contents}
    }

def create_theme_menu(uid):
    theme = THEMES[get_theme(uid)]
    contents = [
        {"type": "text", "text": "🎨 اختر الثيم", "weight": "bold", "size": "xl", "color": theme['primary']},
        {"type": "separator", "margin": "xl"}
    ]
    
    for key, t in THEMES.items():
        contents.append({
            "type": "text",
            "text": f"• {t['name']} - ثيم:{key}",
            "size": "sm",
            "color": theme['text2'],
            "margin": "md"
        })
    
    return {
        "type": "bubble",
        "styles": {"body": {"backgroundColor": theme['bg']}},
        "body": {"type": "box", "layout": "vertical", "contents": contents}
    }

def create_stats_flex(uid):
    theme = THEMES[get_theme(uid)]
    user = db.get_user(uid)
    
    if not user:
        return create_main_menu(uid)
    
    win_rate = (user['wins'] / user['games'] * 100) if user['games'] > 0 else 0
    
    return {
        "type": "bubble",
        "styles": {"body": {"backgroundColor": theme['bg']}},
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": "📊 إحصائياتك", "weight": "bold", "size": "xl", "color": theme['primary']},
                {"type": "separator", "margin": "xl"},
                {"type": "box", "layout": "baseline", "margin": "xl", "contents": [
                    {"type": "text", "text": "الاسم:", "size": "sm", "color": theme['text'], "flex": 0},
                    {"type": "text", "text": user['name'], "size": "sm", "color": theme['text2'], "align": "end"}
                ]},
                {"type": "box", "layout": "baseline", "margin": "md", "contents": [
                    {"type": "text", "text": "النقاط:", "size": "sm", "color": theme['text'], "flex": 0},
                    {"type": "text", "text": str(user['points']), "size": "sm", "color": theme['primary'], "align": "end", "weight": "bold"}
                ]},
                {"type": "box", "layout": "baseline", "margin": "md", "contents": [
                    {"type": "text", "text": "الألعاب:", "size": "sm", "color": theme['text'], "flex": 0},
                    {"type": "text", "text": str(user['games']), "size": "sm", "color": theme['text2'], "align": "end"}
                ]},
                {"type": "box", "layout": "baseline", "margin": "md", "contents": [
                    {"type": "text", "text": "الفوز:", "size": "sm", "color": theme['text'], "flex": 0},
                    {"type": "text", "text": str(user['wins']), "size": "sm", "color": theme['text2'], "align": "end"}
                ]},
                {"type": "box", "layout": "baseline", "margin": "md", "contents": [
                    {"type": "text", "text": "نسبة الفوز:", "size": "sm", "color": theme['text'], "flex": 0},
                    {"type": "text", "text": f"{win_rate:.1f}%", "size": "sm", "color": theme['primary'], "align": "end", "weight": "bold"}
                ]},
            ]
        }
    }

def create_leaderboard_flex(uid):
    theme = THEMES[get_theme(uid)]
    leaders = db.get_leaderboard(10)
    
    contents = [
        {"type": "text", "text": "🏆 لوحة الصدارة", "weight": "bold", "size": "xl", "color": theme['primary']},
        {"type": "separator", "margin": "xl"}
    ]
    
    medals = ['🥇', '🥈', '🥉']
    for i, leader in enumerate(leaders):
        medal = medals[i] if i < 3 else f"{i+1}."
        contents.append({
            "type": "box",
            "layout": "baseline",
            "margin": "md",
            "contents": [
                {"type": "text", "text": medal, "size": "sm", "flex": 0, "color": theme['text']},
                {"type": "text", "text": leader['name'], "size": "sm", "color": theme['text'], "margin": "sm"},
                {"type": "text", "text": f"{leader['points']} نقطة", "size": "sm", "color": theme['primary'], "align": "end", "weight": "bold"}
            ]
        })
    
    if not leaders:
        contents.append({"type": "text", "text": "لا يوجد لاعبون بعد", "size": "sm", "color": theme['text2'], "margin": "md"})
    
    return {
        "type": "bubble",
        "styles": {"body": {"backgroundColor": theme['bg']}},
        "body": {"type": "box", "layout": "vertical", "contents": contents}
    }

# ==================== Routes ====================
@app.route('/')
def home():
    return jsonify({
        'name': 'Bot Mesh Silent',
        'status': 'active',
        'version': '4.0.0',
        'games': len(GAMES)
    })

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
    send_flex(event.reply_token, create_main_menu(uid), 'مرحباً', uid)

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
    
    # الأوامر المتاحة للجميع
    if txt.lower() in ['بداية', 'start', 'مساعدة', 'help']:
        send_flex(event.reply_token, create_main_menu(uid), 'القائمة', uid)
        return
    
    if txt.lower() in ['الألعاب', 'games']:
        send_flex(event.reply_token, create_games_menu(uid), 'الألعاب', uid)
        return
    
    if txt.lower() in ['انضم', 'join']:
        db.register_user(uid)
        send_text(event.reply_token, '✅ تم التسجيل بنجاح! يمكنك الآن لعب الألعاب', uid)
        logger.info(f'User registered: {name}')
        return
    
    if txt == 'ثيم':
        send_flex(event.reply_token, create_theme_menu(uid), 'الثيمات', uid)
        return
    
    if txt.startswith('ثيم:'):
        theme_key = txt.split(':')[1]
        if theme_key in THEMES:
            db.update_theme(uid, theme_key)
            send_text(event.reply_token, f"✨ تم تغيير الثيم إلى {THEMES[theme_key]['name']}", uid)
        return
    
    if txt.lower() in ['نقاطي', 'stats']:
        send_flex(event.reply_token, create_stats_flex(uid), 'إحصائياتك', uid)
        return
    
    if txt.lower() in ['صدارة', 'leaderboard']:
        send_flex(event.reply_token, create_leaderboard_flex(uid), 'الصدارة', uid)
        return
    
    # أمر الانسحاب
    if txt.lower() in ['انسحب', 'leave']:
        db.unregister_user(uid)
        send_text(event.reply_token, '👋 تم الانسحاب بنجاح', uid)
        logger.info(f'User unregistered: {name}')
        return
    
    # من هنا فصاعداً: فقط المسجلون
    if not is_registered:
        return  # صامت تماماً - لا يرد
    
    # إيقاف اللعبة
    if txt.lower() in ['إيقاف', 'stop']:
        if gm.get_game(gid):
            gm.end_game(gid)
            send_text(event.reply_token, '⏹️ تم إيقاف اللعبة', uid)
        else:
            send_text(event.reply_token, '❌ لا توجد لعبة نشطة', uid)
        return
    
    # بدء الألعاب
    if txt in GAMES:
        try:
            with ApiClient(configuration) as api_client:
                line_api = MessagingApi(api_client)
                game_class = GAMES[txt]['class']
                game = game_class(line_api)
                
                # تطبيق ثيم المستخدم
                user_theme = get_theme(uid)
                game.set_theme(user_theme)
                
                gm.start_game(gid, game, txt)
                response = game.start_game()
                
                # إرسال الرد
                line_api.reply_message(ReplyMessageRequest(
                    replyToken=event.reply_token,
                    messages=[response]
                ))
        except Exception as e:
            logger.error(f'Error starting game: {e}')
            send_text(event.reply_token, f'❌ خطأ في بدء اللعبة: {str(e)}', uid)
        return
    
    # معالجة إجابات الألعاب
    active_game = gm.get_game(gid)
    if active_game:
        game = active_game['game']
        game_type = active_game['type']
        
        try:
            result = game.check_answer(txt, uid, name)
            
            if result:
                points = result.get('points', 0)
                won = result.get('won', False)
                game_over = result.get('game_over', False)
                
                # تحديث النقاط
                if points > 0:
                    db.update_points(uid, points, won)
                
                # إنهاء اللعبة إذا انتهت
                if game_over:
                    gm.end_game(gid)
                
                # إرسال الرد
                with ApiClient(configuration) as api_client:
                    line_api = MessagingApi(api_client)
                    response_msg = result.get('response')
                    if response_msg:
                        line_api.reply_message(ReplyMessageRequest(
                            replyToken=event.reply_token,
                            messages=[response_msg]
                        ))
        except Exception as e:
            logger.error(f'Error in game answer: {e}')

# ==================== Run ====================
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    logger.info(f"Bot Mesh Silent v4.0 - Running on port {port}")
    logger.info(f"Loaded {len(GAMES)} games")
    app.run(host='0.0.0.0', port=port, debug=False)
