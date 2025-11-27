"""
Bot Mesh v9.0 - Main Server (Fixed & Clean)
Created by: Abeer Aldosari © 2025
"""

import os
import logging
import threading
import time
from collections import defaultdict
from flask import Flask, request, abort

from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import Configuration, ApiClient, MessagingApi, ReplyMessageRequest, TextMessage
from linebot.v3.webhooks import MessageEvent, TextMessageContent, FollowEvent

from ui import (
    build_home, build_games_menu, build_my_points, build_leaderboard,
    build_registration_required, build_help, send_text_with_quick_reply
)
from db import DB

# استيراد GameLoader من ملف games.py المبسط
try:
    from games import GameLoader
except ImportError:
    # إذا فشل، جرب من games/loader.py
    from games.loader import GameLoader

# ============================================================================
# Setup
# ============================================================================
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ============================================================================
# Configuration
# ============================================================================
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', '')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET', '')
PORT = int(os.getenv('PORT', 10000))

if not LINE_CHANNEL_ACCESS_TOKEN or not LINE_CHANNEL_SECRET:
    logger.error("❌ LINE credentials missing!")
    exit(1)

# ============================================================================
# Initialize
# ============================================================================
app = Flask(__name__)
db = DB()
game_loader = GameLoader()

configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

logger.info(f"✅ Bot Mesh initialized with {len(game_loader.loaded)} games")

# ============================================================================
# Rate Limiting
# ============================================================================
class SimpleRateLimiter:
    def __init__(self):
        self.requests = defaultdict(list)
        self.lock = threading.Lock()
    
    def is_allowed(self, user_id: str, max_per_minute: int = 10) -> bool:
        with self.lock:
            now = time.time()
            minute_ago = now - 60
            self.requests[user_id] = [t for t in self.requests[user_id] if t > minute_ago]
            if len(self.requests[user_id]) >= max_per_minute:
                return False
            self.requests[user_id].append(now)
            return True

rate_limiter = SimpleRateLimiter()

# ============================================================================
# Helper Functions
# ============================================================================
def normalize_text(text: str) -> str:
    if not text:
        return ""
    text = text.strip().lower()
    replacements = {'أ': 'ا', 'إ': 'ا', 'آ': 'ا', 'ى': 'ي', 'ة': 'ه'}
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text

def get_username(profile) -> str:
    try:
        return profile.display_name if profile.display_name else "مستخدم"
    except:
        return "مستخدم"

def safe_reply(line_bot_api, reply_token, messages):
    try:
        if not isinstance(messages, list):
            messages = [messages]
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(reply_token=reply_token, messages=messages)
        )
        return True
    except Exception as e:
        logger.error(f"❌ Failed to send reply: {e}")
        return False

