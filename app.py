"""
Bot Mesh - Professional Gaming Bot (Final Enhanced Version)
Created by: Abeer Aldosari © 2025

نظام بوت احترافي مع:
- نوافذ Flex ذكية
- دعم المنشن التلقائي
- Rich Menu مع أزرار الألعاب
- 7 ثيمات جميلة
"""
import os
import sys
import asyncio
import logging
import importlib
from datetime import datetime
from typing import Dict, Optional, Any

from flask import Flask, request, abort, jsonify
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, 
    FlexSendMessage, FollowEvent, JoinEvent
)

from config import Config
from database import Database
from flex_messages import FlexMessageBuilder, Theme

# Logging
logging.basicConfig(
    level=logging.DEBUG if Config.DEBUG else logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ============================================
# 🎮 تحميل الألعاب
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
    
    logger.info(f"📊 {len(games)} games loaded")
    return games

GAMES_LOADED = load_games()
AVAILABLE_GAMES = {
    k: v for k, v in Config.GAME_MAP.items() 
    if v['class'] in GAMES_LOADED
}

# ============================================
# ⚙️ Flask & LINE
# ============================================
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

line_bot_api = LineBotApi(Config.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(Config.LINE_CHANNEL_SECRET)

# Database
db = Database(Config.DB_PATH, Config.DB_NAME)

# Gemini AI
current_key_idx = 0
USE_AI = bool(Config.GEMINI_API_KEYS)

def get_gemini_key():
    return Config.GEMINI_API_KEYS[current_key_idx] if Config.GEMINI_API_KEYS else None

def switch_key():
    global current_key_idx
    if len(Config.GEMINI_API_KEYS) > 1:
        current_key_idx = (current_key_idx + 1) % len(Config.GEMINI_API_KEYS)
        return True
    return False

# ============================================
# 📊 Metrics
# ============================================
class Metrics:
    """نظام الإحصائيات"""
    def __init__(self):
        self.requests = 0
        self.games = 0
        self.start = datetime.now()
    
    def get(self):
        uptime = (datetime.now() - self.start).total_seconds()
        return {
            'requests': self.requests, 
            'games': self.games, 
            'uptime': f"{int(uptime//3600)}h"
        }

metrics = Metrics()

# ============================================
# 🎮 Game Manager
# ============================================
class GameManager:
    """مدير الألعاب والمستخدمين"""
    def __init__(self):
        self.active: Dict[str, Dict] = {}
        self.users: set = set()
        self.themes: Dict[str, str] = {}
    
    def is_registered(self, uid: str) -> bool:
        return uid in self.users
    
    def register(self, uid: str):
        self.users.add(uid)
        logger.info(f"✅ User registered: {uid}")
    
    def unregister(self, uid: str):
        self.users.discard(uid)
        logger.info(f"👋 User unregistered: {uid}")
    
    def create_game(self, gid: str, game, gtype: str):
        self.active[gid] = {
            'game': game, 
            'type': gtype, 
            'created': datetime.now()
        }
    
    def get_game(self, gid: str):
        return self.active.get(gid)
    
    def end_game(self, gid: str):
        return self.active.pop(gid, None)
    
    def is_active(self, gid: str) -> bool:
        return gid in self.active
    
    def set_theme(self, uid: str, theme: str):
        self.themes[uid] = theme
    
    def get_theme(self, uid: str) -> str:
        return self.themes.get(uid, 'white')

gm = GameManager()

# ============================================
# 🔧 Helpers
# ============================================
def get_name(uid: str) -> str:
    """الحصول على اسم المستخدم"""
    try:
        return line_bot_api.get_profile(uid).display_name
    except:
        return "لاعب"

def get_builder(uid: str) -> FlexMessageBuilder:
    """الحصول على FlexBuilder بثيم المستخدم"""
    theme_name = gm.get_theme(uid)
    theme_map = {
        'white': Theme.WHITE, 'black': Theme.BLACK,
        'gray': Theme.GRAY, 'blue': Theme.BLUE,
        'purple': Theme.PURPLE, 'pink': Theme.PINK,
        'mint': Theme.MINT
    }
    theme = theme_map.get(theme_name, Theme.WHITE)
    return FlexMessageBuilder(theme)

# ============================================
# 🎯 Commands Handler
# ============================================
class Commands:
    """معالج الأوامر"""
    def __init__(self):
        self.cmds = {
            'مساعدة': self.help, 'help': self.help, 'ابدأ': self.help,
            'انضم': self.join, 'تسجيل': self.join,
            'انسحب': self.leave, 'خروج': self.leave,
            'نقاطي': self.stats, 'احصائياتي': self.stats,
            'الصدارة': self.leaderboard,
            'إيقاف': self.stop, 'ايقاف': self.stop,
            'ثيم': self.theme_menu
        }
    
    def handle(self, event, uid: str, text: str, gid: str, name: str) -> bool:
        """معالجة الأوامر"""
        # تغيير الثيم
        if text.startswith('ثيم:'):
            theme = text.split(':')[1]
            self.set_theme(event, uid, theme)
            return True
        
        # الأوامر العادية
        cmd = self.cmds.get(text)
        if cmd:
            cmd(event, uid, gid, name)
            return True
        return False
    
    def help(self, event, uid, *args):
        """نافذة المساعدة الترحيبية"""
        builder = get_builder(uid)
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(
                alt_text="مرحباً بك في Bot Mesh!",
                contents=builder.create_welcome_screen()
            )
        )
    
    def join(self, event, uid, gid, name):
        """انضمام المستخدم"""
        if gm.is_registered(uid):
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(
                    text=f"✅ أنت مسجل بالفعل يا {name}!\n\n"
                         "اختر لعبة من الأزرار الثابتة أسفل الشاشة 🎮"
                )
            )
        else:
            gm.register(uid)
            builder = get_builder(uid)
            line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage(
                    alt_text="مرحباً!",
                    contents=builder.create_welcome_screen()
                )
            )
    
    def leave(self, event, uid, *args):
        """انسحاب المستخدم"""
        if gm.is_registered(uid):
            gm.unregister(uid)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(
                    text="👋 تم الانسحاب بنجاح\n\n"
                         "اكتب 'انضم' للعودة"
                )
            )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="❌ أنت غير مسجل")
            )
    
    def stats(self, event, uid, *args):
        """الإحصائيات مع حالة التسجيل"""
        asyncio.run(db.initialize())
        user = asyncio.run(db.get_user(uid))
        rank = asyncio.run(db.get_user_rank(uid)) if user else 0
        
        is_registered = gm.is_registered(uid)
        
        if user:
            user_data = {
                'total_points': user.total_points,
                'games_played': user.games_played,
                'wins': user.wins,
                'is_registered': is_registered
            }
        else:
            user_data = {
                'total_points': 0,
                'games_played': 0,
                'wins': 0,
                'is_registered': is_registered
            }
        
        builder = get_builder(uid)
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(
                alt_text="نقاطي",
                contents=builder.create_stats_card(user_data, rank)
            )
        )
    
    def leaderboard(self, event, uid, *args):
        """لوحة الصدارة"""
        asyncio.run(db.initialize())
        leaders = asyncio.run(db.get_leaderboard())
        
        leaders_data = [
            {
                'display_name': u.display_name,
                'total_points': u.total_points
            }
            for u in leaders
        ]
        
        builder = get_builder(uid)
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(
                alt_text="الصدارة",
                contents=builder.create_leaderboard(leaders_data)
            )
        )
    
    def stop(self, event, uid, gid, *args):
        """إيقاف اللعبة"""
        if gm.is_active(gid):
            data = gm.end_game(gid)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(
                    text=f"⏹️ تم إيقاف لعبة {data['type']}"
                )
            )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="❌ لا توجد لعبة نشطة")
            )
    
    def theme_menu(self, event, uid, *args):
        """قائمة الثيمات"""
        builder = get_builder(uid)
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(
                alt_text="الثيمات",
                contents=builder.create_theme_selector()
            )
        )
    
    def set_theme(self, event, uid, theme_name):
        """تعيين الثيم"""
        gm.set_theme(uid, theme_name)
        
        theme_names = {
            'white': '⚪ أبيض', 'black': '⚫ أسود',
            'gray': '🔘 رمادي', 'purple': '💜 بنفسجي',
            'blue': '💙 أزرق', 'pink': '🌸 وردي',
            'mint': '🍃 نعناعي'
        }
        
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text=f"✅ تم تغيير الثيم إلى {theme_names.get(theme_name, theme_name)}"
            )
        )

