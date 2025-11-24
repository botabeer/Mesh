"""
Bot Mesh - Main App Fully Integrated v3 SDK
Created by: Abeer Aldosari © 2025
"""

import os
import logging
from datetime import datetime, timedelta
from flask import Flask, request, abort, jsonify

from linebot.v3.messaging import ApiClient, MessagingApi
from linebot.v3.messaging.models import (
    ReplyMessageRequest, TextMessage, FlexMessage
)
from linebot.v3.messaging.models import WebhookRequest
from linebot.v3.messaging.models import Event, MessageEvent, TextMessageContent, FollowEvent

# ===========================
# CONFIGURATION
# ===========================
CHANNEL_ACCESS = os.environ.get("CHANNEL_ACCESS", "")
PORT = int(os.environ.get("PORT", 10000))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# ===========================
# USERS & POINTS SYSTEM
# ===========================
users_db = {}  # {user_id: {"name": str, "points": int, "theme": str, "last_active": datetime}}

DEFAULT_THEME = "💜"
THEMES = ["💜", "💚", "🤍", "🖤", "💙", "🩶", "🩷", "🧡", "🤎"]

def register_user(user_id, name):
    if user_id not in users_db:
        users_db[user_id] = {
            "name": name,
            "points": 0,
            "theme": DEFAULT_THEME,
            "last_active": datetime.now()
        }

# ===========================
# GAME LOADER
# ===========================
import importlib
import inspect
from games.base_game import BaseGame

games_list = []
games_dir = os.path.dirname(__file__) + "/games"
invalid_modules = []

for filename in os.listdir(games_dir):
    if filename.endswith(".py") and filename not in ["__init__.py", "base_game.py", "game_loader.py"]:
        module_name = filename[:-3]
        try:
            module = importlib.import_module(f"games.{module_name}")
            found_game = False
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if issubclass(obj, BaseGame) and obj.__module__ == module.__name__:
                    games_list.append(obj)
                    logger.info(f"✅ Loaded game: {obj.__name__}")
                    found_game = True
            if not found_game:
                invalid_modules.append(module_name)
                logger.warning(f"⚠️ Module '{module_name}' does not contain a valid BaseGame class")
        except Exception as e:
            invalid_modules.append(module_name)
            logger.error(f"❌ Failed to import module '{module_name}': {e}")

logger.info(f"📊 Total valid games loaded: {len(games_list)}")
if invalid_modules:
    logger.warning(f"⚠️ Modules with issues: {', '.join(invalid_modules)}")
else:
    logger.info("🎉 All game modules loaded successfully")

# ===========================
# FLEX MESSAGES BUILDER
# ===========================
def build_footer():
    # أزرار ثابتة أسفل كل نافذة
    buttons = [
        {"type": "button", "action": {"type": "message", "label": "انضم", "text": "انضم"}},
        {"type": "button", "action": {"type": "message", "label": "انسحب", "text": "انسحب"}},
        {"type": "button", "action": {"type": "message", "label": "نقاطي", "text": "نقاطي"}},
        {"type": "button", "action": {"type": "message", "label": "صدارة", "text": "صدارة"}},
    ]
    return {
        "type": "box",
        "layout": "horizontal",
        "spacing": "sm",
        "contents": buttons
    }

def build_home(user_id):
    user = users_db.get(user_id, {})
    name = user.get("name", "غير مسجل")
    points = user.get("points", 0)
    theme = user.get("theme", DEFAULT_THEME)
    return {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                {"type": "text", "text": f" Bot Mesh"},
                {"type": "text", "text": f"▪️ مرحباً: {name}"},
                {"type": "text", "text": f"▪️ النقاط: {points}"},
                {"type": "text", "text": f"▪️ اختر ثيمك: {theme}"},
            ]
        },
        "footer": build_footer()
    }

def build_games_menu():
    game_buttons = []
    for game in games_list:
        game_buttons.append({
            "type": "button",
            "action": {"type": "message", "label": game.__name__, "text": game.__name__}
        })
    return {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [{"type": "text", "text": "🎮 اختر لعبتك:"}] + game_buttons
        },
        "footer": build_footer()
    }

# ===========================
# ROUTES
# ===========================
@app.route("/", methods=["GET"])
def index():
    return "Bot Mesh Online ✅"

@app.route("/webhook", methods=["POST"])
def webhook():
    payload = request.get_data(as_text=True)
    try:
        webhook_request = WebhookRequest.parse_raw(payload)
    except Exception as e:
        logger.error(f"❌ Invalid WebhookRequest: {e}")
        abort(400)

    for event in webhook_request.events:
        handle_event(event)

    return "OK"

# ===========================
# EVENT HANDLER
# ===========================
def handle_event(event: Event):
    user_id = getattr(event.source, "user_id", None)
    if not user_id:
        return

    # تسجيل المستخدم عند أول مرة
    if hasattr(event, "message") and isinstance(event.message, TextMessageContent):
        text = event.message.text
        name = "User"  # يمكنك تعديل لاحقًا لاسم حقيقي
        register_user(user_id, name)

        if text == "بداية":
            send_flex(user_id, build_home(user_id))
        elif text == "مساعدة":
            send_flex(user_id, build_games_menu())
        # يمكنك إضافة التعامل مع الأوامر الأخرى هنا

# ===========================
# SEND FLEX
# ===========================
def send_flex(user_id, flex_dict):
    config = {"access_token": CHANNEL_ACCESS}
    flex_message = FlexMessage(alt_text="Bot Mesh", contents=flex_dict)
    with ApiClient({"access_token": CHANNEL_ACCESS}) as client:
        messaging_api = MessagingApi(client)
        messaging_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token="dummy",  # يجب استبداله بـ event.reply_token عند الاستدعاء الحقيقي
                messages=[flex_message]
            )
        )

# ===========================
# RUN APP
# ===========================
if __name__ == "__main__":
    logger.info("🚀 Starting @Bot Mesh on port %s", PORT)
    app.run(host="0.0.0.0", port=PORT)
