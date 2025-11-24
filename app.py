"""
Bot Mesh - Main Application
Created by: Abeer Aldosari © 2025
"""

import os
import sys
import logging
from datetime import datetime, timedelta
from flask import Flask, request, abort

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

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

from config import (
    BOT_NAME,
    LINE_CHANNEL_SECRET,
    LINE_CHANNEL_ACCESS_TOKEN,
    GEMINI_API_KEYS,
    AI_ENABLED,
    BOT_SETTINGS,
    GAMES_LIST
)

from theme_styles import THEMES, DEFAULT_THEME, FIXED_BUTTONS
from ui_builder import UIBuilder

# =============================================================================
# Flask Setup
# =============================================================================
app = Flask(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# =============================================================================
# LINE Configuration
# =============================================================================
configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# =============================================================================
# In-Memory Database
# =============================================================================
registered_users = {}
user_themes = {}
active_games = {}

# =============================================================================
# Game Classes Import (Dynamic)
# =============================================================================
AVAILABLE_GAMES = {}

try:
    from games.iq_game import IqGame
    AVAILABLE_GAMES["IQ"] = IqGame
except ImportError as e:
    logger.warning(f"⚠️ Could not import IqGame: {e}")

try:
    from games.math_game import MathGame
    AVAILABLE_GAMES["رياضيات"] = MathGame
except ImportError as e:
    logger.warning(f"⚠️ Could not import MathGame: {e}")

try:
    from games.word_color_game import WordColorGame
    AVAILABLE_GAMES["لون الكلمة"] = WordColorGame
except ImportError as e:
    logger.warning(f"⚠️ Could not import WordColorGame: {e}")

try:
    from games.scramble_word_game import ScrambleWordGame
    AVAILABLE_GAMES["كلمة مبعثرة"] = ScrambleWordGame
except ImportError as e:
    logger.warning(f"⚠️ Could not import ScrambleWordGame: {e}")

try:
    from games.fast_typing_game import FastTypingGame
    AVAILABLE_GAMES["كتابة سريعة"] = FastTypingGame
except ImportError as e:
    logger.warning(f"⚠️ Could not import FastTypingGame: {e}")

try:
    from games.opposite_game import OppositeGame
    AVAILABLE_GAMES["عكس"] = OppositeGame
except ImportError as e:
    logger.warning(f"⚠️ Could not import OppositeGame: {e}")

try:
    from games.letters_words_game import LettersWordsGame
    AVAILABLE_GAMES["حروف وكلمات"] = LettersWordsGame
except ImportError as e:
    logger.warning(f"⚠️ Could not import LettersWordsGame: {e}")

try:
    from games.song_game import SongGame
    AVAILABLE_GAMES["أغنية"] = SongGame
except ImportError as e:
    logger.warning(f"⚠️ Could not import SongGame: {e}")

try:
    from games.human_animal_plant_game import HumanAnimalPlantGame
    AVAILABLE_GAMES["إنسان حيوان نبات"] = HumanAnimalPlantGame
except ImportError as e:
    logger.warning(f"⚠️ Could not import HumanAnimalPlantGame: {e}")

try:
    from games.chain_words_game import ChainWordsGame
    AVAILABLE_GAMES["سلسلة كلمات"] = ChainWordsGame
except ImportError as e:
    logger.warning(f"⚠️ Could not import ChainWordsGame: {e}")

try:
    from games.guess_game import GuessGame
    AVAILABLE_GAMES["تخمين"] = GuessGame
except ImportError as e:
    logger.warning(f"⚠️ Could not import GuessGame: {e}")

try:
    from games.compatibility_game import CompatibilityGame
    AVAILABLE_GAMES["توافق"] = CompatibilityGame
except ImportError as e:
    logger.warning(f"⚠️ Could not import CompatibilityGame: {e}")

logger.info(f"✅ Loaded {len(AVAILABLE_GAMES)} games successfully")

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

def update_user_activity(user_id):
    """Update last activity timestamp"""
    if user_id in registered_users:
        registered_users[user_id]['last_activity'] = datetime.now()

# =============================================================================
# Flask Routes
# =============================================================================

@app.route("/callback", methods=['POST'])
def callback():
    """LINE Webhook Callback"""
    signature = request.headers.get('X-Line-Signature', '')
    body = request.get_data(as_text=True)
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        logger.error("⚠️ Invalid signature")
        abort(400)
    except Exception as e:
        logger.error(f"❌ Error handling request: {e}")
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

# =============================================================================
# Message Handler
# =============================================================================

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    """Handle incoming messages"""
    try:
        user_id = event.source.user_id
        text = event.message.text.strip()
        
        if not text:
            return
        
        clean_old_data()
        
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            
            try:
                profile = line_bot_api.get_profile(user_id)
                username = get_username(profile)
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
                    return
                except Exception as e:
                    logger.error(f"❌ Failed to send welcome message: {e}")
            
            update_user_activity(user_id)
            
            current_theme = user_themes.get(user_id, DEFAULT_THEME)
            user_data = registered_users[user_id]
            
            reply = None
            
            text_lower = text.lower()
            
            # ================== FIXED BUTTONS ==================
            if text_lower == "home":
                reply = UIBuilder.build_home(
                    current_theme,
                    username,
                    user_data['points'],
                    user_data['is_registered']
                )
                
            elif text_lower in ["games", "info"]:
                if text_lower == "games":
                    reply = UIBuilder.build_games_menu(current_theme)
                else:
                    reply = UIBuilder.build_info(current_theme)
                    
            # ================== THEME SELECTION ==================
            elif text.startswith("ثيم "):
                theme = text.replace("ثيم ", "").strip()
                if theme in THEMES:
                    user_themes[user_id] = theme
                    reply = UIBuilder.build_home(
                        theme,
                        username,
                        user_data['points'],
                        user_data['is_registered']
                    )
                else:
                    reply = TextMessage(text="⚠️ الثيم غير متوفر")
                    
            # ================== USER MANAGEMENT ==================
            elif text == "انضم":
                registered_users[user_id]["is_registered"] = True
                reply = TextMessage(text=f"✅ مرحباً {username}! تم تسجيلك بنجاح\nيمكنك الآن اختيار لعبة من قائمة الألعاب")
                
            elif text == "انسحب":
                if user_id in registered_users:
                    registered_users[user_id]["is_registered"] = False
                    reply = TextMessage(text=f"👋 {username} تم إلغاء تسجيلك بنجاح")
                    
            elif text == "نقاطي":
                reply = UIBuilder.build_my_points(
                    username,
                    user_data['points'],
                    current_theme
                )
                
            elif text == "صدارة":
                sorted_users = sorted(
                    [(u["name"], u["points"]) for u in registered_users.values() if u.get("is_registered")],
                    key=lambda x: x[1],
                    reverse=True
                )
                reply = UIBuilder.build_leaderboard(sorted_users, current_theme)
                
            # ================== GAME CONTROL ==================
            elif text == "إيقاف":
                if user_id in active_games:
                    del active_games[user_id]
                    reply = TextMessage(text="⏹️ تم إيقاف اللعبة الحالية")
                else:
                    reply = TextMessage(text="⚠️ لا توجد لعبة نشطة")
                    
            # ================== START GAME ==================
            elif text.startswith("لعبة "):
                if not user_data.get("is_registered"):
                    reply = TextMessage(text="⚠️ يجب التسجيل أولاً باستخدام زر 'انضم'")
                else:
                    game_name = text.replace("لعبة ", "").strip()
                    
                    if game_name in AVAILABLE_GAMES:
                        GameClass = AVAILABLE_GAMES[game_name]
                        try:
                            game_instance = GameClass(line_bot_api)
                            game_instance.set_theme(current_theme)
                            active_games[user_id] = game_instance
                            
                            reply = game_instance.start_game()
                            logger.info(f"🎮 {username} started game: {game_name}")
                        except Exception as e:
                            logger.error(f"❌ Error starting game {game_name}: {e}")
                            reply = TextMessage(text=f"❌ حدث خطأ في تشغيل اللعبة")
                    else:
                        reply = TextMessage(text=f"⚠️ اللعبة '{game_name}' غير متوفرة")
                        
            # ================== GAME RESPONSES ==================
            else:
                if user_id in active_games:
                    game_instance = active_games[user_id]
                    
                    try:
                        result = game_instance.check_answer(text, user_id, username)
                        
                        if result:
                            if result.get('points', 0) > 0:
                                registered_users[user_id]['points'] += result['points']
                            
                            if result.get('game_over', False):
                                del active_games[user_id]
                            
                            reply = result.get('response')
                            
                    except Exception as e:
                        logger.error(f"❌ Error processing game answer: {e}")
                        reply = TextMessage(text="❌ حدث خطأ في معالجة إجابتك")
                else:
                    # ✅ رسالة توجيهية بدلاً من التجاهل
                    reply = TextMessage(text=f"مرحباً {username}! 👋\nاضغط على 'Home' للبدء أو 'Games' لعرض الألعاب 🎮")
            
            # Send reply
            if reply:
                try:
                    line_bot_api.reply_message_with_http_info(
                        ReplyMessageRequest(
                            reply_token=event.reply_token,
                            messages=[reply]
                        )
                    )
                except Exception as e:
                    logger.error(f"❌ Failed to send message: {e}")
            else:
                logger.warning("⚠️ No reply generated")
                
    except Exception as e:
        logger.error(f"❌ General error in message handler: {e}", exc_info=True)

# =============================================================================
# Run Application
# =============================================================================

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    logger.info(f"🚀 Starting {BOT_NAME} on port {port}")
    logger.info(f"📦 Loaded {len(AVAILABLE_GAMES)} games")
    logger.info(f"🎨 Available themes: {len(THEMES)}")
    logger.info(f"🤖 AI Features: {'Enabled' if AI_ENABLED else 'Disabled'}")
    logger.info(f"🔇 Silent Mode: {'Disabled' if not BOT_SETTINGS['silent_mode'] else 'Enabled'}")
    
    app.run(host="0.0.0.0", port=port, debug=False)
