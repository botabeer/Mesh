# app.py
"""
Bot Mesh - LINE Bot Application v8.0 ENHANCED (Complete app.py)
تم إنشاء هذا البوت بواسطة عبير الدوسري © 2025

ميزات مضافة:
- نظام SQLite مدمج (users, sessions, games, teams, logs)
- نظام فريقين (Join/Leave, حساب نقاط للفرق فقط)
- قبول الإجابات فقط من المنضمين في وضع الفريقين
- تعطيل 'لمح' و'جاوب' في وضع الفريقين
- عدّاد وقت ⏱️ لكل جولة (قابل للتعديل)
- مستكشف أخطاء مع endpoint لعرض الـ logs
- تكامل مع UI & Games الموجودة (games/*.py و ui_builder.py)
"""

import os
import sys
import logging
import sqlite3
import threading
import time
import json
import traceback
import random
from datetime import datetime, timedelta
from collections import defaultdict

from flask import Flask, request, abort, jsonify

# LINE SDK v3 imports (assumes installed)
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi,
    ReplyMessageRequest, QuickReply, QuickReplyItem,
    MessageAction, TextMessage
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent

# Import your constants and UI builder (from previous files)
from constants import (
    BOT_NAME, BOT_VERSION, BOT_RIGHTS,
    LINE_CHANNEL_SECRET, LINE_CHANNEL_ACCESS_TOKEN,
    validate_env, get_username, GAME_LIST, DEFAULT_THEME, THEMES,
    FIXED_ACTIONS, FIXED_GAME_QR, GAME_CONFIG
)

from ui_builder import (
    build_games_menu, build_my_points, build_leaderboard,
    build_registration_required, build_winner_announcement,
    build_help_window, build_theme_selector, build_enhanced_home,
    build_multiplayer_help_window, build_percentage_result
)

# -------------------------
# Basic configuration check
# -------------------------
try:
    validate_env()
except Exception as e:
    print(f"Configuration error: {e}")
    # continue but LINE calls will fail if env missing
    # sys.exit(1)

# Flask & LINE Setup
app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("botmesh")
logger.setLevel(logging.INFO)

configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# -------------------------
# Simple SQLite DB helper
# -------------------------
DB_PATH = os.getenv("BOT_DB_PATH", "botmesh.db")
DB_LOCK = threading.Lock()

