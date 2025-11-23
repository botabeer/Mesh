"""
Bot Mesh - Main Application (Complete with Themes)
Created by: Abeer Aldosari © 2025
"""
import os
import logging
from flask import Flask, request, abort, jsonify

# === LINE SDK v3 (FIXED IMPORTS) ===
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
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
    FollowEvent
)

# === Local imports ===
from config import LINE_TOKEN, LINE_SECRET, DB_PATH, THEMES
from database import DB
from game_manager import GameManager
from rich_menu_manager import RichMenuManager

# ==================== Logging ====================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ==================== Flask & LINE ====================
app = Flask(__name__)
configuration = Configuration(access_token=LINE_TOKEN)
handler = WebhookHandler(LINE_SECRET)

# Initialize managers
db = DB(DB_PATH)
gm = GameManager()
rich_menu_mgr = RichMenuManager(LINE_TOKEN)

# ==================== Games dictionary ====================
GAMES = {}

# محاولة تحميل الألعاب
try:
    from games.iq_game import IqGame
    from games.word_color_game import WordColorGame
    from games.scramble_word_game import ScrambleWordGame
    from games.math_game import MathGame
    from games.fast_typing_game import FastTypingGame
    from games.opposite_game import OppositeGame
    from games.letters_words_game import LettersWordsGame
    from games.song_game import SongGame
    from games.human_animal_plant_game import HumanAnimalPlantGame
    from games.chain_words_game import ChainWordsGame
    from games.guess_game import GuessGame
    from games.compatibility_game import CompatibilityGame
    
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
    logger.info(f"✅ Loaded {len(GAMES)} games")
except ImportError as e:
    logger.warning(f"⚠️ Could not load games: {e}")
    logger.info("ℹ️ Bot will run without games")

# ==================== Helper functions ====================
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

def create_game_button(icon, name, theme):
    """إنشاء زر لعبة"""
    return {
        "type": "button",
        "action": {
            "type": "message",
            "label": f"{icon} {name}",
            "text": name
        },
        "style": "secondary",
        "color": theme['card'],
        "height": "sm"
    }

# ==================== Flex Message Builders ====================
def create_welcome_flex(uid):
    """نافذة البداية مع الثيمات التسعة"""
    current_theme_key = get_theme(uid)
    theme = THEMES.get(current_theme_key, THEMES['white'])
    user = db.get_user(uid)
    name = user['name'] if user else 'لاعب'
    
    # تقسيم الثيمات إلى 3 صفوف × 3 أعمدة
    theme_rows = [
        ['white', 'black', 'gray'],
        ['blue', 'green', 'pink'],
        ['orange', 'purple', 'brown']
    ]
    
    theme_buttons = []
    for row in theme_rows:
        button_row = {
            "type": "box",
            "layout": "horizontal",
            "contents": [],
            "spacing": "sm",
            "margin": "sm"
        }
        for theme_key in row:
            t = THEMES[theme_key]
            is_current = theme_key == current_theme_key
            button_row["contents"].append({
                "type": "button",
                "action": {
                    "type": "message",
                    "label": f"{t['name']} {'✓' if is_current else ''}",
                    "text": f"ثيم:{theme_key}"
                },
                "style": "primary" if is_current else "secondary",
                "height": "sm",
                "flex": 1
            })
        theme_buttons.append(button_row)
    
    return {
        "type": "bubble",
        "size": "mega",
        "styles": {
            "body": {"backgroundColor": theme['bg']}
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                # Header
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "🎮 Bot Mesh",
                            "weight": "bold",
                            "size": "xxl",
                            "color": theme['primary'],
                            "align": "center"
                        },
                        {
                            "type": "text",
                            "text": "بوت الألعاب الترفيهية",
                            "size": "sm",
                            "color": theme['text2'],
                            "align": "center",
                            "margin": "sm"
                        }
                    ],
                    "backgroundColor": theme['card'],
                    "cornerRadius": "15px",
                    "paddingAll": "20px"
                },
                {
                    "type": "text",
                    "text": f"مرحباً {name}! 👋",
                    "size": "lg",
                    "color": theme['text'],
                    "align": "center",
                    "margin": "lg",
                    "weight": "bold"
                },
                {
                    "type": "separator",
                    "margin": "lg"
                },
                {
                    "type": "text",
                    "text": "🎨 اختر الثيم المفضل",
                    "size": "md",
                    "color": theme['text'],
                    "align": "center",
                    "margin": "lg",
                    "weight": "bold"
                }
            ] + theme_buttons + [
                {
                    "type": "separator",
                    "margin": "lg"
                },
                {
                    "type": "text",
                    "text": "💡 الأوامر المتاحة:",
                    "size": "sm",
                    "color": theme['text'],
                    "weight": "bold",
                    "margin": "lg"
                },
                {
                    "type": "text",
                    "text": "• مساعدة - عرض الألعاب\n• انضم - للتسجيل\n• نقاطي - إحصائياتك\n• صدارة - أفضل اللاعبين",
                    "size": "xs",
                    "color": theme['text2'],
                    "wrap": True,
                    "margin": "sm"
                },
                {
                    "type": "text",
                    "text": "© 2025 Abeer Aldosari",
                    "size": "xxs",
                    "color": theme['text2'],
                    "align": "center",
                    "margin": "lg"
                }
            ],
            "paddingAll": "20px"
        }
    }