# ============================================================================
# Background Message Processing
# ============================================================================
def process_message_background(user_id: str, text: str, reply_token: str):
    try:
        if not rate_limiter.is_allowed(user_id, 10):
            logger.warning(f"⚠️ Rate limit exceeded for {user_id}")
            return
        
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            profile = line_bot_api.get_profile(user_id)
            name = get_username(profile)
            
            user = db.get_user(user_id)
            theme = user['theme'] if user else 'بنفسجي'
            points = user['points'] if user else 0
            is_registered = user is not None and user['status'] == 'active'
            
            normalized = normalize_text(text)
            
            # ==================== الأوامر الأساسية ====================
            
            if normalized in ['بداية', 'start', 'home']:
                msg = build_home(theme, name, points, is_registered)
                safe_reply(line_bot_api, reply_token, msg)
                return
            
            if normalized in ['مساعدة', 'help']:
                msg = build_help(theme)
                safe_reply(line_bot_api, reply_token, msg)
                return
            
            if normalized.startswith('ثيم '):
                new_theme = text.replace('ثيم ', '').strip()
                if new_theme in ['بنفسجي', 'أخضر', 'أزرق', 'رمادي', 'وردي', 'برتقالي', 'أبيض', 'بني', 'أصفر']:
                    if user:
                        db.update_theme(user_id, new_theme)
                        theme = new_theme
                    msg = build_home(theme, name, points, is_registered)
                    safe_reply(line_bot_api, reply_token, msg)
                return
            
            if normalized in ['انضم', 'join']:
                if not is_registered:
                    db.create_user(user_id, name, theme)
                    text_msg = send_text_with_quick_reply(f"▪️ تم تسجيلك يا {name}")
                else:
                    text_msg = send_text_with_quick_reply(f"▪️ أنت مسجل بالفعل يا {name}")
                safe_reply(line_bot_api, reply_token, text_msg)
                return
            
            if normalized in ['انسحب', 'leave']:
                if is_registered:
                    db.deactivate_user(user_id)
                    text_msg = send_text_with_quick_reply(f"▫️ تم إلغاء تسجيلك يا {name}")
                else:
                    text_msg = send_text_with_quick_reply("▫️ أنت غير مسجل")
                safe_reply(line_bot_api, reply_token, text_msg)
                return
            
            if normalized in ['العاب', 'games', 'ألعاب']:
                if not is_registered:
                    msg = build_registration_required(theme)
                else:
                    msg = build_games_menu(theme)
                safe_reply(line_bot_api, reply_token, msg)
                return
            
            if normalized in ['نقاطي', 'points']:
                if not is_registered:
                    msg = build_registration_required(theme)
                else:
                    msg = build_my_points(name, points, theme)
                safe_reply(line_bot_api, reply_token, msg)
                return
            
            if normalized in ['صدارة', 'leaderboard']:
                top = db.get_leaderboard(10)
                msg = build_leaderboard(top, theme)
                safe_reply(line_bot_api, reply_token, msg)
                return
            
            # ==================== الألعاب ====================
            
            if normalized.startswith('لعبة ') or normalized.startswith('لعبه '):
                if not is_registered:
                    msg = build_registration_required(theme)
                    safe_reply(line_bot_api, reply_token, msg)
                    return
                
                game_name = text.replace('لعبة ', '').replace('لعبه ', '').strip()
                
                if game_loader.has_active_game(user_id):
                    game_loader.end_game(user_id)
                
                response = game_loader.start_game(user_id, game_name)
                
                if not response:
                    text_msg = send_text_with_quick_reply(f"▫️ اللعبة '{game_name}' غير موجودة")
                    safe_reply(line_bot_api, reply_token, text_msg)
                    return
                
                safe_reply(line_bot_api, reply_token, response)
                return
            
            if normalized in ['إيقاف', 'stop', 'ايقاف']:
                if game_loader.has_active_game(user_id):
                    game_loader.end_game(user_id)
                    text_msg = send_text_with_quick_reply("▫️ تم إيقاف اللعبة")
                else:
                    text_msg = send_text_with_quick_reply("▫️ لا توجد لعبة نشطة")
                safe_reply(line_bot_api, reply_token, text_msg)
                return
            
            # ==================== أثناء اللعب ====================
            
            if game_loader.has_active_game(user_id):
                game = game_loader.get_game(user_id)
                
                if normalized in ['لمح', 'hint']:
                    hint = game.get_hint() if hasattr(game, 'get_hint') else "▫️ لا يوجد تلميح"
                    hint_msg = send_text_with_quick_reply(hint)
                    safe_reply(line_bot_api, reply_token, hint_msg)
                    return
                
                result = game.check_answer(text, user_id, name)
                
                if result:
                    if result.get('points', 0) > 0:
                        db.add_points(user_id, result['points'])
                    
                    if 'response' in result:
                        safe_reply(line_bot_api, reply_token, result['response'])
                    else:
                        text_msg = send_text_with_quick_reply(result.get('message', 'حدث خطأ'))
                        safe_reply(line_bot_api, reply_token, text_msg)
                    
                    if result.get('game_over'):
                        game_loader.end_game(user_id)
                    
                    return
            
            if not is_registered:
                logger.info(f"Ignored message from unregistered user: {user_id}")
                return
            
            default_msg = send_text_with_quick_reply("▫️ لم أفهم الأمر. اكتب 'مساعدة' للمساعدة")
            safe_reply(line_bot_api, reply_token, default_msg)
            
    except Exception as e:
        logger.error(f"❌ Background processing error: {e}", exc_info=True)

# ============================================================================
# Webhook Handlers
# ============================================================================
@handler.add(FollowEvent)
def handle_follow(event):
    user_id = event.source.user_id
    
    def background():
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            try:
                profile = line_bot_api.get_profile(user_id)
                name = get_username(profile)
                db.create_user(user_id, name, 'بنفسجي')
                msg = build_home('بنفسجي', name, 0, True)
                line_bot_api.push_message_with_http_info(user_id, [msg])
            except Exception as e:
                logger.error(f"❌ Follow error: {e}")
    
    threading.Thread(target=background, daemon=True).start()

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    user_id = event.source.user_id
    text = event.message.text.strip()
    reply_token = event.reply_token
    
    threading.Thread(
        target=process_message_background,
        args=(user_id, text, reply_token),
        daemon=True
    ).start()

# ============================================================================
# Flask Routes
# ============================================================================
@app.route("/", methods=["GET"])
def home():
    return {
        "status": "running",
        "bot": "Bot Mesh v9.0",
        "games": len(game_loader.loaded),
        "users": db.get_total_users()
    }

@app.route("/health", methods=["GET"])
def health():
    return {
        "status": "healthy",
        "games_loaded": len(game_loader.loaded),
        "active_sessions": len(game_loader.active_sessions)
    }, 200

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        logger.error("❌ Invalid signature")
        abort(400)
    except Exception as e:
        logger.error(f"❌ Callback error: {e}", exc_info=True)
    
    return "OK"

@app.route("/stats", methods=["GET"])
def stats():
    return {
        "total_users": db.get_total_users(),
        "total_points": db.get_total_points(),
        "games_available": len(game_loader.loaded),
        "active_games": len(game_loader.active_sessions),
        "leaderboard": db.get_leaderboard(5)
    }

# ============================================================================
# Error Handlers
# ============================================================================
@app.errorhandler(404)
def not_found(error):
    return {"error": "Not found"}, 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"❌ Internal error: {error}")
    return {"error": "Internal server error"}, 500

# ============================================================================
# Startup
# ============================================================================
if __name__ == "__main__":
    logger.info(f"""
    ╔══════════════════════════════════╗
    ║   Bot Mesh v9.0 Starting         ║
    ║   Port: {PORT}                    ║
    ║   Games: {len(game_loader.loaded)}                   ║
    ╚══════════════════════════════════╝
    """)
    
    app.run(host="0.0.0.0", port=PORT, debug=False)
