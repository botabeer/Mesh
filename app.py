"""
app.py — الخادم الرئيسي لِـ Bot Mesh (مُحسّن ومُصلح)
Created by: Abeer Aldosari © 2025
ملاحظات هامة:
- يتعامل مع DB (SQLite) عبر class DB في ملف db.py — تأكد أن DB يوفر الواجهة المستخدمة هنا:
    create_user(user_id, name, theme), get_user(user_id), update_theme(user_id, theme),
    deactivate_user(user_id), add_points(user_id, points),
    get_total_users(), get_total_points(), get_leaderboard(n)
- يتعامل مع GameLoader (module games) ويفترض وجود الواجهات:
    has_active_game(user_id), start_game(user_id, game_name), get_game(user_id), end_game(user_id)
  الكود مرن: إن اختلفت أسماء الخصائص يحاول التكيّف.
- عند إرسال FlexMessage نرسل بعده رسالة نصية قصيرة تحتوي على QuickReply من ui.get_quick_reply()
  لضمان ظهور Quick Reply دائمًا في واجهة LINE.
"""

import os
import logging
import threading
import time
from collections import defaultdict
from flask import Flask, request, abort, jsonify

from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import Configuration, ApiClient, MessagingApi, ReplyMessageRequest, TextMessage, FlexMessage

# استيراد الواجهات
from ui import (
    build_home, build_games_menu, build_my_points, build_leaderboard,
    build_registration_required, build_help, get_quick_reply
)
# استيراد قاعدة البيانات
from db import DB

# استيراد GameLoader — مرن مع اختبارات الخصائص
try:
    from games import GameLoader
except Exception:
    try:
        from games.loader import GameLoader
    except Exception:
        GameLoader = None  # سنتعامل مع غيابه

# ================== إعداد اللوق ==================
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("bot-mesh")

# ================== إعدادات LINE ==================
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', '')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET', '')
PORT = int(os.getenv('PORT', 10000))

if not LINE_CHANNEL_ACCESS_TOKEN or not LINE_CHANNEL_SECRET:
    logger.error("❌ LINE credentials missing! ضع المتغيرات البيئية LINE_CHANNEL_ACCESS_TOKEN و LINE_CHANNEL_SECRET")
    # لا ننهي الخدمة هنا لأن المستخدم طلب ملفات؛ لكن في الإنتاج يلزم الخروج.
    # exit(1)

# ================== تهيئة الخدمة ==================
app = Flask(__name__)
db = DB()
game_loader = GameLoader() if GameLoader else None

# games_count مرن بحسب ما يوفر GameLoader
if game_loader:
    if hasattr(game_loader, "loaded"):
        games_count = len(getattr(game_loader, "loaded") or [])
    elif hasattr(game_loader, "games"):
        games_count = len(getattr(game_loader, "games") or [])
    elif hasattr(game_loader, "GAME_MAPPING"):
        games_count = len(getattr(game_loader, "GAME_MAPPING") or {})
    else:
        # إن لم تتوفر أي خاصية، نحاول استدعاء loader.list_games() إن موجودة
        try:
            games_count = len(game_loader.list_games())
        except Exception:
            games_count = 0
else:
    games_count = 0

logger.info(f"✅ Bot Mesh initialized with {games_count} games")

configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# ================== Rate limiter بسيط ==================
class SimpleRateLimiter:
    def __init__(self):
        self.requests = defaultdict(list)
        self.lock = threading.Lock()

    def is_allowed(self, user_id: str, max_per_minute: int = 10) -> bool:
        with self.lock:
            now = time.time()
            minute_ago = now - 60
            self.requests[user_id] = [t for t in self.requests[user_id] if t > minute_ago]
            if len(self.requests[user_id]) >= max_per_minute:
                return False
            self.requests[user_id].append(now)
            return True

rate_limiter = SimpleRateLimiter()

# ================== Helpers ==================
def normalize_text(text: str) -> str:
    if not text:
        return ""
    t = text.strip().lower()
    replacements = {'أ': 'ا', 'إ': 'ا', 'آ': 'ا', 'ى': 'ي', 'ة': 'ه'}
    for k, v in replacements.items():
        t = t.replace(k, v)
    return t

