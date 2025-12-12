import os
import sys
import logging
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

from config import Config
from database import Database
from ui_builder import UIBuilder
from game_manager import GameManager

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("botmesh")

try:
    Config.validate()
    logger.info("تم التحقق من الإعدادات بنجاح")
except Exception as e:
    logger.error(f"خطأ في الإعدادات: {e}")
    sys.exit(1)

configuration = Configuration(access_token=Config.LINE_ACCESS_TOKEN)
handler = WebhookHandler(Config.LINE_SECRET)

db = Database(Config.DATABASE_PATH)
ui = UIBuilder()
game_mgr = GameManager(db)

user_sessions = {}
pending_registrations = {}
user_rate_limit = defaultdict(list)
user_cache = {}


def is_rate_limited(user_id: str) -> bool:
    now = datetime.utcnow()
    window = timedelta(seconds=Config.RATE_LIMIT_WINDOW)
    timestamps = [t for t in user_rate_limit[user_id] if now - t < window]
    user_rate_limit[user_id] = timestamps
    
    if len(timestamps) >= Config.RATE_LIMIT_MESSAGES:
        logger.warning(f"تجاوز معدل الرسائل: {user_id}")
        return True
    
    user_rate_limit[user_id].append(now)
    return False


def get_user_profile(line_api, user_id: str, src_type: str):
    if user_id in user_cache:
        cached = user_cache[user_id]
        if datetime.utcnow() - cached.get("_cached_at", datetime.min) < timedelta(minutes=5):
            return cached
    
    user = db.get_user(user_id)
    
    if not user:
        name = "مستخدم"
        if src_type == "user":
            try:
                profile = line_api.get_profile(user_id)
                if hasattr(profile, "display_name"):
                    name = profile.display_name or "مستخدم"
            except Exception as e:
                logger.error(f"خطأ في جلب الملف الشخصي: {e}")
        
        db.create_user(user_id, name[:100])
        user = db.get_user(user_id)
    
    user["_cached_at"] = datetime.utcnow()
    user_cache[user_id] = user
    return user


