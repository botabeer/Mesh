"""
Bot Mesh - Professional 3D Design with Permanent Buttons
Created by: Abeer Aldosari © 2025
"""
import os
import logging
from flask import Flask, request, abort, jsonify

from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi,
    ReplyMessageRequest, TextMessage, FlexMessage, FlexContainer,
    QuickReply, QuickReplyItem, MessageAction
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent, FollowEvent

from config import LINE_TOKEN, LINE_SECRET, DB_PATH, THEMES
from database import DB
from game_manager import GameManager
from games import *

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
configuration = Configuration(access_token=LINE_TOKEN)
handler = WebhookHandler(LINE_SECRET)

db = DB(DB_PATH)
gm = GameManager()

GAMES = {
    'ذكاء': IqGame, 'لون': WordColorGame, 'ترتيب': ScrambleWordGame,
    'رياضيات': MathGame, 'أسرع': FastTypingGame, 'ضد': OppositeGame,
    'تكوين': LettersWordsGame, 'أغنية': SongGame, 'لعبة': HumanAnimalPlantGame,
    'سلسلة': ChainWordsGame, 'خمن': GuessGame, 'توافق': CompatibilityGame
}

def get_name(uid):
    try:
        with ApiClient(configuration) as api_client:
            return MessagingApi(api_client).get_profile(uid).display_name
    except: return 'لاعب'

def get_theme(uid):
    user = db.get_user(uid)
    return user.get('theme', 'white') if user else 'white'

def create_permanent_buttons():
    """أزرار ثابتة دائمة - الألعاب فقط"""
    games_list = list(GAMES.keys())
    items = []
    
    # الألعاب الـ 12
    for game in games_list:
        items.append(QuickReplyItem(action=MessageAction(label=game, text=game)))
    
    # أزرار التحكم
    items.append(QuickReplyItem(action=MessageAction(label="إيقاف", text="إيقاف")))
    
    return QuickReply(items=items)

def send_flex_with_buttons(reply_token, flex_content, alt_text='رسالة'):
    """إرسال Flex مع الأزرار الثابتة"""
    try:
        with ApiClient(configuration) as api_client:
            line_api = MessagingApi(api_client)
            
            messages = [
                FlexMessage(altText=alt_text, contents=FlexContainer.from_dict(flex_content)),
                TextMessage(text="اختر لعبة", quickReply=create_permanent_buttons())
            ]
            
            line_api.reply_message(ReplyMessageRequest(replyToken=reply_token, messages=messages))
            return True
    except Exception as e:
        logger.error(f'Error: {e}')
    return False

def send_text_with_buttons(reply_token, text):
    """إرسال نص مع الأزرار الثابتة"""
    try:
        with ApiClient(configuration) as api_client:
            line_api = MessagingApi(api_client)
            line_api.reply_message(ReplyMessageRequest(
                replyToken=reply_token,
                messages=[TextMessage(text=text, quickReply=create_permanent_buttons())]
            ))
            return True
    except Exception as e:
        logger.error(f'Error: {e}')
    return False

def create_welcome_3d(uid):
    """نافذة ترحيب 3D احترافية"""
    colors = THEMES[get_theme(uid)]
    user = db.get_user(uid)
    name = user['name'] if user else 'لاعب'
    
    return {
        "type": "bubble",
        "size": "giga",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": "Bot Mesh", "size": "xxl", "weight": "bold", "color": "#FFFFFF", "align": "center"},
                {"type": "text", "text": "بوت الألعاب الترفيهية", "size": "sm", "color": "#FFFFFF", "align": "center", "margin": "sm"}
            ],
            "backgroundColor": colors["primary"],
            "paddingAll": "25px"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": f"مرحباً {name}", "size": "xl", "weight": "bold", "color": colors["primary"], "align": "center"},
                {"type": "separator", "margin": "lg"},
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "text", "text": "الأوامر المتاحة:", "size": "lg", "weight": "bold", "color": colors["text"], "margin": "lg"},
                        {"type": "text", "text": "• انضم - التسجيل", "size": "sm", "color": colors["text2"], "margin": "md"},
                        {"type": "text", "text": "• مساعدة - الألعاب", "size": "sm", "color": colors["text2"], "margin": "sm"},
                        {"type": "text", "text": "• ثيم - الألوان", "size": "sm", "color": colors["text2"], "margin": "sm"},
                        {"type": "text", "text": "• إحصائيات - النقاط", "size": "sm", "color": colors["text2"], "margin": "sm"}
                    ],
                    "backgroundColor": colors["card"],
                    "cornerRadius": "20px",
                    "paddingAll": "20px",
                    "margin": "lg"
                }
            ],
            "backgroundColor": colors["bg"],
            "paddingAll": "20px"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "button",
                    "action": {"type": "message", "label": "عرض الألعاب", "text": "مساعدة"},
                    "style": "primary",
                    "color": colors["primary"],
                    "height": "md"
                }
            ],
            "backgroundColor": colors["bg"],
            "paddingAll": "15px"
        }
    }

