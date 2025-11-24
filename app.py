"""
Bot Mesh - LINE Bot Application (Enhanced with Fixed Footer & Mentions)
Created by: Abeer Aldosari © 2025
"""

import os
import logging
from datetime import datetime
from flask import Flask, request, abort

from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi,
    ReplyMessageRequest, TextMessage, FlexMessage, FlexContainer
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent

# ============================================================================
# Configuration
# ============================================================================
BOT_NAME = "@Bot Mesh"
BOT_RIGHTS = "تم إنشاء هذا البوت بواسطة عبير الدوسري © 2025"

CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
CHANNEL_ACCESS = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

if not CHANNEL_SECRET or not CHANNEL_ACCESS:
    raise ValueError("❌ Missing LINE credentials!")

# ============================================================================
# Flask Setup
# ============================================================================
app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

configuration = Configuration(access_token=CHANNEL_ACCESS)
line_bot_api = MessagingApi(ApiClient(configuration))
handler = WebhookHandler(CHANNEL_SECRET)

# ============================================================================
# In-Memory Data
# ============================================================================
registered_users = {}
user_themes = {}
active_games = {}

# ============================================================================
# Themes
# ============================================================================
THEMES = {
    "💜": {"primary": "#9F7AEA", "bg": "#E0E5EC", "card": "#E0E5EC", "text": "#44337A", "text2": "#6B46C1", "shadow1": "#A3B1C6", "shadow2": "#FFFFFF"},
    "💚": {"primary": "#48BB78", "bg": "#E0E5EC", "card": "#E0E5EC", "text": "#234E52", "text2": "#2C7A7B", "shadow1": "#A3B1C6", "shadow2": "#FFFFFF"},
    "🤍": {"primary": "#667EEA", "bg": "#E0E5EC", "card": "#E0E5EC", "text": "#2D3748", "text2": "#718096", "shadow1": "#A3B1C6", "shadow2": "#FFFFFF"},
    "🖤": {"primary": "#667EEA", "bg": "#2D3748", "card": "#3A4556", "text": "#E2E8F0", "text2": "#CBD5E0", "shadow1": "#1A202C", "shadow2": "#414D5F"},
    "💙": {"primary": "#3182CE", "bg": "#E0E5EC", "card": "#E0E5EC", "text": "#2C5282", "text2": "#2B6CB0", "shadow1": "#A3B1C6", "shadow2": "#FFFFFF"},
    "🩶": {"primary": "#718096", "bg": "#E0E5EC", "card": "#E0E5EC", "text": "#2D3748", "text2": "#4A5568", "shadow1": "#A3B1C6", "shadow2": "#FFFFFF"},
    "🩷": {"primary": "#D53F8C", "bg": "#E0E5EC", "card": "#E0E5EC", "text": "#702459", "text2": "#97266D", "shadow1": "#A3B1C6", "shadow2": "#FFFFFF"},
    "🧡": {"primary": "#DD6B20", "bg": "#E0E5EC", "card": "#E0E5EC", "text": "#7C2D12", "text2": "#C05621", "shadow1": "#A3B1C6", "shadow2": "#FFFFFF"},
    "🤎": {"primary": "#8B4513", "bg": "#E0E5EC", "card": "#E0E5EC", "text": "#5C2E00", "text2": "#7A4F1D", "shadow1": "#A3B1C6", "shadow2": "#FFFFFF"}
}
DEFAULT_THEME = "💜"

# ============================================================================
# Load Games
# ============================================================================
AVAILABLE_GAMES = {}
games_folder = "games"
try:
    for file in os.listdir(games_folder):
        if file.endswith(".py") and not file.startswith("__"):
            name = file.replace(".py", "")
            module = __import__(f"games.{name}", fromlist=[name])
            AVAILABLE_GAMES[name] = getattr(module, name.title())  # expects class name same as file title case
except Exception as e:
    logger.error(f"❌ Error loading games: {e}")

# ============================================================================
# Footer Builder (Fixed Buttons)
# ============================================================================
def build_fixed_footer(theme="💜"):
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    games_buttons = [
        {"label": "IQ", "text": "لعبة IQ"},
        {"label": "لون", "text": "لعبة لون الكلمة"},
        {"label": "ترتيب", "text": "لعبة كلمة مبعثرة"},
        {"label": "رياضيات", "text": "لعبة رياضيات"},
        {"label": "أسرع", "text": "لعبة كتابة سريعة"},
        {"label": "ضد", "text": "لعبة عكس"},
        {"label": "تكوين", "text": "لعبة حروف وكلمات"},
        {"label": "أغنية", "text": "لعبة أغنية"},
        {"label": "لعبة", "text": "لعبة إنسان حيوان نبات"},
        {"label": "سلسلة", "text": "لعبة سلسلة كلمات"},
        {"label": "خمن", "text": "لعبة تخمين"},
        {"label": "توافق", "text": "لعبة توافق"},
    ]
    # Arrange buttons in rows of 4
    rows = [games_buttons[i:i+4] for i in range(0, len(games_buttons), 4)]
    row_boxes = []
    for row in rows:
        row_boxes.append({
            "type": "box",
            "layout": "horizontal",
            "spacing": "xs",
            "contents": [
                {
                    "type": "button",
                    "action": {"type": "message", "label": b["label"], "text": b["text"]},
                    "style": "secondary",
                    "height": "sm",
                    "color": colors["shadow1"]
                } for b in row
            ]
        })
    # Add Stop + Navigation
    row_boxes.append({
        "type": "box",
        "layout": "horizontal",
        "spacing": "xs",
        "contents": [
            {"type": "button", "action":{"type":"message","label":"إيقاف","text":"إيقاف"},"style":"secondary","height":"sm","color":"#FF5555"},
            {"type": "button", "action":{"type":"message","label":"بداية","text":"بداية"},"style":"secondary","height":"sm","color":colors["shadow1"]},
            {"type": "button", "action":{"type":"message","label":"مساعدة","text":"مساعدة"},"style":"secondary","height":"sm","color":colors["shadow1"]},
        ]
    })
    return row_boxes

