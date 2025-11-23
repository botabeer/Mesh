"""
Bot Mesh - Main Application (Enhanced Version)
Created by: Abeer Aldosari © 2025
Enhanced with better error handling and performance
"""
import os
import logging
from flask import Flask, request, abort, jsonify
from functools import wraps
import time

# === LINE SDK v3 - Correct Imports ===
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
    FlexMessage,
    FlexContainer,
    QuickReply,
    QuickReplyItem,
    MessageAction
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
    FollowEvent
)

# استيراد المكونات
from config import LINE_TOKEN, LINE_SECRET, DB_PATH, THEMES
from database import DB
from flex_builder import FlexBuilder
from game_manager import GameManager
from cache import CacheManager

# استيراد جميع الألعاب تلقائياً
from games import *

# ==================== Logging ====================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ==================== Flask & Line ====================
app = Flask(__name__)

configuration = Configuration(access_token=LINE_TOKEN)
handler = WebhookHandler(LINE_SECRET)

# Initialize managers
db = DB(DB_PATH)
gm = GameManager()
cache = CacheManager(ttl=300)  # 5 minutes cache

# ==================== قاموس الألعاب ====================
GAMES = {
    'ذكاء': IqGame,
    'لون': WordColorGame,
    'ترتيب': ScrambleWordGame,
    'رياضيات': MathGame,
    'أسرع': FastTypingGame,
    'ضد': OppositeGame,
    'تكوين': LettersWordsGame,
    'أغنية': SongGame,
    'لعبة': HumanAnimalPlantGame,
    'سلسلة': ChainWordsGame,
    'خمن': GuessGame,
    'توافق': CompatibilityGame
}

# ==================== Decorators ====================
def error_handler(f):
    """Decorator for error handling"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            logger.error(f'❌ Error in {f.__name__}: {str(e)}', exc_info=True)
            return None
    return decorated_function

def performance_monitor(f):
    """Decorator for performance monitoring"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        start_time = time.time()
        result = f(*args, **kwargs)
        elapsed_time = time.time() - start_time
        if elapsed_time > 1:  # Log if takes more than 1 second
            logger.warning(f'⚠️ Slow operation: {f.__name__} took {elapsed_time:.2f}s')
        return result
    return decorated_function

# ==================== Helpers ====================
@error_handler
@performance_monitor
def get_name(uid):
    """Get user name with caching"""
    # Check cache first
    cached_name = cache.get(f'name_{uid}')
    if cached_name:
        return cached_name
    
    try:
        with ApiClient(configuration) as api_client:
            line_api = MessagingApi(api_client)
            profile = line_api.get_profile(uid)
            name = profile.display_name
            cache.set(f'name_{uid}', name)
            return name
    except Exception as e:
        logger.error(f'Error getting profile: {e}')
        return 'لاعب'

@error_handler
def get_theme(uid):
    """Get user theme"""
    user = db.get_user(uid)
    return user.get('theme', 'white') if user else 'white'

def get_games_quick_reply(uid):
    """Generate quick reply buttons for games"""
    items = []
    
    # Game buttons
    for label in GAMES.keys():
        items.append(QuickReplyItem(
            action=MessageAction(label=label, text=label)
        ))
    
    # Control buttons
    control_buttons = ['إيقاف', 'انضم', 'انسحب', 'إحصائيات']
    for label in control_buttons:
        items.append(QuickReplyItem(
            action=MessageAction(label=label, text=label)
        ))
    
    return QuickReply(items=items)

