# app.py - FIXED VERSION
"""
Bot Mesh - LINE Bot Application v8.0 FIXED
تم إصلاح الأخطاء الحرجة
Created by: Abeer Aldosari © 2025
"""

import os
import sys
import logging
import threading
import time
import traceback
import random
from datetime import datetime, timedelta
from collections import defaultdict

from flask import Flask, request, abort, jsonify

# LINE SDK v3 imports
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi,
    ReplyMessageRequest, TextMessage
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent

# استيراد من الملفات المحلية
from constants import (
    BOT_NAME, BOT_VERSION, BOT_RIGHTS,
    LINE_CHANNEL_SECRET, LINE_CHANNEL_ACCESS_TOKEN,
    validate_env, get_username, GAME_LIST, DEFAULT_THEME
)

from ui_builder import (
    build_games_menu, build_my_points, build_leaderboard,
    build_registration_required, build_winner_announcement,
    build_help_window, build_theme_selector, build_enhanced_home,
    build_multiplayer_help_window, attach_quick_reply_to_message
)

# استيراد قاعدة البيانات المنفصلة
from database import get_database

# -------------------------
# التحقق من المتغيرات
# -------------------------
try:
    validate_env()
except Exception as e:
    print(f"Configuration error: {e}")

# -------------------------
# إعداد Flask & LINE
# -------------------------
app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("botmesh")

configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# -------------------------
# قاعدة البيانات
# -------------------------
db = get_database()

# -------------------------
# حالة التشغيل
# -------------------------
active_games = {}
game_timers = {}
session_meta = {}
user_cache = {}

# معدل الطلبات
RATE_LIMIT = {"max_requests": 10, "window_seconds": 60}
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
# تحميل الألعاب
# -------------------------
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
    from games.compatibility_game import CompatibilitySystem

    AVAILABLE_GAMES = {
        "ذكاء": IqGame,
        "رياضيات": MathGame,
        "لون": WordColorGame,
        "كلمة مبعثرة": ScrambleWordGame,
        "كتابة سريعة": FastTypingGame,
        "أضداد": OppositeGame,
        "تكوين": LettersWordsGame,
        "أغنية": SongGame,
        "لعبة": HumanAnimalPlantGame,
        "سلسلة كلمات": ChainWordsGame,
        "تخمين": GuessGame,
        "توافق": CompatibilitySystem
    }
    logger.info(f"✅ تم تحميل {len(AVAILABLE_GAMES)} لعبة")
except Exception as e:
    logger.error(f"❌ خطأ في تحميل الألعاب: {e}")
    logger.error(traceback.format_exc())

# -------------------------
# إدارة الجلسات
# -------------------------
def ensure_session_meta(game_id):
    if game_id not in session_meta:
        session_meta[game_id] = {
            "session_id": None,
            "team_mode": False,
            "join_phase": False,
            "joined_users": set(),
            "teams": {},
            "owner": None,
            "current_game_name": None
        }
    return session_meta[game_id]

def start_join_phase(game_id, owner_id=None):
    meta = ensure_session_meta(game_id)
    meta["join_phase"] = True
    meta["team_mode"] = True
    meta["joined_users"] = set()
    meta["teams"] = {}
    meta["owner"] = owner_id
    session_id = db.create_game_session(owner_id or "unknown", "multi_game", mode="teams", team_mode=1)
    meta["session_id"] = session_id
    logger.info(f"✅ بدأت مرحلة الانضمام: {game_id}")

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
    logger.info(f"✅ تم تقسيم الفرق: {len(team1)} vs {len(team2)}")

# -------------------------
# إطلاق لعبة
# -------------------------
def launch_game_instance(game_id, owner_id, game_name, line_api, theme=None, team_mode=False):
    if game_name not in AVAILABLE_GAMES:
        raise ValueError(f"اللعبة غير متوفرة: {game_name}")
    
    GameClass = AVAILABLE_GAMES[game_name]
    game_instance = GameClass(line_api)

    # تعيين الثيم
    try:
        if hasattr(game_instance, 'set_theme') and theme:
            game_instance.set_theme(theme)
    except Exception as e:
        logger.error(f"⚠️ فشل تعيين الثيم: {e}")

    active_games[game_id] = game_instance
    meta = ensure_session_meta(game_id)
    meta["current_game_name"] = game_name
    meta["owner"] = owner_id
    
    session_id = db.create_game_session(
        owner_id, 
        game_name, 
        mode=("teams" if team_mode else "solo"), 
        team_mode=1 if team_mode else 0
    )
    meta["session_id"] = session_id
    meta["team_mode"] = team_mode
    
    logger.info(f"✅ تم إطلاق اللعبة: {game_name} (فريقين={team_mode})")
    return game_instance

