"""
🎮 Bot Mesh v7.0 - Production Ready
Created by: Abeer Aldosari © 2025

✨ بوت ألعاب احترافي لمنصة LINE
- 12 لعبة تفاعلية
- دعم اللعب الفردي والمجموعة
- نظام نقاط ذكي
- تصميم ثلاثي الأبعاد
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

# استيراد الوحدات المحلية
from config import Config
from ui import UI
from game_loader import GameLoader

# ============================================================================
# إعداد التطبيق
# ============================================================================

app = Flask(__name__)

# إعداد السجلات
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# التحقق من الإعدادات
config_valid, config_errors = Config.validate()
if not config_valid:
    logger.warning("⚠️ تحذير: إعدادات غير كاملة")
    for error in config_errors:
        logger.warning(f"   - {error}")
    logger.warning("⚠️ البوت يعمل في وضع التطوير")

# إعداد LINE SDK
configuration = Configuration(access_token=Config.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(Config.LINE_CHANNEL_SECRET)

# إعداد واجهة المستخدم
ui = UI()

# إعداد مدير الألعاب
game_loader = GameLoader()

# تخزين بيانات المستخدمين والألعاب في الذاكرة
users_data = defaultdict(lambda: {
    'name': 'مستخدم',
    'points': 0,
    'games_played': 0,
    'wins': 0,
    'theme': '💜',
    'last_activity': datetime.now()
})

active_games = {}  # {user_id: game_instance}
users_lock = Lock()
games_lock = Lock()

# Rate Limiting
rate_limiter = defaultdict(list)
rate_lock = Lock()

# ============================================================================
# Helper Functions
# ============================================================================

def check_rate_limit(user_id: str) -> bool:
    """فحص حد الرسائل"""
    with rate_lock:
        now = datetime.now()
        cutoff = now - timedelta(seconds=60)
        
        rate_limiter[user_id] = [
            msg_time for msg_time in rate_limiter[user_id]
            if msg_time > cutoff
        ]
        
        if len(rate_limiter[user_id]) >= Config.MAX_MESSAGES_PER_MINUTE:
            return False
        
        rate_limiter[user_id].append(now)
        return True

def get_user_profile(api: MessagingApi, user_id: str) -> dict:
    """جلب معلومات المستخدم من LINE"""
    try:
        profile = api.get_profile(user_id)
        return {
            'user_id': user_id,
            'name': profile.display_name or 'مستخدم',
            'picture': getattr(profile, 'picture_url', None)
        }
    except Exception as e:
        logger.error(f"خطأ في جلب الملف الشخصي: {e}")
        return {'user_id': user_id, 'name': 'مستخدم', 'picture': None}

def normalize_text(text: str) -> str:
    """تطبيع النص العربي"""
    import re
    text = text.strip().lower()
    
    replacements = {
        'أ': 'ا', 'إ': 'ا', 'آ': 'ا', 'ء': 'ا',
        'ى': 'ي', 'ة': 'ه', 'ؤ': 'و', 'ئ': 'ي'
    }
    
    for old, new in replacements.items():
        text = text.replace(old, new)
    
    text = re.sub(r'[\u064B-\u065F\u0670]', '', text)
    return text

def add_user_points(user_id: str, points: int):
    """إضافة نقاط للمستخدم"""
    with users_lock:
        users_data[user_id]['points'] += points
        users_data[user_id]['last_activity'] = datetime.now()

def get_user_data(user_id: str) -> dict:
    """الحصول على بيانات المستخدم"""
    with users_lock:
        users_data[user_id]['last_activity'] = datetime.now()
        return users_data[user_id].copy()

def update_user_name(user_id: str, name: str):
    """تحديث اسم المستخدم"""
    with users_lock:
        users_data[user_id]['name'] = name
        users_data[user_id]['last_activity'] = datetime.now()

def get_leaderboard(limit: int = 10) -> list:
    """الحصول على لوحة الصدارة"""
    with users_lock:
        sorted_users = sorted(
            [
                {
                    'name': data['name'],
                    'points': data['points'],
                    'games_played': data['games_played'],
                    'wins': data['wins']
                }
                for data in users_data.values()
            ],
            key=lambda x: x['points'],
            reverse=True
        )
        return sorted_users[:limit]

def get_user_rank(user_id: str) -> int:
    """الحصول على ترتيب المستخدم"""
    with users_lock:
        user_points = users_data[user_id]['points']
        rank = 1
        for data in users_data.values():
            if data['points'] > user_points:
                rank += 1
        return rank

def cleanup_expired_games():
    """تنظيف الألعاب المنتهية"""
    with games_lock:
        expired = []
        for user_id, game in active_games.items():
            if hasattr(game, 'is_expired') and game.is_expired(Config.GAME_TIMEOUT_MINUTES):
                expired.append(user_id)
        
        for user_id in expired:
            del active_games[user_id]
        
        if expired:
            logger.info(f"🧹 تم حذف {len(expired)} ألعاب منتهية")

# ============================================================================
# Routes
# ============================================================================

@app.route("/", methods=['GET'])
def home():
    """الصفحة الرئيسية"""
    total_users = len(users_data)
    total_points = sum(data['points'] for data in users_data.values())
    active_games_count = len(active_games)
    available_games = len(game_loader.games)
    
    return f"""
    <!DOCTYPE html>
    <html dir="rtl" lang="ar">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Bot Mesh v7.0 - بوت الألعاب الذكي</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Segoe UI', 'Cairo', Tahoma, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 20px;
            }}
            
            .container {{
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(20px);
                border-radius: 30px;
                padding: 40px;
                box-shadow: 
                    0 20px 60px rgba(0,0,0,0.3),
                    inset 0 1px 0 rgba(255,255,255,0.6);
                max-width: 600px;
                width: 100%;
                animation: slideUp 0.5s ease-out;
            }}
            
            @keyframes slideUp {{
                from {{
                    opacity: 0;
                    transform: translateY(30px);
                }}
                to {{
                    opacity: 1;
                    transform: translateY(0);
                }}
            }}
            
            h1 {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                font-size: 2.8em;
                margin-bottom: 10px;
                text-align: center;
                font-weight: 800;
            }}
            
            .subtitle {{
                text-align: center;
                color: #718096;
                font-size: 1.1em;
                margin-bottom: 30px;
            }}
            
            .status {{
                background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
                color: white;
                padding: 25px;
                border-radius: 20px;
                margin: 25px 0;
                text-align: center;
                font-size: 1.3em;
                font-weight: bold;
                box-shadow: 0 10px 25px rgba(72, 187, 120, 0.3);
            }}
            
            .stats {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
                gap: 15px;
                margin: 25px 0;
            }}
            
            .stat-box {{
                background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
                padding: 25px 20px;
                border-radius: 20px;
                text-align: center;
                transition: transform 0.3s ease, box-shadow 0.3s ease;
                box-shadow: 
                    5px 5px 15px rgba(0,0,0,0.1),
                    -5px -5px 15px rgba(255,255,255,0.9);
            }}
            
            .stat-box:hover {{
                transform: translateY(-5px);
                box-shadow: 
                    8px 8px 20px rgba(0,0,0,0.15),
                    -8px -8px 20px rgba(255,255,255,1);
            }}
            
            .stat-icon {{
                font-size: 2.5em;
                margin-bottom: 10px;
            }}
            
            .stat-value {{
                font-size: 2em;
                font-weight: bold;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                margin: 10px 0;
            }}
            
            .stat-label {{
                color: #718096;
                font-size: 0.9em;
                font-weight: 600;
            }}
            
            .features {{
                background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
                padding: 25px;
                border-radius: 20px;
                margin: 25px 0;
                box-shadow: 
                    5px 5px 15px rgba(0,0,0,0.1),
                    -5px -5px 15px rgba(255,255,255,0.9);
            }}
            
            .features h3 {{
                color: #667eea;
                margin-bottom: 15px;
                font-size: 1.3em;
            }}
            
            .features ul {{
                list-style: none;
                padding: 0;
            }}
            
            .features li {{
                padding: 10px 0;
                color: #4a5568;
                font-size: 1em;
                border-bottom: 1px solid #e2e8f0;
            }}
            
            .features li:last-child {{
                border-bottom: none;
            }}
            
            .features li:before {{
                content: "✨ ";
                margin-left: 10px;
            }}
            
            .footer {{
                text-align: center;
                margin-top: 30px;
                padding-top: 20px;
                border-top: 2px solid #e2e8f0;
                color: #718096;
                font-size: 0.95em;
            }}
            
            .footer a {{
                color: #667eea;
                text-decoration: none;
                font-weight: 600;
            }}
            
            .version {{
                display: inline-block;
                background: #667eea;
                color: white;
                padding: 5px 15px;
                border-radius: 20px;
                font-size: 0.85em;
                margin: 10px 0;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎮 Bot Mesh</h1>
            <p class="subtitle">بوت الألعاب الترفيهية الذكي</p>
            <span class="version">v7.0 Production</span>
            
            <div class="status">
                ✅ البوت يعمل بكفاءة عالية
            </div>
            
            <div class="stats">
                <div class="stat-box">
                    <div class="stat-icon">👥</div>
                    <div class="stat-value">{total_users}</div>
                    <div class="stat-label">المستخدمون</div>
                </div>
                
                <div class="stat-box">
                    <div class="stat-icon">🎮</div>
                    <div class="stat-value">{available_games}</div>
                    <div class="stat-label">الألعاب</div>
                </div>
                
                <div class="stat-box">
                    <div class="stat-icon">⭐</div>
                    <div class="stat-value">{total_points}</div>
                    <div class="stat-label">النقاط</div>
                </div>
                
                <div class="stat-box">
                    <div class="stat-icon">🔥</div>
                    <div class="stat-value">{active_games_count}</div>
                    <div class="stat-label">ألعاب نشطة</div>
                </div>
            </div>
            
            <div class="features">
                <h3>✨ المميزات الرئيسية</h3>
                <ul>
                    <li>9 ثيمات احترافية قابلة للتبديل</li>
                    <li>تصميم Glass Morphism ثلاثي الأبعاد</li>
                    <li>12 لعبة تفاعلية ممتعة</li>
                    <li>نظام نقاط ولوحة صدارة</li>
                    <li>دعم اللعب الفردي والمجموعة</li>
                    <li>واجهات Flex Messages احترافية</li>
                </ul>
            </div>
            
            <div class="footer">
                <p>© 2025 تم إنشاؤه بواسطة <a href="#">عبير الدوسري</a></p>
                <p>جميع الحقوق محفوظة</p>
            </div>
        </div>
    </body>
    </html>
    """

@app.route("/health", methods=['GET'])
def health():
    """فحص الصحة"""
    return {
        "status": "healthy",
        "version": "7.0",
        "games": len(game_loader.games),
        "active_games": len(active_games),
        "users": len(users_data),
        "timestamp": datetime.now().isoformat()
    }, 200

@app.route("/callback", methods=['POST'])
def callback():
    """معالج Webhook من LINE"""
    signature = request.headers.get('X-Line-Signature', '')
    body = request.get_data(as_text=True)
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        logger.error("❌ توقيع غير صالح")
        abort(400)
    except Exception as e:
        logger.error(f"❌ خطأ في المعالجة: {e}")
        logger.error(traceback.format_exc())
        abort(500)
    
    return 'OK'

# ============================================================================
# Message Handler
# ============================================================================

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    """معالج الرسائل الرئيسي"""
    user_id = event.source.user_id
    text = event.message.text.strip()
    
    # Rate Limiting
    if not check_rate_limit(user_id):
        logger.warning(f"⚠️ تجاوز الحد: {user_id}")
        return
    
    try:
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            
            # جلب معلومات المستخدم
            user_profile = get_user_profile(line_bot_api, user_id)
            username = user_profile['name']
            update_user_name(user_id, username)
            
            # تطبيع النص
            normalized_text = normalize_text(text)
            
            # الحصول على بيانات المستخدم
            user_data = get_user_data(user_id)
            current_theme = user_data['theme']
            
            # معالجة الأوامر
            response = None
            
            # ============================================================
            # تغيير الثيم
            # ============================================================
            if text.startswith('ثيم '):
                theme_emoji = text.replace('ثيم ', '').strip()
                if theme_emoji in ui.THEMES:
                    with users_lock:
                        users_data[user_id]['theme'] = theme_emoji
                    user_data = get_user_data(user_id)
                    response = ui.build_home(username, user_data['points'], theme_emoji)
                else:
                    response = TextMessage(text="❌ ثيم غير موجود")
            
            # ============================================================
            # الصفحة الرئيسية
            # ============================================================
            elif normalized_text in ['بداية', 'البداية', 'ابدا', 'start', 'home']:
                response = ui.build_home(username, user_data['points'], current_theme)
            
            # ============================================================
            # قائمة الألعاب
            # ============================================================
            elif normalized_text in ['العاب', 'ألعاب', 'games', 'مساعدة', 'مساعده', 'info']:
                response = ui.build_games_menu(current_theme)
            
            # ============================================================
            # نقاطي
            # ============================================================
            elif normalized_text in ['نقاطي', 'points', 'نقاط']:
                rank = get_user_rank(user_id)
                response = ui.build_user_stats(username, user_data, rank, current_theme)
            
            # ============================================================
            # الصدارة
            # ============================================================
            elif normalized_text in ['صدارة', 'الصدارة', 'leaderboard']:
                leaderboard = get_leaderboard(10)
                response = ui.build_leaderboard(leaderboard, current_theme)
            
            # ============================================================
            # إيقاف اللعبة
            # ============================================================
            elif normalized_text in ['ايقاف', 'إيقاف', 'stop']:
                with games_lock:
                    if user_id in active_games:
                        del active_games[user_id]
                        response = TextMessage(text="⛔ تم إيقاف اللعبة")
                    else:
                        response = TextMessage(text="لا توجد لعبة نشطة")
            
            # ============================================================
            # بدء لعبة
            # ============================================================
            elif text.startswith('لعبة '):
                game_name = text.replace('لعبة ', '').strip()
                
                # إيقاف اللعبة السابقة
                with games_lock:
                    if user_id in active_games:
                        del active_games[user_id]
                
                # إنشاء لعبة جديدة
                game = game_loader.create_game(game_name)
                
                if game:
                    with games_lock:
                        active_games[user_id] = game
                    
                    game.start()
                    question = game.get_question()
                    response = ui.build_game_question(
                        game.name,
                        question['text'],
                        question['round'],
                        question['total_rounds'],
                        current_theme
                    )
                else:
                    response = TextMessage(text=f"❌ لعبة '{game_name}' غير موجودة")
            
            # ============================================================
            # إجابة على سؤال
            # ============================================================
            elif user_id in active_games:
                with games_lock:
                    game = active_games.get(user_id)
                
                if game:
                    result = game.check_answer(text, user_id, username)
                    
                    if result.get('game_over'):
                        # انتهت اللعبة
                        total_points = result.get('points', 0)
                        
                        if total_points > 0:
                            add_user_points(user_id, total_points)
                            with users_lock:
                                users_data[user_id]['games_played'] += 1
                                users_data[user_id]['wins'] += 1
                        
                        response = ui.build_game_result(
                            game.name,
                            total_points,
                            current_theme
                        )
                        
                        with games_lock:
                            if user_id in active_games:
                                del active_games[user_id]
                    
                    elif result.get('correct'):
                        # إجابة صحيحة
                        next_question = result.get('next_question')
                        points = result.get('points', 10)
                        
                        if next_question:
                            response = ui.build_game_question(
                                game.name,
                                next_question['text'],
                                next_question['round'],
                                next_question['total_rounds'],
                                current_theme,
                                f"✅ صحيح! +{points} نقطة"
                            )
                        else:
                            response = TextMessage(
                                text=f"✅ {result.get('message', 'إجابة صحيحة')}"
                            )
                    
                    elif result.get('hint'):
                        # تلميح
                        response = TextMessage(text=result['hint'])
                    
                    else:
                        # رسالة عامة
                        message = result.get('message', 'حاول مرة أخرى')
                        response = TextMessage(text=message)
            
            # ============================================================
            # رسالة افتراضية
            # ============================================================
            else:
                response = TextMessage(
                    text="مرحباً! 👋\n\nاكتب 'بداية' للبدء\nأو 'العاب' لرؤية الألعاب المتاحة 🎮"
                )
            
            # ============================================================
            # إرسال الرد
            # ============================================================
            if response:
                line_bot_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[response]
                    )
                )
                
                logger.info(f"✅ تم الرد على {username}")
    
    except Exception as e:
        logger.error(f"❌ خطأ في معالجة الرسالة: {e}")
        logger.error(traceback.format_exc())

# ============================================================================
# Startup & Run
# ============================================================================

@app.before_request
def before_request():
    """تنظيف دوري قبل كل طلب"""
    import random
    if random.randint(1, 100) == 1:
        cleanup_expired_games()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    
    logger.info("=" * 70)
    logger.info("🚀 Bot Mesh v7.0 - Production Ready")
    logger.info(f"🌐 Port: {port}")
    logger.info(f"🎮 Games: {len(game_loader.games)}")
    logger.info(f"🎨 Themes: {len(ui.THEMES)}")
    logger.info("=" * 70)
    
    app.run(
        host="0.0.0.0",
        port=port,
        debug=False,
        threaded=True
    )