def create_help_flex(uid):
    """نافذة المساعدة مع الألعاب والأزرار"""
    theme = THEMES.get(get_theme(uid), THEMES['white'])
    
    # 12 لعبة في 4 صفوف × 3 أعمدة
    games_grid = [
        [("🧠", "ذكاء"), ("🎨", "لون"), ("🔤", "ترتيب")],
        [("🔢", "رياضيات"), ("⚡", "أسرع"), ("↔️", "ضد")],
        [("✏️", "تكوين"), ("🎵", "أغنية"), ("🎯", "لعبة")],
        [("🔗", "سلسلة"), ("🤔", "خمن"), ("💕", "توافق")]
    ]
    
    game_buttons = []
    for row in games_grid:
        button_row = {
            "type": "box",
            "layout": "horizontal",
            "contents": [],
            "spacing": "sm",
            "margin": "sm"
        }
        for icon, name in row:
            button_row["contents"].append({
                "type": "button",
                "action": {
                    "type": "message",
                    "label": f"{icon} {name}",
                    "text": name
                },
                "style": "secondary",
                "color": theme['card'],
                "height": "sm",
                "flex": 1
            })
        game_buttons.append(button_row)
    
    return {
        "type": "bubble",
        "size": "mega",
        "styles": {
            "body": {"backgroundColor": theme['bg']}
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "🎮 قائمة الألعاب",
                    "weight": "bold",
                    "size": "xl",
                    "color": theme['primary'],
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": "اختر لعبة للبدء",
                    "size": "sm",
                    "color": theme['text2'],
                    "align": "center",
                    "margin": "sm"
                },
                {
                    "type": "separator",
                    "margin": "lg"
                }
            ] + game_buttons + [
                {
                    "type": "separator",
                    "margin": "lg"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "button",
                            "action": {
                                "type": "message",
                                "label": "📊 نقاطي",
                                "text": "نقاطي"
                            },
                            "style": "secondary",
                            "color": theme['card'],
                            "height": "sm"
                        },
                        {
                            "type": "button",
                            "action": {
                                "type": "message",
                                "label": "🏆 صدارة",
                                "text": "صدارة"
                            },
                            "style": "secondary",
                            "color": theme['card'],
                            "height": "sm"
                        }
                    ],
                    "spacing": "sm",
                    "margin": "md"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "button",
                            "action": {
                                "type": "message",
                                "label": "🚪 انسحب",
                                "text": "انسحب"
                            },
                            "style": "secondary",
                            "color": "#F59E0B",
                            "height": "sm"
                        },
                        {
                            "type": "button",
                            "action": {
                                "type": "message",
                                "label": "👥 انضم",
                                "text": "انضم"
                            },
                            "style": "primary",
                            "color": theme['primary'],
                            "height": "sm"
                        }
                    ],
                    "spacing": "sm",
                    "margin": "sm"
                }
            ],
            "paddingAll": "20px"
        }
    }

