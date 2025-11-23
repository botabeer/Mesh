"""
Bot Mesh - Professional Gaming Bot with Neumorphism Design
نظام كامل متكامل مع تصاميم احترافية
Created by: Abeer Aldosari © 2025
"""
import os
import asyncio
import logging
import importlib
from typing import Dict, Any

from flask import Flask, request, abort, jsonify
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    FlexSendMessage, FollowEvent, JoinEvent
)

from config import Config
from database import Database
from neumorphism_professional_system import (
    NeumorphismFlexBuilder, 
    NeumorphismTheme,
    create_flex_builder
)

# Logging
logging.basicConfig(
    level=logging.DEBUG if Config.DEBUG else logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ==========================================
# تحميل الألعاب
# ==========================================
def load_games() -> Dict[str, Any]:
    """تحميل جميع الألعاب تلقائياً"""
    games = {}
    if not os.path.exists("games"):
        logger.error("❌ games/ directory not found")
        return games
    
    for f in os.listdir("games"):
        if f.endswith("_game.py") and f != "base_game.py":
            name = f[:-3]
            cls = "".join(w.capitalize() for w in name.split("_"))
            try:
                mod = importlib.import_module(f"games.{name}")
                if hasattr(mod, cls):
                    games[cls] = getattr(mod, cls)
                    logger.info(f"✅ Loaded: {cls}")
            except Exception as e:
                logger.warning(f"⚠️ Failed to load {cls}: {e}")
    return games

GAMES = load_games()
GAME_MAP = {k: v for k, v in Config.GAME_MAP.items() if v['class'] in GAMES}

# ==========================================
# Flask & LINE Setup
# ==========================================
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

line_api = LineBotApi(Config.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(Config.LINE_CHANNEL_SECRET)
db = Database(Config.DB_PATH, Config.DB_NAME)

# ==========================================
# Gemini AI Setup
# ==========================================
key_idx = 0
USE_AI = bool(Config.GEMINI_API_KEYS)

def get_key():
    return Config.GEMINI_API_KEYS[key_idx] if Config.GEMINI_API_KEYS else None

def switch_key():
    global key_idx
    if len(Config.GEMINI_API_KEYS) > 1:
        key_idx = (key_idx + 1) % len(Config.GEMINI_API_KEYS)

# ==========================================
# Game Manager مع دعم الثيمات
# ==========================================
class GameManager:
    def __init__(self):
        self.active: Dict[str, Dict] = {}
        self.users: set = set()
        self.themes: Dict[str, str] = {}  # حفظ ثيم كل مستخدم
    
    def registered(self, uid):
        return uid in self.users
    
    def register(self, uid):
        self.users.add(uid)
    
    def unregister(self, uid):
        self.users.discard(uid)
    
    def has_game(self, gid):
        return gid in self.active
    
    def get_game(self, gid):
        return self.active.get(gid)
    
    def start(self, gid, game, gtype):
        self.active[gid] = {'game': game, 'type': gtype}
    
    def end(self, gid):
        return self.active.pop(gid, None)
    
    def set_theme(self, uid, theme):
        """تعيين ثيم المستخدم"""
        self.themes[uid] = theme
        logger.info(f"🎨 User {uid} theme changed to {theme}")
    
    def get_theme(self, uid):
        """الحصول على ثيم المستخدم"""
        return self.themes.get(uid, 'soft')

gm = GameManager()

# ==========================================
# Helper Functions
# ==========================================
def get_name(uid):
    """الحصول على اسم المستخدم"""
    try:
        return line_api.get_profile(uid).display_name
    except Exception as e:
        logger.error(f"❌ Error getting profile: {e}")
        return "لاعب"

def get_builder(uid) -> NeumorphismFlexBuilder:
    """الحصول على Builder حسب ثيم المستخدم"""
    theme_name = gm.get_theme(uid)
    return create_flex_builder(theme_name)

# ==========================================
# الأوامر الأساسية
# ==========================================
def cmd_start(event, uid, gid, name):
    """نافذة البداية مع التصميم الاحترافي"""
    builder = get_builder(uid)
    welcome = builder.create_welcome_screen()
    
    line_api.reply_message(
        event.reply_token,
        FlexSendMessage(alt_text="Bot Mesh", contents=welcome)
    )
    logger.info(f"📱 {name} opened start screen")

def cmd_help(event, uid, gid, name):
    """نافذة المساعدة"""
    help_text = """📖 دليل الاستخدام

🎮 الأوامر الأساسية:
• بداية - عرض القائمة الرئيسية
• انضم - التسجيل في البوت
• نقاطي - عرض إحصائياتك
• الصدارة - أفضل اللاعبين
• ثيم - تغيير الثيم

🎯 أثناء اللعب:
• لمح - الحصول على تلميح
• جاوب - عرض الإجابة
• إيقاف - إنهاء اللعبة

💡 استخدم الأزرار الثابتة أسفل الشاشة للوصول السريع!

Created by Abeer Aldosari © 2025"""
    
    line_api.reply_message(
        event.reply_token,
        TextSendMessage(text=help_text)
    )

def cmd_join(event, uid, gid, name):
    """الانضمام/التسجيل"""
    if gm.registered(uid):
        line_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"✅ أنت مسجل يا {name}!\n\nاستخدم الأزرار أسفل الشاشة لاختيار لعبة")
        )
    else:
        gm.register(uid)
        builder = get_builder(uid)
        welcome = builder.create_welcome_screen()
        
        line_api.reply_message(
            event.reply_token,
            FlexSendMessage(alt_text="مرحباً!", contents=welcome)
        )
        logger.info(f"✅ {name} registered")

