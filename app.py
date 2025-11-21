from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage, QuickReply, QuickReplyButton, MessageAction
import logging
from datetime import datetime, timedelta
from collections import defaultdict
import threading
import time

# الاستيراد من الملفات المحلية
from config import *
from database import *
from ui_components import *
from games import *

# إعداد السجلات
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# تهيئة Flask
app = Flask(__name__)

# تهيئة LINE Bot
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# متغيرات عامة
active_games = {}
registered_players = set()
user_message_count = defaultdict(lambda: {'count': 0, 'reset_time': datetime.now()})
games_lock = threading.Lock()
players_lock = threading.Lock()

# تهيئة قاعدة البيانات
init_database()

# الألعاب المتاحة
AVAILABLE_GAMES = {
    'تكوين': (WordFormationGame, 'تكوين الكلمات'),
    'أسرع': (FastTypingGame, 'الكتابة السريعة'),
    'رياضيات': (MathGame, 'الرياضيات'),
    'ترتيب': (ScrambleGame, 'ترتيب الحروف')
}

def check_rate_limit(user_id, max_messages=MAX_MESSAGES_PER_MINUTE, time_window=60):
    """فحص حد الرسائل"""
    now = datetime.now()
    user_data = user_message_count[user_id]
    
    if now - user_data['reset_time'] > timedelta(seconds=time_window):
        user_data['count'] = 0
        user_data['reset_time'] = now
    
    if user_data['count'] >= max_messages:
        return False
    
    user_data['count'] += 1
    return True

def cleanup_old_games():
    """تنظيف الألعاب القديمة"""
    while True:
        try:
            time.sleep(CLEANUP_INTERVAL_SECONDS)
            now = datetime.now()
            to_delete = []
            
            with games_lock:
                for game_id, game_data in active_games.items():
                    if now - game_data.get('created_at', now) > timedelta(minutes=GAME_TIMEOUT_MINUTES):
                        to_delete.append(game_id)
                
                for game_id in to_delete:
                    del active_games[game_id]
                    logger.info(f"🗑️ تم حذف لعبة منتهية: {game_id}")
        
        except Exception as e:
            logger.error(f"❌ خطأ في التنظيف: {e}")

# بدء مؤشر التنظيف
threading.Thread(target=cleanup_old_games, daemon=True).start()

def get_quick_reply():
    """أزرار الرد السريع"""
    return QuickReply(items=[
        QuickReplyButton(action=MessageAction(label="🎮 تكوين", text="تكوين")),
        QuickReplyButton(action=MessageAction(label="⚡ أسرع", text="أسرع")),
        QuickReplyButton(action=MessageAction(label="🧮 رياضيات", text="رياضيات")),
        QuickReplyButton(action=MessageAction(label="🔤 ترتيب", text="ترتيب")),
        QuickReplyButton(action=MessageAction(label="📊 نقاطي", text="نقاطي")),
        QuickReplyButton(action=MessageAction(label="🏆 الصدارة", text="الصدارة"))
    ])

def get_user_profile_safe(user_id):
    """الحصول على اسم المستخدم بأمان"""
    try:
        profile = line_bot_api.get_profile(user_id)
        return profile.display_name
    except Exception as e:
        logger.error(f"❌ خطأ في جلب الملف الشخصي: {e}")
        return "مستخدم"

def start_game(game_id, game_class, game_type, user_id, event):
    """بدء لعبة جديدة"""
    try:
        with games_lock:
            game = game_class(line_bot_api)
            with players_lock:
                participants = registered_players.copy()
                participants.add(user_id)
            
            active_games[game_id] = {
                'game': game,
                'type': game_type,
                'created_at': datetime.now(),
                'participants': participants
            }
        
        response = game.start_game()
        if isinstance(response, FlexSendMessage):
            response.quick_reply = get_quick_reply()
        
        line_bot_api.reply_message(event.reply_token, response)
        logger.info(f"🎮 بدأت لعبة {game_type} للمستخدم {user_id}")
        return True
    
    except Exception as e:
        logger.error(f"❌ خطأ في بدء اللعبة: {e}")
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text=f"❌ حدث خطأ في بدء {game_type}",
                quick_reply=get_quick_reply()
            )
        )
        return False

