"""
Bot Mesh v7.0 - Production Ready with Database
نظام متكامل مع قاعدة بيانات وتسجيل تلقائي للأسماء
Created by: Abeer Aldosari © 2025
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
from linebot.v3.webhooks import MessageEvent, TextMessageContent, FollowEvent, JoinEvent

from config import Config
from database import Database
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

# تهيئة الأنظمة
db = Database()
ui = UI()
game_loader = GameLoader()

# =====================================================
# ذاكرة مؤقتة للأداء
# =====================================================

user_cache = {}
cache_lock = Lock()
CACHE_TIMEOUT = 300  # 5 دقائق

active_games = {}
games_lock = Lock()

rate_limiter = defaultdict(list)
rate_lock = Lock()

# =====================================================
# أدوات مساعدة
# =====================================================

def get_cached_user(user_id: str):
    """جلب مستخدم من الذاكرة المؤقتة أو قاعدة البيانات"""
    with cache_lock:
        # التحقق من الذاكرة المؤقتة
        if user_id in user_cache:
            cached_data, cached_time = user_cache[user_id]
            if (datetime.now() - cached_time).seconds < CACHE_TIMEOUT:
                return cached_data
        
        # جلب من قاعدة البيانات
        user_data = db.get_user(user_id)
        if user_data:
            user_cache[user_id] = (user_data, datetime.now())
            return user_data
        
        return None

def update_user_cache(user_id: str, user_data: dict):
    """تحديث الذاكرة المؤقتة"""
    with cache_lock:
        user_cache[user_id] = (user_data, datetime.now())

def get_or_create_user(user_id: str, display_name: str = None):
    """جلب أو إنشاء مستخدم مع التحديث التلقائي للاسم"""
    user_data = get_cached_user(user_id)
    
    if not user_data:
        # مستخدم جديد
        name = display_name or "مستخدم"
        user_data = db.create_user(user_id, name)
        update_user_cache(user_id, user_data)
        logger.info(f"✅ مستخدم جديد: {name}")
    else:
        # مستخدم موجود - تحديث الاسم إذا تغير
        if display_name and display_name != user_data['display_name']:
            db.update_user_name(user_id, display_name)
            user_data['display_name'] = display_name
            update_user_cache(user_id, user_data)
            logger.info(f"✅ تم تحديث الاسم: {display_name}")
        
        # تحديث آخر نشاط
        db.update_last_active(user_id)
    
    return user_data

def get_user_display_name(event):
    """جلب اسم المستخدم من LINE API"""
    try:
        with ApiClient(configuration) as api_client:
            line_api = MessagingApi(api_client)
            profile = line_api.get_profile(event.source.user_id)
            return profile.display_name
    except:
        return None

def check_rate_limit(user_id: str) -> bool:
    """فحص معدل الرسائل"""
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
    """تطبيع النص العربي"""
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
    """تنظيف الألعاب المنتهية"""
    with games_lock:
        expired = []
        for user_id, game in active_games.items():
            if hasattr(game, 'is_expired') and game.is_expired(Config.GAME_TIMEOUT_MINUTES):
                expired.append(user_id)
        
        for user_id in expired:
            del active_games[user_id]
            db.delete_active_game(user_id)
        
        if expired:
            logger.info(f"🧹 تم حذف {len(expired)} لعبة منتهية")

# =====================================================
# Webhook Events
# =====================================================

@app.route("/callback", methods=['POST'])
def callback():
    """معالج الـ Webhook"""
    signature = request.headers.get('X-Line-Signature')
    body = request.get_data(as_text=True)
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        logger.error("Invalid signature")
        abort(400)
    except Exception as e:
        logger.error(f"Webhook error: {traceback.format_exc()}")
        abort(500)
    
    return "OK"

@handler.add(FollowEvent)
def handle_follow(event):
    """معالج الإضافة (Follow)"""
    user_id = event.source.user_id
    display_name = get_user_display_name(event)
    
    # إنشاء مستخدم جديد
    user_data = get_or_create_user(user_id, display_name)
    
    with ApiClient(configuration) as api_client:
        line_api = MessagingApi(api_client)
        welcome_msg = TextMessage(
            text=f"مرحباً {user_data['display_name']}! 🎮\n\n"
                 f"أهلاً بك في Bot Mesh\n"
                 f"اكتب 'بداية' للبدء"
        )
        line_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[welcome_msg]
            )
        )

@handler.add(JoinEvent)
def handle_join(event):
    """معالج الانضمام للمجموعة"""
    logger.info("✅ تم إضافة البوت لمجموعة")
    
    with ApiClient(configuration) as api_client:
        line_api = MessagingApi(api_client)
        welcome_msg = TextMessage(
            text="مرحباً! 🎮\n\n"
                 "أنا Bot Mesh - بوت الألعاب الترفيهي\n"
                 "اكتب 'بداية' للبدء"
        )
        line_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[welcome_msg]
            )
        )

# =====================================================
# معالج الرسائل
# =====================================================

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    """معالج الرسائل الرئيسي"""
    user_id = event.source.user_id
    text = event.message.text.strip()
    
    # فحص معدل الرسائل
    if not check_rate_limit(user_id):
        return
    
    try:
        with ApiClient(configuration) as api_client:
            line_api = MessagingApi(api_client)
            
            # جلب اسم المستخدم من LINE
            display_name = get_user_display_name(event)
            
            # جلب أو إنشاء المستخدم (مع تحديث تلقائي للاسم)
            user_data = get_or_create_user(user_id, display_name)
            username = user_data['display_name']
            theme = user_data['theme']
            
            normalized = normalize_text(text)
            response = None
            
            # -----------------------------
            # الصفحة الرئيسية
            # -----------------------------
            if normalized in ['بدايه', 'ابدا', 'البدايه', 'بداية']:
                response = ui.build_home(username, user_data['points'], theme)
            
            # -----------------------------
            # قائمة الألعاب
            # -----------------------------
            elif normalized in ['العاب', 'الالعاب']:
                response = ui.build_games_menu(theme)
            
            # -----------------------------
            # نقاط المستخدم
            # -----------------------------
            elif normalized in ['نقاطي']:
                rank = db.get_user_rank(user_id)
                response = ui.build_user_stats(username, user_data, rank, theme)
            
            # -----------------------------
            # لوحة الصدارة
            # -----------------------------
            elif normalized in ['صداره', 'الصدارة', 'صدارة']:
                leaderboard = db.get_leaderboard(10)
                response = ui.build_leaderboard(leaderboard, theme)
            
            # -----------------------------
            # المساعدة
            # -----------------------------
            elif normalized in ['مساعده', 'مساعدة', 'help']:
                response = ui.build_help(theme)
            
            # -----------------------------
            # تغيير الثيم
            # -----------------------------
            elif text.startswith('ثيم '):
                new_theme = text.replace('ثيم ', '').strip()
                
                if new_theme in ui.THEMES:
                    db.update_theme(user_id, new_theme)
                    user_data['theme'] = new_theme
                    update_user_cache(user_id, user_data)
                    
                    response = ui.build_home(username, user_data['points'], new_theme)
                else:
                    available_themes = ", ".join(ui.THEMES.keys())
                    response = TextMessage(
                        text=f"الثيمات المتاحة:\n{available_themes}"
                    )
            
            # -----------------------------
            # بدء لعبة
            # -----------------------------
            elif normalized.startswith('لعبة ') or normalized.startswith('لعبه '):
                game_name = text.replace('لعبة ', '').replace('لعبه ', '').strip()
                
                # حذف اللعبة القديمة
                with games_lock:
                    active_games.pop(user_id, None)
                db.delete_active_game(user_id)
                
                # إنشاء لعبة جديدة
                game = game_loader.create_game(game_name)
                
                if not game:
                    response = TextMessage(text=f"اللعبة '{game_name}' غير موجودة")
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
                    # اللعبة انتهت
                    with games_lock:
                        active_games.pop(user_id, None)
                    db.delete_active_game(user_id)
                    
                    points = result.get('points', 0)
                    
                    # تحديث قاعدة البيانات
                    if points > 0:
                        db.add_points(user_id, points)
                        db.increment_games(user_id, won=True)
                    else:
                        db.increment_games(user_id, won=False)
                    
                    db.log_game_history(user_id, game.name, points, True)
                    
                    # تحديث الذاكرة المؤقتة
                    user_data['points'] += points
                    user_data['games_played'] += 1
                    if points > 0:
                        user_data['wins'] += 1
                    update_user_cache(user_id, user_data)
                    
                    response = ui.build_game_result(game.name, points, theme)
                
                else:
                    # سؤال تالي
                    q = result.get('next_question')
                    if q:
                        response = ui.build_game_question(
                            game.name,
                            q['text'],
                            q['round'],
                            q['total_rounds'],
                            theme
                        )
                    else:
                        response = TextMessage(text=result.get('message', 'حاول مرة أخرى'))
            
            # -----------------------------
            # أمر انضم (تسجيل يدوي)
            # -----------------------------
            elif normalized in ['انضم', 'تسجيل']:
                # المستخدم مسجل تلقائياً عند أول رسالة
                response = TextMessage(
                    text=f"✅ أنت مسجل بالفعل يا {username}!\n"
                         f"النقاط: {user_data['points']}\n"
                         f"الألعاب: {user_data['games_played']}"
                )
            
            # -----------------------------
            # رسالة افتراضية
            # -----------------------------
            else:
                response = TextMessage(
                    text="اكتب 'بداية' للبدء\n"
                         "أو 'العاب' لعرض قائمة الألعاب"
                )
            
            # إرسال الرد
            if response:
                line_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[response]
                    )
                )
    
    except Exception as e:
        logger.error(f"Message handling error: {traceback.format_exc()}")

# =====================================================
# تنظيف دوري
# =====================================================

@app.before_request
def before_request():
    """تنفيذ قبل كل طلب"""
    cleanup_expired_games()

# =====================================================
# مسارات إضافية
# =====================================================

@app.route("/health", methods=['GET'])
def health_check():
    """فحص صحة البوت"""
    stats = {
        "status": "healthy",
        "total_users": db.get_total_users(),
        "total_games": db.get_total_games_played(),
        "active_games": len(active_games),
        "timestamp": datetime.now().isoformat()
    }
    return stats, 200

@app.route("/", methods=['GET'])
def index():
    """الصفحة الرئيسية"""
    return """
    <html>
        <head><title>Bot Mesh v7.0</title></head>
        <body style="font-family: Arial; text-align: center; padding: 50px;">
            <h1>🎮 Bot Mesh v7.0</h1>
            <p>بوت LINE للألعاب الترفيهية</p>
            <p>Created by: Abeer Aldosari © 2025</p>
        </body>
    </html>
    """, 200

# =====================================================
# تشغيل التطبيق
# =====================================================

if __name__ == "__main__":
    # تحسين قاعدة البيانات عند البدء
    db.optimize_database()
    
    port = int(os.getenv("PORT", 10000))
    logger.info(f"🚀 Bot Mesh v7.0 يعمل على المنفذ {port}")
    app.run(host="0.0.0.0", port=port, debug=False)
