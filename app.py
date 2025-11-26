"""
Bot Mesh v7.0 - Enhanced Main Application
نظام محسن بالكامل مع أداء عالي واستقرار
Created by: Enhanced System © 2025
"""

import os
import logging
from datetime import datetime
from flask import Flask, request, abort, jsonify
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi,
    ReplyMessageRequest, TextMessage
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent

# استيراد المحرك المحسن
from core.game_manager import game_manager, GameMode
import ui

# ============================================================================
# تكوين النظام
# ============================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# LINE Configuration
LINE_SECRET = os.getenv('LINE_CHANNEL_SECRET')
LINE_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')

if not LINE_SECRET or not LINE_TOKEN:
    logger.critical("❌ LINE credentials missing! Set LINE_CHANNEL_SECRET and LINE_CHANNEL_ACCESS_TOKEN")
    exit(1)

configuration = Configuration(access_token=LINE_TOKEN)
handler = WebhookHandler(LINE_SECRET)

# ============================================================================
# تحميل الألعاب تلقائياً
# ============================================================================

def auto_load_games():
    """تحميل جميع الألعاب من مجلد games/"""
    import importlib
    import os
    
    games_loaded = 0
    games_dir = os.path.join(os.path.dirname(__file__), 'games')
    
    if not os.path.exists(games_dir):
        logger.warning("⚠️ مجلد games/ غير موجود")
        return games_loaded
    
    for filename in os.listdir(games_dir):
        if filename.endswith('.py') and not filename.startswith('_'):
            module_name = filename[:-3]
            
            try:
                # استيراد الوحدة
                module = importlib.import_module(f'games.{module_name}')
                
                # تنفيذ دالة register إن وجدت
                if hasattr(module, 'register'):
                    module.register()
                    games_loaded += 1
                    logger.info(f"✅ تم تحميل: games.{module_name}")
                
            except Exception as e:
                logger.error(f"❌ فشل تحميل games.{module_name}: {e}")
    
    return games_loaded

# تحميل الألعاب عند بدء التطبيق
games_count = auto_load_games()
logger.info(f"📦 تم تحميل {games_count} لعبة")

# ============================================================================
# قاعدة بيانات المستخدمين (يمكن استبدالها بـ Redis/PostgreSQL)
# ============================================================================

class UserManager:
    """إدارة بيانات المستخدمين"""
    
    def __init__(self):
        self.users = {}  # {user_id: UserData}
        self.stats = {
            "total_users": 0,
            "total_messages": 0,
            "start_time": datetime.now()
        }
    
    def get_or_create(self, user_id: str, username: str) -> dict:
        """الحصول على مستخدم أو إنشاؤه"""
        if user_id not in self.users:
            self.users[user_id] = {
                "id": user_id,
                "name": username,
                "points": 0,
                "games_played": 0,
                "games_won": 0,
                "theme": "💜",
                "created_at": datetime.now(),
                "last_active": datetime.now()
            }
            self.stats["total_users"] += 1
            logger.info(f"👤 مستخدم جديد: {username}")
        
        self.users[user_id]["last_active"] = datetime.now()
        return self.users[user_id]
    
    def update_points(self, user_id: str, points: int):
        """تحديث نقاط المستخدم"""
        if user_id in self.users:
            self.users[user_id]["points"] += points
    
    def get_leaderboard(self, limit: int = 10) -> list:
        """الحصول على لوحة الصدارة"""
        sorted_users = sorted(
            self.users.values(),
            key=lambda u: (u["points"], u["games_won"]),
            reverse=True
        )
        return [(u["name"], u["points"]) for u in sorted_users[:limit]]

user_manager = UserManager()

# ============================================================================
# معالج الرسائل الرئيسي
# ============================================================================