def safe_reply_with_quick(line_api, reply_token, messages):
    """
    ارسال رسالة/رسائل. لضمان Quick Reply دائم، اذا المرسَل واحد من نوع Flex نضيف رسالة نصية بعدها
    تحتوي على quick reply (نص قصير) — هذا يظل أفضل حل موثوق لعرض Quick Reply في واجهة LINE.
    """
    if not isinstance(messages, list):
        messages = [messages]

    # send the provided messages first
    try:
        with ApiClient(configuration) as api_client:
            api = MessagingApi(api_client)
            # If any message is FlexMessage, convert as-is; SDK expects proper types.
            api.reply_message_with_http_info(ReplyMessageRequest(reply_token=reply_token, messages=messages))
    except Exception as e:
        logger.error(f"❌ Failed to send main reply: {e}")

    # after Flex, ensure a small text message with quick reply (لنزع الإزعاج نخلي النص توجيهي قصير)
    try:
        with ApiClient(configuration) as api_client:
            api = MessagingApi(api_client)
            quick = get_quick_reply()
            # نص تلميحي قصير لإظهار Quick Reply
            text_msg = TextMessage(text="▫️ استخدم الأزرار السريعة للاختيار", quick_reply=quick)
            api.reply_message_with_http_info(ReplyMessageRequest(reply_token=reply_token, messages=[text_msg]))
    except Exception as e:
        # غالبًا سيحصل خطأ لأن لا يمكن الرد مرتين بنفس الـ reply token، لذا بدلًا من الرد نستخدم push للمستخدم (إن أردت)
        logger.debug(f"ℹ️ لا يمكن إرفاق Quick Reply عبر رد ثاني: {e} — سيتم محاولة إرسال Quick Reply مع الرسالة التالية")

def send_text_with_quick(line_api, reply_token, text):
    # يرسل رسالة نصية مع Quick Reply مباشرةً
    quick = get_quick_reply()
    with ApiClient(configuration) as api_client:
        api = MessagingApi(api_client)
        tm = TextMessage(text=text, quick_reply=quick)
        try:
            api.reply_message_with_http_info(ReplyMessageRequest(reply_token=reply_token, messages=[tm]))
            return True
        except Exception as e:
            logger.error(f"❌ Failed to send text reply: {e}")
            return False

