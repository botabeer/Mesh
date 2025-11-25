"""
Bot Mesh v6.1 - Main Application
Simple, Clean & Production-Ready
محدث: تغيير "جماعي" إلى "مجموعة"
"""

import os
import logging
from datetime import datetime, timedelta
from flask import Flask, request, abort
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi,
    ReplyMessageRequest, TextMessage
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent

# استيراد الوحدات
import ui
from games.game_loader import load_games

# تحميل الألعاب من مجلد games/
GAMES = load_games()

# ============================================================================
# إعداد التطبيق
# ============================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# LINE Configuration
LINE_SECRET = os.getenv('LINE_CHANNEL_SECRET')
LINE_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')

if not LINE_SECRET or LINE_TOKEN:
    logger.error("❌ LINE credentials missing!")
    exit(1)

configuration = Configuration(access_token=LINE_TOKEN)
handler = WebhookHandler(LINE_SECRET)

# ============================================================================
# قاعدة البيانات البسيطة (في الذاكرة)
# ============================================================================

# المستخدمون
users = {}  # {user_id: {"name": str, "points": int, "mode": str, "theme": str}}

# الألعاب النشطة
active_games = {}  # {room_id: Game}

# الإحصائيات
stats = {
    "total_users": 0,
    "total_games": 0,
    "total_messages": 0,
    "start_time": datetime.now()
}

# ============================================================================
# دوال مساعدة
# ============================================================================

def get_room_id(event):
    """الحصول على معرف الغرفة (للدردشات المجموعة)"""
    if hasattr(event.source, 'group_id'):
        return f"group_{event.source.group_id}"
    elif hasattr(event.source, 'room_id'):
        return f"room_{event.source.room_id}"
    else:
        return f"user_{event.source.user_id}"

def get_or_create_user(user_id, username):
    """الحصول على المستخدم أو إنشاءه"""
    if user_id not in users:
        users[user_id] = {
            "name": username,
            "points": 0,
            "mode": "فردي",
            "theme": "💜",  # الثيم الافتراضي
            "last_active": datetime.now()
        }
        stats["total_users"] += 1
    
    users[user_id]["last_active"] = datetime.now()
    return users[user_id]

def cleanup_old_games():
    """تنظيف الألعاب القديمة"""
    to_remove = []
    for room_id, game in active_games.items():
        if game.is_expired(max_minutes=30):
            to_remove.append(room_id)
    
    for room_id in to_remove:
        active_games.pop(room_id, None)
    
    if to_remove:
        logger.info(f"🧹 تم حذف {len(to_remove)}ألعاب منتهية")

def get_top_players(limit=10):
    """أفضل اللاعبين"""
    sorted_users = sorted(
        users.values(),
        key=lambda x: x["points"],
        reverse=True
    )
    return [(u["name"], u["points"]) for u in sorted_users[:limit]]

