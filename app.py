from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    QuickReply, QuickReplyButton, MessageAction,
)
import os
from datetime import datetime, timedelta
import sqlite3
from collections import defaultdict
import threading
import time
import re

# استيراد الألعاب
from games.iq_game import IQGame
from games.word_color_game import WordColorGame
from games.chain_words_game import ChainWordsGame
from games.scramble_word_game import ScrambleWordGame
from games.letters_words_game import LettersWordsGame
from games.fast_typing_game import FastTypingGame
from games.human_animal_plant_game import HumanAnimalPlantGame
from games.guess_game import GuessGame
from games.compatibility_game import CompatibilityGame
from games.math_game import MathGame
from games.memory_game import MemoryGame
from games.riddle_game import RiddleGame
from games.opposite_game import OppositeGame
from games.emoji_game import EmojiGame
from games.song_game import SongGame

app = Flask(__name__)

# إعدادات LINE Bot
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', 'YOUR_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET', 'YOUR_CHANNEL_SECRET')

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# مفاتيح Gemini AI
GEMINI_API_KEYS = [
    os.getenv('GEMINI_API_KEY_1', ''),
    os.getenv('GEMINI_API_KEY_2', ''),
    os.getenv('GEMINI_API_KEY_3', '')
]
GEMINI_API_KEYS = [key for key in GEMINI_API_KEYS if key]
current_gemini_key_index = 0
USE_AI = bool(GEMINI_API_KEYS)

def get_gemini_api_key():
    global current_gemini_key_index
    if GEMINI_API_KEYS:
        return GEMINI_API_KEYS[current_gemini_key_index]
    return None

def switch_gemini_key():
    global current_gemini_key_index
    if len(GEMINI_API_KEYS) > 1:
        current_gemini_key_index = (current_gemini_key_index + 1) % len(GEMINI_API_KEYS)
        return True
    return False

active_games = {}
registered_players = set()
user_message_count = defaultdict(lambda: {'count': 0, 'reset_time': datetime.now()})

def normalize_text(text):
    text = text.strip().lower()
    text = re.sub(r'^ال', '', text)
    text = text.replace('أ', 'ا').replace('إ', 'ا').replace('آ', 'ا')
    text = text.replace('ة', 'ه').replace('ى', 'ي')
    text = re.sub(r'[\u064B-\u065F]', '', text)
    return text

