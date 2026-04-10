from flask import Flask, request, abort, jsonify
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi,
    ReplyMessageRequest, TextMessage, FlexMessage, FlexContainer
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent
import os
import sys
import logging
from datetime import datetime, timedelta
from threading import Lock
from apscheduler.schedulers.background import BackgroundScheduler

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

LINE_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
LINE_SECRET = os.getenv('LINE_CHANNEL_SECRET')

if not LINE_TOKEN or not LINE_SECRET:
    logger.error("Missing LINE credentials")
    sys.exit(1)

configuration = Configuration(access_token=LINE_TOKEN)
handler = WebhookHandler(LINE_SECRET)

from database import DB
from ui import UI
from text_commands import TextCommands
from games import (
    CategoryGame, FastGame, CompatibilityGame, SongGame,
    OppositeGame, ChainGame, LettersGame, RiddleGame,
    ScrambleGame, MafiaGame, WordColorGame, LetterGame
)

DB.init()
TextCommands.load_all()

# إصلاح: lock موحد لحماية كل الحالات المشتركة
_state_lock = Lock()

game_sessions = {}
waiting_for_name = set()
user_themes = {}
silent_users = set()

TEXT_COMMANDS = {
    'سؤال': 'questions',
    'منشن': 'mentions',
    'تحدي': 'challenges',
    'اعتراف': 'confessions',
    'اقتباس': 'quotes',
    'موقف': 'situations',
    'خاص': 'private',
    'مجهول': 'anonymous',
    'نصيحة': 'advice',
    'شعر': 'poem'
}

GAME_MAP = {
    'فئه': CategoryGame,
    'اسرع': FastGame,
    'توافق': CompatibilityGame,
    'اغنيه': SongGame,
    'ضد': OppositeGame,
    'سلسله': ChainGame,
    'تكوين': LettersGame,
    'لغز': RiddleGame,
    'ترتيب': ScrambleGame,
    'مافيا': MafiaGame,
    'لون': WordColorGame,
    'حرف': LetterGame
}

# إصلاح: timeout للألعاب المتروكة (30 دقيقة)
GAME_TIMEOUT_MINUTES = 30

scheduler = BackgroundScheduler()


def cleanup_inactive_users():
    """حذف المستخدمين غير النشطين بعد 7 أيام"""
    try:
        deleted = DB.cleanup_inactive_users(days=7)
        logger.info(f"Cleanup: Removed {deleted} inactive users")
    except Exception as e:
        logger.error(f"Cleanup error: {e}")


def cleanup_stale_games():
    """إصلاح: حذف الألعاب المتروكة أكثر من 30 دقيقة"""
    cutoff = datetime.now() - timedelta(minutes=GAME_TIMEOUT_MINUTES)
    stale_groups = []

    with _state_lock:
        for gid, game in list(game_sessions.items()):
            started = getattr(game, '_started_at', None)
            if started and started < cutoff:
                stale_groups.append(gid)

    if stale_groups:
        with _state_lock:
            for gid in stale_groups:
                game_sessions.pop(gid, None)
        logger.info(f"Cleaned {len(stale_groups)} stale game sessions")


scheduler.add_job(cleanup_inactive_users, 'cron', hour=3, minute=0)
scheduler.add_job(cleanup_stale_games, 'interval', minutes=10)
scheduler.start()


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers.get('X-Line-Signature', '')
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        logger.error("Invalid signature")
        abort(400)
    except Exception as e:
        logger.error(f"Webhook error: {e}")
    return 'OK', 200


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        line_api = MessagingApi(api_client)
        user_id = event.source.user_id
        text = event.message.text.strip()
        group_id = getattr(event.source, 'group_id', None) or user_id

        try:
            response = process_message(text, user_id, group_id, line_api)
            if response:
                messages = response if isinstance(response, list) else [response]
                line_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=messages
                    )
                )
        except Exception as e:
            logger.error(f"Message processing error: {e}", exc_info=True)