def cmd_leave(event, uid, gid, name):
    """الانسحاب"""
    if gm.registered(uid):
        gm.unregister(uid)
        line_api.reply_message(
            event.reply_token,
            TextSendMessage(text="👋 تم الانسحاب\nاكتب 'انضم' للعودة")
        )
    else:
        line_api.reply_message(
            event.reply_token,
            TextSendMessage(text="❌ أنت غير مسجل")
        )

def cmd_stats(event, uid, gid, name):
    """عرض الإحصائيات"""
    asyncio.run(db.initialize())
    user = asyncio.run(db.get_user(uid))
    rank = asyncio.run(db.get_user_rank(uid)) if user else 0
    
    data = {
        'total_points': user.total_points if user else 0,
        'games_played': user.games_played if user else 0,
        'wins': user.wins if user else 0,
        'is_registered': gm.registered(uid)
    }
    
    builder = get_builder(uid)
    stats_card = builder.create_stats_card(data, rank)
    
    line_api.reply_message(
        event.reply_token,
        FlexSendMessage(alt_text="إحصائياتي", contents=stats_card)
    )
    logger.info(f"📊 {name} viewed stats")

def cmd_leaderboard(event, uid, gid, name):
    """عرض الصدارة"""
    asyncio.run(db.initialize())
    leaders = asyncio.run(db.get_leaderboard())
    data = [
        {'display_name': u.display_name, 'total_points': u.total_points}
        for u in leaders
    ]
    
    builder = get_builder(uid)
    leaderboard = builder.create_leaderboard(data)
    
    line_api.reply_message(
        event.reply_token,
        FlexSendMessage(alt_text="الصدارة", contents=leaderboard)
    )
    logger.info(f"🏆 {name} viewed leaderboard")

def cmd_stop(event, uid, gid, name):
    """إيقاف اللعبة"""
    if gm.has_game(gid):
        game_data = gm.end(gid)
        line_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"⏹️ تم إيقاف {game_data['type']}")
        )
        logger.info(f"⏹️ {name} stopped game {game_data['type']}")
    else:
        line_api.reply_message(
            event.reply_token,
            TextSendMessage(text="❌ لا توجد لعبة نشطة")
        )

def cmd_theme(event, uid, gid, name):
    """عرض اختيار الثيمات"""
    builder = get_builder(uid)
    theme_selector = builder.create_theme_selector()
    
    line_api.reply_message(
        event.reply_token,
        FlexSendMessage(alt_text="اختر الثيم", contents=theme_selector)
    )
    logger.info(f"🎨 {name} opened theme selector")

def cmd_set_theme(event, uid, theme_name):
    """تعيين ثيم جديد"""
    valid_themes = ['soft', 'dark', 'ocean', 'sunset', 'forest']
    
    if theme_name.lower() not in valid_themes:
        line_api.reply_message(
            event.reply_token,
            TextSendMessage(text="❌ ثيم غير صحيح")
        )
        return
    
    gm.set_theme(uid, theme_name.lower())
    
    theme_names = {
        'soft': '🎨 ناعم',
        'dark': '🌙 داكن',
        'ocean': '🌊 محيطي',
        'sunset': '🌅 غروب',
        'forest': '🌲 طبيعي'
    }
    
    line_api.reply_message(
        event.reply_token,
        TextSendMessage(text=f"✅ تم تغيير الثيم إلى {theme_names.get(theme_name.lower(), theme_name)}")
    )

