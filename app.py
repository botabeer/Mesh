"""
Bot Mesh v2.0 - Professional Gaming Bot
Created by: Abeer Aldosari © 2025
"""
import os
import sys
import logging
import importlib
from datetime import datetime, timedelta
from typing import Dict, Optional, Set
from collections import defaultdict

from flask import Flask, request, abort, jsonify
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage

from config import Config, THEMES
from database import Database
from flex_builder import FlexBuilder

# =============================================
# 📝 Logging Setup
# =============================================
logging.basicConfig(
    level=logging.DEBUG if Config.DEBUG else logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# =============================================
# 🎮 Load Game Modules
# =============================================
GAMES_FOLDER = "games"

def snake_to_camel(name: str) -> str:
    """Convert snake_case to CamelCase"""
    return "".join(word.capitalize() for word in name.split("_"))

def load_game_classes() -> Dict[str, type]:
    """Load all game classes dynamically"""
    games = {}
    
    if not os.path.exists(GAMES_FOLDER):
        logger.error(f"❌ Games folder not found: {GAMES_FOLDER}")
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
                    logger.info(f"✅ Loaded game: {class_name}")
                else:
                    logger.warning(f"⚠️ Class not found: {class_name}")
                    
            except Exception as e:
                logger.warning(f"⚠️ Failed to load {class_name}: {e}")
    
    logger.info(f"📦 Total games loaded: {len(games)}")
    return games

GAMES_LOADED = load_game_classes()

# Filter available games
AVAILABLE_GAMES = {
    key: value for key, value in Config.GAME_MAP.items()
    if value['class'] in GAMES_LOADED
}

logger.info(f"🎯 Available games: {len(AVAILABLE_GAMES)}")

# =============================================
# 🔧 Flask & LINE Bot Setup
# =============================================
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

line_bot_api = LineBotApi(Config.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(Config.LINE_CHANNEL_SECRET)

# =============================================
# 🗄️ Database
# =============================================
db = Database(Config.DB_PATH, Config.DB_NAME)

# =============================================
# 🤖 AI Configuration
# =============================================
current_gemini_key_index = 0
USE_AI = bool(Config.GEMINI_API_KEYS)

def get_gemini_api_key() -> Optional[str]:
    """Get current Gemini API key"""
    if Config.GEMINI_API_KEYS:
        return Config.GEMINI_API_KEYS[current_gemini_key_index]
    return None

def switch_gemini_key() -> bool:
    """Switch to next Gemini API key"""
    global current_gemini_key_index
    if len(Config.GEMINI_API_KEYS) > 1:
        current_gemini_key_index = (current_gemini_key_index + 1) % len(Config.GEMINI_API_KEYS)
        logger.info(f"🔄 Switched to Gemini key #{current_gemini_key_index + 1}")
        return True
    return False

logger.info(f"🤖 AI enabled: {USE_AI} ({len(Config.GEMINI_API_KEYS)} keys)")

# =============================================
# 📊 Metrics
# =============================================
class Metrics:
    """Simple metrics tracker"""
    def __init__(self):
        self.requests = 0
        self.games_started = 0
        self.start_time = datetime.now()
    
    def get_stats(self) -> Dict:
        uptime = datetime.now() - self.start_time
        hours = int(uptime.total_seconds() // 3600)
        return {
            'requests': self.requests,
            'games': self.games_started,
            'uptime_hours': hours
        }

metrics = Metrics()

# =============================================
# 🎮 Game Manager
# =============================================
class GameManager:
    """Manage active games and registered players"""
    
    def __init__(self):
        self.active_games: Dict[str, Dict] = {}
        self.registered_players: Set[str] = set()
        self.user_themes: Dict[str, str] = {}
    
    def is_registered(self, user_id: str) -> bool:
        return user_id in self.registered_players
    
    def register_player(self, user_id: str):
        self.registered_players.add(user_id)
        logger.info(f"✅ Player registered: {user_id}")
    
    def unregister_player(self, user_id: str):
        self.registered_players.discard(user_id)
        logger.info(f"👋 Player unregistered: {user_id}")
    
    def create_game(self, game_id: str, game_instance, game_type: str):
        self.active_games[game_id] = {
            'game': game_instance,
            'type': game_type,
            'created_at': datetime.now()
        }
        logger.info(f"🎮 Game created: {game_type} in {game_id}")
    
    def get_game(self, game_id: str) -> Optional[Dict]:
        return self.active_games.get(game_id)
    
    def end_game(self, game_id: str) -> Optional[Dict]:
        game_data = self.active_games.pop(game_id, None)
        if game_data:
            logger.info(f"🏁 Game ended: {game_data['type']}")
        return game_data
    
    def is_game_active(self, game_id: str) -> bool:
        return game_id in self.active_games
    
    def set_theme(self, user_id: str, theme: str):
        self.user_themes[user_id] = theme
        logger.info(f"🎨 Theme set for {user_id}: {theme}")
    
    def get_theme(self, user_id: str) -> str:
        return self.user_themes.get(user_id, 'white')
    
    def cleanup_old_games(self, max_age_minutes: int = 15):
        """Clean up games older than max_age_minutes"""
        now = datetime.now()
        to_delete = []
        
        for game_id, game_data in self.active_games.items():
            age = now - game_data['created_at']
            if age > timedelta(minutes=max_age_minutes):
                to_delete.append(game_id)
        
        for game_id in to_delete:
            self.end_game(game_id)
        
        if to_delete:
            logger.info(f"🧹 Cleaned up {len(to_delete)} old games")

game_manager = GameManager()

# =============================================
# 🛠️ Helper Functions
# =============================================
def get_user_display_name(user_id: str) -> str:
    """Get user's display name from LINE"""
    try:
        profile = line_bot_api.get_profile(user_id)
        return profile.display_name
    except Exception as e:
        logger.error(f"❌ Failed to get profile: {e}")
        return "لاعب"

def get_flex_builder(user_id: str) -> FlexBuilder:
    """Get FlexBuilder with user's theme"""
    builder = FlexBuilder()
    theme = game_manager.get_theme(user_id)
    builder.set_theme(theme)
    return builder

# =============================================
# 💬 Command Handlers
# =============================================
class CommandHandler:
    """Handle bot commands"""
    
    def __init__(self):
        self.commands = {
            'مساعدة': self.handle_help,
            'help': self.handle_help,
            'انضم': self.handle_join,
            'تسجيل': self.handle_join,
            'انسحب': self.handle_leave,
            'خروج': self.handle_leave,
            'نقاطي': self.handle_stats,
            'احصائياتي': self.handle_stats,
            'الصدارة': self.handle_leaderboard,
            'إيقاف': self.handle_stop,
            'ايقاف': self.handle_stop,
            'ثيم': self.handle_theme_menu
        }
    
    def handle(self, event, user_id: str, text: str, game_id: str, display_name: str) -> bool:
        """Handle command if exists"""
        # Theme selection
        if text.startswith('ثيم:'):
            theme_name = text.split(':', 1)[1]
            self.set_theme(event, user_id, theme_name)
            return True
        
        # Standard commands
        if handler := self.commands.get(text):
            handler(event, user_id, game_id, display_name)
            return True
        
        return False
    
    def handle_help(self, event, user_id: str, *args):
        """Show help menu"""
        builder = get_flex_builder(user_id)
        flex_content = builder.create_help_menu()
        
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(alt_text="المساعدة", contents=flex_content)
        )
    
    def handle_join(self, event, user_id: str, game_id: str, display_name: str):
        """Register player"""
        if game_manager.is_registered(user_id):
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(
                    text=f"✅ أنت مسجل يا {display_name}\n\nاختر لعبة من الأزرار الثابتة أسفل الشاشة"
                )
            )
        else:
            game_manager.register_player(user_id)
            builder = get_flex_builder(user_id)
            
            line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage(
                    alt_text="مرحباً",
                    contents=builder.create_help_menu()
                )
            )
    
    def handle_leave(self, event, user_id: str, *args):
        """Unregister player"""
        if game_manager.is_registered(user_id):
            game_manager.unregister_player(user_id)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="👋 تم الانسحاب بنجاح\n\nاكتب 'انضم' للعودة")
            )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="❌ أنت غير مسجل")
            )
    
    def handle_stats(self, event, user_id: str, *args):
        """Show user statistics"""
        import asyncio
        
        asyncio.run(db.initialize())
        user = asyncio.run(db.get_user(user_id))
        rank = asyncio.run(db.get_user_rank(user_id)) if user else 0
        
        is_registered = game_manager.is_registered(user_id)
        
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
        
        builder = get_flex_builder(user_id)
        
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(
                alt_text="نقاطي",
                contents=builder.create_stats_card(user_data, rank)
            )
        )
    
    def handle_leaderboard(self, event, user_id: str, *args):
        """Show leaderboard"""
        import asyncio
        
        asyncio.run(db.initialize())
        leaders = asyncio.run(db.get_leaderboard())
        
        leaders_data = [
            {
                'display_name': leader.display_name,
                'total_points': leader.total_points
            }
            for leader in leaders
        ]
        
        builder = get_flex_builder(user_id)
        
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(
                alt_text="الصدارة",
                contents=builder.create_leaderboard(leaders_data)
            )
        )
    
    def handle_stop(self, event, user_id: str, game_id: str, *args):
        """Stop active game"""
        if game_manager.is_game_active(game_id):
            game_data = game_manager.end_game(game_id)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=f"⏹️ تم إيقاف لعبة {game_data['type']}")
            )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="❌ لا توجد لعبة نشطة")
            )
    
    def handle_theme_menu(self, event, user_id: str, *args):
        """Show theme selection menu"""
        builder = get_flex_builder(user_id)
        
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(
                alt_text="الثيمات",
                contents=builder.create_theme_selector()
            )
        )
    
    def set_theme(self, event, user_id: str, theme_name: str):
        """Set user theme"""
        game_manager.set_theme(user_id, theme_name)
        
        theme_names = {
            'white': '⚪ أبيض',
            'black': '⚫ أسود',
            'gray': '🔘 رمادي',
            'purple': '💜 بنفسجي',
            'blue': '💙 أزرق',
            'pink': '🌸 وردي',
            'mint': '🍃 نعناعي'
        }
        
        theme_display = theme_names.get(theme_name, theme_name)
        
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"✅ تم تغيير الثيم إلى {theme_display}")
        )