cmds = Commands()

# ============================================
# 🎮 Game Functions
# ============================================
def start_game(gid, game_class, gtype, uid, event):
    """بدء لعبة جديدة"""
    try:
        ai_games = ['IqGame', 'WordColorGame', 'LettersWordsGame', 'HumanAnimalPlantGame']
        
        if game_class.__name__ in ai_games:
            game = game_class(
                line_bot_api, 
                use_ai=USE_AI,
                get_api_key=get_gemini_key, 
                switch_key=switch_key
            )
        else:
            game = game_class(line_bot_api)
        
        gm.create_game(gid, game, gtype)
        response = game.start_game()
        line_bot_api.reply_message(event.reply_token, response)
        metrics.games += 1
        logger.info(f"🎮 Game started: {gtype}")
        return True
    except Exception as e:
        logger.error(f"❌ Game start error: {e}", exc_info=True)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="❌ خطأ في بدء اللعبة")
        )
        return False

def handle_answer(event, uid, text, gid, name):
    """معالجة إجابة اللاعب"""
    data = gm.get_game(gid)
    if not data:
        return
    
    game, gtype = data['game'], data['type']
    
    try:
        result = game.check_answer(text, uid, name)
        if result:
            points = result.get('points', 0)
            if points > 0:
                asyncio.run(db.initialize())
                asyncio.run(db.update_user_score(
                    uid, name, points,
                    result.get('won', False), gtype
                ))
            
            if result.get('game_over'):
                gm.end_game(gid)
            
            response = result.get(
                'response',
                TextSendMessage(text=result.get('message', ''))
            )
            line_bot_api.reply_message(event.reply_token, response)
    except Exception as e:
        logger.error(f"❌ Answer error: {e}", exc_info=True)

