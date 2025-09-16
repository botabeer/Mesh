from flask import Flask, request, abort
from dotenv import load_dotenv
import os
import random

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

load_dotenv()

app = Flask(__name__)

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

# تخزين حالة تشغيل البوت
bot_enabled = True

# تخزين عدد الروابط لكل مستخدم
link_counter = {}

# تحميل الأسئلة
with open("questions.txt", "r", encoding="utf-8") as f:
    QUESTIONS = [q.strip() for q in f.readlines() if q.strip()]

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global bot_enabled

    user_id = event.source.user_id
    text = event.message.text.strip()

    # أمر تشغيل
    if text == "تشغيل":
        bot_enabled = True
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="البوت يعمل الآن")
        )
        return

    # أمر تعطيل
    if text == "تعطيل":
        bot_enabled = False
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="تم إيقاف البوت")
        )
        return

    if not bot_enabled:
        return

    # حماية من تكرار الروابط
    if "http://" in text or "https://" in text:
        link_counter[user_id] = link_counter.get(user_id, 0) + 1
        if link_counter[user_id] >= 2:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=f"ممنوع تكرار الروابط يا @{user_id}")
            )
        return

    # الأسئلة
    if text in ["سؤال", "اسئلة", "اساله", "اسألة"]:
        question = random.choice(QUESTIONS)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=question)
        )
        return

if __name__ == "__main__":
    app.run(port=8000)
