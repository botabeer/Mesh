from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os, random

app = Flask(__name__)

CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

# حالة البوت (تشغيل/إيقاف)
bot_active = True

# قائمة أسئلة شخصية (300 مثال مبسط)
questions = [f"سؤال شخصي رقم {i}" for i in range(1, 301)]

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
    global bot_active
    text = event.message.text.strip()

    # أمر تشغيل
    if text == "تشغيل":
        bot_active = True
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="✅ تم تشغيل البوت"))
        return

    # أمر إيقاف
    if text == "ايقاف":
        bot_active = False
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="⛔ تم إيقاف البوت"))
        return

    # لو البوت متوقف ما يرد
    if not bot_active:
        return

    # حماية من الروابط
    if "http://" in text or "https://" in text:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="⚠️ ممنوع إرسال روابط هنا"))
        return

    # أمر الأسئلة
    if text in ["سؤال", "سوال", "اسئلة", "اساله", "أساله", "أسالة"]:
        q = random.choice(questions)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=q))
        return

    # أوامر الأذكار
    if text in ["استغفر الله", "استغفرالله"]:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="استغفر الله 33 مرة 🌿"))
        return

    if text in ["سبحان الله"]:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="سبحان الله 33 مرة 🌸"))
        return

    if text in ["الحمد لله"]:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="الحمد لله 33 مرة 🌼"))
        return

    if text in ["الله أكبر", "الله اكبر"]:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="الله أكبر 34 مرة 🌺"))
        return

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