@app.route("/", methods=['GET'])
def home():
    """الصفحة الرئيسية"""
    return f'''
    <!DOCTYPE html>
    <html dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{BOT_NAME} - LINE Bot</title>
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
                background: rgba(255, 255, 255, 0.95);
                border-radius: 20px;
                padding: 40px;
                max-width: 600px;
                width: 100%;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                text-align: center;
            }}
            h1 {{
                color: #667eea;
                font-size: 2.5em;
                margin-bottom: 10px;
            }}
            .status {{
                background: #f0f4ff;
                padding: 20px;
                border-radius: 15px;
                margin: 20px 0;
            }}
            .status-item {{
                display: flex;
                justify-content: space-between;
                padding: 10px 0;
                border-bottom: 1px solid #e0e0e0;
            }}
            .status-item:last-child {{ border-bottom: none; }}
            .label {{ color: #666; font-weight: 500; }}
            .value {{ color: #667eea; font-weight: bold; }}
            .footer {{
                margin-top: 30px;
                padding-top: 20px;
                border-top: 2px solid #e0e0e0;
                color: #999;
                font-size: 0.9em;
            }}
            .badge {{
                display: inline-block;
                background: #51cf66;
                color: white;
                padding: 5px 15px;
                border-radius: 20px;
                font-size: 0.9em;
                margin: 10px 0;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎮 {BOT_NAME}</h1>
            <div class="badge">✅ الخادم يعمل بنجاح</div>
            
            <div class="status">
                <div class="status-item">
                    <span class="label">📦 الإصدار</span>
                    <span class="value">{VERSION}</span>
                </div>
                <div class="status-item">
                    <span class="label">🎮 الألعاب المتاحة</span>
                    <span class="value">{len(AVAILABLE_GAMES)}</span>
                </div>
                <div class="status-item">
                    <span class="label">👥 اللاعبون المسجلون</span>
                    <span class="value">{len(registered_players)}</span>
                </div>
                <div class="status-item">
                    <span class="label">🕹️ الألعاب النشطة</span>
                    <span class="value">{len(active_games)}</span>
                </div>
            </div>
            
            <div class="footer">
                <p>تم إنشاء هذا البوت بواسطة {BOT_CREATOR} © {BOT_YEAR}</p>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route("/callback", methods=['POST'])
def callback():
    """معالج الـ webhook"""
    signature = request.headers.get('X-Line-Signature', '')
    body = request.get_data(as_text=True)
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        logger.error("❌ توقيع غير صالح")
        abort(400)
    except Exception as e:
        logger.error(f"❌ خطأ في المعالج: {e}")
    
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    """معالجة الرسائل"""
    try:
        user_id = event.source.user_id
        text = event.message.text.strip()
        
        # فحص حد الرسائل
        if not check_rate_limit(user_id):
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="⚠️ كثير من الرسائل! انتظر قليلاً.")
            )
            return
        
        display_name = get_user_profile_safe(user_id)
        game_id = event.source.group_id if hasattr(event.source, 'group_id') else user_id
        
        logger.info(f"📨 {display_name}: {text}")
        
        # الأوامر الأساسية
        if text in ['البداية', 'ابدأ', 'start', 'قائمة', 'البوت', 'مرحبا']:
            welcome = create_welcome_flex(display_name, len(AVAILABLE_GAMES))
            line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage(alt_text="مرحباً", contents=welcome, quick_reply=get_quick_reply())
            )
            return
        
        elif text == 'نقاطي':
            stats = get_user_stats(user_id)
            if stats:
                stats_flex = create_stats_flex(dict(stats), user_id in registered_players)
                line_bot_api.reply_message(
                    event.reply_token,
                    FlexSendMessage(alt_text="إحصائياتك", contents=stats_flex, quick_reply=get_quick_reply())
                )
            else:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(
                        text="لم تلعب بعد\n\nاكتب 'انضم' للتسجيل",
                        quick_reply=get_quick_reply()
                    )
                )
            return
        
        elif text == 'الصدارة':
            leaders = get_leaderboard()
            if leaders:
                leaderboard = create_leaderboard_flex([dict(l) for l in leaders])
                line_bot_api.reply_message(
                    event.reply_token,
                    FlexSendMessage(alt_text="الصدارة", contents=leaderboard, quick_reply=get_quick_reply())
                )
            else:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text="لا توجد بيانات بعد", quick_reply=get_quick_reply())
                )
            return
        
        elif text in ['إيقاف', 'ايقاف', 'stop']:
            with games_lock:
                if game_id in active_games:
                    game_type = active_games[game_id]['type']
                    del active_games[game_id]
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text=f"تم إيقاف {game_type}", quick_reply=get_quick_reply())
                    )
                else:
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text="لا توجد لعبة نشطة", quick_reply=get_quick_reply())
                    )
            return
        
        elif text in ['انضم', 'تسجيل', 'join']:
            with players_lock:
                if user_id in registered_players:
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(
                            text=f"أنت مسجل بالفعل يا {display_name} ✅",
                            quick_reply=get_quick_reply()
                        )
                    )
                else:
                    registered_players.add(user_id)
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(
                            text=f"🎉 تم التسجيل بنجاح!\n\nمرحباً {display_name}\nيمكنك الآن اللعب وحفظ نقاطك",
                            quick_reply=get_quick_reply()
                        )
                    )
                    logger.info(f"✅ انضم: {display_name}")
            return
        
        elif text == 'مساعدة':
            help_text = f"""📖 دليل {BOT_NAME}

🎮 الألعاب المتاحة:
- تكوين - تكوين الكلمات
- أسرع - الكتابة السريعة
- رياضيات - الرياضيات السريعة
- ترتيب - ترتيب الحروف

📊 الأوامر:
- انضم - للتسجيل
- نقاطي - إحصائياتك
- الصدارة - أفضل اللاعبين
- إيقاف - إنهاء اللعبة

ملاحظة: سجل أولاً لحفظ نقاطك!"""
            
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=help_text, quick_reply=get_quick_reply())
            )
            return
        
        # بدء الألعاب
        if text in AVAILABLE_GAMES:
            game_class, game_type = AVAILABLE_GAMES[text]
            start_game(game_id, game_class, game_type, user_id, event)
            return
        
        # معالجة إجابات الألعاب النشطة
        if game_id in active_games:
            game_data = active_games[game_id]
            
            with players_lock:
                is_registered = user_id in registered_players
            
            if not is_registered and 'participants' in game_data and user_id not in game_data['participants']:
                return
            
            game = game_data['game']
            game_type = game_data['type']
            
            try:
                result = game.check_answer(text, user_id, display_name)
                
                if result:
                    points = result.get('points', 0)
                    if points > 0:
                        update_user_points(user_id, display_name, points, result.get('won', False), game_type)
                    
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
                            response.quick_reply = get_quick_reply()
                    
                    line_bot_api.reply_message(event.reply_token, response)
                return
            
            except Exception as e:
                logger.error(f"❌ خطأ في معالجة الإجابة: {e}")
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(
                        text="❌ حدث خطأ. حاول مرة أخرى.",
                        quick_reply=get_quick_reply()
                    )
                )
                return
    
    except Exception as e:
        logger.error(f"❌ خطأ في معالجة الرسالة: {e}")

@app.errorhandler(Exception)
def handle_error(error):
    """معالج الأخطاء العام"""
    logger.error(f"❌ خطأ غير متوقع: {error}", exc_info=True)
    return 'Internal Server Error', 500

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"🚀 بدء {BOT_NAME} على المنفذ {port}")
    logger.info(f"👥 اللاعبون: {len(registered_players)}")
    logger.info(f"🎮 الألعاب النشطة: {len(active_games)}")
    app.run(host='0.0.0.0', port=port, debug=False)
