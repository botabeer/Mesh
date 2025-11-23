"""
Bot Mesh - Main Application (Silent, Smart, Flex UI, v3 SDK)
Created by: Abeer Aldosari © 2025
"""
import os
import logging
from flask import Flask, request, abort, jsonify

# === LINE SDK v3 ===
from linebot.v3.messaging import MessagingApi, MessagingWebhookHandler
from linebot.v3.messaging.models import (
    TextMessageEvent, TextMessage, TextSendMessage,
    FlexSendMessage, FollowEvent, QuickReply, QuickReplyButton,
    MessageAction
)

# استيراد المكونات
from config import LINE_TOKEN, LINE_SECRET, DB_PATH, THEMES
from database import DB
from flex_builder import FlexBuilder
from game_manager import GameManager

# استيراد جميع الألعاب تلقائيًا
from games import *

# ==================== Logging ====================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ==================== Flask & Line ====================
app = Flask(__name__)
line_api = MessagingApi(LINE_TOKEN)
handler = MessagingWebhookHandler(LINE_SECRET)
db = DB(DB_PATH)
gm = GameManager()

# ==================== قاموس الألعاب ====================
GAMES = {
    'ذكاء': IqGame,
    'لون': WordColorGame,
    'ترتيب': ScrambleWordGameAI,
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

# ==================== Helpers ====================
def get_name(uid):
    try:
        return line_api.get_profile(uid).display_name
    except:
        return 'لاعب'

def get_theme(uid):
    user = db.get_user(uid)
    return user.get('theme', 'white') if user else 'white'

def get_games_quick_reply(uid):
    items = []
    for label in GAMES.keys():
        items.append(QuickReplyButton(
            action=MessageAction(label=label, text=label)
        ))
    items.append(QuickReplyButton(action=MessageAction(label='إيقاف', text='إيقاف')))
    items.append(QuickReplyButton(action=MessageAction(label='انضم', text='انضم')))
    items.append(QuickReplyButton(action=MessageAction(label='انسحب', text='انسحب')))
    return QuickReply(items=items)

def send_flex_reply(reply_token, flex_content, uid=None):
    text_msg = TextSendMessage(
        text="اختر لعبة أو أمر:",
        quick_reply=get_games_quick_reply(uid)
    )
    line_api.reply_message(reply_token, [FlexSendMessage(alt_text='القائمة', contents=flex_content), text_msg])

# ==================== Routes ====================
@app.route('/')
def home():
    return "Bot Mesh - Active"

@app.route('/health')
def health():
    return jsonify({
        'status': 'ok',
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
    except Exception as e:
        logger.error(f'❌ Invalid signature or error: {e}')
        abort(400)
    return 'OK'

# ==================== Event Handlers ====================
@handler.add(FollowEvent)
def on_follow(event):
    uid = event.source.user_id
    name = get_name(uid)
    db.add_or_update_user(uid, name)
    builder = FlexBuilder('white')
    send_flex_reply(event.reply_token, builder.welcome(), uid)

@handler.add(TextMessageEvent)
def on_message(event):
    uid = event.source.user_id
    txt = event.message.text.strip()
    gid = getattr(event.source, 'group_id', uid)
    name = get_name(uid)
    db.add_or_update_user(uid, name)
    builder = FlexBuilder(get_theme(uid))

    # انضم
    if txt == 'انضم':
        gm.register(uid)
        send_flex_reply(event.reply_token, builder.welcome(), uid)
        return

    # انسحب
    if txt == 'انسحب':
        gm.unregister(uid)
        line_api.reply_message(event.reply_token, TextSendMessage(text='تم الانسحاب، لن تُحسب إجاباتك'))
        return

    # إيقاف
    if txt == 'إيقاف':
        if gm.get_game(gid):
            gm.end_game(gid)
            line_api.reply_message(event.reply_token, TextSendMessage(text='تم إيقاف اللعبة'))
        else:
            line_api.reply_message(event.reply_token, TextSendMessage(text='لا توجد لعبة نشطة'))
        return

    # بدء لعبة
    if txt in GAMES:
        if not gm.is_registered(uid):
            line_api.reply_message(event.reply_token, TextSendMessage(text='❌ اكتب "انضم" أولاً للتسجيل'))
            return

        if gm.get_game(gid):
            line_api.reply_message(event.reply_token, TextSendMessage(text='⚠️ يوجد لعبة نشطة بالفعل'))
            return

        game_class = GAMES[txt]
        game = game_class(line_api)
        game.set_theme(get_theme(uid))
        gm.start_game(gid, game, txt)
        response = game.start_game()
        send_flex_reply(event.reply_token, response, uid)
        return

    # الرد على اللعبة (أول إجابة صحيحة فقط)
    game_data = gm.get_game(gid)
    if game_data and gm.is_registered(uid):
        game = game_data['game']
        if not gm.has_answered(gid, uid):
            result = game.check_answer(txt, uid, name)
            if result:
                gm.mark_answered(gid, uid)
                points = result.get('points', 0)
                won = result.get('won', False)
                db.update_points(uid, points, won)
                response = result.get('response')
                if response:
                    send_flex_reply(event.reply_token, response, uid)
        return

# ==================== Run ====================
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    logger.info("Bot Mesh - Running on port %s", port)
    app.run(host='0.0.0.0', port=port, debug=False)
