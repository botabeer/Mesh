import os
import time
import logging
from threading import Thread, Lock
from queue import Queue, Empty
from datetime import datetime
from collections import defaultdict, deque

from flask import Flask, request, abort, jsonify
from apscheduler.schedulers.background import BackgroundScheduler

from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.webhooks import MessageEvent, TextMessageContent
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi,
    PushMessageRequest, TextMessage, FlexMessage, FlexContainer
)

from config import Config
from database import Database
from game_engine import GameEngine
from ui_builder import UIBuilder

# --------------------------------------------------
# Logging
# --------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# --------------------------------------------------
# App
# --------------------------------------------------
app = Flask(__name__)

# --------------------------------------------------
# Validate ENV
# --------------------------------------------------
Config.validate()

configuration = Configuration(access_token=Config.LINE_ACCESS_TOKEN)
handler = WebhookHandler(Config.LINE_SECRET)

# --------------------------------------------------
# Init core services
# --------------------------------------------------
Database.init()
ui_builder = UIBuilder()
game_engine = GameEngine(configuration, Database)

# --------------------------------------------------
# Queue + Workers
# --------------------------------------------------
task_queue = Queue(maxsize=1000)

def worker():
    while True:
        try:
            job = task_queue.get(timeout=1)
            job()
            task_queue.task_done()
        except Empty:
            continue
        except Exception as e:
            logger.exception(f"Worker crash: {e}")

for _ in range(4):
    Thread(target=worker, daemon=True).start()

# --------------------------------------------------
# Rate Limit
# --------------------------------------------------
_rate_lock = Lock()
_requests = defaultdict(lambda: deque())

def is_rate_limited(user_id: str) -> bool:
    now = time.time()
    with _rate_lock:
        q = _requests[user_id]
        while q and now - q[0] > Config.RATE_LIMIT_WINDOW:
            q.popleft()
        if len(q) >= Config.RATE_LIMIT_MESSAGES:
            return True
        q.append(now)
        return False

# --------------------------------------------------
# Scheduler
# --------------------------------------------------
scheduler = BackgroundScheduler()
scheduler.add_job(
    Database.cleanup_inactive_users,
    trigger="interval",
    hours=24,
    id="cleanup"
)
scheduler.start()

# --------------------------------------------------
# Webhook
# --------------------------------------------------
@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    except Exception as e:
        logger.exception(f"Webhook error: {e}")

    return jsonify({"status": "ok"}), 200

# --------------------------------------------------
# Message Handler (FAST)
# --------------------------------------------------
@handler.add(MessageEvent, message=TextMessageContent)
def on_message(event: MessageEvent):
    user_id = event.source.user_id

    if is_rate_limited(user_id):
        logger.warning(f"Rate limit: {user_id}")
        return

    try:
        task_queue.put_nowait(lambda: process_event(event))
    except Exception:
        logger.error("Queue full – dropped message")

# --------------------------------------------------
# Message Processing (ASYNC)
# --------------------------------------------------
def process_event(event: MessageEvent):
    try:
        user_id = event.source.user_id
        text = event.message.text.strip()

        Database.update_last_activity(user_id)

        user_data = Database.get_user_stats(user_id)
        is_registered = user_data is not None
        display_name = user_data["display_name"] if user_data else "مستخدم"

        theme = Database.get_user_theme(user_id)
        ui_builder.theme = theme

        response = handle_command(
            text=text,
            user_id=user_id,
            user_data=user_data,
            is_registered=is_registered,
            display_name=display_name,
            theme=theme
        )

        if response:
            push(user_id, response)

    except Exception as e:
        logger.exception(f"Process error: {e}")

# --------------------------------------------------
# Command Router
# --------------------------------------------------
def handle_command(text, user_id, user_data, is_registered, display_name, theme):
    normalized = Config.normalize(text)
    cmd = Config.resolve_command(normalized)

    # ---- Name input
    if game_engine.is_waiting_for_name(user_id):
        name = text[:50]
        if len(name) >= 2:
            Database.register_or_update_user(user_id, name)
            game_engine.set_waiting_for_name(user_id, False)
            return flex(ui_builder.welcome_card(name, True), "تم التسجيل")
        return TextMessage(text="الاسم يجب أن يكون حرفين على الأقل")

    # ---- Theme
    if cmd == "تغيير_الثيم":
        new_theme = Database.toggle_user_theme(user_id)
        ui_builder.theme = new_theme
        return flex(
            ui_builder.welcome_card(display_name, is_registered),
            "تم تغيير الثيم"
        )

    # ---- System
    if cmd == "بداية":
        return flex(ui_builder.welcome_card(display_name, is_registered), "القائمة")

    if cmd == "مساعدة":
        return flex(ui_builder.help_card(), "المساعدة")

    if cmd == "العاب":
        return flex(ui_builder.games_menu_card(), "الألعاب")

    if cmd == "نقاطي":
        if not is_registered:
            return TextMessage(text="سجّل أولاً")
        return flex(ui_builder.stats_card(display_name, user_data), "إحصائياتك")

    if cmd == "الصدارة":
        leaders = Database.get_leaderboard()
        return flex(ui_builder.leaderboard_card(leaders), "الصدارة")

    if cmd == "ايقاف":
        stopped = game_engine.stop_game(user_id)
        return TextMessage(text="تم إيقاف اللعبة" if stopped else "لا توجد لعبة")

    # ---- Registration
    if cmd in ["تسجيل", "تغيير"]:
        if game_engine.is_game_active(user_id):
            return TextMessage(text="أوقف اللعبة أولاً")
        game_engine.set_waiting_for_name(user_id, True)
        return TextMessage(text="اكتب اسمك:")

    # ---- Games (Sandboxed)
    if game_engine.handle(user_id, cmd, theme):
        return None

    return TextMessage(text="اكتب (بداية) لعرض القائمة")

# --------------------------------------------------
# Push helper
# --------------------------------------------------
def push(user_id: str, message):
    try:
        with ApiClient(configuration) as api_client:
            api = MessagingApi(api_client)
            if not isinstance(message, list):
                message = [message]
            api.push_message(PushMessageRequest(
                to=user_id,
                messages=message
            ))
    except Exception as e:
        logger.exception(f"Push error: {e}")

def flex(card, alt):
    try:
        return FlexMessage(
            alt_text=alt,
            contents=FlexContainer.from_dict(card)
        )
    except Exception:
        return TextMessage(text="حدث خطأ")

# --------------------------------------------------
# Health
# --------------------------------------------------
@app.route("/health")
def health():
    return {
        "status": "ok",
        "queue": task_queue.qsize(),
        "active_games": game_engine.get_active_games_count(),
        "time": datetime.utcnow().isoformat()
    }

@app.route("/")
def index():
    return {"name": Config.BOT_NAME, "version": Config.VERSION}

# --------------------------------------------------
# Run
# --------------------------------------------------
if __name__ == "__main__":
    logger.info(f"Starting {Config.BOT_NAME} v{Config.VERSION}")
    app.run(host="0.0.0.0", port=Config.get_port())
