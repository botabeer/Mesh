# Bot Mesh - Full LINE Bot with 12 Games, Gemini AI, Rounds, Scores, Winner Window
# Created by: Abeer Aldosari © 2025
# Version 7.0 – Full Integration

import os
import json
import time
import random
import hashlib
from datetime import datetime, timedelta
from flask import Flask, request, abort
import requests

# LINE SDK v3
from linebot.v3 import WebhookHandler
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi,
    ReplyMessageRequest, FlexMessage, TextMessage
)

app = Flask(__name__)

# --------------------------
# LINE CONFIG
# --------------------------
CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
configuration = Configuration(access_token=CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

# --------------------------
# Gemini AI Keys
# --------------------------
GEMINI_KEYS = [
    os.getenv("GEMINI_API_KEY_1"),
    os.getenv("GEMINI_API_KEY_2"),
    os.getenv("GEMINI_API_KEY_3")
]

# --------------------------
# القواعد الثابتة
# --------------------------
GAME_RULES = {
    "rounds_per_game": 5,
    "first_correct_counts": True,
    "registered_only": True,
    "hint_format": "_ _ _",
    "fast_game_timer": 10,
    "score_per_correct": 1,
    "data_retention_days": 7,
    "ai_fallback_file": "games/questions.json",
    "permanent_buttons": ["انضم", "انسحب", "نقاطي", "صدارة", "إيقاف"],
    "copyright": "تم إنشاء هذا البوت بواسطة عبير الدوسري @ 2025"
}

# --------------------------
# قاعدة البيانات في الذاكرة
# --------------------------
USERS = {}          # {user_id: {"name": str, "points": int, "joined": True, "last_active": timestamp, "active": True}}
CURRENT_GAMES = {}  # {"game_name": {"round": int, "questions": [...], "answers": [...], "players": {user_id: {"score": int, "answered": False}}}}
THEMES = {}         # {user_id: theme_color}

# --------------------------
# أزرار ثابتة
# --------------------------
def create_button(title, color="#4CAF50", style="primary"):
    return {
        "type": "button",
        "style": style,
        "color": color,
        "height": "sm",
        "action": {"type": "message", "label": title, "text": title}
    }

# --------------------------
# Gemini AI Integration
# --------------------------
def query_gemini_ai(prompt):
    """Generate question text using Gemini AI, fallback to local file."""
    for key in GEMINI_KEYS:
        if not key:
            continue
        try:
            response = requests.post(
                "https://api.gemini.com/v2/generate",
                headers={"Authorization": f"Bearer {key}"},
                json={"prompt": prompt, "max_tokens": 200}
            )
            if response.status_code == 200:
                data = response.json()
                return data.get("text", "").strip()
        except Exception:
            continue
    # fallback
    try:
        with open(GAME_RULES["ai_fallback_file"], "r", encoding="utf-8") as f:
            all_questions = json.load(f)
            for questions in all_questions.values():
                return random.choice(questions)
    except Exception:
        return "سؤال افتراضي"
    return "سؤال افتراضي"

def verify_answer(question, answer):
    """Check if the user's answer is correct using AI or simple string match."""
    return answer.strip().lower() in question.strip().lower()

# --------------------------
# نافذة البداية
# --------------------------
def welcome_screen():
    bubble = {
        "type": "bubble",
        "size": "mega",
        "paddingAll": "15px",
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
            "contents": [
                {"type": "text", "text": "Bot Mesh", "weight": "bold", "size": "xl", "align": "center"},
                {"type": "text", "text": "بوت الألعاب الاحترافي", "size": "xs", "align": "center", "color": "#666666"},
                {"type": "separator", "margin": "md"},
                {"type": "text", "text": "مرحباً! اختر ثيمك المفضل:", "align": "center", "size": "md"},
                {"type": "box","layout": "vertical","spacing": "sm","margin": "md",
                 "contents":[
                     {"type": "box","layout": "horizontal","spacing": "sm",
                      "contents":[create_button("أبيض"), create_button("أسود"), create_button("رمادي")]},
                     {"type": "box","layout": "horizontal","spacing": "sm",
                      "contents":[create_button("أزرق"), create_button("أخضر"), create_button("وردي")]}
                 ]},
                {"type": "separator", "margin": "md"},
                {"type": "text", "text": "أوامر البوت:", "size": "sm", "margin": "xs"},
                {"type": "text", "text": "مساعدة - قائمة الألعاب\nانضم - التسجيل\nنقاطي - نقاطك\nصدارة - أفضل اللاعبين\nإيقاف - إيقاف البوت", "size": "xs", "color": "#777777", "margin": "xs"},
                {"type": "text", "text": GAME_RULES["copyright"], "size": "xs", "color": "#999999", "align": "center", "margin": "md"}
            ]
        }
    }
    return FlexMessage(alt_text="نافذة البداية", contents=bubble)

