# -*- coding: utf-8 -*-
"""
Bot Mesh - LINE Bot Application (Optimized)
Created by: Abeer Aldosari © 2025
"""

import os
import sys
import logging
from datetime import datetime
from flask import Flask, request, abort

from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi,
    ReplyMessageRequest, TextMessage
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent

# ============================================================================
# Configuration
# ============================================================================
BOT_NAME = "Bot Mesh"
BOT_RIGHTS = "تم إنشاء هذا البوت بواسطة عبير الدوسري © 2025"

LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')

if not LINE_CHANNEL_SECRET or not LINE_CHANNEL_ACCESS_TOKEN:
    raise ValueError("❌ Missing LINE credentials!")

# ============================================================================
# Flask Setup
# ============================================================================
app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

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
    "💜": {"color": "#9F7AEA", "bg": "#F3E8FF", "card": "#FAF5FF", "text": "#44337A", "text2": "#6B46C1"},
    "💚": {"color": "#48BB78", "bg": "#E6FFFA", "card": "#F0FFF4", "text": "#234E52", "text2": "#2C7A7B"},
    "🤍": {"color": "#CBD5E0", "bg": "#F8F9FA", "card": "#FFFFFF", "text": "#2D3748", "text2": "#718096"},
    "🖤": {"color": "#2D3748", "bg": "#1A202C", "card": "#2D3748", "text": "#E2E8F0", "text2": "#CBD5E0"},
    "💙": {"color": "#3182CE", "bg": "#EBF8FF", "card": "#BEE3F8", "text": "#2C5282", "text2": "#2B6CB0"},
    "🩶": {"color": "#718096", "bg": "#F7FAFC", "card": "#EDF2F7", "text": "#2D3748", "text2": "#4A5568"},
    "🩷": {"color": "#ED64A6", "bg": "#FFF5F7", "card": "#FED7E2", "text": "#702459", "text2": "#97266D"},
    "🧡": {"color": "#DD6B20", "bg": "#FFFAF0", "card": "#FEEBC8", "text": "#7C2D12", "text2": "#C05621"},
    "🤎": {"color": "#8B4513", "bg": "#F7F3EF", "card": "#EDE0D4", "text": "#5C2E00", "text2": "#7A4F1D"}
}

DEFAULT_THEME = "💜"

# ============================================================================
# Game Loading
# ============================================================================
AVAILABLE_GAMES = {}

try:
    from games.iq_game import IqGame
    from games.math_game import MathGame
    from games.word_color_game import WordColorGame
    from games.scramble_word_game import ScrambleWordGame
    from games.fast_typing_game import FastTypingGame
    from games.opposite_game import OppositeGame
    from games.letters_words_game import LettersWordsGame
    from games.song_game import SongGame
    from games.human_animal_plant_game import HumanAnimalPlantGame
    from games.chain_words_game import ChainWordsGame
    from games.guess_game import GuessGame
    from games.compatibility_game import CompatibilityGame
    
    AVAILABLE_GAMES = {
        "IQ": IqGame,
        "رياضيات": MathGame,
        "لون الكلمة": WordColorGame,
        "كلمة مبعثرة": ScrambleWordGame,
        "كتابة سريعة": FastTypingGame,
        "عكس": OppositeGame,
        "حروف وكلمات": LettersWordsGame,
        "أغنية": SongGame,
        "إنسان حيوان نبات": HumanAnimalPlantGame,
        "سلسلة كلمات": ChainWordsGame,
        "تخمين": GuessGame,
        "توافق": CompatibilityGame
    }
    logger.info(f"✅ تم تحميل {len(AVAILABLE_GAMES)} لعبة")
except Exception as e:
    logger.error(f"❌ خطأ في تحميل الألعاب: {e}")

# ============================================================================
# UI Builder Functions
# ============================================================================
from linebot.v3.messaging import FlexMessage, FlexContainer

