# ============================================================================
# app.py - Fixed for Render with proper error handling
# ============================================================================

import os
import sys
import logging
import threading
import time
from datetime import datetime, timedelta
from collections import defaultdict
from flask import Flask, request, abort, jsonify
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi, 
    ReplyMessageRequest, TextMessage
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent

# Import configurations
from constants import (
    BOT_NAME, BOT_VERSION, LINE_CHANNEL_SECRET, 
    LINE_CHANNEL_ACCESS_TOKEN, validate_env, DEFAULT_THEME,
    normalize_text, get_game_class_name
)
from ui_builder import (
    build_games_menu, build_my_points, build_leaderboard,
    build_enhanced_home, build_help_window, build_registration_status,
    build_unregister_confirmation, build_registration_required,
    build_custom_registration, build_game_stopped, build_winner_announcement,
    build_team_game_end
)
from database import get_database

# Validate environment
try:
    validate_env()
except Exception as e:
    print(f"Config error: {e}")
    sys.exit(1)

# Initialize Flask
app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("botmesh")
logging.getLogger('linebot').setLevel(logging.WARNING)
logging.getLogger('werkzeug').setLevel(logging.WARNING)

# Initialize LINE SDK
configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)
db = get_database()

# Global state
active_games = {}
session_meta = {}
team_mode_state = {}
pending_registrations = {}
user_rate = defaultdict(list)

RATE_LIMIT = {"max_requests": 30, "window_seconds": 60}

# Simple cache
class SimpleCache:
    def __init__(self, max_size=1000):
        self.cache = {}
        self.max_size = max_size
        self.lock = threading.Lock()
    
    def get(self, key):
        with self.lock:
            return self.cache.get(key)
    
    def put(self, key, value):
        with self.lock:
            if len(self.cache) >= self.max_size:
                # Remove oldest
                oldest = next(iter(self.cache))
                del self.cache[oldest]
            self.cache[key] = value
    
    def remove(self, key):
        with self.lock:
            self.cache.pop(key, None)

user_cache = SimpleCache()

# Rate limiting
def is_rate_limited(user_id):
    now = datetime.utcnow()
    window = timedelta(seconds=RATE_LIMIT["window_seconds"])
    user_rate[user_id] = [t for t in user_rate[user_id] if now - t < window]
    
    if len(user_rate[user_id]) >= RATE_LIMIT["max_requests"]:
        return True
    
    user_rate[user_id].append(now)
    return False

# Load games
AVAILABLE_GAMES = {}
try:
    from games.iq_game import IqGame
    from games.roulette_game import RouletteGame
    from games.word_color_game import WordColorGame
    from games.scramble_word_game import ScrambleWordGame
    from games.fast_typing_game import FastTypingGame
    from games.opposite_game import OppositeGame
    from games.letters_words_game import LettersWordsGame
    from games.song_game import SongGame
    from games.human_animal_plant_game import HumanAnimalPlantGame
    from games.chain_words_game import ChainWordsGame
    from games.guess_game import GuessGame
    from games.compatibility_game import CompatibilitySystem
    from games.mafia_game import MafiaGame
    from games.math_game import MathGame
    
    AVAILABLE_GAMES = {
        "ذكاء": IqGame,
        "روليت": RouletteGame,
        "لون": WordColorGame,
        "ترتيب": ScrambleWordGame,
        "أسرع": FastTypingGame,
        "ضد": OppositeGame,
        "تكوين": LettersWordsGame,
        "أغنيه": SongGame,
        "لعبة": HumanAnimalPlantGame,
        "سلسلة": ChainWordsGame,
        "خمن": GuessGame,
        "توافق": CompatibilitySystem,
        "مافيا": MafiaGame,
        "رياضيات": MathGame
    }
    logger.info(f"Loaded {len(AVAILABLE_GAMES)} games")
except Exception as e:
    logger.error(f"Error loading games: {e}")

# Helper functions
def get_user_display_name(line_api, user_id):
    try:
        profile = line_api.get_profile(user_id)
        
        if hasattr(profile, 'display_name'):
            name = profile.display_name
        elif isinstance(profile, dict):
            name = profile.get('display_name') or profile.get('displayName')
        else:
            return None
        
        if name and isinstance(name, str):
            return name.strip()[:50]
        
        return None
    except Exception as e:
        logger.error(f"Profile error: {e}")
        return None

