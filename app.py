"""
Bot Mesh - Main Application (Clean & Organized)
Created by: Abeer Aldosari © 2025
"""
import os
import logging
from flask import Flask, request, abort, jsonify
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    FlexSendMessage, FollowEvent
)

# استيراد المكونات
from config import LINE_TOKEN, LINE_SECRET, DB_PATH, THEMES
from database import DB
from flex_builder import FlexBuilder
from game_manager import GameManager

# استيراد جميع الألعاب تلقائياً من مجلد games
from games import *

# ==================== الإعدادات ====================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ==================== Flask App ====================
app = Flask(__name__)
line_api = LineBotApi(LINE_TOKEN)
handler = WebhookHandler(LINE_SECRET)
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

# ==================== Helper Functions ====================
def get_name(uid):
    """الحصول على اسم المستخدم"""
    try:
        return line_api.get_profile(uid).display_name
    except:
        return 'لاعب'

def get_theme(uid):
    """الحصول على ثيم المستخدم"""
    user = db.get_user(uid)
    return user['theme'] if user else 'white'

# ==================== Routes ====================
@app.route('/')
def home():
    """الصفحة الرئيسية"""
    return f'''<!DOCTYPE html>
<html dir="rtl">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Bot Mesh</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }}
        .container {{
            background: #fff;
            border-radius: 25px;
            padding: 40px;
            text-align: center;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            max-width: 500px;
            width: 100%;
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
            border-radius: 15px;
            margin: 20px 0;
            font-weight: bold;
            font-size: 1.1em;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
            margin: 20px 0;
        }}
        .stat {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 15px;
        }}
        .stat-value {{
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }}
        .stat-label {{
            color: #6c757d;
            margin-top: 5px;
        }}
        footer {{
            margin-top: 20px;
            color: #6c757d;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🎮 Bot Mesh</h1>
        <p style="color: #6c757d; margin-bottom: 20px;">بوت الألعاب الترفيهية</p>
        
        <div class="status">✅ يعمل بنجاح</div>
        
        <div class="stats">
            <div class="stat">
                <div class="stat-value">{gm.get_users_count()}</div>
                <div class="stat-label">👥 لاعب نشط</div>
            </div>
            <div class="stat">
                <div class="stat-value">{len(GAMES)}</div>
                <div class="stat-label">🎯 لعبة متاحة</div>
            </div>
            <div class="stat">
                <div class="stat-value">{len(THEMES)}</div>
                <div class="stat-label">🎨 ثيم</div>
            </div>
            <div class="stat">
                <div class="stat-value">{gm.get_active_games_count()}</div>
                <div class="stat-label">🎮 لعبة نشطة</div>
            </div>
        </div>
        
        <footer>
            Created by Abeer Aldosari © 2025
        </footer>
    </div>
</body>
</html>'''

@app.route('/health')
def health():
    """فحص صحة النظام"""
    return jsonify({
        'status': 'ok',
        'users': gm.get_users_count(),
        'active_games': gm.get_active_games_count(),
        'total_games': len(GAMES),
        'themes': len(THEMES)
    })

@app.route('/callback', methods=['POST'])
def callback():
    """LINE Webhook"""
    signature = request.headers.get('X-Line-Signature')
    if not signature:
        abort(400)
    
    try:
        handler.handle(request.get_data(as_text=True), signature)
    except InvalidSignatureError:
        logger.error('Invalid signature')
        abort(400)
    
    return 'OK'

