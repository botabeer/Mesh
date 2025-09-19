from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os
import random

from questions import questions  # استيراد قائمة الأسئلة

app = Flask(__name__)

# بيانات التوكن والسر
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# فلتر الروابط
links_count = {}

# تتبع الأسئلة المستخدمة
used_questions = []

def get_random_questions(num=10):
    global used_questions
    
    # إعادة التهيئة إذا ما بقي أسئلة كافية
    if len(used_questions) + num > len(questions):
        used_questions = []
    
    remaining = list(set(questions) - set(used_questions))
    selected = random.sample(remaining, num)
    used_questions.extend(selected)
    
    return selected

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    text = event.message.text.strip()

    # تشغيل البوت
    if text == "تشغيل":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="تم تشغيل البوت ✅")
        )

    # المساعدة
    elif text in ["مساعدة", "مساعده"]:
        help_text = (
            "أوامر البوت:\n\n"
            "تشغيل ← لتشغيل البوت\n"
            "سؤال ← يعطيك 10 أسئلة عشوائية بدون تكرار حتى تنتهي القائمة\n"
            "الروابط المكررة غير مسموحة"
        )
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=help_text)
        )

    # الأسئلة (10 عشوائية كل مرة بدون تكرار)
    elif text in ["سؤال", "اسئلة", "سوال", "اساله", "اسالة", "أساله", "أسألة"]:
        selected = get_random_questions(10)
        reply_text = "\n".join(f"- {q}" for q in selected)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_text)
        )

    # الروابط
    elif "http" in text or "https" in text:
        if user_id not in links_count:
            links_count[user_id] = 1
            return
        else:
            links_count[user_id] += 1
            if links_count[user_id] >= 2:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text="الرجاء عدم تكرار الروابط")
                )

const PORT = process.env.PORT || 3000;
app.listen(PORT, '0.0.0.0', () => console.log(`Running on ${PORT}`));
