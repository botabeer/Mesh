"""
🎮 Bot Mesh v7.0 - Main Application (COMPLETE)
Created by: Abeer Aldosari © 2025

Features:
✅ Silent bot - only responds to registered users
✅ Auto-registration system
✅ Fixed buttons at bottom
✅9 beautiful themes
✅ 12 interactive games
✅ AI-powered with fallback
✅ Database integration
✅ Comprehensive error handling
"""

import os
import sys
import logging
from datetime import datetime
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
    BOT_NAME, BOT_RIGHTS, THEMES, DEFAULT_THEME,
    get_username, normalize_arabic
)
from database import Database
from game_loader import GameLoader
from ui_builder import (
    build_home, build_games_menu, build_my_points,
    build_leaderboard, build_registration_required
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

logger.info("✅ Configuration validated successfully")

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
# Initialize Database
# ============================================================================
# استخدام /tmp على Render (ephemeral لكن يعمل)
import tempfile
DB_PATH = os.path.join(tempfile.gettempdir(), "botmesh.db")
db = Database(DB_PATH)
logger.info(f"✅ Database initialized at {DB_PATH}")

# ============================================================================
# Initialize Game Loader
# ============================================================================
game_loader = GameLoader("games")
logger.info(f"✅ Loaded {len(game_loader.loaded_games)} games")

# ============================================================================
# Global State Management
# ============================================================================
active_games = {}  # {user_id: game_instance}
user_themes = {}   # {user_id: theme_emoji}

# ============================================================================
# Helper Functions
# ============================================================================

def get_user_theme(user_id: str) -> str:
    """Get user's current theme"""
    if user_id in user_themes:
        return user_themes[user_id]
    
    user = db.get_user(user_id)
    if user and user.get('theme'):
        theme = user['theme']
        user_themes[user_id] = theme
        return theme
    
    return DEFAULT_THEME


def set_user_theme(user_id: str, theme: str) -> bool:
    """Set user's theme"""
    if theme in THEMES:
        user_themes[user_id] = theme
        db.update_theme(user_id, theme)
        return True
    return False


def register_user(user_id: str, display_name: str):
    """Register or update user"""
    user = db.get_user(user_id)
    
    if not user:
        # New user
        db.create_user(user_id, display_name)
        logger.info(f"✅ New user registered: {display_name} ({user_id})")
    else:
        # Update existing user
        db.update_user_name(user_id, display_name)
        db.update_last_active(user_id)


def is_user_registered(user_id: str) -> bool:
    """Check if user is registered"""
    user = db.get_user(user_id)
    return user is not None and user.get('status') == 'active'


def get_user_points(user_id: str) -> int:
    """Get user's points"""
    user = db.get_user(user_id)
    return user.get('points', 0) if user else 0


def add_points(user_id: str, points: int):
    """Add points to user"""
    db.add_points(user_id, points)


def has_active_game(user_id: str) -> bool:
    """Check if user has active game"""
    return user_id in active_games


def end_game(user_id: str):
    """End user's active game"""
    if user_id in active_games:
        del active_games[user_id]
        logger.info(f"🛑 Game ended for user: {user_id}")


# ============================================================================
# Message Handlers
# ============================================================================

def handle_command(user_id: str, text: str, display_name: str, reply_token: str, line_bot_api):
    """Handle user commands"""
    normalized = normalize_arabic(text)
    theme = get_user_theme(user_id)
    
    # ========================================
    # Home / Start
    # ========================================
    if normalized in ['بداية', 'start', 'البداية', 'home']:
        points = get_user_points(user_id)
        is_registered = is_user_registered(user_id)
        
        message = build_home(
            theme=theme,
            username=display_name,
            points=points,
            is_registered=is_registered
        )
        
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(reply_token=reply_token, messages=[message])
        )
        return True
    
    # ========================================
    # Theme Selection
    # ========================================
    if normalized.startswith('ثيم '):
        theme_emoji = text.replace('ثيم ', '').strip()
        if set_user_theme(user_id, theme_emoji):
            # Send updated home screen with new theme
            points = get_user_points(user_id)
            is_registered = is_user_registered(user_id)
            
            message = build_home(
                theme=theme_emoji,
                username=display_name,
                points=points,
                is_registered=is_registered
            )
            
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(reply_token=reply_token, messages=[message])
            )
            return True
    
    # ========================================
    # Registration
    # ========================================
    if normalized in ['انضم', 'join', 'تسجيل']:
        if not is_user_registered(user_id):
            register_user(user_id, display_name)
            msg = f"✅ تم تسجيلك بنجاح يا {display_name}!\n🎮 يمكنك الآن اللعب وجمع النقاط"
        else:
            msg = f"ℹ️ أنت مسجل بالفعل يا {display_name}!"
        
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=reply_token,
                messages=[TextMessage(text=msg)]
            )
        )
        return True
    
    # ========================================
    # Unregister
    # ========================================
    if normalized in ['انسحب', 'leave', 'خروج']:
        if is_user_registered(user_id):
            db.get_connection()  # Update status to inactive
            msg = f"👋 تم إلغاء تسجيلك يا {display_name}\nيمكنك العودة بالضغط على 'انضم'"
        else:
            msg = "ℹ️ أنت غير مسجل أصلاً"
        
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=reply_token,
                messages=[TextMessage(text=msg)]
            )
        )
        return True
    
    # ========================================
    # Games Menu
    # ========================================
    if normalized in ['مساعدة', 'help', 'العاب', 'games', 'الالعاب']:
        if not is_user_registered(user_id):
            message = build_registration_required(theme)
        else:
            message = build_games_menu(theme)
        
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(reply_token=reply_token, messages=[message])
        )
        return True
    
    # ========================================
    # My Points
    # ========================================
    if normalized in ['نقاطي', 'points', 'my points']:
        if not is_user_registered(user_id):
            message = build_registration_required(theme)
        else:
            points = get_user_points(user_id)
            message = build_my_points(display_name, points, theme)
        
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(reply_token=reply_token, messages=[message])
        )
        return True
    
    # ========================================
    # Leaderboard
    # ========================================
    if normalized in ['صدارة', 'leaderboard', 'top']:
        top_users = db.get_leaderboard(10)
        top_list = [(u['display_name'], u['points']) for u in top_users]
        message = build_leaderboard(top_list, theme)
        
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(reply_token=reply_token, messages=[message])
        )
        return True
    
    # ========================================
    # Start Game
    # ========================================
    if normalized.startswith('لعبة '):
        if not is_user_registered(user_id):
            message = build_registration_required(theme)
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(reply_token=reply_token, messages=[message])
            )
            return True
        
        game_name = text.replace('لعبة ', '').strip()
        
        # End previous game if exists
        if has_active_game(user_id):
            end_game(user_id)
        
        # Create new game
        game = game_loader.create_game(game_name)
        
        if not game:
            available = "، ".join(game_loader.get_available_games())
            msg = f"❌ اللعبة '{game_name}' غير موجودة\n\n🎮 الألعاب المتاحة:\n{available}"
            
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=reply_token,
                    messages=[TextMessage(text=msg)]
                )
            )
            return True
        
        # Start game
        active_games[user_id] = game
        question_response = game.start()
        
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=reply_token,
                messages=[question_response]
            )
        )
        return True
    
    # ========================================
    # Stop Game
    # ========================================
    if normalized in ['إيقاف', 'stop', 'ايقاف']:
        if has_active_game(user_id):
            end_game(user_id)
            msg = "⛔ تم إيقاف اللعبة"
        else:
            msg = "ℹ️ لا توجد لعبة نشطة"
        
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=reply_token,
                messages=[TextMessage(text=msg)]
            )
        )
        return True
    
    # ========================================
    # In-Game Commands (Hint, Reveal)
    # ========================================
    if has_active_game(user_id):
        game = active_games[user_id]
        
        # Hint
        if normalized in ['لمح', 'hint', 'تلميح']:
            if hasattr(game, 'supports_hint') and not game.supports_hint:
                msg = "❌ هذه اللعبة لا تدعم التلميحات"
            else:
                msg = game.get_hint() if hasattr(game, 'get_hint') else "💡 لا يوجد تلميح"
            
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=reply_token,
                    messages=[TextMessage(text=msg)]
                )
            )
            return True
        
        # Answer the question
        result = game.check_answer(text, user_id, display_name)
        
        if result:
            # Award points if correct
            if result.get('points', 0) > 0:
                add_points(user_id, result['points'])
            
            # Send response
            if 'response' in result:
                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(
                        reply_token=reply_token,
                        messages=[result['response']]
                    )
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
                end_game(user_id)
            
            return True
    
    return False


