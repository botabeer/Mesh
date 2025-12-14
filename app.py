# ========================================
# app.py
# ========================================

import os
import logging
import atexit
from datetime import datetime
from threading import Thread
from queue import Queue, Empty

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

from config import Config
from database import Database
from game_engine import GameEngine
from ui_builder import UIBuilder

# ----------------------------------------
# Logging
# ----------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
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
handler = WebhookHandler(Config.LINE_SECRET)

# ----------------------------------------
# Core components
# ----------------------------------------
Database.init()
ui_builder = UIBuilder()

api_client = ApiClient(configuration)
messaging_api = MessagingApi(api_client)

game_engine = GameEngine(messaging_api, Database)

# ----------------------------------------
# Task Queue (Anti-timeout)
# ----------------------------------------
task_queue = Queue()

def background_worker():
    while True:
        try:
            task = task_queue.get(timeout=1)
            if task is None:
                break
            task()
            task_queue.task_done()
        except Empty:
            continue
        except Exception as e:
            logger.error("Background error", exc_info=True)

for _ in range(2):
    Thread(target=background_worker, daemon=True).start()

# ----------------------------------------
# Scheduler (only one worker)
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

if os.environ.get("GUNICORN_WORKER_ID") in (None, "0"):
    start_scheduler()
    atexit.register(lambda: scheduler.shutdown(wait=False))

# ----------------------------------------
# User themes (memory cache)
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
# Quick Reply
# ----------------------------------------
def build_quick_reply() -> QuickReply:
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
        abort(400)
    except Exception:
        logger.error("Callback error", exc_info=True)

    return "OK", 200

# ----------------------------------------
# Message Handler
# ----------------------------------------
@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    def process():
        try:
            text = event.message.text.strip()
            user_id = event.source.user_id

            Database.update_last_activity(user_id)

            response = process_command(text, user_id)

            messages = []

            if isinstance(response, list):
                for msg in response:
                    messages.append(prepare_message(msg))
            else:
                messages.append(prepare_message(response))

            messaging_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=messages
                )
            )

        except Exception:
            logger.error("Message handling error", exc_info=True)
            try:
                messaging_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[TextMessage(text="حدث خطأ، حاول لاحقاً")]
                    )
                )
            except Exception:
                pass

    task_queue.put(process)

def prepare_message(msg):
    qr = build_quick_reply()

    if isinstance(msg, dict):
        flex = FlexMessage(
            alt_text=Config.BOT_NAME,
            contents=FlexContainer.from_dict(msg)
        )
        flex.quick_reply = qr
        return flex

    msg.quick_reply = qr
    return msg

# ----------------------------------------
# Command Processor
# ----------------------------------------
def process_command(text: str, user_id: str):
    text_n = text.lower()
    user = Database.get_user_stats(user_id)
    registered = user is not None
    name = user["display_name"] if user else "مستخدم"
    theme = get_user_theme(user_id)

    if text_n in ("بداية", "start"):
        return ui_builder.welcome_card(name, registered, theme)

    if text_n in ("العاب",):
        return ui_builder.games_menu_card(theme)

    if text_n in ("نقاطي",):
        if not registered:
            return TextMessage(text="يجب التسجيل أولاً\nاكتب: تسجيل")
        return ui_builder.stats_card(name, user, theme)

    if text_n in ("الصدارة",):
        return ui_builder.leaderboard_card(
            Database.get_leaderboard(),
            theme
        )

    if text_n in ("مساعدة",):
        return ui_builder.help_card(theme)

    if text_n == "تسجيل":
        if registered:
            return TextMessage(text="أنت مسجل بالفعل")
        game_engine.set_waiting_for_name(user_id, True)
        return TextMessage(text="اكتب اسمك للتسجيل:")

    if text_n == "ايقاف":
        return TextMessage(
            text="تم إيقاف اللعبة"
            if game_engine.stop_game(user_id)
            else "لا توجد لعبة نشطة"
        )

    return game_engine.process_message(
        text, user_id, user_id, name, registered
    ) or TextMessage(text="أمر غير معروف\nاكتب: مساعدة")

# ----------------------------------------
# Local run
# ----------------------------------------
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=Config.get_port(),
        debug=False
    )