def build_home(theme="💜", username="مستخدم", points=0, is_registered=False):
    """نافذة البداية"""
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    status = "✅ مسجل" if is_registered else "⚠️ غير مسجل"
    
    contents = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
            "contents": [
                {"type": "text", "text": f"{theme} Bot Mesh", "weight": "bold", "size": "xl", "color": colors["color"]},
                {"type": "separator"},
                {"type": "box", "layout": "vertical", "spacing": "sm", "contents": [
                    {"type": "text", "text": f"▪️ مرحباً: {username}", "size": "sm", "color": "#666666"},
                    {"type": "text", "text": f"▪️ الحالة: {status}", "size": "sm", "color": "#666666"},
                    {"type": "text", "text": f"▪️ نقاطك: {points}", "size": "sm", "color": "#666666"},
                    {"type": "text", "text": "▪️ اختر ثيمك:", "size": "sm", "weight": "bold", "color": "#333333"}
                ]},
                {"type": "box", "layout": "horizontal", "spacing": "sm", "contents": [
                    {"type": "button", "action": {"type": "message", "label": t, "text": f"ثيم {t}"},
                     "style": "primary" if t == theme else "secondary", "height": "sm"}
                    for t in list(THEMES.keys())[:3]
                ]},
                {"type": "box", "layout": "horizontal", "spacing": "sm", "contents": [
                    {"type": "button", "action": {"type": "message", "label": t, "text": f"ثيم {t}"},
                     "style": "primary" if t == theme else "secondary", "height": "sm"}
                    for t in list(THEMES.keys())[3:6]
                ]},
                {"type": "box", "layout": "horizontal", "spacing": "sm", "contents": [
                    {"type": "button", "action": {"type": "message", "label": t, "text": f"ثيم {t}"},
                     "style": "primary" if t == theme else "secondary", "height": "sm"}
                    for t in list(THEMES.keys())[6:]
                ]},
                {"type": "separator"},
                {"type": "text", "text": "🕹️ الأزرار الثابتة:", "size": "sm", "weight": "bold"},
                {"type": "box", "layout": "horizontal", "spacing": "xs", "contents": [
                    {"type": "button", "action": {"type": "message", "label": "انضم", "text": "انضم"}, "style": "secondary", "height": "sm"},
                    {"type": "button", "action": {"type": "message", "label": "انسحب", "text": "انسحب"}, "style": "secondary", "height": "sm"}
                ]},
                {"type": "box", "layout": "horizontal", "spacing": "xs", "contents": [
                    {"type": "button", "action": {"type": "message", "label": "نقاطي", "text": "نقاطي"}, "style": "secondary", "height": "sm"},
                    {"type": "button", "action": {"type": "message", "label": "صدارة", "text": "صدارة"}, "style": "secondary", "height": "sm"}
                ]}
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                {"type": "text", "text": "📝 ملاحظة: يمكنك استخدام البوت في الخاص أو القروبات", "size": "xxs", "color": "#999999", "align": "center", "wrap": True},
                {"type": "separator"},
                {"type": "text", "text": BOT_RIGHTS, "size": "xxs", "color": "#999999", "align": "center"}
            ]
        }
    }
    return FlexMessage(alt_text="Home", contents=FlexContainer.from_dict(contents))

def build_games_menu(theme="💜"):
    """قائمة الألعاب"""
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    
    game_buttons = {
        "IQ": "ذكاء", "رياضيات": "رياضيات", "لون الكلمة": "لون",
        "كلمة مبعثرة": "ترتيب", "كتابة سريعة": "أسرع", "عكس": "ضد",
        "حروف وكلمات": "تكوين", "أغنية": "أغنية", "إنسان حيوان نبات": "لعبة",
        "سلسلة كلمات": "سلسلة", "تخمين": "خمن", "توافق": "توافق"
    }
    
    games = list(AVAILABLE_GAMES.keys())
    
    contents = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
            "contents": [
                {"type": "text", "text": f"{theme} الألعاب المتاحة", "weight": "bold", "size": "xl", "color": colors["color"]},
                {"type": "separator"},
                {"type": "box", "layout": "horizontal", "spacing": "xs", "contents": [
                    {"type": "button", "action": {"type": "message", "label": game_buttons.get(game, game[:4]), "text": f"لعبة {game}"},
                     "style": "secondary", "height": "sm"}
                    for game in games[:4]
                ]},
                {"type": "box", "layout": "horizontal", "spacing": "xs", "contents": [
                    {"type": "button", "action": {"type": "message", "label": game_buttons.get(game, game[:4]), "text": f"لعبة {game}"},
                     "style": "secondary", "height": "sm"}
                    for game in games[4:8]
                ]},
                {"type": "box", "layout": "horizontal", "spacing": "xs", "contents": [
                    {"type": "button", "action": {"type": "message", "label": game_buttons.get(game, game[:4]), "text": f"لعبة {game}"},
                     "style": "secondary", "height": "sm"}
                    for game in games[8:]
                ]},
                {"type": "separator"},
                {"type": "box", "layout": "horizontal", "contents": [
                    {"type": "button", "action": {"type": "message", "label": "⏹️ إيقاف", "text": "إيقاف"},
                     "style": "primary", "color": "#FF5555", "height": "sm"}
                ]}
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                {"type": "text", "text": BOT_RIGHTS, "size": "xxs", "color": "#999999", "align": "center"}
            ]
        }
    }
    return FlexMessage(alt_text="Games", contents=FlexContainer.from_dict(contents))

