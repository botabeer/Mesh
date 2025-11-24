# -*- coding: utf-8 -*-
import os
import logging
from datetime import datetime, timedelta
from flask import Flask, request, abort
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent
from constants import BOT_NAME, GEMINI_KEYS, get_username
from ui_builder import UIBuilder

# إعداد Flask
app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# التحقق من المتغيرات البيئية
CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
CHANNEL_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

if not CHANNEL_SECRET or not CHANNEL_TOKEN:
    logging.error("⚠️ متغيرات البيئة مفقودة! تحقق من LINE_CHANNEL_SECRET و LINE_CHANNEL_ACCESS_TOKEN")
    exit(1)

if not any(GEMINI_KEYS):
    logging.warning("⚠️ تحذير: لا توجد مفاتيح Gemini API محددة")

# إعداد LINE
configuration = Configuration(access_token=CHANNEL_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

# قاعدة بيانات المستخدمين
registered_users = {}
user_themes = {}  # تخزين ثيم كل مستخدم
active_games = {}  # الألعاب النشطة

# تنظيف البيانات القديمة (أسبوع)
def clean_old_data():
    """حذف بيانات المستخدمين بعد أسبوع"""
    current_time = datetime.now()
    to_delete = []
    
    for user_id, data in registered_users.items():
        if 'registered_at' in data:
            if current_time - data['registered_at'] > timedelta(days=7):
                to_delete.append(user_id)
    
    for user_id in to_delete:
        del registered_users[user_id]
        if user_id in user_themes:
            del user_themes[user_id]
        if user_id in active_games:
            del active_games[user_id]
        logging.info(f"🗑️ تم حذف بيانات المستخدم: {user_id}")

@app.route("/callback", methods=['POST'])
def callback():
    """استقبال رسائل LINE"""
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        logging.error("⚠️ توقيع غير صالح")
        abort(400)
    
    return 'OK'

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    """معالجة الرسائل الواردة"""
    try:
        user_id = event.source.user_id
        text = event.message.text.strip()
        
        # تنظيف البيانات القديمة
        clean_old_data()
        
        # جلب معلومات المستخدم
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            
            try:
                profile = line_bot_api.get_profile(user_id)
                username = get_username(profile)
            except:
                username = "مستخدم"
            
            # تسجيل المستخدم تلقائيًا عند أول تفاعل
            if user_id not in registered_users:
                registered_users[user_id] = {
                    "name": username,
                    "points": 0,
                    "registered_at": datetime.now(),
                    "is_registered": False
                }
                logging.info(f"✅ مستخدم جديد: {username} ({user_id})")
            
            # الحصول على الثيم الحالي
            current_theme = user_themes.get(user_id, "💜")
            
            # معالجة الأوامر
            if text.lower() == "home":
                reply = UIBuilder.build_home(current_theme)
                
            elif text.lower() in ["games", "info", "help"]:
                reply = UIBuilder.build_help(current_theme)
                
            elif text.startswith("ثيم "):
                theme = text.replace("ثيم ", "").strip()
                if theme in ["💜", "💚", "🤍", "🖤", "💙", "🩶", "🩷", "🧡", "🤎"]:
                    user_themes[user_id] = theme
                    reply = UIBuilder.build_home(theme)
                else:
                    return
                    
            elif text == "انضم":
                registered_users[user_id]["is_registered"] = True
                reply = TextMessage(text=f"✅ {username} تم تسجيلك بنجاح! يمكنك الآن اللعب")
                
            elif text == "انسحب":
                if user_id in registered_users:
                    registered_users[user_id]["is_registered"] = False
                reply = TextMessage(text=f"👋 {username} تم إلغاء تسجيلك")
                
            elif text == "نقاطي":
                if user_id in registered_users:
                    points = registered_users[user_id]["points"]
                    reply = UIBuilder.build_my_points(username, points, current_theme)
                else:
                    reply = TextMessage(text="⚠️ يجب التسجيل أولاً باستخدام زر 'انضم'")
                    
            elif text == "صدارة":
                # ترتيب اللاعبين حسب النقاط
                sorted_users = sorted(
                    [(u["name"], u["points"]) for u in registered_users.values() if u.get("is_registered")],
                    key=lambda x: x[1],
                    reverse=True
                )[:10]
                
                leaderboard = "🏆 لوحة الصدارة:\n\n"
                for i, (name, points) in enumerate(sorted_users, 1):
                    leaderboard += f"{i}. {name}: {points} نقطة\n"
                
                reply = TextMessage(text=leaderboard if sorted_users else "لا يوجد لاعبين مسجلين بعد")
                
            elif text == "إيقاف":
                if user_id in active_games:
                    del active_games[user_id]
                reply = TextMessage(text="⏸️ تم إيقاف اللعبة الحالية")
                
            elif text.startswith("لعبة "):
                # التحقق من التسجيل
                if not registered_users.get(user_id, {}).get("is_registered"):
                    reply = TextMessage(text="⚠️ يجب التسجيل أولاً باستخدام زر 'انضم'")
                else:
                    # هنا سيتم تشغيل اللعبة المطلوبة
                    game_name = text.replace("لعبة ", "").strip()
                    reply = TextMessage(text=f"🎮 جاري تحميل لعبة {game_name}...\n(سيتم إضافة منطق الألعاب لاحقاً)")
                    
            else:
                # البوت صامت - لا يرد على رسائل عشوائية
                return
            
            # إرسال الرد
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[reply]
                )
            )
            
    except Exception as e:
        logging.error(f"❌ خطأ في معالجة الرسالة: {e}")

@app.route("/", methods=['GET'])
def home():
    """صفحة رئيسية بسيطة"""
    return f"""
    <html>
        <head>
            <title>{BOT_NAME}</title>
            <meta charset="utf-8">
        </head>
        <body style="text-align:center; font-family:Arial; padding:50px;">
            <h1>🤖 {BOT_NAME}</h1>
            <p>البوت يعمل بنجاح ✅</p>
            <p>المستخدمين المسجلين: {len(registered_users)}</p>
            <p>تم الإنشاء بواسطة عبير الدوسري @ 2025</p>
        </body>
    </html>
    """

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    logging.info(f"🚀 بدء تشغيل {BOT_NAME} على المنفذ {port}")
    app.run(host="0.0.0.0", port=port, debug=False)
