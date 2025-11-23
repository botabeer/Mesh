"""
Bot Mesh - Main Application (Enhanced Version with Themes)
Created by: Abeer Aldosari © 2025
"""
import os
import logging
from flask import Flask, request, abort, jsonify
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    FlexSendMessage, FollowEvent, QuickReply, QuickReplyButton,
    MessageAction
)

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
    """الحصول على اسم المستخدم"""
    try:
        return line_api.get_profile(uid).display_name
    except:
        return 'لاعب'

def get_theme(uid):
    """الحصول على ثيم المستخدم"""
    user = db.get_user(uid)
    return user['theme'] if user else 'white'

def get_games_quick_reply(uid):
    """أزرار الألعاب + زر إيقاف"""
    items = []
    game_buttons = [
        {'emoji': '🧠', 'label': 'ذكاء', 'text': 'ذكاء'},
        {'emoji': '🎨', 'label': 'لون', 'text': 'لون'},
        {'emoji': '🔤', 'label': 'ترتيب', 'text': 'ترتيب'},
        {'emoji': '🔢', 'label': 'رياضيات', 'text': 'رياضيات'},
        {'emoji': '⚡', 'label': 'أسرع', 'text': 'أسرع'},
        {'emoji': '↔️', 'label': 'ضد', 'text': 'ضد'},
        {'emoji': '✏️', 'label': 'تكوين', 'text': 'تكوين'},
        {'emoji': '🎵', 'label': 'أغنية', 'text': 'أغنية'},
        {'emoji': '🎯', 'label': 'لعبة', 'text': 'لعبة'},
        {'emoji': '⛓️', 'label': 'سلسلة', 'text': 'سلسلة'},
        {'emoji': '🤔', 'label': 'خمن', 'text': 'خمن'},
        {'emoji': '💖', 'label': 'توافق', 'text': 'توافق'},
        {'emoji': '⏹️', 'label': 'إيقاف', 'text': 'إيقاف'}
    ]
    for btn in game_buttons:
        items.append(QuickReplyButton(
            action=MessageAction(label=f"{btn['emoji']} {btn['label']}", text=btn['text'])
        ))
    return QuickReply(items=items)

def get_themes_quick_reply(uid):
    """أزرار الثيمات من البداية"""
    items = []
    for key, theme in THEMES.items():
        items.append(QuickReplyButton(
            action=MessageAction(label=f"{theme['name']}", text=f"ثيم:{key}")
        ))
    return QuickReply(items=items)

def send_with_quick_reply(reply_token, messages, uid=None):
    """إرسال رسالة مع قائمة الألعاب والثيمات"""
    if not isinstance(messages, list):
        messages = [messages]
    for msg in messages:
        if isinstance(msg, TextSendMessage):
            msg.quick_reply = get_games_quick_reply(uid)
    line_api.reply_message(reply_token, messages)

# ==================== Routes ====================
@app.route('/')
def home():
    return f"Bot Mesh - Active"

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

# ==================== Event Handlers ====================
@handler.add(MessageEvent, message=TextMessage)
def on_message(event):
    try:
        uid = event.source.user_id
        txt = event.message.text.strip()
        gid = getattr(event.source, 'group_id', uid)
        name = get_name(uid)
        theme = get_theme(uid)
        builder = FlexBuilder(theme)

        # بداية / قائمة
        if txt in ['@bot Mesh', 'بداية', 'start', 'قائمة']:
            gm.register(uid)
            # إضافة قائمة الألعاب + الثيمات
            send_with_quick_reply(
                event.reply_token,
                [
                    FlexSendMessage(alt_text='القائمة', contents=builder.welcome()),
                    TextSendMessage(text="🎨 اختر ثيمك:", quick_reply=get_themes_quick_reply(uid))
                ], uid=uid
            )
            return

        # تغيير الثيم
        elif txt.startswith('ثيم:'):
            theme_name = txt.split(':')[1]
            if theme_name in THEMES:
                db.set_theme(uid, theme_name)
                send_with_quick_reply(
                    event.reply_token,
                    TextSendMessage(text=f'✅ تم تغيير الثيم إلى {THEMES[theme_name]["name"]}'), uid=uid
                )
            else:
                send_with_quick_reply(
                    event.reply_token,
                    TextSendMessage(text='❌ ثيم غير موجود'), uid=uid
                )
            return

        # إيقاف اللعبة
        elif txt == 'إيقاف':
            if gm.get_game(gid):
                gm.end_game(gid)
                send_with_quick_reply(event.reply_token, TextSendMessage(text='⏹️ تم إيقاف اللعبة'), uid=uid)
            else:
                send_with_quick_reply(event.reply_token, TextSendMessage(text='⚠️ لا توجد لعبة نشطة'), uid=uid)
            return

        # بدء الألعاب
        elif txt in GAMES:
            if not gm.is_registered(uid):
                send_with_quick_reply(
                    event.reply_token,
                    TextSendMessage(text='❌ اكتب "انضم" أولاً للتسجيل'), uid=uid
                )
                return

            if gm.get_game(gid):
                send_with_quick_reply(
                    event.reply_token,
                    TextSendMessage(text='⚠️ توجد لعبة نشطة بالفعل\nاكتب "إيقاف" لإنهائها'), uid=uid
                )
                return

            game_class = GAMES[txt]
            game = game_class(line_api)
            game.set_theme(theme)
            gm.start_game(gid, game, txt)
            response = game.start_game()
            send_with_quick_reply(event.reply_token, response, uid=uid)
            logger.info(f'🎮 بدأت لعبة {txt} للمستخدم {name}')
            return

        # التعامل مع إجابات اللعبة
        elif gm.get_game(gid) and gm.is_registered(uid):
            game_data = gm.get_game(gid)
            game = game_data['game']
            game_type = game_data['type']
            result = game.check_answer(txt, uid, name)

            if result and result.get('game_over'):
                points = result.get('points', 0)
                won = result.get('won', False)
                db.update(uid, name, points, won, game_type)
                gm.end_game(gid)

            response = result.get('response') if result else None
            if response:
                send_with_quick_reply(event.reply_token, response, uid=uid)
            return

    except Exception as e:
        logger.error(f'❌ خطأ في on_message: {e}', exc_info=True)
        try:
            send_with_quick_reply(
                event.reply_token,
                TextSendMessage(text='❌ حدث خطأ، حاول مرة أخرى'), uid=uid
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
        send_with_quick_reply(
            event.reply_token,
            [
                FlexSendMessage(alt_text='مرحباً', contents=builder.welcome()),
                TextSendMessage(text="🎨 اختر ثيمك:", quick_reply=get_themes_quick_reply(uid))
            ], uid=uid
        )
        logger.info(f'👋 مستخدم جديد: {name}')
    except Exception as e:
        logger.error(f'❌ خطأ في on_follow: {e}', exc_info=True)

# ==================== Run ====================
if __name__ == '__main__':
    logger.info('=' * 50)
    logger.info('🎮 Bot Mesh Started Successfully')
    logger.info(f'📊 Games Available: {len(GAMES)}')
    logger.info(f'🎨 Themes Available: {len(THEMES)}')
    logger.info(f'🗄️  Database: {DB_PATH}')
    logger.info('=' * 50)

    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
