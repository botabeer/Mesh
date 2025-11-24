# Bot Mesh - Main Application (v3 SDK)
# Created by: Abeer Aldosari © 2025

import os
from flask import Flask, request, abort

# LINE SDK v3
from linebot.v3 import WebhookHandler
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi,
    ReplyMessageRequest, FlexMessage, TextMessage
)
from linebot.v3.webhooks.events import MessageEvent

app = Flask(__name__)

# --------------------------
# LINE API
# --------------------------
CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

configuration = Configuration(access_token=CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

# --------------------------
# FUNCTIONS
# --------------------------
def theme_button(title, color):
    return {
        "type": "button",
        "style": "primary",
        "color": color,
        "height": "sm",
        "action": {"type": "message", "label": title, "text": title}
    }

# --------------------------
# نافذة البداية
# --------------------------
def create_welcome_screen():
    bubble = {
        "type": "bubble",
        "size": "mega",
        "paddingAll": "15px",
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
            "contents": [
                {"type": "text", "text": "Bot Mesh", "weight": "bold", "size": "xl", "align": "center"},
                {"type": "text", "text": "بوت الألعاب الترفيهية", "size": "xs", "align": "center", "color": "#666666"},
                {"type": "separator", "margin": "md"},
                {"type": "text", "text": "مرحباً", "align": "center", "margin": "md", "size": "md"},
                {"type": "text", "text": "اختر الثيم المفضل", "size": "md", "align": "center", "margin": "sm"},
                {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "xs",
                    "margin": "md",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "spacing": "sm",
                            "contents": [theme_button("أبيض", "#4CAF50"), theme_button("أسود", "#000000"), theme_button("رمادي", "#999999")]
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "spacing": "sm",
                            "contents": [theme_button("أزرق", "#1976D2"), theme_button("أخضر", "#4CAF50"), theme_button("وردي", "#E91E63")]
                        }
                    ]
                },
                {"type": "separator", "margin": "md"},
                {"type": "text", "text": "الأوامر المتاحة:", "size": "sm", "margin": "xs"},
                {"type": "text", "text": "مساعدة - عرض الألعاب\nانضم - للتسجيل\nنقاطي - إحصائياتك\nصدارة - أفضل اللاعبين", "size": "xs", "color": "#777777", "margin": "xs"}
            ]
        }
    }
    return FlexMessage(alt_text="نافذة البداية", contents=bubble)

# --------------------------
# نافذة الألعاب
# --------------------------
def create_games_menu():
    def game_btn(name):
        return {"type": "button", "style": "secondary", "color": "#F0F0F0", "height": "sm", "action": {"type": "message", "label": name, "text": name}}

    bubble = {
        "type": "bubble",
        "size": "mega",
        "paddingAll": "12px",
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
            "contents": [
                {"type": "text", "text": "قائمة الألعاب", "weight": "bold", "size": "xl", "align": "center"},
                {"type": "text", "text": "اختر لعبة للبدء", "size": "xs", "align": "center", "color": "#777777", "margin": "xs"},
                {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "xs",
                    "margin": "md",
                    "contents": [
                        {"type": "box", "layout": "horizontal", "spacing": "sm", "contents": [game_btn("ذكاء"), game_btn("لون"), game_btn("ترتيب")]},
                        {"type": "box", "layout": "horizontal", "spacing": "sm", "contents": [game_btn("رياضيات"), game_btn("أسرع"), game_btn("ضد")]},
                        {"type": "box", "layout": "horizontal", "spacing": "sm", "contents": [game_btn("تكوين"), game_btn("أغنية"), game_btn("لعبة")]},
                        {"type": "box", "layout": "horizontal", "spacing": "sm", "contents": [game_btn("سلسلة"), game_btn("خمن"), game_btn("توافق")]}
                    ]
                },
                {"type": "separator", "margin": "md"},
                {"type": "box", "layout": "horizontal", "spacing": "sm", "contents": [
                    {"type": "button", "style": "secondary", "color": "#E0E0E0", "height": "sm", "action": {"type": "message", "label": "تقاطعي", "text": "تقاطعي"}},
                    {"type": "button", "style": "secondary", "color": "#E0E0E0", "height": "sm", "action": {"type": "message", "label": "صدارة", "text": "صدارة"}}
                ]},
                {"type": "box", "layout": "horizontal", "spacing": "sm", "contents": [
                    {"type": "button", "style": "secondary", "color": "#D9D9D9", "height": "sm", "action": {"type": "message", "label": "انسحب", "text": "انسحب"}},
                    {"type": "button", "style": "primary", "color": "#3F51B5", "height": "sm", "action": {"type": "message", "label": "انضم", "text": "انضم"}}
                ]}
            ]
        }
    }
    return FlexMessage(alt_text="قائمة الألعاب", contents=bubble)

# --------------------------
# Webhook
# --------------------------
@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except Exception:
        abort(400)
    return "OK"

# --------------------------
# EVENT HANDLER
# --------------------------
@handler.add(MessageEvent)
def handle_message(event: MessageEvent):
    text = event.message.text.strip()
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

        if text == "بداية":
            line_bot_api.reply_message(
                ReplyMessageRequest(reply_token=event.reply_token, messages=[create_welcome_screen()])
            )
            return

        if text == "مساعدة":
            line_bot_api.reply_message(
                ReplyMessageRequest(reply_token=event.reply_token, messages=[create_games_menu()])
            )
            return

        # رد افتراضي
        line_bot_api.reply_message(
            ReplyMessageRequest(reply_token=event.reply_token, messages=[TextMessage(text="تم استلام رسالتك")])
        )

# --------------------------
# MAIN
# --------------------------
if __name__ == "__main__":
    app.run(port=5000, debug=True)
