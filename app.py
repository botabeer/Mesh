# app.py (محسّن ومُعقّم)
import os
import sys
import logging
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Optional, Dict, Any, List

from flask import Flask, request, abort, jsonify
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi,
    ReplyMessageRequest, TextMessage, FlexMessage, FlexContainer
)
from linebot.v3.messaging.exceptions import ApiException
from linebot.v3.webhooks import MessageEvent, TextMessageContent

from config import Config
from database import Database
from ui_builder import UIBuilder
from game_manager import GameManager

app = Flask(__name__)

# إعداد Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("botmesh")

# التحقق من الإعدادات (فشل قاطع لو الإعدادات ناقصة)
try:
    Config.validate()
    logger.info("تم التحقق من الإعدادات بنجاح")
except Exception as e:
    logger.error(f"خطأ في الإعدادات: {e}")
    sys.exit(1)

# إعداد LINE SDK
configuration = Configuration(access_token=Config.LINE_ACCESS_TOKEN)
handler = WebhookHandler(Config.LINE_SECRET)

# إعداد المكونات
db = Database(Config.DATABASE_PATH)
ui = UIBuilder()
game_mgr = GameManager(db)

# التخزين المؤقت والحد من الوتيرة
user_sessions: Dict[str, Any] = {}
pending_registrations: Dict[str, datetime] = {}  # اخزن متى بدأ التسجيل لسياسة انتهاء التأكيد
user_rate_limit = defaultdict(list)  # user_id -> list[datetime]
user_cache: Dict[str, dict] = {}      # cache صغير للمستخدمين {user_id: {"data":..., "_cached_at": ...}}

# ----------------- Utilities -----------------

def is_rate_limited(user_id: str) -> bool:
    """فحص معدل الرسائل (sliding window)."""
    now = datetime.utcnow()
    window = timedelta(seconds=Config.RATE_LIMIT_WINDOW)
    timestamps = [t for t in user_rate_limit[user_id] if now - t < window]
    user_rate_limit[user_id] = timestamps

    if len(timestamps) >= Config.RATE_LIMIT_MESSAGES:
        logger.warning(f"تجاوز معدل الرسائل: {user_id}")
        return True

    user_rate_limit[user_id].append(now)
    return False


# ----------------- Flex sanitizer -----------------
# تبسيط: نزيل الخصائص الشائعة التي قد تسبّب خطأ من LINE (مثل backgroundColor في أماكن غير مسموح بها، borderWidth كنص "2px"، paddingAll بصيغة "20px")
# هدفنا إزالة الخصائص الشائعة غير المتوافقة مع Flex spec المستخدمة.
ALLOWED_PROPS_BY_TYPE = {
    "bubble": {"type", "size", "body", "header", "footer", "styles", "hero"},
    "box": {"type", "layout", "contents", "spacing", "margin", "flex", "action", "paddingAll", "paddingTop", "paddingBottom", "paddingStart", "paddingEnd", "cornerRadius"},
    "text": {"type", "text", "size", "weight", "align", "gravity", "wrap", "maxLines", "action", "color"},
    "button": {"type", "action", "style", "height", "margin"},
    "image": {"type", "url", "size", "aspectMode", "aspectRatio", "action"},
    "separator": {"type", "margin"},
    "icon": {"type", "url"}
}
GLOBAL_ALLOWED = {"type", "altText", "contents", "body", "header", "footer", "action"}

def _sanitize_value(v):
    """تنظيف قيم بسيطة مثل حذف 'px' من الأرقام إن لزم أو تركها كما هي."""
    if isinstance(v, str) and v.endswith("px"):
        # Line Flex عادة يقبل كلمات مثل 'md','lg' أو أرقام بدون px — من الأفضل إزالة px
        try:
            return v[:-2]
        except Exception:
            return v
    return v

def sanitize_flex(obj: Any) -> Any:
    """يمر عبر dict/list ويزيل خصائص غير مسموحة بناءً على نوع العنصر."""
    if isinstance(obj, list):
        return [sanitize_flex(v) for v in obj]
    if not isinstance(obj, dict):
        return obj

    obj_type = obj.get("type")
    allowed = set(GLOBAL_ALLOWED)
    if obj_type and obj_type in ALLOWED_PROPS_BY_TYPE:
        allowed |= ALLOWED_PROPS_BY_TYPE[obj_type]
    # بعض الخصائص العامة نتركها
    allowed |= {"text", "url", "label", "size", "weight", "action", "margin", "spacing", "backgroundColor", "color", "paddingAll", "cornerRadius"}

    sanitized = {}
    for k, v in obj.items():
        if k not in allowed:
            # تجاهل خاصية غير مسموح بها
            logger.debug("sanitize_flex: إزالة الخاصية غير المدعومة %s من عنصر %s", k, obj_type)
            continue

        # تنظيف قيم نصية معروفة
        if isinstance(v, (dict, list)):
            sanitized[k] = sanitize_flex(v)
        else:
            sanitized[k] = _sanitize_value(v)
    return sanitized


