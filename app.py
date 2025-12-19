import logging
from flask import Flask, request, abort, jsonify
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import Configuration, ApiClient, MessagingApi, ReplyMessageRequest
from linebot.v3.webhooks import MessageEvent, TextMessageContent
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

from config import Config
from database import Database
from game_manager import GameManager
from text_manager import TextManager
from ui import UI

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

app = Flask(__name__)
line_config = Configuration(access_token=Config.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(Config.LINE_CHANNEL_SECRET)

db = Database()
game_mgr = GameManager(db)
text_mgr = TextManager()

executor = ThreadPoolExecutor(max_workers=Config.WORKERS, thread_name_prefix="worker")

def reply_message(reply_token, messages):
    if not isinstance(messages, list):
        messages = [messages]
    safe_messages = [m for m in messages if m][:5]
    try:
        with ApiClient(line_config) as client:
            MessagingApi(client).reply_message(
                ReplyMessageRequest(reply_token=reply_token, messages=safe_messages)
            )
    except Exception as e:
        logger.error(f"Reply error: {e}")

def process_message(user_id, text, reply_token):
    try:
        normalized = Config.normalize(text)
        
        # تسجيل جديد
        if not db.is_registered(user_id):
            if normalized in ["تسجيل", "تسجل", "سجل"]:
                db.register_user(user_id, f"لاعب{user_id[-4:]}")
                user = db.get_user(user_id)
                reply_message(reply_token, UI.registration_success(user['name'], user['theme']))
            else:
                reply_message(reply_token, UI.text_message("اكتب تسجيل للبدء"))
            return
        
        db.update_activity(user_id)
        user = db.get_user(user_id)
        
        # تغيير اسم
        if db.is_changing_name(user_id):
            if Config.MIN_NAME_LENGTH <= len(text) <= Config.MAX_NAME_LENGTH:
                db.update_name(user_id, text)
                db.clear_changing_name(user_id)
                reply_message(reply_token, UI.text_message(f"تم تغيير اسمك الى: {text}"))
            else:
                reply_message(reply_token, UI.text_message(f"الاسم يجب ان يكون بين {Config.MIN_NAME_LENGTH} و {Config.MAX_NAME_LENGTH} حرف"))
            return
        
        # لعبة نشطة
        if db.has_active_game(user_id):
            game = db.get_game_progress(user_id)
            
            if normalized in ["لمح", "تلميح"] and hasattr(game, 'supports_hint') and game.supports_hint:
                hint = game.get_hint()
                if hint:
                    reply_message(reply_token, UI.text_message(hint))
                return
            
            if normalized in ["جاوب", "الجواب", "الاجابه", "الاجابة"] and hasattr(game, 'supports_reveal') and game.supports_reveal:
                answer = game.reveal_answer()
                if answer:
                    reply_message(reply_token, UI.text_message(answer))
                return
            
            if normalized in ["ايقاف", "توقف", "اوقف", "انهاء", "انهي"]:
                score = game_mgr.stop_game(user_id)
                reply_message(reply_token, UI.text_message(f"تم ايقاف اللعبة. حصلت على {score} نقطة"))
                return
            
            result, correct = game_mgr.process_answer(user_id, text)
            
            if result and isinstance(result, dict) and result.get("finished"):
                messages = [UI.game_result(result['game_name'], result['score'], result['total'], user['theme'])]
                for achievement in result.get('achievements', []):
                    messages.append(UI.achievement_unlocked(achievement, user['theme']))
                reply_message(reply_token, messages)
            elif correct:
                result = game_mgr.next_question(user_id)
                if result:
                    reply_message(reply_token, result)
            else:
                reply_message(reply_token, UI.text_message("اجابة خاطئة، حاول مرة اخرى"))
            return
        
        # اوامر رئيسية
        if normalized in ["بدايه", "بداية", "القائمه", "القائمة", "الرئيسية", "رئيسية"]:
            reply_message(reply_token, UI.main_menu(user, db))
        elif normalized in ["العاب", "الالعاب"]:
            reply_message(reply_token, UI.games_list(user['theme']))
        elif normalized in ["نقاطي", "احصائياتي", "احصائيات", "نقاط"]:
            reply_message(reply_token, UI.user_stats(user))
        elif normalized in ["الصداره", "الصدارة", "المتصدرين"]:
            leaders = db.get_leaderboard(10)
            reply_message(reply_token, UI.leaderboard(leaders, user['theme']))
        elif normalized in ["انجازات", "انجازاتي", "الانجازات"]:
            user_achievements = db.get_user_achievements(user_id)
            reply_message(reply_token, UI.achievements_list(user_achievements, user['theme']))
        elif normalized in ["مكافأة", "مكافاه", "جائزة", "يومية"]:
            if db.claim_reward(user_id):
                reply_message(reply_token, UI.text_message(f"تم! حصلت على +{Config.DAILY_REWARD_POINTS} نقطة"))
            else:
                reply_message(reply_token, UI.text_message(f"يمكنك الحصول على المكافأة كل {Config.DAILY_REWARD_HOURS} ساعة"))
        elif normalized in ["تغيير", "تغير", "غير"]:
            db.set_changing_name(user_id)
            reply_message(reply_token, UI.text_message("اكتب اسمك الجديد:"))
        elif normalized in ["ثيم", "ثم", "المظهر"]:
            current_theme = user.get('theme', 'light')
            new_theme = 'dark' if current_theme == 'light' else 'light'
            db.change_theme(user_id, new_theme)
            theme_name = "داكن" if new_theme == 'dark' else "فاتح"
            reply_message(reply_token, UI.text_message(f"تم تغيير الثيم الى: {theme_name}"))
        elif normalized in ["انسحب", "انسحاب", "حذف", "مسح"]:
            db.withdraw_user(user_id)
            db.clear_game_progress(user_id)
            reply_message(reply_token, UI.text_message("تم الانسحاب. يمكنك العودة بكتابة: تسجيل"))
        elif normalized in ["مساعده", "مساعدة", "ساعدني", "ساعد"]:
            reply_message(reply_token, UI.help_screen(user['theme']))
        elif normalized in game_mgr.game_mappings:
            question = game_mgr.start_game(user_id, normalized, user['theme'])
            if question:
                reply_message(reply_token, question)
            else:
                reply_message(reply_token, UI.text_message("حدث خطأ في بدء اللعبة"))
        elif normalized in text_mgr.cmd_mapping:
            content = text_mgr.get_content(normalized)
            if content:
                reply_message(reply_token, UI.text_message(content))
        else:
            reply_message(reply_token, UI.text_message("امر غير معروف. اكتب مساعدة لعرض الاوامر"))
    
    except Exception as e:
        logger.exception(f"Processing error: {e}")
        reply_message(reply_token, UI.text_message("حدث خطأ. حاول مرة اخرى"))

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    
    return "OK", 200

@handler.add(MessageEvent, message=TextMessageContent)
def on_message(event):
    executor.submit(process_message, event.source.user_id, event.message.text, event.reply_token)

@app.route("/health")
def health():
    return jsonify({"status": "healthy", "timestamp": datetime.utcnow().isoformat()})

@app.route("/")
def index():
    return "Bot Mesh - Running"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=Config.PORT, debug=(Config.ENV == "development"))
