import os
import logging
import atexit
from datetime import datetime
from threading import Thread
from queue import Queue, Empty

from flask import Flask, request, abort
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
    FlexMessage,
    FlexContainer,
    QuickReply,
    QuickReplyItem,
    MessageAction
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent

from apscheduler.schedulers.background import BackgroundScheduler

from database import Database
from game_engine import GameEngine
from ui_builder import UIBuilder
from config import Config

# الإعداد
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Flask
app = Flask(__name__)

# التحقق من المتغيرات
Config.validate()

# LINE API v3
configuration = Configuration(access_token=Config.LINE_ACCESS_TOKEN)
handler = WebhookHandler(Config.LINE_SECRET)

# المكونات الأساسية
Database.init()
ui_builder = UIBuilder()

# قائمة انتظار المهام
task_queue = Queue()

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
            logger.error(f"Background task error: {e}", exc_info=True)

# بدء العمال في الخلفية
for _ in range(2):
    Thread(target=background_worker, daemon=True).start()

# المجدول
scheduler = BackgroundScheduler(timezone="UTC")

def start_scheduler():
    """بدء المجدول"""
    scheduler.add_job(
        Database.cleanup_inactive_users,
        trigger="interval",
        hours=24,
        id="cleanup_users",
        replace_existing=True
    )
    scheduler.start()
    logger.info("Scheduler started")

if os.environ.get("GUNICORN_WORKER_ID") in (None, "0"):
    start_scheduler()
    atexit.register(lambda: scheduler.shutdown(wait=False))

# تخزين الثيمات للمستخدمين
user_themes = {}

def get_user_theme(user_id: str) -> str:
    """الحصول على ثيم المستخدم"""
    return user_themes.get(user_id, Config.DEFAULT_THEME)

def set_user_theme(user_id: str, theme: str):
    """تعيين ثيم المستخدم"""
    if Config.is_valid_theme(theme):
        user_themes[user_id] = theme
        return True
    return False

# محرك الألعاب (مشترك)
game_engines = {}

def get_game_engine(user_id: str):
    """الحصول على محرك الألعاب للمستخدم"""
    if user_id not in game_engines:
        with ApiClient(configuration) as api_client:
            api_instance = MessagingApi(api_client)
            game_engines[user_id] = GameEngine(api_instance, Database)
    return game_engines[user_id]

def create_quick_reply():
    """إنشاء أزرار الرد السريع"""
    items = [
        QuickReplyItem(action=MessageAction(label="بداية", text="بداية")),
        QuickReplyItem(action=MessageAction(label="العاب", text="العاب")),
        QuickReplyItem(action=MessageAction(label="نقاطي", text="نقاطي")),
        QuickReplyItem(action=MessageAction(label="الصدارة", text="الصدارة")),
        QuickReplyItem(action=MessageAction(label="مساعدة", text="مساعدة")),
    ]
    return QuickReply(items=items)

# المسارات
@app.route("/", methods=["GET"])
def index():
    """الصفحة الرئيسية"""
    return {
        "bot": Config.BOT_NAME,
        "version": Config.VERSION,
        "status": "running"
    }, 200

@app.route("/health", methods=["GET"])
def health():
    """فحص الصحة"""
    return {
        "status": "healthy",
        "time": datetime.utcnow().isoformat(),
        "bot": Config.BOT_NAME
    }, 200

@app.route("/callback", methods=["POST"])
def callback():
    """معالج Webhook"""
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        logger.error("Invalid signature")
        abort(400)
    except Exception as e:
        logger.error(f"Callback error: {e}", exc_info=True)
    
    return "OK", 200

# معالج الرسائل
@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    """معالج الرسائل النصية"""
    def process():
        try:
            text = event.message.text.strip()
            user_id = event.source.user_id
            
            # تحديث النشاط
            Database.update_last_activity(user_id)
            
            # معالجة الأمر
            response = process_command(text, user_id)
            
            # إرسال الرد
            with ApiClient(configuration) as api_client:
                api_instance = MessagingApi(api_client)
                
                # تحويل الرد إلى قائمة
                messages = []
                if isinstance(response, list):
                    for msg in response:
                        messages.append(convert_to_message(msg))
                else:
                    messages.append(convert_to_message(response))
                
                # إضافة Quick Reply للرسالة الأخيرة
                if messages:
                    messages[-1].quick_reply = create_quick_reply()
                
                # إرسال الرد
                api_instance.reply_message(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=messages
                    )
                )
        
        except Exception as e:
            logger.error(f"Message error: {e}", exc_info=True)
            try:
                with ApiClient(configuration) as api_client:
                    api_instance = MessagingApi(api_client)
                    api_instance.reply_message(
                        ReplyMessageRequest(
                            reply_token=event.reply_token,
                            messages=[TextMessage(text="حدث خطأ، حاول لاحقاً")]
                        )
                    )
            except Exception:
                pass
    
    task_queue.put(process)