def create_games_3d(uid):
    """قائمة الألعاب 3D"""
    colors = THEMES[get_theme(uid)]
    
    game_cards = []
    games_data = [
        ("ذكاء", "أسئلة ذكاء"), ("لون", "كلمة ولون"), ("ترتيب", "ترتيب حروف"),
        ("رياضيات", "حسابات"), ("أسرع", "كتابة سريعة"), ("ضد", "عكس الكلمة"),
        ("تكوين", "كلمات"), ("أغنية", "تخمين مغني"), ("لعبة", "إنسان حيوان"),
        ("سلسلة", "سلسلة كلمات"), ("خمن", "تخمين"), ("توافق", "التوافق")
    ]
    
    for i in range(0, len(games_data), 3):
        row_games = games_data[i:i+3]
        row = {
            "type": "box",
            "layout": "horizontal",
            "contents": [],
            "spacing": "sm",
            "margin": "sm" if i > 0 else "none"
        }
        
        for game_name, game_desc in row_games:
            row["contents"].append({
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": game_name, "size": "md", "weight": "bold", "color": colors["text"], "align": "center"},
                    {"type": "text", "text": game_desc, "size": "xs", "color": colors["text2"], "align": "center", "margin": "sm"}
                ],
                "backgroundColor": colors["card"],
                "cornerRadius": "15px",
                "paddingAll": "15px",
                "flex": 1,
                "action": {"type": "message", "text": game_name}
            })
        
        game_cards.append(row)
    
    return {
        "type": "bubble",
        "size": "giga",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": "الألعاب المتاحة", "size": "xl", "weight": "bold", "color": "#FFFFFF", "align": "center"}
            ],
            "backgroundColor": colors["primary"],
            "paddingAll": "20px"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": game_cards + [
                {"type": "separator", "margin": "xl"},
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [{"type": "text", "text": "نقاطي", "size": "md", "weight": "bold", "color": colors["text"], "align": "center"}],
                            "backgroundColor": colors["card"],
                            "cornerRadius": "15px",
                            "paddingAll": "15px",
                            "flex": 1,
                            "action": {"type": "message", "text": "إحصائيات"}
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [{"type": "text", "text": "إيقاف", "size": "md", "weight": "bold", "color": "#FFFFFF", "align": "center"}],
                            "backgroundColor": "#EF4444",
                            "cornerRadius": "15px",
                            "paddingAll": "15px",
                            "flex": 1,
                            "margin": "sm",
                            "action": {"type": "message", "text": "إيقاف"}
                        }
                    ],
                    "margin": "lg"
                }
            ],
            "backgroundColor": colors["bg"],
            "paddingAll": "20px"
        }
    }

def create_theme_selector_3d(uid):
    """اختيار الثيم 3D"""
    current = get_theme(uid)
    
    buttons = []
    for key, data in THEMES.items():
        check = "✓ " if key == current else ""
        buttons.append({
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [],
                    "backgroundColor": data["primary"],
                    "width": "40px",
                    "height": "40px",
                    "cornerRadius": "20px"
                },
                {"type": "text", "text": f"{check}{data['name']}", "size": "md", "weight": "bold", "color": data["text"], "margin": "md", "flex": 1}
            ],
            "backgroundColor": data["card"],
            "cornerRadius": "15px",
            "paddingAll": "15px",
            "margin": "sm",
            "action": {"type": "message", "text": f"ثيم:{key}"}
        })
    
    return {
        "type": "bubble",
        "size": "giga",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [{"type": "text", "text": "اختر الثيم", "size": "xl", "weight": "bold", "color": "#FFFFFF", "align": "center"}],
            "backgroundColor": THEMES[current]["primary"],
            "paddingAll": "20px"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": buttons,
            "backgroundColor": THEMES[current]["bg"],
            "paddingAll": "20px"
        }
    }

@app.route('/')
def home():
    return jsonify({'name': 'Bot Mesh', 'status': 'active', 'version': '3.0', 'games': len(GAMES)})

@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'games': gm.get_active_games_count(), 'users': gm.get_users_count()})

@app.route('/callback', methods=['POST'])
def callback():
    signature = request.headers.get('X-Line-Signature')
    if not signature: abort(400)
    
    body = request.get_data(as_text=True)
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    except Exception as e:
        logger.error(f'Error: {e}')
        abort(400)
    
    return 'OK'