@app.route("/", methods=["GET"])
def home():
    stats = db.get_stats()
    active = game_mgr.get_active_count()
    db_size = db.get_database_size() / 1024 / 1024
    
    return f"""<!DOCTYPE html>
<html dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{Config.BOT_NAME}</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
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
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    border-radius: 24px;
    padding: 40px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
}}
h1 {{
    color: #667eea;
    font-size: 2.5em;
    margin-bottom: 10px;
    text-align: center;
}}
.version {{
    color: #999;
    margin-bottom: 20px;
    text-align: center;
}}
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
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
    margin: 30px 0;
}}
.stat {{
    background: rgba(245, 245, 250, 0.9);
    padding: 25px;
    border-radius: 16px;
    text-align: center;
    transition: transform 0.3s;
}}
.stat:hover {{ transform: translateY(-5px); }}
.stat-value {{
    font-size: 2.5em;
    font-weight: bold;
    color: #667eea;
    margin: 10px 0;
}}
.stat-label {{
    color: #666;
    font-size: 0.9em;
}}
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
<h1>{Config.BOT_NAME}</h1>
<div class="version">v{Config.VERSION}</div>
<div style="text-align:center"><div class="status">Online</div></div>
<div class="stats">
<div class="stat"><div class="stat-label">الألعاب النشطة</div><div class="stat-value">{active}</div></div>
<div class="stat"><div class="stat-label">المستخدمين</div><div class="stat-value">{stats.get('total_users', 0)}</div></div>
<div class="stat"><div class="stat-label">المسجلين</div><div class="stat-value">{stats.get('registered_users', 0)}</div></div>
<div class="stat"><div class="stat-label">النشطون اليوم</div><div class="stat-value">{stats.get('active_today', 0)}</div></div>
<div class="stat"><div class="stat-label">حجم قاعدة البيانات</div><div class="stat-value">{db_size:.2f} MB</div></div>
</div>
<div class="footer">{Config.RIGHTS}</div>
</div>
</body>
</html>"""


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat(),
        "active_games": game_mgr.get_active_count(),
        "version": Config.VERSION
    }), 200


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        logger.warning("توقيع غير صالح")
        abort(400)
    except Exception as e:
        logger.error(f"خطأ في معالجة Webhook: {e}", exc_info=True)
    
    return "OK", 200


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    try:
        user_id = event.source.user_id
        text = (event.message.text or "").strip()
        
        if not text or len(text) > 1000:
            return
        
        if is_rate_limited(user_id):
            return
        
        src_type = event.source.type
        ctx_id = (
            event.source.group_id if src_type == "group" else
            event.source.room_id if src_type == "room" else
            user_id
        )
        
        with ApiClient(configuration) as api_client:
            line_api = MessagingApi(api_client)
            user = get_user_profile(line_api, user_id, src_type)
            
            if not user:
                return
            
            username = user.get("name", "مستخدم")
            points = user.get("points", 0)
            is_reg = bool(user.get("is_registered", 0))
            theme = user.get("theme", "فاتح")
            
            # تسجيل اسم جديد
            if user_id in pending_registrations:
                if 0 < len(text) <= 100:
                    db.update_user(user_id, name=text, is_registered=1)
                    user_cache.pop(user_id, None)
                    del pending_registrations[user_id]
                    msg = ui.registration_success(text, points, theme)
                else:
                    msg = TextMessage(text="الاسم غير صالح")
                
                line_api.reply_message(ReplyMessageRequest(reply_token=event.reply_token, messages=[msg]))
                return
            
            norm = Config.normalize(text)
            
            # شاشة البداية
            if norm in ["بداية", "start", "home"]:
                msg = ui.home_screen(username, points, is_reg, theme)
                line_api.reply_message(ReplyMessageRequest(reply_token=event.reply_token, messages=[msg]))
                return
            
            # قائمة الألعاب
            if norm in ["العاب", "games", "الالعاب"]:
                msg = ui.games_menu(theme)
                line_api.reply_message(ReplyMessageRequest(reply_token=event.reply_token, messages=[msg]))
                return
            
            # مساعدة
            if norm in ["مساعدة", "help"]:
                msg = ui.help_screen(theme)
                line_api.reply_message(ReplyMessageRequest(reply_token=event.reply_token, messages=[msg]))
                return
            
            # نقاطي
            if norm == "نقاطي":
                stats = db.get_user_stats(user_id) if is_reg else None
                msg = ui.my_points(username, points, stats, theme)
                line_api.reply_message(ReplyMessageRequest(reply_token=event.reply_token, messages=[msg]))
                return
            
            # صدارة
            if norm == "صدارة":
                top = db.get_leaderboard(20)
                msg = ui.leaderboard(top, theme)
                line_api.reply_message(ReplyMessageRequest(reply_token=event.reply_token, messages=[msg]))
                return
            
            # تسجيل
            if norm == "انضم":
                if is_reg:
                    msg = TextMessage(text=f"انت مسجل بالفعل\nالاسم: {username}\nالنقاط: {points}")
                else:
                    pending_registrations[user_id] = True
                    msg = ui.registration_prompt(theme)
                
                line_api.reply_message(ReplyMessageRequest(reply_token=event.reply_token, messages=[msg]))
                return
            
            # إلغاء التسجيل
            if norm == "انسحب":
                if is_reg:
                    db.update_user(user_id, is_registered=0)
                    user_cache.pop(user_id, None)
                    msg = ui.unregister_confirm(username, points, theme)
                else:
                    msg = TextMessage(text="انت غير مسجل")
                
                line_api.reply_message(ReplyMessageRequest(reply_token=event.reply_token, messages=[msg]))
                return
            
            # إيقاف الألعاب
            if norm in ["ايقاف", "stop"]:
                stopped = game_mgr.stop_game(ctx_id)
                if stopped:
                    msg = ui.game_stopped(stopped, theme)
                    line_api.reply_message(ReplyMessageRequest(reply_token=event.reply_token, messages=[msg]))
                return
            
            # تغيير الثيم
            if text.startswith("ثيم "):
                new_theme = text.split(maxsplit=1)[1].strip()
                
                if Config.is_valid_theme(new_theme):
                    db.set_user_theme(user_id, new_theme)
                    user_cache.pop(user_id, None)
                    msg = ui.home_screen(username, points, is_reg, new_theme)
                else:
                    msg = TextMessage(text="ثيم غير موجود\nالثيمات المتاحة:\nفاتح - داكن")
                
                line_api.reply_message(ReplyMessageRequest(reply_token=event.reply_token, messages=[msg]))
                return
            
            # تمرير الرسالة لمدير الألعاب
            result = game_mgr.process_message(
                ctx_id, user_id, username, text,
                is_reg, theme, src_type
            )
            
            if result:
                msgs = result.get("messages", [])
                if msgs:
                    line_api.reply_message(ReplyMessageRequest(reply_token=event.reply_token, messages=msgs))
                
                gained = result.get("points", 0)
                if gained > 0 and is_reg:
                    db.add_points(user_id, gained)
                    user_cache.pop(user_id, None)
    
    except Exception as e:
        logger.error(f"خطأ في معالج الرسائل: {e}", exc_info=True)


if __name__ == "__main__":
    port = int(os.getenv("PORT", Config.DEFAULT_PORT))
    logger.info(f"بدء التطبيق على المنفذ {port}")
    app.run(host="0.0.0.0", port=port, debug=False, threaded=True)