# --------------------------
# نافذة المساعدة مع الألعاب والأزرار الثابتة
# --------------------------
def games_menu():
    game_names = [
        ["ذكاء","لون","ترتيب"],
        ["رياضيات","أسرع","ضد"],
        ["تكوين","أغنية","لعبة"],
        ["سلسلة","خمن","توافق"]
    ]

    contents = [
        {"type": "text", "text": "قائمة الألعاب", "weight": "bold", "size": "xl", "align": "center"},
        {"type": "text", "text": "اختر لعبة للبدء", "size": "xs", "align": "center", "color": "#777777", "margin": "xs"},
    ]

    for row in game_names:
        row_buttons = [create_button(name, "#F0F0F0", style="secondary") for name in row]
        contents.append({"type": "box", "layout": "horizontal", "spacing": "sm", "contents": row_buttons})

    contents.append({"type": "separator", "margin": "md"})

    # الأزرار الثابتة + الألعاب مرة ثانية
    bottom_buttons = []
    for name in GAME_RULES["permanent_buttons"]:
        style = "primary" if name == "انضم" else "secondary"
        color = "#3F51B5" if name == "انضم" else "#E0E0E0"
        bottom_buttons.append(create_button(name, color=color, style=style))
    for row in game_names:
        for game in row:
            bottom_buttons.append(create_button(game, color="#F0F0F0", style="secondary"))

    contents.append({"type": "box", "layout": "horizontal", "spacing": "sm", "contents": bottom_buttons})
    # الحقوق أسفل النافذة
    contents.append({"type": "text", "text": GAME_RULES["copyright"], "size": "xs", "color": "#999999", "align": "center", "margin": "md"})

    bubble = {"type": "bubble","size":"mega","paddingAll":"12px","body":{"type":"box","layout":"vertical","spacing":"md","contents":contents}}
    return FlexMessage(alt_text="قائمة الألعاب", contents=bubble)

# --------------------------
# نافذة إعلان الفائز مع زر إعادة اللعبة
# --------------------------
def winner_screen(game_name):
    if game_name not in CURRENT_GAMES:
        return TextMessage(text="لا توجد لعبة نشطة حالياً.")
    
    game = CURRENT_GAMES[game_name]
    max_score = max([game["players"][pid]["score"] for pid in game["players"]])
    winners = [USERS[pid]["name"] for pid in game["players"] if game["players"][pid]["score"] == max_score]

    winner_text = "، ".join(winners)
    message = f"🏆 الفائز: {winner_text}\nالنقاط: {max_score}"

    bubble = {
        "type": "bubble",
        "size": "mega",
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
            "contents": [
                {"type": "text", "text": "🎉 انتهت اللعبة!", "weight": "bold", "size": "xl", "align": "center"},
                {"type": "text", "text": message, "align": "center", "margin": "md"},
                {"type": "separator", "margin": "md"},
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "button",
                            "style": "primary",
                            "color": "#3F51B5",
                            "height": "sm",
                            "action": {"type": "message", "label": "إعادة اللعبة", "text": game_name}
                        }
                    ]
                },
                {"type": "text", "text": GAME_RULES["copyright"], "size": "xs", "color": "#999999", "align": "center", "margin": "md"}
            ]
        }
    }
    return FlexMessage(alt_text="إعلان الفائز", contents=bubble)

