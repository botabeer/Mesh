from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os
import logging
from threading import Thread
from queue import Queue
from datetime import datetime

from database import Database
from game_engine import GameEngine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Validate environment variables
required_env = ['LINE_CHANNEL_ACCESS_TOKEN', 'LINE_CHANNEL_SECRET']
for var in required_env:
    if not os.getenv(var):
        raise ValueError(f"Missing {var}")

line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))

# Initialize components
db = Database("botmesh.db")
game_engine = GameEngine(line_bot_api, db)

# Background task queue
task_queue = Queue(maxsize=1000)

def background_worker():
    while True:
        task = task_queue.get()
        if task is None:
            break
        try:
            task()
        except Exception as e:
            logger.error(f"Background task error: {e}", exc_info=True)
        finally:
            task_queue.task_done()

for _ in range(4):
    Thread(target=background_worker, daemon=True).start()

@app.route("/", methods=['GET'])
def home():
    return "Bot Server Running", 200

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers.get('X-Line-Signature', '')
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    except Exception as e:
        logger.error(f"Callback error: {e}", exc_info=True)

    return 'OK', 200

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text.strip()
    user_id = event.source.user_id
    group_id = getattr(event.source, 'group_id', None) or user_id
    reply_token = event.reply_token

    def process():
        try:
            display_name = "مستخدم"

            response = game_engine.process_message(
                text=text,
                user_id=user_id,
                group_id=group_id,
                display_name=display_name
            )

            if not response:
                return

            try:
                line_bot_api.reply_message(
                    reply_token,
                    response if isinstance(response, list) else [response]
                )
            except Exception:
                line_bot_api.push_message(
                    user_id,
                    response if not isinstance(response, list) else response[0]
                )

        except Exception as e:
            logger.error(f"Message processing error: {e}", exc_info=True)
            try:
                line_bot_api.push_message(
                    user_id,
                    TextSendMessage(text="حدث خطأ، حاول مرة أخرى")
                )
            except:
                pass

    try:
        task_queue.put(process, timeout=1)
    except:
        logger.warning("Queue is full")

@app.route('/health', methods=['GET'])
def health_check():
    return {
        'status': 'healthy',
        'queue_size': task_queue.qsize(),
        'timestamp': datetime.now().isoformat()
    }, 200

if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
