"""
Bot Mesh - LINE Bot Application v8.1 MERGED
تم إنشاء هذا البوت بواسطة عبير الدوسري © 2025

✅ Glass iOS Style Design
✅ Auto Name Update from LINE
✅ Complete Theme System
✅ دعم اللعب الفردي + المجموعة تلقائياً
✅ وضع فريقين ديناميكي
✅ تجاهل غير المنضمين
✅ تجاهل رسائل المجموعة غير الخاصة بالأوامر
"""

import os
import sys
import logging
from datetime import datetime, timedelta
from collections import defaultdict

from flask import Flask, request, abort
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi,
    ReplyMessageRequest, QuickReply, QuickReplyItem,
    MessageAction, TextMessage
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent

from constants import (
    BOT_NAME, BOT_VERSION, BOT_RIGHTS,
    LINE_CHANNEL_SECRET, LINE_CHANNEL_ACCESS_TOKEN,
    validate_env, get_username, GAME_LIST,
    DEFAULT_THEME, THEMES,
    RATE_LIMIT_CONFIG, FIXED_GAME_QR, FIXED_ACTIONS
)

from ui_builder import (
    build_enhanced_home,
    build_help_window
)

from database import get_database

# ============================================================================
# Configuration
# ============================================================================
try:
    validate_env()
except ValueError as e:
    print(f"Configuration Error: {e}")
    sys.exit(1)

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

db = get_database()

# ============================================================================
# Runtime Storage
# ============================================================================
active_games = {}              # game_id -> game_instance
team_sessions = {}             # game_id -> {"joined": set(), "team1": [], "team2": []}
user_cache = {}
user_requests = defaultdict(list)

# ============================================================================
# Rate Limiting
# ============================================================================
def is_rate_limited(user_id):
    now = datetime.now()
    cutoff = now - timedelta(seconds=RATE_LIMIT_CONFIG["window_seconds"])
    user_requests[user_id] = [t for t in user_requests[user_id] if t > cutoff]
    if len(user_requests[user_id]) >= RATE_LIMIT_CONFIG["max_requests"]:
        return True
    user_requests[user_id].append(now)
    return False

# ============================================================================
# Helpers
# ============================================================================
def is_group_chat(event):
    return hasattr(event.source, "group_id")

def get_game_id(event):
    return event.source.group_id if is_group_chat(event) else event.source.user_id

def create_games_quick_reply():
    items = [
        QuickReplyItem(
            action=MessageAction(label=btn["label"], text=btn["text"])
        )
        for btn in FIXED_GAME_QR
    ]
    return QuickReply(items=items)

def attach_quick_reply(message):
    message.quick_reply = create_games_quick_reply()
    return message

def send_with_quick_reply(api, token, message):
    message = attach_quick_reply(message)
    api.reply_message_with_http_info(
        ReplyMessageRequest(reply_token=token, messages=[message])
    )

def get_user_data(user_id, username):
    user = db.get_user(user_id)
    if not user:
        db.create_user(user_id, username)
        user = db.get_user(user_id)
    return user

# ============================================================================
# Webhook
# ============================================================================
@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"

# ============================================================================
# Status Page
# ============================================================================
@app.route("/", methods=["GET"])
def home():
    return f"{BOT_NAME} is running ✅"

# ============================================================================
# Message Handler
# ============================================================================
@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    try:
        user_id = event.source.user_id
        game_id = get_game_id(event)
        text = event.message.text.strip()

        if not text:
            return

        if is_rate_limited(user_id):
            return

        with ApiClient(configuration) as api_client:
            api = MessagingApi(api_client)

            # اسم المستخدم
            try:
                profile = api.get_profile(user_id)
                username = get_username(profile)
            except:
                username = "مستخدم"

            user = get_user_data(user_id, username)
            theme = db.get_user_theme(user_id)

            is_group = is_group_chat(event)

            # ===============================
            # تجاهل أي رسالة بالمجموعة ليست أمراً أو لاعباً منضم
            # ===============================
            if is_group:
                allowed_prefix = (
                    [btn["text"] for btn in FIXED_GAME_QR] +
                    ["انضم", "انسحب", "فريقين"]
                )
                if not any(text.startswith(x) for x in allowed_prefix) and game_id not in active_games:
                    return

            reply = None

            # ===============================
            # نافذتي البداية والمساعدة فقط
            # ===============================
            if text in ["بداية", "home", "start"]:
                reply = build_enhanced_home(username, user["points"], user.get("is_registered"), theme)

            elif text in ["مساعدة", "help"]:
                reply = build_help_window(theme)

            # ===============================
            # تفعيل وضع فريقين
            # ===============================
            elif text == "فريقين" and is_group:
                team_sessions[game_id] = {
                    "joined": set(),
                    "team1": [],
                    "team2": []
                }
                reply = TextMessage(text="✅ تم تفعيل وضع فريقين\nاكتب: انضم")

            elif text == "انضم" and is_group and game_id in team_sessions:
                session = team_sessions[game_id]
                session["joined"].add(user_id)
                reply = TextMessage(text=f"✅ {username} انضم")

            elif text == "انسحب" and is_group and game_id in team_sessions:
                session = team_sessions[game_id]
                session["joined"].discard(user_id)
                reply = TextMessage(text=f"✅ {username} انسحب")

            # ===============================
            # بدء التقسيم تلقائياً
            # ===============================
            elif text == "ابدأ" and is_group and game_id in team_sessions:
                session = team_sessions[game_id]
                players = list(session["joined"])
                for i, pid in enumerate(players):
                    if i % 2 == 0:
                        session["team1"].append(pid)
                    else:
                        session["team2"].append(pid)

                reply = TextMessage(
                    text=(
                        f"🟦 الفريق 1: {len(session['team1'])}\n"
                        f"🟥 الفريق 2: {len(session['team2'])}\n"
                        "✅ بدأت المنافسة"
                    )
                )

            # ===============================
            # تشغيل لعبة
            # ===============================
            elif text in GAME_LIST:
                reply = TextMessage(text=f"✅ تم اختيار لعبة: {text}")

            # ===============================
            # إرسال الرد
            # ===============================
            if reply:
                send_with_quick_reply(api, event.reply_token, reply)

    except Exception as e:
        logger.error(f"Handler Error: {e}", exc_info=True)

# ============================================================================
# Run
# ============================================================================
if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    logger.info(f"Starting {BOT_NAME} v{BOT_VERSION}")
    app.run(host="0.0.0.0", port=port, debug=False)
