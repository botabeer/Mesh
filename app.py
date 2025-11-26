import os
import sys
import logging
from datetime import datetime, timedelta
from collections import OrderedDict, defaultdict
from flask import Flask, request, abort
import threading
import json

from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi,
    ReplyMessageRequest
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent

# ===== ✅ الاستيراد الصحيح بعد نقل game_loader =====
from game_loader import GameLoader

# ===== تحميل الألعاب =====
game_loader = GameLoader("games")
AVAILABLE_GAMES = game_loader.loaded_games

# ===== إعداد Flask و LINE =====
app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

registered_users = {}
user_themes = {}
active_games = {}

# ===== Route رئيسية =====
@app.route("/", methods=["GET"])
def home():
    return {"status": "Bot is running", "games": list(AVAILABLE_GAMES.keys())}

# ===== Webhook =====
@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"

# ===== استقبال الرسائل =====
@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    user_id = event.source.user_id
    text = event.message.text.strip()

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

        if text.startswith("لعبة "):
            game_name = text.replace("لعبة ", "").strip()

            game = game_loader.create_game(game_name)

            if not game:
                available = "، ".join(game_loader.get_available_games())
                msg = f"❌ اللعبة غير موجودة\n\n🎮 الألعاب المتاحة:\n{available}"
            else:
                active_games[user_id] = game
                game.start()
                q = game.get_question()

                msg = (
                    f"🎮 {game_name}\n\n"
                    f"السؤال: {q['text']}\n"
                    f"الجولة: {q['round']} / {q['total_rounds']}"
                )

            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[{"type": "text", "text": msg}]
                )
            )

# ===== تشغيل السيرفر =====
if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