def create_leaderboard_flex(uid):
    """لوحة الصدارة"""
    theme = THEMES.get(get_theme(uid), THEMES['white'])
    leaders = db.get_leaderboard(10)
    
    contents = [
        {
            "type": "text",
            "text": "🏆 لوحة الصدارة",
            "weight": "bold",
            "size": "xl",
            "color": theme['primary'],
            "align": "center"
        },
        {
            "type": "separator",
            "margin": "lg"
        }
    ]
    
    if not leaders:
        contents.append({
            "type": "text",
            "text": "لا يوجد لاعبون بعد!",
            "size": "md",
            "color": theme['text2'],
            "align": "center",
            "margin": "lg"
        })
    else:
        medals = ["🥇", "🥈", "🥉"]
        for i, leader in enumerate(leaders):
            medal = medals[i] if i < 3 else f"{i+1}."
            contents.append({
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": f"{medal} {leader['name']}",
                        "size": "sm",
                        "color": theme['text'],
                        "flex": 3
                    },
                    {
                        "type": "text",
                        "text": f"{leader['points']} ⭐",
                        "size": "sm",
                        "color": theme['primary'],
                        "align": "end",
                        "flex": 1
                    }
                ],
                "margin": "md"
            })
    
    return {
        "type": "bubble",
        "styles": {
            "body": {"backgroundColor": theme['bg']}
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": contents,
            "paddingAll": "20px"
        }
    }

# ==================== Routes ====================
@app.route('/')
def home():
    return jsonify({
        'name': 'Bot Mesh',
        'status': 'active',
        'version': '3.2.0',
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
    send_flex_reply(event.reply_token, create_welcome_flex(uid), 'مرحباً')
    rich_menu_mgr.create_and_link_rich_menu(uid)
    logger.info(f'✅ New follower: {name} ({uid})')

@handler.add(MessageEvent, message=TextMessageContent)
def on_message(event):
    uid = event.source.user_id
    txt = event.message.text.strip()
    gid = getattr(event.source, 'group_id', uid)
    name = get_name(uid)

    # تحديث/إضافة المستخدم
    db.add_or_update_user(uid, name)

    # أوامر أساسية
    if txt.lower() in ['بداية', 'start']:
        send_flex_reply(event.reply_token, create_welcome_flex(uid), 'مرحباً')
        return

    if txt.lower() in ['مساعدة', 'help', 'الالعاب']:
        send_flex_reply(event.reply_token, create_help_flex(uid), 'المساعدة')
        return

    if txt.startswith('ثيم:'):
        theme_key = txt.split(':')[1]
        if theme_key in THEMES:
            db.update_user_theme(uid, theme_key)
            send_text_reply(event.reply_token, f"✅ تم تغيير الثيم إلى {THEMES[theme_key]['name']}")
        return

    # تسجيل المستخدم
    if txt.lower() in ['انضم', 'join']:
        gm.register(uid)
        send_text_reply(event.reply_token, '✅ تم التسجيل بنجاح! اكتب "مساعدة" لعرض الألعاب')
        logger.info(f'✅ User registered: {name}')
        return

    # الانسحاب
    if txt.lower() in ['انسحب', 'leave']:
        gm.unregister(uid)
        send_text_reply(event.reply_token, '🚪 تم الانسحاب، لن تُحسب إجاباتك')
        logger.info(f'ℹ️ User unregistered: {name}')
        return

    # إحصائيات / نقاطي
    if txt.lower() in ['إحصائيات', 'احصائيات', 'stats', 'نقاطي']:
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

    # لوحة الصدارة
    if txt.lower() in ['صدارة', 'leaderboard', 'top']:
        send_flex_reply(event.reply_token, create_leaderboard_flex(uid), 'لوحة الصدارة')
        return

    # إيقاف اللعبة
    if txt.lower() in ['إيقاف', 'ايقاف', 'stop']:
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
                if hasattr(response, 'alt_text'):
                    line_api.reply_message(
                        ReplyMessageRequest(replyToken=event.reply_token, messages=[response])
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
                    if hasattr(response, 'alt_text'):
                        with ApiClient(configuration) as api_client:
                            line_api = MessagingApi(api_client)
                            line_api.reply_message(
                                ReplyMessageRequest(replyToken=event.reply_token, messages=[response])
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
    logger.info(f"🚀 Bot Mesh v3.2.0 - Running on port {port}")
    logger.info(f"📊 Loaded {len(GAMES)} games: {', '.join(GAMES.keys())}")
    app.run(host='0.0.0.0', port=port, debug=False)
