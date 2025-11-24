# Bot Mesh - Full LINE Bot v2025
# Created by: Abeer Aldosari © 2025
# Features: Gemini AI, Games, Scoring, User Management, Arabic Normalization

import os, sys, random, re, json, time
from datetime import datetime, timedelta
from flask import Flask, request, abort
from linebot.v3 import WebhookHandler
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi, ReplyMessageRequest, FlexMessage, TextMessage
)
import requests

app = Flask(__name__)

# --------------------------
# LINE CONFIG
# --------------------------
CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

if not CHANNEL_ACCESS_TOKEN or not CHANNEL_SECRET:
    print("⚠️ متغير بيئة مفقود!")
    if not CHANNEL_ACCESS_TOKEN: print("LINE_CHANNEL_ACCESS_TOKEN غير موجود.")
    if not CHANNEL_SECRET: print("LINE_CHANNEL_SECRET غير موجود.")
    sys.exit(1)

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
# قاعدة ثابتة عامة
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
    "permanent_buttons": ["انضم","انسحب","نقاطي","صدارة","إيقاف"],
    "copyright":"تم إنشاء هذا البوت بواسطة عبير الدوسري @ 2025",
    "allowed_emojis": ["▫️","▪️","🏅","🏆"],
    "normalize_arabic": True
}

# --------------------------
# قواعد المستخدمين والألعاب
# --------------------------
USERS = {}  # user_id: {"name":..., "joined":True, "score":0,"last_seen":datetime}
CURRENT_GAMES = {}  # user_id: {"game":..., "round":..., "question":..., "answer":...}
THEMES = {}  # user_id: theme_color

# --------------------------
# Arabic normalization
# --------------------------
ARABIC_NORMALIZATION = {"أ":"ا","إ":"ا","آ":"ا","ؤ":"و","ئ":"ي","ة":"ه","ى":"ي"}
def normalize_arabic(text):
    text=text.strip().lower()
    text=re.sub(r'[\u0617-\u061A\u064B-\u0652]','',text)
    for k,v in ARABIC_NORMALIZATION.items(): text=text.replace(k,v)
    return text

def verify_answer(correct, answer):
    return normalize_arabic(answer) in normalize_arabic(correct)

# --------------------------
# Gemini AI Query
# --------------------------
def query_gemini_ai(prompt):
    for key in GEMINI_KEYS:
        if not key: continue
        try:
            resp=requests.post(
                "https://api.gemini.com/v2/generate",
                headers={"Authorization":f"Bearer {key}"},
                json={"prompt":prompt,"max_tokens":200}
            )
            if resp.status_code==200: return resp.json().get("text","سؤال افتراضي").strip()
        except: continue
    try:
        with open(GAME_RULES["ai_fallback_file"],"r",encoding="utf-8") as f:
            all_q=json.load(f)
            for questions in all_q.values(): return random.choice(questions)
    except: pass
    return "سؤال افتراضي"

# --------------------------
# Buttons
# --------------------------
def create_button(title,color="#4CAF50",style="primary"):
    return {"type":"button","style":style,"color":color,"height":"sm","action":{"type":"message","label":title,"text":title}}

# --------------------------
# Welcome Screen
# --------------------------
def welcome_screen():
    bubble={"type":"bubble","size":"mega","paddingAll":"15px","body":{"type":"box","layout":"vertical","spacing":"md","contents":[
        {"type":"text","text":"Bot Mesh","weight":"bold","size":"xl","align":"center"},
        {"type":"text","text":"بوت الألعاب الاحترافي","size":"xs","align":"center","color":"#666666"},
        {"type":"separator","margin":"md"},
        {"type":"text","text":"مرحباً! اختر ثيمك المفضل:","align":"center","size":"md"},
        {"type":"box","layout":"vertical","spacing":"sm","margin":"md","contents":[
            {"type":"box","layout":"horizontal","spacing":"sm","contents":[create_button("أبيض"),create_button("أسود"),create_button("رمادي")]},
            {"type":"box","layout":"horizontal","spacing":"sm","contents":[create_button("أزرق"),create_button("أخضر"),create_button("وردي")]}
        ]},
        {"type":"separator","margin":"md"},
        {"type":"text","text":"أوامر البوت:","size":"sm","margin":"xs"},
        {"type":"text","text":"مساعدة - قائمة الألعاب\nانضم - التسجيل\nنقاطي - نقاطك\nصدارة - أفضل اللاعبين\nإيقاف - إيقاف اللعبة","size":"xs","color":"#777777","margin":"xs"},
        {"type":"text","text":GAME_RULES["copyright"],"size":"xs","color":"#999999","align":"center","margin":"md"}
    ]}}
    return FlexMessage(alt_text="نافذة البداية",contents=bubble)

# --------------------------
# Games Menu
# --------------------------
def games_menu():
    game_names=[["ذكاء","لون","ترتيب"],["رياضيات","أسرع","ضد"],["تكوين","أغنية","لعبة"],["سلسلة","خمن","توافق"]]
    contents=[{"type":"text","text":"قائمة الألعاب","weight":"bold","size":"xl","align":"center"},
              {"type":"text","text":"اختر لعبة للبدء","size":"xs","align":"center","color":"#777777","margin":"xs"}]
    for row in game_names: contents.append({"type":"box","layout":"horizontal","spacing":"sm","contents":[create_button(name,"#F0F0F0","secondary") for name in row]})
    contents.append({"type":"separator","margin":"md"})
    # bottom fixed buttons (permanent + repeated games)
    bottom_buttons=[]
    for name in GAME_RULES["permanent_buttons"]: 
        bottom_buttons.append(create_button(name,"#3F51B5" if name=="انضم" else "#E0E0E0","primary" if name=="انضم" else "secondary"))
    for row in game_names:
        for game in row: bottom_buttons.append(create_button(game,"#F0F0F0","secondary"))
    contents.append({"type":"box","layout":"horizontal","spacing":"sm","contents":bottom_buttons})
    contents.append({"type":"text","text":GAME_RULES["copyright"],"size":"xs","color":"#999999","align":"center","margin":"md"})
    return FlexMessage(alt_text="قائمة الألعاب",contents={"type":"bubble","size":"mega","paddingAll":"12px","body":{"type":"box","layout":"vertical","spacing":"md","contents":contents}})

# --------------------------
# Webhook
# --------------------------
@app.route("/callback",methods=["POST"])
def callback():
    signature=request.headers.get("X-Line-Signature","")
    body=request.get_data(as_text=True)
    try: handler.handle(body,signature)
    except Exception as e:
        print(f"خطأ في الحدث: {e}")
        abort(400)
    return "OK"

# --------------------------
# Main
# --------------------------
if __name__=="__main__":
    port=int(os.environ.get("PORT",5000))
    print(f"🚀 البوت يعمل على المنفذ {port}")
    app.run(host="0.0.0.0",port=port,debug=True)
