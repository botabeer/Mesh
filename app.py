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

# ❗ تم إصلاح الشرط الخاطئ هنا فقط
if not LINE_SECRET or not LINE_TOKEN:
    logger.error("❌ LINE credentials missing!")
    exit(1)

configuration = Configuration(access_token=LINE_TOKEN)
handler = WebhookHandler(LINE_SECRET)

# ============================================================================
# قاعدة البيانات البسيطة (في الذاكرة)
# ============================================================================

users = {}  
active_games = {}  
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
    if hasattr(event.source, 'group_id'):
        return f"group_{event.source.group_id}"
    elif hasattr(event.source, 'room_id'):
        return f"room_{event.source.room_id}"
    else:
        return f"user_{event.source.user_id}"

def get_or_create_user(user_id, username):
    if user_id not in users:
        users[user_id] = {
            "name": username,
            "points": 0,
            "mode": "فردي",
            "theme": "💜",
            "last_active": datetime.now()
        }
        stats["total_users"] += 1
    
    users[user_id]["last_active"] = datetime.now()
    return users[user_id]

def cleanup_old_games():
    to_remove = []
    for room_id, game in active_games.items():
        if game.is_expired(max_minutes=30):
            to_remove.append(room_id)
    
    for room_id in to_remove:
        active_games.pop(room_id, None)
    
    if to_remove:
        logger.info(f"🧹 تم حذف {len(to_remove)}ألعاب منتهية")

def get_top_players(limit=10):
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
    try:
        stats["total_messages"] += 1
        
        user_id = event.source.user_id
        room_id = get_room_id(event)
        text = event.message.text.strip()
        
        with ApiClient(configuration) as api_client:
            line_api = MessagingApi(api_client)
            
            try:
                profile = line_api.get_profile(user_id)
                username = profile.display_name or "لاعب"
            except:
                username = "لاعب"
            
            user = get_or_create_user(user_id, username)
            
            if stats["total_messages"] % 10 == 0:
                cleanup_old_games()
            
            # ============================================================
            # الأوامر الأساسية
            # ============================================================
            
            if text in ["بداية", "البداية", "start", "@"]:
                reply = ui.home_screen(username, user["points"], user["theme"])
            
            elif text in ["مجموعة", "لعب مجموعة"]:
                user["mode"] = "مجموعة"
                reply = ui.games_menu(mode="مجموعة", theme=user["theme"])
            
            elif text in ["فردي", "لعب فردي"]:
                user["mode"] = "فردي"
                reply = ui.games_menu(mode="فردي", theme=user["theme"])
            
            elif text in ["العاب", "الألعاب", "ألعاب"]:
                reply = ui.games_menu(mode=user["mode"], theme=user["theme"])
            
            elif text in ["ثيمات", "الثيمات", "themes"]:
                reply = ui.themes_selector(current_theme=user["theme"])
            
            elif text.startswith("ثيم "):
                theme_emoji = text.replace("ثيم ", "").strip()
                if theme_emoji in ui.THEMES:
                    user["theme"] = theme_emoji
                    reply = TextMessage(text=f"✅ تم تغيير الثيم إلى {ui.THEMES[theme_emoji]['name']}")
                else:
                    reply = TextMessage(text="❌ ثيم غير موجود!")
            
            elif text in ["صدارة", "الصدارة", "leaderboard"]:
                top = get_top_players()
                reply = ui.leaderboard(top, theme=user["theme"])
            
            # ============================================================
            # بدء لعبة جديدة
            # ============================================================
            
            elif text.startswith("لعبة "):
                game_name = text.replace("لعبة ", "").strip()
                
                if game_name in GAMES:
                    game = GAMES[game_name](mode=user["mode"])
                    active_games[room_id] = game
                    stats["total_games"] += 1
                    
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
                
                if text in ["تلميح", "لمح", "hint"]:
                    reply = TextMessage(text=game.get_hint())
                
                elif text in ["اجابة", "إجابة", "جاوب", "reveal"]:
                    result = game.reveal_answer()
                    
                    if result.get("game_over"):
                        del active_games[room_id]
                        results = result["results"]
                        reply = ui.game_result(
                            results["winner_name"],
                            results["winner_points"],
                            results["all_players"],
                            results["mode"],
                            user["theme"]
                        )
                        for uid, data in game.scores.items():
                            if uid in users:
                                users[uid]["points"] += data["points"]
                    else:
                        q_data = result["next_question"]
                        reply = ui.game_question(
                            q_data["game"],
                            q_data["question"],
                            q_data["round"],
                            q_data["total_rounds"],
                            q_data["mode"],
                            user["theme"]
                        )
                
                elif text in ["ايقاف", "إيقاف", "stop", "خروج"]:
                    del active_games[room_id]
                    reply = TextMessage(text="⛔ تم إيقاف اللعبة")
                
                else:
                    result = game.check_answer(user_id, username, text)
                    
                    if not result["valid"]:
                        reply = TextMessage(text=result["message"])
                    
                    elif result["correct"]:
                        if result.get("game_over"):
                            del active_games[room_id]
                            results = result["results"]
                            reply = ui.game_result(
                                results["winner_name"],
                                results["winner_points"],
                                results["all_players"],
                                results["mode"],
                                user["theme"]
                            )
                            for uid, data in game.scores.items():
                                if uid in users:
                                    users[uid]["points"] += data["points"]
                        else:
                            q_data = result["next_question"]
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
                reply = ui.home_screen(username, user["points"], user["theme"])
            
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

    uptime = datetime.now() - stats["start_time"]
    hours = uptime.total_seconds() / 3600
    
    return f"""
    <html><body><h1>Bot Mesh v6.1 Running</h1></body></html>
    """

@app.route("/health", methods=['GET'])
def health():
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
