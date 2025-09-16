from flask import Flask, request, abort
from dotenv import load_dotenv
import os
import random

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    MemberJoinedEvent, MemberLeftEvent
)

# تحميل بيانات .env
load_dotenv()

app = Flask(__name__)

LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# قائمة الأوامر
help_text = """اوامر البوت:

عامة:
- مساعدة → عرض هذه القائمة
- id → اظهار userId
- بروفايل → اسمك وصورتك

اسلامية:
- استغفر الله → عداد استغفار
- اذكار الصباح → ذكر عشوائي
- اذكار المساء → ذكر عشوائي
- اية → اية قرانية

ترفيهية:
- نرد → رقم عشوائي
- قرعة → عضو عشوائي
- سؤال → سؤال ثقافي

القروب:
- الكل → منشن للجميع
- قفل القروب → تنبيه اغلاق
- فتح القروب → تنبيه فتح
- طرد @user → طرد عضو (لو البوت ادمن)
"""

# عداد الاستغفار
zikr_count = {}

# اذكار تجريبية (تقدر تزيدها)
adhkar_sabah = ["اصبحنا واصبح الملك لله", "اللهم بك اصبحنا وبك نحيا"]
adhkar_masaa = ["امسينا وامسى الملك لله", "اللهم بك امسينا وبك نحيا"]
ayat = ["وقل رب زدني علما", "ان مع العسر يسرا"]

# اسئلة عشوائية
questions = ["ما هي عاصمة السعودية؟", "كم عدد سور القران؟", "ما هو اسرع حيوان؟"]


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"


# الرد على الرسائل
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_text = event.message.text.strip()
    user_id = event.source.user_id

    # مساعدة
    if user_text == "مساعدة":
        reply = help_text

    # userId
    elif user_text.lower() == "id":
        reply = f"userId الخاص بك:\n{user_id}"

    # بروفايل
    elif user_text == "بروفايل":
        profile = line_bot_api.get_profile(user_id)
        reply = f"اسمك: {profile.display_name}\nصورتك: {profile.picture_url}"

    # استغفار
    elif user_text == "استغفر الله":
        zikr_count[user_id] = zikr_count.get(user_id, 0) + 1
        reply = f"استغفرت {zikr_count[user_id]} مرة"

    # اذكار
    elif user_text == "اذكار الصباح":
        reply = random.choice(adhkar_sabah)
    elif user_text == "اذكار المساء":
        reply = random.choice(adhkar_masaa)

    # اية
    elif user_text == "اية":
        reply = random.choice(ayat)

    # نرد
    elif user_text == "نرد":
        reply = f"النتيجة: {random.randint(1, 6)}"

    # قرعة
    elif user_text == "قرعة":
        reply = "سيتم اختيار عضو عشوائي (ميزة للتجربة)."

    # سؤال
    elif user_text == "سؤال":
        reply = random.choice(questions)

    # قفل القروب
    elif user_text == "قفل القروب":
        reply = "تم قفل القروب (تنبيه فقط)."

    # فتح القروب
    elif user_text == "فتح القروب":
        reply = "تم فتح القروب."

    # منشن للكل
    elif user_text == "الكل":
        reply = "منشن للجميع (تحتاج صلاحيات متقدمة لعرض الاسماء)."

    # طرد عضو (لو البوت ادمن)
    elif user_text.startswith("طرد "):
        reply = "هذه الميزة تحتاج ان يكون البوت ادمن بالقروب."

    else:
        reply = f"استقبلت رسالتك: {user_text}"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply)
    )


# ترحيب عند دخول عضو
@handler.add(MemberJoinedEvent)
def handle_member_join(event):
    for member in event.members:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"اهلا بك في القروب")
        )


# وداع عند خروج عضو
@handler.add(MemberLeftEvent)
def handle_member_left(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="وداعا نتمنى لك التوفيق")
    )


if __name__ == "__main__":
    app.run(port=5000)