class Database:
    def __init__(self, path=DB_PATH):
        self.path = path
        self._ensure_schema()

    def _conn(self):
        return sqlite3.connect(self.path, check_same_thread=False)

    def _ensure_schema(self):
        with DB_LOCK:
            conn = self._conn()
            c = conn.cursor()
            # users: id (line user id), name, points, is_registered, theme, last_active
            c.execute("""CREATE TABLE IF NOT EXISTS users(
                user_id TEXT PRIMARY KEY,
                name TEXT,
                points INTEGER DEFAULT 0,
                is_registered INTEGER DEFAULT 0,
                theme TEXT DEFAULT ?,
                last_active TIMESTAMP
            )""", (DEFAULT_THEME,))
            # sessions: game sessions (for persistence)
            c.execute("""CREATE TABLE IF NOT EXISTS sessions(
                session_id INTEGER PRIMARY KEY AUTOINCREMENT,
                game_id TEXT,
                owner_id TEXT,
                created_at TIMESTAMP,
                finished_at TIMESTAMP,
                mode TEXT, -- "solo" or "teams"
                team_mode INTEGER DEFAULT 0,
                extra TEXT
            )""")
            # teams: map session_id -> team_name -> points
            c.execute("""CREATE TABLE IF NOT EXISTS teams(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER,
                team_name TEXT,
                points INTEGER DEFAULT 0
            )""")
            # team_members: session_id, user_id, team_name
            c.execute("""CREATE TABLE IF NOT EXISTS team_members(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER,
                user_id TEXT,
                team_name TEXT
            )""")
            # game_stats: aggregated stats
            c.execute("""CREATE TABLE IF NOT EXISTS game_stats(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                game_name TEXT,
                points INTEGER,
                played_at TIMESTAMP
            )""")
            # logs
            c.execute("""CREATE TABLE IF NOT EXISTS logs(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ts TIMESTAMP,
                level TEXT,
                message TEXT,
                traceback TEXT
            )""")
            conn.commit()
            conn.close()

    # user helpers
    def get_user(self, user_id):
        with DB_LOCK:
            conn = self._conn()
            c = conn.cursor()
            c.execute("SELECT user_id, name, points, is_registered, theme, last_active FROM users WHERE user_id=?", (user_id,))
            row = c.fetchone()
            conn.close()
            if not row:
                return None
            return {
                "user_id": row[0],
                "name": row[1],
                "points": row[2],
                "is_registered": bool(row[3]),
                "theme": row[4],
                "last_active": row[5]
            }

    def create_user(self, user_id, name):
        with DB_LOCK:
            conn = self._conn()
            c = conn.cursor()
            c.execute("INSERT OR IGNORE INTO users(user_id, name, points, is_registered, theme, last_active) VALUES(?,?,?,?,?,?)",
                      (user_id, name, 0, 0, DEFAULT_THEME, datetime.utcnow()))
            conn.commit()
            conn.close()

    def update_user_name(self, user_id, name):
        with DB_LOCK:
            conn = self._conn()
            c = conn.cursor()
            c.execute("UPDATE users SET name=?, last_active=? WHERE user_id=?", (name, datetime.utcnow(), user_id))
            conn.commit()
            conn.close()

    def update_activity(self, user_id):
        with DB_LOCK:
            conn = self._conn()
            c = conn.cursor()
            c.execute("UPDATE users SET last_active=? WHERE user_id=?", (datetime.utcnow(), user_id))
            conn.commit()
            conn.close()

    def update_user(self, user_id, **kwargs):
        keys = []
        vals = []
        for k, v in kwargs.items():
            keys.append(f"{k}=?")
            vals.append(v)
        vals.append(user_id)
        with DB_LOCK:
            conn = self._conn()
            c = conn.cursor()
            c.execute(f"UPDATE users SET {', '.join(keys)} WHERE user_id=?", tuple(vals))
            conn.commit()
            conn.close()

    def add_points(self, user_id, points):
        with DB_LOCK:
            conn = self._conn()
            c = conn.cursor()
            c.execute("UPDATE users SET points = COALESCE(points,0) + ?, last_active=? WHERE user_id=?",
                      (points, datetime.utcnow(), user_id))
            conn.commit()
            conn.close()

    # sessions & teams
    def create_game_session(self, owner_id, game_id, mode="solo", team_mode=0, extra=None):
        with DB_LOCK:
            conn = self._conn()
            c = conn.cursor()
            c.execute("INSERT INTO sessions(game_id, owner_id, created_at, mode, team_mode, extra) VALUES(?,?,?,?,?,?)",
                      (game_id, owner_id, datetime.utcnow(), mode, team_mode, json.dumps(extra) if extra else None))
            session_id = c.lastrowid
            # if team_mode create two teams
            if team_mode:
                c.execute("INSERT INTO teams(session_id, team_name, points) VALUES(?,?,?)", (session_id, "team1", 0))
                c.execute("INSERT INTO teams(session_id, team_name, points) VALUES(?,?,?)", (session_id, "team2", 0))
            conn.commit()
            conn.close()
            return session_id

    def add_team_member(self, session_id, user_id, team_name):
        with DB_LOCK:
            conn = self._conn()
            c = conn.cursor()
            # avoid duplicates
            c.execute("SELECT id FROM team_members WHERE session_id=? AND user_id=?", (session_id, user_id))
            if c.fetchone():
                conn.close()
                return
            c.execute("INSERT INTO team_members(session_id, user_id, team_name) VALUES(?,?,?)", (session_id, user_id, team_name))
            conn.commit()
            conn.close()

    def remove_team_member(self, session_id, user_id):
        with DB_LOCK:
            conn = self._conn()
            c = conn.cursor()
            c.execute("DELETE FROM team_members WHERE session_id=? AND user_id=?", (session_id, user_id))
            conn.commit()
            conn.close()

    def get_team_members(self, session_id):
        with DB_LOCK:
            conn = self._conn()
            c = conn.cursor()
            c.execute("SELECT user_id, team_name FROM team_members WHERE session_id=?", (session_id,))
            rows = c.fetchall()
            conn.close()
            return [{"user_id": r[0], "team": r[1]} for r in rows]

    def add_team_points(self, session_id, team_name, points):
        with DB_LOCK:
            conn = self._conn()
            c = conn.cursor()
            c.execute("UPDATE teams SET points = points + ? WHERE session_id=? AND team_name=?", (points, session_id, team_name))
            conn.commit()
            conn.close()

    def get_team_points(self, session_id):
        with DB_LOCK:
            conn = self._conn()
            c = conn.cursor()
            c.execute("SELECT team_name, points FROM teams WHERE session_id=?", (session_id,))
            rows = c.fetchall()
            conn.close()
            return {r[0]: r[1] for r in rows}

    def finish_session(self, session_id):
        with DB_LOCK:
            conn = self._conn()
            c = conn.cursor()
            c.execute("UPDATE sessions SET finished_at=? WHERE session_id=?", (datetime.utcnow(), session_id))
            conn.commit()
            conn.close()

    # stats
    def record_game_stat(self, user_id, game_name, points):
        with DB_LOCK:
            conn = self._conn()
            c = conn.cursor()
            c.execute("INSERT INTO game_stats(user_id, game_name, points, played_at) VALUES(?,?,?,?)",
                      (user_id, game_name, points, datetime.utcnow()))
            conn.commit()
            conn.close()

    def get_leaderboard(self, limit=10):
        with DB_LOCK:
            conn = self._conn()
            c = conn.cursor()
            c.execute("SELECT user_id, name, points FROM users ORDER BY points DESC LIMIT ?", (limit,))
            rows = c.fetchall()
            conn.close()
            return [(r[1] or r[0], r[2]) for r in rows]

    # logs
    def log(self, level, message, tb=None):
        with DB_LOCK:
            conn = self._conn()
            c = conn.cursor()
            c.execute("INSERT INTO logs(ts, level, message, traceback) VALUES(?,?,?,?)",
                      (datetime.utcnow(), level, message, tb))
            conn.commit()
            conn.close()

    def get_logs(self, limit=200):
        with DB_LOCK:
            conn = self._conn()
            c = conn.cursor()
            c.execute("SELECT ts, level, message, traceback FROM logs ORDER BY ts DESC LIMIT ?", (limit,))
            rows = c.fetchall()
            conn.close()
            return [{"ts": r[0], "level": r[1], "message": r[2], "traceback": r[3]} for r in rows]