# -------------------------
# إدارة المستخدم
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

# -------------------------
# Routes
# -------------------------
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        logger.warning("❌ توقيع غير صالح")
        abort(400)
    except Exception as e:
        logger.error(f"❌ خطأ في المعالج: {e}")
        logger.error(traceback.format_exc())
        abort(500)
    return "OK"

@app.route("/", methods=['GET'])
def status_page():
    return f"""
    <h2>{BOT_NAME} v{BOT_VERSION}</h2>
    <p>✅ الألعاب النشطة: {len(active_games)}</p>
    <p>✅ الألعاب المتاحة: {len(AVAILABLE_GAMES)}</p>
    <p><small>{BOT_RIGHTS}</small></p>
    """

@app.route("/debug/logs", methods=['GET'])
def debug_logs():
    try:
        logs = db.get_logs(limit=100)
        return jsonify({"logs": logs})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -------------------------
# معالج الرسائل
# -------------------------
@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    try:
        user_id = event.source.user_id
        text = event.message.text.strip()
        
        if not text:
            return

        # Rate limiting
        if is_rate_limited(user_id):
            logger.info(f"⚠️ تجاوز الحد: {user_id}")
            return

        in_group = hasattr(event.source, 'group_id')
        game_id = event.source.group_id if in_group else user_id

        with ApiClient(configuration) as api_client:
            line_api = MessagingApi(api_client)

            # الحصول على اسم المستخدم
            try:
                profile = line_api.get_profile(user_id)
                username = get_username(profile)
            except:
                username = "مستخدم"

            user = get_user_data(user_id, username)
            db.update_activity(user_id)
            current_theme = user.get("theme") or DEFAULT_THEME

            lowered = text.lower()
            reply_message = None

            # الأوامر الأساسية
            if lowered in ["مساعدة", "help"]:
                reply_message = build_help_window(current_theme)
            
            elif lowered in ["بداية", "home", "الرئيسية"]:
                reply_message = build_enhanced_home(username, user['points'], user.get('is_registered'), current_theme)
            
            elif lowered in ["ألعاب", "games"]:
                reply_message = build_games_menu(current_theme)
            
            elif lowered in ["نقاطي", "points"]:
                stats = db.get_user_game_stats(user_id)
                reply_message = build_my_points(username, user['points'], stats, current_theme)
            
            elif lowered in ["صدارة", "leaderboard"]:
                top = db.get_leaderboard(20)
                reply_message = build_leaderboard(top, current_theme)
            
            elif lowered in ["انضم", "join"]:
                db.update_user(user_id, is_registered=1)
                if in_group:
                    meta = ensure_session_meta(game_id)
                    if meta.get("join_phase"):
                        meta["joined_users"].add(user_id)
                reply_message = TextMessage(text="✅ تم الانضمام")
            
            elif lowered in ["فريقين", "teams"]:
                if in_group:
                    start_join_phase(game_id, owner_id=user_id)
                    reply_message = TextMessage(text="✅ بدأت مرحلة الانضمام\nاكتب 'انضم' للدخول")
                else:
                    reply_message = TextMessage(text="⚠️ هذا الأمر للمجموعات فقط")
            
            elif lowered.startswith("ثيم "):
                theme_name = text.replace("ثيم ", "").strip()
                from constants import THEMES
                if theme_name in THEMES:
                    db.set_user_theme(user_id, theme_name)
                    reply_message = TextMessage(text=f"✅ تم التغيير إلى {theme_name}")
                else:
                    reply_message = build_theme_selector(current_theme)
            
            elif lowered == "ثيمات":
                reply_message = build_theme_selector(current_theme)
            
            elif lowered in ["إيقاف", "stop"]:
                if game_id in active_games:
                    del active_games[game_id]
                    session_meta.pop(game_id, None)
                    reply_message = TextMessage(text="⛔ تم إيقاف اللعبة")
            
            # بدء اللعبة
            elif text in AVAILABLE_GAMES:
                if not user.get('is_registered'):
                    reply_message = build_registration_required(current_theme)
                else:
                    meta = ensure_session_meta(game_id)
                    team_mode = False
                    if in_group and meta.get("join_phase"):
                        close_join_phase_and_assign(game_id)
                        team_mode = True
                    
                    try:
                        game_instance = launch_game_instance(game_id, user_id, text, line_api, current_theme, team_mode)
                        start_msg = game_instance.start_game()
                        
                        if hasattr(start_msg, 'quick_reply'):
                            line_api.reply_message(ReplyMessageRequest(reply_token=event.reply_token, messages=[start_msg]))
                        else:
                            attach_quick_reply_to_message(start_msg)
                            line_api.reply_message(ReplyMessageRequest(reply_token=event.reply_token, messages=[start_msg]))
                        return
                    except Exception as e:
                        logger.error(f"❌ خطأ في بدء اللعبة: {e}")
                        logger.error(traceback.format_exc())
                        reply_message = TextMessage(text="❌ حدث خطأ في بدء اللعبة")
            
            # معالجة الإجابة
            elif game_id in active_games:
                game_instance = active_games[game_id]
                meta = ensure_session_meta(game_id)
                
                # في وضع الفريقين: تجاهل غير المنضمين
                if meta.get("team_mode"):
                    if user_id not in meta.get("joined_users", set()) and user_id not in meta.get("teams", {}):
                        return
                
                try:
                    result = game_instance.check_answer(text, user_id, username)
                    
                    if not result:
                        return
                    
                    pts = result.get('points', 0)
                    if pts and meta.get("team_mode"):
                        team_name = meta["teams"].get(user_id, "team1")
                        db.add_team_points(meta["session_id"], team_name, pts)
                    elif pts:
                        db.add_points(user_id, pts)
                        db.record_game_stat(user_id, meta.get("current_game_name", "unknown"), pts)
                    
                    if result.get('game_over'):
                        if meta.get("session_id"):
                            db.finish_session(meta["session_id"])
                        
                        if meta.get("team_mode"):
                            team_pts = db.get_team_points(meta["session_id"])
                            t1 = team_pts.get("team1", 0)
                            t2 = team_pts.get("team2", 0)
                            winner_text = f"🏆 الفريق الفائز: {'فريق 1' if t1 > t2 else 'فريق 2'}\n{t1} : {t2}"
                            reply_message = TextMessage(text=winner_text)
                        else:
                            reply_message = build_winner_announcement(
                                username, 
                                meta.get("current_game_name", "اللعبة"), 
                                pts, 
                                user['points'] + pts, 
                                current_theme
                            )
                        
                        del active_games[game_id]
                        session_meta.pop(game_id, None)
                    else:
                        if result.get('response'):
                            attach_quick_reply_to_message(result['response'])
                            line_api.reply_message(ReplyMessageRequest(reply_token=event.reply_token, messages=[result['response']]))
                            return
                        else:
                            reply_message = TextMessage(text=result.get('message', '✅'))
                
                except Exception as e:
                    logger.error(f"❌ خطأ في check_answer: {e}")
                    logger.error(traceback.format_exc())
                    if game_id in active_games:
                        del active_games[game_id]
                    reply_message = TextMessage(text="❌ حدث خطأ في اللعبة")

            # إرسال الرد
            if reply_message:
                attach_quick_reply_to_message(reply_message)
                line_api.reply_message(ReplyMessageRequest(reply_token=event.reply_token, messages=[reply_message]))

    except Exception as e:
        logger.error(f"❌ خطأ عام: {e}")
        logger.error(traceback.format_exc())

# -------------------------
# تنظيف دوري
# -------------------------
def periodic_cleanup():
    def _cleanup():
        while True:
            try:
                time.sleep(300)
                now = datetime.utcnow()
                for uid in list(user_cache.keys()):
                    if uid.endswith("_time"):
                        continue
                    t = user_cache.get(f"{uid}_time", datetime.min)
                    if now - t > timedelta(minutes=30):
                        user_cache.pop(uid, None)
                        user_cache.pop(f"{uid}_time", None)
                logger.info("✅ تنظيف دوري")
            except Exception as e:
                logger.error(f"❌ خطأ في التنظيف: {e}")
    
    t = threading.Thread(target=_cleanup, daemon=True)
    t.start()

periodic_cleanup()

# -------------------------
# تشغيل الخادم
# -------------------------
if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    logger.info("=" * 70)
    logger.info(f"🚀 {BOT_NAME} v{BOT_VERSION}")
    logger.info(f"✅ الألعاب: {len(AVAILABLE_GAMES)}")
    logger.info(f"🌐 المنفذ: {port}")
    logger.info("=" * 70)
    app.run(host="0.0.0.0", port=port, debug=False)
