"""
Bot Mesh - LINE Bot Application v3.0
Created by: Abeer Aldosari © 2025

Enhanced Features:
- Professional Neumorphism 3D Design
- 9 Customizable Themes
- AI-powered Games (Gemini)
- Smart Fallback System
- Group-Friendly
- Auto-Cleanup System
- LINE-Compatible Flex Messages
"""

import os
import sys
import logging
from datetime import datetime, timedelta
from flask import Flask, request, abort

from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi,
    ReplyMessageRequest
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent

# Import our modules
from constants import (
    BOT_NAME, BOT_VERSION, BOT_RIGHTS,
    LINE_CHANNEL_SECRET, LINE_CHANNEL_ACCESS_TOKEN,
    GEMINI_API_KEY_1, GEMINI_API_KEY_2, GEMINI_API_KEY_3,
    validate_env, get_username, GAME_LIST, DEFAULT_THEME
)

from ui_builder import (
    build_home, build_games_menu, build_my_points,
    build_leaderboard, build_registration_required
)

# ============================================================================
# Configuration & Validation
# ============================================================================
try:
    validate_env()
except ValueError as e:
    print(f"❌ Configuration Error: {e}")
    sys.exit(1)

# ============================================================================
# Flask & LINE Setup
# ============================================================================
app = Flask(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# ============================================================================
# In-Memory Storage
# ============================================================================
registered_users = {}  # {user_id: {name, points, is_registered, created_at, last_activity}}
user_themes = {}       # {user_id: theme_emoji}
active_games = {}      # {user_id: game_instance}

# ============================================================================
# AI Integration with Intelligent Fallback
# ============================================================================
current_gemini_key = 0
gemini_keys = [k for k in [GEMINI_API_KEY_1, GEMINI_API_KEY_2, GEMINI_API_KEY_3] if k]

def get_next_gemini_key():
    """Rotate through available Gemini API keys"""
    global current_gemini_key
    if not gemini_keys:
        logger.warning("⚠️ No Gemini API keys available")
        return None
    
    key = gemini_keys[current_gemini_key % len(gemini_keys)]
    current_gemini_key += 1
    logger.info(f"🔑 Using Gemini key #{current_gemini_key % len(gemini_keys) + 1}")
    return key

def ai_generate_question(game_type):
    """Generate question using Gemini AI with fallback"""
    try:
        import google.generativeai as genai
        key = get_next_gemini_key()
        if not key:
            return None
        
        genai.configure(api_key=key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompts = {
            "IQ": "أنشئ لغز ذكاء عربي مع إجابة قصيرة. رد بصيغة JSON: {\"q\": \"السؤال\", \"a\": \"الإجابة\"}",
            "رياضيات": "أنشئ مسألة رياضية بسيطة مع الحل. رد بصيغة JSON: {\"q\": \"المسألة\", \"a\": \"الجواب\"}",
            "عكس": "أعط كلمة عربية وعكسها. رد بصيغة JSON: {\"word\": \"الكلمة\", \"opposite\": \"العكس\"}"
        }
        
        prompt = prompts.get(game_type, prompts["IQ"])
        response = model.generate_content(prompt)
        
        import json
        text = response.text.strip()
        
        # Clean JSON from markdown
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]
        
        return json.loads(text.strip())
    except Exception as e:
        logger.error(f"❌ AI generation error: {e}")
        return None

def ai_check_answer(correct_answer, user_answer):
    """Validate answer using Gemini AI"""
    try:
        import google.generativeai as genai
        key = get_next_gemini_key()
        if not key:
            return False
        
        genai.configure(api_key=key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"هل الإجابة '{user_answer}' صحيحة للجواب '{correct_answer}'? رد فقط بـ 'نعم' أو 'لا'"
        response = model.generate_content(prompt)
        
        answer_text = response.text.strip().lower()
        return 'نعم' in answer_text or 'yes' in answer_text
    except Exception as e:
        logger.error(f"❌ AI check error: {e}")
        return False

# ============================================================================
# Game Loading System
# ============================================================================
AVAILABLE_GAMES = {}

try:
    from games.iq_game import IqGame
    from games.math_game import MathGame
    from games.word_color_game import WordColorGame
    from games.scramble_word_game import ScrambleWordGame
    # Import other games here...
    
    AVAILABLE_GAMES = {
        "IQ": IqGame,
        "رياضيات": MathGame,
        "لون الكلمة": WordColorGame,
        "كلمة مبعثرة": ScrambleWordGame
    }
    
    logger.info(f"✅ تم تحميل {len(AVAILABLE_GAMES)} لعبة بنجاح")
except Exception as e:
    logger.error(f"❌ خطأ في تحميل الألعاب: {e}")

# ============================================================================
# Helper Functions
# ============================================================================
def update_user_activity(user_id):
    """Update last activity timestamp"""
    if user_id in registered_users:
        registered_users[user_id]['last_activity'] = datetime.now()

def cleanup_inactive_users():
    """Remove users inactive for 7 days"""
    cutoff = datetime.now() - timedelta(days=7)
    inactive = [
        uid for uid, data in registered_users.items() 
        if data.get('last_activity', datetime.now()) < cutoff
    ]
    
    for uid in inactive:
        if uid in registered_users:
            del registered_users[uid]
        if uid in user_themes:
            del user_themes[uid]
        if uid in active_games:
            del active_games[uid]
    
    if inactive:
        logger.info(f"🧹 تنظيف {len(inactive)} مستخدم غير نشط")

def is_group_chat(event):
    """Check if message is from a group"""
    return hasattr(event.source, 'group_id')

# ============================================================================
# Flask Routes
# ============================================================================
@app.route("/callback", methods=['POST'])
def callback():
    """LINE webhook callback"""
    signature = request.headers.get('X-Line-Signature', '')
    body = request.get_data(as_text=True)
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        logger.error("❌ Invalid signature")
        abort(400)
    except Exception as e:
        logger.error(f"❌ Callback error: {e}")
        abort(500)
    
    return 'OK'

@app.route("/", methods=['GET'])
def home():
    """Bot status page"""
    cleanup_inactive_users()
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{BOT_NAME} v{BOT_VERSION}</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }}
            
            .container {{
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
                border-radius: 30px;
                padding: 40px;
                max-width: 600px;
                width: 100%;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
                text-align: center;
            }}
            
            h1 {{
                font-size: 3em;
                margin-bottom: 10px;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
            }}
            
            .version {{
                font-size: 0.9em;
                opacity: 0.8;
                margin-bottom: 30px;
            }}
            
            .status {{
                font-size: 1.3em;
                margin: 30px 0;
                padding: 20px;
                background: rgba(255, 255, 255, 0.2);
                border-radius: 20px;
            }}
            
            .stats {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                gap: 20px;
                margin: 30px 0;
            }}
            
            .stat-card {{
                background: rgba(255, 255, 255, 0.2);
                padding: 20px;
                border-radius: 20px;
            }}
            
            .stat-value {{
                font-size: 2.5em;
                font-weight: bold;
                margin: 10px 0;
            }}
            
            .stat-label {{
                font-size: 0.9em;
                opacity: 0.9;
            }}
            
            .footer {{
                margin-top: 30px;
                font-size: 0.85em;
                opacity: 0.7;
            }}
            
            .pulse {{
                animation: pulse 2s infinite;
            }}
            
            @keyframes pulse {{
                0%, 100% {{ opacity: 1; }}
                50% {{ opacity: 0.6; }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎮 {BOT_NAME}</h1>
            <div class="version">Version {BOT_VERSION}</div>
            
            <div class="status pulse">
                ✅ Bot is running smoothly
            </div>
            
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-value">{len(registered_users)}</div>
                    <div class="stat-label">👥 المستخدمين</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{len(AVAILABLE_GAMES)}</div>
                    <div class="stat-label">🎮 الألعاب</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{len(active_games)}</div>
                    <div class="stat-label">⚡ نشط الآن</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{len(gemini_keys)}</div>
                    <div class="stat-label">🤖 AI Keys</div>
                </div>
            </div>
            
            <div class="footer">
                {BOT_RIGHTS}
            </div>
        </div>
    </body>
    </html>
    """

# ============================================================================
# Message Handler
# ============================================================================
@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    """Handle incoming messages"""
    try:
        user_id = event.source.user_id
        text = event.message.text.strip()
        
        if not text:
            return
        
        # Check if in group
        in_group = is_group_chat(event)
        
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            
            # Get user profile
            try:
                profile = line_bot_api.get_profile(user_id)
                username = get_username(profile)
            except:
                username = "مستخدم"
            
            # In groups, only respond to registered users or mentions
            if in_group and "@" not in text.lower():
                if user_id not in registered_users or not registered_users[user_id].get('is_registered'):
                    return
                if user_id not in active_games:
                    return
            
            # Register new user
            if user_id not in registered_users:
                registered_users[user_id] = {
                    "name": username,
                    "points": 0,
                    "is_registered": False,
                    "created_at": datetime.now(),
                    "last_activity": datetime.now()
                }
                logger.info(f"👤 مستخدم جديد: {username}")
                
                current_theme = user_themes.get(user_id, DEFAULT_THEME)
                reply = build_home(current_theme, username, 0, False)
                
                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(reply_token=event.reply_token, messages=[reply])
                )
                return
            
            # Update activity
            update_user_activity(user_id)
            
            # Get user data
            current_theme = user_themes.get(user_id, DEFAULT_THEME)
            user_data = registered_users[user_id]
            reply = None
            
            text_lower = text.lower()
            
            # Command handling
            if text_lower == "بداية" or "@" in text_lower:
                reply = build_home(current_theme, username, user_data['points'], user_data['is_registered'])
            
            elif text_lower == "مساعدة":
                reply = build_games_menu(current_theme)
            
            elif text.startswith("ثيم "):
                theme = text.replace("ثيم ", "").strip()
                from constants import THEMES
                if theme in THEMES:
                    user_themes[user_id] = theme
                    reply = build_home(theme, username, user_data['points'], user_data['is_registered'])
            
            elif text == "انضم":
                registered_users[user_id]["is_registered"] = True
                reply = build_home(current_theme, username, user_data['points'], True)
            
            elif text == "انسحب":
                registered_users[user_id]["is_registered"] = False
                reply = build_home(current_theme, username, user_data['points'], False)
            
            elif text == "نقاطي":
                reply = build_my_points(username, user_data['points'], current_theme)
            
            elif text == "صدارة":
                sorted_users = sorted(
                    [(u["name"], u["points"]) for u in registered_users.values() if u.get("is_registered")],
                    key=lambda x: x[1],
                    reverse=True
                )
                reply = build_leaderboard(sorted_users, current_theme)
            
            elif text == "إيقاف":
                if user_id in active_games:
                    del active_games[user_id]
                    reply = build_games_menu(current_theme)
            
            elif text.startswith("لعبة "):
                if not user_data.get("is_registered"):
                    reply = build_registration_required(current_theme)
                else:
                    game_name = text.replace("لعبة ", "").strip()
                    if game_name in AVAILABLE_GAMES:
                        GameClass = AVAILABLE_GAMES[game_name]
                        game_instance = GameClass(line_bot_api)
                        
                        # Set AI functions for supported games
                        if game_name in ["IQ", "رياضيات", "عكس"]:
                            if hasattr(game_instance, 'ai_generate_question'):
                                game_instance.ai_generate_question = lambda: ai_generate_question(game_name)
                            if hasattr(game_instance, 'ai_check_answer'):
                                game_instance.ai_check_answer = ai_check_answer
                        
                        game_instance.set_theme(current_theme)
                        active_games[user_id] = game_instance
                        reply = game_instance.start_game()
                        
                        logger.info(f"🎮 {username} بدأ لعبة {game_name}")
            
            else:
                # Game answer handling
                if user_id in active_games:
                    game_instance = active_games[user_id]
                    result = game_instance.check_answer(text, user_id, username)
                    
                    if result:
                        # Update points
                        if result.get('points', 0) > 0:
                            registered_users[user_id]['points'] += result['points']
                        
                        # End game if over
                        if result.get('game_over'):
                            del active_games[user_id]
                        
                        reply = result.get('response')
                else:
                    # No active game
                    reply = build_home(current_theme, username, user_data['points'], user_data['is_registered'])
            
            # Send reply
            if reply:
                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(reply_token=event.reply_token, messages=[reply])
                )
                
    except Exception as e:
        logger.error(f"❌ Error in handle_message: {e}", exc_info=True)

# ============================================================================
# Run Application
# ============================================================================
if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    
    logger.info("=" * 60)
    logger.info(f"🚀 Starting {BOT_NAME} v{BOT_VERSION}")
    logger.info(f"📦 Loaded {len(AVAILABLE_GAMES)} games")
    logger.info(f"🤖 AI Keys: {len(gemini_keys)}")
    logger.info(f"🎨 Themes: {len(__import__('constants').THEMES)}")
    logger.info(f"🌐 Server on port {port}")
    logger.info("=" * 60)
    
    app.run(host="0.0.0.0", port=port, debug=False)
