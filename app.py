"""
Bot Mesh - Main Application (Fixed & Enhanced)
Created by: Abeer Aldosari © 2025
"""
import os
import logging
from flask import Flask, request, abort, jsonify

# === LINE SDK v3 - Correct Imports ===
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
    FlexMessage,
    FlexContainer
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent, FollowEvent

# استيراد المكونات
from config import LINE_TOKEN, LINE_SECRET, DB_PATH, THEMES
from database import DB
from flex_builder import FlexBuilder
from game_manager import GameManager

# استيراد جميع الألعاب تلقائياً
from games import *

# ==================== Logging ====================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ==================== Flask & Line ====================
app = Flask(__name__)

configuration = Configuration(access_token=LINE_TOKEN)
handler = WebhookHandler(LINE_SECRET)

# Initialize managers
db = DB(DB_PATH)
gm = GameManager()

# ==================== قاموس الألعاب ====================
GAMES = {
    'ذكاء': IqGame,
    'لون': WordColorGame,
    'ترتيب': ScrambleWordGame,
    'رياضيات': MathGame,
    'أسرع': FastTypingGame,
    'ضد': OppositeGame,
    'تكوين': LettersWordsGame,
    'أغنية': SongGame,
    'لعبة': HumanAnimalPlantGame,
    'سلسلة': ChainWordsGame,
    'خمن': GuessGame,
    'توافق': CompatibilityGame
}

# ==================== Helpers ====================
def get_name(uid):
    try:
        with ApiClient(configuration) as api_client:
            line_api = MessagingApi(api_client)
            profile = line_api.get_profile(uid)
            return profile.display_name
    except Exception as e:
        logger.error(f'Error getting profile: {e}')
        return 'لاعب'

def get_theme(uid):
    user = db.get_user(uid)
    return user.get('theme', 'white') if user else 'white'

def send_flex_reply(reply_token, flex_content, alt_text='القائمة'):
    """إرسال رسالة Flex"""
    try:
        with ApiClient(configuration) as api_client:
            line_api = MessagingApi(api_client)
            
            flex_msg = FlexMessage(
                altText=alt_text,
                contents=FlexContainer.from_dict(flex_content)
            )
            
            line_api.reply_message(
                ReplyMessageRequest(
                    replyToken=reply_token,
                    messages=[flex_msg]
                )
            )
            return True
    except Exception as e:
        logger.error(f'❌ Error sending flex reply: {e}')
    return False

def send_text_reply(reply_token, text):
    try:
        with ApiClient(configuration) as api_client:
            line_api = MessagingApi(api_client)
            line_api.reply_message(
                ReplyMessageRequest(
                    replyToken=reply_token,
                    messages=[TextMessage(text=text)]
                )
            )
            return True
    except Exception as e:
        logger.error(f'❌ Error sending text reply: {e}')
    return False

def create_welcome_flex(uid):
    """نافذة الترحيب"""
    theme = get_theme(uid)
    colors = THEMES[theme]
    user = db.get_user(uid)
    name = user['name'] if user else 'عزيزي اللاعب'
    
    return {
        "type": "bubble",
        "size": "mega",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "🎮 Bot Mesh",
                    "size": "xxl",
                    "weight": "bold",
                    "color": colors["text"],
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": "بوت الألعاب الترفيهية",
                    "size": "sm",
                    "color": colors["text2"],
                    "align": "center",
                    "margin": "sm"
                }
            ],
            "backgroundColor": colors["bg"],
            "paddingAll": "20px"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": f"مرحباً {name} 👋",
                    "size": "lg",
                    "weight": "bold",
                    "color": colors["primary"],
                    "align": "center",
                    "margin": "md"
                },
                {
                    "type": "separator",
                    "margin": "lg"
                },
                {
                    "type": "text",
                    "text": "📚 الأوامر المتاحة:",
                    "size": "md",
                    "weight": "bold",
                    "color": colors["text"],
                    "margin": "lg"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "text", "text": "👥 انضم - التسجيل", "size": "sm", "color": colors["text2"], "margin": "md"},
                        {"type": "text", "text": "📊 إحصائيات - نقاطك", "size": "sm", "color": colors["text2"], "margin": "sm"},
                        {"type": "text", "text": "❓ مساعدة - الألعاب", "size": "sm", "color": colors["text2"], "margin": "sm"},
                        {"type": "text", "text": "🎨 ثيم - الألوان", "size": "sm", "color": colors["text2"], "margin": "sm"}
                    ],
                    "backgroundColor": colors["card"],
                    "cornerRadius": "15px",
                    "paddingAll": "15px",
                    "margin": "md"
                }
            ],
            "backgroundColor": colors["bg"],
            "paddingAll": "20px"
        }
    }

