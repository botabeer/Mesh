import logging
from flask import Flask, request, abort, jsonify
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent, FollowEvent
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

from config import Config
from database import Database
from game_manager import GameManager
from text_manager import TextManager
from ui import UI

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# التحقق من المتغيرات الاساسية
if not Config.LINE_CHANNEL_ACCESS_TOKEN or not Config.LINE_CHANNEL_SECRET:
    logger.error("Missing LINE credentials")
    raise ValueError("LINE_CHANNEL_ACCESS_TOKEN and LINE_CHANNEL_SECRET are required")

line_config = Configuration(
    access_token=Config.LINE_CHANNEL_ACCESS_TOKEN
)
handler = WebhookHandler(Config.LINE_CHANNEL_SECRET)

db = Database()
game_mgr = GameManager(db)
text_mgr = TextManager()

executor = ThreadPoolExecutor(
    max_workers=Config.WORKERS,
    thread_name_prefix="worker"
)

def reply_message(reply_token, messages):
    if not isinstance(messages, list):
        messages = [messages]

    safe_messages = [m for m in messages if m][:5]

    try:
        with ApiClient(line_config) as client:
            MessagingApi(client).reply_message(
                ReplyMessageRequest(
                    reply_token=reply_token,
                    messages=safe_messages
                )
            )
    except Exception as e:
        logger.error(f"Reply error: {e}")

