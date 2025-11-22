"""
Bot Mesh - Professional Gaming Bot (Enhanced Version)
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

from flask import Flask, request, abort, jsonify
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage

from config import Config, THEMES, Theme
from database import Database
from flex_builder import FlexBuilder, THEMES as FLEX_THEMES

# Logging
logging.basicConfig(
    level=logging.DEBUG if Config.DEBUG else logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================
# 🎮 تحميل الألعاب
# ============================================
GAMES_FOLDER = "games"

def snake_to_camel(name: str) -> str:
    return "".join(word.capitalize() for word in name.split("_"))

def load_games() -> Dict[str, Any]:
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
                logger.warning(f"⚠️ Failed: {class_name}: {e}")
    
    logger.info(f"📊 {len(games)} games loaded")
    return games

GAMES_LOADED = load_games()
AVAILABLE_GAMES = {k: v for k, v in Config.GAME_MAP.items() if v['class'] in GAMES_LOADED}

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
    def __init__(self):
        self.requests = 0
        self.games = 0
        self.start = datetime.now()
    
    def get(self):
        uptime = (datetime.now() - self.start).total_seconds()
        return {'requests': self.requests, 'games': self.games, 'uptime': f"{int(uptime//3600)}h"}

metrics = Metrics()

# ============================================
# 🎮 Game Manager
# ============================================
class GameManager:
    def __init__(self):
        self.active: Dict[str, Dict] = {}
        self.users: set = set()
        self.themes: Dict[str, str] = {}  # user_id -> theme_name
    
    def is_registered(self, uid: str) -> bool:
        return uid in self.users
    
    def register(self, uid: str):
        self.users.add(uid)
    
    def unregister(self, uid: str):
        self.users.discard(uid)
    
    def create_game(self, gid: str, game, gtype: str):
        self.active[gid] = {'game': game, 'type': gtype, 'created': datetime.now()}
    
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
    try:
        return line_bot_api.get_profile(uid).display_name
    except:
        return "لاعب"

def get_builder(uid: str) -> FlexBuilder:
    theme = gm.get_theme(uid)
    builder = FlexBuilder()
    builder.set_theme(theme)
    return builder

# ============================================
# 🎯 Commands
# ============================================
class Commands:
    def __init__(self):
        self.cmds = {
            'مساعدة': self.help, 'help': self.help,
            'انضم': self.join, 'تسجيل': self.join,
            'انسحب': self.leave, 'خروج': self.leave,
            'ابدأ': self.start, 'start': self.start,
            'نقاطي': self.stats, 'احصائياتي': self.stats,
            'الصدارة': self.leaderboard,
            'إيقاف': self.stop, 'ايقاف': self.stop,
            'ثيم': self.theme_menu
        }
    
    def handle(self, event, uid: str, text: str, gid: str, name: str) -> bool:
        # تغيير الثيم
        if text.startswith('ثيم:'):
            theme = text.split(':')[1]
            self.set_theme(event, uid, theme)
            return True
        
        cmd = self.cmds.get(text)
        if cmd:
            cmd(event, uid, gid, name)
            return True
        return False
    
    def help(self, event, uid, *args):
        """نافذة المساعدة الشاملة"""
        builder = get_builder(uid)
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(alt_text="المساعدة", contents=builder.create_help_menu())
        )
    
    def join(self, event, uid, gid, name):
        if gm.is_registered(uid):
            line_bot_api.reply_message(event.reply_token,
                TextSendMessage(text=f"✅ أنت مسجل يا {name}\n\nاكتب 'ابدأ' للعب"))
        else:
            gm.register(uid)
            builder = get_builder(uid)
            line_bot_api.reply_message(event.reply_token,
                FlexSendMessage(alt_text="مرحباً", contents=builder.create_help_menu()))
    
    def leave(self, event, uid, *args):
        if gm.is_registered(uid):
            gm.unregister(uid)
            line_bot_api.reply_message(event.reply_token,
                TextSendMessage(text="👋 تم الانسحاب بنجاح\n\nاكتب 'انضم' للعودة"))
        else:
            line_bot_api.reply_message(event.reply_token,
                TextSendMessage(text="❌ أنت غير مسجل"))
    
    def start(self, event, uid, *args):
        if not AVAILABLE_GAMES:
            line_bot_api.reply_message(event.reply_token,
                TextSendMessage(text="⚠️ لا توجد ألعاب متاحة"))
        else:
            builder = get_builder(uid)
            line_bot_api.reply_message(event.reply_token,
                FlexSendMessage(alt_text="الألعاب", 
                               contents=builder.create_games_carousel(AVAILABLE_GAMES)))
    
    def stats(self, event, uid, *args):
        asyncio.run(db.initialize())
        user = asyncio.run(db.get_user(uid))
        rank = asyncio.run(db.get_user_rank(uid)) if user else 0
        
        user_data = None
        if user:
            user_data = {
                'total_points': user.total_points,
                'games_played': user.games_played,
                'wins': user.wins
            }
        
        builder = get_builder(uid)
        line_bot_api.reply_message(event.reply_token,
            FlexSendMessage(alt_text="نقاطي", 
                           contents=builder.create_stats_card(user_data, rank)))
    
    def leaderboard(self, event, uid, *args):
        asyncio.run(db.initialize())
        leaders = asyncio.run(db.get_leaderboard())
        
        leaders_data = []
        for u in leaders:
            leaders_data.append({
                'display_name': u.display_name,
                'total_points': u.total_points
            })
        
        builder = get_builder(uid)
        line_bot_api.reply_message(event.reply_token,
            FlexSendMessage(alt_text="الصدارة", 
                           contents=builder.create_leaderboard(leaders_data)))
    
    def stop(self, event, uid, gid, *args):
        if gm.is_active(gid):
            data = gm.end_game(gid)
            line_bot_api.reply_message(event.reply_token,
                TextSendMessage(text=f"⏹️ تم إيقاف لعبة {data['type']}"))
        else:
            line_bot_api.reply_message(event.reply_token,
                TextSendMessage(text="❌ لا توجد لعبة نشطة"))
    
    def theme_menu(self, event, uid, *args):
        """قائمة الثيمات"""
        builder = get_builder(uid)
        line_bot_api.reply_message(event.reply_token,
            FlexSendMessage(alt_text="الثيمات", 
                           contents=builder.create_theme_selector()))
    
    def set_theme(self, event, uid, theme_name):
        """تعيين الثيم"""
        gm.set_theme(uid, theme_name)
        
        theme_names = {
            'white': '⚪ أبيض', 'black': '⚫ أسود',
            'gray': '🔘 رمادي', 'purple': '💜 بنفسجي', 'blue': '💙 أزرق'
        }
        
        line_bot_api.reply_message(event.reply_token,
            TextSendMessage(text=f"✅ تم تغيير الثيم إلى {theme_names.get(theme_name, theme_name)}"))

cmds = Commands()

# ============================================
# 🎮 Game Functions
# ============================================
def start_game(gid, game_class, gtype, uid, event):
    try:
        ai_games = ['IqGame', 'WordColorGame', 'LettersWordsGame', 'HumanAnimalPlantGame']
        
        if game_class.__name__ in ai_games:
            game = game_class(line_bot_api, use_ai=USE_AI, 
                            get_api_key=get_gemini_key, switch_key=switch_key)
        else:
            game = game_class(line_bot_api)
        
        gm.create_game(gid, game, gtype)
        response = game.start_game()
        line_bot_api.reply_message(event.reply_token, response)
        metrics.games += 1
        return True
    except Exception as e:
        logger.error(f"❌ Game error: {e}")
        line_bot_api.reply_message(event.reply_token,
            TextSendMessage(text="❌ خطأ في بدء اللعبة"))
        return False

def handle_answer(event, uid, text, gid, name):
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
                asyncio.run(db.update_user_score(uid, name, points, 
                                                result.get('won', False), gtype))
            
            if result.get('game_over'):
                gm.end_game(gid)
            
            response = result.get('response', TextSendMessage(text=result.get('message', '')))
            line_bot_api.reply_message(event.reply_token, response)
    except Exception as e:
        logger.error(f"❌ Answer error: {e}")

# ============================================
# 🌐 Routes
# ============================================
@app.route("/")
def home():
    s = metrics.get()
    return f'''<!DOCTYPE html>
<html dir="rtl"><head><meta charset="UTF-8"><title>Bot Mesh</title>
<style>
body{{font-family:sans-serif;background:linear-gradient(135deg,#667eea,#764ba2);
min-height:100vh;display:flex;align-items:center;justify-content:center;margin:0}}
.card{{background:#fff;border-radius:20px;padding:40px;max-width:500px;text-align:center;
box-shadow:0 20px 60px rgba(0,0,0,0.3)}}
h1{{color:#667eea;margin-bottom:10px}}
.status{{background:#d4edda;color:#155724;padding:10px;border-radius:10px;margin:20px 0}}
.stats{{display:grid;grid-template-columns:repeat(3,1fr);gap:15px;margin:20px 0}}
.stat{{background:#f8f9fa;padding:15px;border-radius:10px}}
.stat-val{{font-size:2em;font-weight:bold;color:#667eea}}
</style></head><body>
<div class="card">
<h1>🎮 Bot Mesh</h1>
<div class="status">✅ يعمل بنجاح</div>
<div class="stats">
<div class="stat"><div class="stat-val">{len(GAMES_LOADED)}</div>ألعاب</div>
<div class="stat"><div class="stat-val">{len(gm.users)}</div>لاعبين</div>
<div class="stat"><div class="stat-val">{s["requests"]}</div>طلبات</div>
</div>
<p style="color:#666">Created by Abeer Aldosari © 2025</p>
</div></body></html>'''

@app.route("/health")
def health():
    return jsonify({'status': 'healthy', 'version': Config.BOT_VERSION}), 200

@app.route("/callback", methods=['POST'])
def callback():
    sig = request.headers.get('X-Line-Signature')
    if not sig:
        abort(400)
    
    body = request.get_data(as_text=True)
    metrics.requests += 1
    
    try:
        handler.handle(body, sig)
    except InvalidSignatureError:
        abort(400)
    except Exception as e:
        logger.error(f"❌ Callback: {e}")
        abort(500)
    
    return 'OK'

# ============================================
# 📨 Message Handler
# ============================================
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    try:
        uid = event.source.user_id
        text = event.message.text.strip()
        gid = getattr(event.source, 'group_id', uid)
        name = get_name(uid)
        
        logger.info(f"📨 {name}: {text}")
        
        # الأوامر
        if cmds.handle(event, uid, text, gid, name):
            return
        
        # بدء لعبة
        if text in AVAILABLE_GAMES:
            if not gm.is_registered(uid):
                line_bot_api.reply_message(event.reply_token,
                    TextSendMessage(text="❌ اكتب 'انضم' أولاً"))
                return
            
            game_data = AVAILABLE_GAMES[text]
            game_class = GAMES_LOADED.get(game_data['class'])
            
            if not game_class:
                line_bot_api.reply_message(event.reply_token,
                    TextSendMessage(text="❌ اللعبة غير متاحة"))
                return
            
            # التوافق
            if text == 'توافق':
                game = game_class(line_bot_api)
                gm.create_game(gid, game, text)
                line_bot_api.reply_message(event.reply_token,
                    TextSendMessage(text="💖 لعبة التوافق!\n\nاكتب اسمين بمسافة\nمثال: أحمد فاطمة"))
                return
            
            start_game(gid, game_class, text, uid, event)
            return
        
        # إجابة
        if gm.is_active(gid):
            if gm.is_registered(uid):
                handle_answer(event, uid, text, gid, name)
            return
        
    except Exception as e:
        logger.error(f"❌ Error: {e}", exc_info=True)

# ============================================
# 🚀 Main
# ============================================
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    
    logger.info("=" * 50)
    logger.info("🎮 BOT MESH v2.0")
    logger.info("=" * 50)
    logger.info(f"🌐 Port: {port}")
    logger.info(f"🎯 Games: {len(GAMES_LOADED)}")
    logger.info(f"🎨 Themes: 5 (أبيض/أسود/رمادي/بنفسجي/أزرق)")
    logger.info("=" * 50)
    logger.info("Created by: Abeer Aldosari © 2025")
    logger.info("=" * 50)
    
    app.run(host='0.0.0.0', port=port, debug=Config.DEBUG)
