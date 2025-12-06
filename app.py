import os, sys, logging, threading, time, traceback
from datetime import datetime, timedelta
from collections import defaultdict
from flask import Flask, request, abort, jsonify
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi, 
    ReplyMessageRequest, TextMessage, PushMessageRequest
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent

from constants import (
    BOT_NAME, BOT_VERSION, BOT_RIGHTS, LINE_CHANNEL_SECRET, 
    LINE_CHANNEL_ACCESS_TOKEN, validate_env, DEFAULT_THEME, 
    PRIVACY_SETTINGS, get_game_class_name
)
from ui_builder import (
    build_games_menu, build_my_points, build_leaderboard, 
    build_registration_status, build_winner_announcement, build_help_window,
    build_enhanced_home, build_error_message, 
    build_game_stopped, build_team_game_end, build_unregister_confirmation,
    build_registration_required, build_custom_registration
)
from database import get_database

try:
    validate_env()
except Exception as e:
    print(f"Configuration error: {e}")
    sys.exit(1)

app = Flask(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("botmesh")

configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)
db = get_database()

active_games = {}
session_meta = {}
team_mode_state = {}
pending_registrations = {}

RATE_LIMIT = {"max_requests": 30, "window_seconds": 60}
user_rate = defaultdict(list)

class LRUCache:
    def __init__(self, capacity=1000):
        self.cache = {}
        self.capacity = capacity
        self.order = []
        self.lock = threading.Lock()
    
    def get(self, key):
        with self.lock:
            if key in self.cache:
                self.order.remove(key)
                self.order.append(key)
                return self.cache[key]
            return None
    
    def put(self, key, value):
        with self.lock:
            if key in self.cache:
                self.order.remove(key)
            elif len(self.cache) >= self.capacity:
                oldest = self.order.pop(0)
                del self.cache[oldest]
            self.cache[key] = value
            self.order.append(key)
    
    def remove(self, key):
        with self.lock:
            if key in self.cache:
                del self.cache[key]
                self.order.remove(key)

user_cache = LRUCache(capacity=1000)

def is_rate_limited(user_id):
    now = datetime.utcnow()
    window = timedelta(seconds=RATE_LIMIT["window_seconds"])
    user_rate[user_id] = [t for t in user_rate[user_id] if now - t < window]
    if len(user_rate[user_id]) >= RATE_LIMIT["max_requests"]:
        return True
    user_rate[user_id].append(now)
    return False

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
        "ذكاء": IqGame, "روليت": RouletteGame, "لون": WordColorGame,
        "ترتيب": ScrambleWordGame, "أسرع": FastTypingGame, "ضد": OppositeGame,
        "تكوين": LettersWordsGame, "أغنيه": SongGame, "لعبة": HumanAnimalPlantGame,
        "سلسلة": ChainWordsGame, "خمن": GuessGame, "توافق": CompatibilitySystem,
        "مافيا": MafiaGame, "رياضيات": MathGame
    }
    logger.info(f"Loaded {len(AVAILABLE_GAMES)} games")
except Exception as e:
    logger.error(f"Error loading games: {e}")

def get_user_display_name(line_api, user_id):
    try:
        profile = line_api.get_profile(user_id)
        username = None
        
        if hasattr(profile, 'display_name'):
            username = getattr(profile, 'display_name', None)
        
        if not username and isinstance(profile, dict):
            username = profile.get('display_name') or profile.get('displayName')
        
        if username:
            username = str(username).strip()
            if username and len(username) > 0:
                return username[:50]
        
        return None
    except Exception as e:
        logger.error(f"Failed to get profile: {e}")
        return None

def get_user_data(line_api, user_id):
    cached = user_cache.get(user_id)
    if cached:
        cache_time = cached.get('_cache_time', datetime.min)
        if datetime.utcnow() - cache_time < timedelta(minutes=10):
            return cached
    
    user = db.get_user(user_id)
    if not user:
        username = get_user_display_name(line_api, user_id)
        if username:
            db.create_user(user_id, username)
            user = db.get_user(user_id)
    
    if user:
        user['_cache_time'] = datetime.utcnow()
        user_cache.put(user_id, user)
    
    return user

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    except Exception as e:
        logger.error(f"Handler error: {e}")
    return "OK", 200

@app.route("/health", methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "active_games": len(active_games)}), 200

