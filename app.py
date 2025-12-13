import os
import logging
import atexit
from datetime import datetime
from threading import Thread
from queue import Queue, Empty

from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage,
    FlexSendMessage,
    QuickReply,
    QuickReplyButton,
    MessageAction
)

from apscheduler.schedulers.background import BackgroundScheduler

from database import Database
from game_engine import GameEngine
from ui_builder import UIBuilder

# --------------------------------------------------
# Logging
# --------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# --------------------------------------------------
# App
# --------------------------------------------------
app = Flask(__name__)

# --------------------------------------------------
# Env validation
# --------------------------------------------------
for var in ("LINE_CHANNEL_ACCESS_TOKEN", "LINE_CHANNEL_SECRET"):
    if not os.getenv(var):
        raise RuntimeError(f"Missing environment variable: {var}")

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

# --------------------------------------------------
# Init core
# --------------------------------------------------
Database.init()
ui_builder = UIBuilder()
game_engine = GameEngine(line_bot_api, Database)

# --------------------------------------------------
# Background worker (safe async)
# --------------------------------------------------
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
            logger.error("Background task error", exc_info=e)

for _ in range(2):
    Thread(target=background_worker, daemon=True).start()

# --------------------------------------------------
# Scheduler (SAFE with gunicorn)
# --------------------------------------------------
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

# --------------------------------------------------
# Helpers
# --------------------------------------------------
def normalize_message(msg):
    if msg is None:
        return TextSendMessage(text="اكتب: بداية")
    if isinstance(msg, dict):
        return FlexSendMessage(alt_text="Bot", contents=msg)
    return msg

def attach_quick_reply(msg):
    quick_reply = QuickReply(items=[
        QuickReplyButton(action=MessageAction(label="بداية", text="بداية")),
        QuickReplyButton(action=MessageAction(label="العاب", text="العاب")),
        QuickReplyButton(action=MessageAction(label="نقاطي", text="نقاطي")),
        QuickReplyButton(action=MessageAction(label="الصدارة", text="الصدارة")),
        QuickReplyButton(action=MessageAction(label="ايقاف", text="ايقاف")),
    ])
    if hasattr(msg, "quick_reply"):
        msg.quick_reply = quick_reply
    return msg

# --------------------------------------------------
# Routes
# --------------------------------------------------
@app.route("/", methods=["GET"])
def index():
    return {"status": "running"}, 200

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
    except Exception as e:
        logger.error("Callback error", exc_info=e)
    return "OK", 200

# --------------------------------------------------
# LINE handler
# --------------------------------------------------
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    def process():
        try:
            text = event.message.text.strip()
            user_id = event.source.user_id
            group_id = getattr(event.source, "group_id", user_id)

            Database.update_last_activity(user_id)

            response = process_command(text, user_id, group_id)

            if isinstance(response, list):
                messages = []
                for msg in response:
                    msg = normalize_message(msg)
                    attach_quick_reply(msg)
                    messages.append(msg)
                line_bot_api.reply_message(event.reply_token, messages)
            else:
                msg = normalize_message(response)
                attach_quick_reply(msg)
                line_bot_api.reply_message(event.reply_token, msg)

        except Exception as e:
            logger.error("Message error", exc_info=e)
            try:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text="حدث خطأ، حاول لاحقًا")
                )
            except Exception:
                pass

    task_queue.put(process)

# --------------------------------------------------
# Commands
# --------------------------------------------------
def process_command(text, user_id, group_id):
    text_n = text.strip().lower()
    user = Database.get_user_stats(user_id)
    registered = user is not None
    name = user["display_name"] if user else "مستخدم"

    if text_n in ("بداية", "start"):
        return ui_builder.welcome_card(name, registered)

    if text_n == "العاب":
        return ui_builder.games_menu_card()

    if text_n == "نقاطي":
        if not registered:
            return TextSendMessage(text="يجب التسجيل أولاً")
        return ui_builder.stats_card(name, user)

    if text_n == "الصدارة":
        leaders = Database.get_leaderboard()
        return ui_builder.leaderboard_card(leaders)

    if text_n == "تسجيل":
        game_engine.set_waiting_for_name(user_id, True)
        return TextSendMessage(text="اكتب اسمك للتسجيل:")

    if text_n == "ايقاف":
        return TextSendMessage(
            text="تم إيقاف اللعبة" if game_engine.stop_game(group_id)
            else "لا توجد لعبة نشطة"
        )

    return game_engine.process_message(
        text=text,
        user_id=user_id,
        group_id=group_id,
        display_name=name,
        is_registered=registered
    )

# --------------------------------------------------
# Local run
# --------------------------------------------------
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
