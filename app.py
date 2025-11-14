from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage
import os
from datetime import datetime
from collections import defaultdict
import threading
import logging

# استيراد الوظائف المساعدة
from utils.helpers import get_user_profile_safe, normalize_text, check_rate_limit, cleanup_old_games
from utils.database import init_db, update_user_points, get_user_stats, get_leaderboard
from utils.ui_components import (
    get_quick_reply, get_more_quick_reply, get_winner_announcement,
    get_help_message, get_welcome_message, get_stats_message,
    get_leaderboard_message, get_join_message
)
from utils.gemini_config import get_gemini_api_key, switch_gemini_key, USE_AI

# استيراد جميع الألعاب (15 لعبة)
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

# إعداد السجلات
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

# إعدادات LINE Bot
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', 'YOUR_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET', 'YOUR_CHANNEL_SECRET')

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# تخزين البيانات
active_games = {}
registered_players = set()
user_message_count = defaultdict(lambda: {'count': 0, 'reset_time': datetime.now()})

# أقفال thread-safe
games_lock = threading.Lock()
players_lock = threading.Lock()

# تهيئة قاعدة البيانات
init_db()

# بدء خيط التنظيف
cleanup_thread = threading.Thread(
    target=cleanup_old_games,
    args=(active_games, games_lock),
    daemon=True
)
cleanup_thread.start()

# خريطة الألعاب المتاحة (15 لعبة)
GAMES_MAP = {
    'ذكاء': (IQGame, 'ذكاء'),
    'كلمة ولون': (WordColorGame, 'كلمة ولون'),
    'لون': (WordColorGame, 'كلمة ولون'),
    'سلسلة': (ChainWordsGame, 'سلسلة'),
    'ترتيب الحروف': (ScrambleWordGame, 'ترتيب'),
    'ترتيب': (ScrambleWordGame, 'ترتيب'),
    'تكوين كلمات': (LettersWordsGame, 'تكوين'),
    'تكوين': (LettersWordsGame, 'تكوين'),
    'أسرع': (FastTypingGame, 'أسرع'),
    'لعبة': (HumanAnimalPlantGame, 'لعبة'),
    'خمن': (GuessGame, 'خمن'),
    'توافق': (CompatibilityGame, 'توافق'),
    'رياضيات': (MathGame, 'رياضيات'),
    'ذاكرة': (MemoryGame, 'ذاكرة'),
    'لغز': (RiddleGame, 'لغز'),
    'ضد': (OppositeGame, 'ضد'),
    'إيموجي': (EmojiGame, 'إيموجي'),
    'أغنية': (SongGame, 'أغنية')
}

def start_game(game_id, game_class, game_type, user_id, event):
    """بدء لعبة جديدة"""
    try:
        with games_lock:
            # الألعاب التي تدعم AI
            if game_class in [IQGame, WordColorGame, LettersWordsGame, HumanAnimalPlantGame, SongGame]:
                game = game_class(
                    line_bot_api,
                    use_ai=USE_AI,
                    get_api_key=get_gemini_api_key,
                    switch_key=switch_gemini_key
                )
            else:
                game = game_class(line_bot_api)
            
            with players_lock:
                participants = registered_players.copy()
                participants.add(user_id)
            
            active_games[game_id] = {
                'game': game,
                'type': game_type,
                'created_at': datetime.now(),
                'participants': participants,
                'question_count': 0,
                'max_questions': 5,
                'player_scores': defaultdict(int),
                'answered_users': set()  # لتتبع من أجاب على السؤال الحالي
            }
        
        response = game.start_game()
        line_bot_api.reply_message(event.reply_token, response)
        logger.info(f"✅ بدأت لعبة {game_type} في {game_id}")
        return True
        
    except Exception as e:
        logger.error(f"❌ خطأ في بدء اللعبة {game_type}: {e}", exc_info=True)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text=f"❌ حدث خطأ في بدء لعبة {game_type}",
                quick_reply=get_quick_reply()
            )
        )
        return False

