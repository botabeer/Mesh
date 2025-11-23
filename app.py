"""
Bot Mesh - Professional Gaming Bot (Fixed)
Created by: Abeer Aldosari © 2025
"""
import os
import asyncio
import logging
import importlib
from datetime import datetime
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
from flex_messages import FlexMessageBuilder, Theme

# Logging
logging.basicConfig(
    level=logging.DEBUG if Config.DEBUG else logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('bot.log', encoding='utf-8'), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Load Games
def load_games() -> Dict[str, Any]:
    games = {}
    if not os.path.exists("games"):
        logger.warning("⚠️ games/ directory not found")
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

# Flask & LINE
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
line_api = LineBotApi(Config.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(Config.LINE_CHANNEL_SECRET)
db = Database(Config.DB_PATH, Config.DB_NAME)

# Gemini AI
key_idx = 0
USE_AI = bool(Config.GEMINI_API_KEYS)

def get_key():
    return Config.GEMINI_API_KEYS[key_idx] if Config.GEMINI_API_KEYS else None

def switch_key():
    global key_idx
    if len(Config.GEMINI_API_KEYS) > 1:
        key_idx = (key_idx + 1) % len(Config.GEMINI_API_KEYS)

# Game Manager
class GameManager:
    def __init__(self):
        self.active: Dict[str, Dict] = {}
        self.users: set = set()
        self.themes: Dict[str, str] = {}
    
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
    
    def set_theme(self, uid, t): 
        self.themes[uid] = t
    
    def get_theme(self, uid): 
        return self.themes.get(uid, 'white')

gm = GameManager()

def get_name(uid):
    try: 
        return line_api.get_profile(uid).display_name
    except: 
        return "لاعب"

def get_builder(uid):
    t = gm.get_theme(uid)
    theme_map = {
        'white': Theme.WHITE, 
        'black': Theme.BLACK, 
        'blue': Theme.BLUE,
        'purple': Theme.PURPLE, 
        'pink': Theme.PINK
    }
    return FlexMessageBuilder(theme_map.get(t, Theme.WHITE))

def is_mentioned(text: str) -> bool:
    """Check if bot is mentioned using keywords"""
    text_lower = text.lower()
    keywords = ['@bot', 'بوت', 'bot mesh', 'botmesh', '@botmesh']
    return any(k in text_lower for k in keywords)

# ==========================================
# Commands
# ==========================================
def cmd_start(event, uid, gid, name):
    """Start screen with games list"""
    b = get_builder(uid)
    line_api.reply_message(
        event.reply_token,
        FlexSendMessage(alt_text="Bot Mesh", contents=b.create_start_screen())
    )

def cmd_help(event, uid, gid, name):
    """Help screen"""
    b = get_builder(uid)
    line_api.reply_message(
        event.reply_token,
        FlexSendMessage(alt_text="دليل الاستخدام", contents=b.create_help_screen())
    )

def cmd_join(event, uid, gid, name):
    """Join/Register"""
    if gm.registered(uid):
        line_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"✅ أنت مسجل يا {name}!\nاكتب 'بداية' لعرض الألعاب")
        )
    else:
        gm.register(uid)
        b = get_builder(uid)
        line_api.reply_message(
            event.reply_token,
            FlexSendMessage(alt_text="مرحباً!", contents=b.create_start_screen())
        )

def cmd_leave(event, uid, gid, name):
    """Leave/Unregister"""
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
    """User statistics"""
    asyncio.run(db.initialize())
    user = asyncio.run(db.get_user(uid))
    rank = asyncio.run(db.get_user_rank(uid)) if user else 0
    
    data = {
        'total_points': user.total_points if user else 0,
        'games_played': user.games_played if user else 0,
        'wins': user.wins if user else 0,
        'is_registered': gm.registered(uid)
    }
    
    b = get_builder(uid)
    line_api.reply_message(
        event.reply_token,
        FlexSendMessage(alt_text="إحصائياتي", contents=b.create_stats_card(data, rank))
    )

