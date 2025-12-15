import os
import logging
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

from flask import Flask, request, jsonify, abort

from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.webhooks import MessageEvent, TextMessageContent
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi,
    PushMessageRequest, TextMessage
)

from config import Config
from database import Database
from game_manager import GameManager
from ui import UI


# ---------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------
# Flask App
# ---------------------------------------------------------------------
app = Flask(__name__)


# ---------------------------------------------------------------------
# ENV Validation
# ---------------------------------------------------------------------
if not Config.LINE_SECRET or not Config.LINE_TOKEN:
    raise RuntimeError("LINE credentials are missing")


# ---------------------------------------------------------------------
# LINE SDK
# ---------------------------------------------------------------------
line_config = Configuration(access_token=Config.LINE_TOKEN)
handler = WebhookHandler(Config.LINE_SECRET)


# ---------------------------------------------------------------------
# Core Services
# ---------------------------------------------------------------------
db = Database()
game_mgr = GameManager(db)

executor = ThreadPoolExecutor(
    max_workers=int(os.getenv("WORKERS", 4)),
    thread_name_prefix="bot-worker"
)


# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------
def push_message(user_id: str, messages):
    """Send push message safely"""
    try:
        if not isinstance(messages, list):
            messages = [messages]

        with ApiClient(line_config) as client:
            MessagingApi(client).push_message(
                PushMessageRequest(to=user_id, messages=messages)
            )
    except Exception as e:
        logger.error(f"Push failed for {user_id}: {e}")


def reply_quick(reply_token: str):
    """Instant reply to avoid webhook timeout"""
    try:
        with ApiClient(line_config) as client:
            MessagingApi(client).reply_message(
                reply_token,
                [TextMessage(text="...")]
            )
    except Exception as e:
        logger.warning(f"Quick reply failed: {e}")


# ---------------------------------------------------------------------
# Message Processing (Background)
# ---------------------------------------------------------------------
def process_message(user_id: str, text: str):
    try:
        db.update_activity(user_id)

        user = db.get_user(user_id)
        theme = db.get_theme(user_id)
        ui = UI(theme=theme)

        cmd = Config.normalize(text)

        # ---------------- Commands ----------------
        if cmd == "بداية":
            push_message(user_id, ui.main_menu(user))
            return

        if cmd == "تغيير_الثيم":
            new_theme = db.toggle_theme(user_id)
            push_message(user_id, UI(theme=new_theme).main_menu(user))
            return

        if cmd == "العاب":
            push_message(user_id, ui.games_menu())
            return

        if cmd == "نقاطي":
            if not user:
                push_message(user_id, TextMessage(text="سجل اولا"))
                return
            push_message(user_id, ui.stats_card(user))
            return

        if cmd == "الصدارة":
            push_message(
                user_id,
                ui.leaderboard_card(db.get_leaderboard())
            )
            return

        if cmd in ("تسجيل", "تغيير"):
            db.set_waiting_name(user_id, True)
            push_message(user_id, TextMessage(text="اكتب اسمك:"))
            return

        if cmd == "ايقاف":
            stopped = game_mgr.stop_game(user_id)
            push_message(
                user_id,
                TextMessage(
                    text="تم ايقاف اللعبة" if stopped else "لا توجد لعبة نشطة"
                )
            )
            return

        # ---------------- Name Input ----------------
        if db.is_waiting_name(user_id):
            name = text.strip()[:50]
            if len(name) < 2:
                push_message(user_id, TextMessage(text="الاسم قصير جدا"))
                return

            db.register_user(user_id, name)
            db.set_waiting_name(user_id, False)
            push_message(user_id, ui.main_menu(db.get_user(user_id)))
            return

        # ---------------- Games ----------------
        game_response = game_mgr.handle(user_id, cmd, theme)
        if game_response:
            push_message(user_id, game_response)
            return

        # ---------------- Fallback ----------------
        push_message(user_id, TextMessage(text="اكتب: بداية"))

    except Exception as e:
        logger.exception(f"Processing error ({user_id}): {e}")
        push_message(user_id, TextMessage(text="حدث خطأ غير متوقع"))


# ---------------------------------------------------------------------
# LINE Webhook
# ---------------------------------------------------------------------
@handler.add(MessageEvent, message=TextMessageContent)
def on_message(event: MessageEvent):
    user_id = event.source.user_id
    text = event.message.text.strip()

    reply_quick(event.reply_token)
    executor.submit(process_message, user_id, text)


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


# ---------------------------------------------------------------------
# Health & Root
# ---------------------------------------------------------------------
@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "time": datetime.utcnow().isoformat(),
        "active_games": game_mgr.count_active()
    })


@app.route("/")
def index():
    return jsonify({
        "name": "Bot Mesh",
        "version": "3.0",
        "status": "running"
    })


# ---------------------------------------------------------------------
# Local Run
# ---------------------------------------------------------------------
if __name__ == "__main__":
    logger.info("Starting Bot Mesh v3.0")
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