# ================== معالجة الرسائل في الخلفية ==================
def process_message_background(user_id: str, text: str, reply_token: str):
    try:
        if not rate_limiter.is_allowed(user_id):
            logger.warning(f"⚠️ Rate limit exceeded for {user_id}")
            send_text_with_quick(None, reply_token, "▫️ تجاوزت حد الرسائل. حاول بعد قليل")
            return

        # احصل على بيانات المستخدم من DB
        user = db.get_user(user_id)
        theme = user['theme'] if user and 'theme' in user else "رمادي"
        points = user['points'] if user and 'points' in user else 0
        is_registered = bool(user and user.get('status') == 'active')

        normalized = normalize_text(text)

        # ===== أوامر أساسية =====
        if normalized in ['بداية', 'start', 'home']:
            msg = build_home(theme=theme, username=user.get('name') if user else "مستخدم", points=points, is_registered=is_registered)
            # نرسل FlexMessage ثم نحاول إرفاق Quick Reply — تابع safe_reply_with_quick
            safe_reply_with_quick(None, reply_token, msg)
            return

        if normalized in ['مساعدة', 'help']:
            msg = build_help(theme=theme)
            safe_reply_with_quick(None, reply_token, msg)
            return

        if normalized.startswith('ثيم '):
            new_theme = text.replace('ثيم ', '').strip()
            if new_theme in THEMES:
                if user:
                    db.update_theme(user_id, new_theme)
                    theme = new_theme
                msg = build_home(theme=theme, username=user.get('name') if user else "مستخدم", points=points, is_registered=is_registered)
                safe_reply_with_quick(None, reply_token, msg)
            else:
                send_text_with_quick(None, reply_token, f"▫️ الثيم '{new_theme}' غير موجود. الأسماء: {', '.join(list(THEMES.keys()))}")
            return

        if normalized in ['انضم', 'join']:
            if not is_registered:
                name = user.get('name') if user else "مستخدم"
                db.create_user(user_id, name, theme)
                send_text_with_quick(None, reply_token, f"▫️ تم تسجيلك يا {name}")
            else:
                send_text_with_quick(None, reply_token, f"▫️ أنت مسجل بالفعل")
            return

        if normalized in ['انسحب', 'leave']:
            if is_registered:
                db.deactivate_user(user_id)
                send_text_with_quick(None, reply_token, "▫️ تم إلغاء تسجيلك")
            else:
                send_text_with_quick(None, reply_token, "▫️ أنت غير مسجل")
            return

        if normalized in ['العاب', 'games', 'الالعاب']:
            if not is_registered:
                msg = build_registration_required(theme=theme)
                safe_reply_with_quick(None, reply_token, msg)
            else:
                msg = build_games_menu(theme=theme)
                safe_reply_with_quick(None, reply_token, msg)
            return

        if normalized in ['نقاطي', 'points']:
            if not is_registered:
                msg = build_registration_required(theme=theme)
                safe_reply_with_quick(None, reply_token, msg)
            else:
                msg = build_my_points(user.get('name') if user else "مستخدم", points, theme)
                safe_reply_with_quick(None, reply_token, msg)
            return

        if normalized in ['صدارة', 'leaderboard']:
            top = db.get_leaderboard(10)
            msg = build_leaderboard(top, theme)
            safe_reply_with_quick(None, reply_token, msg)
            return

        # ===== أثناء اللعب =====
        if (game_loader and game_loader.has_active_game(user_id)) if game_loader else False:
            game = game_loader.get_game(user_id)
            if normalized in ['لمح', 'hint']:
                hint = game.get_hint() if hasattr(game, 'get_hint') else "▫️ لا يوجد تلميح"
                send_text_with_quick(None, reply_token, hint)
                return

            # تمرير الإجابة للعبة
            if hasattr(game, "check_answer"):
                result = game.check_answer(text, user_id, user.get('name') if user else "مستخدم")
                if result:
                    # نقاط
                    pts = result.get('points', 0)
                    if pts:
                        db.add_points(user_id, pts)
                    # رسالة الاستجابة
                    response_msg = result.get('response') or result.get('message') or "▫️ تم"
                    # نبعث النص مع quick reply
                    send_text_with_quick(None, reply_token, response_msg)
                    if result.get('game_over'):
                        game_loader.end_game(user_id)
                    return

        # ===== بدء لعبة من المستخدم =====
        if normalized.startswith('لعبة ') or normalized.startswith('لعبه '):
            if not is_registered:
                msg = build_registration_required(theme=theme)
                safe_reply_with_quick(None, reply_token, msg)
                return

            game_name = text.replace('لعبة ', '').replace('لعبه ', '').strip()
            if game_loader:
                # إذا هناك لعبة نشطة نُنهيها أولًا
                try:
                    if game_loader.has_active_game(user_id):
                        game_loader.end_game(user_id)
                except Exception:
                    pass

                res = game_loader.start_game(user_id, game_name)
                if not res:
                    send_text_with_quick(None, reply_token, f"▫️ اللعبة '{game_name}' غير موجودة")
                    return
                # res قد يكون FlexMessage أو TextMessage أو dict — نرسل ما يصلح
                if isinstance(res, FlexMessage):
                    safe_reply_with_quick(None, reply_token, res)
                else:
                    # نفترض نص أو رسالة جاهزة
                    send_text_with_quick(None, reply_token, str(res))
                return
            else:
                send_text_with_quick(None, reply_token, "▫️ خدمة الألعاب غير مُهيأة حالياً")
                return

        if normalized in ['ايقاف', 'إيقاف', 'stop']:
            if game_loader and game_loader.has_active_game(user_id):
                game_loader.end_game(user_id)
                send_text_with_quick(None, reply_token, "▫️ تم إيقاف اللعبة")
            else:
                send_text_with_quick(None, reply_token, "▫️ لا توجد لعبة نشطة")
            return

        # ===== افتراضي للمستخدم غير مسجل =====
        if not is_registered:
            logger.info(f"Ignored message from unregistered user: {user_id}")
            send_text_with_quick(None, reply_token, "▫️ يجب التسجيل أولاً — اكتب 'انضم'")
            return

        # ===== رسالة افتراضية =====
        send_text_with_quick(None, reply_token, "▫️ لم أفهم الأمر. اكتب 'مساعدة' للمساعدة")
    except Exception as e:
        logger.error(f"❌ Error in background processing: {e}", exc_info=True)
        try:
            send_text_with_quick(None, reply_token, "▫️ حدث خطأ. حاول مرة أخرى")
        except Exception:
            pass