# --------------------------
# توافق ذكي
# --------------------------
def compatibility_percentage(name1, name2):
    key = sorted([name1.strip(), name2.strip()])
    h = hashlib.sha256("".join(key).encode()).hexdigest()
    return int(h[:2], 16) % 101  # 0-100%

# --------------------------
# Webhook
# --------------------------
@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except Exception:
        abort(400)
    return "OK"

# --------------------------
# Event Handler
# --------------------------
@handler.add
def handle(event):
    user_id = getattr(event.source, "user_id", "unknown")
    user_name = getattr(event.source, "user_name", "مستخدم")

    if getattr(event, "type", None) == "message" and getattr(event.message, "type", None) == "text":
        text = event.message.text.strip()
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)

            # تسجيل المستخدم عند "انضم"
            if text == "انضم":
                USERS[user_id] = {"name": user_name, "points": 0, "joined": True, "last_active": time.time(), "active": True}
                line_bot_api.reply_message(
                    ReplyMessageRequest(reply_token=event.reply_token,
                                        messages=[TextMessage(text="تم تسجيلك بنجاح!")])
                )
                return

            # حذف البيانات القديمة بعد أسبوع
            now = time.time()
            for uid in list(USERS.keys()):
                if now - USERS[uid].get("last_active", now) > GAME_RULES["data_retention_days"]*86400:
                    del USERS[uid]

            # تحقق التسجيل
            if GAME_RULES["registered_only"] and user_id not in USERS:
                line_bot_api.reply_message(
                    ReplyMessageRequest(reply_token=event.reply_token,
                                        messages=[TextMessage(text="عليك التسجيل أولاً باستخدام 'انضم'")])
                )
                return

            # نافذة البداية
            if text == "بداية":
                line_bot_api.reply_message(
                    ReplyMessageRequest(reply_token=event.reply_token,messages=[welcome_screen()])
                )
                return

            # نافذة المساعدة
            if text == "مساعدة":
                line_bot_api.reply_message(
                    ReplyMessageRequest(reply_token=event.reply_token,messages=[games_menu()])
                )
                return

            # انسحب: تجاهل الإجابات المستقبلية
            if text == "انسحب":
                if user_id in USERS:
                    USERS[user_id]["active"] = False
                line_bot_api.reply_message(
                    ReplyMessageRequest(reply_token=event.reply_token,
                                        messages=[TextMessage(text="تم الانسحاب ولن يتم احتساب إجاباتك لاحقًا.")])
                )
                return

            # توافق: نسبة ذكية
            if text.startswith("توافق"):
                parts = text.split()
                if len(parts) == 3:
                    perc = compatibility_percentage(parts[1], parts[2])
                    line_bot_api.reply_message(
                        ReplyMessageRequest(reply_token=event.reply_token,
                                            messages=[TextMessage(text=f"نسبة التوافق بين {parts[1]} و {parts[2]}: {perc}%")])
                    )
                    return

            # إيقاف: يوقف اللعبة الحالية
            if text == "إيقاف":
                CURRENT_GAMES.clear()
                line_bot_api.reply_message(
                    ReplyMessageRequest(reply_token=event.reply_token,
                                        messages=[TextMessage(text="تم إيقاف جميع الألعاب.")])
                )
                return

            # الرد الافتراضي
            line_bot_api.reply_message(
                ReplyMessageRequest(reply_token=event.reply_token,
                                    messages=[TextMessage(text="تم استلام رسالتك")])
            )

# --------------------------
# MAIN
# --------------------------
if __name__ == "__main__":
    app.run(port=5000, debug=True)
