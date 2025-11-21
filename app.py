"""
app.py - LINE Games Bot - Modern Neumorphism Design
بوت ألعاب احترافي بتصميم عصري
"""

from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage
import logging
from config import Config
from database import Database
from flex_messages import FlexDesign
from games import LettersGame, FastGame, ScrambleGame, ChainGame, IQGame

# إعداد السجلات
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

# إعدادات LINE Bot
line_bot_api = LineBotApi(Config.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(Config.LINE_CHANNEL_SECRET)

# قاعدة البيانات
db = Database()

# تخزين البيانات
active_games = {}
registered_players = set()

# ربط الألعاب بمعرفاتها
GAME_CLASSES = {
    'letters': LettersGame,
    'fast': FastGame,
    'scramble': ScrambleGame,
    'chain': ChainGame,
    'iq': IQGame
}

@app.route("/", methods=['GET'])
def home():
    """الصفحة الرئيسية"""
    return """
    <html>
        <head>
            <title>LINE Games Bot 🎮</title>
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body {
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white; min-height: 100vh;
                    display: flex; align-items: center; justify-content: center;
                }
                .card {
                    background: rgba(255, 255, 255, 0.1);
                    backdrop-filter: blur(10px); border-radius: 30px;
                    padding: 60px 40px; max-width: 600px; text-align: center;
                    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
                }
                h1 { font-size: 4em; margin-bottom: 10px; }
                h2 { font-size: 2em; margin-bottom: 10px; }
                p { font-size: 1.2em; opacity: 0.9; margin-bottom: 30px; }
                .stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-top: 30px; }
                .stat { background: rgba(255, 255, 255, 0.2); padding: 20px; border-radius: 20px; }
                .stat-value { font-size: 2.5em; font-weight: bold; margin-bottom: 5px; }
                .stat-label { font-size: 0.9em; opacity: 0.8; }
            </style>
        </head>
        <body>
            <div class="card">
                <h1>🎮</h1>
                <h2>LINE Games Bot</h2>
                <p>بوت ألعاب احترافي بتصميم Neumorphism</p>
                <div class="stats">
                    <div class="stat"><div class="stat-value">5</div><div class="stat-label">ألعاب</div></div>
                    <div class="stat"><div class="stat-value">✓</div><div class="stat-label">يعمل</div></div>
                    <div class="stat"><div class="stat-value">⚡</div><div class="stat-label">سريع</div></div>
                </div>
            </div>
        </body>
    </html>
    """

@app.route("/callback", methods=['POST'])
def callback():
    """معالج webhook"""
    signature = request.headers.get('X-Line-Signature', '')
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    """معالج الرسائل"""
    user_id = event.source.user_id
    text = event.message.text.strip()
    game_id = event.source.group_id if hasattr(event.source, 'group_id') and event.source.group_id else user_id
    
    # الحصول على اسم المستخدم
    try:
        profile = line_bot_api.get_profile(user_id)
        display_name = profile.display_name
    except:
        display_name = "مستخدم"
    
    # الأوامر الأساسية
    if text in ['البداية', 'start', 'ابدأ', 'القائمة', 'menu']:
        flex = FlexDesign.main_menu()
        line_bot_api.reply_message(event.reply_token, FlexSendMessage(alt_text="القائمة الرئيسية", contents=flex))
        return
    
    # الانضمام
    if text in ['انضم', 'join']:
        registered_players.add(user_id)
        line_bot_api.reply_message(event.reply_token,
            TextSendMessage(text=f"✅ مرحباً بك {display_name}!\n\nتم تسجيلك بنجاح\nيمكنك الآن اللعب في جميع الألعاب"))
        return
    
    # الصدارة
    if text in ['الصدارة', 'leaderboard']:
        leaders = db.get_leaderboard()
        if leaders:
            flex = FlexDesign.leaderboard(leaders)
            line_bot_api.reply_message(event.reply_token, FlexSendMessage(alt_text="لوحة الصدارة", contents=flex))
        else:
            line_bot_api.reply_message(event.reply_token,
                TextSendMessage(text="لا توجد بيانات بعد\nابدأ اللعب لتظهر على اللوحة!"))
        return
    
    # بدء الألعاب
    if text in GAME_CLASSES:
        game_class = GAME_CLASSES[text]
        game = game_class()
        active_games[game_id] = {'game': game, 'type': text}
        flex = game.start()
        line_bot_api.reply_message(event.reply_token, FlexSendMessage(alt_text=game.name, contents=flex))
        return
    
    # طلب تلميح
    if text == 'تلميح' and game_id in active_games:
        game = active_games[game_id]['game']
        hint = game.get_hint()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f"💡 تلميح: {hint}"))
        return
    
    # طلب الحل
    if text == 'الحل' and game_id in active_games:
        game = active_games[game_id]['game']
        solution = game.get_solution()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f"📝 الحل: {solution}"))
        del active_games[game_id]
        return
    
    # معالجة الإجابات
    if game_id in active_games:
        game_data = active_games[game_id]
        game = game_data['game']
        is_correct, points = game.check_answer(text)
        
        if is_correct:
            db.update_user_score(user_id, display_name, points)
            flex = FlexDesign.correct_answer(display_name, points)
            
            # التحقق من انتهاء اللعبة
            if game.is_finished():
                del active_games[game_id]
            else:
                game.next_round()
            
            line_bot_api.reply_message(event.reply_token, FlexSendMessage(alt_text="إجابة صحيحة", contents=flex))
        return

if __name__ == "__main__":
    port = Config.PORT
    logger.info(f"🚀 بدء الخادم على المنفذ {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
