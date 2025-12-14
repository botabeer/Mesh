import os
import logging
from threading import Thread
from queue import Queue, Empty
import atexit
from datetime import datetime

from flask import Flask, request, abort
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi,
    ReplyMessageRequest, TextMessage, FlexMessage, FlexContainer
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3 import WebhookHandler
from apscheduler.schedulers.background import BackgroundScheduler

from config import Config
from database import Database
from game_engine import GameEngine
from ui_builder import UIBuilder

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

for var in ['LINE_CHANNEL_ACCESS_TOKEN', 'LINE_CHANNEL_SECRET']:
    if not os.getenv(var):
        raise ValueError(f"Missing environment variable: {var}")

configuration = Configuration(access_token=os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))

Database.init()
game_engine = GameEngine(configuration, Database)
ui_builder = UIBuilder()

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
            logger.error(f"Background task error: {e}", exc_info=True)

for _ in range(4):
    t = Thread(target=background_worker, daemon=True)
    t.start()

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
        abort(500)
    
    return 'OK', 200

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    task_queue.put(lambda: process_event(event))

def process_event(event):
    try:
        text = event.message.text.strip()
        user_id = event.source.user_id
        
        Database.update_last_activity(user_id)
        
        user_theme = Database.get_user_theme(user_id)
        ui_builder.theme = user_theme
        
        response = process_command(text, user_id)
        
        if response is None:
            response = TextMessage(text="اكتب 'بداية' لعرض القائمة")
        
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            
            if isinstance(response, list):
                line_bot_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=response
                    )
                )
            else:
                line_bot_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[response]
                    )
                )
        
    except Exception as e:
        logger.error(f"Message processing error: {e}", exc_info=True)

def process_command(text, user_id):
    text_normalized = text.lower().strip()
    
    user_data = Database.get_user_stats(user_id)
    is_registered = user_data is not None
    display_name = user_data['display_name'] if user_data else "مستخدم"
    
    if game_engine.is_waiting_for_name(user_id):
        name = text.strip()[:50]
        if len(name) >= 2:
            Database.register_or_update_user(user_id, name)
            game_engine.set_waiting_for_name(user_id, False)
            return safe_flex(ui_builder.welcome_card(name, True), "تم التسجيل")
        return TextMessage(text="الاسم يجب ان يكون حرفين على الاقل")
    
    if text_normalized == "تغيير_الثيم":
        new_theme = Database.toggle_user_theme(user_id)
        ui_builder.theme = new_theme
        theme_ar = "الوضع الداكن" if new_theme == "dark" else "الوضع الفاتح"
        return safe_flex(ui_builder.welcome_card(display_name, is_registered), f"تم التغيير الى {theme_ar}")
    
    resolved_command = Config.resolve_command(text_normalized)
    system_response = handle_system_commands(resolved_command, user_id, user_data, is_registered, display_name)
    if system_response:
        return system_response
    
    registration_response = handle_registration(text_normalized, user_id, is_registered, display_name)
    if registration_response:
        return registration_response
    
    user_theme = Database.get_user_theme(user_id)
    return game_engine.process_message(
        text=text,
        user_id=user_id,
        display_name=display_name,
        is_registered=is_registered,
        theme=user_theme
    )

def handle_system_commands(command, user_id, user_data, is_registered, display_name):
    if command == "بداية":
        return safe_flex(ui_builder.welcome_card(display_name, is_registered), "القائمة الرئيسية")
    if command == "مساعدة":
        return safe_flex(ui_builder.help_card(), "المساعدة")
    if command == "العاب":
        return safe_flex(ui_builder.games_menu_card(), "قائمة الالعاب")
    if command == "نقاطي":
        if not is_registered:
            return TextMessage(text="يجب التسجيل اولا\nاكتب: تسجيل")
        return safe_flex(ui_builder.stats_card(display_name, user_data), "احصائياتك")
    if command == "الصدارة":
        leaders = Database.get_leaderboard(20)
        return safe_flex(ui_builder.leaderboard_card(leaders), "لوحة الصدارة")
    if command == "ايقاف":
        stopped = game_engine.stop_game(user_id)
        return TextMessage(text="تم ايقاف اللعبة" if stopped else "لا توجد لعبة نشطة")
    return None

def handle_registration(text_normalized, user_id, is_registered, display_name):
    if text_normalized in ["تسجيل", "تغيير"]:
        if game_engine.is_game_active(user_id):
            return TextMessage(text="اوقف اللعبة اولا قبل تغيير الاسم")
        game_engine.set_waiting_for_name(user_id, True)
        msg = f"انت مسجل حاليا باسم: {display_name}\n\nادخل الاسم الجديد:" if is_registered else "ادخل اسمك للتسجيل:"
        return TextMessage(text=msg)
    return None

def safe_flex(card_dict, alt_text):
    try:
        return FlexMessage(
            alt_text=alt_text,
            contents=FlexContainer.from_dict(card_dict)
        )
    except Exception as e:
        logger.error(f"FlexMessage build error: {e}", exc_info=True)
        return TextMessage(text="حدث خطأ في عرض البطاقة")

@app.route('/health', methods=['GET'])
def health_check():
    return {
        'status': 'healthy',
        'service': 'bot-mesh',
        'timestamp': datetime.now().isoformat(),
        'active_games': game_engine.get_active_games_count()
    }, 200

@app.route('/')
def index():
    return {
        'status': 'running',
        'service': 'bot-mesh',
        'version': Config.VERSION
    }, 200

if __name__ == "__main__":
    port = Config.get_port()
    debug = os.getenv('FLASK_DEBUG', '0') == '1'
    logger.info(f"Starting Bot Mesh v{Config.VERSION} on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