# قاموس الأوامر
COMMANDS = {
    'بداية': cmd_start,
    'ابدأ': cmd_start,
    'start': cmd_start,
    'قائمة': cmd_start,
    'مساعدة': cmd_help,
    'help': cmd_help,
    'انضم': cmd_join,
    'تسجيل': cmd_join,
    'انسحب': cmd_leave,
    'خروج': cmd_leave,
    'نقاطي': cmd_stats,
    'احصائياتي': cmd_stats,
    'الصدارة': cmd_leaderboard,
    'إيقاف': cmd_stop,
    'ايقاف': cmd_stop,
    'وقف': cmd_stop,
    'ثيم': cmd_theme,
}

# ==========================================
# بدء اللعبة
# ==========================================
def start_game(event, uid, gid, name, game_key):
    """بدء لعبة جديدة"""
    # التحقق من التسجيل
    if not gm.registered(uid):
        line_api.reply_message(
            event.reply_token,
            TextSendMessage(text="❌ اكتب 'انضم' أولاً للتسجيل")
        )
        return
    
    # التحقق من وجود لعبة نشطة
    if gm.has_game(gid):
        line_api.reply_message(
            event.reply_token,
            TextSendMessage(text="⚠️ يوجد لعبة نشطة!\nاكتب 'إيقاف' لإنهائها")
        )
        return
    
    # الحصول على بيانات اللعبة
    gdata = GAME_MAP.get(game_key)
    if not gdata:
        return
    
    cls = GAMES.get(gdata['class'])
    if not cls:
        line_api.reply_message(
            event.reply_token,
            TextSendMessage(text="❌ اللعبة غير متاحة")
        )
        return
    
    try:
        # لعبة التوافق (خاصة)
        if game_key == 'توافق':
            game = cls(line_api)
            gm.start(gid, game, game_key)
            line_api.reply_message(
                event.reply_token,
                TextSendMessage(text="💖 لعبة التوافق!\n\nاكتب اسمين بمسافة\nمثال: أحمد سارة")
            )
            return
        
        # الألعاب التي تستخدم AI
        ai_games = ['IqGame', 'WordColorGame', 'LettersWordsGame', 'HumanAnimalPlantGame']
        if gdata['class'] in ai_games:
            game = cls(line_api, use_ai=USE_AI, get_api_key=get_key, switch_key=switch_key)
        else:
            game = cls(line_api)
        
        # الألعاب التي تدعم الثيمات
        if hasattr(game, 'set_theme'):
            game.set_theme(gm.get_theme(uid))
        
        gm.start(gid, game, game_key)
        resp = game.start_game()
        line_api.reply_message(event.reply_token, resp)
        
        logger.info(f"🎮 {name} started {game_key}")
        
    except Exception as e:
        logger.error(f"❌ Game start error: {e}", exc_info=True)
        line_api.reply_message(
            event.reply_token,
            TextSendMessage(text="❌ خطأ في بدء اللعبة")
        )

# ==========================================
# معالجة الإجابة
# ==========================================
def handle_answer(event, uid, gid, name, text):
    """معالجة إجابة اللاعب"""
    data = gm.get_game(gid)
    if not data:
        return
    
    game = data['game']
    gtype = data['type']
    
    try:
        result = game.check_answer(text, uid, name)
        if result:
            pts = result.get('points', 0)
            
            # تحديث النقاط
            if pts > 0:
                asyncio.run(db.initialize())
                asyncio.run(db.update_user_score(
                    uid, name, pts,
                    result.get('won', False),
                    gtype
                ))
            
            # إنهاء اللعبة إذا انتهت
            if result.get('game_over'):
                gm.end(gid)
            
            # الرد
            resp = result.get('response', TextSendMessage(text=result.get('message', '')))
            line_api.reply_message(event.reply_token, resp)
            
    except Exception as e:
        logger.error(f"❌ Answer handling error: {e}", exc_info=True)

