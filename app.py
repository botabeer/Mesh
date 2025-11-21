from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, FlexSendMessage
import os
from config import Config
from database import Database
from flex_messages import FlexMessages
from games import GameManager

app = Flask(__name__)

# إعداد LINE Bot
line_bot_api = LineBotApi(Config.LINE_ACCESS_TOKEN)
handler = WebhookHandler(Config.LINE_CHANNEL_SECRET)

# إعداد قاعدة البيانات
db = Database()

# إعداد مدير الألعاب
game_manager = GameManager(line_bot_api, db)

@app.route("/", methods=['GET'])
def home():
    """الصفحة الرئيسية"""
    return """
    <html>
        <head>
            <title>LINE Games Bot 🎮</title>
            <style>
                body {
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    text-align: center;
                    padding: 50px;
                    margin: 0;
                }
                .card {
                    background: rgba(255, 255, 255, 0.1);
                    backdrop-filter: blur(10px);
                    border-radius: 20px;
                    padding: 40px;
                    max-width: 600px;
                    margin: 0 auto;
                    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
                }
                h1 { font-size: 3em; margin: 0; }
                p { font-size: 1.2em; opacity: 0.9; }
                .stats {
                    display: grid;
                    grid-template-columns: repeat(3, 1fr);
                    gap: 20px;
                    margin-top: 30px;
                }
                .stat {
                    background: rgba(255, 255, 255, 0.2);
                    padding: 20px;
                    border-radius: 15px;
                }
                .stat-value {
                    font-size: 2em;
                    font-weight: bold;
                }
            </style>
        </head>
        <body>
            <div class="card">
                <h1>🎮</h1>
                <h2>LINE Games Bot</h2>
                <p>Bot Mesh</p>
                
                <div class="stats">
                    <div class="stat">
                        <div class="stat-value">5</div>
                        <div>ألعاب</div>
                    </div>
                    <div class="stat">
                        <div class="stat-value">✓</div>
                        <div>يعمل</div>
                    </div>
                    <div class="stat">
                        <div class="stat-value">⚡</div>
                        <div>سريع</div>
                    </div>
                </div>
            </div>
        </body>
    </html>
    """

@app.route("/callback", methods=['POST'])
def callback():
    """معالج webhook"""
    signature = request.headers['X-Line-Signature']
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
    
    # الأوامر الأساسية
    if text in ['البداية', 'start', 'مساعدة', 'القائمة']:
        flex = FlexMessages.main_menu()
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(alt_text="القائمة الرئيسية", contents=flex)
        )
        return
    
    # معالجة الألعاب
    game_manager.handle_message(event, user_id, text)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
