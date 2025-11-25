"""
Bot Mesh - Full Integrated App
Created by: Abeer Aldosari © 2025
All-in-One LINE Bot with 12 games, Flex Messages, fixed footer, progress bars, themes, and user management
"""

import os
import logging
import json
from flask import Flask, request, abort

from linebot.v3.messaging import ApiClient, MessagingApi
from linebot.v3.messaging.models import ReplyMessageRequest, TextMessage, FlexMessage

# -------------------------
# CONFIGURATION
# -------------------------
CHANNEL_ACCESS = os.environ.get("CHANNEL_ACCESS", "YOUR_CHANNEL_ACCESS_TOKEN")

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -------------------------
# USER MANAGEMENT (IN-MEMORY for demo)
# -------------------------
USERS = {}  # user_id -> {name, points, theme, last_game, progress}

# -------------------------
# GAME LOADER
# -------------------------
from games.game_loader import games_list  # كل الألعاب المدمجة

# -------------------------
# UTILITIES
# -------------------------
def get_user(user_id):
    if user_id not in USERS:
        USERS[user_id] = {"name": f"مستخدم {len(USERS)+1}", "points": 0, "theme": "💜", "last_game": None, "progress": 0}
    return USERS[user_id]

# -------------------------
# FLEX BUILDERS
# -------------------------
def build_home(user_id):
    user = get_user(user_id)
    return {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
            "contents": [
                {"type": "text", "text": "🤖 Bot Mesh", "weight": "bold", "size": "lg"},
                {"type": "text", "text": f"▪️ مرحباً: {user['name']}"},
                {"type": "text", "text": f"▪️ الحالة: مسجل" if user else "▪️ الحالة: غير مسجل"},
                {"type": "text", "text": f"▪️ نقاطك: {user['points']}"},
                {"type": "text", "text": f"▪️ اختر ثيمك:"},
                {"type": "box", "layout": "horizontal", "contents": [
                    {"type": "button", "action": {"type": "message", "label": t, "text": t}} for t in ["💜","💚","🤍","🖤","💙","🩶","🩷","🧡","🤎"]
                ]},
            ]
        },
        "footer": build_fixed_footer()
    }

def build_games_menu():
    return {
        "type": "bubble",
        "body": {
            "type": "box", "layout": "vertical", "spacing": "sm",
            "contents": [
                {"type": "text", "text": "🤖 Bot Mesh – مساعدة", "weight":"bold","size":"md"},
                {"type": "text", "text": "🎮 الألعاب المتاحة:"},
                {"type": "text", "text": "ذكاء – رياضيات – لون – أسرع – ترتيب – أغنية – كلمة – سلسلة – خمن – توافق"},
                {"type": "text", "text": "📝 الأوامر أثناء اللعب:"},
                {"type": "text", "text": "▫️ لمح → تلميح أول حرف وعدد حروف الكلمة"},
                {"type": "text", "text": "▫️ جاوب → لإرسال إجابتك"},
                {"type": "text", "text": "▫️ إعادة → لإعادة نفس السؤال"},
                {"type": "text", "text": "▫️ إيقاف → لإيقاف اللعبة"},
            ]
        },
        "footer": build_fixed_footer()
    }

def build_fixed_footer():
    # أزرار ثابتة أسفل كل نافذة
    return {
        "type": "box",
        "layout": "horizontal",
        "spacing": "sm",
        "contents": [
            {"type": "button", "action": {"type": "message","label": g.__name__.replace("Game",""), "text": g.__name__.replace("Game","")}} for g in games_list
        ] + [{"type": "button","action":{"type":"message","label":"إيقاف","text":"إيقاف"}}]
    }

def build_progress_bar(progress, total=5):
    # مؤشر بصري احترافي بدون إيموجي
    full = int((progress/total)*10)
    empty = 10 - full
    return "[" + "█"*full + "─"*empty + f"] {progress}/{total}"

# -------------------------
# FLASK WEBHOOK
# -------------------------
@app.route("/webhook", methods=["POST"])
def webhook():
    body = request.get_data(as_text=True)
    try:
        data = json.loads(body)
    except Exception as e:
        logger.error(f"❌ Invalid JSON: {e}")
        abort(400)

    for event in data.get("events", []):
        handle_event(event)

    return "OK"

def handle_event(event):
    user_id = event.get("source", {}).get("userId")
    if not user_id:
        return
    msg_type = event.get("type")
    if msg_type == "message" and event["message"]["type"] == "text":
        text = event["message"]["text"]
        reply_token = event.get("replyToken")
        user = get_user(user_id)

        if text == "بداية":
            send_flex(reply_token, build_home(user_id))
        elif text == "مساعدة":
            send_flex(reply_token, build_games_menu())
        elif text in [g.__name__.replace("Game","") for g in games_list]:
            user["last_game"] = text
            user["progress"] = 0
            send_flex(reply_token, build_game_round(user, text))
        elif text == "إيقاف":
            user["last_game"] = None
            send_text(reply_token, "تم إيقاف اللعبة.")
        else:
            send_text(reply_token, f"لم أفهم: {text}")

def build_game_round(user, game_name):
    progress_bar = build_progress_bar(user["progress"])
    return {
        "type": "bubble",
        "body": {
            "type": "box","layout":"vertical","spacing":"sm",
            "contents":[
                {"type":"text","text":f"🕹️ اللعبة: {game_name}"},
                {"type":"text","text":f"▪️ الجولة {user['progress']+1} من 5"},
                {"type":"text","text":progress_bar},
            ]
        },
        "footer": build_fixed_footer()
    }

def send_flex(reply_token, flex_dict):
    flex_message = FlexMessage(alt_text="Bot Mesh", contents=flex_dict)
    with ApiClient({"access_token": CHANNEL_ACCESS}) as client:
        messaging_api = MessagingApi(client)
        messaging_api.reply_message(
            reply_token=reply_token,
            messages=[flex_message]
        )

def send_text(reply_token, text):
    with ApiClient({"access_token": CHANNEL_ACCESS}) as client:
        messaging_api = MessagingApi(client)
        messaging_api.reply_message(
            reply_token=reply_token,
            messages=[TextMessage(text=text)]
        )

# -------------------------
# RUN
# -------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