# ============================================
# 🌐 Routes
# ============================================
@app.route("/")
def home():
    """الصفحة الرئيسية"""
    s = metrics.get()
    return f'''<!DOCTYPE html>
<html dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bot Mesh</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0;
            padding: 20px;
        }}
        .card {{
            background: white;
            border-radius: 25px;
            padding: 40px;
            max-width: 500px;
            width: 100%;
            text-align: center;
            box-shadow: 0 25px 50px rgba(0,0,0,0.3);
        }}
        h1 {{
            color: #667eea;
            margin-bottom: 10px;
            font-size: 2.5em;
        }}
        .status {{
            background: #d4edda;
            color: #155724;
            padding: 15px;
            border-radius: 15px;
            margin: 20px 0;
            font-weight: bold;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
            margin: 30px 0;
        }}
        .stat {{
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            padding: 20px;
            border-radius: 15px;
            transition: transform 0.2s;
        }}
        .stat:hover {{
            transform: translateY(-5px);
        }}
        .stat-val {{
            font-size: 2.5em;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 5px;
        }}
        .stat-label {{
            color: #6c757d;
            font-size: 0.9em;
        }}
        .footer {{
            color: #666;
            margin-top: 20px;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="card">
        <h1>🎮 Bot Mesh</h1>
        <div class="status">✅ يعمل بنجاح</div>
        <div class="stats">
            <div class="stat">
                <div class="stat-val">{len(GAMES_LOADED)}</div>
                <div class="stat-label">ألعاب</div>
            </div>
            <div class="stat">
                <div class="stat-val">{len(gm.users)}</div>
                <div class="stat-label">لاعبين</div>
            </div>
            <div class="stat">
                <div class="stat-val">{s["requests"]}</div>
                <div class="stat-label">طلبات</div>
            </div>
        </div>
        <div class="footer">
            Created by Abeer Aldosari © 2025<br>
            <small>Version {Config.BOT_VERSION}</small>
        </div>
    </div>
</body>
</html>'''

