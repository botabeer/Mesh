"""
Bot Mesh - Ultimate Edition
Created by: Abeer Aldosari © 2025

نسخة كاملة جداً — جاهزة للنشر
تشمل:
- الثيمات
- الألعاب
- النوافذ الرئيسية
- النظام الذكي
- الثابت
- المتغيرات البيئية
- التوافق الكامل مع LINE
"""

import os
import logging
import importlib
import traceback
from datetime import datetime, timedelta
from flask import Flask, request, abort, jsonify

# LINE SDK v3
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    ApiClient, MessagingApi, ReplyMessageRequest, PushMessageRequest,
    FlexMessage, TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent, FollowEvent,
    TextMessageContent
)


# -------------------------------
# المتغيرات البيئية
# -------------------------------
CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
CHANNEL_ACCESS = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

GEMINI_KEYS = [
    os.getenv("GEMINI_API_KEY_1"),
    os.getenv("GEMINI_API_KEY_2"),
    os.getenv("GEMINI_API_KEY_3")
]

if not CHANNEL_SECRET or not CHANNEL_ACCESS:
    raise Exception("❌ المتغيرات البيئية مفقودة — يجب إضافة LINE_CHANNEL_SECRET و LINE_CHANNEL_ACCESS_TOKEN")

# -------------------------------
# بداية التطبيق
# -------------------------------

app = Flask(__name__)
handler = WebhookHandler(CHANNEL_SECRET)

# عميل LINE API
configuration = ApiClient(configuration={"access_token": CHANNEL_ACCESS})
line_bot = MessagingApi(api_client=configuration)


# -------------------------------
# قاعدة بيانات بسيطة للمستخدمين واللعب
# -------------------------------

USERS = {}  # userId → {"name": str, "points": int, "theme": str, "last_active": datetime}
GAMES = {}  # userId → instance of the running game


# -------------------------------
# الثيمات
# -------------------------------

THEMES = ["💜", "💚", "🤍", "🖤", "💙", "🩶", "🩷", "🧡", "🤎"]


# -------------------------------
# الأدوات المساعدة
# -------------------------------

def get_username_from_profile(profile):
    name = profile.display_name
    if not name.strip():
        return "مستخدم"
    return name.strip()


def register_user(user_id, name):
    if user_id not in USERS:
        USERS[user_id] = {
            "name": name,
            "points": 0,
            "theme": "💜",
            "last_active": datetime.now()
        }


def update_activity(user_id):
    if user_id in USERS:
        USERS[user_id]["last_active"] = datetime.now()


def cleanup_old_users():
    now = datetime.now()
    to_delete = []
    for uid, data in USERS.items():
        if now - data["last_active"] > timedelta(days=7):
            to_delete.append(uid)
    for uid in to_delete:
        del USERS[uid]


def load_game_class(name):
    try:
        module = importlib.import_module(f"games.{name}")
        return getattr(module, name)
    except Exception:
        return None


# -------------------------------
# توليد Flex Messages احترافية
# -------------------------------

def fixed_footer():
    return {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "paddingAll": "10px",
        "contents": [
            {
                "type": "button",
                "action": {"type": "message", "label": "بداية", "text": "بداية"},
                "style": "secondary"
            },
            {
                "type": "button",
                "action": {"type": "message", "label": "مساعدة", "text": "مساعدة"},
                "style": "secondary"
            },
            {
                "type": "separator"
            },
            {
                "type": "text",
                "text": "الألعاب:",
                "weight": "bold",
                "size": "sm"
            },
            {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                    # صفوف الألعاب
                    {"type": "box", "layout": "horizontal", "spacing": "sm",
                     "contents": game_buttons(["ذكاء", "رياضيات", "لون", "أسرع"])},
                    {"type": "box", "layout": "horizontal", "spacing": "sm",
                     "contents": game_buttons(["ترتيب", "أغنية", "كلمة", "سلسلة"])},
                    {"type": "box", "layout": "horizontal", "spacing": "sm",
                     "contents": game_buttons(["خمن", "توافق", "ضد", "تكوين"])},
                ]
            },
            {
                "type": "button",
                "action": {"type": "message", "label": "إيقاف", "text": "إيقاف"},
                "color": "#FF4444",
                "style": "primary"
            }
        ]
    }


def game_buttons(list_names):
    return [{
        "type": "button",
        "style": "secondary",
        "action": {"type": "message", "label": name, "text": name}
    } for name in list_names]


# -------------------------------
# نافذة البداية
# -------------------------------

def build_home(user):
    theme = user["theme"]
    name = user["name"]
    points = user["points"]

    return {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
            "paddingAll": "12px",
            "contents": [
                {"type": "text", "text": f"🤖 Bot Mesh ({theme})", "weight": "bold", "size": "lg"},
                {"type": "text", "text": f"مرحباً: {name}"},
                {"type": "text", "text": f"نقاطك: {points}"},
                {"type": "separator"},
                {"type": "text", "text": "اختر ثيمك:"},
                {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                        {"type": "box", "layout": "horizontal", "spacing": "sm",
                         "contents": theme_buttons(THEMES[0:3])},
                        {"type": "box", "layout": "horizontal", "spacing": "sm",
                         "contents": theme_buttons(THEMES[3:6])},
                        {"type": "box", "layout": "horizontal", "spacing": "sm",
                         "contents": theme_buttons(THEMES[6:9])},
                    ]
                }
            ]
        },
        "footer": fixed_footer()
    }


def theme_buttons(list_emojis):
    return [{
        "type": "button",
        "action": {"type": "message", "label": e, "text": f"ثيم {e}"},
        "style": "secondary"
    } for e in list_emojis]


