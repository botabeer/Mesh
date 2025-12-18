import logging
from flask import Flask, request, abort, jsonify
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import Configuration, ApiClient, MessagingApi, ReplyMessageRequest, TextMessage
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import time

from config import Config
from database import Database
from game_manager import GameManager
from text_manager import TextManager
from ui import UI

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
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
    start_time = time.time()
    
    try:
        normalized = Config.normalize(text)
        
        if not db.is_registered(user_id):
            if normalized == "تسجيل":
                db.register_user(user_id, f"لاعب{user_id[-4:]}")
                user = db.get_user(user_id)
                reply_message(reply_token, UI.registration_success(user['name'], user['theme']))
            return
        
        db.update_activity(user_id)
        user = db.get_user(user_id)
        
        if db.is_changing_name(user_id):
            if len(text) < Config.MIN_NAME_LENGTH or len(text) > Config.MAX_NAME_LENGTH:
                reply_message(
                    reply_token,
                    TextMessage(text=f"الاسم يجب ان يكون بين {Config.MIN_NAME_LENGTH} و {Config.MAX_NAME_LENGTH} حرف")
                )
                return
            db.update_name(user_id, text)
            db.clear_changing_name(user_id)
            reply_message(reply_token, TextMessage(text=f"تم تغيير اسمك الى: {text}"))
            return
        
        if db.has_active_game(user_id):
            game = db.get_game_progress(user_id)
            
            if normalized == "لمح" and game.supports_hint:
                hint = game.get_hint()
                if hint:
                    reply_message(reply_token, TextMessage(text=hint))
                return
            
            if normalized == "جاوب" and game.supports_reveal:
                answer = game.reveal_answer()
                if answer:
                    reply_message(reply_token, TextMessage(text=answer))
                return
            
            if normalized == "ايقاف":
                score = game_mgr.stop_game(user_id)
                reply_message(reply_token, TextMessage(text=f"تم ايقاف اللعبة. حصلت على {score} نقطة"))
                return
            
            result, correct = game_mgr.process_answer(user_id, text)
            
            if result and isinstance(result, dict) and result.get("finished"):
                score = result['score']
                total = result['total']
                game_name = result['game_name']
                achievements = result.get('achievements', [])
                
                messages = [UI.game_result(game_name, score, total, user['theme'])]
                
                for achievement in achievements:
                    messages.append(UI.achievement_unlocked(achievement, user['theme']))
                
                reply_message(reply_token, messages)
            elif correct:
                result = game_mgr.next_question(user_id)
                if result:
                    reply_message(reply_token, result)
            return
        
        if normalized in ["بدايه", "بداية", "القائمه", "القائمة"]:
            reply_message(reply_token, UI.main_menu(user, db))
        
        elif normalized == "العاب":
            reply_message(reply_token, UI.games_list(user['theme']))
        
        elif normalized in ["نقاطي", "احصائياتي"]:
            reply_message(reply_token, UI.user_stats(user))
        
        elif normalized in ["الصداره", "الصدارة"]:
            leaders = db.get_leaderboard(10)
            reply_message(reply_token, UI.leaderboard(leaders, user['theme']))
        
        elif normalized == "انجازات":
            user_achievements = db.get_user_achievements(user_id)
            reply_message(reply_token, UI.achievements_list(user_achievements, user['theme']))
        
        elif normalized == "مكافأة":
            if db.claim_reward(user_id):
                reply_message(reply_token, TextMessage(text=f"تم! حصلت على +{Config.DAILY_REWARD_POINTS} نقطة"))
            else:
                reply_message(reply_token, TextMessage(text=f"يمكنك الحصول على المكافأة كل {Config.DAILY_REWARD_HOURS} ساعة"))
        
        elif normalized == "تغيير":
            db.set_changing_name(user_id)
            reply_message(reply_token, TextMessage(text="اكتب اسمك الجديد:"))
        
        elif normalized == "ثيم":
            current_theme = user.get('theme', 'light')
            new_theme = 'dark' if current_theme == 'light' else 'light'
            db.change_theme(user_id, new_theme)
            theme_name = "داكن" if new_theme == 'dark' else "فاتح"
            reply_message(reply_token, TextMessage(text=f"تم تغيير الثيم الى: {theme_name}"))
        
        elif normalized == "انسحب":
            db.withdraw_user(user_id)
            db.clear_game_progress(user_id)
            reply_message(reply_token, TextMessage(text="تم الانسحاب. يمكنك العودة بكتابة: تسجيل"))
        
        elif normalized in ["مساعده", "مساعدة"]:
            reply_message(reply_token, UI.help_screen(user['theme']))
        
        elif normalized in game_mgr.game_mappings:
            question = game_mgr.start_game(user_id, normalized, user['theme'])
            if question:
                reply_message(reply_token, question)
        
        elif normalized in text_mgr.cmd_mapping:
            content = text_mgr.get_content(normalized)
            if content:
                reply_message(reply_token, TextMessage(text=content))
        
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
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "web"
    })

@app.route("/")
def index():
    return "Bot Mesh - Running"

@app.route("/cleanup")
def cleanup():
    try:
        db.cleanup_memory()
        return jsonify({"status": "cleaned", "timestamp": datetime.utcnow().isoformat()})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=Config.PORT, debug=(Config.ENV == "development"))