@app.route("/", methods=['GET'])
def home():
    """الصفحة الرئيسية الأنيقة"""
    return f"""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>تم إنشاء هذا البوت بواسطة عبير الدوسري- LINE Game Bot</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }}
            .container {{
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                max-width: 600px;
                width: 100%;
                overflow: hidden;
            }}
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 40px 30px;
                text-align: center;
            }}
            .header h1 {{
                font-size: 2.5em;
                margin-bottom: 10px;
            }}
            .header p {{
                font-size: 1.1em;
                opacity: 0.9;
            }}
            .content {{
                padding: 40px 30px;
            }}
            .status-card {{
                background: #f8f9fa;
                border-radius: 12px;
                padding: 20px;
                margin-bottom: 20px;
                border-left: 4px solid #667eea;
            }}
            .status-card h3 {{
                color: #333;
                margin-bottom: 15px;
                font-size: 1.2em;
            }}
            .stat {{
                display: flex;
                justify-content: space-between;
                padding: 10px 0;
                border-bottom: 1px solid #e0e0e0;
            }}
            .stat:last-child {{
                border-bottom: none;
            }}
            .stat-label {{
                color: #666;
            }}
            .stat-value {{
                color: #667eea;
                font-weight: bold;
            }}
            .games-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
                gap: 10px;
                margin-top: 20px;
            }}
            .game-chip {{
                background: white;
                border: 2px solid #667eea;
                color: #667eea;
                padding: 8px 12px;
                border-radius: 20px;
                text-align: center;
                font-size: 0.9em;
                font-weight: 500;
            }}
            .footer {{
                background: #f8f9fa;
                padding: 20px;
                text-align: center;
                color: #666;
                font-size: 0.9em;
            }}
            .status-indicator {{
                display: inline-block;
                width: 10px;
                height: 10px;
                background: #4caf50;
                border-radius: 50%;
                margin-left: 10px;
                animation: pulse 2s infinite;
            }}
            @keyframes pulse {{
                0%, 100% {{ opacity: 1; }}
                50% {{ opacity: 0.5; }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Mesh</h1>
                <p>نظام ألعاب LINE Bot تفاعلي</p>
            </div>
            
            <div class="content">
                <div class="status-card">
                    <h3>
                        <span class="status-indicator"></span>
                        حالة الخادم
                    </h3>
                    <div class="stat">
                        <span class="stat-label">▪️ الحالة</span>
                        <span class="stat-value">✅ يعمل بنجاح</span>
                    </div>
                    <div class="stat">
                        <span class="stat-label">▪️ اللاعبون المسجلون</span>
                        <span class="stat-value">{len(registered_players)}</span>
                    </div>
                    <div class="stat">
                        <span class="stat-label">▪️ الألعاب النشطة</span>
                        <span class="stat-value">{len(active_games)}</span>
                    </div>
                    <div class="stat">
                        <span class="stat-label">▪️ عدد الألعاب المتاحة</span>
                        <span class="stat-value">15 لعبة</span>
                    </div>
                </div>

                <div class="status-card">
                    <h3>🎮 الألعاب المتاحة</h3>
                    <div class="games-grid">
                        <div class="game-chip">ذكاء</div>
                        <div class="game-chip">كلمة ولون</div>
                        <div class="game-chip">سلسلة</div>
                        <div class="game-chip">ترتيب</div>
                        <div class="game-chip">تكوين</div>
                        <div class="game-chip">أسرع</div>
                        <div class="game-chip">لعبة</div>
                        <div class="game-chip">خمن</div>
                        <div class="game-chip">توافق</div>
                        <div class="game-chip">رياضيات</div>
                        <div class="game-chip">ذاكرة</div>
                        <div class="game-chip">لغز</div>
                        <div class="game-chip">ضد</div>
                        <div class="game-chip">إيموجي</div>
                        <div class="game-chip">أغنية</div>
                    </div>
                </div>
            </div>

            <div class="footer">
                <p>⚡ Powered by Flask & LINE Messaging API</p>
                <p style="margin-top: 10px; font-size: 0.8em;">© Bot Mesh </p>
            </div>
        </div>
    </body>
    </html>
    """

