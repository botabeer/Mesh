# Bot Mesh - Main Application (v3 SDK)
# Created by: Abeer Aldosari © 2025

import os
from flask import Flask, request, abort
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi,
    ReplyMessageRequest, FlexMessage, TextMessage
)
from linebot.v3.webhook import WebhookHandler
from constants import *
from utils import normalize_answer, load_local_questions, save_user_answer, get_user_stats

app = Flask(__name__)

# LINE API
CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

configuration = Configuration(access_token=CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

# --------------------------
# Flex Helper
# --------------------------
def theme_button(title, color):
    return {"type":"button","style":"primary","color":color,"height":"sm","action":{"type":"message","label":title,"text":title}}

def add_fixed_buttons(bubble_contents, screen_type="game"):
    if screen_type == "help":
        bubble_contents.append({"type":"box","layout":"horizontal","spacing":"sm","contents":HELP_SCREEN_BUTTONS})
    else:
        bubble_contents.append({"type":"box","layout":"horizontal","spacing":"sm","contents":FIXED_GAME_BUTTONS})
    return bubble_contents

# --------------------------
# نافذة البداية
# --------------------------
def create_welcome_screen():
    bubble = {
        "type":"bubble",
        "size":"mega",
        "paddingAll":"15px",
        "body":{"type":"box","layout":"vertical","spacing":"md","contents":[
            {"type":"text","text":"Bot Mesh","weight":"bold","size":"xl","align":"center"},
            {"type":"text","text":"بوت الألعاب الترفيهية","size":"xs","align":"center","color":"#666666"},
            {"type":"separator","margin":"md"},
            {"type":"text","text":"مرحباً","align":"center","margin":"md","size":"md"},
            {"type":"text","text":"اختر الثيم المفضل","size":"md","align":"center","margin":"sm"},
            {"type":"box","layout":"vertical","spacing":"xs","margin":"md","contents":[
                {"type":"box","layout":"horizontal","spacing":"sm","contents":[theme_button(t,THEMES[t]) for t in THEMES.keys()[:3]]},
                {"type":"box","layout":"horizontal","spacing":"sm","contents":[theme_button(t,THEMES[t]) for t in THEMES.keys()[3:6]]},
                {"type":"box","layout":"horizontal","spacing":"sm","contents":[theme_button(t,THEMES[t]) for t in THEMES.keys()[6:9]]}
            ]},
            {"type":"separator","margin":"md"},
            {"type":"text","text":"الأوامر المتاحة:","size":"sm","margin":"xs"},
            {"type":"text","text":"مساعدة - عرض الألعاب\nانضم - للتسجيل\nنقاطي - إحصائياتك\nصدارة - أفضل اللاعبين","size":"xs","color":"#777777","margin":"xs"},
            {"type":"text","text":BOT_RIGHTS,"size":"xxs","color":"#999999","align":"center","margin":"sm"}
        ]}
    }
    return FlexMessage(alt_text="نافذة البداية", contents=bubble)

# --------------------------
# نافذة المساعدة
# --------------------------
def create_games_menu():
    def game_btn(name):
        return {"type":"button","style":"secondary","color":"#F0F0F0","height":"sm","action":{"type":"message","label":name,"text":name}}

    bubble_contents = [
        {"type":"text","text":"قائمة الألعاب","weight":"bold","size":"xl","align":"center"},
        {"type":"text","text":"اختر لعبة للبدء","size":"xs","align":"center","color":"#777777","margin":"xs"},
        {"type":"box","layout":"vertical","spacing":"xs","margin":"md","contents":[
            {"type":"box","layout":"horizontal","spacing":"sm","contents":[game_btn("ذكاء"),game_btn("لون"),game_btn("ترتيب")]},
            {"type":"box","layout":"horizontal","spacing":"sm","contents":[game_btn("رياضيات"),game_btn("أسرع"),game_btn("ضد")]},
            {"type":"box","layout":"horizontal","spacing":"sm","contents":[game_btn("تكوين"),game_btn("أغنية"),game_btn("لعبة")]},
            {"type":"box","layout":"horizontal","spacing":"sm","contents":[game_btn("سلسلة"),game_btn("خمن"),game_btn("توافق")]}
        ]}
    ]
    bubble_contents = add_fixed_buttons(bubble_contents, screen_type="help")
    bubble_contents.append({"type":"text","text":BOT_RIGHTS,"size":"xxs","color":"#999999","align":"center","margin":"sm"})
    bubble = {"type":"bubble","size":"mega","paddingAll":"12px","body":{"type":"box","layout":"vertical","spacing":"md","contents":bubble_contents}}
    return FlexMessage(alt_text="قائمة الألعاب", contents=bubble)

# --------------------------
# Webhook
# --------------------------
@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except:
        abort(400)
    return "OK"

# --------------------------
# EVENT HANDLER
# --------------------------
from linebot.v3.webhooks.events import MessageEvent

@handler.add(MessageEvent=MessageEvent)
def handle_message(event):
    text = event.message.text.strip()
    user_name = event.source.user_id  # للحصول على اسم المستخدم من Line
    user_id = event.source.user_id

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

        if text == "بداية":
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[create_welcome_screen()]
                )
            )
            return

        if text == "مساعدة":
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[create_games_menu()]
                )
            )
            return

        # رد افتراضي على الأوامر فقط
        allowed_commands = ["انضم","انسحب","نقاطي","صدارة","ألعاب","إيقاف","إعادة"]
        if text in allowed_commands:
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=f"تم تنفيذ الأمر: {text}")]
                )
            )
            return

        # تجاهل أي رسالة غير مسجلة
        return

# --------------------------
# MAIN
# --------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
