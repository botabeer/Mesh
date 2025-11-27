"""
Bot Mesh - Enhanced LINE Bot Application v3.1
Created by: Abeer Aldosari © 2025

Key Improvements:
✅ Auto game loading via game_loader
✅ Better error handling
✅ Enhanced AI integration
✅ Improved memory management
✅ LINE-optimized responses
✅ Group chat support
✅ Smarter caching
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

# Import enhanced constants
from constants import (
    BOT_NAME, BOT_VERSION, BOT_RIGHTS,
    LINE_CHANNEL_SECRET, LINE_CHANNEL_ACCESS_TOKEN,
    GEMINI_API_KEY_1, GEMINI_API_KEY_2, GEMINI_API_KEY_3,
    validate_env, get_username, GAME_LIST, DEFAULT_THEME,
    sanitize_user_input, get_user_level
)

from ui_builder import (
    build_home, build_games_menu, build_my_points,
    build_leaderboard, build_registration_required
)

# Import game loader
from games.game_loader import games_list

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

# Enhanced logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('bot_mesh.log') if os.path.exists('/tmp') else logging.NullHandler()
    ]
)
logger = logging.getLogger(__name__)

configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# ============================================================================
# In-Memory Storage (Enhanced)
# ============================================================================
registered_users = {}  # {user_id: {name, points, is_registered, created_at, last_activity}}
user_themes = {}       # {user_id: theme_emoji}
active_games = {}      # {user_id: game_instance}

# Statistics
stats = {
    "total_games_played": 0,
    "total_messages": 0,
    "start_time": datetime.now()
}

# ============================================================================
# Game Loading System (Auto via game_loader)
# ============================================================================
AVAILABLE_GAMES = {}

# Load games automatically
for game_class in games_list:
    try:
        game_name = game_class.__name__.replace('Game', '').replace('_', ' ').title()
        
        # Match with GAME_LIST
        matched_key = None
        for key in GAME_LIST.keys():
            if key.lower() in game_name.lower() or game_name.lower() in key.lower():
                matched_key = key
                break
        
        # Try alternative matching
        if not matched_key:
            name_map = {
                'Iq': 'IQ',
                'Math': 'رياضيات',
                'WordColor': 'لون الكلمة',
                'ScrambleWord': 'كلمة مبعثرة',
                'FastTyping': 'كتابة سريعة',
                'Opposite': 'عكس',
                'LettersWords': 'حروف وكلمات',
                'Song': 'أغنية',
                'HumanAnimalPlant': 'إنسان حيوان نبات',
                'ChainWords': 'سلسلة كلمات',
                'Guess': 'تخمين',
                'Compatibility': 'توافق'
            }
            
            for eng, ar in name_map.items():
                if eng.lower() in game_class.__name__.lower():
                    matched_key = ar
                    break
        
        if matched_key:
            AVAILABLE_GAMES[matched_key] = game_class
            logger.info(f"✅ Loaded: {matched_key} -> {game_class.__name__}")
        else:
            logger.warning(f"⚠️ Could not match: {game_class.__name__}")
            
    except Exception as e:
        logger.error(f"❌ Error loading {game_class.__name__}: {e}")

logger.info(f"📊 Total games loaded: {len(AVAILABLE_GAMES)}/{len(GAME_LIST)}")

# ============================================================================
# Enhanced AI Integration
# ============================================================================
current_gemini_key = 0
gemini_keys = [k for k in [GEMINI_API_KEY_1, GEMINI_API_KEY_2, GEMINI_API_KEY_3] if k]

# AI Response cache (to reduce API calls)
ai_cache = {}

def get_next_gemini_key():
    """Rotate through available Gemini API keys"""
    global current_gemini_key
    if not gemini_keys:
        logger.warning("⚠️ No Gemini API keys available")
        return None
    
    key = gemini_keys[current_gemini_key % len(gemini_keys)]
    current_gemini_key += 1
    return key

def ai_generate_question(game_type, force_new=False):
    """
    Generate question using Gemini AI with intelligent caching
    
    Args:
        game_type: Type of game
        force_new: Force new generation (skip cache)
        
    Returns:
        dict: Question data or None
    """
    # Check cache first
    cache_key = f"{game_type}_{datetime.now().hour}"
    if not force_new and cache_key in ai_cache:
        logger.info(f"📦 Using cached AI question for {game_type}")
        return ai_cache[cache_key].copy()
    
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
        
        result = json.loads(text.strip())
        
        # Cache the result
        ai_cache[cache_key] = result.copy()
        
        logger.info(f"🤖 Generated AI question for {game_type}")
        return result
        
    except Exception as e:
        logger.error(f"❌ AI generation error: {e}")
        return None

def ai_check_answer(correct_answer, user_answer):
    """
    Validate answer using Gemini AI with caching
    
    Args:
        correct_answer: The correct answer
        user_answer: User's answer
        
    Returns:
        bool: True if correct
    """
    # Quick check first
    from constants import normalize_arabic
    if normalize_arabic(correct_answer) == normalize_arabic(user_answer):
        return True
    
    # Check cache
    cache_key = f"{normalize_arabic(correct_answer)}_{normalize_arabic(user_answer)}"
    if cache_key in ai_cache:
        return ai_cache[cache_key]
    
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
        result = 'نعم' in answer_text or 'yes' in answer_text
        
        # Cache result
        ai_cache[cache_key] = result
        
        return result
        
    except Exception as e:
        logger.error(f"❌ AI check error: {e}")
        return False

# ============================================================================
# Helper Functions (Enhanced)
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
        logger.info(f"🧹 Cleaned {len(inactive)} inactive users")

def is_group_chat(event):
    """Check if message is from a group"""
    return hasattr(event.source, 'group_id')

def get_bot_stats():
    """Get bot statistics"""
    uptime = datetime.now() - stats["start_time"]
    return {
        "users": len(registered_users),
        "active_games": len(active_games),
        "games_played": stats["total_games_played"],
        "messages": stats["total_messages"],
        "uptime_hours": uptime.total_seconds() / 3600
    }

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
        logger.error(f"❌ Callback error: {e}", exc_info=True)
        abort(500)
    
    return 'OK'

@app.route("/", methods=['GET'])
def home():
    """Enhanced bot status page"""
    cleanup_inactive_users()
    bot_stats = get_bot_stats()
    
    return f"""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>{BOT_NAME} v{BOT_VERSION}</title>
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
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(20px);
                border-radius: 30px;
                padding: 40px;
                max-width: 800px;
                width: 100%;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            }}
            h1 {{ font-size: 3em; margin-bottom: 10px; text-align: center; }}
            .version {{ text-align: center; opacity: 0.8; margin-bottom: 30px; }}
            .status {{
                background: rgba(72, 187, 120, 0.2);
                padding: 20px;
                border-radius: 15px;
                text-align: center;
                font-size: 1.2em;
                margin: 20px 0;
            }}
            .stats {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                gap: 20px;
                margin: 30px 0;
            }}
            .stat-card {{
                background: rgba(255, 255, 255, 0.15);
                padding: 20px;
                border-radius: 15px;
                text-align: center;
            }}
            .stat-value {{ font-size: 2.5em; font-weight: bold; margin: 10px 0; }}
            .stat-label {{ font-size: 0.9em; opacity: 0.9; }}
            .footer {{ margin-top: 30px; text-align: center; font-size: 0.85em; opacity: 0.7; }}
            .pulse {{ animation: pulse 2s infinite; }}
            @keyframes pulse {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.6; }} }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎮 {BOT_NAME}</h1>
            <div class="version">الإصدار {BOT_VERSION}</div>
            
            <div class="status pulse">✅ البوت يعمل بكفاءة</div>
            
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-value">{bot_stats['users']}</div>
                    <div class="stat-label">👥 المستخدمون</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{len(AVAILABLE_GAMES)}</div>
                    <div class="stat-label">🎮 الألعاب</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{bot_stats['active_games']}</div>
                    <div class="stat-label">⚡ نشط الآن</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{len(gemini_keys)}</div>
                    <div class="stat-label">🤖 AI Keys</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{bot_stats['games_played']}</div>
                    <div class="stat-label">🏆 العاب منتهية</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{bot_stats['uptime_hours']:.1f}</div>
                    <div class="stat-label">⏱️ ساعات العمل</div>
                </div>
            </div>
            
            <div class="footer">{BOT_RIGHTS}</div>
        </div>
    </body>
    </html>
    """

@app.route("/health", methods=['GET'])
def health():
    """Health check endpoint"""
    return {"status": "healthy", "version": BOT_VERSION}, 200

# ============================================================================
# Message Handler (Enhanced)
# ============================================================================

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    """Handle incoming messages with enhanced logic"""
    try:
        user_id = event.source.user_id
        text = sanitize_user_input(event.message.text)
        
        if not text:
            return
        
        # Update stats
        stats["total_messages"] += 1
        
        # Check if in group
        in_group = is_group_chat(event)
        
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            
            # Get user profile
            try:
                profile = line_bot_api.get_profile(user_id)
                username = get_username(profile)
            except Exception:
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
                logger.info(f"👤 New user: {username}")
                
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
                from constants import is_valid_theme
                if is_valid_theme(theme):
                    user_themes[user_id] = theme
                    reply = build_home(theme, username, user_data['points'], user_data['is_registered'])
            
            elif text == "انضم":
                registered_users[user_id]["is_registered"] = True
                reply = build_home(current_theme, username, user_data['points'], True)
            
            elif text == "انسحب":
                registered_users[user_id]["is_registered"] = False
                if user_id in active_games:
                    del active_games[user_id]
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
                        
                        logger.info(f"🎮 {username} started {game_name}")
            
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
                            stats["total_games_played"] += 1
                        
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
    
    logger.info("=" * 70)
    logger.info(f"🚀 Starting {BOT_NAME} v{BOT_VERSION}")
    logger.info(f"📦 Loaded {len(AVAILABLE_GAMES)}/{len(GAME_LIST)} games")
    logger.info(f"🤖 AI Keys: {len(gemini_keys)}")
    logger.info(f"🎨 Themes: {len(__import__('constants').THEMES)}")
    logger.info(f"🌐 Server on port {port}")
    logger.info("=" * 70)
    
    # Auto cleanup every hour
    from threading import Thread
    import time
    
    def auto_cleanup():
        while True:
            time.sleep(3600)  # 1 hour
            cleanup_inactive_users()
            logger.info("🧹 Auto cleanup completed")
    
    cleanup_thread = Thread(target=auto_cleanup, daemon=True)
    cleanup_thread.start()
    
    app.run(host="0.0.0.0", port=port, debug=False)
