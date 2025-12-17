import logging
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from flask import Flask, request, jsonify, abort

from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.webhooks import MessageEvent, TextMessageContent
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi,
    ReplyMessageRequest
)

from config import Config
from database import Database
from game_manager import GameManager
from text_manager import TextManager
from ui import UI

# ================= Logging =================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

# ================= App =================

app = Flask(__name__)

line_config = Configuration(access_token=Config.LINE_TOKEN)
handler = WebhookHandler(Config.LINE_SECRET)

db = Database()
game_mgr = GameManager(db)
text_mgr = TextManager()

executor = ThreadPoolExecutor(
    max_workers=Config.WORKERS,
    thread_name_prefix="worker"
)

# ================= Reply =================

def reply_message(reply_token: str, messages):
    if not reply_token or not messages:
        return

    if not isinstance(messages, list):
        messages = [messages]

    # فلترة الرسائل غير الصالحة + حد LINE (5)
    safe_messages = [m for m in messages if m][:5]

    if not safe_messages:
        return

    try:
        with ApiClient(line_config) as client:
            MessagingApi(client).reply_message(
                ReplyMessageRequest(
                    reply_token=reply_token,
                    messages=safe_messages
                )
            )
        logger.info(f"Reply sent ({len(safe_messages)})")
    except Exception as e:
        logger.error(f"Reply error: {e}")

# ================= Core =================

def process_message(user_id: str, text: str, reply_token: str):
    try:
        logger.info(f"Processing: {user_id} -> {text[:50]}")

        cmd = Config.normalize(text)
        if not cmd:
            return

        db.update_activity(user_id)
        user = db.get_user(user_id)
        is_ignored = db.is_ignored(user_id)

        theme = db.get_theme(user_id) if user else "light"
        ui = UI(theme=theme)

        # ---------- Ignored ----------
        if is_ignored:
            if cmd == "تسجيل":
                db.set_ignored(user_id, False)
                db.set_waiting_name(user_id, True)
                reply_message(reply_token, ui.ask_name())
            return

        # ---------- Main ----------
        if cmd in ("بداية", "بدايه"):
            reply_message(reply_token, ui.main_menu(user))
            return

        if cmd in ("مساعدة", "مساعده"):
            reply_message(reply_token, ui.help_menu())
            return

        # ---------- Theme Toggle ----------
        if cmd == "ثيم":
            if user:
                new_theme = db.toggle_theme(user_id)
                user = db.get_user(user_id)
                ui_new = UI(theme=new_theme)
                theme_name = "الوضع الداكن" if new_theme == "dark" else "الوضع الفاتح"
                reply_message(reply_token, [
                    ui_new.theme_changed(theme_name),
                    ui_new.main_menu(user)
                ])
            else:
                reply_message(reply_token, ui.registration_choice())
            return

        # ---------- Registration ----------
        if db.is_waiting_name(user_id):
            if cmd in Config.RESERVED_COMMANDS:
                reply_message(reply_token, ui.ask_name_invalid())
                return

            name = text.strip()[:Config.MAX_NAME_LENGTH]
            if Config.validate_name(name):
                db.register_user(user_id, name)
                db.set_waiting_name(user_id, False)
                reply_message(reply_token, ui.main_menu(db.get_user(user_id)))
            else:
                reply_message(reply_token, ui.ask_name_invalid())
            return

        if not user:
            if cmd == "تسجيل":
                db.set_waiting_name(user_id, True)
                reply_message(reply_token, ui.ask_name())
            else:
                reply_message(reply_token, ui.registration_choice())
            return

        # ---------- User Commands ----------
        if cmd == "نقاطي":
            reply_message(reply_token, ui.stats_card(user))
            return

        if cmd in ("الصدارة", "الصداره"):
            reply_message(reply_token, ui.leaderboard_card(db.get_leaderboard()))
            return

        if cmd == "العاب":
            reply_message(reply_token, ui.games_menu())
            return

        if cmd in ("ايقاف", "ايقاف اللعبة"):
            if game_mgr.stop_game(user_id):
                reply_message(reply_token, ui.game_stopped())
            return

        # ---------- Text ----------
        text_response = text_mgr.handle(cmd, theme)
        if text_response:
            reply_message(reply_token, text_response)
            return

        # ---------- Games ----------
        game_response = game_mgr.handle(
            user_id=user_id,
            cmd=cmd,
            theme=theme,
            raw_text=text
        )

        if game_response:
            reply_message(reply_token, game_response)
        else:
            reply_message(reply_token, ui.main_menu(user))

    except Exception as e:
        logger.exception(f"Processing error: {e}")

# ================= Webhook =================

@handler.add(MessageEvent, message=TextMessageContent)
def on_message(event: MessageEvent):
    executor.submit(
        process_message,
        event.source.user_id,
        event.message.text,
        event.reply_token
    )

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    except Exception as e:
        logger.error(f"Webhook error: {e}")

    return "OK", 200

# ================= Health =================

@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "active_games": game_mgr.count_active()
    })

@app.route("/")
def index():
    return jsonify({
        "name": Config.BOT_NAME,
        "version": Config.VERSION,
        "status": "running"
    })
