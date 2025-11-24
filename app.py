import os
import random
import datetime
from flask import Flask, request, abort
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi,
    ReplyMessageRequest, FlexMessage, TextMessage
)
from linebot.v3.webhook import WebhookHandler, WebhookParser
from constants import (
    GEMINI_MODEL, GEMINI_KEYS, FIXED_BUTTONS, THEMES
)
from utils import normalize_answer, load_local_questions, save_user_answer, get_user_stats

app = Flask(__name__)

# ----------------------
# LINE API
# ----------------------
CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

if not CHANNEL_ACCESS_TOKEN or not CHANNEL_SECRET:
    raise ValueError("LINE_CHANNEL_ACCESS_TOKEN or CHANNEL_SECRET not set!")

configuration = Configuration(access_token=CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

# ----------------------
# Gemini AI integration
# ----------------------
import openai

def ask_ai(prompt_text, key_index=0):
    if key_index >= len(GEMINI_KEYS):
        return None
    try:
        openai.api_key = GEMINI_KEYS[key_index]
        response = openai.Completion.create(
            model=GEMINI_MODEL,
            prompt=prompt_text,
            max_tokens=50
        )
        answer = response.choices[0].text.strip()
        return answer
    except:
        return ask_ai(prompt_text, key_index + 1)

def generate_question(game_name):
    prompt = f"اعطني سؤال لعبة {game_name} مع الإجابة الصحيحة فقط بصيغة نصية (السؤال|الإجابة)"
    ai_answer = ask_ai(prompt)
    if ai_answer and "|" in ai_answer:
        question, answer = ai_answer.split("|")
    else:
        local_data = load_local_questions(game_name)
        q = random.choice(local_data)
        question, answer = q["question"], q["answer"]
    return question.strip(), answer.strip()

def check_answer(user_text, correct_answer):
    return normalize_answer(user_text) == normalize_answer(correct_answer)

# ----------------------
# نافذة البداية
# ----------------------
def create_welcome_screen():
    bubble = {
        "type": "bubble",
        "size": "mega",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": "Bot Mesh", "weight": "bold", "size": "xl", "align": "center"},
                {"type": "text", "text": "بوت الألعاب الترفيهية", "size": "xs", "align": "center", "color": "#666666"},
                {"type": "separator"},
                {"type": "text", "text": "اختر الثيم المفضل:", "align": "center", "size": "md"},
                {"type": "box", "layout": "horizontal", "contents": [
                    {"type": "button", "style": "primary", "color": t, "action": {"type": "message", "label": name, "text": name}} 
                    for name, t in THEMES.items()
                ]},
                {"type": "separator"},
                {"type": "text", "text": "الأوامر المتاحة:\nمساعدة - عرض الألعاب\nانضم - للتسجيل\nنقاطي - إحصائياتك\nصدارة - أفضل اللاعبين", "size": "xs"},
                {"type": "text", "text": "تم إنشاء هذا البوت بواسطة عبير الدوسري @ 2025", "size": "xxs", "align": "center", "color": "#999999"}
            ]
        }
    }
    return FlexMessage(alt_text="نافذة البداية", contents=bubble)

# ----------------------
# نافذة مساعدة (الألعاب)
# ----------------------
def create_games_menu():
    def game_btn(name):
        return {"type": "button","style":"secondary","color":"#F0F0F0","height":"sm",
                "action":{"type":"message","label":name,"text":name}}

    bubble = {
        "type":"bubble",
        "size":"mega",
        "body":{"type":"box","layout":"vertical","spacing":"md",
            "contents":[
                {"type":"text","text":"قائمة الألعاب","weight":"bold","size":"xl","align":"center"},
                {"type":"text","text":"اختر لعبة للبدء","size":"xs","align":"center","color":"#777777"},
                {"type":"box","layout":"vertical","spacing":"xs","contents":[
                    {"type":"box","layout":"horizontal","spacing":"sm","contents":[game_btn(name) for name in ["ذكاء","لون","ترتيب","رياضيات","أسرع","ضد","تكوين","أغنية","لعبة","سلسلة","خمن","توافق"]]},
                ]},
                {"type":"separator"},
                {"type":"box","layout":"horizontal","spacing":"sm","contents":FIXED_BUTTONS}
            ]
        }
    }
    return FlexMessage(alt_text="قائمة الألعاب", contents=bubble)

# ----------------------
# Webhook
# ----------------------
@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature")
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except:
        abort(400)
    return "OK"

# ----------------------
# Message handler
# ----------------------
from linebot.v3.webhooks.events import MessageEvent

@handler.add(MessageEvent)
def handle_message(event):
    text = event.message.text.strip()
    user_id = event.source.user_id
    user_name = event.source.display_name if hasattr(event.source, "display_name") else "Unknown"

    with ApiClient(configuration) as api_client:
        line_api = MessagingApi(api_client)

        if text == "بداية":
            line_api.reply_message(
                ReplyMessageRequest(reply_token=event.reply_token, messages=[create_welcome_screen()])
            )
            return

        if text == "مساعدة":
            line_api.reply_message(
                ReplyMessageRequest(reply_token=event.reply_token, messages=[create_games_menu()])
            )
            return

        # الرد الافتراضي
        line_api.reply_message(
            ReplyMessageRequest(reply_token=event.reply_token, messages=[TextMessage(text="تم استلام رسالتك")])
        )

# ----------------------
# MAIN
# ----------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
