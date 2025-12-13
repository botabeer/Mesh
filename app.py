# ========================================
# app.py - Main Application File
# ========================================

import os
import sys
import logging
import threading
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Optional, Dict, Any, List

from flask import Flask, request, abort, jsonify
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi,
    ReplyMessageRequest, TextMessage, FlexMessage
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent

from config import Config
from database import Database
from ui_builder import UIBuilder
from game_manager import GameManager

# -------------------------------------------------

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("botmesh")

# -------------------------------------------------
# Configuration
# -------------------------------------------------

Config.validate()

configuration = Configuration(access_token=Config.LINE_ACCESS_TOKEN)
handler = WebhookHandler(Config.LINE_SECRET)

db = Database(Config.DATABASE_PATH)
ui = UIBuilder()
game_mgr = GameManager(db)

# -------------------------------------------------
# Runtime State
# -------------------------------------------------

user_sessions: Dict[str, Any] = {}
pending_registrations: Dict[str, datetime] = {}
user_rate_limit = defaultdict(list)
user_cache: Dict[str, dict] = {}

# -------------------------------------------------
# Helpers
# -------------------------------------------------

def is_rate_limited(user_id: str) -> bool:
    now = datetime.utcnow()
    window = timedelta(seconds=Config.RATE_LIMIT_WINDOW)
    timestamps = [t for t in user_rate_limit[user_id] if now - t < window]
    user_rate_limit[user_id] = timestamps
    if len(timestamps) >= Config.RATE_LIMIT_MESSAGES:
        return True
    user_rate_limit[user_id].append(now)
    return False


def safe_reply(line_api: MessagingApi, reply_token: str, messages: List[Any]):
    if not messages:
        return
    clean = []
    for m in messages:
        if isinstance(m, (FlexMessage, TextMessage)):
            clean.append(m)
        else:
            clean.append(TextMessage(text=str(m)))
    try:
        line_api.reply_message(
            ReplyMessageRequest(
                reply_token=reply_token,
                messages=clean
            )
        )
    except Exception:
        logger.exception("Reply failed")


def get_user_profile(line_api: MessagingApi, user_id: str, src_type: str) -> Optional[dict]:
    cached = user_cache.get(user_id)
    if cached and datetime.utcnow() - cached["_cached_at"] < timedelta(minutes=5):
        return cached["data"]

    user = db.get_user(user_id)
    if not user:
        name = "User"
        if src_type == "user":
            try:
                profile = line_api.get_profile(user_id)
                name = profile.display_name or name
            except Exception:
                pass
        db.create_user(user_id, name[:100])
        user = db.get_user(user_id)

    user_cache[user_id] = {
        "data": user,
        "_cached_at": datetime.utcnow()
    }
    return user

# -------------------------------------------------
# Async Message Processor
# -------------------------------------------------

def process_message_async(event, line_api):
    try:
        user_id = event.source.user_id
        text = (event.message.text or "").strip()
        if not text or is_rate_limited(user_id):
            return

        src_type = event.source.type
        ctx_id = (
            getattr(event.source, "group_id", None)
            or getattr(event.source, "room_id", None)
            or user_id
        )

        user = get_user_profile(line_api, user_id, src_type)
        if not user:
            return

        username = user["name"]
        points = int(user["points"])
        is_reg = bool(user["is_registered"])
        theme = user.get("theme", "light")

        normalized = Config.normalize(text)

        if normalized in ("بداية", "start", "home"):
            safe_reply(line_api, event.reply_token, [
                ui.home_screen(username, points, is_reg, theme)
            ])
            return

        if normalized in ("العاب", "games"):
            safe_reply(line_api, event.reply_token, [
                ui.games_menu(theme)
            ])
            return

        if normalized in ("مساعدة", "help"):
            safe_reply(line_api, event.reply_token, [
                ui.help_screen(theme)
            ])
            return

        if normalized in ("نقاط", "points"):
            safe_reply(line_api, event.reply_token, [
                ui.points_screen(username, points, is_reg, theme)
            ])
            return

        if normalized in ("انضم", "join"):
            if is_reg:
                safe_reply(line_api, event.reply_token, [
                    TextMessage(text="انت مسجل بالفعل")
                ])
            else:
                pending_registrations[user_id] = datetime.utcnow()
                safe_reply(line_api, event.reply_token, [
                    TextMessage(text="ارسل اسمك للتسجيل")
                ])
            return

        if user_id in pending_registrations:
            if datetime.utcnow() - pending_registrations[user_id] < timedelta(minutes=5):
                name = text[:50].strip()
                if len(name) >= 2:
                    db.update_user(user_id, name=name, is_registered=1)
                    pending_registrations.pop(user_id, None)
                    user_cache.pop(user_id, None)
                    safe_reply(line_api, event.reply_token, [
                        TextMessage(text=f"تم التسجيل: {name}")
                    ])
            return

        if ctx_id in game_mgr.active_games:
            result = game_mgr.process_message(ctx_id, user_id, username, text)
            if result:
                safe_reply(line_api, event.reply_token, [result])
            return

        safe_reply(line_api, event.reply_token, [
            TextMessage(text="ارسل 'بداية' للقائمة الرئيسية")
        ])

    except Exception:
        logger.exception("Async processing error")

# -------------------------------------------------
# Routes
# -------------------------------------------------

@app.route("/", methods=["GET"])
def home():
    stats = db.get_stats()
    active = len(game_mgr.active_games)
    return f"BotMesh | Active games: {active} | Users: {stats.get('total_users', 0)}"


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "time": datetime.utcnow().isoformat()
    })


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

# -------------------------------------------------
# LINE Handler
# -------------------------------------------------

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        line_api = MessagingApi(api_client)
        threading.Thread(
            target=process_message_async,
            args=(event, line_api),
            daemon=True
        ).start()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=Config.get_port(), threaded=True)