# قاعدة البيانات
def init_db():
    conn = sqlite3.connect('game_scores.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (user_id TEXT PRIMARY KEY, 
                  display_name TEXT,
                  total_points INTEGER DEFAULT 0,
                  games_played INTEGER DEFAULT 0,
                  wins INTEGER DEFAULT 0,
                  last_played TEXT)''')
    conn.commit()
    conn.close()

init_db()

def update_user_points(user_id, display_name, points, won=False):
    conn = sqlite3.connect('game_scores.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = c.fetchone()
    if user:
        new_points = user[2] + points
        new_games = user[3] + 1
        new_wins = user[4] + (1 if won else 0)
        c.execute('''UPDATE users SET total_points = ?, games_played = ?, wins = ?, 
                     last_played = ?, display_name = ? WHERE user_id = ?''',
                  (new_points, new_games, new_wins, datetime.now().isoformat(), display_name, user_id))
    else:
        c.execute('''INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)''',
                  (user_id, display_name, points, 1, 1 if won else 0, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_leaderboard():
    conn = sqlite3.connect('game_scores.db')
    c = conn.cursor()
    c.execute('SELECT display_name, total_points, games_played, wins FROM users ORDER BY total_points DESC LIMIT 10')
    leaders = c.fetchall()
    conn.close()
    return leaders

# معدل الرسائل
def check_rate_limit(user_id):
    now = datetime.now()
    user_data = user_message_count[user_id]
    if now - user_data['reset_time'] > timedelta(minutes=1):
        user_data['count'] = 0
        user_data['reset_time'] = now
    if user_data['count'] >= 20:
        return False
    user_data['count'] += 1
    return True

# تنظيف الألعاب القديمة
def cleanup_old_games():
    while True:
        time.sleep(300)
        now = datetime.now()
        to_delete = []
        for game_id, game_data in active_games.items():
            if now - game_data.get('created_at', now) > timedelta(minutes=5):
                to_delete.append(game_id)
        for game_id in to_delete:
            del active_games[game_id]

threading.Thread(target=cleanup_old_games, daemon=True).start()

# القوائم السريعة
def get_quick_reply():
    return QuickReply(items=[
        QuickReplyButton(action=MessageAction(label="🎮 انضم", text="انضم")),
        QuickReplyButton(action=MessageAction(label="⚡ أسرع", text="أسرع")),
        QuickReplyButton(action=MessageAction(label="🧠 ذكاء", text="ذكاء")),
        QuickReplyButton(action=MessageAction(label="🎨 لون", text="كلمة ولون")),
        QuickReplyButton(action=MessageAction(label="🎵 أغنية", text="أغنية")),
        QuickReplyButton(action=MessageAction(label="🔗 سلسلة", text="سلسلة")),
        QuickReplyButton(action=MessageAction(label="🧩 ترتيب", text="ترتيب الحروف")),
        QuickReplyButton(action=MessageAction(label="🎯 خمن", text="خمن")),
        QuickReplyButton(action=MessageAction(label="❓ لغز", text="لغز")),
        QuickReplyButton(action=MessageAction(label="🏆 الصدارة", text="الصدارة"))
    ])

def get_more_quick_reply():
    return QuickReply(items=[
        QuickReplyButton(action=MessageAction(label="➕ رياضيات", text="رياضيات")),
        QuickReplyButton(action=MessageAction(label="😀 إيموجي", text="إيموجي")),
        QuickReplyButton(action=MessageAction(label="💖 توافق", text="توافق")),
        QuickReplyButton(action=MessageAction(label="🧠 ذاكرة", text="ذاكرة")),
        QuickReplyButton(action=MessageAction(label="🔄 ضد", text="ضد")),
    ])

# نقطة البداية
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    text = event.message.text.strip()

    if not check_rate_limit(user_id):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="⚠️ أرسل رسائل كثيرة بسرعة! انتظر قليلاً.")
        )
        return

    # ✅ إصلاح اسم المستخدم
    display_name = "لاعب"
    try:
        profile = line_bot_api.get_profile(user_id)
        if profile and getattr(profile, "display_name", None):
            display_name = profile.display_name
    except Exception:
        display_name = f"مشارك-{user_id[-4:]}"

    game_id = getattr(event.source, 'group_id', user_id)

    # ✅ أمر جاوب
    if text in ['جاوب', 'الجواب', 'الاجابة', 'الإجابة']:
        if game_id in active_games:
            game_data = active_games[game_id]
            game = game_data['game']
            if hasattr(game, 'show_answer'):
                answer_text = game.show_answer()
                if isinstance(answer_text, str):
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(
                            text=f"✅ الإجابة الصحيحة:\n{answer_text}",
                            quick_reply=get_quick_reply()
                        )
                    )
                else:
                    line_bot_api.reply_message(event.reply_token, answer_text)
            else:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(
                        text="❌ هذه اللعبة لا تدعم عرض الإجابة",
                        quick_reply=get_quick_reply()
                    )
                )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(
                    text="❌ لا توجد لعبة نشطة\n\n🎮 ابدأ لعبة جديدة أولاً",
                    quick_reply=get_quick_reply()
                )
            )
        return

    # 📍 أوامر الألعاب
    games = {
        "ذكاء": IQGame,
        "كلمة ولون": WordColorGame,
        "سلسلة": ChainWordsGame,
        "ترتيب الحروف": ScrambleWordGame,
        "تكوين كلمات": LettersWordsGame,
        "أسرع": FastTypingGame,
        "إنسان حيوان نبات": HumanAnimalPlantGame,
        "خمن": GuessGame,
        "توافق": CompatibilityGame,
        "رياضيات": MathGame,
        "ذاكرة": MemoryGame,
        "لغز": RiddleGame,
        "ضد": OppositeGame,
        "إيموجي": EmojiGame,
        "أغنية": SongGame
    }

    if text in games:
        game_class = games[text]
        game = game_class(line_bot_api, USE_AI, get_gemini_api_key, switch_gemini_key)
        active_games[game_id] = {"game": game, "created_at": datetime.now()}
        response = game.start(display_name)
        line_bot_api.reply_message(event.reply_token, response)
        return

    # 📈 الصدارة
    if text in ["الصدارة", "الترتيب"]:
        leaders = get_leaderboard()
        if leaders:
            msg = "🏆 أعلى اللاعبين:\n\n"
            for i, (name, pts, games, wins) in enumerate(leaders, start=1):
                msg += f"{i}. {name} - {pts} نقطة ({wins} فوز)\n"
        else:
            msg = "لا توجد نتائج بعد!"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=msg, quick_reply=get_quick_reply()))
        return

    # 📌 أوامر عامة
    if text in ["انضم", "ابدأ"]:
        registered_players.add(user_id)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"✅ تم انضمامك يا {display_name}! اختر لعبة من القائمة 👇", quick_reply=get_quick_reply())
        )
        return

    if text in ["انسحب", "خروج"]:
        registered_players.discard(user_id)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="🚪 تم انسحابك من اللعبة.", quick_reply=get_quick_reply()))
        return

    if text in ["الألعاب", "الكل"]:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="🎮 كل الألعاب المتاحة:", quick_reply=get_more_quick_reply()))
        return

    # أي رد آخر يعالج كإجابة على اللعبة الحالية
    if game_id in active_games:
        game_data = active_games[game_id]
        game = game_data['game']
        response = game.check_answer(user_id, display_name, text)
        if response:
            line_bot_api.reply_message(event.reply_token, response)
        return

    # رد افتراضي
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="👋 أهلاً! اكتب 'انضم' للبدء بالألعاب 🎮", quick_reply=get_quick_reply())
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
