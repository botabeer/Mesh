"""
Bot Mesh v7.0 - Production Ready
تم إنشاء هذا البوت بواسطة عبير الدوسري © 2025
"""

import os
import sys
import logging
from datetime import datetime, timedelta
from collections import defaultdict
from threading import Lock
import traceback

from flask import Flask, request, abort
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi,
    ReplyMessageRequest, TextMessage
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent

from config import Config
from ui import UI
from game_loader import GameLoader

# =====================================================
# إعداد التطبيق
# =====================================================

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

configuration = Configuration(access_token=Config.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(Config.LINE_CHANNEL_SECRET)

ui = UI()
game_loader = GameLoader()

# =====================================================
# بيانات المستخدمين
# =====================================================

users_data = defaultdict(lambda: {
    'name': 'مستخدم',
    'points': 0,
    'games_played': 0,
    'wins': 0,
    'theme': 'ابيض',
    'last_activity': datetime.now()
})

active_games = {}

users_lock = Lock()
games_lock = Lock()

rate_limiter = defaultdict(list)
rate_lock = Lock()

# =====================================================
# أدوات مساعدة
# =====================================================

def check_rate_limit(user_id: str) -> bool:
    with rate_lock:
        now = datetime.now()
        cutoff = now - timedelta(seconds=60)

        rate_limiter[user_id] = [
            t for t in rate_limiter[user_id] if t > cutoff
        ]

        if len(rate_limiter[user_id]) >= Config.MAX_MESSAGES_PER_MINUTE:
            return False

        rate_limiter[user_id].append(now)
        return True


def normalize_text(text: str) -> str:
    import re
    text = text.strip().lower()

    replacements = {
        'أ': 'ا', 'إ': 'ا', 'آ': 'ا',
        'ى': 'ي', 'ة': 'ه', 'ؤ': 'و', 'ئ': 'ي'
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    return re.sub(r'[\u064B-\u065F\u0670]', '', text)


def cleanup_expired_games():
    with games_lock:
        expired = []
        for user_id, game in active_games.items():
            if hasattr(game, 'is_expired') and game.is_expired(10):
                expired.append(user_id)

        for user_id in expired:
            del active_games[user_id]

# =====================================================
# Webhook
# =====================================================

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers.get('X-Line-Signature')
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    except Exception:
        logger.error(traceback.format_exc())
        abort(500)

    return "OK"

# =====================================================
# معالج الرسائل
# =====================================================

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    user_id = event.source.user_id
    text = event.message.text.strip()

    if not check_rate_limit(user_id):
        return

    try:
        with ApiClient(configuration) as api_client:
            line_api = MessagingApi(api_client)
            normalized = normalize_text(text)

            with users_lock:
                user_data = users_data[user_id]
                username = user_data['name']
                theme = user_data['theme']

            response = None

            # -----------------------------
            # الصفحة الرئيسية
            # -----------------------------
            if normalized in ['بدايه', 'ابدا', 'البدايه']:
                response = ui.build_home(username, user_data['points'], theme)

            # -----------------------------
            # قائمة الألعاب
            # -----------------------------
            elif normalized in ['العاب']:
                response = ui.build_games_menu(theme)

            # -----------------------------
            # نقاط المستخدم
            # -----------------------------
            elif normalized in ['نقاطي']:
                rank = 1
                with users_lock:
                    all_users = sorted(
                        users_data.values(),
                        key=lambda x: x['points'],
                        reverse=True
                    )
                    for i, u in enumerate(all_users, 1):
                        if u is user_data:
                            rank = i
                            break

                response = ui.build_user_stats(username, user_data, rank, theme)

            # -----------------------------
            # لوحة الصدارة
            # -----------------------------
            elif normalized in ['صداره', 'الصدارة']:
                with users_lock:
                    leaderboard = sorted(
                        users_data.values(),
                        key=lambda x: x['points'],
                        reverse=True
                    )[:10]

                display = [
                    {
                        'name': u['name'],
                        'points': u['points']
                    } for u in leaderboard
                ]

                response = ui.build_leaderboard(display, theme)

            # -----------------------------
            # تغيير الثيم
            # -----------------------------
            elif text.startswith('ثيم '):
                new_theme = text.replace('ثيم ', '').strip()

                if new_theme in ui.THEMES:
                    with users_lock:
                        users_data[user_id]['theme'] = new_theme
                        theme = new_theme

                    response = ui.build_home(username, user_data['points'], theme)
                else:
                    response = TextMessage(text="الثيم غير موجود")

            # -----------------------------
            # بدء لعبة
            # -----------------------------
            elif normalized.startswith('لعبة '):
                game_name = text.replace('لعبة ', '').strip()

                with games_lock:
                    active_games.pop(user_id, None)

                game = game_loader.create_game(game_name)

                if not game:
                    response = TextMessage(text="اللعبة غير موجودة")
                else:
                    with games_lock:
                        active_games[user_id] = game

                    game.start()
                    q = game.get_question()

                    response = ui.build_game_question(
                        game.name,
                        q['text'],
                        q['round'],
                        q['total_rounds'],
                        theme
                    )

            # -----------------------------
            # إجابة داخل لعبة
            # -----------------------------
            elif user_id in active_games:
                game = active_games[user_id]
                result = game.check_answer(text, user_id, username)

                if result.get('game_over'):
                    with games_lock:
                        active_games.pop(user_id, None)

                    points = result.get('points', 0)

                    with users_lock:
                        users_data[user_id]['points'] += points
                        users_data[user_id]['games_played'] += 1
                        if points > 0:
                            users_data[user_id]['wins'] += 1

                    response = ui.build_game_result(
                        game.name,
                        points,
                        theme
                    )

                else:
                    q = result.get('next_question')
                    response = ui.build_game_question(
                        game.name,
                        q['text'],
                        q['round'],
                        q['total_rounds'],
                        theme
                    )

            # -----------------------------
            # رسالة افتراضية
            # -----------------------------
            else:
                response = TextMessage(
                    text="اكتب بداية للبدء أو العاب لعرض قائمة الألعاب"
                )

            if response:
                line_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[response]
                    )
                )

    except Exception:
        logger.error(traceback.format_exc())


# =====================================================
# تنظيف دوري
# =====================================================

@app.before_request
def before_request():
    cleanup_expired_games()

# =====================================================
# تشغيل التطبيق
# =====================================================

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)
