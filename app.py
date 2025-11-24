"""
Bot Mesh - Main Application with Enhanced Debugging
Created by: Abeer Aldosari © 2025
"""

import os
import sys
import logging
import traceback
from datetime import datetime, timedelta
from flask import Flask, request, abort, jsonify

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# =============================================================================
# Enhanced Logging Setup
# =============================================================================
logging.basicConfig(
    level=logging.DEBUG,  # تغيير إلى DEBUG لعرض كل التفاصيل
    format='%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('bot_mesh.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

# =============================================================================
# Import with Error Handling
# =============================================================================
try:
    from linebot.v3 import WebhookHandler
    from linebot.v3.exceptions import InvalidSignatureError
    from linebot.v3.messaging import (
        Configuration,
        ApiClient,
        MessagingApi,
        ReplyMessageRequest,
        TextMessage
    )
    from linebot.v3.webhooks import MessageEvent, TextMessageContent
    logger.info("✅ LINE SDK imported successfully")
except ImportError as e:
    logger.error(f"❌ Failed to import LINE SDK: {e}")
    sys.exit(1)

try:
    from config import (
        BOT_NAME,
        LINE_CHANNEL_SECRET,
        LINE_CHANNEL_ACCESS_TOKEN,
        GEMINI_API_KEYS,
        AI_ENABLED,
        BOT_SETTINGS,
        GAMES_LIST
    )
    logger.info("✅ Config imported successfully")
except ImportError as e:
    logger.error(f"❌ Failed to import config: {e}")
    sys.exit(1)

try:
    from theme_styles import THEMES, DEFAULT_THEME, FIXED_BUTTONS
    from ui_builder import UIBuilder
    logger.info("✅ UI components imported successfully")
except ImportError as e:
    logger.error(f"❌ Failed to import UI components: {e}")
    sys.exit(1)

# =============================================================================
# Flask Setup
# =============================================================================
app = Flask(__name__)

# =============================================================================
# LINE Configuration
# =============================================================================
try:
    configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)
    handler = WebhookHandler(LINE_CHANNEL_SECRET)
    logger.info("✅ LINE configuration initialized")
except Exception as e:
    logger.error(f"❌ Failed to initialize LINE: {e}")
    sys.exit(1)

# =============================================================================
# In-Memory Database
# =============================================================================
registered_users = {}
user_themes = {}
active_games = {}

logger.info("✅ In-memory databases initialized")

# =============================================================================
# Game Classes Import (Dynamic with Error Handling)
# =============================================================================
AVAILABLE_GAMES = {}

game_imports = {
    "IQ": ("games.iq_game", "IqGame"),
    "رياضيات": ("games.math_game", "MathGame"),
    "لون الكلمة": ("games.word_color_game", "WordColorGame"),
    "كلمة مبعثرة": ("games.scramble_word_game", "ScrambleWordGame"),
    "كتابة سريعة": ("games.fast_typing_game", "FastTypingGame"),
    "عكس": ("games.opposite_game", "OppositeGame"),
    "حروف وكلمات": ("games.letters_words_game", "LettersWordsGame"),
    "أغنية": ("games.song_game", "SongGame"),
    "إنسان حيوان نبات": ("games.human_animal_plant_game", "HumanAnimalPlantGame"),
    "سلسلة كلمات": ("games.chain_words_game", "ChainWordsGame"),
    "تخمين": ("games.guess_game", "GuessGame"),
    "توافق": ("games.compatibility_game", "CompatibilityGame")
}

for game_name, (module_path, class_name) in game_imports.items():
    try:
        module = __import__(module_path, fromlist=[class_name])
        game_class = getattr(module, class_name)
        AVAILABLE_GAMES[game_name] = game_class
        logger.info(f"✅ Loaded game: {game_name}")
    except ImportError as e:
        logger.warning(f"⚠️ Could not import {game_name}: {e}")
    except AttributeError as e:
        logger.warning(f"⚠️ Class {class_name} not found in {module_path}: {e}")
    except Exception as e:
        logger.error(f"❌ Unexpected error loading {game_name}: {e}")

logger.info(f"📊 Loaded {len(AVAILABLE_GAMES)}/{len(game_imports)} games successfully")

if len(AVAILABLE_GAMES) == 0:
    logger.error("❌ No games loaded! Bot cannot function properly")

# =============================================================================
# Helper Functions
# =============================================================================

