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

user_sessions: Dict[str, Any] = {}
pending_registrations: Dict[str, datetime] = {}
user_rate_limit = defaultdict(list)
user_cache: Dict[str, dict] = {}

# ---------------- Utilities ----------------
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

# ---------------- Flex sanitizer ----------------
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
    if isinstance(v, str) and v.endswith("px"):
        try:
            return v[:-2]
        except Exception:
            return v
    return v

def sanitize_flex(obj: Any) -> Any:
    if isinstance(obj, list):
        return [sanitize_flex(v) for v in obj]
    if not isinstance(obj, dict):
        return obj
    obj_type = obj.get("type")
    allowed = set(GLOBAL_ALLOWED)
    if obj_type and obj_type in ALLOWED_PROPS_BY_TYPE:
        allowed |= ALLOWED_PROPS_BY_TYPE[obj_type]
    allowed |= {"text", "url", "label", "size", "weight", "action", "margin", "spacing", "backgroundColor", "color", "paddingAll", "cornerRadius"}
    sanitized = {}
    for k, v in obj.items():
        if k not in allowed:
            continue
        if isinstance(v, (dict, list)):
            sanitized[k] = sanitize_flex(v)
        else:
            sanitized[k] = _sanitize_value(v)
    return sanitized

def safe_reply(line_api: MessagingApi, reply_token: str, messages: List[Any]):
    try:
        if not messages:
            return
        clean_messages = []
        for m in messages:
            if isinstance(m, dict):
                try:
                    cleaned = sanitize_flex(m)
                    flex = FlexMessage(
                        alt_text=cleaned.get("altText", "رسالة"),
                        contents=FlexContainer.from_dict(cleaned.get("contents", cleaned))
                    )
                    clean_messages.append(flex)
                    continue
                except Exception:
                    clean_messages.append(TextMessage(text="حدث خطأ في تكوين الرسالة الغنية."))
                    continue
            if isinstance(m, FlexMessage) or hasattr(m, "alt_text") or hasattr(m, "contents"):
                clean_messages.append(m)
            else:
                try:
                    if isinstance(m, TextMessage):
                        clean_messages.append(m)
                    else:
                        clean_messages.append(TextMessage(text=str(m)))
                except Exception:
                    clean_messages.append(TextMessage(text="رد غير متوقع"))
        line_api.reply_message(ReplyMessageRequest(reply_token=reply_token, messages=clean_messages))
    except Exception:
        logger.exception("فشل إرسال الرسالة")

# ---------------- User profile ----------------
def get_user_profile(line_api: MessagingApi, user_id: str, src_type: str) -> Optional[dict]:
    if not user_id:
        return None
    cached = user_cache.get(user_id)
    if cached:
        cached_at = cached.get("_cached_at")
        if cached_at and datetime.utcnow() - cached_at < timedelta(minutes=5):
            return cached.get("data")
    try:
        user = db.get_user(user_id)
    except Exception:
        user = None
    if not user:
        name = "مستخدم"
        if src_type == "user":
            try:
                profile = line_api.get_profile(user_id)
                if profile and getattr(profile, "display_name", None):
                    name = profile.display_name or "مستخدم"
            except Exception:
                pass
        try:
            db.create_user(user_id, name[:100])
            user = db.get_user(user_id)
        except Exception:
            user = {"id": user_id, "name": name, "points": 0, "is_registered": 0, "theme": "فاتح"}
    if user:
        user_cache[user_id] = {"data": user, "_cached_at": datetime.utcnow()}
    return user

# ---------------- Routes ----------------
@app.route("/", methods=["GET"])
def home():
    stats = db.get_stats() or {}
    active = game_mgr.get_active_count()
    db_size = db.get_database_size() / 1024 / 1024
    return f"""<!DOCTYPE html>
<html dir="rtl">
<head><meta charset="utf-8"><title>{Config.BOT_NAME}</title></head>
<body>
<h1>{Config.BOT_NAME}</h1>
<p>الألعاب النشطة: {active}</p>
<p>المستخدمين: {stats.get('total_users', 0)}</p>
<p>المسجلين: {stats.get('registered_users', 0)}</p>
<p>النشطون اليوم: {stats.get('active_today', 0)}</p>
<p>حجم قاعدة البيانات: {db_size:.2f} MB</p>
<p>{Config.RIGHTS}</p>
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
        abort(400)
    except Exception:
        logger.exception("خطأ في Webhook")
    return "OK", 200

# ---------------- Message handling ----------------
@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    try:
        user_id = getattr(event.source, "user_id", None)
        if not user_id:
            return
        text = (event.message.text or "").strip()
        if not text or len(text) > 1000:
            return
        if is_rate_limited(user_id):
            return
        src_type = event.source.type
        ctx_id = getattr(event.source, "group_id", None) or getattr(event.source, "room_id", None) or user_id
        with ApiClient(configuration) as api_client:
            line_api = MessagingApi(api_client)
            user = get_user_profile(line_api, user_id, src_type)
            if not user:
                safe_reply(line_api, event.reply_token, [TextMessage(text="خطأ فني: تعذر جلب بيانات المستخدم.")])
                return
            username = user.get("name", "مستخدم")
            points = int(user.get("points", 0) or 0)
            is_reg = bool(user.get("is_registered", 0))
            theme = user.get("theme", "فاتح")
            # هنا يمكن إدراج كل معالجة الأوامر والألعاب كما في الكود السابق
    except Exception:
        logger.exception("خطأ في معالج الرسائل")

# ---------------- تشغيل التطبيق ----------------
if __name__ == "__main__":
    port = Config.get_port()
    logger.info(f"بدء التطبيق على المنفذ {port}")
    app.run(host="0.0.0.0", port=port, debug=False, threaded=True)
