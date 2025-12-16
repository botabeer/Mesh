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

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)

# Flask
app = Flask(__name__)

# LINE
line_config = Configuration(access_token=Config.LINE_TOKEN)
handler = WebhookHandler(Config.LINE_SECRET)

# Core
db = Database()
game_mgr = GameManager(db)
text_mgr = TextManager()

executor = ThreadPoolExecutor(
    max_workers=Config.WORKERS,
    thread_name_prefix="worker"
)

# Helpers
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
        logger.info("Message sent successfully")
    except Exception as e:
        logger.error(f"Reply error: {e}")

# Message Processor
def process_message(user_id: str, text: str, reply_token: str):
    try:
        logger.info(f"Processing: {user_id} -> {text}")
        
        cmd = Config.normalize(text)
        if not cmd:
            logger.warning("Empty command")
            return

        logger.info(f"Normalized: '{cmd}'")
        
        db.update_activity(user_id)
        user = db.get_user(user_id)
        theme = db.get_theme(user_id) if user else "light"
        ui = UI(theme=theme)

        # ========================================
        # PRIORITY 1: Global Commands (Always Work)
        # ========================================
        if cmd in ("بدايه", "بداية"):
            logger.info("Main menu")
            reply_message(reply_token, ui.main_menu(user))
            return

        if cmd in ("مساعده", "مساعدة"):
            logger.info("Help menu")
            reply_message(reply_token, ui.help_menu())
            return

        # ========================================
        # PRIORITY 2: Registration State
        # ========================================
        if db.is_waiting_name(user_id):
            logger.info("User waiting for name")
            
            # تجاهل الأوامر المحجوزة
            if cmd in Config.RESERVED_COMMANDS:
                logger.warning(f"Reserved command ignored: {cmd}")
                reply_message(reply_token, ui.ask_name_invalid())
                return
            
            # قبول الاسم
            name = text.strip()[:Config.MAX_NAME_LENGTH]
            if len(name) >= Config.MIN_NAME_LENGTH:
                logger.info(f"Registering: {name}")
                success = db.register_user(user_id, name)
                db.set_waiting_name(user_id, False)
                
                if success:
                    user = db.get_user(user_id)
                    reply_message(reply_token, ui.main_menu(user))
                else:
                    reply_message(reply_token, ui.ask_name())
            else:
                logger.warning(f"Name too short: {len(name)}")
                reply_message(reply_token, ui.ask_name())
            return

        # تغيير الاسم (حالة انتظار)
        if db.is_changing_name(user_id):
            logger.info("User changing name")
            
            if cmd in Config.RESERVED_COMMANDS:
                logger.warning(f"Reserved command ignored: {cmd}")
                reply_message(reply_token, ui.ask_new_name_invalid())
                return
            
            name = text.strip()[:Config.MAX_NAME_LENGTH]
            if len(name) >= Config.MIN_NAME_LENGTH:
                logger.info(f"Changing name to: {name}")
                success = db.change_name(user_id, name)
                db.set_changing_name(user_id, False)
                
                if success:
                    user = db.get_user(user_id)
                    reply_message(reply_token, ui.main_menu(user))
                else:
                    reply_message(reply_token, ui.ask_new_name())
            else:
                reply_message(reply_token, ui.ask_new_name())
            return

        # ========================================
        # PRIORITY 3: Unregistered Users
        # ========================================
        if not user:
            logger.info("Unregistered user")
            if cmd == "تسجيل":
                db.set_waiting_name(user_id, True)
                reply_message(reply_token, ui.ask_name())
            else:
                reply_message(reply_token, ui.registration_required())
            return

        # ========================================
        # PRIORITY 4: User Commands (Registered)
        # ========================================
        
        # Theme
        if cmd == "ثيم":
            logger.info("Theme toggle")
            new_theme = db.toggle_theme(user_id)
            user = db.get_user(user_id)
            reply_message(reply_token, UI(theme=new_theme).main_menu(user))
            return

        # Stats
        if cmd == "نقاطي":
            logger.info("Stats")
            reply_message(reply_token, ui.stats_card(user))
            return

        # Leaderboard
        if cmd in ("الصداره", "الصدارة"):
            logger.info("Leaderboard")
            reply_message(reply_token, ui.leaderboard_card(db.get_leaderboard()))
            return

        # Games Menu
        if cmd == "العاب":
            logger.info("Games menu")
            reply_message(reply_token, ui.games_menu())
            return

        # Change Name
        if cmd in ("تغيير الاسم", "تغيير اسمي"):
            logger.info("Change name request")
            db.set_changing_name(user_id, True)
            reply_message(reply_token, ui.ask_new_name())
            return

        # Quit Game
        if cmd == "انسحب":
            logger.info("Quit game")
            if game_mgr.stop_game(user_id):
                reply_message(reply_token, ui.game_stopped())
            else:
                # لا توجد لعبة نشطة - تجاهل
                logger.info("No active game to quit")
            return

        # Stop Game (إيقاف)
        if cmd in ("ايقاف", "ايقاف اللعبة"):
            logger.info("Stop game")
            if game_mgr.stop_game(user_id):
                reply_message(reply_token, ui.game_stopped())
            else:
                logger.info("No active game to stop")
            return

        # ========================================
        # PRIORITY 5: Static Text
        # ========================================
        text_response = text_mgr.handle(cmd, theme)
        if text_response:
            logger.info("Static text")
            reply_message(reply_token, text_response)
            return

        # ========================================
        # PRIORITY 6: Games
        # ========================================
        game_response = game_mgr.handle(
            user_id=user_id,
            cmd=cmd,
            theme=theme,
            raw_text=text
        )

        if game_response:
            logger.info("Game response")
            reply_message(reply_token, game_response)
        else:
            # Fallback: تجاهل الرسالة بصمت أو عرض القائمة
            logger.info("Unknown command - showing main menu")
            reply_message(reply_token, ui.main_menu(user))

    except Exception as e:
        logger.exception(f"Processing error: {e}")
        try:
            ui = UI()
            reply_message(reply_token, ui.main_menu(db.get_user(user_id)))
        except:
            pass

# Webhook Handler
@handler.add(MessageEvent, message=TextMessageContent)
def on_message(event: MessageEvent):
    user_id = event.source.user_id
    text = event.message.text
    reply_token = event.reply_token

    logger.info(f"Received: {user_id} -> {text}")
    executor.submit(process_message, user_id, text, reply_token)

# Routes
@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)

    logger.info(f"Webhook: {len(body)} bytes")

    try:
        handler.handle(body, signature)
        logger.info("Webhook handled")
    except InvalidSignatureError:
        logger.error("Invalid signature")
        abort(400)
    except Exception as e:
        logger.error(f"Webhook error: {e}")

    return "OK", 200

@app.route("/health")
def health():
    active_games = game_mgr.count_active()
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
        "status": "running"
    })

# Entry
if __name__ == "__main__":
    logger.info(f"Starting {Config.BOT_NAME} v{Config.VERSION}")
    logger.info(f"Games: {list(game_mgr._games.keys())}")
    
    from apscheduler.schedulers.background import BackgroundScheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        func=db.cleanup_memory,
        trigger="interval",
        minutes=30,
        id="cleanup"
    )
    scheduler.start()
    logger.info("Scheduler started")
    
    try:
        app.run(
            host="0.0.0.0",
            port=Config.PORT,
            threaded=True
        )
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        logger.info("Shutdown complete")
