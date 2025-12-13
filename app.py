import os
import logging
from datetime import datetime
from threading import Thread
from queue import Queue
import atexit

from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage, QuickReply, QuickReplyButton, MessageAction
from apscheduler.schedulers.background import BackgroundScheduler

from database import Database
from game_engine import GameEngine
from ui_builder import UIBuilder

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('bot.log'), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Flask App
app = Flask(__name__)

# Environment variables
required_env = ['LINE_CHANNEL_ACCESS_TOKEN', 'LINE_CHANNEL_SECRET']
for var in required_env:
    if not os.getenv(var):
        raise ValueError(f"Missing {var}")

line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))

# Initialize Database
Database.init()

# Game engine and UI
game_engine = GameEngine(line_bot_api, Database)
ui_builder = UIBuilder()

# Background task queue
task_queue = Queue()

def background_worker():
    from queue import Empty
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
            logger.error(f"Background task error: {e}", exc_info=True)

for _ in range(4):
    t = Thread(target=background_worker, daemon=True)
    t.start()

# Scheduler for cleanup
scheduler = BackgroundScheduler()
scheduler.add_job(
    func=Database.cleanup_inactive_users,
    trigger="interval",
    hours=24,
    id='cleanup',
    replace_existing=True
)
scheduler.start()
atexit.register(lambda: scheduler.shutdown())

# Quick reply helper
def add_quick_reply(message):
    quick_reply = QuickReply(items=[
        QuickReplyButton(action=MessageAction(label="بداية", text="بداية")),
        QuickReplyButton(action=MessageAction(label="تسجيل", text="تسجيل")),
        QuickReplyButton(action=MessageAction(label="العاب", text="العاب")),
        QuickReplyButton(action=MessageAction(label="نقاطي", text="نقاطي")),
        QuickReplyButton(action=MessageAction(label="الصدارة", text="الصدارة")),
        QuickReplyButton(action=MessageAction(label="ايقاف", text="ايقاف"))
    ])
    if isinstance(message, (TextSendMessage, FlexSendMessage)):
        message.quick_reply = quick_reply
    return message

# Webhook callback
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers.get('X-Line-Signature', '')
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        logger.error("Invalid signature")
        abort(400)
    except Exception as e:
        logger.error(f"Callback error: {e}", exc_info=True)
    return 'OK', 200

# Handle messages
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    def process_message():
        try:
            text = event.message.text.strip()
            user_id = event.source.user_id
            group_id = getattr(event.source, 'group_id', None) or user_id
            logger.info(f"Received message: {text} from user: {user_id}")

            Database.update_last_activity(user_id)

            response = process_command(text, user_id, group_id)

            if response is None:
                response = TextSendMessage(text="اكتب 'بداية' لعرض القائمة")

            # Always send as a list
            if isinstance(response, list):
                response_list = [add_quick_reply(msg) for msg in response]
            else:
                response_list = [add_quick_reply(response)]

            line_bot_api.reply_message(event.reply_token, response_list)
            logger.info(f"Reply sent successfully to user: {user_id}")

        except Exception as e:
            logger.error(f"Message processing error: {e}", exc_info=True)
            try:
                line_bot_api.reply_message(
                    event.reply_token,
                    [TextSendMessage(text="حدث خطا، حاول مرة اخرى")]
                )
            except Exception as reply_error:
                logger.error(f"Failed to send error reply: {reply_error}")

    task_queue.put(process_message)

# Command processing
def process_command(text, user_id, group_id):
    text_normalized = text.lower().strip()
    user_data = Database.get_user_stats(user_id)
    is_registered = user_data is not None
    display_name = user_data['display_name'] if user_data else "مستخدم"

    if text_normalized in ["بداية", "start", "بدايه"]:
        return FlexSendMessage(alt_text="Bot Mesh", contents=ui_builder.welcome_card(display_name, is_registered))
    if text_normalized in ["مساعدة", "help", "مساعده"]:
        return FlexSendMessage(alt_text="المساعدة", contents=ui_builder.help_card())
    if text in ["العاب", "ألعاب"]:
        return FlexSendMessage(alt_text="قائمة الالعاب", contents=ui_builder.games_menu_card())
    if text_normalized in ["تسجيل", "تغيير"]:
        return handle_registration(user_id, is_registered, display_name)
    if text_normalized in ["نقاطي", "احصائياتي"]:
        if not is_registered:
            return TextSendMessage(text="يجب التسجيل اولا\nاكتب: تسجيل")
        return FlexSendMessage(alt_text="احصائياتك", contents=ui_builder.stats_card(display_name, user_data))
    if text_normalized in ["الصدارة", "المتصدرين", "الصداره"]:
        leaders = Database.get_leaderboard(20)
        return FlexSendMessage(alt_text="لوحة الصدارة", contents=ui_builder.leaderboard_card(leaders))
    if text_normalized in ["ايقاف", "stop", "إيقاف"]:
        stopped = game_engine.stop_game(group_id)
        return TextSendMessage(text="تم ايقاف اللعبة" if stopped else "لا توجد لعبة نشطة")

    return game_engine.process_message(text=text, user_id=user_id, group_id=group_id, display_name=display_name, is_registered=is_registered)

def handle_registration(user_id, is_registered, current_name):
    game_engine.set_waiting_for_name(user_id, True)
    if is_registered:
        msg = f"انت مسجل حاليا باسم: {current_name}\n\nادخل الاسم الجديد:"
    else:
        msg = "ادخل اسمك للتسجيل:"
    return TextSendMessage(text=msg)

# Health check
@app.route('/health', methods=['GET'])
def health_check():
    return {'status': 'healthy', 'service': 'bot-alhoot', 'timestamp': datetime.now().isoformat()}, 200

@app.route('/')
def index():
    return {'status': 'running', 'service': 'bot-alhoot'}, 200

if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', '0') == '1'
    logger.info(f"Starting Bot Alhoot on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
