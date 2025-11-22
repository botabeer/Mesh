"""
Bot Mesh - Professional Gaming Bot (Enhanced Async Version)
Created by: Abeer Aldosari © 2025
"""
import os
import sys
import asyncio
import logging
import signal
import importlib
from datetime import datetime
from typing import Dict, Optional, Any
from contextlib import asynccontextmanager

from flask import Flask, request, abort, jsonify
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, FlexSendMessage
)

from config import Config, THEMES, Theme
from database import Database, db
from cache import CacheManager, cache_manager
from flex_builder import FlexBuilder, flex_builder

# Logging Setup
logging.basicConfig(
    level=logging.DEBUG if Config.DEBUG else logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================
# 🎮 Dynamic Games Loading
# ============================================
GAMES_FOLDER = "games"

def snake_to_camel(name: str) -> str:
    """تحويل snake_case إلى CamelCase"""
    return "".join(word.capitalize() for word in name.split("_"))

def load_games() -> Dict[str, Any]:
    """تحميل الألعاب ديناميكياً"""
    games = {}
    
    if not os.path.exists(GAMES_FOLDER):
        logger.warning(f"⚠️ {GAMES_FOLDER} folder not found")
        return games
    
    logger.info(f"📂 Loading games from {GAMES_FOLDER}")
    
    for filename in os.listdir(GAMES_FOLDER):
        if filename.endswith("_game.py") and not filename.startswith("__"):
            module_name = filename[:-3]
            class_name = snake_to_camel(module_name)
            
            try:
                module = importlib.import_module(f"{GAMES_FOLDER}.{module_name}")
                game_class = getattr(module, class_name, None)
                
                if game_class:
                    games[class_name] = game_class
                    logger.info(f"✅ Loaded: {class_name}")
            except Exception as e:
                logger.warning(f"⚠️ Failed to load {class_name}: {e}")
    
    logger.info(f"📊 Total games loaded: {len(games)}")
    return games

GAMES_LOADED = load_games()

# خريطة الألعاب
GAME_MAP = {
    'ذكاء': {'class': 'IqGame', 'emoji': '🧠', 'name': 'اختبار الذكاء', 'color': '#667EEA'},
    'لون': {'class': 'WordColorGame', 'emoji': '🎨', 'name': 'لعبة الألوان', 'color': '#9F7AEA'},
    'سلسلة': {'class': 'ChainWordsGame', 'emoji': '⛓️', 'name': 'سلسلة الكلمات', 'color': '#4FD1C5'},
    'ترتيب': {'class': 'ScrambleWordGame', 'emoji': '🔤', 'name': 'ترتيب الحروف', 'color': '#68D391'},
    'تكوين': {'class': 'LettersWordsGame', 'emoji': '✏️', 'name': 'تكوين الكلمات', 'color': '#FC8181'},
    'أسرع': {'class': 'FastTypingGame', 'emoji': '⚡', 'name': 'الكتابة السريعة', 'color': '#F687B3'},
    'لعبة': {'class': 'HumanAnimalPlantGame', 'emoji': '🎯', 'name': 'إنسان حيوان نبات', 'color': '#63B3ED'},
    'خمن': {'class': 'GuessGame', 'emoji': '🤔', 'name': 'خمن الكلمة', 'color': '#B794F4'},
    'توافق': {'class': 'CompatibilityGame', 'emoji': '💖', 'name': 'نسبة التوافق', 'color': '#FEB2B2'},
    'رياضيات': {'class': 'MathGame', 'emoji': '🔢', 'name': 'الرياضيات', 'color': '#667EEA'},
    'ذاكرة': {'class': 'MemoryGame', 'emoji': '🧩', 'name': 'اختبار الذاكرة', 'color': '#90CDF4'},
    'لغز': {'class': 'RiddleGame', 'emoji': '🎭', 'name': 'حل الألغاز', 'color': '#FBD38D'},
    'ضد': {'class': 'OppositeGame', 'emoji': '↔️', 'name': 'الأضداد', 'color': '#9AE6B4'},
    'إيموجي': {'class': 'EmojiGame', 'emoji': '😀', 'name': 'خمن الإيموجي', 'color': '#FEEBC8'},
    'أغنية': {'class': 'SongGame', 'emoji': '🎵', 'name': 'خمن الأغنية', 'color': '#E9D8FD'}
}

AVAILABLE_GAMES = {k: v for k, v in GAME_MAP.items() if v['class'] in GAMES_LOADED}

# ============================================
# ⚙️ Flask & LINE Setup
# ============================================
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

line_bot_api = LineBotApi(Config.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(Config.LINE_CHANNEL_SECRET)

# Gemini AI Setup
current_gemini_key_index = 0
USE_AI = bool(Config.GEMINI_API_KEYS)

def get_gemini_api_key() -> Optional[str]:
    """الحصول على مفتاح Gemini الحالي"""
    if Config.GEMINI_API_KEYS:
        return Config.GEMINI_API_KEYS[current_gemini_key_index]
    return None

def switch_gemini_key() -> bool:
    """التبديل لمفتاح Gemini التالي"""
    global current_gemini_key_index
    if len(Config.GEMINI_API_KEYS) > 1:
        current_gemini_key_index = (current_gemini_key_index + 1) % len(Config.GEMINI_API_KEYS)
        return True
    return False

# ============================================
# 📊 Metrics
# ============================================
class Metrics:
    """مقاييس الأداء"""
    
    def __init__(self):
        self.requests = 0
        self.games_started = 0
        self.errors = 0
        self.start_time = datetime.now()
        self._lock = asyncio.Lock()
    
    async def increment(self, metric: str):
        """زيادة مقياس"""
        async with self._lock:
            setattr(self, metric, getattr(self, metric, 0) + 1)
    
    def get_stats(self) -> Dict[str, Any]:
        """الحصول على الإحصائيات"""
        uptime = (datetime.now() - self.start_time).total_seconds()
        return {
            'requests': self.requests,
            'games_started': self.games_started,
            'errors': self.errors,
            'uptime_seconds': uptime,
            'uptime_formatted': f"{int(uptime // 3600)}h {int((uptime % 3600) // 60)}m"
        }

metrics = Metrics()

# ============================================
# 🎮 Game Manager
# ============================================
class GameManager:
    """مدير الألعاب المحسن"""
    
    def __init__(self):
        self.active_games: Dict[str, Dict] = {}
        self.registered_users: set = set()
        self.user_themes: Dict[str, str] = {}
        self._lock = asyncio.Lock()
    
    async def is_registered(self, user_id: str) -> bool:
        """التحقق من تسجيل المستخدم"""
        async with self._lock:
            return user_id in self.registered_users
    
    async def register(self, user_id: str):
        """تسجيل مستخدم"""
        async with self._lock:
            self.registered_users.add(user_id)
    
    async def unregister(self, user_id: str):
        """إلغاء تسجيل مستخدم"""
        async with self._lock:
            self.registered_users.discard(user_id)
    
    async def create_game(self, game_id: str, game: Any, game_type: str):
        """إنشاء لعبة جديدة"""
        async with self._lock:
            self.active_games[game_id] = {
                'game': game,
                'type': game_type,
                'created': datetime.now()
            }
    
    async def get_game(self, game_id: str) -> Optional[Dict]:
        """الحصول على لعبة"""
        async with self._lock:
            return self.active_games.get(game_id)
    
    async def end_game(self, game_id: str) -> Optional[Dict]:
        """إنهاء لعبة"""
        async with self._lock:
            return self.active_games.pop(game_id, None)
    
    async def is_active(self, game_id: str) -> bool:
        """التحقق من نشاط اللعبة"""
        async with self._lock:
            return game_id in self.active_games
    
    async def set_user_theme(self, user_id: str, theme: str):
        """تعيين ثيم المستخدم"""
        async with self._lock:
            self.user_themes[user_id] = theme
    
    async def get_user_theme(self, user_id: str) -> str:
        """الحصول على ثيم المستخدم"""
        async with self._lock:
            return self.user_themes.get(user_id, 'light')
    
    async def cleanup_expired_games(self, timeout_minutes: int = 30):
        """تنظيف الألعاب المنتهية"""
        async with self._lock:
            expired = []
            for game_id, data in self.active_games.items():
                game = data['game']
                if hasattr(game, 'is_expired') and game.is_expired(timeout_minutes):
                    expired.append(game_id)
            
            for game_id in expired:
                del self.active_games[game_id]
                logger.info(f"🗑️ Cleaned up expired game: {game_id}")

game_manager = GameManager()

# ============================================
# 🔧 Helper Functions
# ============================================
def get_profile(user_id: str) -> str:
    """الحصول على اسم المستخدم"""
    try:
        return line_bot_api.get_profile(user_id).display_name
    except:
        return "لاعب"

async def get_user_flex_builder(user_id: str) -> FlexBuilder:
    """الحصول على FlexBuilder مع ثيم المستخدم"""
    theme = await game_manager.get_user_theme(user_id)
    builder = FlexBuilder()
    builder.set_theme(theme)
    return builder

# ============================================
# 🎯 Command Handler
# ============================================
class CommandHandler:
    """معالج الأوامر"""
    
    def __init__(self, gm: GameManager, api: LineBotApi):
        self.gm = gm
        self.api = api
        self.commands = {
            'مساعدة': self.help, 'help': self.help,
            'انضم': self.join, 'تسجيل': self.join,
            'انسحب': self.leave, 'خروج': self.leave,
            'ابدأ': self.start, 'start': self.start,
            'نقاطي': self.stats, 'احصائياتي': self.stats,
            'الصدارة': self.leaderboard,
            'إيقاف': self.stop, 'ايقاف': self.stop,
            'ثيم': self.theme_selector
        }
    
    async def handle(self, event, user_id: str, text: str, 
                     game_id: str, display_name: str) -> bool:
        """معالجة الأمر"""
        # معالجة اختيار الثيم
        if text.startswith('ثيم:'):
            theme_name = text.split(':')[1]
            await self.set_theme(event, user_id, theme_name)
            return True
        
        handler_func = self.commands.get(text)
        if handler_func:
            await handler_func(event, user_id, game_id, display_name)
            return True
        return False
    
    async def help(self, event, user_id: str, *args):
        """عرض المساعدة"""
        builder = await get_user_flex_builder(user_id)
        self.api.reply_message(
            event.reply_token,
            FlexSendMessage(alt_text="المساعدة", contents=builder.create_help())
        )
    
    async def join(self, event, user_id: str, game_id: str, display_name: str):
        """الانضمام"""
        if await self.gm.is_registered(user_id):
            self.api.reply_message(
                event.reply_token,
                TextSendMessage(text=f"✅ أنت مسجل بالفعل يا {display_name}\n\nاكتب 'ابدأ' للعب")
            )
        else:
            await self.gm.register(user_id)
            builder = await get_user_flex_builder(user_id)
            self.api.reply_message(
                event.reply_token,
                FlexSendMessage(alt_text="مرحباً", contents=builder.create_main_menu())
            )
    
    async def leave(self, event, user_id: str, *args):
        """الانسحاب"""
        if await self.gm.is_registered(user_id):
            await self.gm.unregister(user_id)
            self.api.reply_message(
                event.reply_token,
                TextSendMessage(text="👋 تم الانسحاب بنجاح")
            )
        else:
            self.api.reply_message(
                event.reply_token,
                TextSendMessage(text="❌ أنت غير مسجل")
            )
    
    async def start(self, event, user_id: str, *args):
        """بدء اللعب"""
        if not AVAILABLE_GAMES:
            self.api.reply_message(
                event.reply_token,
                TextSendMessage(text="⚠️ لا توجد ألعاب متاحة حالياً")
            )
        else:
            builder = await get_user_flex_builder(user_id)
            self.api.reply_message(
                event.reply_token,
                FlexSendMessage(
                    alt_text="اختر لعبة",
                    contents=builder.create_games_carousel(AVAILABLE_GAMES)
                )
            )
    
    async def stats(self, event, user_id: str, *args):
        """عرض الإحصائيات"""
        await db.initialize()
        user = await db.get_user(user_id)
        rank = await db.get_user_rank(user_id) if user else 0
        
        builder = await get_user_flex_builder(user_id)
        self.api.reply_message(
            event.reply_token,
            FlexSendMessage(
                alt_text="إحصائياتك",
                contents=builder.create_stats_card(user, rank)
            )
        )
    
    async def leaderboard(self, event, user_id: str, *args):
        """عرض لوحة الصدارة"""
        await db.initialize()
        leaders = await db.get_leaderboard()
        
        builder = await get_user_flex_builder(user_id)
        self.api.reply_message(
            event.reply_token,
            FlexSendMessage(
                alt_text="الصدارة",
                contents=builder.create_leaderboard(leaders)
            )
        )
    
    async def stop(self, event, user_id: str, game_id: str, *args):
        """إيقاف اللعبة"""
        if await self.gm.is_active(game_id):
            data = await self.gm.end_game(game_id)
            self.api.reply_message(
                event.reply_token,
                TextSendMessage(text=f"⏸️ تم إيقاف لعبة {data['type']}")
            )
        else:
            self.api.reply_message(
                event.reply_token,
                TextSendMessage(text="❌ لا توجد لعبة نشطة")
            )
    
    async def theme_selector(self, event, user_id: str, *args):
        """عرض قائمة الثيمات"""
        builder = await get_user_flex_builder(user_id)
        self.api.reply_message(
            event.reply_token,
            FlexSendMessage(
                alt_text="اختر الثيم",
                contents=builder.create_theme_selector()
            )
        )
    
    async def set_theme(self, event, user_id: str, theme_name: str):
        """تعيين الثيم"""
        await self.gm.set_user_theme(user_id, theme_name)
        
        # تحديث في قاعدة البيانات
        await db.initialize()
        await db.set_user_theme(user_id, theme_name)
        
        theme_names = {
            'light': '🌞 فاتح',
            'dark': '🌙 داكن',
            'purple': '💜 بنفسجي',
            'ocean': '🌊 محيط',
            'sunset': '🌅 غروب'
        }
        
        self.api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"✅ تم تغيير الثيم إلى {theme_names.get(theme_name, theme_name)}")
        )

