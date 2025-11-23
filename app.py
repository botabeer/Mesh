"""
Bot Mesh - Main Application (v3 SDK)
Created by: Abeer Aldosari © 2025
"""
import os
import logging
from flask import Flask, request, abort, jsonify

# LINE SDK v3
from linebot.v3 import WebhookHandler
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi,
    ReplyMessageRequest, TextMessage, FlexMessage, FlexContainer,
    QuickReply, QuickReplyItem, MessageAction
)
from linebot.v3.webhooks import (
    MessageEvent, FollowEvent, TextMessageContent
)
from linebot.v3.exceptions import InvalidSignatureError

# استيراد المكونات
from config import LINE_TOKEN, LINE_SECRET, DB_PATH, THEMES
from database import DB
from flex_builder import FlexBuilder
from game_manager import GameManager

# ==================== Logging ====================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ==================== Flask & Line ====================
app = Flask(__name__)

# إعداد LINE SDK v3
configuration = Configuration(access_token=LINE_TOKEN)
handler = WebhookHandler(LINE_SECRET)

db = DB(DB_PATH)
gm = GameManager()

# ==================== قاموس الألعاب ====================
GAMES = {}

# استيراد جميع الألعاب
try:
    from games import *
    from games.base_game import BaseGame
    import games
    import inspect
    
    # البحث عن جميع الكلاسات الفرعية من BaseGame
    for name, obj in inspect.getmembers(games):
        if inspect.isclass(obj) and issubclass(obj, BaseGame) and obj != BaseGame:
            # استخراج اسم اللعبة من اسم الكلاس
            game_name = name.replace('Game', '').replace('AI', '')
            logger.info(f"✅ Game loaded: {game_name} -> {name}")
    
    # تعريف القاموس الرسمي
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
    logger.info(f"✅ Total games loaded: {len(GAMES)}")
except Exception as e:
    logger.error(f"❌ Failed to load games: {e}")

# ==================== Helpers ====================
def get_name(uid):
    """الحصول على اسم المستخدم من LINE"""
    try:
        with ApiClient(configuration) as api_client:
            api = MessagingApi(api_client)
            profile = api.get_profile(uid)
            return profile.display_name
    except Exception as e:
        logger.error(f"❌ Error getting user profile: {e}")
        return 'لاعب'

def get_theme(uid):
    """الحصول على ثيم المستخدم"""
    user = db.get_user(uid)
    return user.get('theme', 'white') if user else 'white'

def get_games_quick_reply():
    """إنشاء قائمة سريعة للألعاب"""
    items = []
    
    # إضافة الألعاب
    for label in GAMES.keys():
        items.append(
            QuickReplyItem(
                action=MessageAction(label=label, text=label)
            )
        )
    
    # إضافة الأوامر
    commands = [
        ('انضم', 'انضم'),
        ('انسحب', 'انسحب'),
        ('إيقاف', 'إيقاف'),
        ('ترتيب', 'ترتيب')
    ]
    
    for label, text in commands:
        items.append(
            QuickReplyItem(
                action=MessageAction(label=label, text=text)
            )
        )
    
    return QuickReply(items=items[:13])  # LINE يدعم حتى 13 عنصر

def send_flex_reply(reply_token, flex_content, with_quick_reply=True):
    """إرسال رد Flex مع قائمة سريعة"""
    try:
        with ApiClient(configuration) as api_client:
            api = MessagingApi(api_client)
            
            messages = [
                FlexMessage(
                    alt_text='Bot Mesh',
                    contents=FlexContainer.from_dict(flex_content)
                )
            ]
            
            # إضافة رسالة نصية مع القائمة السريعة
            if with_quick_reply:
                messages.append(
                    TextMessage(
                        text="اختر لعبة أو أمر:",
                        quick_reply=get_games_quick_reply()
                    )
                )
            
            api.reply_message(
                ReplyMessageRequest(
                    reply_token=reply_token,
                    messages=messages
                )
            )
    except Exception as e:
        logger.error(f"❌ Error sending flex reply: {e}")

def send_text_reply(reply_token, text, with_quick_reply=True):
    """إرسال رد نصي"""
    try:
        with ApiClient(configuration) as api_client:
            api = MessagingApi(api_client)
            
            message = TextMessage(text=text)
            if with_quick_reply:
                message.quick_reply = get_games_quick_reply()
            
            api.reply_message(
                ReplyMessageRequest(
                    reply_token=reply_token,
                    messages=[message]
                )
            )
    except Exception as e:
        logger.error(f"❌ Error sending text reply: {e}")

# ==================== Routes ====================
@app.route('/')
def home():
    return jsonify({
        'status': 'active',
        'bot': 'Bot Mesh',
        'version': '2.0.0',
        'author': 'Abeer Aldosari'
    })

@app.route('/health')
def health():
    """فحص صحة البوت"""
    stats = db.get_stats()
    return jsonify({
        'status': 'ok',
        'active_games': gm.get_active_games_count(),
        'registered_users': gm.get_users_count(),
        'total_games': len(GAMES),
        'themes': len(THEMES),
        'database': stats
    })

@app.route('/callback', methods=['POST'])
def callback():
    """استقبال أحداث LINE"""
    signature = request.headers.get('X-Line-Signature')
    if not signature:
        logger.error("❌ Missing signature")
        abort(400)
    
    body = request.get_data(as_text=True)
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        logger.error("❌ Invalid signature")
        abort(400)
    except Exception as e:
        logger.error(f"❌ Error handling request: {e}")
        abort(500)
    
    return 'OK'