command_handler = CommandHandler()

# =============================================
# 🎮 Game Functions
# =============================================
def start_game(game_id: str, game_class: type, game_type: str, user_id: str, event):
    """Start a new game"""
    try:
        # Games that need AI
        ai_games = ['IqGame', 'WordColorGame', 'LettersWordsGame', 'HumanAnimalPlantGame']
        
        if game_class.__name__ in ai_games:
            game_instance = game_class(
                line_bot_api,
                use_ai=USE_AI,
                get_api_key=get_gemini_api_key,
                switch_key=switch_gemini_key
            )
        else:
            game_instance = game_class(line_bot_api)
        
        game_manager.create_game(game_id, game_instance, game_type)
        
        response = game_instance.start_game()
        line_bot_api.reply_message(event.reply_token, response)
        
        metrics.games_started += 1
        logger.info(f"🎮 Game started: {game_type} for {user_id}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to start game {game_type}: {e}")
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"❌ خطأ في بدء اللعبة. حاول مرة أخرى.")
        )
        return False

def handle_game_answer(event, user_id: str, text: str, game_id: str, display_name: str):
    """Handle answer for active game"""
    game_data = game_manager.get_game(game_id)
    if not game_data:
        return
    
    game = game_data['game']
    game_type = game_data['type']
    
    try:
        result = game.check_answer(text, user_id, display_name)
        
        if result:
            # Update points if earned
            if points := result.get('points', 0):
                if points > 0:
                    import asyncio
                    asyncio.run(db.initialize())
                    asyncio.run(db.update_user_score(
                        user_id,
                        display_name,
                        points,
                        result.get('won', False),
                        game_type
                    ))
            
            # End game if finished
            if result.get('game_over'):
                game_manager.end_game(game_id)
            
            # Send response
            response = result.get('response', TextSendMessage(text=result.get('message', '')))
            line_bot_api.reply_message(event.reply_token, response)
            
    except Exception as e:
        logger.error(f"❌ Error handling answer: {e}")