def cmd_leaderboard(event, uid, gid, name):
    """Leaderboard"""
    asyncio.run(db.initialize())
    leaders = asyncio.run(db.get_leaderboard())
    data = [{'display_name': u.display_name, 'total_points': u.total_points} for u in leaders]
    
    b = get_builder(uid)
    line_api.reply_message(
        event.reply_token,
        FlexSendMessage(alt_text="الصدارة", contents=b.create_leaderboard(data))
    )

def cmd_stop(event, uid, gid, name):
    """Stop current game"""
    if gm.has_game(gid):
        d = gm.end(gid)
        line_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"⏹️ تم إيقاف {d['type']}")
        )
    else:
        line_api.reply_message(
            event.reply_token,
            TextSendMessage(text="❌ لا توجد لعبة نشطة")
        )

def cmd_theme(event, uid, gid, name):
    """Theme selector"""
    b = get_builder(uid)
    line_api.reply_message(
        event.reply_token,
        FlexSendMessage(alt_text="الثيمات", contents=b.create_theme_selector())
    )

def cmd_set_theme(event, uid, theme_name):
    """Set theme"""
    gm.set_theme(uid, theme_name)
    names = {
        'white': '⚪ أبيض', 
        'black': '⚫ أسود', 
        'blue': '💙 أزرق',
        'purple': '💜 بنفسجي', 
        'pink': '🌸 وردي'
    }
    line_api.reply_message(
        event.reply_token,
        TextSendMessage(text=f"✅ تم تغيير الثيم إلى {names.get(theme_name, theme_name)}")
    )

COMMANDS = {
    'بداية': cmd_start, 'ابدأ': cmd_start, 'start': cmd_start, 'قائمة': cmd_start,
    'مساعدة': cmd_help, 'help': cmd_help,
    'انضم': cmd_join, 'تسجيل': cmd_join,
    'انسحب': cmd_leave, 'خروج': cmd_leave,
    'نقاطي': cmd_stats, 'احصائياتي': cmd_stats,
    'الصدارة': cmd_leaderboard,
    'إيقاف': cmd_stop, 'ايقاف': cmd_stop, 'وقف': cmd_stop,
    'ثيم': cmd_theme,
}

# ==========================================
# Start Game
# ==========================================
def start_game(event, uid, gid, name, game_key):
    """Start a game"""
    if not gm.registered(uid):
        line_api.reply_message(
            event.reply_token,
            TextSendMessage(text="❌ اكتب 'انضم' أولاً للتسجيل")
        )
        return
    
    if gm.has_game(gid):
        line_api.reply_message(
            event.reply_token,
            TextSendMessage(text="⚠️ يوجد لعبة نشطة!\nاكتب 'إيقاف' لإنهائها")
        )
        return
    
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
        # Compatibility game is special
        if game_key == 'توافق':
            game = cls(line_api)
            gm.start(gid, game, game_key)
            line_api.reply_message(
                event.reply_token,
                TextSendMessage(text="💖 لعبة التوافق!\n\nاكتب اسمين بمسافة\nمثال: أحمد سارة")
            )
            return
        
        # AI-powered games
        ai_games = ['IqGame', 'WordColorGame', 'LettersWordsGame', 'HumanAnimalPlantGame']
        if gdata['class'] in ai_games:
            game = cls(line_api, use_ai=USE_AI, get_api_key=get_key, switch_key=switch_key)
        else:
            game = cls(line_api)
        
        gm.start(gid, game, game_key)
        resp = game.start_game()
        line_api.reply_message(event.reply_token, resp)
        logger.info(f"🎮 Started: {game_key} by {name}")
        
    except Exception as e:
        logger.error(f"❌ Game error: {e}", exc_info=True)
        line_api.reply_message(
            event.reply_token,
            TextSendMessage(text="❌ خطأ في بدء اللعبة")
        )

