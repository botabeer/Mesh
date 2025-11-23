"""
Bot Mesh - Main Application (Enhanced Version)
Created by: Abeer Aldosari © 2025
"""
import os
import logging
from flask import Flask, request, abort, jsonify
from linebot import LineBotApi
from linebot.v3.webhook import WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage

# استيراد المكونات
from config import LINE_TOKEN, LINE_SECRET, DB_PATH, THEMES
from database import DB
from flex_builder import FlexBuilder
from game_manager import GameManager

# استيراد جميع الألعاب
from games import *

# ==================== الإعدادات ====================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ==================== Flask App ====================
app = Flask(__name__)
line_api = LineBotApi(LINE_TOKEN)
handler = WebhookHandler(LINE_SECRET)
db = DB(DB_PATH)
gm = GameManager()

# ==================== قاموس الألعاب ====================
GAMES = {
    'ذكاء': IqGame,
    'لون': WordColorGame,
    'ترتيب': ScrambleWordGame,
    'رياضيات': MathGame,
    'أسرع': FastTypingGame,
    'ضد': OppositeGame,
    'تكوين': LettersWordsGame,
    'أغنية': SongGame,
    'لعبة': HumanAnimalPlantGame,
    'سلسلة': ChainWordsGame,
    'خمن': GuessGame,
    'توافق': CompatibilityGame
}

# ==================== Helper Functions ====================
def get_name(uid):
    try:
        return line_api.get_profile(uid).display_name
    except:
        return 'لاعب'

def get_theme(uid):
    user = db.get_user(uid)
    return user['theme'] if user else 'white'

def send_flex(reply_token, flex_content, uid=None):
    """إرسال نافذة فلكس مع قائمة الألعاب"""
    theme = get_theme(uid)
    builder = FlexBuilder(theme)
    flex_msg = FlexSendMessage(alt_text="Bot Mesh", contents=flex_content)
    text_msg = TextSendMessage(text="اختر لعبة:", quick_reply=builder.get_games_quick_reply())
    line_api.reply_message(reply_token, [flex_msg, text_msg])

# ==================== Routes ====================
@app.route('/')
def home():
    return "Bot Mesh - Active"

@app.route('/health')
def health():
    return jsonify({
        'status': 'ok',
        'users': gm.get_users_count(),
        'active_games': gm.get_active_games_count(),
        'total_games': len(GAMES),
        'themes': len(THEMES)
    })

@app.route('/callback', methods=['POST'])
def callback():
    signature = request.headers.get('X-Line-Signature')
    if not signature:
        abort(400)
    try:
        handler.handle(request.get_data(as_text=True), signature)
    except InvalidSignatureError:
        logger.error("Invalid signature")
        abort(400)
    return 'OK'

# ==================== Event Handlers ====================
@handler.add(MessageEvent, message=TextMessage)
def on_message(event):
    uid = event.source.user_id
    txt = event.message.text.strip()
    gid = getattr(event.source, 'group_id', uid)
    name = get_name(uid)

    # تسجيل المستخدم إذا كتب "انضم"
    if txt == "انضم":
        gm.register(uid)
        send_flex(event.reply_token, FlexBuilder(get_theme(uid)).welcome(), uid)
        return

    # انسحب
    if txt == "انسحب":
        gm.unregister(uid)
        line_api.reply_message(event.reply_token, TextSendMessage(text="تم الانسحاب، لن تُحسب إجاباتك"))
        return

    # إيقاف اللعبة
    if txt == "إيقاف":
        if gm.get_game(gid):
            gm.end_game(gid)
            line_api.reply_message(event.reply_token, TextSendMessage(text="⏹️ تم إيقاف اللعبة"))
        else:
            line_api.reply_message(event.reply_token, TextSendMessage(text="⚠️ لا توجد لعبة نشطة"))
        return

    # بدء لعبة جديدة
    if txt in GAMES:
        if not gm.is_registered(uid):
            line_api.reply_message(event.reply_token, TextSendMessage(text="❌ اكتب 'انضم' أولاً للتسجيل"))
            return
        if gm.get_game(gid):
            line_api.reply_message(event.reply_token, TextSendMessage(text="⚠️ لعبة نشطة بالفعل"))
            return
        game_class = GAMES[txt]
        game = game_class(line_api)
        game.set_theme(get_theme(uid))
        gm.start_game(gid, game, txt)
        response = game.start_game()
        send_flex(event.reply_token, response, uid)
        return

    # التعامل مع إجابات اللعبة (صامت للمستخدمين غير المسجلين)
    game_data = gm.get_game(gid)
    if game_data and gm.is_registered(uid) and not gm.has_answered(gid, uid):
        game = game_data['game']
        result = game.check_answer(txt, uid, name)
        if result and result.get("game_over"):
            points = result.get("points", 0)
            won = result.get("won", False)
            db.update(uid, name, points, won, game_data['type'])
            gm.end_game(gid)
        response = result.get("response") if result else None
        if response:
            send_flex(event.reply_token, response, uid)
        return

@handler.add(FollowEvent)
def on_follow(event):
    uid = event.source.user_id
    gm.register(uid)
    send_flex(event.reply_token, FlexBuilder(get_theme(uid)).welcome(), uid)

# ==================== Run ====================
if __name__ == "__main__":
    logger.info("Bot Mesh Started")
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
