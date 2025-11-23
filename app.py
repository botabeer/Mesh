import os, logging
from flask import Flask, request, abort, jsonify
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage, FollowEvent, QuickReply, QuickReplyButton, MessageAction
from linebot.exceptions import InvalidSignatureError

from config import LINE_TOKEN, LINE_SECRET, THEMES
from database import DB
from flex_builder import FlexBuilder
from game_manager import GameManager

from games import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
line_api = LineBotApi(LINE_TOKEN)
handler = WebhookHandler(LINE_SECRET)
db = DB(os.getenv('DB_PATH', 'data/game.db'))
gm = GameManager()

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

def get_name(uid):
    try: return line_api.get_profile(uid).display_name
    except: return 'لاعب'

def get_theme(uid):
    user = db.get_user(uid)
    return user['theme'] if user else 'white'

def get_games_quick_reply(uid):
    items=[]
    for label in GAMES.keys():
        items.append(QuickReplyButton(action=MessageAction(label=label, text=label)))
    items.append(QuickReplyButton(action=MessageAction(label='إيقاف', text='إيقاف')))
    return QuickReply(items=items)

def send_with_games_menu(reply_token, message, uid=None):
    if isinstance(message, TextSendMessage): message.quick_reply=get_games_quick_reply(uid); line_api.reply_message(reply_token, message)
    else: line_api.reply_message(reply_token, [message, TextSendMessage(text="اختر لعبة:", quick_reply=get_games_quick_reply(uid))])

@app.route('/')
def home(): return "Bot Mesh Active"
@app.route('/health')
def health(): return jsonify({'status':'ok', 'active_games':len(gm.active_games), 'registered_users':len(gm.registered_users)})

@app.route('/callback', methods=['POST'])
def callback():
    signature = request.headers.get('X-Line-Signature')
    if not signature: abort(400)
    try: handler.handle(request.get_data(as_text=True), signature)
    except InvalidSignatureError: abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def on_message(event):
    uid = event.source.user_id
    gid = getattr(event.source,'group_id',uid)
    txt = event.message.text.strip()
    if txt == 'انضم': gm.register(uid,get_name(uid)); send_with_games_menu(event.reply_token, TextSendMessage(text='✅ تم التسجيل'),uid=uid); return
    if txt == 'انسحب': gm.unregister(uid); send_with_games_menu(event.reply_token, TextSendMessage(text='✅ تم الانسحاب'),uid=uid); return
    if gm.should_ignore(uid): return  # تجاهل المستخدم
    game_data=gm.get_game(gid)
    if txt in GAMES:
        if gm.is_registered(uid):
            if game_data: send_with_games_menu(event.reply_token, TextSendMessage(text='⚠️ لعبة نشطة بالفعل'),uid=uid); return
            game_class=GAMES[txt]; game=game_class(line_api); game.set_theme('white'); gm.start_game(gid,game,txt)
            resp=game.start_game(); send_with_games_menu(event.reply_token, resp,uid=uid)
        else: send_with_games_menu(event.reply_token, TextSendMessage(text='❌ اكتب "انضم" أولاً'),uid=uid)
        return
    if game_data and gm.is_registered(uid):
        game=game_data['game']; if not gm.has_answered(gid,uid):
            result=game.check_answer(txt,uid,get_name(uid))
            if result: gm.mark_answered(gid,uid)
            send_with_games_menu(event.reply_token,result.get('response'),uid=uid)

@handler.add(FollowEvent)
def on_follow(event): uid=event.source.user_id; gm.register(uid,get_name(uid)); builder=FlexBuilder('white'); send_with_games_menu(event.reply_token,FlexSendMessage(alt_text='مرحباً',contents=builder.welcome()),uid=uid)

if __name__=='__main__':
    port=int(os.getenv('PORT',5000))
    app.run(host='0.0.0.0',port=port,debug=False)
