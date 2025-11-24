# -*- coding: utf-8 -*-
import os
import sys
import logging
from datetime import datetime, timedelta
from flask import Flask, request, abort

# إضافة المسار الرئيسي للمشروع
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

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

# استيراد الألعاب
from games import *

# إعداد Flask
app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# التحقق من المتغيرات البيئية
CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
CHANNEL_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

if not CHANNEL_SECRET or not CHANNEL_TOKEN:
    logger.error("⚠️ متغيرات البيئة مفقودة! تحقق من LINE_CHANNEL_SECRET و LINE_CHANNEL_ACCESS_TOKEN")
    exit(1)

if not any(GEMINI_KEYS):
    logger.warning("⚠️ تحذير: لا توجد مفاتيح Gemini API محددة")

# إعداد LINE
configuration = Configuration(access_token=CHANNEL_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

# قاعدة بيانات المستخدمين والألعاب
registered_users = {}
user_themes = {}
active_games = {}

# خريطة الألعاب المتاحة
AVAILABLE_GAMES = {
    "IQ": IqGame,
    "رياضيات": MathGame,
    "لون الكلمة": WordColorGame,
    "كلمة مبعثرة": ScrambleWordGame,
    "كتابة سريعة": FastTypingGame,
    "عكس": OppositeGame,
    "حروف وكلمات": LettersWordsGame,
    "أغنية": SongGame,
    "إنسان حيوان نبات": HumanAnimalPlantGame,
    "سلسلة كلمات": ChainWordsGame,
    "تخمين": GuessGame,
    "توافق": CompatibilityGame
}

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
        logger.info(f"🗑️ تم حذف بيانات المستخدم: {user_id}")

@app.route("/callback", methods=['POST'])
def callback():
    """استقبال رسائل LINE"""
    signature = request.headers.get('X-Line-Signature', '')
    body = request.get_data(as_text=True)
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        logger.error("⚠️ توقيع غير صالح")
        abort(400)
    except Exception as e:
        logger.error(f"❌ خطأ في معالجة الطلب: {e}")
        abort(500)
    
    return 'OK'

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    """معالجة الرسائل الواردة"""
    try:
        user_id = event.source.user_id
        text = event.message.text.strip()
        
        if not text:
            logger.warning(f"⚠️ رسالة فارغة من {user_id}")
            return
        
        # تنظيف البيانات القديمة
        clean_old_data()
        
        # جلب معلومات المستخدم
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            
            try:
                profile = line_bot_api.get_profile(user_id)
                username = get_username(profile)
            except Exception as e:
                logger.warning(f"⚠️ فشل جلب ملف المستخدم: {e}")
                username = "مستخدم"
            
            # تسجيل المستخدم تلقائيًا عند أول تفاعل
            if user_id not in registered_users:
                registered_users[user_id] = {
                    "name": username,
                    "points": 0,
                    "registered_at": datetime.now(),
                    "is_registered": False
                }
                logger.info(f"✅ مستخدم جديد: {username} ({user_id})")
            
            # الحصول على الثيم الحالي
            current_theme = user_themes.get(user_id, "💜")
            
            # متغير للرد (مهم جداً)
            reply = None
            
            # معالجة الأوامر
            text_lower = text.lower()
            
            if text_lower == "home":
                reply = UIBuilder.build_home(current_theme)
                
            elif text_lower in ["games", "info", "help"]:
                reply = UIBuilder.build_help(current_theme)
                
            elif text.startswith("ثيم "):
                theme = text.replace("ثيم ", "").strip()
                if theme in ["💜", "💚", "🤍", "🖤", "💙", "🩶", "🩷", "🧡", "🤎"]:
                    user_themes[user_id] = theme
                    reply = UIBuilder.build_home(theme)
                else:
                    reply = TextMessage(text="⚠️ الثيم غير صالح")
                    
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
                sorted_users = sorted(
                    [(u["name"], u["points"]) for u in registered_users.values() if u.get("is_registered")],
                    key=lambda x: x[1],
                    reverse=True
                )[:10]
                
                if sorted_users:
                    leaderboard = "🏆 لوحة الصدارة:\n\n"
                    for i, (name, points) in enumerate(sorted_users, 1):
                        medal = ["🥇", "🥈", "🥉"][i-1] if i <= 3 else f"{i}."
                        leaderboard += f"{medal} {name}: {points} نقطة\n"
                else:
                    leaderboard = "لا يوجد لاعبين مسجلين بعد"
                
                reply = TextMessage(text=leaderboard)
                
            elif text == "إيقاف":
                if user_id in active_games:
                    del active_games[user_id]
                    reply = TextMessage(text="⏸️ تم إيقاف اللعبة الحالية")
                else:
                    reply = TextMessage(text="⚠️ لا توجد لعبة نشطة")
                
            elif text.startswith("لعبة "):
                if not registered_users.get(user_id, {}).get("is_registered"):
                    reply = TextMessage(text="⚠️ يجب التسجيل أولاً باستخدام زر 'انضم'")
                else:
                    game_name = text.replace("لعبة ", "").strip()
                    
                    if game_name in AVAILABLE_GAMES:
                        GameClass = AVAILABLE_GAMES[game_name]
                        try:
                            # إنشاء نسخة من اللعبة
                            game_instance = GameClass(line_bot_api)
                            game_instance.set_theme(current_theme)
                            
                            # حفظ اللعبة النشطة
                            active_games[user_id] = game_instance
                            
                            # بدء اللعبة
                            reply = game_instance.start_game()
                            logger.info(f"🎮 {username} بدأ لعبة {game_name}")
                        except Exception as e:
                            logger.error(f"❌ خطأ في تشغيل اللعبة {game_name}: {e}")
                            reply = TextMessage(text=f"❌ حدث خطأ في تشغيل اللعبة: {str(e)}")
                    else:
                        reply = TextMessage(text=f"⚠️ اللعبة '{game_name}' غير متاحة")
                    
            else:
                # التحقق إذا كان المستخدم في لعبة نشطة
                if user_id in active_games:
                    game_instance = active_games[user_id]
                    
                    try:
                        result = game_instance.check_answer(text, user_id, username)
                        
                        if result:
                            # تحديث النقاط
                            if result.get('points', 0) > 0:
                                registered_users[user_id]['points'] += result['points']
                            
                            # إذا انتهت اللعبة، احذفها
                            if result.get('game_over', False):
                                del active_games[user_id]
                            
                            # الحصول على الرد
                            reply = result.get('response')
                            
                            if not reply:
                                logger.warning(f"⚠️ اللعبة لم ترجع رد مناسب")
                                return
                                
                    except Exception as e:
                        logger.error(f"❌ خطأ في معالجة إجابة اللعبة: {e}")
                        reply = TextMessage(text="❌ حدث خطأ في معالجة إجابتك")
                else:
                    # البوت صامت - لا يرد على رسائل غير معروفة
                    logger.info(f"📝 رسالة من مستخدم غير مسجل في لعبة: {text[:50]}")
                    return
            
            # إرسال الرد (فقط إذا كان موجود)
            if reply:
                try:
                    line_bot_api.reply_message_with_http_info(
                        ReplyMessageRequest(
                            reply_token=event.reply_token,
                            messages=[reply]
                        )
                    )
                except Exception as e:
                    logger.error(f"❌ فشل إرسال الرسالة: {e}")
            else:
                logger.warning("⚠️ لا يوجد رد للإرسال - البوت صامت")
            
    except Exception as e:
        logger.error(f"❌ خطأ عام في معالجة الرسالة: {e}", exc_info=True)

@app.route("/", methods=['GET'])
def home():
    """صفحة رئيسية بسيطة"""
    return f"""
    <html>
        <head>
            <title>{BOT_NAME}</title>
            <meta charset="utf-8">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    text-align: center;
                    padding: 50px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                }}
                .container {{
                    background: rgba(255,255,255,0.1);
                    padding: 30px;
                    border-radius: 15px;
                    max-width: 600px;
                    margin: 0 auto;
                }}
                h1 {{ margin-bottom: 20px; }}
                .stats {{
                    background: rgba(255,255,255,0.2);
                    padding: 20px;
                    border-radius: 10px;
                    margin-top: 20px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🤖 {BOT_NAME}</h1>
                <p>✅ البوت يعمل بنجاح</p>
                <div class="stats">
                    <p><strong>المستخدمين المسجلين:</strong> {len(registered_users)}</p>
                    <p><strong>الألعاب المتاحة:</strong> {len(AVAILABLE_GAMES)}</p>
                    <p><strong>الألعاب النشطة:</strong> {len(active_games)}</p>
                </div>
                <p style="margin-top: 20px; font-size: 12px;">
                    تم الإنشاء بواسطة عبير الدوسري @ 2025
                </p>
            </div>
        </body>
    </html>
    """

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    logger.info(f"🚀 بدء تشغيل {BOT_NAME} على المنفذ {port}")
    logger.info(f"📦 تم تحميل {len(AVAILABLE_GAMES)} لعبة")
    app.run(host="0.0.0.0", port=port, debug=False)