# =============================================
# 🌐 Flask Routes
# =============================================
@app.route("/")
def home():
    """Home page with status"""
    stats = metrics.get_stats()
    
    return f'''
    <!DOCTYPE html>
    <html dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Bot Mesh - Gaming Bot</title>
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
            .container {{
                background: white;
                border-radius: 20px;
                padding: 40px;
                max-width: 600px;
                width: 100%;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                text-align: center;
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
                border-radius: 10px;
                margin: 20px 0;
                font-weight: bold;
            }}
            .stats {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                gap: 15px;
                margin: 30px 0;
            }}
            .stat {{
                background: #f8f9fa;
                padding: 20px;
                border-radius: 10px;
                transition: transform 0.2s;
            }}
            .stat:hover {{
                transform: translateY(-5px);
            }}
            .stat-value {{
                font-size: 2.5em;
                font-weight: bold;
                color: #667eea;
                display: block;
            }}
            .stat-label {{
                color: #6c757d;
                font-size: 0.9em;
                margin-top: 5px;
            }}
            .footer {{
                margin-top: 30px;
                color: #6c757d;
                font-size: 0.9em;
            }}
            .info {{
                background: #e7f3ff;
                border-left: 4px solid #2196F3;
                padding: 15px;
                border-radius: 5px;
                margin: 20px 0;
                text-align: right;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎮 Bot Mesh</h1>
            <div class="status">✅ الخادم يعمل بنجاح</div>
            
            <div class="stats">
                <div class="stat">
                    <span class="stat-value">{len(GAMES_LOADED)}</span>
                    <div class="stat-label">ألعاب</div>
                </div>
                <div class="stat">
                    <span class="stat-value">{len(game_manager.registered_players)}</span>
                    <div class="stat-label">لاعبين</div>
                </div>
                <div class="stat">
                    <span class="stat-value">{len(game_manager.active_games)}</span>
                    <div class="stat-label">ألعاب نشطة</div>
                </div>
                <div class="stat">
                    <span class="stat-value">{stats['requests']}</span>
                    <div class="stat-label">طلبات</div>
                </div>
                <div class="stat">
                    <span class="stat-value">{stats['games']}</span>
                    <div class="stat-label">ألعاب بدأت</div>
                </div>
                <div class="stat">
                    <span class="stat-value">{stats['uptime_hours']}h</span>
                    <div class="stat-label">وقت التشغيل</div>
                </div>
            </div>
            
            <div class="info">
                <strong>🎯 الألعاب المتاحة:</strong><br>
                {', '.join(AVAILABLE_GAMES.keys())}
            </div>
            
            <div class="footer">
                <p><strong>Bot Mesh v{Config.BOT_VERSION}</strong></p>
                <p>Created by Abeer Aldosari © 2025</p>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route("/health")
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'version': Config.BOT_VERSION,
        'games': len(GAMES_LOADED),
        'players': len(game_manager.registered_players)
    }), 200

@app.route("/callback", methods=['POST'])
def callback():
    """LINE webhook callback"""
    signature = request.headers.get('X-Line-Signature')
    if not signature:
        abort(400)
    
    body = request.get_data(as_text=True)
    metrics.requests += 1
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        logger.error("❌ Invalid signature")
        abort(400)
    except Exception as e:
        logger.error(f"❌ Callback error: {e}", exc_info=True)
        abort(500)
    
    return 'OK'

# =============================================
# 📨 Message Handler
# =============================================
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    """Main message handler"""
    try:
        user_id = event.source.user_id
        text = event.message.text.strip()
        game_id = getattr(event.source, 'group_id', user_id)
        display_name = get_user_display_name(user_id)
        
        logger.info(f"📨 {display_name}: {text}")
        
        # Handle commands
        if command_handler.handle(event, user_id, text, game_id, display_name):
            return
        
        # Start game
        if text in AVAILABLE_GAMES:
            if not game_manager.is_registered(user_id):
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text="❌ اكتب 'انضم' أولاً")
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
            
            # Special handling for compatibility game
            if text == 'توافق':
                game_instance = game_class(line_bot_api)
                game_manager.create_game(game_id, game_instance, text)
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(
                        text="💖 لعبة التوافق!\n\nاكتب اسمين بمسافة\nمثال: ميش عبير"
                    )
                )
                return
            
            start_game(game_id, game_class, text, user_id, event)
            return
        
        # Handle game answers
        if game_manager.is_game_active(game_id) and game_manager.is_registered(user_id):
            handle_game_answer(event, user_id, text, game_id, display_name)
        
    except Exception as e:
        logger.error(f"❌ Message handler error: {e}", exc_info=True)

# =============================================
# 🚀 Startup
# =============================================
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    
    logger.info("=" * 50)
    logger.info("🎮 BOT MESH v2.0")
    logger.info("=" * 50)
    logger.info(f"🌐 Port: {port}")
    logger.info(f"🎯 Games loaded: {len(GAMES_LOADED)}")
    logger.info(f"🎨 Available themes: 7")
    logger.info(f"🤖 AI enabled: {USE_AI}")
    logger.info("=" * 50)
    logger.info("Created by: Abeer Aldosari © 2025")
    logger.info("=" * 50)
    
    app.run(host='0.0.0.0', port=port, debug=Config.DEBUG)