def create_help_flex(uid):
    """نافذة المساعدة مع الألعاب"""
    theme = get_theme(uid)
    colors = THEMES[theme]
    
    return {
        "type": "bubble",
        "size": "mega",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "🎮 Bot Mesh",
                    "size": "xxl",
                    "weight": "bold",
                    "color": colors["text"],
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": "بوت الألعاب الترفيهية",
                    "size": "sm",
                    "color": colors["text2"],
                    "align": "center",
                    "margin": "sm"
                }
            ],
            "backgroundColor": colors["bg"],
            "paddingAll": "20px"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                # صف الألعاب الأول
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        create_game_card("🧠", "ذكاء", colors),
                        create_game_card("🎨", "لون", colors),
                        create_game_card("abc", "ترتيب", colors)
                    ],
                    "spacing": "sm"
                },
                # صف الألعاب الثاني
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        create_game_card("🔢", "رياضيات", colors),
                        create_game_card("⚡", "أسرع", colors),
                        create_game_card("↔️", "ضد", colors)
                    ],
                    "spacing": "sm",
                    "margin": "sm"
                },
                # صف الألعاب الثالث
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        create_game_card("✏️", "تكوين", colors),
                        create_game_card("🎵", "أغنية", colors),
                        create_game_card("🎯", "لعبة", colors)
                    ],
                    "spacing": "sm",
                    "margin": "sm"
                },
                # صف الألعاب الرابع
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        create_game_card("🔗", "سلسلة", colors),
                        create_game_card("🤔", "خمن", colors),
                        create_game_card("💕", "توافق", colors)
                    ],
                    "spacing": "sm",
                    "margin": "sm"
                },
                {
                    "type": "separator",
                    "margin": "xl"
                },
                # الأزرار السفلية
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {"type": "text", "text": "نقاطي 📊", "size": "md", "weight": "bold", "color": colors["text"], "align": "center"}
                            ],
                            "backgroundColor": colors["card"],
                            "cornerRadius": "15px",
                            "paddingAll": "15px",
                            "flex": 1,
                            "action": {"type": "message", "text": "إحصائيات"}
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {"type": "text", "text": "صدارة 🏆", "size": "md", "weight": "bold", "color": colors["text"], "align": "center"}
                            ],
                            "backgroundColor": colors["card"],
                            "cornerRadius": "15px",
                            "paddingAll": "15px",
                            "flex": 1,
                            "margin": "sm",
                            "action": {"type": "message", "text": "صدارة"}
                        }
                    ],
                    "margin": "xl"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {"type": "text", "text": "إيقاف 🔴", "size": "md", "weight": "bold", "color": "#FFFFFF", "align": "center"}
                            ],
                            "backgroundColor": "#EF4444",
                            "cornerRadius": "15px",
                            "paddingAll": "15px",
                            "flex": 1,
                            "action": {"type": "message", "text": "إيقاف"}
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {"type": "text", "text": "انضم 👥", "size": "md", "weight": "bold", "color": "#FFFFFF", "align": "center"}
                            ],
                            "backgroundColor": colors["primary"],
                            "cornerRadius": "15px",
                            "paddingAll": "15px",
                            "flex": 1,
                            "margin": "sm",
                            "action": {"type": "message", "text": "انضم"}
                        }
                    ],
                    "margin": "sm"
                },
                {
                    "type": "text",
                    "text": "© 2025 Abeer Aldosari",
                    "size": "xs",
                    "color": colors["text2"],
                    "align": "center",
                    "margin": "xl"
                }
            ],
            "backgroundColor": colors["bg"],
            "paddingAll": "20px"
        }
    }

def create_game_card(icon, name, colors):
    """إنشاء بطاقة لعبة"""
    return {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "text",
                "text": icon,
                "size": "xxl",
                "align": "center"
            },
            {
                "type": "text",
                "text": name,
                "size": "sm",
                "weight": "bold",
                "color": colors["text"],
                "align": "center",
                "margin": "sm"
            }
        ],
        "backgroundColor": colors["card"],
        "cornerRadius": "15px",
        "paddingAll": "15px",
        "flex": 1,
        "action": {
            "type": "message",
            "text": name
        }
    }

