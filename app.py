# ========================================
# app.py
# ========================================

import os
import logging
from datetime import datetime

from flask import Flask, request, abort

from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
    FlexMessage,
    FlexContainer,
    QuickReply,
    QuickReplyItem,
    MessageAction
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent

from apscheduler.schedulers.background import BackgroundScheduler

from database import Database
from game_engine import GameEngine
from ui_builder import UIBuilder
from config import Config

# ----------------------------------------
# Logging
# ----------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# ----------------------------------------
# Flask
# ----------------------------------------
app = Flask(__name__)

# ----------------------------------------
# Config validation
# ----------------------------------------
Config.validate()

# ----------------------------------------
# LINE SDK
# ----------------------------------------
configuration = Configuration(access_token=Config.LINE_ACCESS_TOKEN)
api_client = ApiClient(configuration)
api_instance = MessagingApi(api_client)

handler = WebhookHandler(Config.LINE_SECRET)

# ----------------------------------------
# Core components
# ----------------------------------------
Database.init()
ui_builder = UIBuilder()

# ----------------------------------------
# Scheduler (مقبول مؤقتاً مع workers=1)
# ----------------------------------------
scheduler = BackgroundScheduler(timezone="UTC")

def start_scheduler():
    scheduler.add_job(
        Database.cleanup_inactive_users,
        trigger="interval",
        hours=24,
        id="cleanup_users",
        replace_existing=True
    )
    scheduler.start()
    logger.info("Scheduler started")

if os.environ.get("RUN_SCHEDULER", "1") == "1":
    start_scheduler()

# ----------------------------------------
# User themes
# ----------------------------------------
user_themes = {}

def get_user_theme(user_id: str) -> str:
    return user_themes.get(user_id, Config.DEFAULT_THEME)

def set_user_theme(user_id: str, theme: str) -> bool:
    if Config.is_valid_theme(theme):
        user_themes[user_id] = theme
        return True
    return False

# ----------------------------------------
# Game engines (per user)
# ----------------------------------------
game_engines = {}

def get_game_engine(user_id: str) -> GameEngine:
    if user_id not in game_engines:
        game_engines[user_id] = GameEngine(api_instance, Database)
    return game_engines[user_id]

# ----------------------------------------
# Quick Reply
# ----------------------------------------
def create_quick_reply() -> QuickReply:
    return QuickReply(items=[
        QuickReplyItem(action=MessageAction(label="بداية", text="بداية")),
        QuickReplyItem(action=MessageAction(label="العاب", text="العاب")),
        QuickReplyItem(action=MessageAction(label="نقاطي", text="نقاطي")),
        QuickReplyItem(action=MessageAction(label="الصدارة", text="الصدارة")),
        QuickReplyItem(action=MessageAction(label="مساعدة", text="مساعدة")),
    ])

# ----------------------------------------
# Routes
# ----------------------------------------
@app.route("/", methods=["GET"])
def index():
    return {
        "bot": Config.BOT_NAME,
        "version": Config.VERSION,
        "status": "running"
    }, 200

@app.route("/health", methods=["GET"])
def health():
    return {
        "status": "healthy",
        "time": datetime.utcnow().isoformat()
    }, 200

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        logger.error("Invalid LINE signature")
        abort(400)
    except Exception as e:
        logger.error(f"Callback error: {e}", exc_info=True)

    return "OK", 200

# ----------------------------------------
# Message handler (متزامن 100%)
# ----------------------------------------
@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    try:
        text = event.message.text.strip()
        user_id = event.source.user_id

        Database.update_last_activity(user_id)

        response = process_command(text, user_id)

        if isinstance(response, list):
            messages = [convert_to_message(r) for r in response]
        else:
            messages = [convert_to_message(response)]

        messages[-1].quick_reply = create_quick_reply()

        api_instance.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=messages
            )
        )

    except Exception as e:
        logger.error(f"Message handling error: {e}", exc_info=True)
        try:
            api_instance.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text="حدث خطأ، حاول لاحقاً")]
                )
            )
        except Exception:
            pass

# ----------------------------------------
# Helpers
# ----------------------------------------
def convert_to_message(response):
    if isinstance(response, dict):
        return FlexMessage(
            alt_text=Config.BOT_NAME,
            contents=FlexContainer.from_dict(response)
        )
    if isinstance(response, TextMessage):
        return response
    if isinstance(response, str):
        return TextMessage(text=response)
    return TextMessage(text=str(response))

# ----------------------------------------
# Command processing
# ----------------------------------------
def process_command(text: str, user_id: str):
    text_n = text.lower().strip()

    user = Database.get_user_stats(user_id)
    registered = user is not None
    name = user["display_name"] if user else "مستخدم"
    theme = get_user_theme(user_id)

    game_engine = get_game_engine(user_id)

    if game_engine.is_waiting_for_name(user_id):
        return handle_registration_name(text, user_id, game_engine)

    if text_n in ("بداية", "start"):
        return ui_builder.welcome_card(name, registered, theme)

    if text_n in ("العاب", "الالعاب"):
        return ui_builder.games_menu_card(theme)

    if text_n in ("نقاطي", "احصائياتي"):
        if not registered:
            return "يجب التسجيل أولاً\nاكتب: تسجيل"
        return ui_builder.stats_card(name, user, theme)

    if text_n in ("الصدارة",):
        leaders = Database.get_leaderboard()
        return ui_builder.leaderboard_card(leaders, theme)

    if text_n in ("مساعدة", "help"):
        return ui_builder.help_card(theme)

    if text_n in ("ثيم فاتح", "فاتح"):
        set_user_theme(user_id, "light")
        return "تم التغيير للثيم الفاتح"

    if text_n in ("ثيم داكن", "داكن"):
        set_user_theme(user_id, "dark")
        return "تم التغيير للثيم الداكن"

    if text_n == "تسجيل":
        if registered:
            return "أنت مسجل بالفعل"
        game_engine.set_waiting_for_name(user_id, True)
        return "اكتب اسمك للتسجيل:"

    if text_n == "ايقاف":
        if game_engine.stop_game(user_id):
            return "تم إيقاف اللعبة"
        return "لا توجد لعبة نشطة"

    response = game_engine.process_message(
        text=text,
        user_id=user_id,
        session_id=user_id,
        display_name=name,
        registered=registered
    )

    if response:
        return response

    return "أمر غير معروف\nاكتب: مساعدة"

def handle_registration_name(text: str, user_id: str, game_engine):
    name = text.strip()

    if len(name) < 2:
        return "الاسم قصير جداً"
    if len(name) > 20:
        return "الاسم طويل جداً"

    if Database.register_or_update_user(user_id, name):
        game_engine.set_waiting_for_name(user_id, False)
        return f"تم التسجيل بنجاح\nالاسم: {name}"

    return "حدث خطأ في التسجيل"

# ----------------------------------------
# Run (Local only)
# ----------------------------------------
if __name__ == "__main__":
    port = Config.get_port()
    app.run(host="0.0.0.0", port=port)