# instantiate DB
db = Database()

# -------------------------
# In-memory runtime state
# -------------------------
active_games = {}  # key: game_id (group id or user id) -> game instance
game_timers = {}   # key: game_id -> Timer object (for question timeout)
standalone_sessions = {}  # for independent windows/games waiting for start
user_cache = {}
user_requests = defaultdict(list)
session_meta = {}  # additional meta per active game: {game_id: {"session_id", "team_mode", "join_phase", "joined_users": set(), "teams": {user:team}}}

# Rate limiting (simple)
RATE_LIMIT = {
    "max_requests": 10,
    "window_seconds": 60
}
user_rate = defaultdict(list)

def is_rate_limited(user_id):
    now = datetime.utcnow()
    window = timedelta(seconds=RATE_LIMIT["window_seconds"])
    user_rate[user_id] = [t for t in user_rate[user_id] if now - t < window]
    if len(user_rate[user_id]) >= RATE_LIMIT["max_requests"]:
        return True
    user_rate[user_id].append(now)
    return False

# -------------------------
# Games loader (reuse your games folder)
# -------------------------
AVAILABLE_GAMES = {}
try:
    # Import classes if present; if not, loader will log error
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
        "ذكاء": IqGame, "رياضيات": MathGame, "لون الكلمة": WordColorGame,
        "كلمة مبعثرة": ScrambleWordGame, "كتابة سريعة": FastTypingGame,
        "عكس": OppositeGame, "تكوين": LettersWordsGame,
        "أغنية": SongGame, "إنسان حيوان نبات": HumanAnimalPlantGame,
        "سلسلة كلمات": ChainWordsGame, "تخمين": GuessGame, "توافق": CompatibilityGame
    }
    logger.info(f"Loaded {len(AVAILABLE_GAMES)} games")
except Exception as e:
    logger.exception("Error loading game modules")

# -------------------------
# Quick Reply helper (games only)
# -------------------------
def create_games_quick_reply_items():
    items = []
    for qr in FIXED_GAME_QR:
        # QuickReplyItem requires MessageAction or PostbackAction
        items.append(QuickReplyItem(action=MessageAction(label=qr["label"], text=qr["text"])))
    return items

