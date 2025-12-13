from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os
import logging
from threading import Thread
from queue import Queue
from datetime import datetime

from database import Database
from game_engine import GameEngine

# إعداد السجلات
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# التحقق من المتغيرات البيئية
required_env = ['LINE_CHANNEL_ACCESS_TOKEN', 'LINE_CHANNEL_SECRET']
for var in required_env:
    if not os.getenv(var):
        logger.error(f"Missing environment variable: {var}")
        raise ValueError(f"Missing {var}")

# تهيئة LINE Bot
try:
    line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
    handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))
    logger.info("LINE Bot API initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize LINE Bot API: {e}")
    raise

# تهيئة قاعدة البيانات ومحرك الألعاب
try:
    db = Database("botmesh.db")
    game_engine = GameEngine(line_bot_api, db)
    logger.info("Database and Game Engine initialized")
except Exception as e:
    logger.error(f"Failed to initialize components: {e}")
    raise

# قائمة المهام الخلفية
task_queue = Queue(maxsize=1000)

def background_worker():
    """معالج المهام الخلفية"""
    while True:
        try:
            task = task_queue.get(timeout=1)
            if task is None:
                break
            task()
        except Exception as e:
            logger.error(f"Background task error: {e}", exc_info=True)
        finally:
            try:
                task_queue.task_done()
            except:
                pass

# تشغيل 4 معالجات خلفية
for i in range(4):
    t = Thread(target=background_worker, daemon=True, name=f"Worker-{i}")
    t.start()
    logger.info(f"Started background worker {i}")

@app.route("/", methods=['GET'])
def home():
    """الصفحة الرئيسية - للتحقق من تشغيل الخادم"""
    return {
        "status": "online",
        "service": "Bot Mesh",
        "version": "1.0",
        "timestamp": datetime.now().isoformat()
    }, 200

@app.route("/health", methods=['GET'])
def health_check():
    """فحص الصحة"""
    return {
        'status': 'healthy',
        'queue_size': task_queue.qsize(),
        'timestamp': datetime.now().isoformat()
    }, 200

@app.route("/callback", methods=['POST'])
def callback():
    """استقبال Webhook من LINE"""
    signature = request.headers.get('X-Line-Signature', '')
    body = request.get_data(as_text=True)
    
    logger.info(f"Webhook received - Signature present: {bool(signature)}")

    try:
        handler.handle(body, signature)
        logger.info("Webhook handled successfully")
    except InvalidSignatureError:
        logger.error("Invalid signature")
        abort(400)
    except Exception as e:
        logger.error(f"Callback error: {e}", exc_info=True)

    return 'OK', 200

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    """معالج الرسائل النصية"""
    try:
        text = event.message.text.strip()
        user_id = event.source.user_id
        group_id = getattr(event.source, 'group_id', None) or user_id
        reply_token = event.reply_token
        
        logger.info(f"Message from {user_id}: {text[:50]}")

        def process():
            try:
                # الحصول على اسم المستخدم
                display_name = "مستخدم"
                try:
                    if hasattr(event.source, 'group_id'):
                        profile = line_bot_api.get_group_member_profile(
                            event.source.group_id, user_id
                        )
                    else:
                        profile = line_bot_api.get_profile(user_id)
                    display_name = profile.display_name
                except:
                    pass

                # معالجة الرسالة
                response = game_engine.process_message(
                    text=text,
                    user_id=user_id,
                    group_id=group_id,
                    display_name=display_name
                )

                if not response:
                    logger.warning("No response generated")
                    return

                # إرسال الرد
                try:
                    messages = response if isinstance(response, list) else [response]
                    line_bot_api.reply_message(reply_token, messages)
                    logger.info(f"Reply sent successfully to {user_id}")
                except LineBotApiError as e:
                    logger.error(f"Reply failed, trying push: {e}")
                    # محاولة الإرسال المباشر إذا فشل الرد
                    msg = messages[0] if isinstance(messages, list) else messages
                    line_bot_api.push_message(user_id, msg)
                    logger.info(f"Push message sent to {user_id}")

            except Exception as e:
                logger.error(f"Message processing error: {e}", exc_info=True)
                try:
                    line_bot_api.push_message(
                        user_id,
                        TextSendMessage(text="حدث خطأ، حاول مرة أخرى")
                    )
                except Exception as push_error:
                    logger.error(f"Failed to send error message: {push_error}")

        # إضافة المهمة للقائمة
        try:
            task_queue.put(process, timeout=1)
            logger.info("Task queued successfully")
        except Exception as e:
            logger.error(f"Queue full or error: {e}")
            # معالجة فورية إذا فشلت القائمة
            process()

    except Exception as e:
        logger.error(f"Handler error: {e}", exc_info=True)

@app.errorhandler(404)
def not_found(error):
    return {"error": "Not found"}, 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal error: {error}")
    return {"error": "Internal server error"}, 500

if __name__ == "__main__":
    port = int(os.getenv('PORT', 10000))
    logger.info(f"Starting Flask app on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