cmd_handler = CommandHandler(game_manager, line_bot_api)

# ============================================
# 🎮 Game Functions
# ============================================
async def start_game(game_id: str, game_class, game_type: str, 
                     user_id: str, event) -> bool:
    """بدء لعبة جديدة"""
    try:
        # ألعاب تحتاج AI
        ai_games = ['IqGame', 'WordColorGame', 'LettersWordsGame', 'HumanAnimalPlantGame']
        
        if game_class.__name__ in ai_games:
            game = game_class(
                line_bot_api,
                use_ai=USE_AI,
                get_api_key=get_gemini_api_key,
                switch_key=switch_gemini_key
            )
        else:
            game = game_class(line_bot_api)
        
        await game_manager.create_game(game_id, game, game_type)
        response = game.start_game()
        
        line_bot_api.reply_message(event.reply_token, response)
        await metrics.increment('games_started')
        
        logger.info(f"✅ Game started: {game_type}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Game start error: {e}")
        await metrics.increment('errors')
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="❌ خطأ في بدء اللعبة")
        )
        return False

async def handle_answer(event, user_id: str, text: str, 
                        game_id: str, display_name: str):
    """معالجة إجابة اللاعب"""
    data = await game_manager.get_game(game_id)
    if not data:
        return
    
    game = data['game']
    game_type = data['type']
    
    try:
        result = game.check_answer(text, user_id, display_name)
        
        if result:
            points = result.get('points', 0)
            
            if points > 0:
                await db.initialize()
                await db.update_user_score(
                    user_id, display_name, points,
                    result.get('won', False), game_type
                )
            
            if result.get('game_over', False):
                await game_manager.end_game(game_id)
            
            response = result.get('response', TextSendMessage(text=result.get('message', '')))
            line_bot_api.reply_message(event.reply_token, response)
            
    except Exception as e:
        logger.error(f"❌ Answer handling error: {e}")
        await metrics.increment('errors')