GAMES_QR = QuickReply(items=create_games_quick_reply_items())

def attach_quick_reply_message(message):
    try:
        message.quick_reply = GAMES_QR
    except Exception:
        # not all message types support attribute assignment depending on SDK object
        pass
    return message

# -------------------------
# Timer & helpers
# -------------------------
QUESTION_TIMEOUT = GAME_CONFIG.get("timeout_seconds", 30)  # default per constants

def start_question_timer(game_id, seconds=QUESTION_TIMEOUT, on_timeout=None):
    # cancel existing
    cancel_question_timer(game_id)
    def _timeout():
        try:
            logger.info(f"[TIMER] timeout for {game_id}")
            if on_timeout:
                on_timeout()
        except Exception as e:
            logger.exception("Timer on_timeout error")
    t = threading.Timer(seconds, _timeout)
    game_timers[game_id] = t
    t.daemon = True
    t.start()

def cancel_question_timer(game_id):
    t = game_timers.get(game_id)
    if t:
        try:
            t.cancel()
        except:
            pass
        del game_timers[game_id]

# -------------------------
# Debug logging decorator
# -------------------------
def log_exception(e, context=""):
    tb = traceback.format_exc()
    msg = f"{context} - {str(e)}"
    logger.error(msg)
    db.log("ERROR", msg, tb)

# -------------------------
# Helper: get user object & caching
# -------------------------
def get_user_data(user_id, username="مستخدم"):
    if user_id in user_cache:
        cache_time = user_cache.get(f"{user_id}_time", datetime.min)
        if datetime.utcnow() - cache_time < timedelta(minutes=5):
            return user_cache[user_id]
    user = db.get_user(user_id)
    if not user:
        db.create_user(user_id, username)
        user = db.get_user(user_id)
    user_cache[user_id] = user
    user_cache[f"{user_id}_time"] = datetime.utcnow()
    return user

def update_user_cache(user_id):
    user = db.get_user(user_id)
    if user:
        user_cache[user_id] = user
        user_cache[f"{user_id}_time"] = datetime.utcnow()

# -------------------------
# Game session helpers (team logic)
# -------------------------
def ensure_session_meta(game_id):
    if game_id not in session_meta:
        session_meta[game_id] = {
            "session_id": None,
            "team_mode": False,
            "join_phase": False,
            "joined_users": set(),
            "teams": {},  # user_id -> "team1" or "team2"
            "owner": None,
            "current_game_name": None
        }
    return session_meta[game_id]

def start_join_phase(game_id, owner_id=None):
    meta = ensure_session_meta(game_id)
    meta["join_phase"] = True
    meta["team_mode"] = True
    meta["join_started_at"] = datetime.utcnow()
    meta["joined_users"] = set()
    meta["teams"] = {}
    meta["owner"] = owner_id
    # create persistent session in DB
    session_id = db.create_game_session(owner_id or "unknown", "multi_game", mode="teams", team_mode=1, extra=None)
    meta["session_id"] = session_id
    logger.info(f"Join phase started for {game_id}, session {session_id}")

def close_join_phase_and_assign(game_id):
    meta = ensure_session_meta(game_id)
    if not meta.get("join_phase"):
        return
    users = list(meta["joined_users"])
    random.shuffle(users)
    team1 = users[0::2]
    team2 = users[1::2]
    for u in team1:
        db.add_team_member(meta["session_id"], u, "team1")
        meta["teams"][u] = "team1"
    for u in team2:
        db.add_team_member(meta["session_id"], u, "team2")
        meta["teams"][u] = "team2"
    meta["join_phase"] = False
    logger.info(f"Teams assigned for session {meta['session_id']}: team1={len(team1)} team2={len(team2)}")

def add_join_user(game_id, user_id):
    meta = ensure_session_meta(game_id)
    if not meta.get("join_phase"):
        # if no join phase active, start one automatically
        start_join_phase(game_id, owner_id=user_id)
    meta["joined_users"].add(user_id)
    logger.info(f"user {user_id} joined session {meta.get('session_id')}")

def remove_join_user(game_id, user_id):
    meta = ensure_session_meta(game_id)
    if user_id in meta.get("joined_users", set()):
        meta["joined_users"].remove(user_id)
    # remove from persistent
    if meta.get("session_id"):
        db.remove_team_member(meta["session_id"], user_id)
    if user_id in meta.get("teams", {}):
        del meta["teams"][user_id]
    logger.info(f"user {user_id} removed from join list for session {meta.get('session_id')}")

