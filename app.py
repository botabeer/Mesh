import logging
from flask import Flask, request, abort, jsonify
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import Configuration, ApiClient, MessagingApi, ReplyMessageRequest, TextMessage
from linebot.v3.webhooks import MessageEvent, TextMessageContent
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import pytz
import time

from config import Config
from database import Database
from game_manager import GameManager
from text_manager import TextManager
from ui import UI

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger(__name__)

app = Flask(__name__)
line_config = Configuration(access_token=Config.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(Config.LINE_CHANNEL_SECRET)

db = Database()
game_mgr = GameManager(db)
text_mgr = TextManager()

executor = ThreadPoolExecutor(max_workers=Config.WORKERS, thread_name_prefix="worker")

scheduler = BackgroundScheduler(timezone=pytz.UTC)
scheduler.add_job(func=lambda: db.cleanup_memory(), trigger="interval", minutes=30)
scheduler.start()

def reply_message(reply_token, messages):
    if not isinstance(messages, list):
        messages = [messages]
    safe_messages = [m for m in messages if m][:5]
    try:
        with ApiClient(line_config) as client:
            MessagingApi(client).reply_message(ReplyMessageRequest(reply_token=reply_token, messages=safe_messages))
    except Exception as e:
        logger.error(f"Reply error: {e}")

def process_message(user_id, text, reply_token):
    start_time = time.time()
    
    try:
        normalized = Config.normalize(text)
        
        # التسجيل الأولي
        if not db.is_registered(user_id):
            db.register_user(user_id, f"لاعب{user_id[-4:]}")
            user = db.get_user(user_id)
            reply_message(reply_token, [
                TextMessage(text=f"مرحبا! تم تسجيلك بنجاح", quickReply=UI.get_quick_reply()),
                UI.main_menu(user, db)
            ])
            return
        
        db.update_activity(user_id)
        user = db.get_user(user_id)
        
        # تغيير الاسم
        if db.is_changing_name(user_id):
            if len(text) < Config.MIN_NAME_LENGTH or len(text) > Config.MAX_NAME_LENGTH:
                reply_message(reply_token, TextMessage(text=f"الاسم يجب ان يكون بين {Config.MIN_NAME_LENGTH} و {Config.MAX_NAME_LENGTH} حرف", quickReply=UI.get_quick_reply()))
                return
            db.update_name(user_id, text)
            db.clear_changing_name(user_id)
            reply_message(reply_token, TextMessage(text=f"تم تغيير اسمك الى: {text}", quickReply=UI.get_quick_reply()))
            return
        
        # إيقاف اللعبة
        if db.has_active_game(user_id) and normalized == "ايقاف":
            score = game_mgr.stop_game(user_id)
            reply_message(reply_token, TextMessage(text=f"تم ايقاف اللعبة. حصلت على {score} نقطة", quickReply=UI.get_quick_reply()))
            return
        
        # اللعب
        if db.has_active_game(user_id):
            result, correct = game_mgr.process_answer(user_id, text)
            
            if result and isinstance(result, dict) and result.get("finished"):
                score = result['score']
                total = result['total']
                game_name = result['game_name']
                achievements = result.get('achievements', [])
                
                status = f"فوز رائع {score}/{total}" if score == total else f"جيد {score}/{total}"
                msg = f"{game_name}\n{status}\nالنقاط: +{score}"
                
                messages = [TextMessage(text=msg, quickReply=UI.get_quick_reply())]
                
                for achievement in achievements:
                    messages.append(UI.achievement_unlocked(achievement, user['theme']))
                
                reply_message(reply_token, messages)
            elif correct:
                result = game_mgr.next_question(user_id)
                if result:
                    reply_message(reply_token, result)
            return
        
        # القوائم والأوامر
        if normalized in ["بدايه", "بداية", "القائمه", "القائمة", "تسجيل"]:
            reply_message(reply_token, UI.main_menu(user, db))
        
        elif normalized == "العاب":
            reply_message(reply_token, UI.games_list(user['theme']))
        
        elif normalized in ["نقاطي", "احصائياتي"]:
            win_rate = (user['wins'] / user['games'] * 100) if user['games'] > 0 else 0
            msg = f"الاسم: {user['name']}\nالنقاط: {user['points']}\nالالعاب: {user['games']}\nالانتصارات: {user['wins']}\nنسبة الفوز: {win_rate:.1f}%\nالسلسلة: {user['streak']}\nافضل سلسلة: {user['best_streak']}"
            reply_message(reply_token, TextMessage(text=msg, quickReply=UI.get_quick_reply()))
        
        elif normalized in ["الصداره", "الصدارة"]:
            leaders = db.get_leaderboard(10)
            reply_message(reply_token, UI.leaderboard(leaders, user['theme']))
        
        elif normalized == "انجازات":
            user_achievements = db.get_user_achievements(user_id)
            reply_message(reply_token, UI.achievements_list(user_achievements, user['theme']))
        
        elif normalized == "مكافأة":
            if db.claim_reward(user_id):
                reply_message(reply_token, TextMessage(text=f"تم! حصلت على +{Config.DAILY_REWARD_POINTS} نقطة", quickReply=UI.get_quick_reply()))
            else:
                reply_message(reply_token, TextMessage(text=f"يمكنك الحصول على المكافأة كل {Config.DAILY_REWARD_HOURS} ساعة", quickReply=UI.get_quick_reply()))
        
        elif normalized == "تغيير":
            db.set_changing_name(user_id)
            reply_message(reply_token, TextMessage(text="اكتب اسمك الجديد:", quickReply=UI.get_quick_reply()))
        
        elif normalized == "ثيم":
            current_theme = user.get('theme', 'light')
            new_theme = 'dark' if current_theme == 'light' else 'light'
            db.change_theme(user_id, new_theme)
            theme_name = "داكن" if new_theme == 'dark' else "فاتح"
            reply_message(reply_token, TextMessage(text=f"تم تغيير الثيم الى: {theme_name}", quickReply=UI.get_quick_reply()))
        
        elif normalized == "انسحب":
            reply_message(reply_token, TextMessage(text="شكرا لاستخدامك البوت!", quickReply=UI.get_quick_reply()))
        
        elif normalized in ["مساعده", "مساعدة"]:
            reply_message(reply_token, UI.help_screen())
        
        elif normalized in game_mgr.game_mappings:
            question = game_mgr.start_game(user_id, normalized, user['theme'])
            if question:
                reply_message(reply_token, question)
        
        elif normalized in text_mgr.cmd_mapping:
            content = text_mgr.get_content(normalized)
            if content:
                reply_message(reply_token, TextMessage(text=content, quickReply=UI.get_quick_reply()))
        
        elapsed = time.time() - start_time
        logger.info(f"Message processed in {elapsed:.2f}s")
    
    except Exception as e:
        logger.exception(f"Processing error: {e}")

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
