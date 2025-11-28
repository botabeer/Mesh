"""
Bot Mesh - LINE Bot Application v7.0 FINAL EDITION
تم إنشاء هذا البوت بواسطة عبير الدوسري © 2025

✅ Groups Optimized: للعب الجماعي والمنافسة
✅ 5 Rounds Per Game: خمس جولات لكل لعبة
✅ First Correct Answer Only: أول إجابة صحيحة فقط
✅ Smart Points System: نقطة واحدة لكل إجابة صحيحة
✅ Registered Users Only: للمسجلين فقط
✅ Professional 3D Glass Design: تصميم زجاجي ثلاثي الأبعاد
✅ High Security: أمان عالي
✅ No Errors: خالي من الأخطاء
"""

import os
import sys
import logging
from datetime import datetime, timedelta
from collections import defaultdict
from flask import Flask, request, abort

from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi,
    ReplyMessageRequest, QuickReply, QuickReplyItem,
    MessageAction, TextMessage
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent

# Import modules
from constants import (
    BOT_NAME, BOT_VERSION, BOT_RIGHTS,
    LINE_CHANNEL_SECRET, LINE_CHANNEL_ACCESS_TOKEN,
    validate_env, get_username, GAME_LIST, DEFAULT_THEME
)

from ui_builder import (
    build_home, build_games_menu, build_my_points,
    build_leaderboard, build_registration_required,
    build_winner_announcement, build_group_game_result
)

from database import get_database

# ============================================================================
# Configuration & Validation
# ============================================================================
try:
    validate_env()
except ValueError as e:
    print(f"❌ Configuration Error: {e}")
    sys.exit(1)