def is_user_joined(game_id, user_id):
    meta = ensure_session_meta(game_id)
    return user_id in meta.get("joined_users", set()) or user_id in meta.get("teams", {})

def get_user_team(game_id, user_id):
    meta = ensure_session_meta(game_id)
    return meta.get("teams", {}).get(user_id)

# -------------------------
# Helper: start a game instance (solo or team-aware)
# -------------------------
def launch_game_instance(game_id, owner_id, game_name, line_api, theme=None, team_mode=False):
    """
    Create game instance and attach meta.
    game_id: group id or user id
    owner_id: who started
    """
    if game_name not in AVAILABLE_GAMES:
        raise ValueError("Game not available")
    GameClass = AVAILABLE_GAMES[game_name]
    game_instance = GameClass(line_api)

    # optional set theme if game supports it
    try:
        if hasattr(game_instance, 'set_theme') and theme:
            game_instance.set_theme(theme)
    except Exception:
        logger.exception("set_theme failed")

    active_games[game_id] = game_instance
    meta = ensure_session_meta(game_id)
    meta["current_game_name"] = game_name
    meta["owner"] = owner_id
    # create session
    session_id = db.create_game_session(owner_id, game_name, mode=("teams" if team_mode else "solo"), team_mode=1 if team_mode else 0)
    meta["session_id"] = session_id
    meta["team_mode"] = team_mode
    if team_mode:
        # ensure team rows exist in DB created above
        pass
    logger.info(f"Launched game {game_name} for {game_id} (team_mode={team_mode}) session={session_id}")
    return game_instance

# -------------------------
# LINE webhook & handler
# -------------------------
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        logger.warning("Invalid signature")
        abort(400)
    except Exception as e:
        logger.exception("Error in handler.handle")
        db.log("ERROR", "handler.handle exception", traceback.format_exc())
        abort(500)
    return "OK"

@app.route("/", methods=['GET'])
def status_page():
    stats = {
        "total_users": len(db.get_leaderboard(1000)),
        "registered_users": 0,  # could be computed if needed
        "available_games": len(AVAILABLE_GAMES),
        "active_games": len(active_games)
    }
    # Simple HTML status
    return f"<h3>{BOT_NAME} v{BOT_VERSION}</h3><p>Active games: {stats['active_games']}</p><p>Available games: {stats['available_games']}</p><p>{BOT_RIGHTS}</p>"

@app.route("/debug/logs", methods=['GET'])
def debug_logs():
    try:
        logs = db.get_logs(limit=200)
        return jsonify({"logs": logs})
    except Exception as e:
        logger.exception("Error fetching logs")
        return jsonify({"error": str(e)}), 500