@app.route("/health")
def health():
    """فحص صحة التطبيق"""
    return jsonify({
        'status': 'healthy',
        'version': Config.BOT_VERSION,
        'games': len(GAMES_LOADED),
        'users': len(gm.users)
    }), 200

@app.route("/callback", methods=['POST'])
def callback():
    """معالج LINE Webhook"""
    sig = request.headers.get('X-Line-Signature')
    if not sig:
        abort(400)
    
    body = request.get_data(as_text=True)
    metrics.requests += 1
    
    try:
        handler.handle(body, sig)
    except InvalidSignatureError:
        logger.error("❌ Invalid signature")
        abort(400)
    except Exception as e:
        logger.error(f"❌ Callback error: {e}", exc_info=True)
        abort(500)
    
    return 'OK'

# ============================================
# 📨 Event Handlers
# ============================================
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    """معالج الرسائل النصية"""
    try:
        uid = event.source.user_id
        text = event.message.text.strip()
        gid = getattr(event.source, 'group_id', uid)
        name = get_name(uid)
        
        logger.info(f"📨 {name}: {text}")
        
        # معالجة الأوامر
        if cmds.handle(event, uid, text, gid, name):
            return
        
        # بدء لعبة
        if text in AVAILABLE_GAMES:
            if not gm.is_registered(uid):
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(
                        text="❌ اكتب 'انضم' أولاً للتسجيل"
                    )
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
            
            # لعبة التوافق (خاصة)
            if text == 'توافق':
                game = game_class(line_bot_api)
                gm.create_game(gid, game, text)
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(
                        text="💖 لعبة التوافق!\n\n"
                             "اكتب اسمين بمسافة\n"
                             "مثال: ميش عبير"
                    )
                )
                return
            
            start_game(gid, game_class, text, uid, event)
            return
        
        # معالجة الإجابة
        if gm.is_active(gid):
            if gm.is_registered(uid):
                handle_answer(event, uid, text, gid, name)
            return
        
    except Exception as e:
        logger.error(f"❌ Message handling error: {e}", exc_info=True)

@handler.add(FollowEvent)
def handle_follow(event):
    """عند إضافة البوت كصديق"""
    uid = event.source.user_id
    name = get_name(uid)
    logger.info(f"👤 New follower: {name}")
    
    builder = get_builder(uid)
    line_bot_api.reply_message(
        event.reply_token,
        FlexSendMessage(
            alt_text="مرحباً بك!",
            contents=builder.create_welcome_screen()
        )
    )

@handler.add(JoinEvent)
def handle_join(event):
    """عند إضافة البوت لمجموعة"""
    gid = event.source.group_id
    logger.info(f"👥 Joined group: {gid}")
    
    builder = FlexMessageBuilder(Theme.WHITE)
    line_bot_api.reply_message(
        event.reply_token,
        FlexSendMessage(
            alt_text="مرحباً!",
            contents=builder.create_welcome_screen()
        )
    )

# ============================================
# 🚀 Main
# ============================================
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    
    logger.info("=" * 60)
    logger.info("🎮 BOT MESH v2.0 - Enhanced Edition")
    logger.info("=" * 60)
    logger.info(f"🌐 Port: {port}")
    logger.info(f"🎯 Games: {len(GAMES_LOADED)}")
    logger.info(f"🎨 Themes: 7")
    logger.info(f"✨ Features: Rich Menu + Flex Messages + Auto Help")
    logger.info("=" * 60)
    logger.info("Created by: Abeer Aldosari © 2025")
    logger.info("=" * 60)
    
    app.run(host='0.0.0.0', port=port, debug=Config.DEBUG)