# ==================== Event Handlers ====================
@handler.add(FollowEvent)
def handle_follow(event):
    """عند متابعة البوت"""
    uid = event.source.user_id
    name = get_name(uid)
    db.add_or_update_user(uid, name)
    
    builder = FlexBuilder('white')
    send_flex_reply(event.reply_token, builder.welcome(name))
    logger.info(f"✅ New follower: {name} ({uid})")

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    """معالجة الرسائل النصية"""
    uid = event.source.user_id
    txt = event.message.text.strip()
    
    # تحديد معرف المجموعة أو الشات
    if hasattr(event.source, 'group_id'):
        gid = event.source.group_id
    elif hasattr(event.source, 'room_id'):
        gid = event.source.room_id
    else:
        gid = uid
    
    name = get_name(uid)
    db.add_or_update_user(uid, name)
    theme = get_theme(uid)
    builder = FlexBuilder(theme)
    
    # ==== انضم ====
    if txt == 'انضم':
        gm.register(uid)
        send_flex_reply(event.reply_token, builder.welcome(name))
        logger.info(f"✅ User joined: {name}")
        return
    
    # ==== انسحب ====
    if txt == 'انسحب':
        gm.unregister(uid)
        send_text_reply(event.reply_token, '✅ تم الانسحاب، لن تُحسب إجاباتك')
        logger.info(f"✅ User left: {name}")
        return
    
    # ==== إيقاف ====
    if txt == 'إيقاف':
        if gm.get_game(gid):
            gm.end_game(gid)
            send_text_reply(event.reply_token, '⛔ تم إيقاف اللعبة')
            logger.info(f"✅ Game stopped in {gid}")
        else:
            send_text_reply(event.reply_token, '⚠️ لا توجد لعبة نشطة')
        return
    
    # ==== تغيير الثيم ====
    if txt.startswith('ثيم:'):
        theme_name = txt.split(':')[1].strip()
        if theme_name in THEMES:
            db.update_theme(uid, theme_name)
            builder = FlexBuilder(theme_name)
            send_flex_reply(
                event.reply_token,
                builder.welcome(name)
            )
            logger.info(f"✅ Theme changed for {name}: {theme_name}")
        else:
            send_text_reply(event.reply_token, '❌ ثيم غير موجود')
        return
    
    # ==== ترتيب (Leaderboard) ====
    if txt == 'ترتيب':
        leaderboard = db.get_leaderboard(10)
        if leaderboard:
            send_flex_reply(
                event.reply_token,
                builder.leaderboard(leaderboard)
            )
        else:
            send_text_reply(event.reply_token, '📊 لا توجد بيانات بعد')
        return
    
    # ==== بدء لعبة ====
    if txt in GAMES:
        if not gm.is_registered(uid):
            send_text_reply(event.reply_token, '❌ اكتب "انضم" أولاً للتسجيل')
            logger.warning(f"⚠️ Unregistered user tried to start game: {name}")
            return
        
        if gm.get_game(gid):
            send_text_reply(event.reply_token, '⚠️ يوجد لعبة نشطة بالفعل')
            return
        
        try:
            game_class = GAMES[txt]
            
            # إنشاء اللعبة مع API client
            with ApiClient(configuration) as api_client:
                api = MessagingApi(api_client)
                game = game_class(api)
                game.set_theme(theme)
                
                gm.start_game(gid, game, txt)
                response = game.start_game()
                send_flex_reply(event.reply_token, response)
                logger.info(f"✅ Game started: {txt} by {name} in {gid}")
        except Exception as e:
            logger.error(f"❌ Error starting game: {e}")
            send_text_reply(event.reply_token, '❌ حدث خطأ في بدء اللعبة')
        return
    
    # ==== الرد على اللعبة ====
    game_data = gm.get_game(gid)
    if game_data and gm.is_registered(uid):
        game = game_data['game']
        game_type = game_data['type']
        
        # التحقق: هل اللاعب أجاب من قبل؟
        if gm.has_answered(gid, uid):
            logger.debug(f"⚠️ User {name} already answered")
            return
        
        try:
            # فحص الإجابة
            result = game.check_answer(txt, uid, name)
            
            if result:
                # تسجيل الإجابة
                gm.mark_answered(gid, uid)
                
                points = result.get('points', 0)
                won = result.get('won', False)
                response = result.get('response')
                
                # تحديث النقاط في قاعدة البيانات
                db.update_points(uid, points, won)
                db.add_game_stat(uid, game_type, points, won)
                
                # إرسال الرد
                if response:
                    send_flex_reply(event.reply_token, response)
                
                logger.info(f"✅ Correct answer by {name}: +{points} pts")
                
                # إنهاء اللعبة إذا انتهت
                if won or result.get('game_over', False):
                    gm.end_game(gid)
                    logger.info(f"✅ Game ended in {gid}")
        except Exception as e:
            logger.error(f"❌ Error checking answer: {e}")

# ==================== تنظيف دوري ====================
@app.before_request
def periodic_cleanup():
    """تنظيف دوري للبيانات القديمة"""
    import random
    # تنظيف عشوائي (1% احتمال)
    if random.random() < 0.01:
        db.cleanup_inactive_users(7)
        gm.cleanup_old_games()

# ==================== Run ====================
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    logger.info(f"🚀 Bot Mesh v2.0.0 starting on port {port}")
    logger.info(f"📊 Games available: {len(GAMES)}")
    logger.info(f"🎨 Themes available: {len(THEMES)}")
    app.run(host='0.0.0.0', port=port, debug=False)