# ----------------- إرسال آمن مع تنظيف Flex -----------------
def safe_reply(line_api: MessagingApi, reply_token: str, messages: List[Any]):
    """إرسال الرد بشكل آمن مع محاولة تنظيف رسائل Flex إذا كانت عبارة عن dict."""
    try:
        if not messages:
            return

        clean_messages = []
        for m in messages:
            # إذا كانت رسالة مرّت كـ dict (قوالب Flex المبنية يدوياً)، نعمل sanitize ثم نحوّل إلى FlexMessage
            if isinstance(m, dict):
                try:
                    cleaned = sanitize_flex(m)
                    flex = FlexMessage(alt_text=cleaned.get("altText", "رسالة"), contents=FlexContainer.from_dict(cleaned.get("contents", cleaned)))
                    # إذا لم يكن هناك contents واضح، نحستخدم cleaned كـ bubble
                    clean_messages.append(flex)
                    continue
                except Exception as e:
                    logger.exception("فشل تحويل dict -> FlexMessage بعد التنظيف: %s", e)
                    # أضف كـ نص احتياطي
                    clean_messages.append(TextMessage(text="حدث خطأ في تكوين الرسالة الغنية."))
                    continue

            # إذا كانت رسالة من نوع FlexMessage أو TextMessage (من SDK)، أرسلها كما هي
            if isinstance(m, FlexMessage) or hasattr(m, "alt_text") or hasattr(m, "contents"):
                # لا تعديل، SDK من المفترض أنه جاهز
                clean_messages.append(m)
            else:
                # افتراض: رسالة نصية عادية أو object قابل للتحويل إلى نص
                try:
                    if isinstance(m, TextMessage):
                        clean_messages.append(m)
                    else:
                        clean_messages.append(TextMessage(text=str(m)))
                except Exception:
                    clean_messages.append(TextMessage(text="رد غير متوقع"))
        # إرسال واحد
        line_api.reply_message(ReplyMessageRequest(reply_token=reply_token, messages=clean_messages))

    except ApiException as e:
        # حاول استخراج جسم الخطأ وطباعته
        try:
            body = getattr(e, "body", None)
            status = getattr(e, "status", None)
            logger.error("ApiException (status=%s) body=%s", status, body)
        except Exception:
            logger.exception("خطأ أثناء معالجة ApiException")
        logger.exception("فشل إرسال الرسالة عبر LINE API")
    except Exception as e:
        logger.exception("خطأ غير متوقع في safe_reply: %s", e)


# ----------------- معلومات المستخدم -----------------
def get_user_profile(line_api: MessagingApi, user_id: str, src_type: str) -> Optional[dict]:
    """
    جلب بيانات المستخدم مع كاش محلي صغير (5 دقائق).
    نحفظ في الكاش نسخة مبسطة وليس كائن DB الأصلي لتجنب تعديل الكائن DB مباشرة.
    """
    if not user_id:
        return None

    # تحقق الكاش
    cached = user_cache.get(user_id)
    if cached:
        cached_at = cached.get("_cached_at")
        if cached_at and datetime.utcnow() - cached_at < timedelta(minutes=5):
            return cached.get("data")

    # جلب من قاعدة البيانات
    try:
        user = db.get_user(user_id)
    except Exception:
        logger.exception("خطأ في جلب المستخدم من DB")
        user = None

    # إذا غير موجود، نحاول إنشاءه
    if not user:
        name = "مستخدم"
        if src_type == "user":
            try:
                profile = line_api.get_profile(user_id)
                if profile and getattr(profile, "display_name", None):
                    name = profile.display_name or "مستخدم"
            except Exception as e:
                logger.warning("تعذر جلب الملف الشخصي عبر LINE: %s", e)
        try:
            db.create_user(user_id, name[:100])
            user = db.get_user(user_id)
        except Exception:
            logger.exception("فشل إنشاء مستخدم في DB")
            user = {"id": user_id, "name": name, "points": 0, "is_registered": 0, "theme": "فاتح"}

    # ضع نسخة مبسطة في الكاش
    if user:
        user_cache[user_id] = {"data": user, "_cached_at": datetime.utcnow()}
    return user