def get_username(profile):
    """Get username from LINE profile"""
    try:
        return profile.display_name
    except:
        return "مستخدم"

def clean_old_data():
    """Delete user data after 7 days of inactivity"""
    try:
        current_time = datetime.now()
        to_delete = []
        
        for user_id, data in registered_users.items():
            if 'last_activity' in data:
                inactive_days = (current_time - data['last_activity']).days
                if inactive_days >= BOT_SETTINGS['auto_delete_after_days']:
                    to_delete.append(user_id)
        
        for user_id in to_delete:
            del registered_users[user_id]
            if user_id in user_themes:
                del user_themes[user_id]
            if user_id in active_games:
                del active_games[user_id]
            logger.info(f"🗑️ Deleted inactive user: {user_id}")
    except Exception as e:
        logger.error(f"❌ Error in clean_old_data: {e}")

def update_user_activity(user_id):
    """Update last activity timestamp"""
    try:
        if user_id in registered_users:
            registered_users[user_id]['last_activity'] = datetime.now()
    except Exception as e:
        logger.error(f"❌ Error updating user activity: {e}")

# =============================================================================
# Flask Routes
# =============================================================================

@app.route("/callback", methods=['POST'])
def callback():
    """LINE Webhook Callback"""
    signature = request.headers.get('X-Line-Signature', '')
    body = request.get_data(as_text=True)
    
    logger.debug(f"📥 Received callback request")
    logger.debug(f"Signature: {signature[:20]}...")
    logger.debug(f"Body length: {len(body)} bytes")
    
    try:
        handler.handle(body, signature)
        logger.debug("✅ Handler processed successfully")
    except InvalidSignatureError:
        logger.error("❌ Invalid signature!")
        abort(400)
    except Exception as e:
        logger.error(f"❌ Error handling request: {e}")
        logger.error(traceback.format_exc())
        abort(500)
    
    return 'OK'

@app.route("/", methods=['GET'])
def home():
    """Simple status page"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{BOT_NAME}</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
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
                background: rgba(255,255,255,0.1);
                backdrop-filter: blur(10px);
                padding: 40px;
                border-radius: 20px;
                max-width: 600px;
                width: 100%;
                box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            }}
            h1 {{
                font-size: 2.5em;
                margin-bottom: 20px;
                text-align: center;
            }}
            .status {{
                text-align: center;
                font-size: 1.2em;
                margin: 20px 0;
            }}
            .stats {{
                background: rgba(255,255,255,0.2);
                padding: 20px;
                border-radius: 10px;
                margin-top: 30px;
            }}
            .stat-item {{
                display: flex;
                justify-content: space-between;
                padding: 10px 0;
                border-bottom: 1px solid rgba(255,255,255,0.2);
            }}
            .stat-item:last-child {{ border-bottom: none; }}
            .footer {{
                text-align: center;
                margin-top: 20px;
                font-size: 0.8em;
                opacity: 0.7;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 {BOT_NAME}</h1>
            <div class="status">✅ Bot is running successfully</div>
            
            <div class="stats">
                <div class="stat-item">
                    <span><strong>Registered Users:</strong></span>
                    <span>{len(registered_users)}</span>
                </div>
                <div class="stat-item">
                    <span><strong>Available Games:</strong></span>
                    <span>{len(AVAILABLE_GAMES)}</span>
                </div>
                <div class="stat-item">
                    <span><strong>Active Games:</strong></span>
                    <span>{len(active_games)}</span>
                </div>
                <div class="stat-item">
                    <span><strong>AI Features:</strong></span>
                    <span>{'✅ Enabled' if AI_ENABLED else '❌ Disabled'}</span>
                </div>
                <div class="stat-item">
                    <span><strong>Silent Mode:</strong></span>
                    <span>{'❌ Disabled' if not BOT_SETTINGS['silent_mode'] else '✅ Enabled'}</span>
                </div>
            </div>
            
            <div class="footer">
                تم إنشاء هذا البوت بواسطة عبير الدوسري © 2025
            </div>
        </div>
    </body>
    </html>
    """

@app.route("/debug", methods=['GET'])
def debug_status():
    """Debug endpoint for monitoring"""
    return jsonify({
        "status": "running",
        "registered_users": len(registered_users),
        "active_games": len(active_games),
        "available_games": list(AVAILABLE_GAMES.keys()),
        "ai_enabled": AI_ENABLED,
        "silent_mode": BOT_SETTINGS.get('silent_mode', False)
    })

