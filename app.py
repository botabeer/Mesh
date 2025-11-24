import os
import logging
from flask import Flask, request, jsonify
from linebot.v3.messaging import ApiClient, WebhookHandler, FlexSendMessage
from linebot.v3.messaging.models import TextMessage

# -------------------------------
# إعداد Flask و Logging
# -------------------------------
app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# -------------------------------
# متغيرات البيئة
# -------------------------------
CHANNEL_ACCESS = os.environ.get("CHANNEL_ACCESS", "YOUR_CHANNEL_ACCESS")
CHANNEL_SECRET = os.environ.get("CHANNEL_SECRET", "YOUR_CHANNEL_SECRET")

# -------------------------------
# LINE API Client
# -------------------------------
api_client = ApiClient(CHANNEL_ACCESS)
handler = WebhookHandler(CHANNEL_SECRET)

# -------------------------------
# المستخدمين
# -------------------------------
USERS = {}  # user_id: {"name": str, "points": int, "theme": str}

# -------------------------------
# قائمة الألعاب
# -------------------------------
GAMES = [
    "ذكاء","رياضيات","لون","أسرع","ترتيب","أغنية",
    "كلمة","سلسلة","خمن","توافق","تكوين","ضد"
]

# -------------------------------
# الأزرار الثابتة أسفل الشاشة
# -------------------------------
FOOTER_BUTTONS = [
    "إيقاف", "ذكاء", "لون", "ترتيب", "رياضيات",
    "أسرع", "ضد", "تكوين", "أغنية",
    "لعبة", "سلسلة", "خمن", "توافق"
]

def build_footer():
    buttons = []
    for label in FOOTER_BUTTONS:
        buttons.append({
            "type": "button",
            "action": {"type": "postback", "label": label, "data": label},
            "style": "secondary",
            "color": "#DDDDDD"
        })
    return buttons

# -------------------------------
# نافذة البداية
# -------------------------------
def build_home_flex(user_id):
    user = USERS.get(user_id, {"name": "ضيف", "points": 0, "theme": "💜"})
    flex = {
        "type": "bubble",
        "header": {"type": "text", "text": "🤖 Bot Mesh", "weight": "bold", "size": "lg"},
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": f"▪️ مرحباً: {user['name']}"},
                {"type": "text", "text": f"▪️ النقاط: {user['points']}"},
                {"type": "text", "text": "▪️ اختر ثيمك:"},
                {"type": "box", "layout": "horizontal", "contents": [
                    {"type": "button", "action": {"type": "postback", "label": t, "data": f"theme_{t}"}} 
                    for t in ["💜","💚","🤍","🖤","💙","🩶","🩷","🧡","🤎"]
                ]}
            ]
        },
        "footer": {"type": "box", "layout": "vertical", "contents": build_footer()}
    }
    return FlexSendMessage(alt_text="Bot Mesh Home", contents=flex)

# -------------------------------
# نافذة المساعدة
# -------------------------------
def build_help_flex():
    commands = ["▫️ لمح → تلميح أول حرف وعدد حروف الكلمة",
                "▫️ جاوب → لإرسال إجابتك",
                "▫️ إعادة → لإعادة نفس السؤال",
                "▫️ إيقاف → لإيقاف اللعبة"]
    flex = {
        "type": "bubble",
        "header": {"type": "text", "text": "🤖 Bot Mesh – مساعدة", "weight": "bold", "size": "lg"},
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": "🎮 الألعاب المتاحة:"},
                {"type": "text", "text": " – ".join(GAMES[:10])},
                {"type": "text", "text": "📝 الأوامر أثناء اللعب:"},
            ] + [{"type": "text", "text": cmd} for cmd in commands]
        },
        "footer": {"type": "box", "layout": "vertical", "contents": build_footer()}
    }
    return FlexSendMessage(alt_text="Bot Mesh Help", contents=flex)