def get_room_id(event) -> str:
    """تحديد معرف الغرفة/المحادثة"""
    if hasattr(event.source, 'group_id'):
        return f"group_{event.source.group_id}"
    elif hasattr(event.source, 'room_id'):
        return f"room_{event.source.room_id}"
    else:
        return f"user_{event.source.user_id}"


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    """معالج الرسائل المحسن"""
    try:
        user_manager.stats["total_messages"] += 1
        
        user_id = event.source.user_id
        room_id = get_room_id(event)
        text = event.message.text.strip()
        
        with ApiClient(configuration) as api_client:
            line_api = MessagingApi(api_client)
            
            # الحصول على اسم المستخدم
            try:
                profile = line_api.get_profile(user_id)
                username = profile.display_name or "لاعب"
            except:
                username = "لاعب"
            
            # الحصول على/إنشاء بيانات المستخدم
            user = user_manager.get_or_create(user_id, username)
            
            # تنظيف الألعاب المنتهية كل 10 رسائل
            if user_manager.stats["total_messages"] % 10 == 0:
                game_manager.cleanup_expired_games()
            
            # ============================================================
            # معالجة الأوامر
            # ============================================================
            
            reply = None
            
            # الشاشة الرئيسية
            if text in ["بداية", "البداية", "start", "home", "@"]:
                reply = ui.home_screen(username, user["points"], user["theme"])
            
            # قائمة الألعاب
            elif text in ["العاب", "الألعاب", "ألعاب", "games"]:
                stats = game_manager.get_statistics()
                available_games = stats["available_games"]
                reply = ui.games_menu(available_games, user["theme"])
            
            # الصدارة
            elif text in ["صدارة", "الصدارة", "leaderboard"]:
                top_players = user_manager.get_leaderboard()
                reply = ui.leaderboard(top_players, user["theme"])
            
            # الثيمات
            elif text in ["ثيمات", "الثيمات", "themes"]:
                reply = ui.themes_selector(user["theme"])
            
            elif text.startswith("ثيم "):
                theme_emoji = text.replace("ثيم ", "").strip()
                if theme_emoji in ui.THEMES:
                    user["theme"] = theme_emoji
                    reply = TextMessage(
                        text=f"✅ تم تغيير الثيم إلى {ui.THEMES[theme_emoji]['name']}"
                    )
                else:
                    reply = TextMessage(text="❌ ثيم غير موجود!")
            
            # بدء لعبة جديدة
            elif text.startswith("لعبة "):
                game_name = text.replace("لعبة ", "").strip()
                
                # تحديد وضع اللعب (افتراضي: فردي)
                mode = GameMode.SINGLE
                if "group_" in room_id:
                    mode = GameMode.GROUP
                
                game = game_manager.create_game(room_id, game_name, mode)
                
                if game:
                    result = game.start()
                    if result.get("valid"):
                        reply = ui.game_question(
                            result["question"]["game"],
                            result["question"]["question"],
                            result["question"]["round"],
                            result["question"]["total_rounds"],
                            result["question"]["mode"],
                            user["theme"]
                        )
                    else:
                        reply = TextMessage(text="❌ فشل بدء اللعبة")
                else:
                    reply = TextMessage(text=f"❌ اللعبة '{game_name}' غير موجودة")
            
            # التعامل مع لعبة نشطة
            elif game_manager.get_game(room_id):
                game = game_manager.get_game(room_id)
                
                # أوامر اللعبة
                if text in ["تلميح", "لمح", "hint"]:
                    result = game.get_hint(user_id)
                    reply = TextMessage(text=result.get("message", ""))
                
                elif text in ["اجابة", "إجابة", "جاوب", "reveal"]:
                    result = game.reveal_answer()
                    
                    if result.get("game_over"):
                        # اللعبة انتهت
                        game_manager.remove_game(room_id)
                        results = result["results"]
                        
                        # تحديث نقاط اللاعبين
                        for player_data in results["players"]:
                            # البحث عن المستخدم بالاسم (يمكن تحسينه)
                            for uid, udata in user_manager.users.items():
                                if udata["name"] == player_data["name"]:
                                    user_manager.update_points(uid, player_data["points"])
                                    break
                        
                        reply = ui.game_result(
                            results["winner"]["name"] if results["winner"] else "لا أحد",
                            results["winner"]["points"] if results["winner"] else 0,
                            [(p["name"], p["points"]) for p in results["players"]],
                            game.mode.value,
                            user["theme"]
                        )
                    else:
                        # سؤال تالٍ
                        q = result["question"]
                        reply = ui.game_question(
                            q["game"], q["question"], q["round"],
                            q["total_rounds"], q["mode"], user["theme"]
                        )
                        # إضافة رسالة الإجابة
                        if result.get("message"):
                            # يمكن إرسال رسالتين: واحدة للإجابة وواحدة للسؤال
                            pass
                
                elif text in ["ايقاف", "إيقاف", "stop", "quit"]:
                    result = game.stop()
                    game_manager.remove_game(room_id)
                    reply = TextMessage(text=result.get("message", "⛔ تم إيقاف اللعبة"))
                
                else:
                    # محاولة إجابة
                    result = game.submit_answer(user_id, username, text)
                    
                    if not result.get("valid"):
                        reply = TextMessage(text=result.get("message", ""))
                    
                    elif result.get("game_over"):
                        # اللعبة انتهت
                        game_manager.remove_game(room_id)
                        results = result["results"]
                        
                        # تحديث النقاط
                        for player_data in results["players"]:
                            for uid, udata in user_manager.users.items():
                                if udata["name"] == player_data["name"]:
                                    user_manager.update_points(uid, player_data["points"])
                                    break
                        
                        reply = ui.game_result(
                            results["winner"]["name"] if results["winner"] else "لا أحد",
                            results["winner"]["points"] if results["winner"] else 0,
                            [(p["name"], p["points"]) for p in results["players"]],
                            game.mode.value,
                            user["theme"]
                        )
                    
                    elif result.get("question"):
                        # سؤال تالٍ
                        q = result["question"]
                        reply = ui.game_question(
                            q["game"], q["question"], q["round"],
                            q["total_rounds"], q["mode"], user["theme"]
                        )
                    
                    else:
                        # إجابة خاطئة
                        reply = TextMessage(text=result.get("message", ""))
            
            # رسالة افتراضية
            else:
                reply = ui.home_screen(username, user["points"], user["theme"])
            
            # إرسال الرد
            if reply:
                line_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[reply]
                    )
                )
    
    except Exception as e:
        logger.error(f"❌ خطأ في معالجة الرسالة: {e}", exc_info=True)