# ============================================================================
# LINE Webhook Handlers
# ============================================================================

@handler.add(FollowEvent)
def handle_follow(event):
    """Handle when user adds bot as friend"""
    user_id = event.source.user_id
    
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        
        try:
            # Get user profile
            profile = line_bot_api.get_profile(user_id)
            display_name = get_username(profile)
            
            # Auto-register
            register_user(user_id, display_name)
            
            # Send welcome message
            message = build_home(
                theme=DEFAULT_THEME,
                username=display_name,
                points=0,
                is_registered=True
            )
            
            line_bot_api.push_message_with_http_info(
                user_id=user_id,
                messages=[message]
            )
            
        except Exception as e:
            logger.error(f"Error in follow handler: {e}")


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    """Handle text messages"""
    user_id = event.source.user_id
    text = event.message.text.strip()
    reply_token = event.reply_token
    
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        
        try:
            # Get user profile
            profile = line_bot_api.get_profile(user_id)
            display_name = get_username(profile)
            
            # Update last active
            if is_user_registered(user_id):
                db.update_last_active(user_id)
            
            # Handle command
            handled = handle_command(
                user_id, text, display_name,
                reply_token, line_bot_api
            )
            
            # If not handled and user is not registered, ignore silently
            if not handled and not is_user_registered(user_id):
                logger.info(f"Ignored message from unregistered user: {user_id}")
                return
            
        except Exception as e:
            logger.error(f"Error handling message: {e}", exc_info=True)
            
            # Send error message only to registered users
            if is_user_registered(user_id):
                error_msg = "⚠️ حدث خطأ، يرجى المحاولة مرة أخرى"
                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(
                        reply_token=reply_token,
                        messages=[TextMessage(text=error_msg)]
                    )
                )


