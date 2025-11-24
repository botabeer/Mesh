"""
Bot Mesh - Ultimate LINE Bot (2025)
Created by: Abeer Aldosari © 2025
Features: All-in-One Games, Fixed Footer, Themes, User Management, Progress Bars
"""

import os
import logging
import importlib
import inspect
from flask import Flask, request
from linebot.v3.messaging import ApiClient, FlexSendMessage

# ------------------- Logging -------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ------------------- Config -------------------
CHANNEL_ACCESS = os.environ.get("CHANNEL_ACCESS", "YOUR_CHANNEL_ACCESS_TOKEN")
API_CLIENT = ApiClient({"access_token": CHANNEL_ACCESS})

# ------------------- Flask App -------------------
app = Flask(__name__)

# ------------------- Users & Games -------------------
USERS = {}  # user_id: {"name": str, "points": int, "theme": str}
GAMES = []  # List of game classes
ACTIVE_GAMES = {}  # user_id: {"game": BaseGame instance, "round": int, "letters": str, "prev_answer": str}

# ------------------- Base Game -------------------
class BaseGame:
    name = "Base"
    rounds = 5
    def start(self, user_id):
        return "لعبة افتراضية", ["ا", "ب", "ت"]  # مثال

# ------------------- Load Games Automatically -------------------
games_dir = os.path.join(os.path.dirname(__file__), "games")
for filename in os.listdir(games_dir):
    if filename.endswith(".py") and filename not in ["__init__.py", "base_game.py"]:
        module_name = filename[:-3]
        try:
            module = importlib.import_module(f"games.{module_name}")
            found = False
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if issubclass(obj, BaseGame) and obj.__module__ == module.__name__:
                    GAMES.append(obj)
                    logger.info(f"✅ Loaded game: {obj.__name__}")
                    found = True
            if not found:
                logger.warning(f"⚠️ Module '{module_name}' has no valid BaseGame class")
        except Exception as e:
            logger.error(f"❌ Failed to import module '{module_name}': {e}")

logger.info(f"📊 Total valid games loaded: {len(GAMES)}")

# ------------------- Footer Buttons -------------------
FOOTER_BUTTONS = [
    "ذكاء", "لون", "ترتيب", "رياضيات",
    "أسرع", "ضد", "تكوين", "أغنية",
    "لعبة", "سلسلة", "خمن", "توافق",
    "إيقاف"
]

# ------------------- Flex Builders -------------------
def build_progress_bar(current: int, total: int):
    bar_segments = []
    for i in range(total):
        color = "#4CAF50" if i < current else "#E0E5EC"
        bar_segments.append({
            "type": "box",
            "layout": "vertical",
            "contents": [{"type": "text", "text": " "}],
            "backgroundColor": color,
            "width": f"{100/total}%",
            "height": "6px"
        })
    return {"type": "box", "layout": "horizontal", "contents": bar_segments, "spacing": "sm"}

def build_home(user_id):
    user = USERS.get(user_id, {"name": "ضيف", "points": 0, "theme": "💜"})
    theme_buttons = ["💜", "💚", "🤍", "🖤", "💙", "🩶", "🩷", "🧡", "🤎"]
    flex = {
        "type": "bubble",
        "header": {"type": "box", "layout": "vertical", "contents":[
            {"type": "text", "text": f"🤖 Bot Mesh", "weight": "bold", "size": "lg"},
            {"type": "text", "text": f"▪️ مرحباً: {user['name']}"},
            {"type": "text", "text": f"▪️ الحالة: {'مسجل' if user_id in USERS else 'غير مسجل'}"},
            {"type": "text", "text": f"▪️ نقاطك: {user['points']}"},
            {"type": "text", "text": f"▪️ اختر ثيمك:"}
        ]},
        "body": {"type": "box", "layout": "horizontal", "contents": [
            {"type": "button", "action": {"type": "message", "label": t, "text": f"ثيم {t}"}} for t in theme_buttons
        ]},
        "footer": {"type": "box", "layout": "horizontal", "contents": [
            {"type": "button", "action": {"type": "message", "label": btn, "text": btn}} for btn in ["انضم", "انسحب", "نقاطي", "صدارة"]
        ]}
    }
    return FlexSendMessage(alt_text="الصفحة الرئيسية", contents=flex)

def build_games_menu():
    flex = {
        "type": "bubble",
        "header": {"type": "text", "text": "🤖 Bot Mesh – مساعدة", "weight": "bold", "size": "lg"},
        "body": {"type": "box", "layout": "vertical", "contents":[
            {"type": "text", "text": "🎮 الألعاب المتاحة:"},
            {"type": "text", "text": "ذكاء – رياضيات – لون – أسرع – ترتيب – أغنية – كلمة – سلسلة – خمن – توافق"},
            {"type": "text", "text": "📝 الأوامر أثناء اللعب:"},
            {"type": "text", "text": "▫️ لمح → تلميح أول حرف وعدد حروف الكلمة"},
            {"type": "text", "text": "▫️ جاوب → لإرسال إجابتك"},
            {"type": "text", "text": "▫️ إعادة → لإعادة نفس السؤال"},
            {"type": "text", "text": "▫️ إيقاف → لإيقاف اللعبة"},
        ]}
    }
    return FlexSendMessage(alt_text="مساعدة الألعاب", contents=flex)

def build_game_round(user_id):
    active = ACTIVE_GAMES[user_id]
    game = active["game"]
    round_no = active["round"]
    total_rounds = game.rounds
    letters = active["letters"]
    prev = active.get("prev_answer", "-")
    flex = {
        "type": "bubble",
        "header": {"type": "text", "text": f"🕹️ الجولة {round_no} من {total_rounds}"},
        "body": {"type": "box", "layout": "vertical", "contents":[
            build_progress_bar(round_no, total_rounds),
            {"type": "text", "text": f"🕹️ اللعبة: {game.name}"},
            {"type": "text", "text": f"الحروف المعطاة: {letters}"},
            {"type": "text", "text": f"✅ الإجابة الصحيحة للجولة السابقة: {prev}"}
        ]},
        "footer": {"type": "box", "layout": "horizontal", "contents": [
            {"type": "button", "action": {"type": "message", "label": btn, "text": btn}} for btn in FOOTER_BUTTONS
        ]}
    }
    return FlexSendMessage(alt_text=f"جولة {round_no}", contents=flex)

# ------------------- Webhook -------------------
@app.route("/callback", methods=["POST"])
def callback():
    body = request.get_data(as_text=True)
    events = API_CLIENT.parse_events_from_json(body)
    for event in events:
        user_id = event.source.user_id
        if user_id not in USERS:
            USERS[user_id] = {"name": "ضيف", "points": 0, "theme": "💜"}

        if hasattr(event, "message") and event.message.type == "text":
            text = event.message.text.strip()
            # عند منشن البوت
            if "@Bot Mesh." in text:
                msg = build_games_menu()
            # عند طلب مساعدة
            elif text.lower() in ["مساعدة", "help"]:
                msg = build_games_menu()
            # أي رسالة أخرى: الصفحة الرئيسية
            else:
                msg = build_home(user_id)
            API_CLIENT.push_message(user_id, msg)
    return "OK"

# ------------------- Run -------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
