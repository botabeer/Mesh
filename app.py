import os
import sys
import logging
from datetime import datetime, timedelta
from collections import defaultdict
from flask import Flask, request, abort, jsonify
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import Configuration, ApiClient, MessagingApi, ReplyMessageRequest, TextMessage
from linebot.v3.webhooks import MessageEvent, TextMessageContent
from config import Config
from database import Database
from ui_builder import UIBuilder
from game_manager import GameManager

app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                   handlers=[logging.StreamHandler(sys.stdout)])
logger = logging.getLogger("botmesh")

try:
    Config.validate()
except Exception as e:
    logger.error(f"Config error: {e}")
    sys.exit(1)

configuration = Configuration(access_token=Config.LINE_ACCESS_TOKEN)
handler = WebhookHandler(Config.LINE_SECRET)
db = Database()
ui = UIBuilder()
game_mgr = GameManager(db)

user_sessions = {}
pending_registrations = {}
user_rate_limit = defaultdict(list)
user_cache = {}

def is_rate_limited(user_id: str) -> bool:
    now = datetime.utcnow()
    window = timedelta(seconds=60)
    user_rate_limit[user_id] = [t for t in user_rate_limit[user_id] if now - t < window]
    if len(user_rate_limit[user_id]) >= 30:
        return True
    user_rate_limit[user_id].append(now)
    return False

def get_user_profile(line_api, user_id: str, src_type: str):
    if user_id in user_cache:
        cached = user_cache[user_id]
        if datetime.utcnow() - cached.get('_cached_at', datetime.min) < timedelta(minutes=5):
            return cached
    
    user = db.get_user(user_id)
    if not user:
        name = 'User'
        if src_type == "user":
            try:
                profile = line_api.get_profile(user_id)
                name = profile.display_name if hasattr(profile, 'display_name') else 'User'
            except Exception as e:
                logger.error(f"Profile error: {e}")
        db.create_user(user_id, name[:50])
        user = db.get_user(user_id)
    
    if user:
        user['_cached_at'] = datetime.utcnow()
        user_cache[user_id] = user
    return user

@app.route("/", methods=['GET'])
def home():
    stats = db.get_stats()
    active = game_mgr.get_active_count()
    total = game_mgr.get_total_games()
    return f"""<!DOCTYPE html>
<html dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{Config.BOT_NAME}</title><style>*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'Segoe UI',sans-serif;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);
min-height:100vh;display:flex;align-items:center;justify-content:center;padding:20px}}
.c{{max-width:600px;width:100%;background:white;border-radius:20px;padding:40px;
box-shadow:0 20px 60px rgba(0,0,0,0.3)}}h1{{color:#667eea;margin-bottom:10px;font-size:2.5em}}
.v{{color:#999;margin-bottom:20px}}.st{{display:inline-block;padding:8px 20px;
background:#28a745;color:white;border-radius:25px;font-weight:bold;margin:15px 0}}
.stats{{display:grid;grid-template-columns:repeat(2,1fr);gap:20px;margin:30px 0}}
.stat{{background:#f8f9fa;padding:25px;border-radius:15px;text-align:center;border:2px solid #e9ecef}}
.sv{{font-size:2.5em;font-weight:bold;color:#667eea;margin:10px 0}}
.sl{{color:#666;font-size:0.9em}}
.f{{margin-top:30px;padding-top:20px;border-top:2px solid #eee;text-align:center;color:#999}}
</style></head><body><div class="c"><h1>{Config.BOT_NAME}</h1>
<div class="v">v{Config.VERSION}</div><div class="st">Online</div>
<div class="stats"><div class="stat"><div class="sl">Active</div>
<div class="sv">{active}</div></div><div class="stat">
<div class="sl">Total</div><div class="sv">{total}</div></div>
<div class="stat"><div class="sl">Users</div><div class="sv">{stats.get('total_users',0)}</div></div>
<div class="stat"><div class="sl">Registered</div><div class="sv">{stats.get('registered_users',0)}</div>
</div></div><div class="f">{Config.RIGHTS}</div></div></body></html>"""

@app.route("/health", methods=['GET'])
def health():
    return jsonify({"status":"ok","ts":datetime.now().isoformat(),"active":game_mgr.get_active_count()}), 200