def get_user_data(line_api, user_id):
    # Check cache first
    cached = user_cache.get(user_id)
    if cached:
        cache_time = cached.get('_cache_time', datetime.min)
        if datetime.utcnow() - cache_time < timedelta(minutes=5):
            return cached
    
    # Get from database
    user = db.get_user(user_id)
    
    if not user:
        # Create new user
        username = get_user_display_name(line_api, user_id)
        if username:
            db.create_user(user_id, username)
            user = db.get_user(user_id)
    
    if user:
        user['_cache_time'] = datetime.utcnow()
        user_cache.put(user_id, user)
    
    return user

# Routes
@app.route("/", methods=['GET'])
def home():
    try:
        stats = db.get_stats_summary()
        return f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{BOT_NAME}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }}
        .container {{
            max-width: 800px;
            width: 100%;
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }}
        h1 {{ color: #667eea; margin-bottom: 10px; font-size: 2.5em; }}
        .version {{ color: #999; margin-bottom: 20px; }}
        .status {{
            display: inline-block;
            padding: 8px 20px;
            background: #28a745;
            color: white;
            border-radius: 25px;
            font-weight: bold;
            margin: 15px 0;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }}
        .stat {{
            background: #f8f9fa;
            padding: 25px;
            border-radius: 15px;
            text-align: center;
            border: 2px solid #e9ecef;
        }}
        .stat-value {{
            font-size: 2.5em;
            font-weight: bold;
            color: #667eea;
            margin: 10px 0;
        }}
        .stat-label {{ color: #666; font-size: 0.9em; text-transform: uppercase; }}
        .footer {{
            margin-top: 30px;
            padding-top: 20px;
            border-top: 2px solid #eee;
            text-align: center;
            color: #999;
        }}
        .info {{
            background: #e7f3ff;
            padding: 15px;
            border-radius: 10px;
            margin: 20px 0;
            border-left: 4px solid #667eea;
        }}
        .info strong {{ color: #667eea; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{BOT_NAME}</h1>
        <div class="version">الإصدار {BOT_VERSION}</div>
        <div class="status">متصل</div>
        
        <div class="info">
            <strong>حالة السيرفر:</strong> يعمل بشكل طبيعي<br>
            <strong>الاستجابة:</strong> سريعة<br>
            <strong>قاعدة البيانات:</strong> متصلة
        </div>
        
        <div class="stats">
            <div class="stat">
                <div class="stat-label">الالعاب النشطة</div>
                <div class="stat-value">{len(active_games)}</div>
            </div>
            <div class="stat">
                <div class="stat-label">اجمالي الالعاب</div>
                <div class="stat-value">{len(AVAILABLE_GAMES)}</div>
            </div>
            <div class="stat">
                <div class="stat-label">المستخدمين</div>
                <div class="stat-value">{stats.get('total_users', 0)}</div>
            </div>
            <div class="stat">
                <div class="stat-label">المسجلين</div>
                <div class="stat-value">{stats.get('registered_users', 0)}</div>
            </div>
        </div>
        
        <div class="footer">
            جميع الحقوق محفوظة - عبير الدوسري 2025
        </div>
    </div>
</body>
</html>"""
    except Exception as e:
        logger.error(f"Home error: {e}")
        return "Bot is running", 200

@app.route("/health", methods=['GET'])
def health():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "games": len(active_games),
        "users": len(user_cache.cache)
    }), 200

@app.route("/callback", methods=['POST'])
def callback():
    # Get signature
    signature = request.headers.get('X-Line-Signature', '')
    
    # Get request body
    body = request.get_data(as_text=True)
    
    # Log for debugging
    logger.info("Received webhook request")
    
    try:
        # Handle webhook
        handler.handle(body, signature)
    except InvalidSignatureError:
        logger.warning("Invalid signature")
        abort(400)
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        # Don't abort - return 200 to avoid retries
        return "OK", 200
    
    return "OK", 200

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    try:
        # Get user info
        user_id = event.source.user_id
        text = event.message.text.strip() if event.message.text else ""
        
        # Validate input
        if not text or len(text) > 1000:
            return
        
        # Rate limit
        if is_rate_limited(user_id):
            return
        
        # Determine context
        source_type = event.source.type
        if source_type == "group":
            game_id = event.source.group_id
        elif source_type == "room":
            game_id = event.source.room_id
        else:
            game_id = user_id
        
        # Process with LINE API
        with ApiClient(configuration) as api_client:
            line_api = MessagingApi(api_client)
            
            # Get user data
            user_data = get_user_data(line_api, user_id)
            if not user_data:
                return
            
            username = user_data.get('name', 'مستخدم')
            points = user_data.get('points', 0)
            is_registered = bool(user_data.get('is_registered', 0))
            theme = user_data.get('theme', DEFAULT_THEME)
            
            # Normalize input
            normalized = normalize_text(text)
            
            # Handle registration
            if user_id in pending_registrations:
                if 0 < len(text) <= 100:
                    db.update_user_name(user_id, text)
                    db.update_user(user_id, is_registered=1)
                    user_cache.remove(user_id)
                    del pending_registrations[user_id]
                    msg = build_registration_status(text, points, theme)
                else:
                    msg = TextMessage(text="اسم غير صالح")
                
                line_api.reply_message(
                    ReplyMessageRequest(reply_token=event.reply_token, messages=[msg])
                )
                return
            
            # Navigation commands
            if normalized in ["بداية", "home", "start"]:
                mode = team_mode_state.get(game_id, "فردي")
                msg = build_enhanced_home(username, points, is_registered, theme, mode)
                line_api.reply_message(
                    ReplyMessageRequest(reply_token=event.reply_token, messages=[msg])
                )
                return
            
            if normalized in ["العاب", "games"]:
                top = db.get_top_games(13)
                msg = build_games_menu(theme, top)
                line_api.reply_message(
                    ReplyMessageRequest(reply_token=event.reply_token, messages=[msg])
                )
                return
            
            if normalized == "مساعدة":
                msg = build_help_window(theme)
                line_api.reply_message(
                    ReplyMessageRequest(reply_token=event.reply_token, messages=[msg])
                )
                return
            
            if normalized == "نقاطي":
                stats = db.get_user_game_stats(user_id) if is_registered else None
                msg = build_my_points(username, points, stats, theme)
                line_api.reply_message(
                    ReplyMessageRequest(reply_token=event.reply_token, messages=[msg])
                )
                return
            
            if normalized == "صدارة":
                top = db.get_leaderboard_all(20)
                msg = build_leaderboard(top, theme)
                line_api.reply_message(
                    ReplyMessageRequest(reply_token=event.reply_token, messages=[msg])
                )
                return
            
            if normalized == "انضم":
                if is_registered:
                    msg = TextMessage(text=f"مسجل: {username}\nالنقاط: {points}")
                else:
                    pending_registrations[user_id] = True
                    msg = build_custom_registration(theme)
                
                line_api.reply_message(
                    ReplyMessageRequest(reply_token=event.reply_token, messages=[msg])
                )
                return
            
            if normalized == "انسحب":
                if is_registered:
                    db.update_user(user_id, is_registered=0)
                    user_cache.remove(user_id)
                    msg = build_unregister_confirmation(username, points, theme)
                else:
                    msg = TextMessage(text="غير مسجل")
                
                line_api.reply_message(
                    ReplyMessageRequest(reply_token=event.reply_token, messages=[msg])
                )
                return
            
            if normalized == "ايقاف":
                if game_id in active_games:
                    name = active_games[game_id].game_name
                    del active_games[game_id]
                    msg = build_game_stopped(name, theme)
                    line_api.reply_message(
                        ReplyMessageRequest(reply_token=event.reply_token, messages=[msg])
                    )
                return
            
            # Theme change
            if text.startswith("ثيم "):
                from constants import THEMES
                theme_name = text.split(maxsplit=1)[1].strip()
                if theme_name in THEMES:
                    db.set_user_theme(user_id, theme_name)
                    user_cache.remove(user_id)
                    mode = team_mode_state.get(game_id, "فردي")
                    msg = build_enhanced_home(username, points, is_registered, theme_name, mode)
                else:
                    msg = TextMessage(text="ثيم غير موجود")
                
                line_api.reply_message(
                    ReplyMessageRequest(reply_token=event.reply_token, messages=[msg])
                )
                return
            
            # Team mode
            if source_type in ["group", "room"]:
                if normalized == "فريقين":
                    team_mode_state[game_id] = "فريقين"
                    msg = TextMessage(text="وضع الفريقين")
                    line_api.reply_message(
                        ReplyMessageRequest(reply_token=event.reply_token, messages=[msg])
                    )
                    return
                
                if normalized == "فردي":
                    team_mode_state[game_id] = "فردي"
                    msg = TextMessage(text="الوضع الفردي")
                    line_api.reply_message(
                        ReplyMessageRequest(reply_token=event.reply_token, messages=[msg])
                    )
                    return
            
            # Start game
            game_name = get_game_class_name(text)
            if game_name in AVAILABLE_GAMES:
                # Special games
                if game_name == "مافيا" and source_type not in ["group", "room"]:
                    msg = TextMessage(text="المافيا للمجموعات فقط")
                    line_api.reply_message(
                        ReplyMessageRequest(reply_token=event.reply_token, messages=[msg])
                    )
                    return
                
                # توافق doesn't require registration
                if game_name == "توافق":
                    GameClass = AVAILABLE_GAMES[game_name]
                    game = GameClass(line_api)
                    if hasattr(game, 'set_theme'):
                        game.set_theme(theme)
                    active_games[game_id] = game
                    question = game.start_game()
                    line_api.reply_message(
                        ReplyMessageRequest(reply_token=event.reply_token, messages=[question])
                    )
                    return
                
                # Other games require registration
                if not is_registered:
                    msg = build_registration_required(theme)
                    line_api.reply_message(
                        ReplyMessageRequest(reply_token=event.reply_token, messages=[msg])
                    )
                    return
                
                # Create game
                team_mode = (
                    team_mode_state.get(game_id, "فردي") == "فريقين"
                    if source_type in ["group", "room"] else False
                )
                
                GameClass = AVAILABLE_GAMES[game_name]
                game = GameClass(line_api)
                
                if hasattr(game, 'set_theme'):
                    game.set_theme(theme)
                if hasattr(game, 'set_database'):
                    game.set_database(db)
                
                game.team_mode = team_mode
                if team_mode:
                    game.supports_hint = False
                    game.supports_reveal = False
                
                active_games[game_id] = game
                
                # Create session
                if game_name != "مافيا":
                    sid = db.create_game_session(
                        user_id, game_name,
                        mode="teams" if team_mode else "solo",
                        team_mode=1 if team_mode else 0
                    )
                    session_meta[game_id] = {
                        "session_id": sid,
                        "team_mode": team_mode
                    }
                
                question = game.start_game()
                line_api.reply_message(
                    ReplyMessageRequest(reply_token=event.reply_token, messages=[question])
                )
                return
            
            # Handle game answer
            if game_id in active_games:
                game = active_games[game_id]
                meta = session_meta.get(game_id, {})
                
                # Team mode join
                if game.team_mode and not game.is_user_joined(user_id):
                    team = game.join_user(user_id)
                    if meta.get("session_id"):
                        db.add_team_member(meta["session_id"], user_id, team)
                
                # Check answer
                result = game.check_answer(text, user_id, username)
                
                if result:
                    pts = result.get('points', 0)
                    
                    # Award points
                    if pts > 0:
                        if game.team_mode:
                            team = result.get('team', 'team1')
                            if meta.get("session_id"):
                                db.add_team_points(meta["session_id"], team, 1)
                        else:
                            db.add_points(user_id, 1)
                            db.record_game_stat(
                                user_id, game.game_name, 1,
                                result.get('game_over', False)
                            )
                    
                    # Build response
                    messages = []
                    
                    msg_text = result.get('message', '')
                    if msg_text:
                        messages.append(TextMessage(text=msg_text))
                    
                    if result.get('game_over'):
                        if game.team_mode:
                            tp = (
                                db.get_team_points(meta["session_id"])
                                if meta.get("session_id")
                                else game.team_scores
                            )
                            winner = build_team_game_end(tp, theme)
                            messages.append(winner)
                        else:
                            fresh = get_user_data(line_api, user_id)
                            total = fresh.get('points', points)
                            winner = build_winner_announcement(
                                username, game.game_name, pts, total, theme
                            )
                            messages.append(winner)
                        
                        if meta.get("session_id"):
                            db.finish_session(meta["session_id"], pts)
                        
                        del active_games[game_id]
                        if game_id in session_meta:
                            del session_meta[game_id]
                    
                    elif result.get('response'):
                        messages.append(result['response'])
                    
                    if messages:
                        line_api.reply_message(
                            ReplyMessageRequest(
                                reply_token=event.reply_token,
                                messages=messages
                            )
                        )
    
    except Exception as e:
        logger.error(f"Handler error: {e}")
        # Don't raise - just log

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    logger.info(f"Starting on port {port}")
    app.run(host="0.0.0.0", port=port, debug=False, threaded=True)