@app.route("/", methods=['GET'])
def status_page():
    stats = db.get_stats_summary()
    return f"""<!DOCTYPE html>
<html>
<head>
    <title>{BOT_NAME}</title>
    <meta charset="utf-8">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', sans-serif;
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
        h1 {{ color: #667eea; margin-bottom: 10px; }}
        .version {{ color: #999; margin-bottom: 20px; }}
        .status {{
            display: inline-block;
            padding: 5px 15px;
            background: #28a745;
            color: white;
            border-radius: 20px;
            font-weight: bold;
            margin: 15px 0;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }}
        .stat {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 15px;
            text-align: center;
        }}
        .stat-value {{
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
            margin: 10px 0;
        }}
        .stat-label {{ color: #666; font-size: 0.9em; }}
        .footer {{
            margin-top: 30px;
            padding-top: 20px;
            border-top: 2px solid #eee;
            text-align: center;
            color: #999;
            font-size: 0.85em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{BOT_NAME}</h1>
        <div class="version">Version {BOT_VERSION}</div>
        <div class="status">ONLINE</div>
        <div class="stats">
            <div class="stat">
                <div class="stat-label">Active Games</div>
                <div class="stat-value">{len(active_games)}</div>
            </div>
            <div class="stat">
                <div class="stat-label">Total Games</div>
                <div class="stat-value">{len(AVAILABLE_GAMES)}</div>
            </div>
            <div class="stat">
                <div class="stat-label">Total Users</div>
                <div class="stat-value">{stats.get('total_users', 0)}</div>
            </div>
            <div class="stat">
                <div class="stat-label">Registered</div>
                <div class="stat-value">{stats.get('registered_users', 0)}</div>
            </div>
        </div>
        <div class="footer">{BOT_RIGHTS}</div>
    </div>
</body>
</html>"""

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    try:
        user_id = event.source.user_id
        text = event.message.text.strip() if event.message.text else ""
        
        if not text or len(text) > 1000 or is_rate_limited(user_id):
            return
        
        source_type = event.source.type
        game_id = (
            event.source.group_id if source_type == "group" else
            event.source.room_id if source_type == "room" else user_id
        )
        
        with ApiClient(configuration) as api_client:
            line_api = MessagingApi(api_client)
            user_data = get_user_data(line_api, user_id)
            
            if not user_data:
                return
            
            username = user_data.get('name', 'مستخدم')
            points = user_data.get('points', 0)
            is_registered = bool(user_data.get('is_registered', 0))
            theme = user_data.get('theme', DEFAULT_THEME)
            
            from constants import normalize_text
            normalized = normalize_text(text)
            
            # Handle registration input
            if user_id in pending_registrations:
                if len(text.strip()) > 0 and len(text.strip()) <= 100:
                    db.update_user_name(user_id, text.strip())
                    db.update_user(user_id, is_registered=1)
                    user_cache.remove(user_id)
                    del pending_registrations[user_id]
                    response = build_registration_status(text.strip(), points, theme)
                else:
                    response = TextMessage(text="اسم غير صالح - حاول مرة اخرى")
                
                line_api.reply_message(
                    ReplyMessageRequest(reply_token=event.reply_token, messages=[response])
                )
                return
            
            # Navigation commands
            if normalized in ["بداية", "home", "start"]:
                mode = team_mode_state.get(game_id, "فردي")
                response = build_enhanced_home(username, points, is_registered, theme, mode)
                line_api.reply_message(
                    ReplyMessageRequest(reply_token=event.reply_token, messages=[response])
                )
                return
            
            if normalized in ["العاب", "games"]:
                top = db.get_top_games(13)
                response = build_games_menu(theme, top)
                line_api.reply_message(
                    ReplyMessageRequest(reply_token=event.reply_token, messages=[response])
                )
                return
            
            if normalized == "مساعدة":
                response = build_help_window(theme)
                line_api.reply_message(
                    ReplyMessageRequest(reply_token=event.reply_token, messages=[response])
                )
                return
            
            if normalized == "نقاطي":
                stats = db.get_user_game_stats(user_id) if is_registered else None
                response = build_my_points(username, points, stats, theme)
                line_api.reply_message(
                    ReplyMessageRequest(reply_token=event.reply_token, messages=[response])
                )
                return
            
            if normalized == "صدارة":
                top = db.get_leaderboard_all(20)
                response = build_leaderboard(top, theme)
                line_api.reply_message(
                    ReplyMessageRequest(reply_token=event.reply_token, messages=[response])
                )
                return
            
            if normalized == "انضم":
                if is_registered:
                    response = TextMessage(text=f"انت مسجل\n{username}\n{points} نقطة")
                else:
                    pending_registrations[user_id] = True
                    response = build_custom_registration(theme)
                line_api.reply_message(
                    ReplyMessageRequest(reply_token=event.reply_token, messages=[response])
                )
                return
            
            if normalized == "انسحب":
                if is_registered:
                    db.update_user(user_id, is_registered=0)
                    user_cache.remove(user_id)
                    response = build_unregister_confirmation(username, points, theme)
                else:
                    response = TextMessage(text="انت غير مسجل")
                line_api.reply_message(
                    ReplyMessageRequest(reply_token=event.reply_token, messages=[response])
                )
                return
            
            if normalized == "ايقاف":
                if game_id in active_games:
                    name = active_games[game_id].game_name
                    del active_games[game_id]
                    response = build_game_stopped(name, theme)
                    line_api.reply_message(
                        ReplyMessageRequest(reply_token=event.reply_token, messages=[response])
                    )
                return
            
            # Theme change
            if text.startswith("ثيم "):
                from constants import THEMES
                t = text.split(maxsplit=1)[1].strip()
                if t in THEMES:
                    db.set_user_theme(user_id, t)
                    user_cache.remove(user_id)
                    mode = team_mode_state.get(game_id, "فردي")
                    response = build_enhanced_home(username, points, is_registered, t, mode)
                else:
                    response = TextMessage(text="ثيم غير موجود")
                line_api.reply_message(
                    ReplyMessageRequest(reply_token=event.reply_token, messages=[response])
                )
                return
            
            # Team mode (groups only)
            if source_type in ["group", "room"]:
                if normalized == "فريقين":
                    team_mode_state[game_id] = "فريقين"
                    response = TextMessage(text="وضع الفريقين مفعل")
                    line_api.reply_message(
                        ReplyMessageRequest(reply_token=event.reply_token, messages=[response])
                    )
                    return
                
                if normalized == "فردي":
                    team_mode_state[game_id] = "فردي"
                    response = TextMessage(text="الوضع الفردي مفعل")
                    line_api.reply_message(
                        ReplyMessageRequest(reply_token=event.reply_token, messages=[response])
                    )
                    return
            
            # Start game
            game_name = get_game_class_name(text)
            if game_name in AVAILABLE_GAMES:
                # Special games
                if game_name in ["توافق", "مافيا"]:
                    if game_name == "مافيا" and source_type not in ["group", "room"]:
                        response = TextMessage(text="المافيا للمجموعات فقط")
                        line_api.reply_message(
                            ReplyMessageRequest(reply_token=event.reply_token, messages=[response])
                        )
                        return
                    
                    GameClass = AVAILABLE_GAMES[game_name]
                    game = GameClass(line_api)
                    if hasattr(game, 'set_theme'):
                        game.set_theme(theme)
                    active_games[game_id] = game
                    msg = game.start_game()
                    line_api.reply_message(
                        ReplyMessageRequest(reply_token=event.reply_token, messages=[msg])
                    )
                    return
                
                # Regular games require registration
                if not is_registered:
                    response = build_registration_required(theme)
                    line_api.reply_message(
                        ReplyMessageRequest(reply_token=event.reply_token, messages=[response])
                    )
                    return
                
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
                
                session_id = db.create_game_session(
                    user_id, game_name, 
                    mode="teams" if team_mode else "solo",
                    team_mode=1 if team_mode else 0
                )
                
                if game_id not in session_meta:
                    session_meta[game_id] = {}
                session_meta[game_id]["session_id"] = session_id
                session_meta[game_id]["team_mode"] = team_mode
                
                msg = game.start_game()
                line_api.reply_message(
                    ReplyMessageRequest(reply_token=event.reply_token, messages=[msg])
                )
                return
            
            # Handle game answer
            if game_id in active_games:
                game = active_games[game_id]
                meta = session_meta.get(game_id, {})
                
                if game.team_mode and not game.is_user_joined(user_id):
                    team = game.join_user(user_id)
                    if meta.get("session_id"):
                        db.add_team_member(meta["session_id"], user_id, team)
                
                result = game.check_answer(text, user_id, username)
                if result:
                    pts = result.get('points', 0)
                    if pts > 0:
                        if game.team_mode:
                            team = result.get('team', 'team1')
                            if meta.get("session_id"):
                                db.add_team_points(meta["session_id"], team, 1)
                        else:
                            db.add_points(user_id, 1)
                            db.record_game_stat(user_id, game.game_name, 1, result.get('game_over', False))
                    
                    messages = []
                    msg_text = result.get('message', '')
                    if msg_text:
                        messages.append(TextMessage(text=msg_text))
                    
                    if result.get('game_over'):
                        if game.team_mode:
                            tp = db.get_team_points(meta["session_id"]) if meta.get("session_id") else game.team_scores
                            winner = build_team_game_end(tp, theme)
                            messages.append(winner)
                        else:
                            fresh = get_user_data(line_api, user_id)
                            total = fresh.get('points', points)
                            winner = build_winner_announcement(username, game.game_name, pts, total, theme)
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
                            ReplyMessageRequest(reply_token=event.reply_token, messages=messages)
                        )
    
    except Exception as e:
        logger.error(f"Error: {e}")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)