@handler.add(FollowEvent)
def on_follow(event):
    uid = event.source.user_id
    name = get_name(uid)
    db.add_or_update_user(uid, name)
    send_flex_with_buttons(event.reply_token, create_welcome_3d(uid), 'مرحباً')
    logger.info(f'New follower: {name}')

@handler.add(MessageEvent, message=TextMessageContent)
def on_message(event):
    uid = event.source.user_id
    txt = event.message.text.strip()
    gid = getattr(event.source, 'group_id', uid)
    name = get_name(uid)
    
    db.add_or_update_user(uid, name)

    # الأوامر الأساسية
    if txt in ['بداية', 'start']:
        send_flex_with_buttons(event.reply_token, create_welcome_3d(uid), 'مرحباً')
        return
    
    if txt in ['مساعدة', 'help', 'الالعاب']:
        send_flex_with_buttons(event.reply_token, create_games_3d(uid), 'الألعاب')
        return
    
    if txt in ['ثيم', 'theme']:
        send_flex_with_buttons(event.reply_token, create_theme_selector_3d(uid), 'الثيمات')
        return
    
    if txt.startswith('ثيم:'):
        theme_key = txt.split(':')[1]
        if theme_key in THEMES:
            db.update_user_theme(uid, theme_key)
            send_text_with_buttons(event.reply_token, f"تم تغيير الثيم إلى {THEMES[theme_key]['name']}")
        return
    
    if txt in ['انضم', 'join']:
        gm.register(uid)
        send_flex_with_buttons(event.reply_token, create_welcome_3d(uid), 'مرحباً')
        logger.info(f'User registered: {name}')
        return
    
    if txt in ['انسحب', 'leave']:
        gm.unregister(uid)
        send_text_with_buttons(event.reply_token, 'تم الانسحاب')
        return
    
    if txt in ['إحصائيات', 'stats']:
        user = db.get_user(uid)
        if not user:
            send_text_with_buttons(event.reply_token, "لم تلعب أي ألعاب بعد")
            return
        
        win_rate = (user['wins'] / user['games'] * 100) if user['games'] > 0 else 0
        stats = f"""إحصائياتك:
━━━━━━━━━
الاسم: {user['name']}
النقاط: {user['points']}
الألعاب: {user['games']}
الفوز: {user['wins']}
نسبة الفوز: {win_rate:.1f}%
انضممت: {user['joined_at'][:10]}"""
        send_text_with_buttons(event.reply_token, stats)
        return
    
    if txt in ['إيقاف', 'stop']:
        if gm.get_game(gid):
            gm.end_game(gid)
            send_text_with_buttons(event.reply_token, 'تم إيقاف اللعبة')
        else:
            send_text_with_buttons(event.reply_token, 'لا توجد لعبة نشطة')
        return
    
    # بدء لعبة
    if txt in GAMES:
        if not gm.is_registered(uid):
            send_text_with_buttons(event.reply_token, 'اكتب "انضم" أولاً')
            return
        
        if gm.get_game(gid):
            send_text_with_buttons(event.reply_token, 'يوجد لعبة نشطة\nاكتب "إيقاف" لإنهائها')
            return
        
        try:
            with ApiClient(configuration) as api_client:
                line_api = MessagingApi(api_client)
                game = GAMES[txt](line_api)
                game.set_theme(get_theme(uid))
                gm.start_game(gid, game, txt)
                response = game.start_game()
                
                if hasattr(response, 'altText'):
                    line_api.reply_message(ReplyMessageRequest(replyToken=event.reply_token, messages=[response, TextMessage(text="اختر لعبة", quickReply=create_permanent_buttons())]))
                else:
                    send_flex_with_buttons(event.reply_token, response, txt)
                
                logger.info(f'Game started: {txt} by {name}')
        except Exception as e:
            logger.error(f'Error starting game: {e}')
            send_text_with_buttons(event.reply_token, 'حدث خطأ')
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
                            line_api.reply_message(ReplyMessageRequest(replyToken=event.reply_token, messages=[response, TextMessage(text="اختر لعبة", quickReply=create_permanent_buttons())]))
                    else:
                        send_flex_with_buttons(event.reply_token, response, 'نتيجة')
                
                if result.get('game_over'):
                    gm.end_game(gid)
        except Exception as e:
            logger.error(f'Error: {e}')

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    logger.info(f"Bot Mesh v3.0 - Port {port}")
    logger.info(f"Loaded {len(GAMES)} games")
    app.run(host='0.0.0.0', port=port, debug=False)
