"""
Bot Mesh - Enhanced Silent Bot (Complete with Games)
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

# استيراد UI Builder
from ui_builder import UIBuilder

# ==================== Configuration ====================
LINE_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', '')
LINE_SECRET = os.getenv('LINE_CHANNEL_SECRET', '')
DB_PATH = os.getenv('DB_PATH', 'data/game.db')

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
        self.answered_users = {}

    def start_game(self, gid, game, game_type):
        self.active_games[gid] = {"game": game, "type": game_type}
        self.answered_users[gid] = set()

    def get_game(self, gid):
        return self.active_games.get(gid)

    def end_game(self, gid):
        self.active_games.pop(gid, None)
        self.answered_users.pop(gid, None)

    def has_answered(self, gid, uid):
        return uid in self.answered_users.get(gid, set())

    def mark_answered(self, gid, uid):
        if gid in self.answered_users:
            self.answered_users[gid].add(uid)

# ==================== Flask & LINE ====================
app = Flask(__name__)
configuration = Configuration(access_token=LINE_TOKEN)
handler = WebhookHandler(LINE_SECRET)
db = Database(DB_PATH)
gm = GameManager()

# استيراد الألعاب
try:
    from games import (IqGame, WordColorGame, ScrambleWordGame, MathGame,
                      FastTypingGame, OppositeGame, LettersWordsGame, SongGame,
                      HumanAnimalPlantGame, ChainWordsGame, GuessGame, CompatibilityGame)
    
    GAMES = {
        'ذكاء': IqGame, 'لون': WordColorGame, 'ترتيب': ScrambleWordGame,
        'رياضيات': MathGame, 'أسرع': FastTypingGame, 'ضد': OppositeGame,
        'تكوين': LettersWordsGame, 'أغنية': SongGame, 'لعبة': HumanAnimalPlantGame,
        'سلسلة': ChainWordsGame, 'خمن': GuessGame, 'توافق': CompatibilityGame
    }
    logger.info(f"Loaded {len(GAMES)} games successfully")
except Exception as e:
    logger.error(f"Failed to load games: {e}")
    GAMES = {}

# ==================== Helper Functions ====================
def get_name(uid):
    try:
        with ApiClient(configuration) as api_client:
            return MessagingApi(api_client).get_profile(uid).display_name
    except:
        return 'لاعب'

def get_theme(uid):
    user = db.get_user(uid)
    return user.get('theme', 'white') if user else 'white'

def create_game_buttons():
    """أزرار الألعاب الثابتة"""
    items = []
    for game_name in GAMES.keys():
        items.append(QuickReplyItem(action=MessageAction(label=game_name, text=game_name)))
    items.append(QuickReplyItem(action=MessageAction(label="إيقاف", text="إيقاف")))
    return QuickReply(items=items)

def send_flex_with_buttons(reply_token, content, alt='رسالة'):
    """إرسال Flex مع أزرار الألعاب"""
    try:
        with ApiClient(configuration) as api_client:
            line_api = MessagingApi(api_client)
            messages = [
                FlexMessage(altText=alt, contents=FlexContainer.from_dict(content)),
                TextMessage(text="اختر لعبة", quickReply=create_game_buttons())
            ]
            line_api.reply_message(ReplyMessageRequest(replyToken=reply_token, messages=messages))
            return True
    except Exception as e:
        logger.error(f'Error: {e}')
    return False

def send_text_with_buttons(reply_token, text):
    """إرسال نص مع أزرار الألعاب"""
    try:
        with ApiClient(configuration) as api_client:
            line_api = MessagingApi(api_client)
            line_api.reply_message(ReplyMessageRequest(
                replyToken=reply_token,
                messages=[TextMessage(text=text, quickReply=create_game_buttons())]
            ))
            return True
    except Exception as e:
        logger.error(f'Error: {e}')
    return False

def send_text(reply_token, text):
    """إرسال نص بدون أزرار"""
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

# ==================== Routes ====================
@app.route('/')
def home():
    return jsonify({'name': 'Bot Mesh Silent', 'status': 'active', 'version': '4.1', 'games': len(GAMES)})

@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'games': len(gm.active_games), 'db': 'connected'})

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
    colors = THEMES[get_theme(uid)]
    db.add_or_update_user(uid, name, False)
    is_registered = db.is_registered(uid)
    send_flex_with_buttons(event.reply_token, 
        UIBuilder.create_welcome_flex(uid, colors, name, is_registered), 'مرحباً')
    logger.info(f'New user: {name}')

@handler.add(MessageEvent, message=TextMessageContent)
def on_message(event):
    uid = event.source.user_id
    txt = event.message.text.strip()
    gid = getattr(event.source, 'group_id', uid)
    name = get_name(uid)
    
    # إضافة/تحديث المستخدم
    if not db.get_user(uid):
        db.add_or_update_user(uid, name, False)
    
    is_registered = db.is_registered(uid)
    
    # المنشن
    if '@Bot Mesh' in txt or '@bot' in txt.lower():
        colors = THEMES[get_theme(uid)]
        send_flex_with_buttons(event.reply_token, 
            UIBuilder.create_welcome_flex(uid, colors, name, is_registered), 'القائمة')
        return
    
    # أوامر متاحة للجميع
    if txt.lower() in ['بداية', 'start', 'مساعدة', 'help', 'الالعاب']:
        colors = THEMES[get_theme(uid)]
        send_flex_with_buttons(event.reply_token, 
            UIBuilder.create_games_menu_flex(uid, colors), 'القائمة')
        return
    
    if txt.lower() in ['انضم', 'join']:
        db.register_user(uid)
        send_text_with_buttons(event.reply_token, '✅ تم التسجيل بنجاح!\nالآن يمكنك اللعب')
        logger.info(f'User registered: {name}')
        return
    
    if txt == 'ثيم':
        colors = THEMES[get_theme(uid)]
        send_flex_with_buttons(event.reply_token, 
            UIBuilder.create_theme_menu_flex(uid, colors, get_theme(uid)), 'الثيمات')
        return
    
    if txt.startswith('ثيم:'):
        theme_key = txt.split(':')[1]
        if theme_key in THEMES:
            db.update_theme(uid, theme_key)
            send_text_with_buttons(event.reply_token, f"✅ تم التغيير إلى {THEMES[theme_key]['name']}")
        return
    
    if txt.lower() in ['نقاطي', 'stats', 'إحصائيات']:
        user = db.get_user(uid)
        if not user:
            send_text_with_buttons(event.reply_token, "لم تلعب أي ألعاب بعد!")
            return
        colors = THEMES[get_theme(uid)]
        send_flex_with_buttons(event.reply_token, 
            UIBuilder.create_stats_flex(uid, colors, user), 'إحصائياتك')
        return
    
    if txt.lower() in ['صدارة', 'leaderboard']:
        colors = THEMES[get_theme(uid)]
        leaders = db.get_leaderboard(10)
        send_flex_with_buttons(event.reply_token, 
            UIBuilder.create_leaderboard_flex(uid, colors, leaders), 'الصدارة')
        return
    
    if txt.lower() in ['انسحب', 'leave']:
        db.unregister_user(uid)
        send_text(event.reply_token, '🚪 تم الانسحاب')
        logger.info(f'User unregistered: {name}')
        return
    
    # من هنا: فقط المسجلون
    if not is_registered:
        return  # صامت تماماً
    
    # إيقاف
    if txt.lower() in ['إيقاف', 'stop']:
        if gm.get_game(gid):
            gm.end_game(gid)
            send_text_with_buttons(event.reply_token, '✅ تم إيقاف اللعبة')
        else:
            send_text_with_buttons(event.reply_token, 'لا توجد لعبة نشطة')
        return
    
    # بدء لعبة
    if txt in GAMES:
        if gm.get_game(gid):
            send_text_with_buttons(event.reply_token, '⚠️ يوجد لعبة نشطة\nاكتب "إيقاف" لإنهائها')
            return
        
        try:
            with ApiClient(configuration) as api_client:
                line_api = MessagingApi(api_client)
                game = GAMES[txt](line_api)
                game.set_theme(get_theme(uid))
                gm.start_game(gid, game, txt)
                response = game.start_game()
                
                if hasattr(response, 'altText'):
                    messages = [response, TextMessage(text="اختر لعبة", quickReply=create_game_buttons())]
                    line_api.reply_message(ReplyMessageRequest(replyToken=event.reply_token, messages=messages))
                else:
                    send_flex_with_buttons(event.reply_token, response, txt)
                
                logger.info(f'Game started: {txt} by {name}')
        except Exception as e:
            logger.error(f'Error starting game: {e}')
            send_text_with_buttons(event.reply_token, '❌ حدث خطأ')
        return
    
    # الرد على اللعبة
    game_data = gm.get_game(gid)
    if game_data:
        game = game_data['game']
        
        if gm.has_answered(gid, uid):
            return  # صامت
        
        try:
            result = game.check_answer(txt, uid, name)
            if result:
                gm.mark_answered(gid, uid)
                points = result.get('points', 0)
                won = result.get('won', False)
                db.update_points(uid, points, won)
                response = result.get('response')
                
                if response:
                    if hasattr(response, 'altText'):
                        with ApiClient(configuration) as api_client:
                            line_api = MessagingApi(api_client)
                            messages = [response, TextMessage(text="اختر لعبة", quickReply=create_game_buttons())]
                            line_api.reply_message(ReplyMessageRequest(replyToken=event.reply_token, messages=messages))
                    else:
                        send_flex_with_buttons(event.reply_token, response, 'نتيجة')
                
                if result.get('game_over'):
                    gm.end_game(gid)
        except Exception as e:
            logger.error(f'Error: {e}')

# ==================== Run ====================
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    logger.info(f"🚀 Bot Mesh Silent v4.1 - Port {port}")
    logger.info(f"📊 Loaded {len(GAMES)} games")
    app.run(host='0.0.0.0', port=port, debug=False)