def create_theme_selector_flex(uid):
    """نافذة اختيار الثيم"""
    current_theme = get_theme(uid)
    
    theme_buttons = []
    for theme_key, theme_data in THEMES.items():
        is_current = "✓ " if theme_key == current_theme else ""
        theme_buttons.append({
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [],
                    "backgroundColor": theme_data["primary"],
                    "width": "30px",
                    "height": "30px",
                    "cornerRadius": "15px"
                },
                {
                    "type": "text",
                    "text": f"{is_current}{theme_data['name']}",
                    "size": "md",
                    "weight": "bold",
                    "color": theme_data["text"],
                    "margin": "md",
                    "flex": 1
                }
            ],
            "backgroundColor": theme_data["card"],
            "cornerRadius": "15px",
            "paddingAll": "15px",
            "margin": "sm",
            "action": {
                "type": "message",
                "text": f"ثيم:{theme_key}"
            }
        })
    
    return {
        "type": "bubble",
        "size": "mega",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "🎨 اختر الثيم المفضل",
                    "size": "xl",
                    "weight": "bold",
                    "color": "#FFFFFF",
                    "align": "center"
                }
            ],
            "backgroundColor": THEMES[current_theme]["primary"],
            "paddingAll": "20px"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": theme_buttons,
            "backgroundColor": THEMES[current_theme]["bg"],
            "paddingAll": "20px"
        }
    }

# ==================== Routes ====================
@app.route('/')
def home():
    return jsonify({
        'name': 'Bot Mesh',
        'status': 'active',
        'version': '3.0.0',
        'games': list(GAMES.keys())
    })

@app.route('/health')
def health():
    return jsonify({
        'status': 'ok',
        'active_games': gm.get_active_games_count(),
        'registered_users': gm.get_users_count(),
        'total_games': len(GAMES)
    })

@app.route('/callback', methods=['POST'])
def callback():
    signature = request.headers.get('X-Line-Signature')
    if not signature:
        abort(400)
    
    body = request.get_data(as_text=True)
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        logger.error('❌ Invalid signature')
        abort(400)
    except Exception as e:
        logger.error(f'❌ Error handling webhook: {e}')
        abort(400)
    
    return 'OK'

# ==================== Event Handlers ====================
@handler.add(FollowEvent)
def on_follow(event):
    uid = event.source.user_id
    name = get_name(uid)
    db.add_or_update_user(uid, name)
    
    welcome_flex = create_welcome_flex(uid)
    send_flex_reply(event.reply_token, welcome_flex, 'مرحباً')
    
    logger.info(f'✅ New follower: {name} ({uid})')