@app.route("/health", methods=['GET'])
def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "active_games": len(active_games),
        "registered_players": len(registered_players),
        "timestamp": datetime.now().isoformat()
    }

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers.get('X-Line-Signature', '')
    body = request.get_data(as_text=True)
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        logger.error("❌ توقيع غير صالح")
        abort(400)
    except Exception as e:
        logger.error(f"❌ خطأ في معالجة webhook: {e}", exc_info=True)
    
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    try:
        user_id = event.source.user_id
        text = event.message.text.strip()
        display_name = get_user_profile_safe(user_id, line_bot_api)
        game_id = event.source.group_id if hasattr(event.source, 'group_id') else user_id
        
        logger.info(f"📩 {display_name}: {text}")
        
        # فحص حد المعدل
        if not check_rate_limit(user_id, user_message_count):
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(
                    text="⚠️ عدد كبير من الرسائل! انتظر دقيقة.",
                    quick_reply=get_quick_reply()
                )
            )
            return
        
        # === أوامر البداية والترحيب ===
        if text in ['البداية', 'ابدأ', 'start', 'قائمة', 'البوت']:
            flex_message = get_welcome_message(display_name)
            line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage(
                    alt_text="مرحباً بك",
                    contents=flex_message,
                    quick_reply=get_quick_reply()
                )
            )
            return
        
        # === المزيد من الألعاب ===
        elif text in ['أكثر', 'المزيد', 'more']:
            more_message = {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "ألعاب إضافية",
                            "weight": "bold",
                            "size": "xl",
                            "color": "#1a1a1a",
                            "align": "center"
                        },
                        {
                            "type": "separator",
                            "margin": "lg",
                            "color": "#e8e8e8"
                        },
                        {
                            "type": "text",
                            "text": "اختر من الأزرار أدناه",
                            "size": "sm",
                            "color": "#6a6a6a",
                            "align": "center",
                            "margin": "lg"
                        }
                    ],
                    "backgroundColor": "#ffffff",
                    "paddingAll": "24px"
                },
                "styles": {
                    "body": {
                        "separator": True
                    }
                }
            }
            line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage(
                    alt_text="ألعاب إضافية",
                    contents=more_message,
                    quick_reply=get_more_quick_reply()
                )
            )
            return
        
        # === المساعدة ===
        elif text == 'مساعدة':
            line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage(
                    alt_text="مساعدة",
                    contents=get_help_message(),
                    quick_reply=get_quick_reply()
                )
            )
            return
        
        # === نقاطي ===
        elif text == 'نقاطي':
            stats = get_user_stats(user_id)
            if stats:
                is_registered = user_id in registered_players
                flex_stats = get_stats_message(display_name, stats, is_registered)
                line_bot_api.reply_message(
                    event.reply_token,
                    FlexSendMessage(
                        alt_text="إحصائياتك",
                        contents=flex_stats,
                        quick_reply=get_quick_reply()
                    )
                )
            else:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(
                        text="▫️ لم تلعب أي لعبة بعد\n\nاكتب 'انضم' للتسجيل والبدء",
                        quick_reply=get_quick_reply()
                    )
                )
            return
        
        # === الصدارة ===
        elif text == 'الصدارة':
            leaders = get_leaderboard()
            if leaders:
                flex_leaderboard = get_leaderboard_message(leaders)
                line_bot_api.reply_message(
                    event.reply_token,
                    FlexSendMessage(
                        alt_text="لوحة الصدارة",
                        contents=flex_leaderboard,
                        quick_reply=get_quick_reply()
                    )
                )
            else:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(
                        text="▫️ لا توجد بيانات بعد",
                        quick_reply=get_quick_reply()
                    )
                )
            return
        
        # === إيقاف اللعبة ===
        elif text in ['إيقاف', 'ايقاف', 'stop']:
            with games_lock:
                if game_id in active_games:
                    game_type = active_games[game_id]['type']
                    del active_games[game_id]
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(
                            text=f"⏹️ تم إيقاف لعبة {game_type}",
                            quick_reply=get_quick_reply()
                        )
                    )
                else:
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(
                            text="▫️ لا توجد لعبة نشطة",
                            quick_reply=get_quick_reply()
                        )
                    )
            return
        
        # === الانضمام ===
        elif text in ['انضم', 'تسجيل', 'join']:
            with players_lock:
                if user_id in registered_players:
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(
                            text=f"▪️ أنت مسجل بالفعل يا {display_name}\n\nيمكنك اللعب في جميع الألعاب",
                            quick_reply=get_quick_reply()
                        )
                    )
                else:
                    registered_players.add(user_id)
                    with games_lock:
                        for gid, game_data in active_games.items():
                            if 'participants' not in game_data:
                                game_data['participants'] = set()
                            game_data['participants'].add(user_id)
                    
                    join_message = get_join_message(display_name)
                    line_bot_api.reply_message(
                        event.reply_token,
                        FlexSendMessage(
                            alt_text="تم التسجيل",
                            contents=join_message,
                            quick_reply=get_quick_reply()
                        )
                    )
                    logger.info(f"✅ انضم لاعب جديد: {display_name}")
            return
        
        # === الانسحاب ===
        elif text in ['انسحب', 'خروج', 'leave']:
            with players_lock:
                if user_id in registered_players:
                    registered_players.remove(user_id)
                    with games_lock:
                        for gid, game_data in active_games.items():
                            if 'participants' in game_data and user_id in game_data['participants']:
                                game_data['participants'].remove(user_id)
                    
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(
                            text=f"▫️ تم انسحابك يا {display_name}\n\nيمكنك الانضمام مرة أخرى بكتابة 'انضم'",
                            quick_reply=get_quick_reply()
                        )
                    )
                    logger.info(f"❌ انسحب لاعب: {display_name}")
                else:
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(
                            text="▫️ أنت غير مسجل\n\nاكتب 'انضم' للتسجيل",
                            quick_reply=get_quick_reply()
                        )
                    )
            return
        
        # === بدء الألعاب ===
        if text in GAMES_MAP:
            game_class, game_type = GAMES_MAP[text]
            start_game(game_id, game_class, game_type, user_id, event)
            return
        
        # === معالجة إجابات الألعاب النشطة ===
        if game_id in active_games:
            game_data = active_games[game_id]
            
            # التحقق من التسجيل
            with players_lock:
                is_registered = user_id in registered_players
            
            if not is_registered and 'participants' in game_data and user_id not in game_data['participants']:
                return
            
            # التحقق من أن اللاعب لم يجب على السؤال الحالي
            if user_id in game_data.get('answered_users', set()):
                return  # تجاهل الإجابات المتكررة من نفس اللاعب
            
            game = game_data['game']
            game_type = game_data['type']
            
            try:
                # معالجة أمر "لمح"
                if normalize_text(text) in ['لمح', 'تلميح', 'hint']:
                    if hasattr(game, 'get_hint'):
                        hint_result = game.get_hint()
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(
                                text=hint_result,
                                quick_reply=get_quick_reply()
                            )
                        )
                    return
                
                # معالجة أمر "جاوب"
                if normalize_text(text) in ['جاوب', 'الجواب', 'answer']:
                    if hasattr(game, 'reveal_answer'):
                        answer_result = game.reveal_answer()
                        
                        # الانتقال للسؤال التالي
                        game_data['question_count'] += 1
                        game_data['answered_users'] = set()  # إعادة تعيين
                        
                        if game_data['question_count'] >= game_data['max_questions']:
                            # انتهت اللعبة
                            if game_data['player_scores']:
                                winner_id = max(game_data['player_scores'], key=game_data['player_scores'].get)
                                winner_points = game_data['player_scores'][winner_id]
                                winner_name = get_user_profile_safe(winner_id, line_bot_api)
                                
                                winner_flex = get_winner_announcement(
                                    winner_name,
                                    winner_points,
                                    game_type,
                                    game_data['max_questions']
                                )
                                
                                with games_lock:
                                    if game_id in active_games:
                                        del active_games[game_id]
                                
                                line_bot_api.reply_message(
                                    event.reply_token,
                                    FlexSendMessage(
                                        alt_text=f"🏆 {winner_name} فاز!",
                                        contents=winner_flex,
                                        quick_reply=get_quick_reply()
                                    )
                                )
                            else:
                                with games_lock:
                                    if game_id in active_games:
                                        del active_games[game_id]
                                
                                line_bot_api.reply_message(
                                    event.reply_token,
                                    TextSendMessage(
                                        text=f"⏹️ انتهت لعبة {game_type}\n\nجرب لعبة أخرى!",
                                        quick_reply=get_quick_reply()
                                    )
                                )
                            return
                        else:
                            # سؤال جديد
                            next_question = game.start_game()
                            if isinstance(next_question, TextSendMessage):
                                next_question.text = f"{answer_result}\n\n{next_question.text}\n\n📊 السؤال {game_data['question_count']}/{game_data['max_questions']}"
                                next_question.quick_reply = get_quick_reply()
                            
                            line_bot_api.reply_message(event.reply_token, next_question)
                            return
                    return
                
                # فحص الإجابة
                result = game.check_answer(text, user_id, display_name)
                
                if result:
                    points = result.get('points', 0)
                    
                    # إضافة اللاعب إلى قائمة من أجابوا
                    game_data['answered_users'].add(user_id)
                    
                    # تحديث النقاط
                    if points > 0:
                        game_data['player_scores'][user_id] += points
                        game_data['question_count'] += 1
                        game_data['answered_users'] = set()  # إعادة تعيين للسؤال التالي
                        
                        update_user_points(
                            user_id,
                            display_name,
                            points,
                            result.get('won', False),
                            game_type
                        )
                        logger.info(f"✅ {display_name} حصل على {points} نقطة في {game_type}")
                    
                    # فحص إذا انتهت الأسئلة
                    if game_data['question_count'] >= game_data['max_questions']:
                        if game_data['player_scores']:
                            winner_id = max(game_data['player_scores'], key=game_data['player_scores'].get)
                            winner_points = game_data['player_scores'][winner_id]
                            winner_name = get_user_profile_safe(winner_id, line_bot_api)
                            
                            winner_flex = get_winner_announcement(
                                winner_name,
                                winner_points,
                                game_type,
                                game_data['max_questions']
                            )
                            
                            with games_lock:
                                if game_id in active_games:
                                    del active_games[game_id]
                            
                            line_bot_api.reply_message(
                                event.reply_token,
                                FlexSendMessage(
                                    alt_text=f"🏆 {winner_name} فاز!",
                                    contents=winner_flex,
                                    quick_reply=get_quick_reply()
                                )
                            )
                        else:
                            with games_lock:
                                if game_id in active_games:
                                    del active_games[game_id]
                            
                            line_bot_api.reply_message(
                                event.reply_token,
                                TextSendMessage(
                                    text=f"⏹️ انتهت لعبة {game_type}\n\nجرب لعبة أخرى!",
                                    quick_reply=get_quick_reply()
                                )
                            )
                        return
                    
                    # إذا لم تنته اللعبة بعد
                    if result.get('game_over', False):
                        with games_lock:
                            if game_id in active_games:
                                del active_games[game_id]
                        response = TextSendMessage(
                            text=result.get('message', 'انتهت اللعبة'),
                            quick_reply=get_quick_reply()
                        )
                    else:
                        response = result.get('response', TextSendMessage(text=result.get('message', '')))
                        
                        if isinstance(response, TextSendMessage):
                            if hasattr(response, 'text'):
                                response.text += f"\n\n📊 السؤال {game_data['question_count']}/{game_data['max_questions']}"
                            response.quick_reply = get_quick_reply()
                    
                    line_bot_api.reply_message(event.reply_token, response)
                return
                
            except Exception as e:
                logger.error(f"❌ خطأ في معالجة إجابة اللعبة: {e}", exc_info=True)
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(
                        text="❌ حدث خطأ. حاول مرة أخرى.",
                        quick_reply=get_quick_reply()
                    )
                )
                return
        
        # === رسالة افتراضية للرسائل غير المعروفة ===
        else:
            logger.info(f"❓ رسالة غير معروفة من {display_name}: {text}")
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(
                    text="❓ أمر غير معروف\n\n▪️ اكتب 'مساعدة' لعرض الأوامر\n▪️ أو 'البداية' للقائمة الرئيسية",
                    quick_reply=get_quick_reply()
                )
            )
    
    except Exception as e:
        logger.error(f"❌ خطأ عام في معالجة الرسالة: {e}", exc_info=True)
        try:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(
                    text="❌ حدث خطأ غير متوقع\n\nحاول مرة أخرى أو اكتب 'مساعدة'"
                )
            )
        except:
            pass

@app.errorhandler(Exception)
def handle_error(error):
    """معالج الأخطاء العام"""
    logger.error(f"❌ خطأ غير متوقع: {error}", exc_info=True)
    return 'Internal Server Error', 500

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    logger.info("=" * 50)
    logger.info(f"🚀 بدء خادم LINE Bot على المنفذ {port}")
    logger.info(f"📊 اللاعبون المسجلون: {len(registered_players)}")
    logger.info(f"🎮 الألعاب النشطة: {len(active_games)}")
    logger.info(f"🎯 عدد الألعاب المتاحة: {len(GAMES_MAP)}")
    logger.info("=" * 50)
    app.run(host='0.0.0.0', port=port, debug=False)
