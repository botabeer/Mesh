"""
Bot Mesh - LINE Bot Application v6.0 DATABASE EDITION
Created by: Abeer Aldosari © 2025

التحسينات الجديدة v6.0:
- ✅ قاعدة بيانات SQLite للبيانات الدائمة
- ✅ نظام الإنجازات الكامل
- ✅ إشعارات فتح الإنجازات
- ✅ إحصائيات محسّنة من قاعدة البيانات
- ✅ تنظيف تلقائي للبيانات القديمة
- ✅ نسخ احتياطي تلقائي يومي
"""

import os
import sys
import logging
from datetime import datetime, timedelta
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
    build_winner_announcement, build_help_menu,
    build_game_stats, build_detailed_game_info
)

# Import new modules
from database import get_database
from achievements import AchievementManager, build_achievements_ui, build_achievement_unlock_notification

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
# Database & Achievement System
# ============================================================================
db = get_database()
achievement_manager = AchievementManager(db)

# ============================================================================
# In-Memory Storage (للأداء السريع)
# ============================================================================
active_games = {}      # {user_id: game_instance}
user_cache = {}        # {user_id: user_data} - cache مؤقت

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
# Quick Reply Helper Function
# ============================================================================
def create_quick_reply():
    """Create permanent Quick Reply buttons"""
    return QuickReply(items=[
        QuickReplyItem(action=MessageAction(label="🏠 البداية", text="بداية")),
        QuickReplyItem(action=MessageAction(label="🎮 الألعاب", text="ألعاب")),
        QuickReplyItem(action=MessageAction(label="⭐ نقاطي", text="نقاطي")),
        QuickReplyItem(action=MessageAction(label="🏆 الصدارة", text="صدارة")),
        QuickReplyItem(action=MessageAction(label="🎖️ الإنجازات", text="إنجازات")),
        QuickReplyItem(action=MessageAction(label="❓ مساعدة", text="مساعدة")),
        QuickReplyItem(action=MessageAction(label="⛔ إيقاف", text="إيقاف"))
    ])

def attach_quick_reply(message):
    """Attach Quick Reply to any message"""
    if hasattr(message, 'quick_reply'):
        message.quick_reply = create_quick_reply()
    return message

# ============================================================================
# Helper Functions
# ============================================================================
def get_user_data(user_id: str, username: str = "مستخدم") -> dict:
    """الحصول على بيانات المستخدم مع cache"""
    # التحقق من الـ cache
    if user_id in user_cache:
        return user_cache[user_id]
    
    # الحصول من قاعدة البيانات
    user = db.get_user(user_id)
    
    if not user:
        # إنشاء مستخدم جديد
        db.create_user(user_id, username)
        user = db.get_user(user_id)
    
    # حفظ في الـ cache
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

def send_achievement_notifications(line_bot_api, reply_token, achievements, theme):
    """إرسال إشعارات الإنجازات المفتوحة"""
    if not achievements:
        return
    
    messages = []
    for achievement in achievements[:3]:  # أقصى 3 إشعارات
        msg = build_achievement_unlock_notification(achievement, theme)
        messages.append(attach_quick_reply(msg))
    
    if messages:
        try:
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(reply_token=reply_token, messages=messages)
            )
        except:
            pass

def is_group_chat(event):
    """Check if message is from a group"""
    return hasattr(event.source, 'group_id')