# ============================================================================
# معالج الرسائل الرئيسي
# ============================================================================

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    """معالج الرسائل"""
    try:
        stats["total_messages"] += 1
        
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
            
            # تسجيل/تحديث المستخدم
            user = get_or_create_user(user_id, username)
            
            # تنظيف الألعاب القديمة
            if stats["total_messages"] % 10 == 0:
                cleanup_old_games()
            
            # ============================================================
            # الأوامر الأساسية
            # ============================================================
            
            if text in ["بداية", "البداية", "start", "@"]:
                # الشاشة الرئيسية
                reply = ui.home_screen(username, user["points"], user["theme"])
            
            elif text in ["مجموعة", "لعب مجموعة"]:
                # تغيير الوضع إلى مجموعة
                user["mode"] = "مجموعة"
                reply = ui.games_menu(mode="مجموعة", theme=user["theme"])
            
            elif text in ["فردي", "لعب فردي"]:
                # تغيير الوضع إلى فردي
                user["mode"] = "فردي"
                reply = ui.games_menu(mode="فردي", theme=user["theme"])
            
            elif text in ["العاب", "الألعاب", "ألعاب"]:
                # قائمة الألعاب
                reply = ui.games_menu(mode=user["mode"], theme=user["theme"])
            
            elif text in ["ثيمات", "الثيمات", "themes"]:
                # شاشة اختيار الثيمات
                reply = ui.themes_selector(current_theme=user["theme"])
            
            elif text.startswith("ثيم "):
                # تغيير الثيم
                theme_emoji = text.replace("ثيم ", "").strip()
                if theme_emoji in ui.THEMES:
                    user["theme"] = theme_emoji
                    reply = TextMessage(text=f"✅ تم تغيير الثيم إلى {ui.THEMES[theme_emoji]['name']}")
                else:
                    reply = TextMessage(text="❌ ثيم غير موجود!")
            
            elif text in ["صدارة", "الصدارة", "leaderboard"]:
                # لوحة الصدارة
                top = get_top_players()
                reply = ui.leaderboard(top, theme=user["theme"])
            
            # ============================================================
            # بدء لعبة جديدة
            # ============================================================
            
            elif text.startswith("لعبة "):
                game_name = text.replace("لعبة ", "").strip()
                
                # إنشاء اللعبة من مجلد games/
                if game_name in GAMES:
                    game = GAMES[game_name](mode=user["mode"])
                    
                    # حفظ اللعبة
                    active_games[room_id] = game
                    stats["total_games"] += 1
                    
                    # بدء اللعبة
                    q_data = game.start()
                    reply = ui.game_question(
                        q_data["game"],
                        q_data["question"],
                        q_data["round"],
                        q_data["total_rounds"],
                        q_data["mode"],
                        user["theme"]
                    )
                else:
                    reply = TextMessage(text="❌ لعبة غير موجودة!")
            
            # ============================================================
            # التعامل مع الألعاب النشطة
            # ============================================================
            
            elif room_id in active_games:
                game = active_games[room_id]
                
                # أوامر خاصة
                if text in ["تلميح", "لمح", "hint"]:
                    hint = game.get_hint()
                    reply = TextMessage(text=hint)
                
                elif text in ["اجابة", "إجابة", "جاوب", "reveal"]:
                    result = game.reveal_answer()
                    
                    if result.get("game_over"):
                        # انتهت اللعبة
                        del active_games[room_id]
                        results = result["results"]
                        reply = ui.game_result(
                            results["winner_name"],
                            results["winner_points"],
                            results["all_players"],
                            results["mode"],
                            user["theme"]
                        )
                        
                        # تحديث نقاط اللاعبين
                        for uid, data in game.scores.items():
                            if uid in users:
                                users[uid]["points"] += data["points"]
                    else:
                        # السؤال التالي
                        q_data = result["next_question"]
                        answer_msg = f"📝 الإجابة: {result['answer']}\n\n"
                        reply = ui.game_question(
                            q_data["game"],
                            q_data["question"],
                            q_data["round"],
                            q_data["total_rounds"],
                            q_data["mode"],
                            user["theme"]
                        )
                
                elif text in ["ايقاف", "إيقاف", "stop", "خروج"]:
                    # إيقاف اللعبة
                    del active_games[room_id]
                    reply = TextMessage(text="⛔ تم إيقاف اللعبة")
                
                else:
                    # فحص الإجابة
                    result = game.check_answer(user_id, username, text)
                    
                    if not result["valid"]:
                        reply = TextMessage(text=result["message"])
                    
                    elif result["correct"]:
                        if result.get("game_over"):
                            # انتهت اللعبة
                            del active_games[room_id]
                            results = result["results"]
                            reply = ui.game_result(
                                results["winner_name"],
                                results["winner_points"],
                                results["all_players"],
                                results["mode"],
                                user["theme"]
                            )
                            
                            # تحديث نقاط اللاعبين
                            for uid, data in game.scores.items():
                                if uid in users:
                                    users[uid]["points"] += data["points"]
                        else:
                            # السؤال التالي
                            q_data = result["next_question"]
                            success_msg = f"✅ إجابة صحيحة يا {username}!\n+{result['points']} نقطة\n\n"
                            reply = ui.game_question(
                                q_data["game"],
                                q_data["question"],
                                q_data["round"],
                                q_data["total_rounds"],
                                q_data["mode"],
                                user["theme"]
                            )
                    else:
                        reply = TextMessage(text=result["message"])
            
            else:
                # رسالة افتراضية
                reply = ui.home_screen(username, user["points"], user["theme"])
            
            # إرسال الرد
            line_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[reply]
                )
            )
    
    except Exception as e:
        logger.error(f"❌ خطأ: {e}", exc_info=True)

