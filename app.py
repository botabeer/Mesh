"""
Bot Mesh - Full Game Bot (LINE v3 Compatible)
Created by: Abeer Aldosari © 2025
Features:
- 12 Games Auto-loaded
- Fixed Footer Buttons (Always Visible)
- Flex Windows: البداية, مساعدة, نقاطي, الصدارة
- Professional Progress Bars
- Neumorphism Themes
- Tracks Points & Game Rounds
- Show Previous Answer
"""

import os
import logging
from flask import Flask, request
from datetime import datetime
from linebot.v3.messaging import ApiClient
from linebot.v3.messaging.models import FlexSendMessage, TextMessage

# ------------------------------
# GAME LOADER
# ------------------------------
import importlib
import inspect
from games.base_game import BaseGame

games_dir = os.path.dirname(__file__) + "/games"
games_list = []

for filename in os.listdir(games_dir):
    if filename.endswith(".py") and filename not in ["__init__.py", "base_game.py"]:
        module_name = filename[:-3]
        try:
            module = importlib.import_module(f"games.{module_name}")
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if issubclass(obj, BaseGame) and obj.__module__ == module.__name__:
                    games_list.append(obj())
                    logging.info(f"✅ Loaded game: {obj.__name__}")
        except Exception as e:
            logging.error(f"❌ Failed to load {module_name}: {e}")

logging.info(f"📊 Total games loaded: {len(games_list)}")

# ------------------------------
# CONFIG
# ------------------------------
CHANNEL_ACCESS = os.environ.get("CHANNEL_ACCESS", "")
CHANNEL_SECRET = os.environ.get("CHANNEL_SECRET", "")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
client = ApiClient(configuration={"access_token": CHANNEL_ACCESS})

# ------------------------------
# USERS & THEMES
# ------------------------------
users = {}
THEMES = ["💜","💚","🤍","🖤","💙","🩶","🩷","🧡","🤎"]
DEFAULT_THEME = "💜"

# ------------------------------
# FOOTER BUTTONS
# ------------------------------
FOOTER_BUTTONS = [
    "ذكاء", "لون", "ترتيب", "رياضيات",
    "أسرع", "ضد", "تكوين", "أغنية",
    "لعبة", "سلسلة", "خمن", "توافق"
]
STOP_BUTTON = "إيقاف"
HELP_BUTTON = "مساعدة"
HOME_BUTTON = "بداية"

# ------------------------------
# FLEX BUILDERS
# ------------------------------
def build_progress_bar(current:int, total:int) -> dict:
    blocks = []
    for i in range(total):
        color = "#4CAF50" if i < current else "#E0E0E0"
        blocks.append({"type":"box","layout":"vertical","width":f"{int(100/total)}%","height":"6px","backgroundColor":color})
    return {"type":"box","layout":"horizontal","spacing":"sm","contents":blocks}

def build_home(user_id:str) -> FlexSendMessage:
    user = users.get(user_id, {"points":0, "theme":DEFAULT_THEME})
    theme_buttons = [{"type":"button","action":{"type":"postback","label":t,"data":f"theme:{t}"}} for t in THEMES]
    flex_content = {
        "type":"bubble",
        "header":{"type":"text","text":" Bot Mesh - البداية","weight":"bold","size":"lg"},
        "body":{"type":"box","layout":"vertical","spacing":"md","contents":[
            {"type":"text","text":f"▪️ مرحباً: {user_id}"},
            {"type":"text","text":f"▪️ نقاطك: {user['points']}"},
            {"type":"text","text":"▪️ اختر ثيمك:"},
            {"type":"box","layout":"horizontal","contents":theme_buttons}
        ]},
        "footer":{"type":"box","layout":"vertical","contents":[
            {"type":"text","text":"🕹️ الأزرار الثابتة:"},
            {"type":"box","layout":"horizontal","contents":[{"type":"button","action":{"type":"postback","label":b,"data":f"game:{b}"}} for b in FOOTER_BUTTONS]},
            {"type":"button","action":{"type":"postback","label":STOP_BUTTON,"data":"stop"}}
        ]}
    }
    return FlexSendMessage(alt_text="البداية", contents=flex_content)

def build_help() -> FlexSendMessage:
    flex_content = {
        "type":"bubble",
        "header":{"type":"text","text":" Bot Mesh - مساعدة","weight":"bold"},
        "body":{"type":"box","layout":"vertical","contents":[
            {"type":"text","text":"🎮 الألعاب المتاحة:"},
            {"type":"text","text":" ".join(FOOTER_BUTTONS)},
            {"type":"text","text":"📝 أوامر اللعب:"},
            {"type":"text","text":"▫️ لمح → تلميح أول حرف وعدد الحروف"},
            {"type":"text","text":"▫️ جاوب → لإرسال إجابتك"},
            {"type":"text","text":"▫️ إعادة → لإعادة نفس السؤال"},
            {"type":"text","text":"▫️ إيقاف → لإيقاف اللعبة"}
        ]}
    }
    return FlexSendMessage(alt_text="مساعدة", contents=flex_content)

def build_game_round(user_id:str) -> FlexSendMessage:
    user = users[user_id]
    game = user.get("current_game")
    if not game:
        return build_home(user_id)
    round_number = user.get("round",1)
    total_rounds = game.total_rounds
    progress = build_progress_bar(round_number, total_rounds)
    flex_content = {
        "type":"bubble",
        "header":{"type":"text","text":f"🎮 اللعبة: {game.name} | الجولة {round_number}/{total_rounds}","weight":"bold"},
        "body":{"type":"box","layout":"vertical","spacing":"md","contents":[
            progress,
            {"type":"text","text":f"الحروف المعطاة: {game.get_letters()}"},
            {"type":"text","text":f"✅ الإجابة السابقة: {user.get('last_answer','-')}"}
        ]},
        "footer":{"type":"box","layout":"horizontal","contents":[
            {"type":"button","action":{"type":"postback","label":"▫️ لمح","data":"hint"}},
            {"type":"button","action":{"type":"postback","label":"▫️ جاوب","data":"answer"}},
            {"type":"button","action":{"type":"postback","label":"▫️ إعادة","data":"repeat"}},
            {"type":"button","action":{"type":"postback","label":"▫️ إيقاف","data":"stop"}}
        ]}
    }
    return FlexSendMessage(alt_text=f"جولة {round_number}", contents=flex_content)

# ------------------------------
# CALLBACK
# ------------------------------
@app.route("/callback", methods=["POST"])
def callback():
    body = request.get_data(as_text=True)
    logger.info(f"Incoming request: {body}")

    # For simplicity, using pseudo deserialization
    events = [{"user_id":"test_user","message":body}]  # Replace with real WebhookEvent parsing

    for event in events:
        user_id = event["user_id"]
        if user_id not in users:
            users[user_id] = {"points":0,"theme":DEFAULT_THEME,"current_game":None,"round":0,"last_answer":""}

        if "منشن" in event["message"]:
            # عند منشنة البوت
            client.messaging_api.push_message(to=user_id, messages=[build_home(user_id)])
            client.messaging_api.push_message(to=user_id, messages=[build_help()])

    return "OK"

# ------------------------------
# MAIN
# ------------------------------
if __name__ == "__main__":
    logger.info("🚀 Starting @Bot Mesh...")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