def build_my_points(username, points, theme="💜"):
    """نافذة نقاطي"""
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    
    contents = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
            "contents": [
                {"type": "text", "text": f"{theme} نقاطي", "weight": "bold", "size": "xl", "color": colors["color"]},
                {"type": "separator"},
                {"type": "box", "layout": "vertical", "spacing": "md", "contents": [
                    {"type": "text", "text": f"👤 الاسم: {username}", "size": "md"},
                    {"type": "text", "text": f"⭐ النقاط: {points}", "size": "lg", "weight": "bold", "color": colors["color"]},
                    {"type": "separator"},
                    {"type": "text", "text": "⚠️ تحذير: سيتم حذف بياناتك بعد 7 أيام من عدم النشاط",
                     "size": "xs", "color": "#FF5551", "wrap": True}
                ]}
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": BOT_RIGHTS, "size": "xxs", "color": "#999999", "align": "center"}
            ]
        }
    }
    return FlexMessage(alt_text="My Points", contents=FlexContainer.from_dict(contents))

def build_leaderboard(top_users, theme="💜"):
    """نافذة الصدارة"""
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    
    leaderboard_contents = []
    medals = ["🥇", "🥈", "🥉"]
    
    for i, (name, points) in enumerate(top_users[:10], 1):
        medal = medals[i-1] if i <= 3 else f"{i}."
        leaderboard_contents.append({
            "type": "text",
            "text": f"{medal} {name}: {points} نقطة",
            "size": "sm",
            "color": "#666666"
        })
    
    contents = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
            "contents": [
                {"type": "text", "text": f"{theme} لوحة الصدارة", "weight": "bold", "size": "xl", "color": colors["color"]},
                {"type": "separator"},
                {"type": "box", "layout": "vertical", "spacing": "sm", "contents": leaderboard_contents if leaderboard_contents else [
                    {"type": "text", "text": "لا يوجد لاعبين مسجلين بعد", "size": "sm", "color": "#999999", "align": "center"}
                ]}
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": BOT_RIGHTS, "size": "xxs", "color": "#999999", "align": "center"}
            ]
        }
    }
    return FlexMessage(alt_text="Leaderboard", contents=FlexContainer.from_dict(contents))

# ============================================================================
# Helper Functions
# ============================================================================
def get_username(profile):
    """Get username from LINE profile"""
    try:
        return profile.display_name
    except:
        return "مستخدم"

def update_user_activity(user_id):
    """Update last activity"""
    if user_id in registered_users:
        registered_users[user_id]['last_activity'] = datetime.now()

# ============================================================================
# Flask Routes
# ============================================================================
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers.get('X-Line-Signature', '')
    body = request.get_data(as_text=True)
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        logger.error("⚠️ Invalid signature")
        abort(400)
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        abort(500)
    
    return 'OK'