@app.route("/callback", methods=['POST'])
def callback():
    sig = request.headers.get('X-Line-Signature', '')
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, sig)
    except InvalidSignatureError:
        logger.warning("Invalid sig")
        abort(400)
    except Exception as e:
        logger.error(f"Webhook err: {e}")
    return "OK", 200

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    try:
        user_id = event.source.user_id
        text = event.message.text.strip() if event.message.text else ""
        if not text or len(text) > 1000:
            return
        if is_rate_limited(user_id):
            return
        
        src_type = event.source.type
        ctx_id = event.source.group_id if src_type == "group" else (
            event.source.room_id if src_type == "room" else user_id)
        
        with ApiClient(configuration) as api_client:
            line_api = MessagingApi(api_client)
            user = get_user_profile(line_api, user_id, src_type)
            if not user:
                return
            
            username = user.get('name', 'User')
            points = user.get('points', 0)
            is_reg = bool(user.get('is_registered', 0))
            theme = user.get('theme', 'ابيض')
            
            if user_id in pending_registrations:
                if 0 < len(text) <= 100:
                    db.update_user_name(user_id, text)
                    db.update_user(user_id, is_registered=1)
                    user_cache.pop(user_id, None)
                    del pending_registrations[user_id]
                    msg = ui.registration_success(text, points, theme)
                else:
                    msg = TextMessage(text="الاسم غير صالح")
                line_api.reply_message(ReplyMessageRequest(reply_token=event.reply_token, messages=[msg]))
                return
            
            norm = Config.normalize(text)
            
            if norm in ["بداية", "home", "start"]:
                mode = user_sessions.get(ctx_id, {}).get('mode', 'فردي')
                msg = ui.home_screen(username, points, is_reg, theme, mode)
                line_api.reply_message(ReplyMessageRequest(reply_token=event.reply_token, messages=[msg]))
                return
            
            if norm in ["العاب", "games"]:
                top = db.get_popular_games(13)
                msg = ui.games_menu(theme, top)
                line_api.reply_message(ReplyMessageRequest(reply_token=event.reply_token, messages=[msg]))
                return
            
            if norm == "مساعدة":
                msg = ui.help_screen(theme)
                line_api.reply_message(ReplyMessageRequest(reply_token=event.reply_token, messages=[msg]))
                return
            
            if norm == "نقاطي":
                stats = db.get_user_stats(user_id) if is_reg else None
                msg = ui.my_points(username, points, stats, theme)
                line_api.reply_message(ReplyMessageRequest(reply_token=event.reply_token, messages=[msg]))
                return
            
            if norm == "صدارة":
                top = db.get_leaderboard(20)
                msg = ui.leaderboard(top, theme)
                line_api.reply_message(ReplyMessageRequest(reply_token=event.reply_token, messages=[msg]))
                return
            
            if norm == "انضم":
                if is_reg:
                    msg = TextMessage(text=f"مسجل\n\n{username}\nالنقاط {points}")
                else:
                    pending_registrations[user_id] = True
                    msg = ui.registration_prompt(theme)
                line_api.reply_message(ReplyMessageRequest(reply_token=event.reply_token, messages=[msg]))
                return
            
            if norm == "انسحب":
                if is_reg:
                    db.update_user(user_id, is_registered=0)
                    user_cache.pop(user_id, None)
                    msg = ui.unregister_confirm(username, points, theme)
                else:
                    msg = TextMessage(text="غير مسجل")
                line_api.reply_message(ReplyMessageRequest(reply_token=event.reply_token, messages=[msg]))
                return
            
            if norm == "ايقاف":
                stopped = game_mgr.stop_game(ctx_id)
                if stopped:
                    msg = ui.game_stopped(stopped, theme)
                    line_api.reply_message(ReplyMessageRequest(reply_token=event.reply_token, messages=[msg]))
                return
            
            if text.startswith("ثيم "):
                theme_name = text.split(maxsplit=1)[1].strip()
                if Config.is_valid_theme(theme_name):
                    db.set_user_theme(user_id, theme_name)
                    user_cache.pop(user_id, None)
                    mode = user_sessions.get(ctx_id, {}).get('mode', 'فردي')
                    msg = ui.home_screen(username, points, is_reg, theme_name, mode)
                else:
                    msg = TextMessage(text="ثيم غير صالح")
                line_api.reply_message(ReplyMessageRequest(reply_token=event.reply_token, messages=[msg]))
                return
            
            if src_type in ["group", "room"]:
                if norm == "فريقين":
                    user_sessions.setdefault(ctx_id, {})['mode'] = "فريقين"
                    msg = TextMessage(text="تم تفعيل وضع الفريقين")
                    line_api.reply_message(ReplyMessageRequest(reply_token=event.reply_token, messages=[msg]))
                    return
                if norm == "فردي":
                    user_sessions.setdefault(ctx_id, {})['mode'] = "فردي"
                    msg = TextMessage(text="تم تفعيل الوضع الفردي")
                    line_api.reply_message(ReplyMessageRequest(reply_token=event.reply_token, messages=[msg]))
                    return
            
            result = game_mgr.process_message(ctx_id, user_id, username, text, 
                                             is_reg, theme, src_type)
            if result:
                msgs = result.get('messages', [])
                if msgs:
                    line_api.reply_message(ReplyMessageRequest(reply_token=event.reply_token, messages=msgs))
                if result.get('points', 0) > 0:
                    db.add_points(user_id, result['points'])
                    user_cache.pop(user_id, None)
    except Exception as e:
        logger.error(f"Handler err: {e}", exc_info=True)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    logger.info(f"Starting on {port}")
    app.run(host="0.0.0.0", port=port, debug=False, threaded=True)