# ----------------- Routes -----------------
@app.route("/", methods=["GET"])
def home():
    """الصفحة الرئيسية (واجهة بسيطة للمراقبة)"""
    stats = {}
    try:
        stats = db.get_stats() or {}
    except Exception:
        logger.exception("تعذر جلب الإحصائيات")

    active = 0
    try:
        active = game_mgr.get_active_count()
    except Exception:
        logger.exception("تعذر جلب عدد الألعاب النشطة")

    try:
        db_size = db.get_database_size() / 1024 / 1024
    except Exception:
        db_size = 0.0

    return f"""<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{Config.BOT_NAME}</title>
<style>
/* ... CSS كما في الأصل (اختصار للحجم) ... */
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;margin:0;padding:0}}
.container{{max-width:800px;width:100%;margin:40px auto;background:#fff;padding:32px;border-radius:16px;box-shadow:0 8px 30px rgba(0,0,0,.1)}}
h1{{color:#333;text-align:center}}
.stat{{padding:16px;border-radius:12px;background:#fafafa;margin:12px 0}}
.footer{{text-align:center;color:#888;margin-top:20px}}
</style>
</head>
<body>
<div class="container">
<h1>{Config.BOT_NAME}</h1>
<div style="text-align:center;color:#666">v{Config.VERSION}</div>
<div class="stat">الألعاب النشطة: <strong>{active}</strong></div>
<div class="stat">المستخدمين: <strong>{stats.get('total_users', 0)}</strong></div>
<div class="stat">المسجلين: <strong>{stats.get('registered_users', 0)}</strong></div>
<div class="stat">النشطون اليوم: <strong>{stats.get('active_today', 0)}</strong></div>
<div class="stat">حجم قاعدة البيانات: <strong>{db_size:.2f} MB</strong></div>
<div class="footer">{Config.RIGHTS}</div>
</div>
</body>
</html>"""


@app.route("/health", methods=["GET"])
def health():
    """فحص صحة التطبيق"""
    return jsonify({
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat(),
        "active_games": game_mgr.get_active_count(),
        "version": Config.VERSION
    }), 200


@app.route("/callback", methods=["POST"])
def callback():
    """معالجة Webhook من LINE"""
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        logger.warning("توقيع غير صالح")
        abort(400)
    except Exception:
        logger.exception("خطأ في معالجة Webhook")
        # لا نفشل بالـ 500 لأن LINE يحتاج 200 عادة، لكن هنا يمكننا إرجاع 200 مع تسجيل الخطأ
    return "OK", 200


