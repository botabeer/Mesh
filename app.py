# ===================================================================
# BOT MESH - COMPLETE CLEAN VERSION
# Created by Abeer Aldossari 2025
# ===================================================================

# FILE STRUCTURE:
# /
# ├── app.py                 (Main application)
# ├── config.py              (Configuration)
# ├── database.py            (Database operations)
# ├── game_engine.py         (Game management)
# ├── ui_builder.py          (UI components)
# ├── requirements.txt       (Dependencies)
# ├── gunicorn_config.py     (Server config)
# ├── Dockerfile             (Container)
# ├── .gitignore             (Git ignore)
# └── games/                 (Game modules)
#     ├── __init__.py
#     ├── base_game.py
#     ├── iq_game.py
#     ├── guess_game.py
#     ├── opposite_game.py
#     ├── scramble_word_game.py
#     ├── math_game.py
#     ├── song_game.py
#     ├── word_color_game.py
#     ├── letters_words_game.py
#     ├── human_animal_plant_game.py
#     ├── chain_words_game.py
#     ├── fast_typing_game.py
#     ├── compatibility_game.py
#     ├── mafia_game.py
#     ├── questions.txt
#     ├── mentions.txt
#     ├── challenges.txt
#     ├── confessions.txt
#     ├── situations.txt
#     └── quotes.txt

# ===================================================================
# app.py
# ===================================================================

from flask import Flask, request, abort
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi,
    ReplyMessageRequest, TextMessage, FlexMessage, FlexContainer
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3 import WebhookHandler
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import os
import logging
from threading import Thread
from queue import Queue, Empty
import atexit

from database import Database
from game_engine import GameEngine
from ui_builder import UIBuilder

# ===================================================================
# LOGGING SETUP
# ===================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ===================================================================
# FLASK APP
# ===================================================================

app = Flask(__name__)

# Environment validation
required_env = ['LINE_CHANNEL_ACCESS_TOKEN', 'LINE_CHANNEL_SECRET']
for var in required_env:
    if not os.getenv(var):
        raise ValueError(f"Missing environment variable: {var}")

# LINE Bot setup
configuration = Configuration(access_token=os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))

# Initialize components
Database.init()
game_engine = GameEngine(configuration, Database)
ui_builder = UIBuilder()

# Background task queue
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

# Start workers
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

# ===================================================================
# WEBHOOK HANDLER
# ===================================================================

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers.get('X-Line-Signature', '')
    body = request.get_data(as_text=True)
    
    logger.info(f"Webhook received: signature={signature[:20]}...")
    
    try:
        handler.handle(body, signature)
        logger.info("Webhook handled successfully")
    except InvalidSignatureError:
        logger.error("Invalid signature")
        abort(400)
    except Exception as e:
        logger.error(f"Callback error: {e}", exc_info=True)
        abort(500)
    
    return 'OK', 200

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    try:
        text = event.message.text.strip()
        user_id = event.source.user_id
        
        logger.info(f"Message: '{text}' from {user_id}")
        
        Database.update_last_activity(user_id)
        
        # Get user theme
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
        
        logger.info(f"Reply sent to {user_id}")
        
    except Exception as e:
        logger.error(f"Message error: {e}", exc_info=True)

# ===================================================================
# COMMAND PROCESSOR
# ===================================================================

