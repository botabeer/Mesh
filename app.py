"""
🎮 Bot Mesh v7.0 - Main Application (TIMEOUT FIXED)
Created by: Abeer Aldosari © 2025

✅ No database file errors
✅ Fast response (< 1 second)
✅ Silent bot behavior
✅ Comprehensive error handling
"""

import os
import sys
import logging
from flask import Flask, request, abort

from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi,
    ReplyMessageRequest, TextMessage
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent, FollowEvent

# Import local modules
from config import Config
from constants import (
    BOT_NAME, THEMES, DEFAULT_THEME,
    get_username, normalize_arabic
)

# ============================================================================
# Setup Logging
# ============================================================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# Validate Configuration
# ============================================================================
if not Config.is_valid():
    is_valid, errors = Config.validate()
    logger.error(f"❌ Configuration errors: {errors}")
    sys.exit(1)

logger.info("✅ Configuration validated")

# ============================================================================
# Initialize Flask
# ============================================================================
app = Flask(__name__)

# ============================================================================
# Initialize LINE SDK
# ============================================================================
configuration = Configuration(access_token=Config.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(Config.LINE_CHANNEL_SECRET)

# ============================================================================
# In-Memory Database (Simple & Fast)
# ============================================================================
class SimpleDB:
    """قاعدة بيانات بسيطة في الذاكرة"""
    
    def __init__(self):
        self.users = {}  # {user_id: {name, points, theme, status}}
        self.active_games = {}  # {user_id: game_instance}
        logger.info("✅ In-memory database initialized")
    
    def get_user(self, user_id):
        return self.users.get(user_id)
    
    def create_user(self, user_id, name):
        self.users[user_id] = {
            'name': name,
            'points': 0,
            'theme': DEFAULT_THEME,
            'status': 'active'
        }
        logger.info(f"✅ User created: {name}")
        return self.users[user_id]
    
    def update_user(self, user_id, **kwargs):
        if user_id in self.users:
            self.users[user_id].update(kwargs)
    
    def add_points(self, user_id, points):
        if user_id in self.users:
            self.users[user_id]['points'] += points
    
    def get_leaderboard(self, limit=10):
        sorted_users = sorted(
            [(uid, u) for uid, u in self.users.items() if u['status'] == 'active'],
            key=lambda x: x[1]['points'],
            reverse=True
        )
        return [(u['name'], u['points']) for _, u in sorted_users[:limit]]

# ============================================================================
# Initialize Database
# ============================================================================
db = SimpleDB()

# ============================================================================
# Lazy Load Games (Only when needed)
# ============================================================================
game_loader = None

def get_game_loader():
    """Load games only when first requested"""
    global game_loader
    if game_loader is None:
        from game_loader import GameLoader
        game_loader = GameLoader("games")
        logger.info(f"✅ Loaded {len(game_loader.loaded_games)} games")
    return game_loader

# ============================================================================
# Helper Functions
# ============================================================================

def is_registered(user_id):
    """Check if user is registered"""
    user = db.get_user(user_id)
    return user is not None and user['status'] == 'active'


def register_user(user_id, name):
    """Register new user"""
    user = db.get_user(user_id)
    if not user:
        db.create_user(user_id, name)
    else:
        db.update_user(user_id, name=name, status='active')


# ============================================================================
# Message Handlers (FAST - No blocking operations)
# ============================================================================

def handle_command(user_id, text, name, reply_token, line_bot_api):
    """Handle user commands - MUST BE FAST"""
    
    normalized = normalize_arabic(text)
    
    # Import UI builders only when needed
    from ui_builder import (
        build_home, build_games_menu, build_my_points,
        build_leaderboard, build_registration_required
    )
    
    # ========================================
    # Home
    # ========================================
    if normalized in ['بداية', 'start', 'home']:
        user = db.get_user(user_id)
        theme = user['theme'] if user else DEFAULT_THEME
        points = user['points'] if user else 0
        is_reg = is_registered(user_id)
        
        msg = build_home(theme, name, points, is_reg)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(reply_token=reply_token, messages=[msg])
        )
        return True
    
    # ========================================
    # Theme Selection
    # ========================================
    if normalized.startswith('ثيم '):
        theme = text.replace('ثيم ', '').strip()
        if theme in THEMES:
            db.update_user(user_id, theme=theme)
            user = db.get_user(user_id)
            msg = build_home(theme, name, user['points'], True)
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(reply_token=reply_token, messages=[msg])
            )
            return True
    
    # ========================================
    # Registration
    # ========================================
    if normalized in ['انضم', 'join']:
        if not is_registered(user_id):
            register_user(user_id, name)
            text = f"✅ تم تسجيلك يا {name}!"
        else:
            text = f"ℹ️ أنت مسجل بالفعل يا {name}"
        
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(reply_token=reply_token, messages=[TextMessage(text=text)])
        )
        return True
    
    # ========================================
    # Unregister
    # ========================================
    if normalized in ['انسحب', 'leave']:
        if is_registered(user_id):
            db.update_user(user_id, status='inactive')
            text = f"👋 تم إلغاء تسجيلك يا {name}"
        else:
            text = "ℹ️ أنت غير مسجل"
        
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(reply_token=reply_token, messages=[TextMessage(text=text)])
        )
        return True
    
    # ========================================
    # Games Menu
    # ========================================
    if normalized in ['مساعدة', 'help', 'العاب', 'games']:
        user = db.get_user(user_id)
        theme = user['theme'] if user else DEFAULT_THEME
        
        if not is_registered(user_id):
            msg = build_registration_required(theme)
        else:
            msg = build_games_menu(theme)
        
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(reply_token=reply_token, messages=[msg])
        )
        return True
    
    # ========================================
    # My Points
    # ========================================
    if normalized in ['نقاطي', 'points']:
        user = db.get_user(user_id)
        theme = user['theme'] if user else DEFAULT_THEME
        
        if not is_registered(user_id):
            msg = build_registration_required(theme)
        else:
            msg = build_my_points(name, user['points'], theme)
        
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(reply_token=reply_token, messages=[msg])
        )
        return True
    
    # ========================================
    # Leaderboard
    # ========================================
    if normalized in ['صدارة', 'leaderboard']:
        user = db.get_user(user_id)
        theme = user['theme'] if user else DEFAULT_THEME
        top = db.get_leaderboard(10)
        msg = build_leaderboard(top, theme)
        
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(reply_token=reply_token, messages=[msg])
        )
        return True
    
    # ========================================
    # Start Game
    # ========================================
    if normalized.startswith('لعبة '):
        if not is_registered(user_id):
            user = db.get_user(user_id)
            theme = user['theme'] if user else DEFAULT_THEME
            msg = build_registration_required(theme)
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(reply_token=reply_token, messages=[msg])
            )
            return True
        
        game_name = text.replace('لعبة ', '').strip()
        loader = get_game_loader()
        
        # End previous game
        if user_id in db.active_games:
            del db.active_games[user_id]
        
        # Create game
        game = loader.create_game(game_name)
        
        if not game:
            available = "، ".join(loader.get_available_games())
            text = f"❌ اللعبة '{game_name}' غير موجودة\n\n🎮 المتاحة:\n{available}"
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(reply_token=reply_token, messages=[TextMessage(text=text)])
            )
            return True
        
        # Start game
        db.active_games[user_id] = game
        response = game.start()
        
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(reply_token=reply_token, messages=[response])
        )
        return True
    
    # ========================================
    # Stop Game
    # ========================================
    if normalized in ['إيقاف', 'stop', 'ايقاف']:
        if user_id in db.active_games:
            del db.active_games[user_id]
            text = "⛔ تم إيقاف اللعبة"
        else:
            text = "ℹ️ لا توجد لعبة نشطة"
        
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(reply_token=reply_token, messages=[TextMessage(text=text)])
        )
        return True
    
    # ========================================
    # In-Game Commands
    # ========================================
    if user_id in db.active_games:
        game = db.active_games[user_id]
        
        # Hint
        if normalized in ['لمح', 'hint']:
            hint = game.get_hint() if hasattr(game, 'get_hint') else "💡 لا يوجد تلميح"
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(reply_token=reply_token, messages=[TextMessage(text=hint)])
            )
            return True
        
        # Check answer
        result = game.check_answer(text, user_id, name)
        
        if result:
            # Award points
            if result.get('points', 0) > 0:
                db.add_points(user_id, result['points'])
            
            # Send response
            if 'response' in result:
                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(reply_token=reply_token, messages=[result['response']])
                )
            else:
                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(
                        reply_token=reply_token,
                        messages=[TextMessage(text=result.get('message', 'حدث خطأ'))]
                    )
                )
            
            # End game if finished
            if result.get('game_over'):
                del db.active_games[user_id]
            
            return True
    
    return False