# ==========================================
# Handle Answer
# ==========================================
def handle_answer(event, uid, gid, name, text):
    """Handle game answer"""
    data = gm.get_game(gid)
    if not data:
        return
    
    game = data['game']
    gtype = data['type']
    
    try:
        result = game.check_answer(text, uid, name)
        if result:
            pts = result.get('points', 0)
            if pts > 0:
                asyncio.run(db.initialize())
                asyncio.run(db.update_user_score(
                    uid, name, pts, 
                    result.get('won', False), 
                    gtype
                ))
            
            if result.get('game_over'):
                gm.end(gid)
            
            resp = result.get('response', TextSendMessage(text=result.get('message', '')))
            line_api.reply_message(event.reply_token, resp)
            
    except Exception as e:
        logger.error(f"❌ Answer error: {e}", exc_info=True)

# ==========================================
# Routes
# ==========================================
@app.route("/")
def home():
    return f'''<!DOCTYPE html>
<html dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Bot Mesh</title>
<style>
body{{font-family:sans-serif;background:linear-gradient(135deg,#667eea,#764ba2);
min-height:100vh;display:flex;align-items:center;justify-content:center;margin:0}}
.c{{background:#fff;border-radius:25px;padding:40px;max-width:400px;text-align:center;
box-shadow:0 20px 40px rgba(0,0,0,.3)}}
h1{{color:#667eea;margin:0}}
.s{{background:#d4edda;color:#155724;padding:15px;border-radius:15px;margin:20px 0}}
.info{{margin:10px 0;color:#666}}
</style>
</head>
<body>
<div class="c">
<h1>🎮 Bot Mesh</h1>
<div class="s">✅ يعمل بنجاح</div>
<div class="info">🎯 {len(GAMES)} لعبة متاحة</div>
<div class="info">👥 {len(gm.users)} لاعب نشط</div>
<small>Created by Abeer Aldosari © 2025</small>
</div>
</body>
</html>'''

@app.route("/health")
def health():
    return jsonify({
        'status': 'ok',
        'games': len(GAMES),
        'active_users': len(gm.users),
        'active_games': len(gm.active)
    })

@app.route("/callback", methods=['POST'])
def callback():
    sig = request.headers.get('X-Line-Signature')
    if not sig:
        abort(400)
    
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, sig)
    except InvalidSignatureError:
        logger.error("Invalid signature")
        abort(400)
    
    return 'OK'

# ==========================================
# Event Handlers
# ==========================================
@handler.add(MessageEvent, message=TextMessage)
def on_message(event):
    try:
        uid = event.source.user_id
        text = event.message.text.strip()
        gid = getattr(event.source, 'group_id', uid)
        name = get_name(uid)
        
        logger.info(f"📨 {name}: {text}")
        
        # Mention detection - show start screen
        if is_mentioned(text):
            cmd_start(event, uid, gid, name)
            return
        
        # Theme change
        if text.startswith('ثيم:'):
            theme = text.split(':')[1].strip()
            cmd_set_theme(event, uid, theme)
            return
        
        # Commands
        if text in COMMANDS:
            COMMANDS[text](event, uid, gid, name)
            return
        
        # Start game
        if text in GAME_MAP:
            start_game(event, uid, gid, name, text)
            return
        
        # Answer in active game
        if gm.has_game(gid) and gm.registered(uid):
            handle_answer(event, uid, gid, name, text)
    
    except Exception as e:
        logger.error(f"❌ Message handler error: {e}", exc_info=True)

@handler.add(FollowEvent)
def on_follow(event):
    uid = event.source.user_id
    gm.register(uid)
    b = get_builder(uid)
    line_api.reply_message(
        event.reply_token,
        FlexSendMessage(alt_text="مرحباً!", contents=b.create_start_screen())
    )

@handler.add(JoinEvent)
def on_join(event):
    b = FlexMessageBuilder(Theme.WHITE)
    line_api.reply_message(
        event.reply_token,
        FlexSendMessage(alt_text="مرحباً!", contents=b.create_start_screen())
    )

# ==========================================
# Main
# ==========================================
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"🎮 Bot Mesh v{Config.BOT_VERSION}")
    logger.info(f"📊 Port: {port} | Games: {len(GAMES)} | AI: {USE_AI}")
    app.run(host='0.0.0.0', port=port, debug=Config.DEBUG)
