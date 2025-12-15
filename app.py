import os
import logging
from threading import Thread
from queue import Queue, Empty
from datetime import datetime

from flask import Flask, request, abort, jsonify
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi,
    PushMessageRequest, TextMessage, FlexMessage, FlexContainer
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
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Validate environment
for var in ['LINE_CHANNEL_ACCESS_TOKEN', 'LINE_CHANNEL_SECRET']:
    if not os.getenv(var):
        raise ValueError(f"Missing: {var}")

configuration = Configuration(access_token=os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))

# Initialize
Database.init()
game_engine = GameEngine(configuration, Database)
ui_builder = UIBuilder()

# Task queue
task_queue = Queue(maxsize=1000)

def background_worker():
    """معالج المهام في الخلفية"""
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
            logger.error(f"Worker error: {e}")

# Start workers
for _ in range(4):
    Thread(target=background_worker, daemon=True).start()

# Cleanup scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(
    func=Database.cleanup_inactive_users,
    trigger="interval",
    hours=24,
    id='cleanup',
    replace_existing=True
)
scheduler.start()

@app.route("/callback", methods=['POST'])
def callback():
    """استقبال Webhook من LINE - يجب أن يرد فوراً"""
    signature = request.headers.get('X-Line-Signature', '')
    body = request.get_data(as_text=True)
    
    try:
        # التحقق من التوقيع فقط
        handler.handle(body, signature)
    except InvalidSignatureError:
        logger.error("Invalid signature")
        abort(400)
    except Exception as e:
        logger.error(f"Handler error: {e}")
    
    # رد فوري لـ LINE (مهم جداً)
    return jsonify({"status": "ok"}), 200

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    """إضافة المهمة للـ Queue فقط - لا معالجة هنا"""
    task_queue.put(lambda: process_event_async(event))

def process_event_async(event):
    """معالجة الرسالة في الخلفية"""
    try:
        text = event.message.text.strip()
        user_id = event.source.user_id
        
        Database.update_last_activity(user_id)
        
        user_theme = Database.get_user_theme(user_id)
        ui_builder.theme = user_theme
        
        response = process_command(text, user_id)
        
        if response is None:
            response = TextMessage(text="اكتب 'بداية' لعرض القائمة")
        
        # استخدام push_message بدلاً من reply_message
        send_message(user_id, response)
        
    except Exception as e:
        logger.error(f"Process error: {e}")

def send_message(user_id: str, messages):
    """إرسال رسالة باستخدام push_message"""
    try:
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            
            if not isinstance(messages, list):
                messages = [messages]
            
            line_bot_api.push_message(
                PushMessageRequest(to=user_id, messages=messages)
            )
    except Exception as e:
        logger.error(f"Send message error: {e}")

def process_command(text, user_id):
    text_normalized = text.lower().strip()
    
    user_data = Database.get_user_stats(user_id)
    is_registered = user_data is not None
    display_name = user_data['display_name'] if user_data else "مستخدم"
    
    # Name registration
    if game_engine.is_waiting_for_name(user_id):
        name = text.strip()[:50]
        if len(name) >= 2:
            Database.register_or_update_user(user_id, name)
            game_engine.set_waiting_for_name(user_id, False)
            return safe_flex(ui_builder.welcome_card(name, True), "تم التسجيل")
        return TextMessage(text="الاسم يجب ان يكون حرفين على الاقل")
    
    # Theme toggle
    if text_normalized == "تغيير_الثيم":
        new_theme = Database.toggle_user_theme(user_id)
        ui_builder.theme = new_theme
        theme_ar = "الوضع الداكن" if new_theme == "dark" else "الوضع الفاتح"
        return safe_flex(ui_builder.welcome_card(display_name, is_registered), f"تم التغيير الى {theme_ar}")
    
    # System commands
    resolved = Config.resolve_command(text_normalized)
    sys_resp = handle_system_commands(resolved, user_id, user_data, is_registered, display_name)
    if sys_resp:
        return sys_resp
    
    # Registration
    reg_resp = handle_registration(text_normalized, user_id, is_registered, display_name)
    if reg_resp:
        return reg_resp
    
    # Game processing
    return game_engine.process_message(text, user_id, display_name, is_registered, user_theme)

def handle_system_commands(cmd, user_id, user_data, is_registered, display_name):
    if cmd == "بداية":
        return safe_flex(ui_builder.welcome_card(display_name, is_registered), "القائمة")
    if cmd == "مساعدة":
        return safe_flex(ui_builder.help_card(), "المساعدة")
    if cmd == "العاب":
        return safe_flex(ui_builder.games_menu_card(), "الالعاب")
    if cmd == "نقاطي":
        if not is_registered:
            return TextMessage(text="يجب التسجيل اولا\nاكتب: تسجيل")
        return safe_flex(ui_builder.stats_card(display_name, user_data), "احصائياتك")
    if cmd == "الصدارة":
        leaders = Database.get_leaderboard(20)
        return safe_flex(ui_builder.leaderboard_card(leaders), "الصدارة")
    if cmd == "ايقاف":
        stopped = game_engine.stop_game(user_id)
        return TextMessage(text="تم ايقاف اللعبة" if stopped else "لا توجد لعبة نشطة")
    return None

def handle_registration(text, user_id, is_registered, display_name):
    if text in ["تسجيل", "تغيير"]:
        if game_engine.is_game_active(user_id):
            return TextMessage(text="اوقف اللعبة اولا")
        game_engine.set_waiting_for_name(user_id, True)
        msg = f"انت مسجل باسم: {display_name}\n\nادخل الاسم الجديد:" if is_registered else "ادخل اسمك:"
        return TextMessage(text=msg)
    return None

def safe_flex(card, alt):
    try:
        return FlexMessage(alt_text=alt, contents=FlexContainer.from_dict(card))
    except Exception as e:
        logger.error(f"Flex error: {e}")
        return TextMessage(text="حدث خطأ")

@app.route('/health', methods=['GET'])
def health():
    return {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'queue_size': task_queue.qsize(),
        'active_games': game_engine.get_active_games_count()
    }, 200

@app.route('/')
def index():
    return {'status': 'running', 'version': Config.VERSION}, 200

if __name__ == "__main__":
    port = Config.get_port()
    logger.info(f"Starting Bot v{Config.VERSION}")
    app.run(host='0.0.0.0', port=port, debug=False)