@handler.add(MessageEvent, message=TextMessageContent)
def on_message(event):
    uid = event.source.user_id
    txt = event.message.text.strip()
    gid = getattr(event.source, 'group_id', uid)
    name = get_name(uid)
    
    db.add_or_update_user(uid, name)

    # بداية
    if txt in ['بداية', 'البداية', 'start', 'Start']:
        welcome_flex = create_welcome_flex(uid)
        send_flex_reply(event.reply_token, welcome_flex, 'مرحباً')
        return

    # مساعدة
    if txt in ['مساعدة', 'help', 'Help', '؟', 'الالعاب']:
        help_flex = create_help_flex(uid)
        send_flex_reply(event.reply_token, help_flex, 'المساعدة')
        return

    # ثيم
    if txt in ['ثيم', 'theme', 'Theme', 'الوان', 'ألوان']:
        theme_flex = create_theme_selector_flex(uid)
        send_flex_reply(event.reply_token, theme_flex, 'الثيمات')
        return

    # تغيير الثيم
    if txt.startswith('ثيم:'):
        theme_key = txt.split(':')[1]
        if theme_key in THEMES:
            db.update_user_theme(uid, theme_key)
            send_text_reply(event.reply_token, f"✅ تم تغيير الثيم إلى {THEMES[theme_key]['name']}")
        return

    # انضم
    if txt in ['انضم', 'join']:
        gm.register(uid)
        welcome_flex = create_welcome_flex(uid)
        send_flex_reply(event.reply_token, welcome_flex, 'مرحباً')
        logger.info(f'✅ User registered: {name}')
        return

    # انسحب
    if txt in ['انسحب', 'leave']:
        gm.unregister(uid)
        send_text_reply(event.reply_token, '🚪 تم الانسحاب، لن تُحسب إجاباتك')
        logger.info(f'ℹ️ User unregistered: {name}')
        return

    # إحصائيات
    if txt in ['إحصائيات', 'احصائيات', 'stats', 'نقاطي']:
        user = db.get_user(uid)
        if not user:
            send_text_reply(event.reply_token, "لم تلعب أي ألعاب بعد!")
            return
        
        win_rate = (user['wins'] / user['games'] * 100) if user['games'] > 0 else 0
        stats = f"""
📊 إحصائياتك:
━━━━━━━━━━━━━━
👤 الاسم: {user['name']}
⭐ النقاط: {user['points']}
🎮 الألعاب: {user['games']}
🏆 الفوز: {user['wins']}
📈 نسبة الفوز: {win_rate:.1f}%
📅 انضممت: {user['joined_at'][:10]}
━━━━━━━━━━━━━━
        """.strip()
        send_text_reply(event.reply_token, stats)
        return

    # إيقاف
    if txt in ['إيقاف', 'ايقاف', 'stop']:
        if gm.get_game(gid):
            gm.end_game(gid)
            send_text_reply(event.reply_token, '✅ تم إيقاف اللعبة')
            logger.info(f'ℹ️ Game stopped in {gid}')
        else:
            send_text_reply(event.reply_token, '❌ لا توجد لعبة نشطة')
        return

    # بدء لعبة
    if txt in GAMES:
        if not gm.is_registered(uid):
            send_text_reply(event.reply_token, '❌ اكتب "انضم" أولاً للتسجيل')
            return

        if gm.get_game(gid):
            send_text_reply(event.reply_token, '⚠️ يوجد لعبة نشطة بالفعل\nاكتب "إيقاف" لإنهائها')
            return

        try:
            with ApiClient(configuration) as api_client:
                line_api = MessagingApi(api_client)
                game_class = GAMES[txt]
                game = game_class(line_api)
                game.set_theme(get_theme(uid))
                gm.start_game(gid, game, txt)
                response = game.start_game()
                
                if hasattr(response, 'altText'):
                    line_api.reply_message(
                        ReplyMessageRequest(
                            replyToken=event.reply_token,
                            messages=[response]
                        )
                    )
                else:
                    send_flex_reply(event.reply_token, response, f'لعبة {txt}')
                
                logger.info(f'✅ Game started: {txt} in {gid} by {name}')
        except Exception as e:
            logger.error(f'❌ Error starting game {txt}: {e}', exc_info=True)
            send_text_reply(event.reply_token, '❌ حدث خطأ أثناء بدء اللعبة')
        return

    # الرد على اللعبة
    game_data = gm.get_game(gid)
    if game_data and gm.is_registered(uid):
        game = game_data['game']
        
        if gm.has_answered(gid, uid):
            return
        
        try:
            result = game.check_answer(txt, uid, name)
            if result:
                gm.mark_answered(gid, uid)
                points = result.get('points', 0)
                won = result.get('won', False)
                db.update_points(uid, points, won)
                response = result.get('response')
                
                if response:
                    if hasattr(response, 'altText'):
                        with ApiClient(configuration) as api_client:
                            line_api = MessagingApi(api_client)
                            line_api.reply_message(
                                ReplyMessageRequest(
                                    replyToken=event.reply_token,
                                    messages=[response]
                                )
                            )
                    else:
                        send_flex_reply(event.reply_token, response, 'نتيجة')
                    logger.info(f'✅ Answer from {name}: {"✓" if won else "✗"} (+{points} points)')
                
                if result.get('game_over'):
                    gm.end_game(gid)
                    
        except Exception as e:
            logger.error(f'❌ Error checking answer: {e}', exc_info=True)
        return

# ==================== Run ====================
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    logger.info("🚀 Bot Mesh v3.0.0 - Running on port %s", port)
    logger.info(f"📊 Loaded {len(GAMES)} games: {', '.join(GAMES.keys())}")
    app.run(host='0.0.0.0', port=port, debug=False)