# Message handler
@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    try:
        user_id = event.source.user_id
        text = event.message.text.strip()
        if not text:
            return

        # rate limiting
        if is_rate_limited(user_id):
            logger.info(f"Rate limited: {user_id}")
            return

        in_group = hasattr(event.source, 'group_id')  # group chat if true
        game_id = event.source.group_id if in_group else event.source.user_id

        # init LINE API client for this request
        with ApiClient(configuration) as api_client:
            line_api = MessagingApi(api_client)

            # get fresh profile name
            try:
                profile = line_api.get_profile(user_id)
                username = get_username(profile)
            except Exception:
                username = "مستخدم"

            user = get_user_data(user_id, username)
            db.update_activity(user_id)
            current_theme = user.get("theme") or DEFAULT_THEME

            # ignore group messages unless mentions or active game
            if in_group and "@" not in text and game_id not in active_games and not ensure_session_meta(game_id).get("join_phase"):
                # allow quick commands like 'ألعاب' or 'مساعدة' even if not mentioned
                lowered = text.lower()
                if lowered not in ["ألعاب", "مساعدة", "بداية", "home", "أسرع"] and lowered not in [g.lower() for g in GAME_LIST] :
                    return

            lowered = text.lower()

            reply_message = None

            # ----- Admin / debug commands -----
            if lowered in ["debug logs", "logs", "لوق"]:
                # return minimal logs (as text)
                logs = db.get_logs(limit=30)
                txt = "\n".join([f"{l['ts']}|{l['level']}|{l['message']}" for l in logs[:20]])
                reply_message = TextMessage(text=f"Logs:\n{txt or 'empty'}")

            # ----- Help / Home -----
            elif lowered in ["مساعدة", "help", "بداية", "start", "home", "الرئيسية", "البداية"]:
                # Build main home or help
                if lowered in ["مساعدة", "help"]:
                    reply_message = build_help_window(current_theme)
                else:
                    reply_message = build_enhanced_home(username, user['points'], user.get('is_registered'), current_theme)

            # ----- Themes -----
            elif lowered.startswith("ثيم "):
                theme_name = text.replace("ثيم ", "").strip()
                if theme_name in THEMES:
                    db.update_user(user_id, theme=theme_name)
                    update_user_cache(user_id)
                    reply_message = TextMessage(text=f"✅ تم تغيير الثيم إلى {theme_name}")
                else:
                    reply_message = TextMessage(text=f"الثيمات المتاحة:\n{', '.join(THEMES.keys())}")

            elif lowered in ["ثيمات", "ثيم"]:
                reply_message = build_theme_selector(current_theme)

            # ----- Games menu -----
            elif lowered in ["ألعاب", "games"]:
                reply_message = build_games_menu(current_theme)

            # ----- Register / Join / Leave -----
            elif lowered in ["انضم", "join", "register"]:
                db.update_user(user_id, is_registered=1)
                update_user_cache(user_id)
                reply_message = TextMessage(text="✅ تم التسجيل بنجاح")

            elif lowered in ["انسحب", "leave", "unregister"]:
                db.update_user(user_id, is_registered=0)
                update_user_cache(user_id)
                # Also remove from any join lists in active sessions (group)
                if in_group:
                    remove_join_user(game_id, user_id)
                reply_message = TextMessage(text="❌ تم إلغاء التسجيل (وانسحبت من الفرق إن وُجدت)")

            # ----- Teams join flow -----
            elif lowered in ["فريقين", "teams"]:
                # Only in group context makes sense
                if not in_group:
                    reply_message = TextMessage(text="▫️ أمر 'فريقين' يعمل داخل المجموعات فقط")
                else:
                    # start join phase for this group
                    start_join_phase(game_id, owner_id=user_id)
                    reply_message = TextMessage(text="▫️ بدأ وقت الانضمام: اكتب 'انضم' للانضمام، اكتب 'انسحب' للخروج. سيتم تقسيم اللاعبين تلقائياً لفريقين عند بداية اللعبة.")

            elif lowered == "انضم":
                if in_group:
                    meta = ensure_session_meta(game_id)
                    if not meta.get("join_phase"):
                        start_join_phase(game_id, owner_id=user_id)
                    add_join_user(game_id, user_id)
                    reply_message = TextMessage(text=f"▫️ تمت الإضافة لقائمة الانضمام. حالياً {len(meta['joined_users'])} منضمين.")
                else:
                    # solo join -> just register
                    db.update_user(user_id, is_registered=1)
                    update_user_cache(user_id)
                    reply_message = TextMessage(text="✅ تم تفعيلك للعب الفردي (منضم)")

            elif lowered == "انسحب":
                if in_group:
                    remove_join_user(game_id, user_id)
                    reply_message = TextMessage(text="▫️ تم إخراجك من قائمة الانضمام")
                else:
                    db.update_user(user_id, is_registered=0)
                    update_user_cache(user_id)
                    reply_message = TextMessage(text="▫️ تم إلغاء التسجيل")

            # ----- Stop -----
            elif lowered in ["إيقاف", "stop", "quit", "exit"]:
                if game_id in active_games:
                    del active_games[game_id]
                    cancel_question_timer(game_id)
                    # close session if exists
                    meta = ensure_session_meta(game_id)
                    if meta.get("session_id"):
                        db.finish_session(meta["session_id"])
                    session_meta.pop(game_id, None)
                    reply_message = TextMessage(text="⛔ تم إيقاف اللعبة")
                else:
                    reply_message = TextMessage(text="▫️ لا توجد لعبة نشطة هنا")

            # ----- Start Game (by text or Quick Reply) -----
            elif (text in GAME_LIST) or (lowered.startswith("لعبة ") or lowered.startswith("إعادة ")):
                # Determine requested game name normalized to your AVAILABLE_GAMES keys
                # The GAME_LIST structure you used maps labels to commands — but we also maintained AVAILABLE_GAMES mapping by Arabic labels
                # Try to map: if exact match in AVAILABLE_GAMES keys use it
                game_key = None
                # if text equals one of GAME_LIST keys (labels) -> use that label
                if text in AVAILABLE_GAMES:
                    game_key = text
                else:
                    # try mapping via GAME_LIST constant (if dict)
                    try:
                        if isinstance(GAME_LIST, dict):
                            if text in GAME_LIST:
                                # GAME_LIST[text] may have 'command' field like "لعبة IQ"
                                cmd = GAME_LIST[text].get("command", text)
                                game_key = cmd.replace("لعبة ", "").strip()
                            else:
                                # maybe text is "أغنية" etc.
                                if text in AVAILABLE_GAMES:
                                    game_key = text
                    except Exception:
                        pass

                    # fallback: attempt to find available game whose key or name contains text
                    if not game_key:
                        for k in AVAILABLE_GAMES.keys():
                            if normalize_text_k := k.lower():
                                if text.lower() in normalize_text_k or normalize_text_k in text.lower():
                                    game_key = k
                                    break

                if not game_key:
                    reply_message = TextMessage(text=f"❌ اللعبة '{text}' غير موجودة")
                else:
                    # require registration
                    if not user.get('is_registered'):
                        reply_message = build_registration_required(current_theme)
                    else:
                        # If group and team join phase active -> assign teams and start in team_mode
                        meta = ensure_session_meta(game_id)
                        team_mode = False
                        if in_group and meta.get("join_phase"):
                            # close join phase and assign teams
                            close_join_phase_and_assign(game_id)
                            team_mode = True
                        # launch game
                        try:
                            game_instance = launch_game_instance(game_id, user_id, game_key, line_api, theme=current_theme, team_mode=team_mode)
                            # start game and send its initial message
                            start_msg = game_instance.start_game()
                            # if team_mode, ensure we don't allow hints/reveals
                            meta = ensure_session_meta(game_id)
                            meta["team_mode"] = team_mode
                            # persistent session creation was done in launch_game_instance; attach session id to game_instance if needed
                            send_with_quick_reply(line_api, event.reply_token, start_msg)
                            continue  # we've already replied
                        except Exception as e:
                            log_exception(e, context="start game")
                            reply_message = TextMessage(text="❌ خطأ في بدء اللعبة")

            # ----- Game answer handling -----
            else:
                # If there's an active game for this context, forward to game check
                if game_id in active_games:
                    game_instance = active_games[game_id]
                    meta = ensure_session_meta(game_id)
                    # In team_mode: only accept answers from joined users
                    if meta.get("team_mode"):
                        if not is_user_joined(game_id, user_id):
                            # ignore answers from non-joined to avoid spam
                            logger.info(f"Ignored answer from non-joined user {user_id} in team session")
                            return
                        # disable hints/reveals in team mode
                        if lowered in ["لمح", "جاوب"]:
                            reply_message = TextMessage(text="▫️ في وضع الفريقين لا تتوفر أوامر 'لمح' أو 'جاوب'. اكتب الإجابة مباشرةً.")
                            send_with_quick_reply(line_api, event.reply_token, reply_message)
                            return

                    # now forward to the game's check_answer method
                    try:
                        # game_instance.check_answer should return a dict as in your games: {'message':..., 'response': FlexMessage or TextMessage, 'points': n, 'game_over': bool}
                        result = None
                        # some game implementations might accept (text,user_id,username)
                        if hasattr(game_instance, 'check_answer'):
                            result = game_instance.check_answer(text, user_id, username)
                        else:
                            # fallback: ignore
                            result = None

                        if not result:
                            # either duplicate answer or ignored
                            return

                        # if points awarded
                        pts = result.get('points', 0)
                        if pts and meta.get("team_mode"):
                            # credit team points instead of individual
                            team_name = get_user_team(game_id, user_id) or "team1"
                            db.add_team_points(meta["session_id"], team_name, pts)
                            logger.info(f"Added {pts} points to {team_name} in session {meta['session_id']}")
                        elif pts:
                            # individual points
                            db.add_points(user_id, pts)
                            db.record_game_stat(user_id, meta.get("current_game_name") or getattr(game_instance, "game_name", "unknown"), pts)

                        # if game reports game_over
                        if result.get('game_over'):
                            # finalize session
                            if meta.get("session_id"):
                                db.finish_session(meta["session_id"])
                            # build final announcement: if team_mode -> show team standings
                            if meta.get("team_mode"):
                                team_pts = db.get_team_points(meta["session_id"])
                                # determine winner
                                t1 = team_pts.get("team1", 0)
                                t2 = team_pts.get("team2", 0)
                                if t1 > t2:
                                    winner_text = f"🏆 الفريق الفائز: فريق 1 — {t1} نقطة مقابل {t2}"
                                elif t2 > t1:
                                    winner_text = f"🏆 الفريق الفائز: فريق 2 — {t2} نقطة مقابل {t1}"
                                else:
                                    winner_text = f"🏆 تعادل — {t1} : {t2}"
                                # send final text then winner announcement UI
                                reply_message = TextMessage(text=winner_text)
                                # also send winner announcement UI if available
                                try:
                                    # build_winner_announcement signature: username, game_name, total_score, final_points, theme
                                    reply_ui = build_winner_announcement("المجموعة", meta.get("current_game_name", "اللعبة"), max(t1, t2), max(t1, t2), current_theme)
                                    send_with_quick_reply(line_api, event.reply_token, reply_ui)
                                    # also record to DB aggregated stats if desired
                                except Exception:
                                    send_with_quick_reply(line_api, event.reply_token, reply_message)
                            else:
                                # individual winner handled by game logic
                                winner_ui = build_winner_announcement(username, meta.get("current_game_name", getattr(game_instance, "game_name", "اللعبة")), result.get('points', 0), db.get_user(user_id)['points'], current_theme)
                                send_with_quick_reply(line_api, event.reply_token, winner_ui)
                            # cleanup
                            if game_id in active_games:
                                del active_games[game_id]
                            cancel_question_timer(game_id)
                            session_meta.pop(game_id, None)
                            return
                        else:
                            # not finished: if game returned an immediate response object (Flex or Text) send it
                            if result.get('response'):
                                send_with_quick_reply(line_api, event.reply_token, result.get('response'))
                                return
                            else:
                                # default: send message text
                                reply_message = TextMessage(text=result.get('message', 'تم'))
                    except Exception as e:
                        log_exception(e, context="check_answer")
                        # cleanup to avoid stuck states
                        try:
                            if game_id in active_games:
                                del active_games[game_id]
                        except:
                            pass
                        reply_message = TextMessage(text="❌ حدث خطأ أثناء فحص الإجابة")

            # send reply if available
            if reply_message:
                send_with_quick_reply(line_api, event.reply_token, reply_message)

    except Exception as e:
        log_exception(e, context="handle_message top")
        # don't crash flask route
        return