def process_message(user_id, text, reply_token):
    try:
        normalized = Config.normalize(text)

        # اوامر عامه بدون تسجيل
        if normalized in ["بدايه", "بداية"]:
            if not db.is_registered(user_id):
                reply_message(reply_token, UI.welcome_screen())
            else:
                user = db.get_user(user_id)
                reply_message(reply_token, UI.main_menu(user, db))
            return

        if normalized in ["مساعده", "مساعدة"]:
            theme = "light"
            if db.is_registered(user_id):
                user = db.get_user(user_id)
                theme = user.get("theme", "light")
            reply_message(reply_token, UI.help_screen(theme))
            return

        # محتوى نصي - متاح للجميع
        if normalized in text_mgr.cmd_mapping:
            content = text_mgr.get_content(normalized)
            if content:
                reply_message(reply_token, UI.text_message(content))
            return
        
        # شرح لعبة المافيا
        if normalized == "شرح":
            theme = "light"
            if db.is_registered(user_id):
                user = db.get_user(user_id)
                theme = user.get("theme", "light")
            from games.mafia import MafiaGame
            mafia = MafiaGame(db, theme)
            reply_message(reply_token, mafia.help_screen())
            return

        # لعبه التوافق - متاحة للجميع
        if normalized == "توافق":
            theme = "light"
            if db.is_registered(user_id):
                user = db.get_user(user_id)
                theme = user.get("theme", "light")
            question = game_mgr.start_game(user_id, normalized, theme)
            if question:
                reply_message(reply_token, question)
            return

        # اجابه التوافق
        if db.has_active_game(user_id):
            game = db.get_game_progress(user_id)
            if getattr(game, "game_name", None) == "توافق":
                if game.check_answer(text):
                    reply_message(reply_token, game.current_answer)
                    db.clear_game_progress(user_id)
                else:
                    reply_message(
                        reply_token,
                        UI.text_message("اكتب اسمين بينهما كلمه و\nمثال: اسم و اسم")
                    )
                return

        # تسجيل جديد - يدوي فقط
        if not db.is_registered(user_id):
            if normalized == "تسجيل":
                db.register_user(user_id, f"لاعب{user_id[-4:]}")
                user = db.get_user(user_id)
                reply_message(
                    reply_token,
                    UI.registration_success(user["name"], user["theme"])
                )
            return

        # مستخدم مسجل - الاوامر فقط
        db.update_activity(user_id)
        user = db.get_user(user_id)

        # تغيير الاسم
        if db.is_changing_name(user_id):
            name = text.strip()
            if not name:
                reply_message(reply_token, UI.text_message("الاسم لا يمكن ان يكون فارغ"))
                return
            if len(name) > Config.MAX_NAME_LENGTH:
                reply_message(
                    reply_token,
                    UI.text_message(f"الاسم يجب ان لا يتجاوز {Config.MAX_NAME_LENGTH} حرف")
                )
                return
            db.update_name(user_id, name)
            db.clear_changing_name(user_id)
            reply_message(reply_token, UI.text_message(f"تم تغيير اسمك الى: {name}"))
            return

        # لعبه نشطه
        if db.has_active_game(user_id):
            game = db.get_game_progress(user_id)

            # لعبة المافيا - معالجة خاصة
            if getattr(game, "game_name", None) == "مافيا":
                result = game_mgr.process_answer(user_id, text)
                if result and isinstance(result, tuple):
                    response, correct = result
                    if response:
                        reply_message(reply_token, response)
                return

            # لعبة اسرع - عرض التلميح التلقائي
            if getattr(game, "game_name", None) == "اسرع":
                hint = game.get_hint()
                if hint:
                    result, correct = game_mgr.process_answer(user_id, text)
                    if correct:
                        next_q = game_mgr.next_question(user_id)
                        if next_q:
                            reply_message(reply_token, next_q)
                        else:
                            score = getattr(game, 'score', 0)
                            total = getattr(game, 'total_q', 5)
                            reply_message(
                                reply_token,
                                UI.game_result("اسرع", score, total, user["theme"])
                            )
                    else:
                        reply_message(reply_token, UI.text_message(game.last_error or "خطأ"))
                    return

            # التلميحات والاجابات
            if normalized in ["لمح", "تلميح"] and getattr(game, "supports_hint", False):
                hint = game.get_hint()
                if hint:
                    reply_message(reply_token, UI.text_message(hint))
                return

            if normalized in ["جاوب", "الجواب"] and getattr(game, "supports_reveal", False):
                answer = game.reveal_answer()
                if answer:
                    reply_message(reply_token, UI.text_message(answer))
                return

            if normalized in ["ايقاف", "توقف", "اوقف"]:
                score = game_mgr.stop_game(user_id)
                reply_message(
                    reply_token,
                    UI.text_message(f"تم ايقاف اللعبه. حصلت على {score} نقطه")
                )
                return

            result, correct = game_mgr.process_answer(user_id, text)

            if result and isinstance(result, dict) and result.get("finished"):
                messages = [
                    UI.game_result(
                        result["game_name"],
                        result["score"],
                        result["total"],
                        user["theme"]
                    )
                ]
                for achievement in result.get("achievements", []):
                    messages.append(
                        UI.achievement_unlocked(achievement, user["theme"])
                    )
                reply_message(reply_token, messages)
            elif correct:
                next_q = game_mgr.next_question(user_id)
                if next_q:
                    reply_message(reply_token, next_q)
            else:
                reply_message(reply_token, UI.text_message("اجابه خاطئه، حاول مره اخرى"))
            return

        # اوامر رئيسيه - فقط للمسجلين
        if normalized in ["القائمه", "القائمة", "الرئيسيه", "الرئيسية"]:
            reply_message(reply_token, UI.main_menu(user, db))

        elif normalized in ["العاب", "الالعاب"]:
            reply_message(reply_token, UI.games_list(user["theme"]))

        elif normalized in ["نقاطي", "احصائياتي"]:
            reply_message(reply_token, UI.user_stats(user))

        elif normalized in ["الصداره", "الصدارة"]:
            leaders = db.get_leaderboard(10)
            reply_message(reply_token, UI.leaderboard(leaders, user["theme"]))

        elif normalized in ["انجازات", "انجازاتي"]:
            achievements = db.get_user_achievements(user_id)
            reply_message(
                reply_token,
                UI.achievements_list(achievements, user["theme"])
            )

        elif normalized in ["مكافأه", "مكافاة", "مكافأة", "جائزه", "جائزة"]:
            if db.claim_reward(user_id):
                reply_message(
                    reply_token,
                    UI.text_message(f"تم! حصلت على +{Config.DAILY_REWARD_POINTS} نقطه")
                )
            else:
                reply_message(
                    reply_token,
                    UI.text_message(f"يمكنك الحصول على المكافأه كل {Config.DAILY_REWARD_HOURS} ساعه")
                )

        elif normalized in ["تغيير", "تغير", "غير"]:
            db.set_changing_name(user_id)
            reply_message(reply_token, UI.text_message("اكتب اسمك الجديد:"))

        elif normalized in ["ثيم", "الثيم", "المظهر"]:
            current = user.get("theme", "light")
            new_theme = "dark" if current == "light" else "light"
            db.change_theme(user_id, new_theme)
            reply_message(
                reply_token,
                UI.text_message(f"تم تغيير الثيم الى: {'داكن' if new_theme == 'dark' else 'فاتح'}")
            )

        elif normalized in ["انسحب", "انسحاب", "حذف"]:
            db.withdraw_user(user_id)
            db.clear_game_progress(user_id)
            reply_message(
                reply_token,
                UI.text_message("تم الانسحاب. نقاطك محفوظه، يمكنك العوده بكتابه: تسجيل")
            )

        elif normalized in game_mgr.game_mappings:
            question = game_mgr.start_game(user_id, normalized, user["theme"])
            if question:
                reply_message(reply_token, question)

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
    executor.submit(
        process_message,
        event.source.user_id,
        event.message.text,
        event.reply_token
    )

@handler.add(FollowEvent)
def handle_follow(event):
    user_id = event.source.user_id
    try:
        with ApiClient(line_config) as client:
            api = MessagingApi(client)
            api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[UI.welcome_screen()]
                )
            )
    except Exception as e:
        logger.error(f"Follow event error: {e}")

@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    })

@app.route("/")
def index():
    return "Bot Mesh - Running"

if __name__ == "__main__":
    logger.info(f"Starting on port {Config.PORT}")
    app.run(
        host="0.0.0.0",
        port=Config.PORT,
        debug=(Config.ENV == "development")
    )
