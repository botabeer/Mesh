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
    PushMessageRequest, TextMessage
)

from config import Config
from database import Database
from game_manager import GameManager
from ui import UI

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

# Flask App
app = Flask(__name__)

# Validate ENV
if not Config.LINE_SECRET or not Config.LINE_TOKEN:
    raise RuntimeError("LINE credentials missing")

# LINE SDK
config = Configuration(access_token=Config.LINE_TOKEN)
handler = WebhookHandler(Config.LINE_SECRET)

# Services
db = Database()
ui = UI()
game_mgr = GameManager(db)  # ✅ تم التصحيح - وسيط واحد فقط

# Thread pool
executor = ThreadPoolExecutor(max_workers=4, thread_name_prefix="worker")


def push(user_id: str, message):
    """ارسال رسالة"""
    try:
        with ApiClient(config) as client:
            api = MessagingApi(client)
            if not isinstance(message, list):
                message = [message]
            api.push_message(PushMessageRequest(to=user_id, messages=message))
    except Exception as e:
        logger.error(f"Push error: {e}")


def process_message(user_id: str, text: str):
    """معالجة الرسالة في background"""
    try:
        db.update_activity(user_id)
        
        user = db.get_user(user_id)
        theme = db.get_theme(user_id)
        ui.set_theme(theme)
        
        cmd = Config.normalize(text)
        
        # الاوامر
        if cmd == "بداية":
            push(user_id, ui.main_menu(user))
            return
        
        if cmd == "تغيير_الثيم":
            new_theme = db.toggle_theme(user_id)
            ui.set_theme(new_theme)
            push(user_id, ui.main_menu(user))
            return
        
        if cmd == "العاب":
            push(user_id, ui.games_menu())
            return
        
        if cmd == "نقاطي":
            if not user:
                push(user_id, TextMessage(text="سجل اولا"))
                return
            push(user_id, ui.stats_card(user))
            return
        
        if cmd == "الصدارة":
            leaders = db.get_leaderboard()
            push(user_id, ui.leaderboard_card(leaders))
            return
        
        if cmd in ["تسجيل", "تغيير"]:
            db.set_waiting_name(user_id, True)
            push(user_id, TextMessage(text="اكتب اسمك:"))
            return
        
        if cmd == "ايقاف":
            stopped = game_mgr.stop_game(user_id)
            txt = "تم ايقاف اللعبة" if stopped else "لا توجد لعبة"
            push(user_id, TextMessage(text=txt))
            return
        
        # ادخال الاسم
        if db.is_waiting_name(user_id):
            name = text.strip()[:50]
            if len(name) < 2:
                push(user_id, TextMessage(text="الاسم قصير جدا"))
                return
            
            db.register_user(user_id, name)
            db.set_waiting_name(user_id, False)
            user = db.get_user(user_id)
            push(user_id, ui.main_menu(user))
            return
        
        # الالعاب
        result = game_mgr.handle(user_id, cmd, theme)
        if result:
            push(user_id, result)
            return
        
        # رد افتراضي
        push(user_id, TextMessage(text="اكتب: بداية"))
        
    except Exception as e:
        logger.exception(f"Process error: {e}")
        push(user_id, TextMessage(text="حدث خطأ"))


@handler.add(MessageEvent, message=TextMessageContent)
def on_message(event: MessageEvent):
    """معالج الرسائل - رد فوري"""
    user_id = event.source.user_id
    text = event.message.text.strip()
    
    # رد فوري
    try:
        with ApiClient(config) as client:
            api = MessagingApi(client)
            api.reply_message(event.reply_token, [TextMessage(text="...")])
    except:
        pass
    
    # معالجة في background
    executor.submit(process_message, user_id, text)


@app.route("/callback", methods=["POST"])
def callback():
    """Webhook endpoint"""
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
    """Health check"""
    return jsonify({
        "status": "ok",
        "time": datetime.utcnow().isoformat(),
        "active_games": game_mgr.count_active()
    })


@app.route("/")
def index():
    """Home"""
    return jsonify({
        "name": "Bot Mesh",
        "version": "3.0",
        "status": "running"
    })


if __name__ == "__main__":
    logger.info("Starting Bot Mesh v3.0")
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
