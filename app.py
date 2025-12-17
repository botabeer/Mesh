import logging
import atexit
from datetime import datetime
from threading import Lock
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict

from flask import Flask, request, jsonify, abort
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.webhooks import MessageEvent, TextMessageContent
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
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

# ================= Rate Limiter =================

class RateLimiter:
    def __init__(self, max_requests, window):
        self.max_requests = max_requests
        self.window = window
        self.requests = defaultdict(list)
        self._lock = Lock()

    def is_allowed(self, user_id):
        now = datetime.now().timestamp()
        cutoff = now - self.window

        with self._lock:
            self.requests[user_id] = [
                t for t in self.requests[user_id] if t > cutoff
            ]

            if len(self.requests[user_id]) >= self.max_requests:
                return False

            self.requests[user_id].append(now)
            return True


rate_limiter = RateLimiter(
    Config.RATE_LIMIT_REQUESTS,
    Config.RATE_LIMIT_WINDOW
)

# ================= Cleanup =================

def cleanup():
    logger.info("Shutting down executor")
    executor.shutdown(wait=True, cancel_futures=True)
    db.cleanup_memory(timeout=0)
    logger.info("Cleanup completed")


atexit.register(cleanup)

# ================= LINE Helpers =================

def reply_message(reply_token, messages):
    if not reply_token or not messages:
        return

    if not isinstance(messages, list):
        messages = [messages]

    messages = [m for m in messages if m][:5]
    if not messages:
        return

    try:
        with ApiClient(line_config) as client:
            MessagingApi(client).reply_message(
                ReplyMessageRequest(
                    reply_token=reply_token,
                    messages=messages
                )
            )
    except Exception as e:
        logger.error(f"Reply error: {e}")

# ================= Core Logic =================

def process_message(user_id, text, reply_token):
    try:
        if not rate_limiter.is_allowed(user_id):
            logger.warning(f"Rate limit exceeded: {user_id}")
            return

        if not text or len(text) > Config.MAX_MESSAGE_LENGTH:
            return

        cmd = Config.normalize(text)
        if not cmd:
            return

        db.update_activity(user_id)
        user = db.get_user(user_id)
        theme = db.get_theme(user_id) if user else "light"
        ui = UI(theme)

        if db.is_ignored(user_id):
            if cmd == "تسجيل":
                db.set_ignored(user_id, False)
                db.set_waiting_name(user_id, True)
                reply_message(reply_token, ui.ask_name())
            return

        if cmd in ("بداية", "بدايه"):
            reply_message(reply_token, ui.main_menu(user))
            return

        if cmd in ("مساعدة", "مساعده"):
            reply_message(reply_token, ui.help_menu())
            return

        if cmd == "ثيم":
            if user:
                new_theme = db.toggle_theme(user_id)
                ui_new = UI(new_theme)
                name = "الوضع الداكن" if new_theme == "dark" else "الوضع الفاتح"
                reply_message(
                    reply_token,
                    [ui_new.theme_changed(name), ui_new.main_menu(db.get_user(user_id))]
                )
            else:
                reply_message(reply_token, ui.registration_choice())
            return

        if db.is_waiting_name(user_id):
            if cmd in Config.RESERVED_COMMANDS:
                reply_message(reply_token, ui.ask_name_invalid())
                return

            name = Config.sanitize_text(text, Config.MAX_NAME_LENGTH)
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

        if cmd == "نقاطي":
            reply_message(reply_token, ui.stats_card(user))
            return

        if cmd in ("الصدارة", "الصداره"):
            reply_message(
                reply_token,
                ui.leaderboard_card(db.get_leaderboard())
            )
            return

        if cmd == "العاب":
            reply_message(reply_token, ui.games_menu())
            return

        if cmd in ("ايقاف", "ايقاف اللعبة"):
            if game_mgr.stop_game(user_id):
                reply_message(reply_token, ui.game_stopped())
            return

        text_response = text_mgr.handle(cmd, theme)
        if text_response:
            reply_message(reply_token, text_response)
            return

        game_response = game_mgr.handle(
            user_id=user_id,
            cmd=cmd,
            raw_text=text,
            theme=theme
        )

        reply_message(
            reply_token,
            game_response if game_response else ui.main_menu(user)
        )

    except Exception as e:
        logger.exception(f"Processing error [{user_id}]: {e}")
        reply_message(reply_token, UI("light").error_message("general"))

# ================= Webhooks =================

@handler.add(MessageEvent, message=TextMessageContent)
def on_message(event):
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
        logger.warning(f"Invalid signature from {request.remote_addr}")
        abort(400)
    except Exception as e:
        logger.exception(f"Webhook error: {e}")
        abort(500)

    return "OK", 200

# ================= Health =================

@app.route("/health")
def health():
    return jsonify(
        status="healthy",
        timestamp=datetime.utcnow().isoformat(),
        active_games=game_mgr.count_active()
    )

@app.route("/")
def index():
    return jsonify(
        name=Config.BOT_NAME,
        version=Config.VERSION,
        status="running"
    )

# ================= Run =================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=Config.PORT,
        debug=False
    )