# -------------------------------
# نافذة النقاط
# -------------------------------
def build_points_flex(user_id):
    user = USERS.get(user_id, {"name": "ضيف", "points": 0})
    flex = {
        "type": "bubble",
        "header": {"type": "text", "text": "📊 نقاطي", "weight": "bold", "size": "lg"},
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": f"▪️ {user['name']} نقاطه: {user['points']}"},
                {"type": "text", "text": "⚠️ ملاحظة: سيتم حذف الحساب بعد 7 أيام من عدم النشاط"}
            ]
        },
        "footer": {"type": "box", "layout": "vertical", "contents": build_footer()}
    }
    return FlexSendMessage(alt_text="Bot Mesh Points", contents=flex)

# -------------------------------
# نافذة الصدارة
# -------------------------------
def build_leaderboard_flex():
    sorted_users = sorted(USERS.items(), key=lambda x: x[1]["points"], reverse=True)
    contents = [{"type": "text", "text": f"{idx+1}. {user[1]['name']} - {user[1]['points']}"} for idx, user in enumerate(sorted_users[:10])]
    flex = {
        "type": "bubble",
        "header": {"type": "text", "text": "🏆 الصدارة", "weight": "bold", "size": "lg"},
        "body": {"type": "box", "layout": "vertical", "contents": contents},
        "footer": {"type": "box", "layout": "vertical", "contents": build_footer()}
    }
    return FlexSendMessage(alt_text="Bot Mesh Leaderboard", contents=flex)

# -------------------------------
# مؤشر التقدم بصري
# -------------------------------
def progress_bar(current, total, width=12):
    filled = int((current / total) * width)
    empty = width - filled
    return "█"*filled + "░"*empty

# -------------------------------
# نافذة الجولة
# -------------------------------
def build_game_round_flex(game_name, round_number, total_rounds, question, previous_answer="-"):
    progress = progress_bar(round_number, total_rounds)
    flex = {
        "type": "bubble",
        "header": {"type": "text", "text": f"🕹️ {game_name}", "weight": "bold", "size": "lg"},
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": f"▪️ الجولة {round_number} من {total_rounds}"},
                {"type": "text", "text": f"التقدم: {progress}"},
                {"type": "text", "text": f"السؤال: {question}"},
                {"type": "text", "text": f"✅ الإجابة الصحيحة للجولة السابقة: {previous_answer}"},
                {"type": "text", "text": "الأوامر المتاحة: ▫️ لمح ▫️ جاوب ▫️ إعادة ▫️ إيقاف"},
            ]
        },
        "footer": {"type": "box", "layout": "vertical", "contents": build_footer()}
    }
    return FlexSendMessage(alt_text=f"Game Round {round_number}", contents=flex)

# -------------------------------
# Webhook
# -------------------------------
@app.route("/callback", methods=['POST'])
def callback():
    data = request.get_json()
    user_id = data.get("source", {}).get("userId", "guest")
    message_text = data.get("message", {}).get("text", "")

    if user_id not in USERS:
        USERS[user_id] = {"name": f"مستخدم {len(USERS)+1}", "points": 0, "theme": "💜"}

    # منشنة البوت
    if "@Bot Mesh" in message_text:
        return jsonify({"reply": [build_home_flex(user_id), build_help_flex()]})

    # الأوامر النصية
    if message_text.startswith("بداية"):
        return jsonify({"reply": [build_home_flex(user_id)]})
    if message_text.startswith("مساعدة"):
        return jsonify({"reply": [build_help_flex()]})
    if message_text.startswith("نقاطي"):
        return jsonify({"reply": [build_points_flex(user_id)]})
    if message_text.startswith("صدارة"):
        return jsonify({"reply": [build_leaderboard_flex()]})

    return jsonify({"reply": [{"type": "text", "text": "مرحباً! استخدم @Bot Mesh. لعرض الألعاب."}]})

# -------------------------------
# تشغيل التطبيق
# -------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
