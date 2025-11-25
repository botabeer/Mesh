"""
Bot Mesh - LINE All-in-One Full
Created by: Abeer Aldosari © 2025
Features:
- 12 games auto-loaded
- Persistent footer buttons
- Separate Home, Help, Points, Leaderboard windows
- Professional progress indicator per round
- Show last correct answer
- Fully LINE Flex compatible
"""

import os
import json
import logging
from flask import Flask, request, abort
from linebot.v3.messaging import ApiClient, SendMessage
from linebot.v3.messaging.models import TextMessage, FlexSendMessage

# --- Load Games ---
from games.game_loader import games_list
from games.base_game import BaseGame

# --- Logging ---
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

# --- Flask ---
app = Flask(__name__)

# --- LINE ---
CHANNEL_ACCESS = os.getenv("CHANNEL_ACCESS_TOKEN", "")
if not CHANNEL_ACCESS:
    logger.error("❌ CHANNEL_ACCESS_TOKEN not set")
    exit(1)

client = ApiClient(channel_access_token=CHANNEL_ACCESS)

# --- User DB ---
users = {}  # {user_id: {name, points, theme, current_game, round, last_answer}}

# --- Footer buttons ---
FOOTER_BUTTONS = [
    "ذكاء", "لون", "ترتيب", "رياضيات",
    "أسرع", "ضد", "تكوين", "أغنية",
    "لعبة", "سلسلة", "خمن", "توافق"
]

THEMES = ["💜","💚","🤍","🖤","💙","🩶","🩷","🧡","🤎"]

# --- Helper Functions ---
def get_user(user_id, display_name="زائر"):
    if user_id not in users:
        users[user_id] = {
            "name": display_name,
            "points": 0,
            "theme": "💜",
            "current_game": None,
            "round": 0,
            "last_answer": None
        }
    return users[user_id]

def build_progress_bar(round_num, total_rounds=5):
    filled = int(round_num / total_rounds * 100)
    return {
        "type":"box",
        "layout":"horizontal",
        "contents":[
            {"type":"filler","backgroundColor":"#4B9CD3","width":f"{filled}%", "height":"8px", "cornerRadius":"4px"},
            {"type":"filler","backgroundColor":"#E0E5EC","width":f"{100-filled}%", "height":"8px", "cornerRadius":"4px"}
        ]
    }

def build_footer_buttons():
    return {
        "type":"box",
        "layout":"baseline",
        "spacing":"sm",
        "contents":[
            {"type":"button","action":{"type":"message","label":b,"text":b}} for b in FOOTER_BUTTONS
        ]
    }

def build_home(user):
    return {
        "type":"bubble",
        "body":{
            "type":"box",
            "layout":"vertical",
            "spacing":"md",
            "contents":[
                {"type":"text","text":" Bot Mesh","weight":"bold","size":"lg"},
                {"type":"text","text":f"▪️ مرحباً: {user['name']}"},
                {"type":"text","text":f"▪️ الحالة: {'مسجل' if user else 'غير مسجل'}"},
                {"type":"text","text":f"▪️ نقاطك: {user['points']}"},
                {"type":"text","text":"▪️ اختر ثيمك:"},
                {"type":"box","layout":"baseline","contents":[{"type":"button","action":{"type":"message","label":t,"text":t}} for t in THEMES]},
                {"type":"text","text":"🕹️ الأزرار الثابتة:"},
                build_footer_buttons()
            ]
        }
    }

def build_help():
    return {
        "type":"bubble",
        "body":{
            "type":"box","layout":"vertical","spacing":"md",
            "contents":[
                {"type":"text","text":" Bot Mesh – مساعدة","weight":"bold","size":"lg"},
                {"type":"text","text":"🎮 الألعاب المتاحة:"},
                {"type":"text","text":" – ".join(FOOTER_BUTTONS)},
                {"type":"text","text":"📝 الأوامر أثناء اللعب:"},
                {"type":"text","text":"▫️ لمح → تلميح أول حرف وعدد الحروف\n▫️ جاوب → لإرسال إجابتك\n▫️ إعادة → لإعادة نفس السؤال\n▫️ إيقاف → لإيقاف اللعبة"},
                {"type":"text","text":"📝 ملاحظة: يمكنك استخدام البوت في الخاص أو القروبات"},
                {"type":"text","text":"تم إنشاء هذا البوت بواسطة عبير الدوسري © 2025"}
            ]
        }
    }

def build_game_round(user, game_obj:BaseGame):
    return {
        "type":"bubble",
        "body":{
            "type":"box","layout":"vertical","spacing":"md",
            "contents":[
                {"type":"text","text":f"▪️ الجولة {user['round']} من 5"},
                build_progress_bar(user['round'], 5),
                {"type":"text","text":f"🕹️ اللعبة: {user['current_game']}"},
                {"type":"text","text":f"الحروف / المهمة: {game_obj.get_prompt()}"},
                {"type":"text","text":"🎮 الأوامر المتاحة: ▫️ لمح ▫️ جاوب ▫️ إعادة ▫️ إيقاف"},
                {"type":"text","text":f"✅ الإجابة الصحيحة للجولة السابقة: {user['last_answer'] or '-'}"},
                build_footer_buttons()
            ]
        }
    }

# --- Event Handling ---
def handle_event(event):
    user_id = event.get("source", {}).get("userId", "unknown")
    user = get_user(user_id, event.get("source", {}).get("displayName","زائر"))

    if event.get("type") == "message" and "text" in event:
        text = event["text"]
        if text in THEMES:
            user["theme"] = text
        elif text == "مساعدة":
            msg = FlexSendMessage(alt_text="مساعدة", contents=build_help())
            client.send_message(user_id, msg)
        elif text == "بداية":
            msg = FlexSendMessage(alt_text="البداية", contents=build_home(user))
            client.send_message(user_id, msg)
        elif text in FOOTER_BUTTONS:
            user["current_game"] = text
            user["round"] = 1
            # Find the game object
            game_obj = next((g() for g in games_list if g.__name__.startswith(text)), None)
            if game_obj:
                msg = FlexSendMessage(alt_text=text, contents=build_game_round(user, game_obj))
                client.send_message(user_id, msg)
        else:
            client.send_message(user_id, TextMessage(text="أرسل 'بداية' أو 'مساعدة' أو اختر لعبة"))

# --- Flask route ---
@app.route("/callback", methods=["POST"])
def callback():
    body = request.get_data(as_text=True)
    try:
        data = json.loads(body)
    except Exception as e:
        logger.error(f"❌ Invalid JSON: {e}")
        abort(400)
    for event in data.get("events", []):
        handle_event(event)
    return "OK"

# --- Run App ---
if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
