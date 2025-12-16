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
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
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
    """ارسال رسالة رد"""
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
        logger.info("Message sent")
    except Exception as e:
        logger.error(f"Reply error: {e}")


def process_message(user_id: str, text: str, reply_token: str):
    """معالجة الرسائل الواردة"""
    try:
        logger.info(f"Processing: {user_id} -> {text[:50]}")
        
        cmd = Config.normalize(text)
        if not cmd:
            logger.warning("Empty command")
            return

        db.update_activity(user_id)
        user = db.get_user(user_id)
        is_ignored = db.is_ignored(user_id)
        
        # تجاهل المستخدمين الذين اختاروا انسحب (إلا إذا كتبوا أوامر محددة)
        if is_ignored:
            logger.info(f"Ignored user: {user_id}")
            # فقط نرد على الأوامر الرئيسية
            if cmd not in ("تسجيل", "بدايه", "بداية", "مساعده", "مساعدة"):
                return  # تجاهل تام
            
            # إذا كتب تسجيل، نلغي التجاهل ونبدأ التسجيل
            if cmd == "تسجيل":
                db.set_ignored(user_id, False)
                db.set_waiting_name(user_id, True)
                reply_message(reply_token, UI(theme="light").ask_name())
                return
        
        theme = db.get_theme(user_id) if user else "light"
        ui = UI(theme=theme)

        # أولوية 1: الاوامر العامة
        if cmd in ("بدايه", "بداية"):
            logger.info("Main menu")
            reply_message(reply_token, ui.main_menu(user))
            return

        if cmd in ("مساعده", "مساعدة"):
            logger.info("Help menu")
            reply_message(reply_token, ui.help_menu())
            return

        # أولوية 2: حالات الانتظار
        if db.is_waiting_name(user_id):
            logger.info("Waiting for name")
            
            if cmd in Config.RESERVED_COMMANDS:
                logger.warning(f"Reserved command: {cmd}")
                reply_message(reply_token, ui.ask_name_invalid())
                return
            
            name = text.strip()[:Config.MAX_NAME_LENGTH]
            if Config.validate_name(name):
                logger.info(f"Registering: {name}")
                success = db.register_user(user_id, name)
                db.set_waiting_name(user_id, False)
                
                if success:
                    user = db.get_user(user_id)
                    reply_message(reply_token, ui.main_menu(user))
                else:
                    reply_message(reply_token, ui.ask_name())
            else:
                logger.warning(f"Invalid name: {name}")
                reply_message(reply_token, ui.ask_name_invalid())
            return

        if db.is_changing_name(user_id):
            logger.info("Changing name")
            
            if cmd in Config.RESERVED_COMMANDS:
                logger.warning(f"Reserved command: {cmd}")
                reply_message(reply_token, ui.ask_new_name_invalid())
                return
            
            name = text.strip()[:Config.MAX_NAME_LENGTH]
            if Config.validate_name(name):
                logger.info(f"Name changed: {name}")
                success = db.change_name(user_id, name)
                db.set_changing_name(user_id, False)
                
                if success:
                    user = db.get_user(user_id)
                    reply_message(reply_token, ui.main_menu(user))
                else:
                    reply_message(reply_token, ui.ask_new_name())
            else:
                reply_message(reply_token, ui.ask_new_name_invalid())
            return

        # أولوية 3: أمر انسحب (تجاهل المستخدم)
        if cmd == "انسحب":
            logger.info("User chose to be ignored")
            db.set_ignored(user_id, True)
            db.set_waiting_name(user_id, False)
            return  # لا نرد بشيء، مجرد تجاهل

        # أولوية 4: المستخدمون غير المسجلين (وليسوا متجاهلين)
        if not user:
            logger.info("User not registered")
            
            if cmd == "تسجيل":
                db.set_waiting_name(user_id, True)
                reply_message(reply_token, ui.ask_name())
            else:
                reply_message(reply_token, ui.registration_choice())
            return

        # أولوية 5: اوامر المستخدم المسجل
        if cmd == "ثيم":
            logger.info("Theme toggle")
            new_theme = db.toggle_theme(user_id)
            user = db.get_user(user_id)
            reply_message(reply_token, UI(theme=new_theme).main_menu(user))
            return

        if cmd == "نقاطي":
            logger.info("Stats")
            reply_message(reply_token, ui.stats_card(user))
            return

        if cmd in ("الصداره", "الصدارة"):
            logger.info("Leaderboard")
            reply_message(reply_token, ui.leaderboard_card(db.get_leaderboard()))
            return

        if cmd == "العاب":
            logger.info("Games menu")
            reply_message(reply_token, ui.games_menu())
            return

        if cmd in ("تغيير الاسم", "تغيير اسمي"):
            logger.info("Change name")
            db.set_changing_name(user_id, True)
            reply_message(reply_token, ui.ask_new_name())
            return

        # ايقاف اللعبة الحالية
        if cmd in ("ايقاف", "ايقاف اللعبة"):
            logger.info("Game stop")
            if game_mgr.stop_game(user_id):
                reply_message(reply_token, ui.game_stopped())
            else:
                logger.info("No active game")
            return

        # أولوية 6: المحتوى النصي التفاعلي
        text_response = text_mgr.handle(cmd, theme)
        if text_response:
            logger.info("Text response")
            reply_message(reply_token, text_response)
            return

        # أولوية 7: الالعاب
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
            # Fallback
            logger.info("Unknown - main menu")
            reply_message(reply_token, ui.main_menu(user))

    except Exception as e:
        logger.exception(f"Processing error: {e}")
        try:
            ui = UI()
            reply_message(reply_token, ui.main_menu(db.get_user(user_id)))
        except:
            pass


@handler.add(MessageEvent, message=TextMessageContent)
def on_message(event: MessageEvent):
    """معالجة الرسائل الواردة"""
    user_id = event.source.user_id
    text = event.message.text
    reply_token = event.reply_token

    logger.info(f"Received: {user_id} -> {text[:50]}")
    executor.submit(process_message, user_id, text, reply_token)


@app.route("/callback", methods=["POST"])
def callback():
    """LINE Webhook Callback"""
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
    """Health Check"""
    try:
        active_games = game_mgr.count_active()
        
        return jsonify({
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "active_games": active_games,
            "database": "connected"
        }), 200
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            "status": "unhealthy",
            "error": str(e)
        }), 500


@app.route("/")
def index():
    """Index"""
    return jsonify({
        "name": Config.BOT_NAME,
        "version": Config.VERSION,
        "status": "running",
        "copyright": Config.COPYRIGHT
    })


if __name__ == "__main__":
    logger.info(f"Starting {Config.BOT_NAME} v{Config.VERSION}")
    logger.info(f"Environment: {Config.ENV}")
    logger.info(f"Games: {list(game_mgr._games.keys())}")
    
    from apscheduler.schedulers.background import BackgroundScheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        func=db.cleanup_memory,
        trigger="interval",
        minutes=30,
        id="cleanup_memory"
    )
    scheduler.start()
    logger.info("Scheduler started")
    
    try:
        app.run(
            host="0.0.0.0",
            port=Config.PORT,
            threaded=True,
            debug=(Config.ENV == "development")
        )
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        executor.shutdown(wait=True)
        logger.info("Shutdown completed")