# ============================================================================
# Flask Routes
# ============================================================================

@app.route("/callback", methods=['POST'])
def callback():
    """Webhook callback من LINE"""
    signature = request.headers.get('X-Line-Signature', '')
    body = request.get_data(as_text=True)
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        logger.error("❌ توقيع غير صحيح")
        abort(400)
    except Exception as e:
        logger.error(f"❌ خطأ في Callback: {e}")
        abort(500)
    
    return 'OK'


@app.route("/", methods=['GET'])
def home():
    """الصفحة الرئيسية"""
    stats = game_manager.get_statistics()
    user_stats = user_manager.stats
    
    uptime = datetime.now() - user_stats["start_time"]
    uptime_str = str(uptime).split('.')[0]
    
    return f"""
    <!DOCTYPE html>
    <html dir="rtl" lang="ar">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Bot Mesh v7.0</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: #fff;
                margin: 0;
                padding: 20px;
            }}
            .container {{
                max-width: 800px;
                margin: 0 auto;
                background: rgba(255,255,255,0.1);
                backdrop-filter: blur(10px);
                border-radius: 20px;
                padding: 30px;
                box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            }}
            h1 {{ font-size: 2.5em; margin-bottom: 10px; }}
            .stats {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
                margin-top: 30px;
            }}
            .stat-box {{
                background: rgba(255,255,255,0.2);
                padding: 20px;
                border-radius: 15px;
                text-align: center;
            }}
            .stat-value {{
                font-size: 2em;
                font-weight: bold;
                margin: 10px 0;
            }}
            .stat-label {{
                font-size: 0.9em;
                opacity: 0.9;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎮 Bot Mesh v7.0</h1>
            <p>نظام ألعاب ذكي ومحسّن</p>
            
            <div class="stats">
                <div class="stat-box">
                    <div class="stat-label">⏱️ وقت التشغيل</div>
                    <div class="stat-value">{uptime_str}</div>
                </div>
                
                <div class="stat-box">
                    <div class="stat-label">👥 المستخدمون</div>
                    <div class="stat-value">{user_stats['total_users']}</div>
                </div>
                
                <div class="stat-box">
                    <div class="stat-label">🎮 الألعاب النشطة</div>
                    <div class="stat-value">{stats['active_games']}</div>
                </div>
                
                <div class="stat-box">
                    <div class="stat-label">📊 إجمالي الألعاب</div>
                    <div class="stat-value">{stats['total_games_created']}</div>
                </div>
                
                <div class="stat-box">
                    <div class="stat-label">💬 الرسائل</div>
                    <div class="stat-value">{user_stats['total_messages']}</div>
                </div>
                
                <div class="stat-box">
                    <div class="stat-label">🎯 ألعاب متاحة</div>
                    <div class="stat-value">{len(stats['available_games'])}</div>
                </div>
            </div>
            
            <div style="margin-top: 30px; text-align: center; opacity: 0.8;">
                <p>📦 Cache Hit Rate: {stats['cache_stats']['hit_rate']}</p>
                <p>🔧 Enhanced System © 2025</p>
            </div>
        </div>
    </body>
    </html>
    """


@app.route("/health", methods=['GET'])
def health():
    """فحص صحة الخادم"""
    stats = game_manager.get_statistics()
    
    return jsonify({
        "status": "healthy",
        "version": "7.0",
        "uptime_hours": stats["uptime_hours"],
        "users": user_manager.stats["total_users"],
        "active_games": stats["active_games"],
        "total_games": stats["total_games_created"],
        "cache": stats["cache_stats"]
    }), 200


@app.route("/stats", methods=['GET'])
def statistics():
    """إحصائيات مفصلة"""
    return jsonify({
        "game_manager": game_manager.get_statistics(),
        "users": {
            "total": user_manager.stats["total_users"],
            "messages": user_manager.stats["total_messages"]
        }
    }), 200


# ============================================================================
# تشغيل التطبيق
# ============================================================================

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    
    logger.info("=" * 70)
    logger.info("🎮 Bot Mesh v7.0 - Enhanced Edition")
    logger.info(f"📦 {games_count} ألعاب محملة")
    logger.info("✨ محرك موحد مع أداء محسّن")
    logger.info("🎨 9 ثيمات جميلة")
    logger.info("👥 دعم اللعب الفردي والمجموعة")
    logger.info(f"🌐 Port {port}")
    logger.info("=" * 70)
    
    app.run(host="0.0.0.0", port=port, debug=False)