@app.route("/", methods=['GET'])
def home():
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{BOT_NAME}</title>
        <meta charset="utf-8">
        <style>
            body {{
                font-family: 'Segoe UI', sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }}
            .container {{
                background: rgba(255,255,255,0.1);
                backdrop-filter: blur(10px);
                padding: 40px;
                border-radius: 20px;
                max-width: 600px;
                text-align: center;
            }}
            h1 {{ font-size: 2.5em; margin-bottom: 20px; }}
            .status {{ font-size: 1.2em; margin: 20px 0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 {BOT_NAME}</h1>
            <div class="status">✅ Bot is running</div>
            <p>Users: {len(registered_users)} | Games: {len(AVAILABLE_GAMES)} | Active: {len(active_games)}</p>
            <p style="font-size: 0.8em; opacity: 0.7; margin-top: 20px;">{BOT_RIGHTS}</p>
        </div>
    </body>
    </html>
    """

# ============================================================================
# Message Handler
# ============================================================================
@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    try:
        user_id = event.source.user_id
        text = event.message.text.strip()
        
        if not text:
            return
        
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            
            try:
                profile = line_bot_api.get_profile(user_id)
                username = get_username(profile)
            except:
                username = "مستخدم"
            
            # New user registration
            if user_id not in registered_users:
                registered_users[user_id] = {
                    "name": username,
                    "points": 0,
                    "is_registered": False,
                    "created_at": datetime.now(),
                    "last_activity": datetime.now()
                }
                logger.info(f"✅ New user: {username}")
                
                current_theme = user_themes.get(user_id, DEFAULT_THEME)
                welcome_reply = build_home(current_theme, username, 0, False)
                
                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(reply_token=event.reply_token, messages=[welcome_reply])
                )
                return
            
            update_user_activity(user_id)
            
            current_theme = user_themes.get(user_id, DEFAULT_THEME)
            user_data = registered_users[user_id]
            reply = None
            
            text_lower = text.lower()
            
            # Commands
            if text_lower == "home":
                reply = build_home(current_theme, username, user_data['points'], user_data['is_registered'])
            elif text_lower == "games":
                reply = build_games_menu(current_theme)
            elif text.startswith("ثيم "):
                theme = text.replace("ثيم ", "").strip()
                if theme in THEMES:
                    user_themes[user_id] = theme
                    reply = build_home(theme, username, user_data['points'], user_data['is_registered'])
            elif text == "انضم":
                registered_users[user_id]["is_registered"] = True
                reply = TextMessage(text=f"✅ مرحباً {username}! تم تسجيلك بنجاح")
            elif text == "انسحب":
                registered_users[user_id]["is_registered"] = False
                reply = TextMessage(text=f"👋 {username} تم إلغاء تسجيلك")
            elif text == "نقاطي":
                reply = build_my_points(username, user_data['points'], current_theme)
            elif text == "صدارة":
                sorted_users = sorted(
                    [(u["name"], u["points"]) for u in registered_users.values() if u.get("is_registered")],
                    key=lambda x: x[1], reverse=True
                )
                reply = build_leaderboard(sorted_users, current_theme)
            elif text == "إيقاف":
                if user_id in active_games:
                    del active_games[user_id]
                    reply = TextMessage(text="⏹️ تم إيقاف اللعبة")
            elif text.startswith("لعبة "):
                if not user_data.get("is_registered"):
                    reply = TextMessage(text="⚠️ يجب التسجيل أولاً")
                else:
                    game_name = text.replace("لعبة ", "").strip()
                    if game_name in AVAILABLE_GAMES:
                        GameClass = AVAILABLE_GAMES[game_name]
                        game_instance = GameClass(line_bot_api)
                        game_instance.set_theme(current_theme)
                        active_games[user_id] = game_instance
                        reply = game_instance.start_game()
            else:
                if user_id in active_games:
                    game_instance = active_games[user_id]
                    result = game_instance.check_answer(text, user_id, username)
                    if result:
                        if result.get('points', 0) > 0:
                            registered_users[user_id]['points'] += result['points']
                        if result.get('game_over'):
                            del active_games[user_id]
                        reply = result.get('response')
                else:
                    reply = TextMessage(text=f"مرحباً {username}! 👋\nاضغط على 'Home' للبدء أو 'Games' لعرض الألعاب 🎮")
            
            if reply:
                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(reply_token=event.reply_token, messages=[reply])
                )
                
    except Exception as e:
        logger.error(f"❌ Error: {e}", exc_info=True)

# ============================================================================
# Run
# ============================================================================
if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    logger.info(f"🚀 Starting {BOT_NAME} on port {port}")
    logger.info(f"📦 Loaded {len(AVAILABLE_GAMES)} games")
    app.run(host="0.0.0.0", port=port, debug=False)
