from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, Mention, Mentionee
import os
import random

app = Flask(__name__)

LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# قائمة أسئلة (تقدر تزيد لين 300)
questions = [
    "ما هو أجمل يوم مرّ عليك في حياتك؟",
    "لو رجع بك الزمن، ما الشيء الذي تود تغييره؟",
    "ما أكثر صفة تحبها في نفسك؟",
    "من الشخص الأقرب لقلبك؟",
    "ما هي أحلامك للمستقبل؟",
    "لو خيروك تعيش في أي بلد، وش تختار؟",
    "متى آخر مرة بكيت وليه؟",
    "ما أكثر شيء يضحكك؟",
    "لو ربحت مليون ريال وش أول شيء تسويه؟",
    "ما هو أكثر موقف محرج صار لك؟",
    "لو كان عندك قوة خارقة، وش بتكون؟",
    "ما أكثر عادة سيئة ودك تتركها؟",
    "وش أكثر أكل تحبه؟",
    "من الشخص اللي مستحيل تنساه؟",
    "وش أكثر شيء تخاف منه؟",
]

def get_random_questions(n=10):
    return random.sample(questions, min(n, len(questions)))

# تخزين عدد الروابط لكل مستخدم
user_links_count = {}

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
    user_id = event.source.user_id
    text = event.message.text.strip()

    # تشغيل
    if text == "تشغيل":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="تم تشغيل البوت")
        )

    # مساعدة
    elif text in ["مساعدة", "مساعده"]:
        help_text = (
            "اوامر البوت:\n\n"
            "- سؤال / اساله: يعطيك 10 اسئلة عشوائية\n"
            "- مساعدة: قائمة الاوامر\n"
            "- تشغيل: تشغيل البوت\n"
        )
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=help_text)
        )

    # الأسئلة
    elif text in ["سؤال", "سوال", "اساله", "أساله", "اسألة", "أسالة"]:
        selected = get_random_questions(10)
        reply_text = "اليك 10 اسئلة عشوائية:\n\n" + "\n".join([f"- {q}" for q in selected])
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_text)
        )

    # منع الروابط
    elif "http" in text or "https" in text:
        if user_id not in user_links_count:
            user_links_count[user_id] = 1
            # اول مرة → تجاهل
            return
        else:
            user_links_count[user_id] += 1
            if user_links_count[user_id] >= 2:
                mention = Mention(
                    mentionees=[Mentionee(user_id=user_id)]
                )
                warning_msg = TextSendMessage(
                    text="الرجاء عدم تكرار الروابط",
                    mention=mention
                )
                line_bot_api.reply_message(event.reply_token, warning_msg)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
