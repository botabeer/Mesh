# app.py
"""
Bot Mesh - Production LINE Bot Application v4.0
Created by: Abeer Aldosari © 2025
"""

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
from linebot.v3.messaging import Configuration, ApiClient, MessagingApi, ReplyMessageRequest
from linebot.v3.webhooks import MessageEvent, TextMessageContent

from constants import (
    BOT_NAME, BOT_VERSION, BOT_RIGHTS,
    LINE_CHANNEL_SECRET, LINE_CHANNEL_ACCESS_TOKEN,
    GEMINI_KEYS, validate_env, get_username, GAME_LIST,
    DEFAULT_THEME, sanitize_user_input, get_user_level,
    MAX_CACHE_SIZE, RATE_LIMIT_MESSAGES, MAX_CONCURRENT_GAMES
)

from ui_builder import (
    build_home, build_games_menu, build_my_points,
    build_leaderboard, build_registration_required
)

from game_loader import GameLoader

# ========================
# ENV CHECK
# ========================
try:
    validate_env()
except ValueError as e:
    print(f"❌ خطأ: {e}")
    sys.exit(1)

# ========================
# FLASK
# ========================
app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# ========================
# STORAGE
# ========================
registered_users = {}
user_themes = {}

user_message_count = defaultdict(list)
rate_limit_lock = threading.Lock()

# ========================
# GAME LOADER
# ========================
game_loader = GameLoader()

# ========================
# ROUTES
# ========================
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers.get('X-Line-Signature', '')
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@app.route("/")
def home():
    return f"{BOT_NAME} v{BOT_VERSION} is running ✅"

# ========================
# MESSAGE HANDLER
# ========================
@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    user_id = event.source.user_id
    text = sanitize_user_input(event.message.text)

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

        if text.startswith("لعبة "):
            game_name = text.replace("لعبة ", "").strip()
            game = game_loader.create_game(game_name)

            if not game:
                available = ", ".join(game_loader.get_available_games())
                reply_text = f"❌ اللعبة غير موجودة\n\nالمتاح:\n{available}"
            else:
                game.start()
                q = game.get_question()
                reply_text = q["text"]

            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[{"type": "text", "text": reply_text}]
                )
            )

# ========================
# START
# ========================
if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