# ==========================================
# Routes
# ==========================================
@app.route("/")
def home():
    """الصفحة الرئيسية"""
    return f'''<!DOCTYPE html>
<html dir="rtl">
<head>
<meta charset="UTF-8">
<title>Bot Mesh</title>
<style>
body{{font-family:sans-serif;background:linear-gradient(135deg,#667eea,#764ba2);
min-height:100vh;display:flex;align-items:center;justify-content:center;margin:0}}
.c{{background:#fff;border-radius:25px;padding:40px;max-width:500px;text-align:center;
box-shadow:0 20px 60px rgba(0,0,0,0.3)}}
h1{{color:#667eea;margin:0 0 10px 0;font-size:2.5em}}
.s{{background:#d4edda;color:#155724;padding:20px;border-radius:15px;margin:20px 0;
font-weight:bold}}
.info{{margin:10px 0;color:#666;font-size:1.1em}}
small{{color:#999}}
</style>
</head>
<body>
<div class="c">
<h1>🎮 Bot Mesh</h1>
<div class="s">✅ يعمل بنجاح<br>Neumorphism Design Active</div>
<div class="info">🎯 {len(GAMES)} لعبة محسّنة</div>
<div class="info">👥 {len(gm.users)} لاعب نشط</div>
<div class="info">🎨 5 ثيمات احترافية</div>
<small>Created by Abeer Aldosari © 2025</small>
</div>
</body>
</html>'''

@app.route("/health")
def health():
    """Health check"""
    return jsonify({
        'status': 'ok',
        'games': len(GAMES),
        'active_users': len(gm.users),
        'active_games': len(gm.active),
        'version': Config.BOT_VERSION
    })

@app.route("/callback", methods=['POST'])
def callback():
    """LINE webhook callback"""
    sig = request.headers.get('X-Line-Signature')
    if not sig:
        abort(400)
    
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, sig)
    except InvalidSignatureError:
        logger.error("❌ Invalid signature")
        abort(400)
    
    return 'OK'

# ==========================================
# Event Handlers
# ==========================================
@handler.add(MessageEvent, message=TextMessage)
def on_message(event):
    """معالجة الرسائل"""
    try:
        uid = event.source.user_id
        text = event.message.text.strip()
        gid = getattr(event.source, 'group_id', uid)
        name = get_name(uid)
        
        logger.info(f"📨 {name}: {text}")
        
        # تغيير الثيم
        if text.startswith('ثيم:'):
            theme = text.split(':')[1].strip()
            cmd_set_theme(event, uid, theme)
            return
        
        # الأوامر
        if text in COMMANDS:
            COMMANDS[text](event, uid, gid, name)
            return
        
        # بدء لعبة
        if text in GAME_MAP:
            start_game(event, uid, gid, name, text)
            return
        
        # إجابة في لعبة نشطة
        if gm.has_game(gid) and gm.registered(uid):
            handle_answer(event, uid, gid, name, text)
    
    except Exception as e:
        logger.error(f"❌ Message handler error: {e}", exc_info=True)

@handler.add(FollowEvent)
def on_follow(event):
    """عند متابعة البوت"""
    uid = event.source.user_id
    name = get_name(uid)
    gm.register(uid)
    
    builder = get_builder(uid)
    welcome = builder.create_welcome_screen()
    
    line_api.reply_message(
        event.reply_token,
        FlexSendMessage(alt_text="مرحباً!", contents=welcome)
    )
    logger.info(f"👋 {name} followed the bot")

@handler.add(JoinEvent)
def on_join(event):
    """عند انضمام البوت للمجموعة"""
    builder = NeumorphismFlexBuilder(NeumorphismTheme.SOFT)
    welcome = builder.create_welcome_screen()
    
    line_api.reply_message(
        event.reply_token,
        FlexSendMessage(alt_text="مرحباً!", contents=welcome)
    )
    logger.info("📢 Bot joined a group")

# ==========================================
# Main
# ==========================================
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    
    logger.info("=" * 50)
    logger.info(f"🎮 Bot Mesh v{Config.BOT_VERSION}")
    logger.info(f"📊 Port: {port}")
    logger.info(f"🎯 Games: {len(GAMES)}")
    logger.info(f"🤖 AI: {USE_AI}")
    logger.info(f"🎨 Neumorphism Design: Active")
    logger.info("=" * 50)
    
    app.run(host='0.0.0.0', port=port, debug=Config.DEBUG)
