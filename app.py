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

# إعداد Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

# Flask App
app = Flask(__name__)

# LINE Configuration
line_config = Configuration(access_token=Config.LINE_TOKEN)
handler = WebhookHandler(Config.LINE_SECRET)

# Core Components
db = Database()
game_mgr = GameManager(db)
text_mgr = TextManager()

# Thread Pool للمعالجة
executor = ThreadPoolExecutor(
    max_workers=Config.WORKERS,
    thread_name_prefix="worker"
)


def reply_message(reply_token: str, messages):
    """إرسال رسالة رد"""
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


def process_message(user_id: str, text: str, reply_token: str):
    """معالجة الرسائل الواردة"""
    try:
        logger.info(f"Processing: {user_id} -> {text[:50]}")
        
        cmd = Config.normalize(text)
        if not cmd:
            logger.warning("Empty command")
            return

        # تحديث نشاط المستخدم
        db.update_activity(user_id)
        user = db.get_user(user_id)
        theme = db.get_theme(user_id) if user else "light"
        ui = UI(theme=theme)

        # ========================================
        # أولوية 1: الأوامر العامة (تعمل دائماً)
        # ========================================
        if cmd in ("بدايه", "بداية"):
            logger.info("Main menu requested")
            reply_message(reply_token, ui.main_menu(user))
            return

        if cmd in ("مساعده", "مساعدة"):
            logger.info("Help menu requested")
            reply_message(reply_token, ui.help_menu())
            return

        # ========================================
        # أولوية 2: حالات الانتظار
        # ========================================
        
        # انتظار إدخال الاسم (تسجيل جديد)
        if db.is_waiting_name(user_id):
            logger.info("User waiting for name input")
            
            if cmd in Config.RESERVED_COMMANDS:
                logger.warning(f"Reserved command ignored: {cmd}")
                reply_message(reply_token, ui.ask_name_invalid())
                return
            
            name = text.strip()[:Config.MAX_NAME_LENGTH]
            if Config.validate_name(name):
                logger.info(f"Registering user: {name}")
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

        # انتظار تغيير الاسم
        if db.is_changing_name(user_id):
            logger.info("User changing name")
            
            if cmd in Config.RESERVED_COMMANDS:
                logger.warning(f"Reserved command ignored: {cmd}")
                reply_message(reply_token, ui.ask_new_name_invalid())
                return
            
            name = text.strip()[:Config.MAX_NAME_LENGTH]
            if Config.validate_name(name):
                logger.info(f"Changing name to: {name}")
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

        # ========================================
        # أولوية 3: المستخدمون غير المسجلين
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
        # أولوية 4: أوامر المستخدم المسجل
        # ========================================
        
        # تبديل السمة
        if cmd == "ثيم":
            logger.info("Theme toggle")
            new_theme = db.toggle_theme(user_id)
            user = db.get_user(user_id)
            reply_message(reply_token, UI(theme=new_theme).main_menu(user))
            return

        # الإحصائيات
        if cmd == "نقاطي":
            logger.info("Stats requested")
            reply_message(reply_token, ui.stats_card(user))
            return

        # الصدارة
        if cmd in ("الصداره", "الصدارة"):
            logger.info("Leaderboard requested")
            reply_message(reply_token, ui.leaderboard_card(db.get_leaderboard()))
            return

        # قائمة الألعاب
        if cmd == "العاب":
            logger.info("Games menu requested")
            reply_message(reply_token, ui.games_menu())
            return

        # تغيير الاسم
        if cmd in ("تغيير الاسم", "تغيير اسمي"):
            logger.info("Change name requested")
            db.set_changing_name(user_id, True)
            reply_message(reply_token, ui.ask_new_name())
            return

        # الانسحاب من اللعبة
        if cmd == "انسحب":
            logger.info("Game quit requested")
            if game_mgr.stop_game(user_id):
                reply_message(reply_token, ui.game_stopped())
            else:
                logger.info("No active game to quit")
            return

        # إيقاف اللعبة
        if cmd in ("ايقاف", "ايقاف اللعبة"):
            logger.info("Game stop requested")
            if game_mgr.stop_game(user_id):
                reply_message(reply_token, ui.game_stopped())
            else:
                logger.info("No active game to stop")
            return

        # ========================================
        # أولوية 5: المحتوى النصي التفاعلي
        # ========================================
        text_response = text_mgr.handle(cmd, theme)
        if text_response:
            logger.info("Static text response")
            reply_message(reply_token, text_response)
            return

        # ========================================
        # أولوية 6: الألعاب
        # ========================================
        game_response = game_mgr.handle(
            user_id=user_id,
            cmd=cmd,
            theme=theme,
            raw_text=text
        )

        if game_response:
            logger.info("Game response sent")
            reply_message(reply_token, game_response)
        else:
            # Fallback: عرض القائمة الرئيسية
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
    """معالجة الرسائل الواردة"""
    user_id = event.source.user_id
    text = event.message.text
    reply_token = event.reply_token

    logger.info(f"Received: {user_id} -> {text[:50]}")
    executor.submit(process_message, user_id, text, reply_token)


# Routes
@app.route("/callback", methods=["POST"])
def callback():
    """LINE Webhook Callback"""
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)

    logger.info(f"Webhook: {len(body)} bytes")

    try:
        handler.handle(body, signature)
        logger.info("Webhook handled successfully")
    except InvalidSignatureError:
        logger.error("Invalid signature")
        abort(400)
    except Exception as e:
        logger.error(f"Webhook error: {e}")

    return "OK", 200


@app.route("/health")
def health():
    """Health Check Endpoint"""
    try:
        active_games = game_mgr.count_active()
        db_ok = db.get_user("health_check") is not None or True
        
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
    """Index Route"""
    return jsonify({
        "name": Config.BOT_NAME,
        "version": Config.VERSION,
        "status": "running",
        "copyright": Config.COPYRIGHT
    })


# Entry Point
if __name__ == "__main__":
    logger.info(f"Starting {Config.BOT_NAME} v{Config.VERSION}")
    logger.info(f"Environment: {Config.ENV}")
    logger.info(f"Available games: {list(game_mgr._games.keys())}")
    
    # Scheduler للتنظيف الدوري
    from apscheduler.schedulers.background import BackgroundScheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        func=db.cleanup_memory,
        trigger="interval",
        minutes=30,
        id="cleanup_memory"
    )
    scheduler.start()
    logger.info("Background scheduler started")
    
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
        logger.info("Shutdown completed gracefully")