# -------------------------------
# نافذة المساعدة
# -------------------------------

def build_help():
    return {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
            "paddingAll": "12px",
            "contents": [
                {"type": "text", "text": "🤖 Bot Mesh – مساعدة", "weight": "bold", "size": "lg"},
                {"type": "text", "text": "🎮 الألعاب المتاحة:", "weight": "bold"},
                {"type": "text", "text": "ذكاء – رياضيات – لون – أسرع – ترتيب – أغنية"},
                {"type": "text", "text": "كلمة – سلسلة – خمن – توافق – ضد – تكوين"},
                {"type": "separator"},
                {"type": "text", "text": "أوامر اللعب:"},
                {"type": "text", "text": "▫️ لمح — تلميح\n▫️ جاوب — إرسال إجابة\n▫️ إيقاف — إنهاء اللعبة"},
            ]
        },
        "footer": fixed_footer()
    }


# -------------------------------
# نافذة النقاط
# -------------------------------

def build_my_points(user):
    return {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
            "contents": [
                {"type": "text", "text": "📊 نقاطي", "weight": "bold", "size": "lg"},
                {"type": "text", "text": f"الاسم: {user['name']}"},
                {"type": "text", "text": f"النقاط: {user['points']}"},
                {"type": "separator"},
                {"type": "text", "text": "🔥 ملاحظة: سيتم حذفك تلقائياً بعد 7 أيام من عدم النشاط"}
            ]
        },
        "footer": fixed_footer()
    }


# -------------------------------
# نافذة الصدارة
# -------------------------------

def build_leaderboard():
    sorted_users = sorted(USERS.items(), key=lambda x: x[1]['points'], reverse=True)
    top = "\n".join([f"{i+1}. {u[1]['name']} — {u[1]['points']} نقطة"
                     for i, u in enumerate(sorted_users[:10])])

    if not top:
        top = "لا يوجد لاعبين بعد"

    return {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
            "contents": [
                {"type": "text", "text": "🏆 الصدارة", "weight": "bold", "size": "lg"},
                {"type": "text", "text": top}
            ]
        },
        "footer": fixed_footer()
    }


# -------------------------------
# معالجة الرسائل الأساسية
# -------------------------------

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature")
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"


@handler.add(FollowEvent)
def on_follow(event):
    uid = event.source.user_id
    profile = line_bot.get_profile(uid)
    name = get_username_from_profile(profile)
    register_user(uid, name)

    send_flex(uid, build_home(USERS[uid]))


@handler.add(MessageEvent)
def on_message(event):
    try:
        uid = event.source.user_id
        text = event.message.text.strip()

        cleanup_old_users()

        # جلب اسم المستخدم
        profile = line_bot.get_profile(uid)
        name = get_username_from_profile(profile)
        register_user(uid, name)
        update_activity(uid)

        # الأوامر الأساسية
        if text == "بداية":
            send_flex(uid, build_home(USERS[uid]))
            return

        if text == "مساعدة":
            send_flex(uid, build_help())
            return

        if text == "صدارة":
            send_flex(uid, build_leaderboard())
            return

        if text == "نقاطي":
            send_flex(uid, build_my_points(USERS[uid]))
            return

        # تغيير الثيم
        if text.startswith("ثيم "):
            emo = text.replace("ثيم ", "").strip()
            if emo in THEMES:
                USERS[uid]["theme"] = emo
                send_text(uid, f"تم تغيير الثيم إلى {emo}")
                send_flex(uid, build_home(USERS[uid]))
            return

        # إيقاف اللعبة
        if text == "إيقاف":
            if uid in GAMES:
                del GAMES[uid]
            send_text(uid, "✔️ تم إيقاف اللعبة")
            return

        # بدء لعبة جديدة
        game_map = {
            "ذكاء": "IqGame",
            "رياضيات": "MathGame",
            "لون": "WordColorGame",
            "أسرع": "FastTypingGame",
            "ترتيب": "SortGame",
            "أغنية": "SongGame",
            "كلمة": "ScrambleWordGame",
            "سلسلة": "ChainWordsGame",
            "خمن": "GuessGame",
            "توافق": "CompatibilityGame",
            "ضد": "OppositeGame",
            "تكوين": "LettersWordsGame"
        }

        if text in game_map:
            game_name = game_map[text]
            cls = load_game_class(game_name)
            if cls:
                GAMES[uid] = cls(uid, USERS)
                question = GAMES[uid].start()
                send_flex(uid, question)
            else:
                send_text(uid, "❌ اللعبة غير موجودة")
            return

        # اللعب مستمر
        if uid in GAMES:
            next_ui = GAMES[uid].handle_answer(text)
            send_flex(uid, next_ui)
            return

        # منشنة البوت
        if "@Bot Mesh." in text or "@Bot Mesh" in text:
            send_flex(uid, build_help())
            return

    except Exception as e:
        logging.error("Error: %s", traceback.format_exc())
        send_text(uid, "⚠️ حدث خطأ غير متوقع")


# -------------------------------
# أدوات الإرسال
# -------------------------------

def send_text(uid, text):
    line_bot.push_message(
        PushMessageRequest(
            to=uid,
            messages=[TextMessage(text=text)]
        )
    )


def send_flex(uid, bubble):
    flex = FlexMessage(alt_text="Bot Mesh", contents=bubble)
    line_bot.push_message(
        PushMessageRequest(
            to=uid,
            messages=[flex]
        )
    )


# -------------------------------
# تشغيل التطبيق
# -------------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)))