# ==================== LINE Event Handlers ====================
@handler.add(MessageEvent, message=TextMessage)
def on_message(event):
    """معالج الرسائل"""
    try:
        uid = event.source.user_id
        txt = event.message.text.strip()
        gid = getattr(event.source, 'group_id', uid)
        name = get_name(uid)
        theme = get_theme(uid)
        builder = FlexBuilder(theme)
        
        # الأوامر الأساسية
        if txt in ['@botmesh', 'بداية', 'مساعدة', 'start']:
            gm.register(uid)
            line_api.reply_message(
                event.reply_token,
                FlexSendMessage(alt_text='القائمة', contents=builder.welcome())
            )
            return
        
        # عرض النقاط
        elif txt == 'نقاطي':
            user = db.get_user(uid)
            if user:
                data = {
                    'points': user['points'],
                    'games': user['games'],
                    'wins': user['wins']
                }
                rank = db.rank(uid)
                line_api.reply_message(
                    event.reply_token,
                    FlexSendMessage(alt_text='نقاطي', contents=builder.stats(data, rank))
                )
            else:
                line_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text='❌ لم تلعب بعد\nاكتب "بداية" للبدء')
                )
            return
        
        # عرض الصدارة
        elif txt == 'الصدارة':
            leaders = db.leaderboard()
            line_api.reply_message(
                event.reply_token,
                FlexSendMessage(alt_text='الصدارة', contents=builder.leaderboard(leaders))
            )
            return
        
        # عرض الثيمات
        elif txt == 'ثيم':
            line_api.reply_message(
                event.reply_token,
                FlexSendMessage(alt_text='الثيمات', contents=builder.themes())
            )
            return
        
        # تغيير الثيم
        elif txt.startswith('ثيم:'):
            theme_name = txt.split(':')[1]
            if theme_name in THEMES:
                db.set_theme(uid, theme_name)
                line_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=f'✅ تم التغيير إلى {THEMES[theme_name]["name"]}')
                )
            else:
                line_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text='❌ ثيم غير موجود')
                )
            return
        
        # إيقاف اللعبة
        elif txt == 'إيقاف':
            if gm.get_game(gid):
                gm.end_game(gid)
                line_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text='⏹️ تم إيقاف اللعبة')
                )
            else:
                line_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text='⚠️ لا توجد لعبة نشطة')
                )
            return
        
        # بدء لعبة جديدة
        elif txt in GAMES:
            if not gm.is_registered(uid):
                line_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text='❌ اكتب "بداية" أولاً للتسجيل')
                )
                return
            
            if gm.get_game(gid):
                line_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text='⚠️ يوجد لعبة نشطة بالفعل\nاكتب "إيقاف" لإنهائها')
                )
                return
            
            # إنشاء اللعبة
            game_class = GAMES[txt]
            game = game_class(line_api)
            game.set_theme(theme)
            gm.start_game(gid, game, txt)
            
            # بدء اللعبة
            response = game.start_game()
            line_api.reply_message(event.reply_token, response)
            logger.info(f'🎮 بدأت لعبة {txt} للمستخدم {name}')
            return
        
        # التعامل مع إجابات اللعبة
        elif gm.get_game(gid) and gm.is_registered(uid):
            game_data = gm.get_game(gid)
            game = game_data['game']
            game_type = game_data['type']
            
            # فحص الإجابة
            result = game.check_answer(txt, uid, name)
            
            # التعامل مع نهاية اللعبة
            if result and result.get('game_over'):
                points = result.get('points', 0)
                won = result.get('won', False)
                
                # حفظ النتيجة
                db.update(uid, name, points, won, game_type)
                logger.info(f'✅ انتهت لعبة {game_type} - {name}: {points} نقطة')
                
                # إنهاء اللعبة
                gm.end_game(gid)
            
            # إرسال الرد
            response = result.get('response') if result else None
            if response:
                line_api.reply_message(event.reply_token, response)
            return
    
    except Exception as e:
        logger.error(f'❌ خطأ في on_message: {e}', exc_info=True)
        try:
            line_api.reply_message(
                event.reply_token,
                TextSendMessage(text='❌ حدث خطأ، حاول مرة أخرى')
            )
        except:
            pass

@handler.add(FollowEvent)
def on_follow(event):
    """عند إضافة البوت"""
    try:
        uid = event.source.user_id
        name = get_name(uid)
        gm.register(uid)
        
        builder = FlexBuilder('white')
        line_api.reply_message(
            event.reply_token,
            FlexSendMessage(alt_text='مرحباً', contents=builder.welcome())
        )
        logger.info(f'👋 مستخدم جديد: {name}')
    except Exception as e:
        logger.error(f'❌ خطأ في on_follow: {e}', exc_info=True)

# ==================== Run ====================
if __name__ == '__main__':
    logger.info('=' * 50)
    logger.info('🎮 Bot Mesh Started Successfully')
    logger.info(f'📊 Games Available: {len(GAMES)}')
    logger.info(f'🎨 Themes Available: {len(THEMES)}')
    logger.info(f'🗄️  Database: {DB_PATH}')
    logger.info('=' * 50)
    
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