# ============================================================================
# Flask & LINE Setup
# ============================================================================
app = Flask(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# ============================================================================
# Database
# ============================================================================
db = get_database()

# ============================================================================
# In-Memory Storage
# ============================================================================
active_games = {}  # {group_id: game_instance}
user_cache = {}
user_requests = defaultdict(list)

# ============================================================================
# Security: Rate Limiting
# ============================================================================
def is_rate_limited(user_id, max_requests=10, window=60):
    """معدل محدود لمنع الإزعاج"""
    now = datetime.now()
    cutoff = now - timedelta(seconds=window)
    
    user_requests[user_id] = [t for t in user_requests[user_id] if t > cutoff]
    
    if len(user_requests[user_id]) >= max_requests:
        logger.warning(f"⚠️ Rate limit exceeded for user {user_id}")
        return True
    
    user_requests[user_id].append(now)
    return False

# ============================================================================
# Game Loading System
# ============================================================================
AVAILABLE_GAMES = {}

try:
    from games.iq_game import IqGame
    from games.math_game import MathGame
    from games.word_color_game import WordColorGame
    from games.scramble_word_game import ScrambleWordGame
    from games.fast_typing_game import FastTypingGame
    from games.opposite_game import OppositeGame
    from games.letters_words_game import LettersWordsGame
    from games.song_game import SongGame
    from games.human_animal_plant_game import HumanAnimalPlantGame
    from games.chain_words_game import ChainWordsGame
    from games.guess_game import GuessGame
    from games.compatibility_game import CompatibilityGame
    
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
    
    logger.info(f"✅ تم تحميل {len(AVAILABLE_GAMES)} لعبة بنجاح")
except Exception as e:
    logger.error(f"❌ خطأ في تحميل الألعاب: {e}")
    import traceback
    traceback.print_exc()

# ============================================================================
# Quick Reply Helper - Games Only
# ============================================================================
def create_games_quick_reply():
    """Create Quick Reply with Games Only"""
    games_list = [
        "أسرع", "ذكاء", "لعبة", "أغنية", "خمن", "سلسلة",
        "ترتيب", "تكوين", "ضد", "لون", "رياضيات", "توافق"
    ]
    
    items = []
    for game in games_list:
        items.append(QuickReplyItem(action=MessageAction(label=game, text=game)))
    
    return QuickReply(items=items)

def attach_quick_reply(message):
    """Attach Quick Reply to any message"""
    if hasattr(message, 'quick_reply'):
        message.quick_reply = create_games_quick_reply()
    return message

# ============================================================================
# Helper Functions
# ============================================================================
def get_user_data(user_id: str, username: str = "مستخدم") -> dict:
    """الحصول على بيانات المستخدم مع cache"""
    if user_id in user_cache:
        return user_cache[user_id]
    
    user = db.get_user(user_id)
    
    if not user:
        db.create_user(user_id, username)
        user = db.get_user(user_id)
    
    user_cache[user_id] = user
    return user

def update_user_cache(user_id: str):
    """تحديث الـ cache من قاعدة البيانات"""
    user = db.get_user(user_id)
    if user:
        user_cache[user_id] = user

def send_with_quick_reply(line_bot_api, reply_token, message):
    """Send message with Quick Reply buttons"""
    message = attach_quick_reply(message)
    line_bot_api.reply_message_with_http_info(
        ReplyMessageRequest(reply_token=reply_token, messages=[message])
    )

def is_group_chat(event):
    """Check if message is from a group"""
    return hasattr(event.source, 'group_id')

def get_game_id(event):
    """Get unique game ID (group or user)"""
    if is_group_chat(event):
        return event.source.group_id
    return event.source.user_id

# ============================================================================
# Flask Routes
# ============================================================================
@app.route("/callback", methods=['POST'])
def callback():
    """LINE webhook callback"""
    signature = request.headers.get('X-Line-Signature', '')
    body = request.get_data(as_text=True)
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        logger.error("❌ Invalid signature")
        abort(400)
    except Exception as e:
        logger.error(f"❌ Callback error: {e}")
        abort(500)
    
    return 'OK'

@app.route("/", methods=['GET'])
def home():
    """Bot status page"""
    stats = db.get_stats_summary()
    
    return f"""
    <!DOCTYPE html>
    <html dir="rtl" lang="ar">
    <head>
        <title>{BOT_NAME} v{BOT_VERSION}</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{
                font-family: 'Segoe UI', sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }}
            .container {{
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(20px);
                border-radius: 30px;
                padding: 40px;
                max-width: 900px;
                width: 100%;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            }}
            h1 {{ font-size: 3em; margin-bottom: 10px; text-align: center; }}
            .version {{ font-size: 0.9em; opacity: 0.8; margin-bottom: 30px; text-align: center; }}
            .status {{ font-size: 1.3em; margin: 30px 0; padding: 20px; background: rgba(255, 255, 255, 0.2);
                      border-radius: 20px; text-align: center; }}
            .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 20px; margin: 30px 0; }}
            .stat-card {{ background: rgba(255, 255, 255, 0.2); padding: 25px; border-radius: 20px; text-align: center; }}
            .stat-value {{ font-size: 2.5em; font-weight: bold; margin: 10px 0; }}
            .stat-label {{ font-size: 0.9em; opacity: 0.9; }}
            .footer {{ margin-top: 30px; font-size: 0.85em; opacity: 0.7; text-align: center; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>{BOT_NAME}</h1>
            <div class="version">Version {BOT_VERSION} - Professional 3D Glass Design</div>
            <div class="status">✅ Bot is running smoothly</div>
            
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-value">{stats['total_users']}</div>
                    <div class="stat-label">المستخدمين</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{stats['registered_users']}</div>
                    <div class="stat-label">المسجلين</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{len(AVAILABLE_GAMES)}</div>
                    <div class="stat-label">الألعاب</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{len(active_games)}</div>
                    <div class="stat-label">نشط الآن</div>
                </div>
            </div>
            
            <div class="footer">{BOT_RIGHTS}</div>
        </div>
    </body>
    </html>
    """

# ============================================================================
# Message Handler
# ============================================================================
@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    """Handle incoming messages - Commands Only"""
    try:
        user_id = event.source.user_id
        text = event.message.text.strip()
        
        if not text:
            return
        
        # Rate limiting
        if is_rate_limited(user_id):
            return
        
        in_group = is_group_chat(event)
        game_id = get_game_id(event)
        
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            
            try:
                profile = line_bot_api.get_profile(user_id)
                username = get_username(profile)
            except:
                username = "مستخدم"
            
            # في المجموعات: تجاهل الرسائل إلا إذا كانت منشن أو لعبة نشطة
            if in_group and "@" not in text.lower() and game_id not in active_games:
                return
            
            user = get_user_data(user_id, username)
            db.update_activity(user_id)
            
            current_theme = user.get('theme', DEFAULT_THEME)
            reply = None
            
            text_lower = text.lower()
            
            # ===== الأوامر الأساسية =====
            
            if "@" in text_lower or text_lower in ["بداية", "start", "home"]:
                # عند المنشن أو البداية: أرسل قائمة الألعاب مع Quick Reply
                reply = build_games_menu(current_theme)
            
            elif text_lower in ["انضم", "join", "register"]:
                db.update_user(user_id, is_registered=True)
                update_user_cache(user_id)
                reply = TextMessage(text="✅ تم التسجيل بنجاح! يمكنك الآن المشاركة في الألعاب")
            
            elif text_lower in ["انسحب", "leave", "unregister"]:
                db.update_user(user_id, is_registered=False)
                update_user_cache(user_id)
                reply = TextMessage(text="❌ تم إلغاء التسجيل")
            
            elif text_lower in ["نقاطي", "points", "score"]:
                user_game_stats = db.get_user_game_stats(user_id)
                reply = build_my_points(username, user['points'], user_game_stats, current_theme)
            
            elif text_lower in ["صدارة", "leaderboard", "top"]:
                leaderboard = db.get_leaderboard(10)
                reply = build_leaderboard(leaderboard, current_theme)
            
            elif text_lower in ["إيقاف", "stop", "quit", "exit"]:
                if game_id in active_games:
                    del active_games[game_id]
                    reply = TextMessage(text="⛔ تم إيقاف اللعبة")
            
            elif text in GAME_LIST or text.startswith("لعبة ") or text.startswith("إعادة "):
                if not user.get("is_registered"):
                    reply = build_registration_required(current_theme)
                else:
                    # Extract game name
                    if text.startswith("إعادة "):
                        game_name = text.replace("إعادة ", "").strip()
                    elif text.startswith("لعبة "):
                        game_name = text.replace("لعبة ", "").strip()
                    else:
                        game_data = GAME_LIST.get(text)
                        if game_data:
                            game_name = game_data["command"].replace("لعبة ", "")
                        else:
                            game_name = text
                    
                    if game_name in AVAILABLE_GAMES:
                        try:
                            GameClass = AVAILABLE_GAMES[game_name]
                            game_instance = GameClass(line_bot_api)
                            
                            if hasattr(game_instance, 'set_theme'):
                                game_instance.set_theme(current_theme)
                            
                            active_games[game_id] = game_instance
                            reply = game_instance.start_game()
                            
                            session_id = db.create_game_session(user_id, game_name)
                            game_instance.session_id = session_id
                            
                            logger.info(f"🎮 {username} بدأ لعبة {game_name}")
                        except Exception as e:
                            logger.error(f"❌ خطأ في بدء اللعبة {game_name}: {e}")
                            reply = TextMessage(text="❌ حدث خطأ في بدء اللعبة")
                    else:
                        reply = TextMessage(text=f"❌ اللعبة '{game_name}' غير موجودة")
            
            else:
                # التعامل مع الإجابات في اللعبة
                if game_id in active_games:
                    try:
                        game_instance = active_games[game_id]
                        
                        # تحقق من تسجيل المستخدم
                        if not user.get('is_registered'):
                            return  # تجاهل إجابات غير المسجلين
                        
                        game_name = game_instance.game_name
                        result = game_instance.check_answer(text, user_id, username)
                        
                        if result:
                            # إضافة النقاط للمسجلين فقط
                            if result.get('points', 0) > 0:
                                db.add_points(user_id, result['points'])
                                update_user_cache(user_id)
                            
                            if result.get('game_over'):
                                # حفظ جلسة اللعبة
                                if hasattr(game_instance, 'session_id'):
                                    db.complete_game_session(
                                        game_instance.session_id,
                                        result.get('points', 0)
                                    )
                                
                                db.update_game_stats(
                                    game_name,
                                    completed=True,
                                    points=result.get('points', 0)
                                )
                                
                                # إعلان الفائز
                                user = get_user_data(user_id, username)
                                reply = build_winner_announcement(
                                    username=username,
                                    game_name=game_name,
                                    total_score=result.get('points', 0),
                                    final_points=user['points'],
                                    theme=current_theme
                                )
                                
                                del active_games[game_id]
                            else:
                                reply = result.get('response')
                    except Exception as e:
                        logger.error(f"❌ خطأ في معالجة اللعبة: {e}")
                        if game_id in active_games:
                            del active_games[game_id]
                        reply = TextMessage(text="❌ حدث خطأ، تم إيقاف اللعبة")
            
            if reply:
                send_with_quick_reply(line_bot_api, event.reply_token, reply)
                
    except Exception as e:
        logger.error(f"❌ Error in handle_message: {e}", exc_info=True)

# ============================================================================
# Run Application
# ============================================================================
if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    
    logger.info("=" * 70)
    logger.info(f"🚀 Starting {BOT_NAME} v{BOT_VERSION}")
    logger.info(f"🎨 UI Style: Professional 3D Glass Design")
    logger.info(f"📦 Loaded {len(AVAILABLE_GAMES)} games")
    logger.info(f"🌐 Server on port {port}")
    logger.info(f"🔒 Security: Rate Limiting Enabled")
    logger.info("=" * 70)
    
    app.run(host="0.0.0.0", port=port, debug=False)