# ============================================================================
# Flask Routes
# ============================================================================

@app.route("/callback", methods=['POST'])
def callback():
    """LINE Webhook"""
    signature = request.headers.get('X-Line-Signature', '')
    body = request.get_data(as_text=True)
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        logger.error("❌ توقيع خاطئ")
        abort(400)
    except Exception as e:
        logger.error(f"❌ خطأ: {e}")
        abort(500)
    
    return 'OK'

@app.route("/", methods=['GET'])
def home():
    """الصفحة الرئيسية"""
    uptime = datetime.now() - stats["start_time"]
    hours = uptime.total_seconds() / 3600
    
    return f"""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>🎮 Bot Mesh v6.1</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{
                font-family: 'Segoe UI', Arial, sans-serif;
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
                padding: 50px;
                max-width: 800px;
                text-align: center;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            }}
            h1 {{ font-size: 3.5em; margin-bottom: 20px; }}
            .version {{ font-size: 1.2em; opacity: 0.9; margin-bottom: 40px; }}
            .status {{
                background: rgba(72, 187, 120, 0.2);
                padding: 25px;
                border-radius: 20px;
                font-size: 1.3em;
                margin: 30px 0;
            }}
            .stats {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                gap: 20px;
                margin: 40px 0;
            }}
            .stat {{
                background: rgba(255, 255, 255, 0.15);
                padding: 25px;
                border-radius: 20px;
            }}
            .stat-value {{ font-size: 2.5em; font-weight: bold; margin: 15px 0; }}
            .stat-label {{ font-size: 1em; opacity: 0.8; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎮 Bot Mesh</h1>
            <div class="version">v6.1 - محدث ومحسن</div>
            
            <div class="status">✅ البوت يعمل بكفاءة عالية</div>
            
            <div class="stats">
                <div class="stat">
                    <div class="stat-value">{stats['total_users']}</div>
                    <div class="stat-label">👥 المستخدمون</div>
                </div>
                <div class="stat">
                    <div class="stat-value">{len(active_games)}</div>
                    <div class="stat-label">🎮 ألعاب نشطة</div>
                </div>
                <div class="stat">
                    <div class="stat-value">{stats['total_games']}</div>
                    <div class="stat-label">🏆 ألعاب منتهية</div>
                </div>
                <div class="stat">
                    <div class="stat-value">{hours:.1f}h</div>
                    <div class="stat-label">⏱️ وقت التشغيل</div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

@app.route("/health", methods=['GET'])
def health():
    """Health Check"""
    return {
        "status": "healthy",
        "version": "6.1",
        "uptime": (datetime.now() - stats["start_time"]).total_seconds(),
        "users": stats["total_users"],
        "active_games": len(active_games),
        "total_games": stats["total_games"]
    }, 200

# ============================================================================
# تشغيل التطبيق
# ============================================================================

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    
    logger.info("=" * 60)
    logger.info("🎮 Bot Mesh v6.1 - محدث")
    logger.info(f"📦 {len(GAMES)} ألعاب متاحة")
    logger.info("🎨 9 ثيمات جميلة")
    logger.info("👥 يدعم اللعب الفردي والمجموعة")
    logger.info(f"🌐 Port {port}")
    logger.info("=" * 60)
    
    app.run(host="0.0.0.0", port=port, debug=False)