# ============================================
# 🌐 Flask Routes
# ============================================
@app.route("/", methods=['GET'])
def home():
    """الصفحة الرئيسية"""
    stats = metrics.get_stats()
    
    return f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Bot Mesh</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }}
        .container {{
            background: rgba(255,255,255,0.95);
            border-radius: 20px;
            padding: 40px;
            max-width: 600px;
            width: 100%;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }}
        h1 {{ color: #667eea; font-size: 2.5em; margin-bottom: 10px; text-align: center; }}
        .status {{ 
            background: #d4edda; 
            color: #155724; 
            padding: 10px 20px; 
            border-radius: 10px; 
            text-align: center; 
            margin: 20px 0;
        }}
        .stats {{ 
            display: grid; 
            grid-template-columns: repeat(2, 1fr); 
            gap: 15px; 
            margin: 20px 0; 
        }}
        .stat {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 15px;
            text-align: center;
        }}
        .stat-value {{ font-size: 2em; font-weight: bold; color: #667eea; }}
        .stat-label {{ color: #666; font-size: 0.9em; margin-top: 5px; }}
        .footer {{ text-align: center; color: #666; margin-top: 30px; font-size: 0.9em; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🎮 Bot Mesh</h1>
        <div class="status">✅ البوت يعمل بنجاح</div>
        <div class="stats">
            <div class="stat">
                <div class="stat-value">{len(GAMES_LOADED)}</div>
                <div class="stat-label">ألعاب</div>
            </div>
            <div class="stat">
                <div class="stat-value">{len(game_manager.registered_users)}</div>
                <div class="stat-label">لاعبين</div>
            </div>
            <div class="stat">
                <div class="stat-value">{len(game_manager.active_games)}</div>
                <div class="stat-label">ألعاب نشطة</div>
            </div>
            <div class="stat">
                <div class="stat-value">{stats['requests']}</div>
                <div class="stat-label">طلبات</div>
            </div>
        </div>
        <p class="footer">Created by Abeer Aldosari © 2025<br>Version {Config.BOT_VERSION}</p>
    </div>
</body>
</html>'''

@app.route("/health", methods=['GET'])
def health():
    """فحص الصحة"""
    return jsonify({
        'status': 'healthy',
        'version': Config.BOT_VERSION,
        'games': len(GAMES_LOADED),
        'metrics': metrics.get_stats()
    }), 200

@app.route("/callback", methods=['POST'])
def callback():
    """معالجة Webhook من LINE"""
    signature = request.headers.get('X-Line-Signature')
    if not signature:
        abort(400)
    
    body = request.get_data(as_text=True)
    
    # زيادة عداد الطلبات
    asyncio.run(metrics.increment('requests'))
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        logger.error("Invalid signature")
        abort(400)
    except Exception as e:
        logger.error(f"Callback error: {e}")
        asyncio.run(metrics.increment('errors'))
        abort(500)
    
    return 'OK'

# ============================================
# 📨 Message Handler
# ============================================
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    """معالجة الرسائل"""
    asyncio.run(_handle_message_async(event))

async def _handle_message_async(event):
    """معالجة الرسائل بشكل غير متزامن"""
    try:
        user_id = event.source.user_id
        text = event.message.text.strip()
        game_id = getattr(event.source, 'group_id', user_id)
        display_name = get_profile(user_id)
        
        logger.info(f"📨 {display_name}: {text}")
        
        # معالجة الأوامر
        if await cmd_handler.handle(event, user_id, text, game_id, display_name):
            return
        
        # بدء لعبة جديدة
        if text in AVAILABLE_GAMES:
            if not await game_manager.is_registered(user_id):
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text="❌ يجب التسجيل أولاً\n\nاكتب 'انضم'")
                )
                return
            
            game_data = AVAILABLE_GAMES[text]
            game_class = GAMES_LOADED.get(game_data['class'])
            
            if not game_class:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text="❌ اللعبة غير متاحة")
                )
                return
            
            # لعبة التوافق لها معاملة خاصة
            if text == 'توافق':
                game = game_class(line_bot_api)
                await game_manager.create_game(game_id, game, text)
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text="💖 لعبة التوافق!\n\nاكتب اسمين مفصولين بمسافة\nمثال: أحمد فاطمة")
                )
                return
            
            await start_game(game_id, game_class, text, user_id, event)
            return
        
        # إجابات الألعاب
        if await game_manager.is_active(game_id):
            if not await game_manager.is_registered(user_id):
                return
            await handle_answer(event, user_id, text, game_id, display_name)
            return
        
        logger.debug(f"🔇 Ignored: {text}")
        
    except Exception as e:
        logger.error(f"❌ Message handling error: {e}", exc_info=True)
        await metrics.increment('errors')

# ============================================
# 🛑 Graceful Shutdown
# ============================================
async def shutdown():
    """إيقاف البوت بشكل آمن"""
    logger.info("🛑 Shutting down...")
    await db.close()
    await cache_manager.disconnect()

def signal_handler(signum, frame):
    """معالج الإشارات"""
    asyncio.run(shutdown())
    sys.exit(0)

signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

# ============================================
# 🚀 Entry Point
# ============================================
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    
    logger.info("=" * 60)
    logger.info("🎮 BOT MESH - Enhanced Version")
    logger.info("=" * 60)
    logger.info(f"🌐 Port: {port}")
    logger.info(f"🎯 Games: {len(GAMES_LOADED)}")
    logger.info(f"✨ Available: {len(AVAILABLE_GAMES)}")
    logger.info(f"🤖 AI: {'✅' if USE_AI else '❌'}")
    logger.info(f"📦 Redis: {'✅' if Config.REDIS_ENABLED else '❌'}")
    logger.info("=" * 60)
    logger.info("Created by: Abeer Aldosari © 2025")
    logger.info("=" * 60)
    
    app.run(host='0.0.0.0', port=port, debug=Config.DEBUG, threaded=True)