# ============================================================================
# Scheduled Tasks
# ============================================================================
def run_daily_cleanup():
    """تنظيف يومي للبيانات القديمة"""
    try:
        # حذف المستخدمين غير النشطين
        deleted_users = db.cleanup_inactive_users(days=7)
        
        # حذف جلسات الألعاب القديمة
        deleted_sessions = db.cleanup_old_sessions(days=30)
        
        # نسخ احتياطي
        backup_path = f"backups/botmesh_{datetime.now().strftime('%Y%m%d')}.db"
        os.makedirs("backups", exist_ok=True)
        db.backup_database(backup_path)
        
        logger.info(f"🧹 Daily cleanup: {deleted_users} users, {deleted_sessions} sessions")
        logger.info(f"💾 Backup saved: {backup_path}")
    except Exception as e:
        logger.error(f"❌ Daily cleanup error: {e}")

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
    game_stats = db.get_all_game_stats()
    
    total_games_played = sum(g.get('plays', 0) for g in game_stats.values())
    total_completions = sum(g.get('completions', 0) for g in game_stats.values())
    
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
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
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
                backdrop-filter: blur(10px);
                border-radius: 30px;
                padding: 40px;
                max-width: 900px;
                width: 100%;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            }}
            h1 {{ font-size: 3em; margin-bottom: 10px; text-align: center; text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3); }}
            .version {{ font-size: 0.9em; opacity: 0.8; margin-bottom: 30px; text-align: center; }}
            .status {{
                font-size: 1.3em;
                margin: 30px 0;
                padding: 20px;
                background: rgba(255, 255, 255, 0.2);
                border-radius: 20px;
                text-align: center;
            }}
            .stats {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
                gap: 20px;
                margin: 30px 0;
            }}
            .stat-card {{
                background: rgba(255, 255, 255, 0.2);
                padding: 25px;
                border-radius: 20px;
                text-align: center;
            }}
            .stat-value {{ font-size: 2.5em; font-weight: bold; margin: 10px 0; }}
            .stat-label {{ font-size: 0.9em; opacity: 0.9; }}
            .footer {{ margin-top: 30px; font-size: 0.85em; opacity: 0.7; text-align: center; }}
            .pulse {{ animation: pulse 2s infinite; }}
            @keyframes pulse {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.6; }} }}
            .features {{
                background: rgba(255, 255, 255, 0.15);
                padding: 20px;
                border-radius: 15px;
                margin: 20px 0;
            }}
            .features h3 {{ margin-bottom: 15px; font-size: 1.5em; }}
            .features ul {{ list-style: none; padding: 0; }}
            .features li {{ padding: 8px 0; font-size: 0.95em; }}
            .features li:before {{ content: "✅ "; color: #48BB78; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎮 {BOT_NAME}</h1>
            <div class="version">Version {BOT_VERSION} - Database Edition v6.0</div>
            <div class="status pulse">✅ Bot is running smoothly</div>
            
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-value">{stats['total_users']}</div>
                    <div class="stat-label">👥 المستخدمين</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{stats['registered_users']}</div>
                    <div class="stat-label">📝 المسجلين</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{len(AVAILABLE_GAMES)}</div>
                    <div class="stat-label">🎮 الألعاب</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{len(active_games)}</div>
                    <div class="stat-label">⚡ نشط الآن</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{total_games_played}</div>
                    <div class="stat-label">🎯 إجمالي الألعاب</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{total_completions}</div>
                    <div class="stat-label">✅ الإنجازات</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{stats['total_points']}</div>
                    <div class="stat-label">⭐ النقاط الممنوحة</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{len(achievement_manager.ACHIEVEMENTS) if hasattr(achievement_manager, 'ACHIEVEMENTS') else 21}</div>
                    <div class="stat-label">🏆 الإنجازات</div>
                </div>
            </div>
            
            <div class="features">
                <h3>✨ المميزات الجديدة v6.0</h3>
                <ul>
                    <li>قاعدة بيانات SQLite للبيانات الدائمة</li>
                    <li>نظام الإنجازات الكامل (21 إنجاز)</li>
                    <li>إشعارات فتح الإنجازات</li>
                    <li>إحصائيات محسّنة من قاعدة البيانات</li>
                    <li>تنظيف تلقائي للبيانات القديمة</li>
                    <li>نسخ احتياطي تلقائي يومي</li>
                    <li>Quick Reply Buttons دائمة</li>
                    <li>12 لعبة متنوعة</li>
                    <li>9 ثيمات احترافية</li>
                    <li>نظام نقاط وصدارة متقدم</li>
                    <li>دعم كامل للمجموعات</li>
                </ul>
            </div>
            
            <div class="footer">{BOT_RIGHTS}</div>
        </div>
    </body>
    </html>
    """

@app.route("/cleanup", methods=['POST'])
def manual_cleanup():
    """تنظيف يدوي (للمطورين)"""
    run_daily_cleanup()
    return {"status": "success", "message": "Cleanup completed"}

# ============================================================================
# Message Handler
# ============================================================================
@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    """Handle incoming messages with Database integration"""
    try:
        user_id = event.source.user_id
        text = event.message.text.strip()
        
        if not text:
            return
        
        # Check if in group
        in_group = is_group_chat(event)
        
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            
            # Get user profile
            try:
                profile = line_bot_api.get_profile(user_id)
                username = get_username(profile)
            except:
                username = "مستخدم"
            
            # In groups, only respond to registered users or mentions
            if in_group and "@" not in text.lower():
                user = get_user_data(user_id, username)
                if not user.get('is_registered'):
                    return
                if user_id not in active_games:
                    return
            
            # Get or create user
            user = get_user_data(user_id, username)
            
            # Update activity
            db.update_activity(user_id)
            
            # Get theme from database
            current_theme = user.get('theme', DEFAULT_THEME)
            reply = None
            
            text_lower = text.lower()
            
            # ===== Command Handling =====
            
            # Home/Start
            if text_lower in ["بداية", "start", "home"] or "@" in text_lower:
                reply = build_home(current_theme, username, user['points'], user['is_registered'])
            
            # Games Menu
            elif text_lower in ["ألعاب", "games", "مساعدة", "help"] and user_id not in active_games:
                reply = build_games_menu(current_theme)
            
            # Achievements
            elif text_lower in ["إنجازات", "achievements"]:
                reply = build_achievements_ui(user_id, achievement_manager, current_theme)
            
            # Theme Change
            elif text.startswith("ثيم "):
                from constants import THEMES
                theme = text.replace("ثيم ", "").strip()
                if theme in THEMES:
                    db.update_user(user_id, theme=theme)
                    update_user_cache(user_id)
                    reply = build_home(theme, username, user['points'], user['is_registered'])
                else:
                    reply = TextMessage(text=f"❌ ثيم '{theme}' غير موجود")
            
            # Join/Register
            elif text_lower in ["انضم", "join", "register"]:
                db.update_user(user_id, is_registered=True)
                update_user_cache(user_id)
                
                # فتح إنجاز التسجيل
                unlocked = achievement_manager.check_and_unlock(user_id, "registered")
                if unlocked:
                    send_achievement_notifications(line_bot_api, event.reply_token, unlocked, current_theme)
                
                reply = build_home(current_theme, username, user['points'], True)
            
            # Leave/Unregister
            elif text_lower in ["انسحب", "leave", "unregister"]:
                db.update_user(user_id, is_registered=False)
                update_user_cache(user_id)
                reply = build_home(current_theme, username, user['points'], False)
            
            # My Points
            elif text_lower in ["نقاطي", "points", "score"]:
                user_game_stats = db.get_user_game_stats(user_id)
                reply = build_my_points(username, user['points'], user_game_stats, current_theme)
            
            # Leaderboard
            elif text_lower in ["صدارة", "leaderboard", "top"]:
                leaderboard = db.get_leaderboard(10)
                reply = build_leaderboard(leaderboard, current_theme)
            
            # Stop Game
            elif text_lower in ["إيقاف", "stop", "quit", "exit"]:
                if user_id in active_games:
                    game_name = active_games[user_id].game_name
                    del active_games[user_id]
                    reply = build_games_menu(current_theme)
                else:
                    reply = TextMessage(text="❌ لا يوجد لعبة نشطة")
            
            # Start Game or Replay
            elif text.startswith("لعبة ") or text.startswith("إعادة "):
                if not user.get("is_registered"):
                    reply = build_registration_required(current_theme)
                else:
                    # Extract game name
                    if text.startswith("إعادة "):
                        game_name = text.replace("إعادة ", "").strip()
                    else:
                        game_name = text.replace("لعبة ", "").strip()
                    
                    if game_name in AVAILABLE_GAMES:
                        try:
                            GameClass = AVAILABLE_GAMES[game_name]
                            game_instance = GameClass(line_bot_api)
                            
                            # Set theme
                            if hasattr(game_instance, 'set_theme'):
                                game_instance.set_theme(current_theme)
                            
                            active_games[user_id] = game_instance
                            reply = game_instance.start_game()
                            
                            # Create session in database
                            session_id = db.create_game_session(user_id, game_name)
                            game_instance.session_id = session_id
                            
                            # فتح إنجاز اللعبة الأولى
                            unlocked = achievement_manager.check_and_unlock(user_id, "game_played")
                            if unlocked:
                                send_achievement_notifications(line_bot_api, event.reply_token, unlocked, current_theme)
                            
                            logger.info(f"🎮 {username} بدأ لعبة {game_name}")
                        except Exception as e:
                            logger.error(f"❌ خطأ في بدء اللعبة {game_name}: {e}")
                            reply = TextMessage(text=f"❌ حدث خطأ في بدء اللعبة")
                    else:
                        reply = TextMessage(text=f"❌ اللعبة '{game_name}' غير موجودة")
            
            # Game Answer Handling
            else:
                if user_id in active_games:
                    try:
                        game_instance = active_games[user_id]
                        game_name = game_instance.game_name
                        result = game_instance.check_answer(text, user_id, username)
                        
                        if result:
                            # Update points in database
                            if result.get('points', 0) > 0:
                                db.add_points(user_id, result['points'])
                                update_user_cache(user_id)
                                
                                # التحقق من إنجازات النقاط
                                unlocked = achievement_manager.check_and_unlock(user_id, "points_updated")
                                if unlocked:
                                    send_achievement_notifications(line_bot_api, event.reply_token, unlocked, current_theme)
                            
                            # Check if game over
                            if result.get('game_over'):
                                # Complete session
                                if hasattr(game_instance, 'session_id'):
                                    db.complete_game_session(game_instance.session_id, result.get('points', 0))
                                
                                # Update game stats
                                db.update_game_stats(game_name, completed=True, points=result.get('points', 0))
                                
                                # Winner announcement
                                user = get_user_data(user_id, username)
                                reply = build_winner_announcement(
                                    username=username,
                                    game_name=game_name,
                                    total_score=result.get('points', 0),
                                    final_points=user['points'],
                                    theme=current_theme
                                )
                                
                                # فتح إنجازات الفوز
                                unlocked = achievement_manager.check_and_unlock(user_id, "game_won")
                                unlocked += achievement_manager.check_and_unlock(user_id, "games_count")
                                if unlocked:
                                    send_achievement_notifications(line_bot_api, event.reply_token, unlocked, current_theme)
                                
                                del active_games[user_id]
                            else:
                                reply = result.get('response')
                    except Exception as e:
                        logger.error(f"❌ خطأ في معالجة إجابة اللعبة: {e}")
                        reply = TextMessage(text="❌ حدث خطأ في معالجة الإجابة")
                else:
                    # No active game
                    reply = build_home(current_theme, username, user['points'], user['is_registered'])
            
            # ===== Send Reply with Quick Reply =====
            if reply:
                send_with_quick_reply(line_bot_api, event.reply_token, reply)
                
    except Exception as e:
        logger.error(f"❌ Error in handle_message: {e}", exc_info=True)
        try:
            error_msg = TextMessage(text="❌ حدث خطأ غير متوقع. الرجاء المحاولة مرة أخرى.")
            send_with_quick_reply(line_bot_api, event.reply_token, error_msg)
        except:
            pass

# ============================================================================
# Run Application
# ============================================================================
if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    
    logger.info("=" * 70)
    logger.info(f"🚀 Starting {BOT_NAME} v{BOT_VERSION} - Database Edition v6.0")
    logger.info(f"📦 Loaded {len(AVAILABLE_GAMES)} games")
    logger.info(f"🎨 Themes: {len(__import__('constants').THEMES)}")
    logger.info(f"🗄️ Database: SQLite")
    logger.info(f"🏆 Achievements: 21 achievements")
    logger.info(f"🌐 Server on port {port}")
    logger.info("=" * 70)
    
    # تشغيل التنظيف الأولي
    logger.info("🧹 Running initial cleanup...")
    run_daily_cleanup()
    
    app.run(host="0.0.0.0", port=port, debug=False)
