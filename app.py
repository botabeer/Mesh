"""
Bot Mesh - Main Application (Silent, Smart, Flex UI, v3 SDK)
Created by: Abeer Aldosari © 2025
"""
import os
import logging
from flask import Flask, request, abort, jsonify

# === LINE SDK v3 - Correct Imports ===
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
    FlexMessage,
    FlexContainer,
    QuickReply,
    QuickReplyItem,
    MessageAction
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
    FollowEvent
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

configuration = Configuration(access_token=LINE_TOKEN)
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

# ==================== Helpers ====================
def get_name(uid):
    try:
        with ApiClient(configuration) as api_client:
            line_api = MessagingApi(api_client)
            profile = line_api.get_profile(uid)
            return profile.display_name
    except Exception as e:
        logger.error(f'Error getting profile: {e}')
        return 'لاعب'

def get_theme(uid):
    user = db.get_user(uid)
    return user.get('theme', 'white') if user else 'white'

def get_games_quick_reply(uid):
    items = []
    for label in GAMES.keys():
        items.append(QuickReplyItem(
            action=MessageAction(label=label, text=label)
        ))
    items.append(QuickReplyItem(action=MessageAction(label='إيقاف', text='إيقاف')))
    items.append(QuickReplyItem(action=MessageAction(label='انضم', text='انضم')))
    items.append(QuickReplyItem(action=MessageAction(label='انسحب', text='انسحب')))
    return QuickReply(items=items)

def send_flex_reply(reply_token, flex_content, uid=None):
    """إرسال رسالة Flex مع Quick Reply باستخدام v3 API"""
    try:
        with ApiClient(configuration) as api_client:
            line_api = MessagingApi(api_client)
            
            text_msg = TextMessage(
                text="اختر لعبة أو أمر:",
                quickReply=get_games_quick_reply(uid)
            )
            
            flex_msg = FlexMessage(
                altText='القائمة',
                contents=FlexContainer.from_dict(flex_content)
            )
            
            line_api.reply_message(
                ReplyMessageRequest(
                    replyToken=reply_token,
                    messages=[flex_msg, text_msg]
                )
            )
    except Exception as e:
        logger.error(f'❌ Error sending flex reply: {e}')
        try:
            with ApiClient(configuration) as api_client:
                line_api = MessagingApi(api_client)
                line_api.reply_message(
                    ReplyMessageRequest(
                        replyToken=reply_token,
                        messages=[text_msg]
                    )
                )
        except Exception as e2:
            logger.error(f'❌ Error sending fallback reply: {e2}')

def send_text_reply(reply_token, text):
    try:
        with ApiClient(configuration) as api_client:
            line_api = MessagingApi(api_client)
            line_api.reply_message(
                ReplyMessageRequest(
                    replyToken=reply_token,
                    messages=[TextMessage(text=text)]
                )
            )
    except Exception as e:
        logger.error(f'❌ Error sending text reply: {e}')

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
    
    body = request.get_data(as_text=True)
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        logger.error('❌ Invalid signature')
        abort(400)
    except Exception as e:
        logger.error(f'❌ Error handling webhook: {e}')
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

@handler.add(MessageEvent, message=TextMessageContent)
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
        send_text_reply(event.reply_token, 'تم الانسحاب، لن تُحسب إجاباتك')
        return

    # إيقاف
    if txt == 'إيقاف':
        if gm.get_game(gid):
            gm.end_game(gid)
            send_text_reply(event.reply_token, 'تم إيقاف اللعبة')
        else:
            send_text_reply(event.reply_token, 'لا توجد لعبة نشطة')
        return

    # بدء لعبة
    if txt in GAMES:
        if not gm.is_registered(uid):
            send_text_reply(event.reply_token, '❌ اكتب "انضم" أولاً للتسجيل')
            return

        if gm.get_game(gid):
            send_text_reply(event.reply_token, '⚠️ يوجد لعبة نشطة بالفعل')
            return

        try:
            with ApiClient(configuration) as api_client:
                line_api = MessagingApi(api_client)
                game_class = GAMES[txt]
                game = game_class(line_api)
                game.set_theme(get_theme(uid))
                gm.start_game(gid, game, txt)
                response = game.start_game()
                send_flex_reply(event.reply_token, response, uid)
        except Exception as e:
            logger.error(f'❌ Error starting game: {e}')
            send_text_reply(event.reply_token, '❌ حدث خطأ أثناء بدء اللعبة')
        return

    # الرد على اللعبة
    game_data = gm.get_game(gid)
    if game_data and gm.is_registered(uid):
        game = game_data['game']
        if not gm.has_answered(gid, uid):
            try:
                result = game.check_answer(txt, uid, name)
                if result:
                    gm.mark_answered(gid, uid)
                    points = result.get('points', 0)
                    won = result.get('won', False)
                    db.update_points(uid, points, won)
                    response = result.get('response')
                    if response:
                        send_flex_reply(event.reply_token, response, uid)
            except Exception as e:
                logger.error(f'❌ Error checking answer: {e}')
        return

# ==================== Run ====================
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    logger.info("🚀 Bot Mesh - Running on port %s", port)
    app.run(host='0.0.0.0', port=port, debug=False)
