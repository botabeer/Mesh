import os
import sys
import logging
import threading
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

# إعداد التطبيق
app = Flask(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("botmesh")

# التحقق من الإعدادات
try:
    Config.validate()
except Exception as e:
    logger.error(f"خطأ في الإعدادات: {e}")
    sys.exit(1)

# تهيئة المكونات
configuration = Configuration(access_token=Config.LINE_ACCESS_TOKEN)
handler = WebhookHandler(Config.LINE_SECRET)
db = Database()
ui = UIBuilder()
game_mgr = GameManager(db)

# إدارة الحالة
user_sessions = {}
pending_registrations = {}
user_rate_limit = defaultdict(list)
user_cache = {}

def is_rate_limited(user_id: str) -> bool:
    """التحقق من حد المعدل"""
    now = datetime.utcnow()
    window = timedelta(seconds=60)
    user_rate_limit[user_id] = [t for t in user_rate_limit[user_id] if now - t < window]
    
    if len(user_rate_limit[user_id]) >= 30:
        return True
    
    user_rate_limit[user_id].append(now)
    return False

def get_user_profile(line_api, user_id: str):
    """الحصول على بيانات المستخدم"""
    if user_id in user_cache:
        cached = user_cache[user_id]
        if datetime.utcnow() - cached.get('_cached_at', datetime.min) < timedelta(minutes=5):
            return cached
    
    user = db.get_user(user_id)
    if not user:
        try:
            profile = line_api.get_profile(user_id)
            name = profile.display_name if hasattr(profile, 'display_name') else 'مستخدم'
            db.create_user(user_id, name[:50])
            user = db.get_user(user_id)
        except Exception as e:
            logger.error(f"خطأ في الملف الشخصي: {e}")
            return None
    
    if user:
        user['_cached_at'] = datetime.utcnow()
        user_cache[user_id] = user
    
    return user

@app.route("/", methods=['GET'])
def home():
    """الصفحة الرئيسية"""
    stats = db.get_stats()
    active_games = game_mgr.get_active_count()
    
    return f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{Config.BOT_NAME}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }}
        .container {{
            max-width: 600px;
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
            grid-template-columns: repeat(2, 1fr);
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
        .stat-label {{ color: #666; font-size: 0.9em; }}
        .footer {{
            margin-top: 30px;
            padding-top: 20px;
            border-top: 2px solid #eee;
            text-align: center;
            color: #999;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{Config.BOT_NAME}</h1>
        <div class="version">الإصدار {Config.VERSION}</div>
        <div class="status">متصل</div>
        
        <div class="stats">
            <div class="stat">
                <div class="stat-label">الالعاب النشطة</div>
                <div class="stat-value">{active_games}</div>
            </div>
            <div class="stat">
                <div class="stat-label">اجمالي الالعاب</div>
                <div class="stat-value">{game_mgr.get_total_games()}</div>
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
            {Config.RIGHTS}
        </div>
    </div>
</body>
</html>"""

@app.route("/health", methods=['GET'])
def health():
    """فحص الصحة"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "active_games": game_mgr.get_active_count()
    }), 200

@app.route("/callback", methods=['POST'])
def callback():
    """معالج الويب هوك"""
    signature = request.headers.get('X-Line-Signature', '')
    body = request.get_data(as_text=True)
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        logger.warning("توقيع غير صالح")
        abort(400)
    except Exception as e:
        logger.error(f"خطأ في الويب هوك: {e}")
    
    return "OK", 200

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    """معالج الرسائل"""
    try:
        user_id = event.source.user_id
        text = event.message.text.strip() if event.message.text else ""
        
        if not text or len(text) > 1000:
            return
        
        if is_rate_limited(user_id):
            return
        
        # تحديد السياق
        source_type = event.source.type
        if source_type == "group":
            context_id = event.source.group_id
        elif source_type == "room":
            context_id = event.source.room_id
        else:
            context_id = user_id
        
        with ApiClient(configuration) as api_client:
            line_api = MessagingApi(api_client)
            
            # الحصول على بيانات المستخدم
            user = get_user_profile(line_api, user_id)
            if not user:
                return
            
            username = user.get('name', 'مستخدم')
            points = user.get('points', 0)
            is_registered = bool(user.get('is_registered', 0))
            theme = user.get('theme', 'أبيض')
            
            # معالجة التسجيل المعلق
            if user_id in pending_registrations:
                if 0 < len(text) <= 100:
                    db.update_user_name(user_id, text)
                    db.update_user(user_id, is_registered=1)
                    user_cache.pop(user_id, None)
                    del pending_registrations[user_id]
                    msg = ui.registration_success(text, points, theme)
                else:
                    msg = TextMessage(text="اسم غير صالح")
                
                line_api.reply_message(
                    ReplyMessageRequest(reply_token=event.reply_token, messages=[msg])
                )
                return
            
            # معالجة الأوامر
            normalized = Config.normalize(text)
            
            # القائمة الرئيسية
            if normalized in ["بداية", "home", "start"]:
                mode = user_sessions.get(context_id, {}).get('mode', 'فردي')
                msg = ui.home_screen(username, points, is_registered, theme, mode)
                line_api.reply_message(
                    ReplyMessageRequest(reply_token=event.reply_token, messages=[msg])
                )
                return
            
            # قائمة الالعاب
            if normalized in ["العاب", "games"]:
                top_games = db.get_popular_games(13)
                msg = ui.games_menu(theme, top_games)
                line_api.reply_message(
                    ReplyMessageRequest(reply_token=event.reply_token, messages=[msg])
                )
                return
            
            # المساعدة
            if normalized == "مساعدة":
                msg = ui.help_screen(theme)
                line_api.reply_message(
                    ReplyMessageRequest(reply_token=event.reply_token, messages=[msg])
                )
                return
            
            # النقاط
            if normalized == "نقاطي":
                stats = db.get_user_stats(user_id) if is_registered else None
                msg = ui.my_points(username, points, stats, theme)
                line_api.reply_message(
                    ReplyMessageRequest(reply_token=event.reply_token, messages=[msg])
                )
                return
            
            # الصدارة
            if normalized == "صدارة":
                top = db.get_leaderboard(20)
                msg = ui.leaderboard(top, theme)
                line_api.reply_message(
                    ReplyMessageRequest(reply_token=event.reply_token, messages=[msg])
                )
                return
            
            # التسجيل
            if normalized == "انضم":
                if is_registered:
                    msg = TextMessage(text=f"مسجل: {username}\nالنقاط: {points}")
                else:
                    pending_registrations[user_id] = True
                    msg = ui.registration_prompt(theme)
                
                line_api.reply_message(
                    ReplyMessageRequest(reply_token=event.reply_token, messages=[msg])
                )
                return
            
            # الانسحاب
            if normalized == "انسحب":
                if is_registered:
                    db.update_user(user_id, is_registered=0)
                    user_cache.pop(user_id, None)
                    msg = ui.unregister_confirm(username, points, theme)
                else:
                    msg = TextMessage(text="غير مسجل")
                
                line_api.reply_message(
                    ReplyMessageRequest(reply_token=event.reply_token, messages=[msg])
                )
                return
            
            # إيقاف اللعبة
            if normalized == "ايقاف":
                stopped = game_mgr.stop_game(context_id)
                if stopped:
                    msg = ui.game_stopped(stopped, theme)
                    line_api.reply_message(
                        ReplyMessageRequest(reply_token=event.reply_token, messages=[msg])
                    )
                return
            
            # تغيير الثيم
            if text.startswith("ثيم "):
                theme_name = text.split(maxsplit=1)[1].strip()
                if Config.is_valid_theme(theme_name):
                    db.set_user_theme(user_id, theme_name)
                    user_cache.pop(user_id, None)
                    mode = user_sessions.get(context_id, {}).get('mode', 'فردي')
                    msg = ui.home_screen(username, points, is_registered, theme_name, mode)
                else:
                    msg = TextMessage(text="ثيم غير موجود")
                
                line_api.reply_message(
                    ReplyMessageRequest(reply_token=event.reply_token, messages=[msg])
                )
                return
            
            # وضع الفريقين
            if source_type in ["group", "room"]:
                if normalized == "فريقين":
                    if context_id not in user_sessions:
                        user_sessions[context_id] = {}
                    user_sessions[context_id]['mode'] = "فريقين"
                    msg = TextMessage(text="وضع الفريقين")
                    line_api.reply_message(
                        ReplyMessageRequest(reply_token=event.reply_token, messages=[msg])
                    )
                    return
                
                if normalized == "فردي":
                    if context_id not in user_sessions:
                        user_sessions[context_id] = {}
                    user_sessions[context_id]['mode'] = "فردي"
                    msg = TextMessage(text="الوضع الفردي")
                    line_api.reply_message(
                        ReplyMessageRequest(reply_token=event.reply_token, messages=[msg])
                    )
                    return
            
            # بدء أو متابعة لعبة
            result = game_mgr.process_message(
                context_id, user_id, username, text, 
                is_registered, theme, source_type
            )
            
            if result:
                messages = result.get('messages', [])
                if messages:
                    line_api.reply_message(
                        ReplyMessageRequest(
                            reply_token=event.reply_token,
                            messages=messages
                        )
                    )
                
                # تحديث النقاط
                if result.get('points', 0) > 0:
                    db.add_points(user_id, result['points'])
                    user_cache.pop(user_id, None)
    
    except Exception as e:
        logger.error(f"خطأ في المعالجة: {e}")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    logger.info(f"بدء التشغيل على المنفذ {port}")
    app.run(host="0.0.0.0", port=port, debug=False, threaded=True)