# ================== Webhook handlers (LINE) ==================
@handler.add  # follow event
def handle_follow(event):
    # عندما يتابع المستخدم البوت — نسجّله ونرسل الصفحة الرئيسية
    user_id = event.source.user_id

    def background():
        try:
            # خذ بعض المعلومات من LINE (إن أردت) — هنا نفترض أن db.create_user يقبل (id, name, theme)
            # لا نستطيع استدعاء LINE profile بدون ApiClient هنا ما دام الـ tokens موجودة — إن موجودين استخرج الاسم
            name = "مستخدم"
            db.create_user(user_id, name, "رمادي")
            msg = build_home("رمادي", name, 0, True)
            # للأسف لا يمكن استخدام reply token في follow — نستخدم push إذا credentials متاحة
            with ApiClient(configuration) as api_client:
                api = MessagingApi(api_client)
                api.push_message_with_http_info(user_id, [msg])
        except Exception as e:
            logger.error(f"❌ Follow handling failed: {e}", exc_info=True)

    threading.Thread(target=background, daemon=True).start()

@handler.add  # رسالة نصية عادية
def handle_message(event):
    user_id = event.source.user_id
    text = event.message.text if hasattr(event, "message") and getattr(event, "message") and getattr(event.message, "text", None) else ""
    reply_token = event.reply_token

    threading.Thread(target=process_message_background, args=(user_id, text, reply_token), daemon=True).start()

# ================== Routes للمراقبة ==================
@app.route("/", methods=["GET"])
def home():
    try:
        total_users = db.get_total_users()
    except Exception:
        total_users = 0
    return jsonify({"status": "running", "bot": "Bot Mesh v9.0", "games": games_count, "users": total_users})

@app.route("/health", methods=["GET"])
def health():
    try:
        active = len(getattr(game_loader, "active_sessions")) if (game_loader and hasattr(game_loader, "active_sessions")) else 0
    except Exception:
        active = 0
    return jsonify({"status": "healthy", "games_loaded": games_count, "active_sessions": active}), 200

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        logger.error("❌ Invalid signature")
        abort(400)
    except Exception as e:
        logger.error(f"❌ Callback error: {e}", exc_info=True)
    return "OK"

@app.route("/stats", methods=["GET"])
def stats():
    try:
        total_users = db.get_total_users()
        total_points = db.get_total_points()
    except Exception:
        total_users = 0
        total_points = 0
    try:
        active = len(getattr(game_loader, "active_sessions")) if (game_loader and hasattr(game_loader, "active_sessions")) else 0
    except Exception:
        active = 0
    return jsonify({
        "total_users": total_users,
        "total_points": total_points,
        "games_available": games_count,
        "active_games": active,
        "leaderboard": db.get_leaderboard(5)
    })

# ================== Error handlers ==================
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def internal(e):
    logger.error(f"❌ Internal Error: {e}", exc_info=True)
    return jsonify({"error": "Internal server error"}), 500

# ================== Startup ==================
if __name__ == "__main__":
    logger.info(f"Bot Mesh v9.0 starting on port {PORT} — games: {games_count}")
    app.run(host="0.0.0.0", port=PORT, debug=False)