def process_command(text, user_id):
    text_normalized = text.lower().strip()
    
    user_data = Database.get_user_stats(user_id)
    is_registered = user_data is not None
    display_name = user_data['display_name'] if user_data else "مستخدم"
    
    # Check if waiting for name input
    if game_engine.is_waiting_for_name(user_id):
        name = text.strip()[:50]
        if len(name) >= 2:
            Database.register_or_update_user(user_id, name)
            game_engine.set_waiting_for_name(user_id, False)
            return FlexMessage(
                alt_text="تم التسجيل",
                contents=FlexContainer.from_dict(
                    ui_builder.welcome_card(name, True)
                )
            )
        return TextMessage(text="الاسم يجب ان يكون حرفين على الاقل")
    
    # Theme toggle
    if text_normalized == "تغيير_الثيم":
        new_theme = Database.toggle_user_theme(user_id)
        ui_builder.theme = new_theme
        theme_ar = "الوضع الداكن" if new_theme == "dark" else "الوضع الفاتح"
        return FlexMessage(
            alt_text=f"تم التغيير الى {theme_ar}",
            contents=FlexContainer.from_dict(
                ui_builder.welcome_card(display_name, is_registered)
            )
        )
    
    # Main menu
    if text_normalized in ["بداية", "start", "بدايه"]:
        return FlexMessage(
            alt_text="القائمة الرئيسية",
            contents=FlexContainer.from_dict(
                ui_builder.welcome_card(display_name, is_registered)
            )
        )
    
    # Help
    if text_normalized in ["مساعدة", "help", "مساعده"]:
        return FlexMessage(
            alt_text="المساعدة",
            contents=FlexContainer.from_dict(ui_builder.help_card())
        )
    
    # Games menu
    if text in ["العاب", "ألعاب"]:
        return FlexMessage(
            alt_text="قائمة الالعاب",
            contents=FlexContainer.from_dict(ui_builder.games_menu_card())
        )
    
    # Registration
    if text_normalized in ["تسجيل", "تغيير"]:
        game_engine.set_waiting_for_name(user_id, True)
        if is_registered:
            msg = f"انت مسجل حاليا باسم: {display_name}\n\nادخل الاسم الجديد:"
        else:
            msg = "ادخل اسمك للتسجيل:"
        return TextMessage(text=msg)
    
    # Stats
    if text_normalized in ["نقاطي", "احصائياتي"]:
        if not is_registered:
            return TextMessage(text="يجب التسجيل اولا\nاكتب: تسجيل")
        return FlexMessage(
            alt_text="احصائياتك",
            contents=FlexContainer.from_dict(
                ui_builder.stats_card(display_name, user_data)
            )
        )
    
    # Leaderboard
    if text_normalized in ["الصدارة", "المتصدرين", "الصداره"]:
        leaders = Database.get_leaderboard(20)
        return FlexMessage(
            alt_text="لوحة الصدارة",
            contents=FlexContainer.from_dict(
                ui_builder.leaderboard_card(leaders)
            )
        )
    
    # Stop game
    if text_normalized in ["ايقاف", "stop", "إيقاف"]:
        stopped = game_engine.stop_game(user_id)
        return TextMessage(text="تم ايقاف اللعبة" if stopped else "لا توجد لعبة نشطة")
    
    # Game processing
    game_response = game_engine.process_message(
        text=text,
        user_id=user_id,
        display_name=display_name,
        is_registered=is_registered,
        theme=ui_builder.theme
    )
    
    return game_response

# ===================================================================
# HEALTH CHECK
# ===================================================================

@app.route('/health', methods=['GET'])
def health_check():
    return {
        'status': 'healthy',
        'service': 'bot-mesh',
        'timestamp': datetime.now().isoformat()
    }, 200

@app.route('/')
def index():
    return {
        'status': 'running',
        'service': 'bot-mesh'
    }, 200

# ===================================================================
# MAIN
# ===================================================================

if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', '0') == '1'
    logger.info(f"Starting Bot Mesh on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)


# ===================================================================
# DEPLOYMENT NOTES
# ===================================================================
# 1. Set environment variables:
#    - LINE_CHANNEL_ACCESS_TOKEN
#    - LINE_CHANNEL_SECRET
# 
# 2. Install dependencies:
#    pip install -r requirements.txt
# 
# 3. Run with Gunicorn:
#    gunicorn app:app -c gunicorn_config.py
# 
# 4. Database auto-initializes on first run
# 
# 5. All games auto-load from games/ directory
# 
# 6. Theme system: light/dark auto-switches per user
# 
# 7. Background cleanup runs every 24h automatically
# ===================================================================