@error_handler
@performance_monitor
def send_flex_reply(reply_token, flex_content, uid=None, alt_text='القائمة'):
    """إرسال رسالة Flex مع Quick Reply باستخدام v3 API"""
    try:
        with ApiClient(configuration) as api_client:
            line_api = MessagingApi(api_client)
            
            messages = []
            
            # Flex message
            if flex_content:
                flex_msg = FlexMessage(
                    altText=alt_text,
                    contents=FlexContainer.from_dict(flex_content)
                )
                messages.append(flex_msg)
            
            # Quick reply
            if uid:
                text_msg = TextMessage(
                    text="اختر لعبة أو أمر:",
                    quickReply=get_games_quick_reply(uid)
                )
                messages.append(text_msg)
            
            if messages:
                line_api.reply_message(
                    ReplyMessageRequest(
                        replyToken=reply_token,
                        messages=messages
                    )
                )
                return True
            
    except Exception as e:
        logger.error(f'❌ Error sending flex reply: {e}')
        # Fallback to text message
        if uid:
            send_text_reply(reply_token, "حدث خطأ في عرض الرسالة. الرجاء المحاولة مرة أخرى.")
    
    return False

@error_handler
def send_text_reply(reply_token, text, quick_reply=None):
    """Send text message reply"""
    try:
        with ApiClient(configuration) as api_client:
            line_api = MessagingApi(api_client)
            msg = TextMessage(text=text)
            if quick_reply:
                msg.quickReply = quick_reply
            
            line_api.reply_message(
                ReplyMessageRequest(
                    replyToken=reply_token,
                    messages=[msg]
                )
            )
            return True
    except Exception as e:
        logger.error(f'❌ Error sending text reply: {e}')
    return False

@error_handler
def get_user_stats(uid):
    """Get user statistics"""
    user = db.get_user(uid)
    if not user:
        return "لم تلعب أي ألعاب بعد!"
    
    win_rate = (user['wins'] / user['games'] * 100) if user['games'] > 0 else 0
    
    stats = f"""
📊 إحصائياتك:
━━━━━━━━━━━━━━
👤 الاسم: {user['name']}
⭐ النقاط: {user['points']}
🎮 الألعاب: {user['games']}
🏆 الفوز: {user['wins']}
📈 نسبة الفوز: {win_rate:.1f}%
📅 انضممت: {user['joined_at'][:10]}
━━━━━━━━━━━━━━
    """.strip()
    
    return stats

# ==================== Routes ====================
@app.route('/')
def home():
    return jsonify({
        'name': 'Bot Mesh',
        'status': 'active',
        'version': '3.0.0',
        'games': list(GAMES.keys())
    })

@app.route('/health')
def health():
    """Health check endpoint"""
    try:
        # Check database
        db.get_user('health_check')
        db_status = 'ok'
    except Exception as e:
        db_status = f'error: {str(e)}'
    
    return jsonify({
        'status': 'ok',
        'database': db_status,
        'active_games': gm.get_active_games_count(),
        'registered_users': gm.get_users_count(),
        'total_games': len(GAMES),
        'themes': len(THEMES),
        'cache_hits': cache.hits,
        'cache_misses': cache.misses
    })

@app.route('/stats')
def stats():
    """Statistics endpoint"""
    return jsonify({
        'games': {
            'total_available': len(GAMES),
            'active_sessions': gm.get_active_games_count(),
            'game_types': list(GAMES.keys())
        },
        'users': {
            'registered': gm.get_users_count()
        },
        'cache': {
            'hits': cache.hits,
            'misses': cache.misses,
            'hit_rate': f"{(cache.hits / (cache.hits + cache.misses) * 100):.1f}%" if (cache.hits + cache.misses) > 0 else "0%"
        }
    })

@app.route('/callback', methods=['POST'])
@performance_monitor
def callback():
    """LINE webhook callback"""
    signature = request.headers.get('X-Line-Signature')
    if not signature:
        logger.error('❌ Missing signature')
        abort(400)
    
    body = request.get_data(as_text=True)
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        logger.error('❌ Invalid signature')
        abort(400)
    except Exception as e:
        logger.error(f'❌ Error handling webhook: {e}', exc_info=True)
        abort(500)
    
    return 'OK'

# ==================== Event Handlers ====================
@handler.add(FollowEvent)
@performance_monitor
def on_follow(event):
    """Handle new follower"""
    uid = event.source.user_id
    name = get_name(uid)
    db.add_or_update_user(uid, name)
    builder = FlexBuilder('white')
    send_flex_reply(event.reply_token, builder.welcome(), uid, 'مرحباً')
    logger.info(f'✅ New follower: {name} ({uid})')

