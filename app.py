"""
Bot Mesh - Main Application (Enhanced AI Version)
Created by: Abeer Aldosari © 2025
"""
import os
import logging
from flask import Flask, request, abort, jsonify
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, FlexSendMessage, FollowEvent,
    QuickReply, QuickReplyButton, MessageAction
)

# استيراد الإعدادات والمكونات
from config import LINE_TOKEN, LINE_SECRET, DB_PATH, THEMES
from database import DB
from flex_builder import FlexBuilder
from game_manager import GameManager

# استيراد جميع الألعاب تلقائياً من مجلد games
from games import *

# ==================== إعداد اللوق ====================
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
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
    """الحصول على اسم المستخدم من LINE"""
    try:
        return line_api.get_profile(uid).display_name
    except:
        return 'لاعب'

def get_theme(uid):
    """الحصول على ثيم المستخدم"""
    user = db.get_user(uid)
    return user['theme'] if user else 'white'

def get_games_quick_reply(uid):
    """إنشاء أزرار الألعاب الثابتة مع زر إيقاف"""
    items = []
    for label in GAMES.keys():
        items.append(
            QuickReplyButton(
                action=MessageAction(label=label, text=label)
            )
        )
    items.append(
        QuickReplyButton(
            action=MessageAction(label='إيقاف', text='إيقاف')
        )
    )
    return QuickReply(items=items)

def send_with_games_menu(reply_token, message, uid=None):
    """إرسال رسالة مع قائمة الألعاب"""
    if isinstance(message, TextSendMessage):
        message.quick_reply = get_games_quick_reply(uid)
        line_api.reply_message(reply_token, message)
    elif isinstance(message, FlexSendMessage):
        text_msg = TextSendMessage(
            text="اختر لعبة أو أمر:",
            quick_reply=get_games_quick_reply(uid)
        )
        line_api.reply_message(reply_token, [message, text_msg])
    else:
        line_api.reply_message(reply_token, message)

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
        logger.error('Invalid signature')
        abort(400)
    return 'OK'

# ==================== LINE Event Handlers ====================
@handler.add(MessageEvent, message=TextMessage)
def on_message(event):
    try:
        uid = event.source.user_id
        txt = event.message.text.strip()
        gid = getattr(event.source, 'group_id', uid)
        name = get_name(uid)
        theme = get_theme(uid)
        builder = FlexBuilder(theme)

        # تسجيل أو تحديث اسم المستخدم أسبوعياً
        db.register_or_update_user(uid, name)

        # تجاهل المستخدم إذا انسحب
        if txt == 'انسحب':
            gm.remove_user(uid)
            send_with_games_menu(
                event.reply_token,
                TextSendMessage(text='تم إلغاء تسجيلك من الألعاب'), uid=uid
            )
            return

        # أوامر البداية والمساعدة
        if txt in ['@bot Mesh', 'بداية', 'start', 'قائمة']:
            gm.register(uid)
            send_with_games_menu(
                event.reply_token,
                FlexSendMessage(alt_text='القائمة', contents=builder.welcome())
            )
            return
        elif txt == 'مساعدة':
            send_with_games_menu(
                event.reply_token,
                FlexSendMessage(alt_text='مساعدة', contents=builder.help())
            )
            return
        elif txt == 'نقاطي':
            user = db.get_user(uid)
            if user:
                data = {'points': user['points'], 'games': user['games'], 'wins': user['wins']}
                rank = db.rank(uid)
                send_with_games_menu(
                    event.reply_token,
                    FlexSendMessage(alt_text='نقاطي', contents=builder.stats(data, rank))
                )
            else:
                send_with_games_menu(
                    event.reply_token,
                    TextSendMessage(text='لم تلعب بعد\nاكتب "انضم" للبدء'), uid=uid
                )
            return
        elif txt.startswith('ثيم:'):
            theme_name = txt.split(':')[1]
            if theme_name in THEMES:
                db.set_theme(uid, theme_name)
                send_with_games_menu(
                    event.reply_token,
                    TextSendMessage(text=f'تم التغيير إلى {THEMES[theme_name]["name"]}'), uid=uid
                )
            else:
                send_with_games_menu(
                    event.reply_token,
                    TextSendMessage(text='ثيم غير موجود'), uid=uid
                )
            return
        elif txt == 'إيقاف':
            if gm.get_game(gid):
                gm.end_game(gid)
                send_with_games_menu(
                    event.reply_token,
                    TextSendMessage(text='تم إيقاف اللعبة'), uid=uid
                )
            return
        elif txt in GAMES:
            if not gm.is_registered(uid):
                send_with_games_menu(
                    event.reply_token,
                    TextSendMessage(text='اكتب "انضم" أولاً للتسجيل'), uid=uid
                )
                return
            if gm.get_game(gid):
                send_with_games_menu(
                    event.reply_token,
                    TextSendMessage(text='يوجد لعبة نشطة بالفعل\nاكتب "إيقاف" لإنهائها'), uid=uid
                )
                return
            game_class = GAMES[txt]
            game = game_class(line_api)
            game.set_theme(theme)
            gm.start_game(gid, game, txt)
            response = game.start_game()
            send_with_games_menu(event.reply_token, response, uid=uid)
            return

        # التعامل مع إجابات اللعبة
        game_data = gm.get_game(gid)
        if game_data and gm.is_registered(uid):
            game = game_data['game']
            if gm.has_answered(gid, uid):
                return
            result = game.check_answer(txt, uid, name)
            gm.mark_answered(gid, uid)
            if result and result.get('game_over'):
                points = result.get('points', 0)
                won = result.get('won', False)
                db.update(uid, name, points, won, game_data['type'])
                gm.end_game(gid)
            response = result.get('response') if result else None
            if response:
                send_with_games_menu(event.reply_token, response, uid=uid)

    except Exception as e:
        logger.error(f'خطأ في on_message: {e}', exc_info=True)
        try:
            send_with_games_menu(
                event.reply_token,
                TextSendMessage(text='حدث خطأ، حاول مرة أخرى'), uid=uid
            )
        except:
            pass

@handler.add(FollowEvent)
def on_follow(event):
    try:
        uid = event.source.user_id
        name = get_name(uid)
        gm.register(uid)
        builder = FlexBuilder('white')
        send_with_games_menu(
            event.reply_token,
            FlexSendMessage(alt_text='مرحباً', contents=builder.welcome()), uid=uid
        )
    except Exception as e:
        logger.error(f'خطأ في on_follow: {e}', exc_info=True)

if __name__ == '__main__':
    logger.info('Bot Mesh Started Successfully')
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