# -------------------------
# Utility to send with quick reply
# -------------------------
def send_with_quick_reply(line_api, reply_token, message):
    try:
        # attach games-only quick reply
        try:
            attach_quick_reply_message(message)
        except Exception:
            pass
        line_api.reply_message_with_http_info(
            ReplyMessageRequest(reply_token=reply_token, messages=[message])
        )
    except Exception as e:
        log_exception(e, context="send_with_quick_reply")

# -------------------------
# Periodic cleanup thread
# -------------------------
def periodic_cleanup():
    def _cleanup():
        while True:
            try:
                time.sleep(300)  # every 5 minutes
                # remove stale active games that have no activity (optionally)
                # Also prune user_cache
                now = datetime.utcnow()
                for uid in list(user_cache.keys()):
                    if uid.endswith("_time"):
                        continue
                    t = user_cache.get(f"{uid}_time", datetime.min)
                    if now - t > timedelta(minutes=30):
                        user_cache.pop(uid, None)
                        user_cache.pop(f"{uid}_time", None)
                db.log("INFO", "Periodic cleanup ran", None)
            except Exception as e:
                log_exception(e, "cleanup")
    t = threading.Thread(target=_cleanup, daemon=True)
    t.start()

# Start cleanup
periodic_cleanup()

# -------------------------
# Run server
# -------------------------
if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    logger.info("=" * 70)
    logger.info(f"Starting {BOT_NAME} v{BOT_VERSION}")
    logger.info(f"Games loaded: {len(AVAILABLE_GAMES)}")
    logger.info(f"Listening on port {port}")
    logger.info("=" * 70)
    app.run(host="0.0.0.0", port=port, debug=False)