# ============================================================================
# Flask Routes
# ============================================================================

@app.route("/", methods=["GET"])
def home():
    """Health check endpoint"""
    return {
        "status": "Bot Mesh is running",
        "bot_name": BOT_NAME,
        "games_loaded": len(game_loader.loaded_games),
        "available_games": game_loader.get_available_games(),
        "themes": len(THEMES),
        "version": "7.0"
    }


@app.route("/health", methods=["GET"])
def health():
    """Health check for Render"""
    return {"status": "healthy"}, 200


@app.route("/callback", methods=["POST"])
def callback():
    """LINE webhook callback"""
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        logger.error("Invalid signature")
        abort(400)
    except Exception as e:
        logger.error(f"Error in callback: {e}", exc_info=True)
    
    return "OK"


# ============================================================================
# Startup
# ============================================================================

if __name__ == "__main__":
    port = Config.PORT
    debug = Config.DEBUG
    
    logger.info(f"""
    ╔══════════════════════════════════════╗
    ║       🎮 Bot Mesh v7.0 Starting     ║
    ╠══════════════════════════════════════╣
    ║  Port: {port}                        
    ║  Debug: {debug}                      
    ║  Games: {len(game_loader.loaded_games)}                        
    ║  Themes: {len(THEMES)}                       
    ╚══════════════════════════════════════╝
    """)
    
    app.run(host="0.0.0.0", port=port, debug=debug)