# ============================================================================
# LINE Webhook Handlers
# ============================================================================

@handler.add(FollowEvent)
def handle_follow(event):
    """Handle when user adds bot"""
    user_id = event.source.user_id
    
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        
        try:
            profile = line_bot_api.get_profile(user_id)
            name = get_username(profile)
            
            # Auto-register
            register_user(user_id, name)
            
            # Send welcome
            from ui_builder import build_home
            msg = build_home(DEFAULT_THEME, name, 0, True)
            
            line_bot_api.push_message_with_http_info(
                user_id=user_id,
                messages=[msg]
            )
            
        except Exception as e:
            logger.error(f"Follow error: {e}")


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    """Handle text messages - MUST BE FAST"""
    user_id = event.source.user_id
    text = event.message.text.strip()
    reply_token = event.reply_token
    
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        
        try:
            # Get profile
            profile = line_bot_api.get_profile(user_id)
            name = get_username(profile)
            
            # Handle command
            handled = handle_command(user_id, text, name, reply_token, line_bot_api)
            
            # Ignore if not handled and not registered
            if not handled and not is_registered(user_id):
                logger.info(f"Ignored: {user_id}")
                # Send empty response to acknowledge
                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(
                        reply_token=reply_token,
                        messages=[TextMessage(text="")]
                    )
                )
                return
            
        except Exception as e:
            logger.error(f"Message error: {e}", exc_info=True)
            
            # Always respond to avoid timeout
            try:
                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(
                        reply_token=reply_token,
                        messages=[TextMessage(text="⚠️ حدث خطأ")]
                    )
                )
            except:
                pass


# ============================================================================
# Flask Routes
# ============================================================================

@app.route("/", methods=["GET"])
def home():
    """Health check"""
    loader = get_game_loader()
    return {
        "status": "running",
        "bot": BOT_NAME,
        "games": len(loader.loaded_games),
        "users": len(db.users)
    }


@app.route("/health", methods=["GET"])
def health():
    """Health check for Render"""
    return {"status": "healthy"}, 200


@app.route("/callback", methods=["POST"])
def callback():
    """LINE webhook - MUST RESPOND QUICKLY"""
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        logger.error("Invalid signature")
        abort(400)
    except Exception as e:
        logger.error(f"Callback error: {e}", exc_info=True)
    
    return "OK"


# ============================================================================
# Startup
# ============================================================================

if __name__ == "__main__":
    logger.info(f"""
    ╔══════════════════════════════════╗
    ║   🎮 {BOT_NAME} v7.0 Starting   ║
    ║   Port: {Config.PORT}                    ║
    ║   Ready for LINE webhooks       ║
    ╚══════════════════════════════════╝
    """)
    
    app.run(host="0.0.0.0", port=Config.PORT, debug=Config.DEBUG)
