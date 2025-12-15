import os
import logging
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from flask import Flask, request, jsonify, abort
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.webhooks import MessageEvent, TextMessageContent
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi,
    ReplyMessageRequest
)

from config import Config
from database import Database
from game_manager import GameManager
from text_manager import TextManager
from ui import UI

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

line_config = Configuration(access_token=Config.LINE_TOKEN)
handler = WebhookHandler(Config.LINE_SECRET)

db = Database()
game_mgr = GameManager(db)
text_mgr = TextManager()

executor = ThreadPoolExecutor(
    max_workers=Config.WORKERS,
    thread_name_prefix="worker"
)

def reply_message(reply_token: str, messages):
    if not isinstance(messages, list):
        messages = [messages]
    try:
        with ApiClient(line_config) as client:
            MessagingApi(client).reply_message(
                ReplyMessageRequest(
                    reply_token=reply_token,
                    messages=messages
                )
            )
    except Exception as e:
        logger.error(f"Reply error: {e}")

def process_message(user_id: str, text: str, reply_token: str):
    try:
        db.update_activity(user_id)
        user = db.get_user(user_id)
        theme = db.get_theme(user_id) if user else "light"
        ui = UI(theme=theme)
        cmd = Config.normalize(text)

        if cmd in ("بداية", "بدايه"):
            reply_message(reply_token, ui.main_menu(user))
            return
        
        if cmd == "تغيير_الثيم" and user:
            new_theme = db.toggle_theme(user_id)
            reply_message(reply_token, UI(theme=new_theme).main_menu(user))
            return
        
        if cmd in ("مساعدة", "مساعده"):
            reply_message(reply_token, ui.help_menu())
            return

        if cmd in ("الصدارة", "الصداره"):
            reply_message(reply_token, ui.leaderboard_card(db.get_leaderboard()))
            return

        text_response = text_mgr.handle(cmd, theme)
        if text_response:
            reply_message(reply_token, text_response)
            return

        if not user:
            if cmd == "تسجيل":
                db.set_waiting_name(user_id, True)
                reply_message(reply_token, ui.ask_name())
                return
            return

        if db.is_waiting_name(user_id):
            name = text.strip()[:50]
            if len(name) >= 2:
                db.register_user(user_id, name)
                db.set_waiting_name(user_id, False)
                reply_message(reply_token, ui.main_menu(db.get_user(user_id)))
            return

        if cmd in ("العاب", "الالعاب"):
            reply_message(reply_token, ui.games_menu())
            return
        
        if cmd == "نقاطي":
            reply_message(reply_token, ui.stats_card(user))
            return
        
        if cmd == "انسحب":
            stopped = game_mgr.stop_game(user_id)
            if stopped:
                reply_message(reply_token, ui.game_stopped())
            return

        game_response = game_mgr.handle(user_id, cmd, theme, text)
        if game_response:
            reply_message(reply_token, game_response)
            return

    except Exception as e:
        logger.exception(f"Error ({user_id}): {e}")

@handler.add(MessageEvent, message=TextMessageContent)
def on_message(event: MessageEvent):
    user_id = event.source.user_id
    text = event.message.text.strip()
    reply_token = event.reply_token
    executor.submit(process_message, user_id, text, reply_token)

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    except Exception as e:
        logger.error(f"Webhook error: {e}")
    return "OK", 200

@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "time": datetime.utcnow().isoformat(),
        "active_games": game_mgr.count_active()
    })

@app.route("/")
def index():
    return jsonify({
        "name": Config.BOT_NAME,
        "version": Config.VERSION,
        "status": "running",
        "copyright": Config.COPYRIGHT
    })

if __name__ == "__main__":
    logger.info(f"Starting {Config.BOT_NAME} v{Config.VERSION}")
    app.run(host="0.0.0.0", port=Config.PORT)
