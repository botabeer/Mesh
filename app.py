# Bot Mesh - Main Application with Enhanced Debugging
# Created by: Abeer Aldosari © 2025

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
# Logging Setup
# =============================================================================
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('bot_mesh.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

# =============================================================================
# Imports with Error Handling
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
# In-Memory Databases
# =============================================================================
registered_users = {}
user_themes = {}
active_games = {}

logger.info("✅ In-memory databases initialized")

# =============================================================================
# Dynamic Game Imports
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
    try:
        return profile.display_name
    except:
        return "مستخدم"

def clean_old_data():
    try:
        current_time = datetime.now()
        to_delete = []
        for user_id, data in registered_users.items():
            if 'last_activity' in data:
                inactive_days = (current_time - data['last_activity']).days
                if inactive_days >= BOT_SETTINGS.get('auto_delete_after_days', 7):
                    to_delete.append(user_id)
        for user_id in to_delete:
            del registered_users[user_id]
            user_themes.pop(user_id, None)
            active_games.pop(user_id, None)
            logger.info(f"🗑️ Deleted inactive user: {user_id}")
    except Exception as e:
        logger.error(f"❌ Error in clean_old_data: {e}")

def update_user_activity(user_id):
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
    signature = request.headers.get('X-Line-Signature', '')
    body = request.get_data(as_text=True)
    logger.debug(f"📥 Received callback request: {len(body)} bytes")
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
    return f"<h1>{BOT_NAME} is running ✅</h1>"

@app.route("/debug", methods=['GET'])
def debug_status():
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
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

# =============================================================================
# Message Handler
# =============================================================================
@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    try:
        user_id = event.source.user_id
        text = (event.message.text or "").strip()
        if not text:
            logger.warning("⚠️ Empty message received")
            return

        clean_old_data()
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            try:
                profile = line_bot_api.get_profile(user_id)
                username = get_username(profile)
            except:
                username = "مستخدم"

            if user_id not in registered_users:
                registered_users[user_id] = {
                    "name": username,
                    "points": 0,
                    "is_registered": False,
                    "created_at": datetime.now(),
                    "last_activity": datetime.now()
                }

            update_user_activity(user_id)
            current_theme = user_themes.get(user_id, DEFAULT_THEME)
            user_data = registered_users[user_id]
            reply = None

            # Commands handling
            cmd = text.lower()
            if cmd == "home":
                reply = UIBuilder.build_home(current_theme, username, user_data['points'], user_data['is_registered'])
            elif cmd in ["games", "info"]:
                if cmd == "games":
                    reply = UIBuilder.build_games_menu(current_theme)
                else:
                    reply = UIBuilder.build_info(current_theme)
            elif text.startswith("ثيم "):
                theme = text.replace("ثيم ", "").strip()
                if theme in THEMES:
                    user_themes[user_id] = theme
                    reply = UIBuilder.build_home(theme, username, user_data['points'], user_data['is_registered'])
                else:
                    reply = TextMessage(text="⚠️ الثيم غير متوفر")
            elif text == "انضم":
                registered_users[user_id]["is_registered"] = True
                reply = TextMessage(text=f"✅ مرحباً {username}! تم تسجيلك بنجاح")
            elif text == "انسحب":
                registered_users[user_id]["is_registered"] = False
                reply = TextMessage(text=f"👋 {username} تم إلغاء تسجيلك بنجاح")
            elif text == "نقاطي":
                reply = UIBuilder.build_my_points(username, user_data['points'], current_theme)
            elif text == "صدارة":
                sorted_users = sorted(
                    [(u["name"], u["points"]) for u in registered_users.values() if u.get("is_registered")],
                    key=lambda x: x[1], reverse=True
                )
                reply = UIBuilder.build_leaderboard(sorted_users, current_theme)
            elif text == "إيقاف":
                active_games.pop(user_id, None)
                reply = TextMessage(text="⏹️ تم إيقاف اللعبة الحالية")
            elif text.startswith("لعبة "):
                game_name = text.replace("لعبة ", "").strip()
                if not user_data.get("is_registered"):
                    reply = TextMessage(text="⚠️ يجب التسجيل أولاً باستخدام زر 'انضم'")
                elif game_name in AVAILABLE_GAMES:
                    GameClass = AVAILABLE_GAMES[game_name]
                    try:
                        game_instance = GameClass(line_bot_api)
                        game_instance.set_theme(current_theme)
                        active_games[user_id] = game_instance
                        reply = game_instance.start_game()
                    except Exception as e:
                        logger.error(f"❌ Error starting game {game_name}: {e}")
                        reply = TextMessage(text=f"❌ حدث خطأ في تشغيل اللعبة")
                else:
                    reply = TextMessage(text=f"⚠️ اللعبة '{game_name}' غير متوفرة")
            else:
                if user_id in active_games:
                    game_instance = active_games[user_id]
                    try:
                        result = game_instance.check_answer(text, user_id, username)
                        if result:
                            registered_users[user_id]['points'] += result.get('points', 0)
                            if result.get('game_over', False):
                                active_games.pop(user_id, None)
                            reply = result.get('response')
                    except Exception as e:
                        logger.error(f"❌ Error processing game answer: {e}")
                        reply = TextMessage(text="❌ حدث خطأ في معالجة إجابتك")
                else:
                    reply = TextMessage(text=f"مرحباً {username}! 👋\nاضغط على 'Home' للبدء أو 'Games' لعرض الألعاب 🎮")

            if reply:
                try:
                    line_bot_api.reply_message_with_http_info(
                        ReplyMessageRequest(reply_token=event.reply_token, messages=[reply])
                    )
                except Exception as e:
                    logger.error(f"❌ Failed to send message: {e}")

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
    logger.info(f"🚀 Starting {BOT_NAME} on port {port}")
    app.run(host="0.0.0.0", port=port, debug=False)