@app.route("/health", methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

# =============================================================================
# Message Handler
# =============================================================================

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    """Handle incoming messages"""
    try:
        user_id = event.source.user_id
        text = event.message.text.strip()
        
        logger.info(f"📨 Message from {user_id}: {text[:50]}...")
        
        if not text:
            logger.warning("⚠️ Empty message received")
            return
        
        clean_old_data()
        
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            
            try:
                profile = line_bot_api.get_profile(user_id)
                username = get_username(profile)
                logger.debug(f"✅ Got profile: {username}")
            except Exception as e:
                logger.warning(f"⚠️ Failed to get user profile: {e}")
                username = "مستخدم"
            
            # ✅ إرسال رسالة ترحيب للمستخدمين الجدد
            if user_id not in registered_users:
                registered_users[user_id] = {
                    "name": username,
                    "points": 0,
                    "is_registered": False,
                    "created_at": datetime.now(),
                    "last_activity": datetime.now()
                }
                logger.info(f"✅ New user: {username} ({user_id})")
                
                # إرسال نافذة Home تلقائياً
                current_theme = user_themes.get(user_id, DEFAULT_THEME)
                welcome_reply = UIBuilder.build_home(current_theme, username, 0, False)
                
                try:
                    line_bot_api.reply_message_with_http_info(
                        ReplyMessageRequest(
                            reply_token=event.reply_token,
                            messages=[welcome_reply]
                        )
                    )
                    logger.info(f"✅ Sent welcome message to {username}")
                    return
                except Exception as e:
                    logger.error(f"❌ Failed to send welcome message: {e}")
                    logger.error(traceback.format_exc())
            
            update_user_activity(user_id)
            
            current_theme = user_themes.get(user_id, DEFAULT_THEME)
            user_data = registered_users[user_id]
            
            reply = None
            
            text_lower = text.lower()
            
            # ================== FIXED BUTTONS ==================
            if text_lower == "home":
                logger.debug("🏠 Home button pressed")
                reply = UIBuilder.build_home(
                    current_theme,
                    username,
                    user_data['points'],
                    user_data['is_registered']
                )
                
            elif text_lower in ["games", "info"]:
                logger.debug(f"📋 {text_lower} button pressed")
                if text_lower == "games":
                    reply = UIBuilder.build_games_menu(current_theme)
                else:
                    reply = UIBuilder.build_info(current_theme)
                    
            # ================== THEME SELECTION ==================
            elif text.startswith("ثيم "):
                theme = text.replace("ثيم ", "").strip()
                logger.debug(f"🎨 Theme change requested: {theme}")
                if theme in THEMES:
                    user_themes[user_id] = theme
                    reply = UIBuilder.build_home(
                        theme,
                        username,
                        user_data['points'],
                        user_data['is_registered']
                    )
                    logger.info(f"✅ Theme changed to {theme} for {username}")
                else:
                    reply = TextMessage(text="⚠️ الثيم غير متوفر")
                    
            # ================== USER MANAGEMENT ==================
            elif text == "انضم":
                logger.debug(f"➕ Registration for {username}")
                registered_users[user_id]["is_registered"] = True
                reply = TextMessage(text=f"✅ مرحباً {username}! تم تسجيلك بنجاح\nيمكنك الآن اختيار لعبة من قائمة الألعاب")
                
            elif text == "انسحب":
                logger.debug(f"➖ Unregistration for {username}")
                if user_id in registered_users:
                    registered_users[user_id]["is_registered"] = False
                    reply = TextMessage(text=f"👋 {username} تم إلغاء تسجيلك بنجاح")
                    
            elif text == "نقاطي":
                logger.debug(f"📊 Points request from {username}")
                reply = UIBuilder.build_my_points(
                    username,
                    user_data['points'],
                    current_theme
                )
                
            elif text == "صدارة":
                logger.debug("🏆 Leaderboard request")
                sorted_users = sorted(
                    [(u["name"], u["points"]) for u in registered_users.values() if u.get("is_registered")],
                    key=lambda x: x[1],
                    reverse=True
                )
                reply = UIBuilder.build_leaderboard(sorted_users, current_theme)
                
            # ================== GAME CONTROL ==================
            elif text == "إيقاف":
                logger.debug(f"⏸️ Stop game request from {username}")
                if user_id in active_games:
                    del active_games[user_id]
                    reply = TextMessage(text="⏹️ تم إيقاف اللعبة الحالية")
                else:
                    reply = TextMessage(text="⚠️ لا توجد لعبة نشطة")
                    
            # ================== START GAME ==================
            elif text.startswith("لعبة "):
                game_name = text.replace("لعبة ", "").strip()
                logger.debug(f"🎮 Game start request: {game_name} by {username}")
                
                if not user_data.get("is_registered"):
                    reply = TextMessage(text="⚠️ يجب التسجيل أولاً باستخدام زر 'انضم'")
                    logger.warning(f"⚠️ Unregistered user tried to play: {username}")
                else:
                    if game_name in AVAILABLE_GAMES:
                        GameClass = AVAILABLE_GAMES[game_name]
                        try:
                            game_instance = GameClass(line_bot_api)
                            game_instance.set_theme(current_theme)
                            active_games[user_id] = game_instance
                            
                            reply = game_instance.start_game()
                            logger.info(f"✅ {username} started game: {game_name}")
                        except Exception as e:
                            logger.error(f"❌ Error starting game {game_name}: {e}")
                            logger.error(traceback.format_exc())
                            reply = TextMessage(text=f"❌ حدث خطأ في تشغيل اللعبة")
                    else:
                        reply = TextMessage(text=f"⚠️ اللعبة '{game_name}' غير متوفرة")
                        logger.warning(f"⚠️ Game not found: {game_name}")
                        
            # ================== GAME RESPONSES ==================
            else:
                if user_id in active_games:
                    logger.debug(f"🎯 Processing game answer from {username}")
                    game_instance = active_games[user_id]
                    
                    try:
                        result = game_instance.check_answer(text, user_id, username)
                        
                        if result:
                            if result.get('points', 0) > 0:
                                registered_users[user_id]['points'] += result['points']
                                logger.info(f"✅ {username} earned {result['points']} points")
                            
                            if result.get('game_over', False):
                                del active_games[user_id]
                                logger.info(f"🏁 Game ended for {username}")
                            
                            reply = result.get('response')
                            
                    except Exception as e:
                        logger.error(f"❌ Error processing game answer: {e}")
                        logger.error(traceback.format_exc())
                        reply = TextMessage(text="❌ حدث خطأ في معالجة إجابتك")
                else:
                    # ✅ رسالة توجيهية بدلاً من التجاهل
                    reply = TextMessage(text=f"مرحباً {username}! 👋\nاضغط على 'Home' للبدء أو 'Games' لعرض الألعاب 🎮")
                    logger.debug(f"ℹ️ Sent guidance message to {username}")
            
            # Send reply
            if reply:
                try:
                    line_bot_api.reply_message_with_http_info(
                        ReplyMessageRequest(
                            reply_token=event.reply_token,
                            messages=[reply]
                        )
                    )
                    logger.info(f"✅ Reply sent to {username}")
                except Exception as e:
                    logger.error(f"❌ Failed to send message: {e}")
                    logger.error(traceback.format_exc())
            else:
                logger.warning("⚠️ No reply generated")
                
    except Exception as e:
        logger.error(f"❌ General error in message handler: {e}")
        logger.error(traceback.format_exc())

# =============================================================================
# Error Handlers
# =============================================================================

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not Found"}), 404

@app.errorhandler(500)
def internal_error(e):
    logger.error(f"❌ Internal server error: {e}")
    return jsonify({"error": "Internal Server Error"}), 500

# =============================================================================
# Run Application
# =============================================================================

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    
    logger.info("=" * 60)
    logger.info(f"🚀 Starting {BOT_NAME} on port {port}")
    logger.info("=" * 60)
    logger.info(f"📦 Loaded {len(AVAILABLE_GAMES)} games: {list(AVAILABLE_GAMES.keys())}")
    logger.info(f"🎨 Available themes: {len(THEMES)}")
    logger.info(f"🤖 AI Features: {'Enabled' if AI_ENABLED else 'Disabled'}")
    logger.info(f"🔇 Silent Mode: {'Disabled' if not BOT_SETTINGS['silent_mode'] else 'Enabled'}")
    logger.info(f"👥 Registered Only: {'Yes' if BOT_SETTINGS.get('registered_users_only') else 'No'}")
    logger.info("=" * 60)
    
    app.run(host="0.0.0.0", port=port, debug=False)