# ----------------- Message handling -----------------
@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    """معالجة الرسائل النصية"""
    try:
        user_id = getattr(event.source, "user_id", None)
        if not user_id:
            logger.warning("حدث بدون user_id")
            return

        text = (event.message.text or "").strip()
        if not text or len(text) > 1000:
            # تجاهل رسائل فارغة أو طويلة للغاية
            return

        if is_rate_limited(user_id):
            # يمكن إرسال رد بسيط إن أردت
            logger.info("Rate limited %s", user_id)
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
                safe_reply(line_api, event.reply_token, [
                    TextMessage(text="خطأ فني: تعذر جلب بيانات المستخدم.")
                ])
                return

            # استخراج القيم الأساسية
            username = user.get("name", "مستخدم")
            points = int(user.get("points", 0) or 0)
            is_reg = bool(user.get("is_registered", 0))
            theme = user.get("theme", "فاتح")

            # معالجة التسجيل المؤقت (نضيف صلاحية 3 دقائق مثلاً)
            if user_id in pending_registrations:
                started = pending_registrations[user_id]
                if isinstance(started, datetime) and datetime.utcnow() - started > timedelta(minutes=3):
                    # انتهاء صلاحية الطلب
                    pending_registrations.pop(user_id, None)

                elif 0 < len(text) <= 100:
                    try:
                        db.update_user(user_id, name=text, is_registered=1)
                        # إلغاء الكاش والطلب
                        user_cache.pop(user_id, None)
                        pending_registrations.pop(user_id, None)
                        msg = ui.registration_success(text, points, theme)
                    except Exception:
                        logger.exception("فشل تحديث المستخدم للتسجيل")
                        msg = TextMessage(text="حدث خطأ أثناء التسجيل.")
                    safe_reply(line_api, event.reply_token, [msg])
                    return
                else:
                    safe_reply(line_api, event.reply_token, [TextMessage(text="الاسم غير صالح (1-100 حرف)")])
                    return

            norm = Config.normalize(text)

            # الأوامر الأساسية
            if norm in ["بداية", "start", "home"]:
                msg = ui.home_screen(username, points, is_reg, theme)
                safe_reply(line_api, event.reply_token, [msg])
                return

            if norm in ["العاب", "games", "الالعاب"]:
                # games_menu قد يرِجع FlexMessage أو dict
                msg = ui.games_menu(theme)
                safe_reply(line_api, event.reply_token, [msg])
                return

            if norm in ["مساعدة", "help"]:
                msg = ui.help_screen(theme)
                safe_reply(line_api, event.reply_token, [msg])
                return

            if norm == "نقاطي":
                stats = db.get_user_stats(user_id) if is_reg else None
                msg = ui.my_points(username, points, stats, theme)
                safe_reply(line_api, event.reply_token, [msg])
                return

            if norm == "صدارة":
                top = db.get_leaderboard(20)
                msg = ui.leaderboard(top, theme)
                safe_reply(line_api, event.reply_token, [msg])
                return

            if norm == "انضم":
                if is_reg:
                    msg = TextMessage(text=f"أنت مسجل بالفعل\nالاسم: {username}\nالنقاط: {points}")
                else:
                    pending_registrations[user_id] = datetime.utcnow()
                    msg = ui.registration_prompt(theme)
                safe_reply(line_api, event.reply_token, [msg])
                return

            if norm == "انسحب":
                if is_reg:
                    try:
                        db.update_user(user_id, is_registered=0)
                        user_cache.pop(user_id, None)
                        msg = ui.unregister_confirm(username, points, theme)
                    except Exception:
                        logger.exception("فشل في عملية الانسحاب")
                        msg = TextMessage(text="حدث خطأ أثناء الانسحاب.")
                else:
                    msg = TextMessage(text="أنت غير مسجل")
                safe_reply(line_api, event.reply_token, [msg])
                return

            if norm in ["ايقاف", "stop"]:
                stopped = game_mgr.stop_game(ctx_id)
                if stopped:
                    msg = ui.game_stopped(stopped, theme)
                    safe_reply(line_api, event.reply_token, [msg])
                return

            if text.startswith("ثيم "):
                new_theme = text.split(maxsplit=1)[1].strip()
                if Config.is_valid_theme(new_theme):
                    try:
                        db.set_user_theme(user_id, new_theme)
                        user_cache.pop(user_id, None)
                        msg = ui.home_screen(username, points, is_reg, new_theme)
                    except Exception:
                        logger.exception("فشل في تغيير الثيم")
                        msg = TextMessage(text="خطأ أثناء تغيير الثيم.")
                else:
                    msg = TextMessage(text="ثيم غير موجود\nالثيمات المتاحة:\n• فاتح\n• داكن")
                safe_reply(line_api, event.reply_token, [msg])
                return

            # تمرير الرسالة إلى مدير الألعاب
            try:
                result = game_mgr.process_message(
                    ctx_id, user_id, username, text,
                    is_reg, theme, src_type
                )
            except Exception:
                logger.exception("خطأ داخل مدير الألعاب")
                result = None

            if result:
                msgs = result.get("messages", [])
                if msgs:
                    safe_reply(line_api, event.reply_token, msgs)

                gained = int(result.get("points", 0) or 0)
                if gained > 0 and is_reg:
                    try:
                        db.add_points(user_id, gained)
                        user_cache.pop(user_id, None)
                    except Exception:
                        logger.exception("فشل إضافة نقاط للمستخدم")

    except Exception:
        logger.exception("خطأ في معالج الرسائل")


# ----------------- تشغيل التطبيق -----------------
if __name__ == "__main__":
    port = int(os.getenv("PORT", Config.DEFAULT_PORT))
    logger.info(f"بدء التطبيق على المنفذ {port}")
    # debug=False في الإنتاج؛ارسل threaded=True لتوافق بعض بيئات الاستضافة
    app.run(host="0.0.0.0", port=port, debug=False, threaded=True)
