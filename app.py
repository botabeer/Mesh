import os
import logging
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

from flask import Flask, request, abort, jsonify

from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.webhooks import MessageEvent, TextMessageContent
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    PushMessageRequest,
    TextMessage
)

from config import Config
from database import Database
from game_manager import GameManager
from ui import UI

# ----------------------------------
# Logging
# ----------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("bot")

# ----------------------------------
# Flask
# ----------------------------------
app = Flask(__name__)

# ----------------------------------
# LINE
# ----------------------------------
if not Config.LINE_SECRET or not Config.LINE_TOKEN:
    raise RuntimeError("LINE credentials missing")

line_config = Configuration(access_token=Config.LINE_TOKEN)
handler = WebhookHandler(Config.LINE_SECRET)

api_client = ApiClient(line_config)
messaging_api = MessagingApi(api_client)

# ----------------------------------
# Core services
# ----------------------------------
db = Database()
ui = UI()
games = GameManager(db, ui)

executor = ThreadPoolExecutor(max_workers=2)

# ----------------------------------
# Helpers
# ----------------------------------
def push(user_id: str, messages):
    if not isinstance(messages, list):
        messages = [messages]

    try:
        messaging_api.push_message(
            PushMessageRequest(
                to=user_id,
                messages=messages
            )
        )
    except Exception:
        logger.exception("Push failed")

# ----------------------------------
# Background processing
# ----------------------------------
def process_message(user_id: str, text: str):
    try:
        db.touch(user_id)

        theme = db.get_theme(user_id)
        ui.set_theme(theme)

        result = games.handle(user_id, text)
        if result:
            push(user_id, result)

    except Exception:
        logger.exception("Processing error")
        push(user_id, TextMessage(text="حدث خطأ غير متوقع"))

# ----------------------------------
# Webhook handler (FAST)
# ----------------------------------
@handler.add(MessageEvent, message=TextMessageContent)
def on_message(event: MessageEvent):
    user_id = event.source.user_id
    text = event.message.text.strip()

    # رد فوري خفيف جدًا
    try:
        messaging_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text="⏳")]
            )
        )
    except Exception:
        pass

    executor.submit(process_message, user_id, text)

# ----------------------------------
# Routes
# ----------------------------------
@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    except Exception:
        logger.exception("Webhook error")

    return "OK", 200


@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "time": datetime.utcnow().isoformat(),
        "active_games": games.active_count()
    })


@app.route("/")
def index():
    return jsonify({
        "name": "Bot Mesh",
        "version": "3.0",
        "status": "running"
    })


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