def convert_to_message(response):
    """تحويل الرد إلى رسالة LINE v3"""
    if isinstance(response, dict):
        # Flex Message
        return FlexMessage(
            alt_text=Config.BOT_NAME,
            contents=FlexContainer.from_dict(response)
        )
    elif isinstance(response, TextMessage):
        # رسالة نصية جاهزة
        return response
    elif isinstance(response, str):
        # نص عادي
        return TextMessage(text=response)
    else:
        # افتراضي
        return TextMessage(text=str(response))

def process_command(text: str, user_id: str):
    """معالجة الأوامر"""
    text_n = text.strip().lower()
    user = Database.get_user_stats(user_id)
    registered = user is not None
    name = user["display_name"] if user else "مستخدم"
    theme = get_user_theme(user_id)
    
    # محرك الألعاب
    game_engine = get_game_engine(user_id)
    
    # التحقق من حالة انتظار الاسم
    if game_engine.is_waiting_for_name(user_id):
        return handle_registration_name(text, user_id, game_engine)
    
    # الأوامر الأساسية
    if text_n in ("بداية", "start", "البداية"):
        return ui_builder.welcome_card(name, registered, theme)
    
    if text_n in ("العاب", "الالعاب"):
        return ui_builder.games_menu_card(theme)
    
    if text_n in ("نقاطي", "احصائياتي", "الاحصائيات"):
        if not registered:
            return TextMessage(text="يجب التسجيل أولاً\nاكتب: تسجيل")
        return ui_builder.stats_card(name, user, theme)
    
    if text_n in ("الصدارة", "لوحة الصدارة"):
        leaders = Database.get_leaderboard()
        return ui_builder.leaderboard_card(leaders, theme)
    
    if text_n in ("مساعدة", "help", "المساعدة"):
        return ui_builder.help_card(theme)
    
    # تغيير الثيم
    if text_n in ("ثيم فاتح", "فاتح", "light"):
        set_user_theme(user_id, "light")
        return TextMessage(text="تم التغيير للثيم الفاتح")
    
    if text_n in ("ثيم داكن", "داكن", "dark"):
        set_user_theme(user_id, "dark")
        return TextMessage(text="تم التغيير للثيم الداكن")
    
    # التسجيل
    if text_n == "تسجيل":
        if registered:
            return TextMessage(text="انت مسجل بالفعل")
        game_engine.set_waiting_for_name(user_id, True)
        return TextMessage(text="اكتب اسمك للتسجيل:")
    
    # إيقاف اللعبة
    if text_n == "ايقاف":
        if game_engine.stop_game(user_id):
            return TextMessage(text="تم إيقاف اللعبة")
        return TextMessage(text="لا توجد لعبة نشطة")
    
    # معالجة الألعاب
    response = game_engine.process_message(text, user_id, user_id, name, registered)
    
    if response:
        return response
    
    # رد افتراضي
    return TextMessage(text="امر غير معروف\nاكتب: مساعدة")

def handle_registration_name(text: str, user_id: str, game_engine):
    """معالجة اسم التسجيل"""
    name = text.strip()
    
    if len(name) < 2:
        return TextMessage(text="الاسم قصير جداً\nالحد الأدنى حرفان")
    
    if len(name) > 20:
        return TextMessage(text="الاسم طويل جداً\nالحد الأقصى 20 حرف")
    
    success = Database.register_or_update_user(user_id, name)
    
    if success:
        game_engine.set_waiting_for_name(user_id, False)
        return TextMessage(text=f"تم التسجيل بنجاح\n\nالاسم: {name}\n\nيمكنك الآن اللعب وكسب النقاط")
    else:
        return TextMessage(text="حدث خطأ في التسجيل\nحاول مرة أخرى")

# التشغيل
if __name__ == "__main__":
    port = Config.get_port()
    app.run(host="0.0.0.0", port=port, debug=False)