@handler.add(MessageEvent, message=TextMessageContent)
@performance_monitor
def on_message(event):
    """Handle incoming messages"""
    uid = event.source.user_id
    txt = event.message.text.strip()
    gid = getattr(event.source, 'group_id', uid)
    name = get_name(uid)
    
    # Update user
    db.add_or_update_user(uid, name)
    builder = FlexBuilder(get_theme(uid))

    # انضم
    if txt == 'انضم':
        gm.register(uid)
        send_flex_reply(event.reply_token, builder.welcome(), uid, 'مرحباً')
        logger.info(f'✅ User registered: {name}')
        return

    # انسحب
    if txt == 'انسحب':
        gm.unregister(uid)
        send_text_reply(event.reply_token, 'تم الانسحاب، لن تُحسب إجاباتك')
        logger.info(f'ℹ️ User unregistered: {name}')
        return

    # إحصائيات
    if txt == 'إحصائيات':
        stats = get_user_stats(uid)
        send_text_reply(event.reply_token, stats)
        return

    # إيقاف
    if txt == 'إيقاف':
        if gm.get_game(gid):
            gm.end_game(gid)
            send_text_reply(event.reply_token, '✅ تم إيقاف اللعبة')
            logger.info(f'ℹ️ Game stopped in {gid}')
        else:
            send_text_reply(event.reply_token, '❌ لا توجد لعبة نشطة')
        return

    # بدء لعبة
    if txt in GAMES:
        if not gm.is_registered(uid):
            send_text_reply(event.reply_token, '❌ اكتب "انضم" أولاً للتسجيل')
            return

        if gm.get_game(gid):
            send_text_reply(event.reply_token, '⚠️ يوجد لعبة نشطة بالفعل\nاكتب "إيقاف" لإنهائها')
            return

        try:
            with ApiClient(configuration) as api_client:
                line_api = MessagingApi(api_client)
                game_class = GAMES[txt]
                game = game_class(line_api)
                game.set_theme(get_theme(uid))
                gm.start_game(gid, game, txt)
                response = game.start_game()
                send_flex_reply(event.reply_token, response, uid, f'لعبة {txt}')
                logger.info(f'✅ Game started: {txt} in {gid} by {name}')
        except Exception as e:
            logger.error(f'❌ Error starting game {txt}: {e}', exc_info=True)
            send_text_reply(event.reply_token, '❌ حدث خطأ أثناء بدء اللعبة')
        return

    # الرد على اللعبة
    game_data = gm.get_game(gid)
    if game_data and gm.is_registered(uid):
        game = game_data['game']
        
        if gm.has_answered(gid, uid):
            # User already answered
            return
        
        try:
            result = game.check_answer(txt, uid, name)
            if result:
                gm.mark_answered(gid, uid)
                points = result.get('points', 0)
                won = result.get('won', False)
                db.update_points(uid, points, won)
                response = result.get('response')
                
                if response:
                    send_flex_reply(event.reply_token, response, uid, 'نتيجة')
                    logger.info(f'✅ Answer from {name}: {"✓" if won else "✗"} (+{points} points)')
                
                # Check if game should end
                if result.get('game_over'):
                    gm.end_game(gid)
                    
        except Exception as e:
            logger.error(f'❌ Error checking answer: {e}', exc_info=True)
        return

# ==================== Background Tasks ====================
def cleanup_task():
    """Periodic cleanup task"""
    try:
        db.cleanup_names()
        cache.clear()
        logger.info('✅ Cleanup completed')
    except Exception as e:
        logger.error(f'❌ Cleanup error: {e}')

# ==================== Run ====================
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    logger.info("🚀 Bot Mesh v3.0.0 - Running on port %s", port)
    logger.info(f"📊 Loaded {len(GAMES)} games: {', '.join(GAMES.keys())}")
    app.run(host='0.0.0.0', port=port, debug=False)
