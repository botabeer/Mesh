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

# ===============================
# Logging
# ===============================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)

# ===============================
# Flask
# ===============================
app = Flask(__name__)

# ===============================
# LINE
# ===============================
line_config = Configuration(access_token=Config.LINE_TOKEN)
handler = WebhookHandler(Config.LINE_SECRET)

# ===============================
# Core
# ===============================
db = Database()
game_mgr = GameManager(db)
text_mgr = TextManager()

executor = ThreadPoolExecutor(
    max_workers=Config.WORKERS,
    thread_name_prefix="worker"
)

# ===============================
# Helpers
# ===============================
def reply_message(reply_token: str, messages):
    if not messages:
        return

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
        logger.info("✓ Message sent successfully")
    except Exception as e:
        logger.error(f"✗ Reply error: {e}")

# ===============================
# Message Processor
# ===============================
def process_message(user_id: str, text: str, reply_token: str):
    try:
        logger.info(f"Processing message from {user_id}: {text}")
        
        cmd = Config.normalize(text)
        if not cmd:
            logger.warning("Empty command after normalization")
            return

        logger.info(f"Normalized command: '{cmd}'")
        
        db.update_activity(user_id)
        user = db.get_user(user_id)
        theme = db.get_theme(user_id) if user else "light"
        ui = UI(theme=theme)

        # ===============================
        # Global Commands
        # ===============================
        if cmd in ("بداية", "بدايه"):
            logger.info("Main menu command")
            reply_message(reply_token, ui.main_menu(user))
            return

        if cmd in ("مساعدة", "مساعده"):
            logger.info("Help menu command")
            reply_message(reply_token, ui.help_menu())
            return

        if cmd in ("الصدارة", "الصداره"):
            logger.info("Leaderboard command")
            reply_message(
                reply_token,
                ui.leaderboard_card(db.get_leaderboard())
            )
            return

        # ===============================
        # Theme
        # ===============================
        if cmd in ("تغيير الثيم", "تغيير_الثيم") and user:
            logger.info("Theme toggle command")
            new_theme = db.toggle_theme(user_id)
            reply_message(
                reply_token,
                UI(theme=new_theme).main_menu(user)
            )
            return

        # ===============================
        # Static Texts
        # ===============================
        text_response = text_mgr.handle(cmd, theme)
        if text_response:
            logger.info("Static text response")
            reply_message(reply_token, text_response)
            return

        # ===============================
        # Registration
        # ===============================
        if not user:
            logger.info(f"Unregistered user: {user_id}")
            if cmd == "تسجيل":
                logger.info("Registration command")
                db.set_waiting_name(user_id, True)
                reply_message(reply_token, ui.ask_name())
                return
            else:
                # إرسال رسالة للتسجيل
                logger.info("Sending registration prompt")
                reply_message(reply_token, ui.main_menu(None))
                return

        if db.is_waiting_name(user_id):
            logger.info("User is waiting to submit name")
            name = text.strip()[:Config.MAX_NAME_LENGTH]
            if len(name) >= Config.MIN_NAME_LENGTH:
                logger.info(f"Registering user with name: {name}")
                db.register_user(user_id, name)
                db.set_waiting_name(user_id, False)
                reply_message(
                    reply_token,
                    ui.main_menu(db.get_user(user_id))
                )
            else:
                logger.warning(f"Name too short: {len(name)} chars")
            return

        # ===============================
        # User Commands
        # ===============================
        if cmd in ("العاب", "الالعاب"):
            logger.info("Games menu command")
            reply_message(reply_token, ui.games_menu())
            return

        if cmd == "نقاطي":
            logger.info("Stats command")
            reply_message(reply_token, ui.stats_card(user))
            return

        if cmd == "انسحب":
            logger.info("Quit game command")
            if game_mgr.stop_game(user_id):
                reply_message(reply_token, ui.game_stopped())
            return

        # ===============================
        # Games
        # ===============================
        logger.info(f"Checking if '{cmd}' is a game command")
        game_response = game_mgr.handle(
            user_id=user_id,
            cmd=cmd,
            theme=theme,
            raw_text=text
        )

        if game_response:
            logger.info("Game response generated")
            reply_message(reply_token, game_response)
        else:
            logger.warning(f"No handler found for command: '{cmd}'")
            # إرسال القائمة الرئيسية كـ fallback
            reply_message(reply_token, ui.main_menu(user))

    except Exception as e:
        logger.exception(f"✗ Processing error ({user_id}): {e}")
        # إرسال رسالة خطأ للمستخدم
        try:
            ui = UI()
            reply_message(reply_token, ui.main_menu(db.get_user(user_id)))
        except:
            pass

# ===============================
# Webhook Handler
# ===============================
@handler.add(MessageEvent, message=TextMessageContent)
def on_message(event: MessageEvent):
    user_id = event.source.user_id
    text = event.message.text
    reply_token = event.reply_token

    logger.info(f"Received message from {user_id}: {text}")

    # تنفيذ غير متزامن
    executor.submit(process_message, user_id, text, reply_token)

# ===============================
# Routes
# ===============================
@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)

    logger.info(f"Webhook received: {len(body)} bytes")

    try:
        handler.handle(body, signature)
        logger.info("✓ Webhook handled successfully")
    except InvalidSignatureError:
        logger.error("✗ Invalid signature")
        abort(400)
    except Exception as e:
        logger.error(f"✗ Webhook error: {e}")

    # رد فوري لتفادي timeout
    return "OK", 200

@app.route("/health")
def health():
    active_games = game_mgr.count_active()
    logger.info(f"Health check: {active_games} active games")
    
    return jsonify({
        "status": "ok",
        "time": datetime.utcnow().isoformat(),
        "active_games": active_games
    })

@app.route("/")
def index():
    return jsonify({
        "name": Config.BOT_NAME,
        "version": Config.VERSION,
        "status": "running",
        "copyright": Config.COPYRIGHT
    })

# ===============================
# Entry
# ===============================
if __name__ == "__main__":
    logger.info(f"Starting {Config.BOT_NAME} v{Config.VERSION}")
    logger.info(f"Available games: {game_mgr._games.keys()}")
    app.run(
        host="0.0.0.0",
        port=Config.PORT,
        threaded=True
    )
