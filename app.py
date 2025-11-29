# app.py - FINAL FIXED v11.1
"""
Bot Mesh - LINE Bot Application v11.1 FIXED
✅ وضع الفريقين: بدون لمح/جاوب - أول إجابة صحيحة تفوز
✅ وضع فردي: مع لمح/جاوب حسب اللعبة
✅ لعبة التوافق: بدون نقاط، بدون إعلان فائز
✅ كل شيء نوافذ فلكس وأزرار
✅ إصلاح: منع لمح/جاوب في وضع الفريقين نهائياً
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
    build_multiplayer_help_window, attach_quick_reply
)

from database import get_database

# -------------------------
# التحقق من المتغيرات
# -------------------------
try:
    validate_env()
except Exception as e:
    print(f"Configuration error: {e}")
    sys.exit(1)

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
    """التحقق من معدل الطلبات"""
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
        "إنسان حيوان نبات": HumanAnimalPlantGame,
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
    """التأكد من وجود metadata للجلسة"""
    if game_id not in session_meta:
        session_meta[game_id] = {
            "session_id": None,
            "team_mode": False,
            "join_phase": False,
            "joined_users": set(),
            "teams": {},
            "owner": None,
            "current_game_name": None,
            "session_type": "solo"
        }
    return session_meta[game_id]

def start_join_phase(game_id, owner_id=None):
    """بدء مرحلة الانضمام للفرق"""
    meta = ensure_session_meta(game_id)
    meta["join_phase"] = True
    meta["team_mode"] = True
    meta["joined_users"] = set()
    meta["teams"] = {}
    meta["owner"] = owner_id
    meta["session_type"] = "teams"
    session_id = db.create_game_session(owner_id or "unknown", "multi_game", mode="teams", team_mode=1)
    meta["session_id"] = session_id
    logger.info(f"✅ بدأت مرحلة الانضمام: {game_id}")

def close_join_phase_and_assign(game_id):
    """إغلاق مرحلة الانضمام وتوزيع الفرق"""
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
# إطلاق لعبة - FIXED VERSION
# -------------------------
def launch_game_instance(game_id, owner_id, game_name, line_api, theme=None, team_mode=False, source_type="user"):
    """إطلاق نسخة من اللعبة - مع إصلاح لمح/جاوب"""
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

    # تعيين قاعدة البيانات
    try:
        if hasattr(game_instance, 'set_database'):
            game_instance.set_database(db)
        else:
            game_instance.db = db
    except Exception as e:
        logger.warning(f"⚠️ لم يتم ربط قاعدة البيانات: {e}")

    # ✅ تعيين session_type
    if source_type == "group":
        game_instance.session_type = "teams" if team_mode else "group"
    else:
        game_instance.session_type = "solo"

    # ✅ في وضع الفريقين: تعطيل لمح وجاوب بشكل نهائي
    if team_mode:
        game_instance.team_mode = True  # ✅ تفعيل وضع الفريقين أولاً
        game_instance.supports_hint = False
        game_instance.supports_reveal = False
        
        # نقل بيانات الفرق من session_meta
        meta = ensure_session_meta(game_id)
        if meta.get("joined_users"):
            game_instance.joined_users = meta["joined_users"].copy()
        if meta.get("teams"):
            game_instance.user_teams = meta["teams"].copy()

    active_games[game_id] = game_instance
    meta = ensure_session_meta(game_id)
    meta["current_game_name"] = game_name
    meta["owner"] = owner_id
    meta["session_type"] = game_instance.session_type
    
    session_id = db.create_game_session(
        owner_id, 
        game_name, 
        mode=game_instance.session_type, 
        team_mode=1 if team_mode else 0
    )
    meta["session_id"] = session_id
    meta["team_mode"] = team_mode
    
    # ✅ لوج تفصيلي للتأكد
    logger.info(f"✅ تم إطلاق اللعبة: {game_name}")
    logger.info(f"   - نوع={game_instance.session_type}")
    logger.info(f"   - فريقين={team_mode}")
    logger.info(f"   - team_mode={game_instance.team_mode}")
    logger.info(f"   - supports_hint={game_instance.supports_hint}")
    logger.info(f"   - supports_reveal={game_instance.supports_reveal}")
    
    return game_instance

# -------------------------
# إدارة المستخدم
# -------------------------
def get_user_data(user_id, username="مستخدم"):
    """الحصول على بيانات المستخدم"""
    if user_id in user_cache:
        cache_time = user_cache.get(f"{user_id}_time", datetime.min)
        if datetime.utcnow() - cache_time < timedelta(minutes=5):
            return user_cache[user_id]
    
    user = db.get_user(user_id)
    if not user:
        db.create_user(user_id, username)
        user = db.get_user(user_id)
    
    # تحديث الاسم إذا تغير
    if user and user.get('name') != username:
        db.update_user_name(user_id, username)
        user['name'] = username
    
    user_cache[user_id] = user
    user_cache[f"{user_id}_time"] = datetime.utcnow()
    return user

# -------------------------
# Routes
# -------------------------
@app.route("/callback", methods=['POST'])
def callback():
    """Webhook callback من LINE"""
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
    """صفحة الحالة"""
    stats = db.get_stats_summary()
    return f"""
    <html>
    <head><title>{BOT_NAME}</title></head>
    <body style="font-family: Arial; padding: 20px; background: #f5f5f5;">
        <h1>🎮 {BOT_NAME} v{BOT_VERSION}</h1>
        <div style="background: white; padding: 20px; border-radius: 10px; margin: 20px 0;">
            <h2>📊 الإحصائيات</h2>
            <p>✅ الألعاب النشطة: {len(active_games)}</p>
            <p>✅ الألعاب المتاحة: {len(AVAILABLE_GAMES)}</p>
            <p>✅ المستخدمين: {stats.get('total_users', 0)}</p>
            <p>✅ المسجلين: {stats.get('registered_users', 0)}</p>
            <p>✅ الجلسات: {stats.get('total_sessions', 0)}</p>
        </div>
        <p><small>{BOT_RIGHTS}</small></p>
    </body>
    </html>
    """

@app.route("/health", methods=['GET'])
def health_check():
    """فحص الصحة"""
    return jsonify({
        "status": "ok",
        "version": BOT_VERSION,
        "active_games": len(active_games),
        "available_games": len(AVAILABLE_GAMES)
    })

# -------------------------
# معالج الرسائل
# -------------------------
@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    """معالج الرسائل - كل شيء فلكس وأزرار"""
    try:
        user_id = event.source.user_id
        text = event.message.text.strip()
        
        if not text:
            return

        # Rate limiting
        if is_rate_limited(user_id):
            logger.info(f"⚠️ تجاوز الحد: {user_id}")
            return

        # تحديد نوع المصدر
        in_group = hasattr(event.source, 'group_id')
        game_id = event.source.group_id if in_group else user_id
        source_type = "group" if in_group else "user"

        with ApiClient(configuration) as api_client:
            line_api = MessagingApi(api_client)

            # الحصول على اسم المستخدم
            try:
                profile = line_api.get_profile(user_id)
                username = get_username(profile)
            except Exception:
                username = "مستخدم"

            user = get_user_data(user_id, username)
            db.update_activity(user_id)
            current_theme = user.get("theme") or DEFAULT_THEME

            lowered = text.lower()
            reply_message = None

            # ===== الأوامر الأساسية =====
            
            if lowered in ["مساعدة", "help", "؟"]:
                reply_message = build_help_window(current_theme)
            
            elif lowered in ["بداية", "home", "الرئيسية", "start"]:
                reply_message = build_enhanced_home(username, user['points'], user.get('is_registered'), current_theme)
            
            elif lowered in ["ألعاب", "games", "العاب"]:
                reply_message = build_games_menu(current_theme)
            
            elif lowered in ["نقاطي", "points", "نقاط"]:
                stats = db.get_user_game_stats(user_id)
                reply_message = build_my_points(username, user['points'], stats, current_theme)
            
            elif lowered in ["صدارة", "leaderboard", "ترتيب"]:
                top = db.get_leaderboard(20)
                reply_message = build_leaderboard(top, current_theme)
            
            elif lowered in ["انضم", "join", "تسجيل"]:
                db.update_user(user_id, is_registered=1)
                meta = ensure_session_meta(game_id)
                if meta.get("join_phase"):
                    meta["joined_users"].add(user_id)
                    from ui_builder import build_join_confirmation
                    reply_message = build_join_confirmation(username, current_theme)
                else:
                    from ui_builder import build_registration_success
                    reply_message = build_registration_success(username, current_theme)
            
            elif lowered in ["فريقين", "teams", "فرق"]:
                if in_group:
                    start_join_phase(game_id, owner_id=user_id)
                    reply_message = build_multiplayer_help_window(current_theme)
                else:
                    from ui_builder import build_error_message
                    reply_message = build_error_message("⚠️ هذا الأمر للمجموعات فقط", current_theme)
            
            elif lowered.startswith("ثيم "):
                theme_name = text.replace("ثيم ", "").strip()
                from constants import THEMES
                if theme_name in THEMES:
                    db.set_user_theme(user_id, theme_name)
                    user_cache.pop(user_id, None)
                    from ui_builder import build_theme_change_success
                    reply_message = build_theme_change_success(theme_name, current_theme)
                else:
                    reply_message = build_theme_selector(current_theme)
            
            elif lowered in ["ثيمات", "themes", "مظهر"]:
                reply_message = build_theme_selector(current_theme)
            
            elif lowered in ["إيقاف", "stop", "انهاء"]:
                if game_id in active_games:
                    game_name = session_meta.get(game_id, {}).get("current_game_name", "اللعبة")
                    del active_games[game_id]
                    session_meta.pop(game_id, None)
                    from ui_builder import build_game_stopped
                    reply_message = build_game_stopped(game_name, current_theme)
                else:
                    from ui_builder import build_error_message
                    reply_message = build_error_message("⚠️ لا توجد لعبة نشطة", current_theme)
            
            # ===== بدء اللعبة =====
            elif text in AVAILABLE_GAMES:
                # ✅ لعبة التوافق: لا تحتاج تسجيل
                if text == "توافق":
                    try:
                        game_instance = launch_game_instance(
                            game_id, user_id, text, line_api, 
                            current_theme, False, source_type
                        )
                        start_msg = game_instance.start_game()
                        attach_quick_reply(start_msg)
                        line_api.reply_message(ReplyMessageRequest(reply_token=event.reply_token, messages=[start_msg]))
                        return
                    except Exception as e:
                        logger.error(f"❌ خطأ في بدء التوافق: {e}")
                        logger.error(traceback.format_exc())
                        from ui_builder import build_error_message
                        reply_message = build_error_message(f"❌ حدث خطأ", current_theme)
                
                # باقي الألعاب تحتاج تسجيل
                elif not user.get('is_registered'):
                    reply_message = build_registration_required(current_theme)
                else:
                    meta = ensure_session_meta(game_id)
                    team_mode = False
                    
                    # ✅ تحقق من وضع الفريقين
                    if in_group and meta.get("join_phase"):
                        close_join_phase_and_assign(game_id)
                        team_mode = True
                        logger.info(f"🎯 بدء لعبة فريقين: {text}")
                    
                    try:
                        game_instance = launch_game_instance(
                            game_id, user_id, text, line_api, 
                            current_theme, team_mode, source_type
                        )
                        
                        # ✅ تأكيد تعطيل لمح/جاوب
                        if team_mode:
                            logger.info(f"🔒 وضع الفريقين نشط للعبة {text}")
                            logger.info(f"   - team_mode: {game_instance.team_mode}")
                            logger.info(f"   - supports_hint: {game_instance.supports_hint}")
                            logger.info(f"   - supports_reveal: {game_instance.supports_reveal}")
                        
                        start_msg = game_instance.start_game()
                        attach_quick_reply(start_msg)
                        line_api.reply_message(ReplyMessageRequest(reply_token=event.reply_token, messages=[start_msg]))
                        return
                    
                    except Exception as e:
                        logger.error(f"❌ خطأ في بدء اللعبة: {e}")
                        logger.error(traceback.format_exc())
                        from ui_builder import build_error_message
                        reply_message = build_error_message(f"❌ حدث خطأ في بدء اللعبة", current_theme)
            
            # ===== معالجة الإجابة =====
            elif game_id in active_games:
                game_instance = active_games[game_id]
                meta = ensure_session_meta(game_id)
                
                # ✅ لعبة التوافق: لا نقاط ولا إعلان فائز
                is_compatibility = meta.get("current_game_name") == "توافق"
                
                # في وضع الفريقين: تجاهل غير المنضمين
                if meta.get("team_mode"):
                    all_joined = meta.get("joined_users", set()) | set(meta.get("teams", {}).keys())
                    if user_id not in all_joined:
                        return
                
                try:
                    result = game_instance.check_answer(text, user_id, username)
                    
                    if not result:
                        return
                    
                    pts = result.get('points', 0)
                    
                    # ✅ حفظ النقاط (ما عدا التوافق)
                    if pts and not is_compatibility:
                        if meta.get("team_mode"):
                            team_name = meta["teams"].get(user_id, "team1")
                            db.add_team_points(meta["session_id"], team_name, pts)
                        else:
                            db.add_points(user_id, pts)
                            game_name = meta.get("current_game_name", "unknown")
                            db.record_game_stat(user_id, game_name, pts, result.get('game_over', False))
                    
                    # ✅ نهاية اللعبة
                    if result.get('game_over'):
                        if meta.get("session_id"):
                            db.finish_session(meta["session_id"], pts)
                        
                        # ✅ لعبة التوافق: بدون إعلان فائز
                        if is_compatibility:
                            # إرسال النتيجة مباشرة
                            if result.get('response'):
                                response_msg = result['response']
                                attach_quick_reply(response_msg)
                                line_api.reply_message(ReplyMessageRequest(reply_token=event.reply_token, messages=[response_msg]))
                                return
                        else:
                            # باقي الألعاب: إعلان فائز
                            if meta.get("team_mode"):
                                team_pts = db.get_team_points(meta["session_id"])
                                from ui_builder import build_team_game_end
                                reply_message = build_team_game_end(team_pts, current_theme)
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
                            response_msg = result['response']
                            attach_quick_reply(response_msg)
                            line_api.reply_message(ReplyMessageRequest(reply_token=event.reply_token, messages=[response_msg]))
                            return
                        else:
                            from ui_builder import build_answer_feedback
                            reply_message = build_answer_feedback(result.get('message', '✅'), current_theme)
                
                except Exception as e:
                    logger.error(f"❌ خطأ في check_answer: {e}")
                    logger.error(traceback.format_exc())
                    if game_id in active_games:
                        del active_games[game_id]
                    from ui_builder import build_error_message
                    reply_message = build_error_message(f"❌ حدث خطأ", current_theme)

            # إرسال الرد مع Quick Reply دائماً
            if reply_message:
                attach_quick_reply(reply_message)
                line_api.reply_message(ReplyMessageRequest(reply_token=event.reply_token, messages=[reply_message]))

    except Exception as e:
        logger.error(f"❌ خطأ عام في handle_message: {e}")
        logger.error(traceback.format_exc())

# -------------------------
# تنظيف دوري
# -------------------------
def periodic_cleanup():
    """تنظيف دوري للذاكرة"""
    def _cleanup():
        while True:
            try:
                time.sleep(300)  # كل 5 دقائق
                now = datetime.utcnow()
                
                # تنظيف الكاش
                for uid in list(user_cache.keys()):
                    if uid.endswith("_time"):
                        continue
                    t = user_cache.get(f"{uid}_time", datetime.min)
                    if now - t > timedelta(minutes=30):
                        user_cache.pop(uid, None)
                        user_cache.pop(f"{uid}_time", None)
                
                # تنظيف الجلسات القديمة
                for game_id in list(session_meta.keys()):
                    meta = session_meta[game_id]
                    if game_id not in active_games and meta.get("session_id"):
                        session_meta.pop(game_id, None)
                
                logger.info("✅ تنظيف دوري مكتمل")
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
    logger.info(f"🚀 {BOT_NAME} v{BOT_VERSION} - FINAL FIXED")
    logger.info(f"✅ الألعاب المتاحة: {len(AVAILABLE_GAMES)}")
    logger.info(f"✅ وضع الفريقين: بدون لمح/جاوب نهائياً")
    logger.info(f"✅ لعبة التوافق: بدون نقاط/إعلان")
    logger.info(f"🌐 المنفذ: {port}")
    logger.info("=" * 70)
    app.run(host="0.0.0.0", port=port, debug=False)