# ============================================================================
# Build Windows
# ============================================================================
def build_home(theme="💜", username="مستخدم", points=0, is_registered=False):
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    status = "✅ مسجل" if is_registered else "⚠️ غير مسجل"
    contents = {
        "type": "bubble",
        "body": {"type": "box", "layout": "vertical", "spacing": "md", "contents":[
            {"type":"text","text":f"🎮 {BOT_NAME}","weight":"bold","size":"xl","color":colors["primary"],"align":"center"},
            {"type":"text","text":f"▪️ مرحباً: {username}","size":"sm","color":colors["text"]},
            {"type":"text","text":f"▪️ الحالة: {status}","size":"sm","color":colors["text"]},
            {"type":"text","text":f"▪️ نقاطك: {points}","size":"sm","color":colors["text"]},
        ], "backgroundColor": colors["bg"], "paddingAll":"20px"},
        "footer":{"type":"box","layout":"vertical","spacing":"sm","contents":build_fixed_footer(theme), "backgroundColor": colors["bg"], "paddingAll":"10px"}
    }
    return FlexMessage(alt_text="Bot Mesh - البداية", contents=FlexContainer.from_dict(contents))

def build_games_menu(theme="💜"):
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    contents = {
        "type":"bubble",
        "body":{"type":"box","layout":"vertical","spacing":"md","contents":[
            {"type":"text","text":f"🤖 {BOT_NAME} – مساعدة","weight":"bold","size":"xl","color":colors["primary"],"align":"center"},
            {"type":"text","text":"🎮 الألعاب المتاحة: IQ – لون – ترتيب – رياضيات – أسرع – ضد – تكوين – أغنية – لعبة – سلسلة – خمن – توافق","size":"sm","color":colors["text"],"wrap":True},
            {"type":"text","text":"📝 الأوامر أثناء اللعب: ▫️ لمح ▫️ جاوب ▫️ إيقاف","size":"sm","color":colors["text"]},
        ],"backgroundColor": colors["bg"], "paddingAll":"20px"},
        "footer":{"type":"box","layout":"vertical","spacing":"sm","contents":build_fixed_footer(theme),"backgroundColor":colors["bg"],"paddingAll":"10px"}
    }
    return FlexMessage(alt_text="Bot Mesh - مساعدة", contents=FlexContainer.from_dict(contents))

# ============================================================================
# Helper Functions
# ============================================================================
def get_username(profile):
    try: return profile.display_name
    except: return "مستخدم"

def update_user_activity(user_id):
    if user_id in registered_users:
        registered_users[user_id]["last_activity"] = datetime.now()

# ============================================================================
# Routes
# ============================================================================
@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        abort(500)
    return "OK"

@app.route("/", methods=["GET"])
def home_route():
    return f"<h1>{BOT_NAME} is running</h1>"

# ============================================================================
# Message Handler
# ============================================================================
@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    user_id = event.source.user_id
    text = event.message.text.strip()
    if not text: return

    # User registration
    if user_id not in registered_users:
        registered_users[user_id] = {"name":"مستخدم","points":0,"is_registered":False,"created_at":datetime.now(),"last_activity":datetime.now()}
    update_user_activity(user_id)
    theme = user_themes.get(user_id, DEFAULT_THEME)

    # Mentions
    if f"@bot mesh" in text.lower():
        msg = build_home(theme, registered_users[user_id]["name"], registered_users[user_id]["points"], registered_users[user_id]["is_registered"])
        line_bot_api.reply_message_with_http_info(ReplyMessageRequest(reply_token=event.reply_token, messages=[msg]))
        return

    # Commands
    reply = None
    text_lower = text.lower()
    if text_lower in ["بداية", "home"]:
        reply = build_home(theme, registered_users[user_id]["name"], registered_users[user_id]["points"], registered_users[user_id]["is_registered"])
    elif text_lower in ["مساعدة","games"]:
        reply = build_games_menu(theme)
    # Additional commands and games logic here...

    if reply:
        line_bot_api.reply_message_with_http_info(ReplyMessageRequest(reply_token=event.reply_token, messages=[reply]))

# ============================================================================
# Run
# ============================================================================
if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    logger.info(f"🚀 Starting {BOT_NAME} on port {port}")
    app.run(host="0.0.0.0", port=port, debug=False)