def process_message(text, user_id, group_id, line_api):
    normalized_text = text.lower().strip()

    # إصلاح: قراءة الحالة داخل lock
    with _state_lock:
        is_silent = user_id in silent_users
        is_waiting = user_id in waiting_for_name

    if is_silent:
        if normalized_text in ['تسجيل', 'بداية', 'start', 'ابدا']:
            with _state_lock:
                silent_users.discard(user_id)
            logger.info(f"User {user_id} reactivated")
        else:
            return None

    user = DB.get_user(user_id)
    theme = user_themes.get(user_id, user['theme'] if user else 'light')

    if is_waiting:
        return handle_name_registration(text, user_id)

    if normalized_text in TEXT_COMMANDS:
        content = TextCommands.get_random(TEXT_COMMANDS[normalized_text])
        msg = TextMessage(text=content)
        msg.quick_reply = UI.get_quick_reply()
        return msg

    if normalized_text in ['بداية', 'start', 'ابدا']:
        if user:
            DB.update_activity(user_id)
        return create_welcome_message(user, theme)

    if normalized_text in ['مساعدة', 'help', 'مساعده']:
        return FlexMessage(
            alt_text="Help",
            contents=FlexContainer.from_dict(UI.help_card(theme))
        )

    if normalized_text in ['نص', 'نصوص']:
        return FlexMessage(
            alt_text="Text Commands",
            contents=FlexContainer.from_dict(UI.text_commands_menu(theme))
        )

    if normalized_text in ['العاب', 'ألعاب', 'الالعاب']:
        return FlexMessage(
            alt_text="Games",
            contents=FlexContainer.from_dict(UI.games_menu(theme))
        )

    if normalized_text in ['تسجيل', 'تغيير']:
        with _state_lock:
            silent_users.discard(user_id)
            waiting_for_name.add(user_id)
        msg = TextMessage(text="اكتب اسمك الان")
        msg.quick_reply = UI.get_quick_reply()
        return msg

    if normalized_text == 'نقاطي':
        if not user:
            return create_error_message("يجب التسجيل اولا - اكتب: تسجيل")
        DB.update_activity(user_id)
        return FlexMessage(
            alt_text="Your Stats",
            contents=FlexContainer.from_dict(UI.stats(user, theme))
        )

    if normalized_text in ['الصدارة', 'صدارة']:
        leaders = DB.get_leaderboard()
        return FlexMessage(
            alt_text="Leaderboard",
            contents=FlexContainer.from_dict(UI.leaderboard(leaders, theme))
        )

    if normalized_text == 'ثيم':
        if not user:
            return create_error_message("يجب التسجيل اولا")
        new_theme = 'dark' if theme == 'light' else 'light'
        DB.set_theme(user_id, new_theme)
        user_themes[user_id] = new_theme
        theme_name = 'الداكن' if new_theme == 'dark' else 'الفاتح'
        return create_success_message(f"تم التغيير للثيم {theme_name}")

    if normalized_text == 'انسحب':
        with _state_lock:
            game = game_sessions.get(group_id)
            if game:
                game.withdrawn_users.add(user_id)
            silent_users.add(user_id)

        logger.info(f"User {user_id} entered silent mode")
        msg = TextMessage(text="تم الانسحاب - لن يتم احتساب اجاباتك\nللعودة اكتب: تسجيل")
        msg.quick_reply = UI.get_quick_reply()
        return msg

    if normalized_text == 'ايقاف':
        with _state_lock:
            removed = game_sessions.pop(group_id, None)
        if removed:
            return create_success_message("تم ايقاف اللعبة")
        return None

    if not user:
        return None

    if normalized_text in GAME_MAP:
        return start_game(normalized_text, group_id, line_api, theme)

    with _state_lock:
        active_game = game_sessions.get(group_id)

    if active_game:
        return handle_game_answer(group_id, text, user_id, user)

    return None


def handle_name_registration(name, user_id):
    name = name.strip()
    if 1 <= len(name) <= 20:
        DB.register_user(user_id, name)
        with _state_lock:
            waiting_for_name.discard(user_id)
            silent_users.discard(user_id)

        user = DB.get_user(user_id)
        msg = FlexMessage(
            alt_text="Registration Complete",
            contents=FlexContainer.from_dict(
                UI.welcome(name, True, user['theme'])
            )
        )
        msg.quick_reply = UI.get_quick_reply()
        return msg

    with _state_lock:
        waiting_for_name.discard(user_id)
    return create_error_message("الاسم يجب ان يكون بين 1 و 20 حرف")


def create_welcome_message(user, theme):
    name = user['name'] if user else 'لاعب'
    is_registered = bool(user)
    msg = FlexMessage(
        alt_text="Bot Mesh",
        contents=FlexContainer.from_dict(UI.welcome(name, is_registered, theme))
    )
    msg.quick_reply = UI.get_quick_reply()
    return msg


def create_error_message(text):
    msg = TextMessage(text=text)
    msg.quick_reply = UI.get_quick_reply()
    return msg


def create_success_message(text):
    msg = TextMessage(text=text)
    msg.quick_reply = UI.get_quick_reply()
    return msg


def start_game(game_type, group_id, line_api, theme):
    try:
        game_class = GAME_MAP[game_type]
        game = game_class(line_api, theme=theme)
        with _state_lock:
            game_sessions[group_id] = game
        return game.start_game()
    except Exception as e:
        logger.error(f"Game start error {game_type}: {e}", exc_info=True)
        return create_error_message("حدث خطأ في بدء اللعبة")


def handle_game_answer(group_id, text, user_id, user):
    with _state_lock:
        game = game_sessions.get(group_id)

    if not game:
        return None

    if user_id in game.withdrawn_users:
        return None

    try:
        result = game.check_answer(text, user_id, user['name'])
    except Exception as e:
        logger.error(f"Game answer error: {e}", exc_info=True)
        return None

    if not result:
        return None

    if isinstance(result, (TextMessage, FlexMessage)):
        return result

    if not isinstance(result, dict):
        return None

    if result.get('withdrawn') or result.get('game_over'):
        with _state_lock:
            game_sessions.pop(group_id, None)

        points = result.get('points', 0)
        if points > 0 and not result.get('withdrawn'):
            won = result.get('won', True)
            DB.add_points(user_id, points, won, game.game_name)

    return result.get('response')


@app.route('/health')
def health():
    with _state_lock:
        active_games = len(game_sessions)
        silent_count = len(silent_users)
    return jsonify({
        'status': 'ok',
        'time': datetime.now().isoformat(),
        'users': DB.get_stats(),
        'active_games': active_games,
        'silent_users': silent_count
    }), 200


@app.route('/')
def index():
    return "Bot Mesh - Running", 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
