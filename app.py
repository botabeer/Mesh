"""
Bot Mesh - نظام مضغوط كامل
Created by: Abeer Aldosari © 2025
"""
import os, logging, asyncio, sqlite3, random, importlib
from datetime import datetime
from flask import Flask, request, abort, jsonify
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage, FollowEvent

# ==================== الإعدادات ====================
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class Config:
    LINE_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', '')
    LINE_SECRET = os.getenv('LINE_CHANNEL_SECRET', '')
    DB_PATH = os.getenv('DB_PATH', 'data/game.db')
    GEMINI_KEYS = [k for k in [os.getenv(f'GEMINI_API_KEY_{i}') for i in range(1,4)] if k]

# ==================== قاعدة البيانات ====================
class DB:
    def __init__(self, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.path = path
        self._init()
    
    def _init(self):
        c = sqlite3.connect(self.path)
        c.execute('''CREATE TABLE IF NOT EXISTS users (
            uid TEXT PRIMARY KEY, name TEXT, points INT DEFAULT 0, 
            games INT DEFAULT 0, wins INT DEFAULT 0, theme TEXT DEFAULT 'soft')''')
        c.execute('''CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY, uid TEXT, game TEXT, points INT, 
            won INT, time TEXT)''')
        c.commit()
        c.close()
    
    def get_user(self, uid):
        c = sqlite3.connect(self.path)
        c.row_factory = sqlite3.Row
        r = c.execute('SELECT * FROM users WHERE uid=?', (uid,)).fetchone()
        c.close()
        return dict(r) if r else None
    
    def update(self, uid, name, pts, won, game):
        c = sqlite3.connect(self.path)
        if c.execute('SELECT 1 FROM users WHERE uid=?', (uid,)).fetchone():
            c.execute('UPDATE users SET points=points+?, games=games+1, wins=wins+?, name=? WHERE uid=?',
                     (pts, 1 if won else 0, name, uid))
        else:
            c.execute('INSERT INTO users VALUES (?,?,?,1,?,?)', (uid, name, pts, 1 if won else 0, 'soft'))
        c.execute('INSERT INTO history VALUES (NULL,?,?,?,?,?)', 
                 (uid, game, pts, 1 if won else 0, datetime.now().isoformat()))
        c.commit()
        c.close()
    
    def leaderboard(self, limit=10):
        c = sqlite3.connect(self.path)
        c.row_factory = sqlite3.Row
        rs = c.execute('SELECT * FROM users ORDER BY points DESC LIMIT ?', (limit,)).fetchall()
        c.close()
        return [dict(r) for r in rs]
    
    def rank(self, uid):
        c = sqlite3.connect(self.path)
        r = c.execute('''SELECT COUNT(*)+1 FROM users WHERE points > 
            (SELECT COALESCE(points,0) FROM users WHERE uid=?)''', (uid,)).fetchone()
        c.close()
        return r[0] if r else 0
    
    def set_theme(self, uid, theme):
        c = sqlite3.connect(self.path)
        c.execute('UPDATE users SET theme=? WHERE uid=?', (theme, uid))
        c.commit()
        c.close()

# ==================== نظام الثيمات والتصميم ====================
THEMES = {
    'soft': {'bg':'#E0E5EC', 'card':'#E0E5EC', 'primary':'#6C8EEF', 'text':'#2C3E50', 'text2':'#718096', 'name':'🎨 ناعم'},
    'dark': {'bg':'#2C3E50', 'card':'#34495E', 'primary':'#00D9FF', 'text':'#ECF0F1', 'text2':'#BDC3C7', 'name':'🌙 داكن'},
    'ocean': {'bg':'#D4E4F0', 'card':'#D4E4F0', 'primary':'#0EA5E9', 'text':'#0C4A6E', 'text2':'#475569', 'name':'🌊 محيطي'},
    'sunset': {'bg':'#FFE8D6', 'card':'#FFE8D6', 'primary':'#F97316', 'text':'#7C2D12', 'text2':'#92400E', 'name':'🌅 غروب'},
    'forest': {'bg':'#D4E4D4', 'card':'#D4E4D4', 'primary':'#10B981', 'text':'#064E3B', 'text2':'#047857', 'name':'🌲 طبيعي'}
}

class FlexBuilder:
    def __init__(self, theme='soft'):
        self.t = THEMES.get(theme, THEMES['soft'])
    
    def _btn(self, emoji, txt, cmd):
        return {"type":"box", "layout":"vertical", "action":{"type":"message", "text":cmd},
                "contents":[{"type":"text", "text":emoji, "size":"xl", "align":"center", "color":self.t['primary']},
                           {"type":"text", "text":txt, "size":"sm", "align":"center", "weight":"bold", "margin":"sm"}],
                "backgroundColor":self.t['card'], "cornerRadius":"15px", "paddingAll":"md", "flex":1}
    
    def _card(self, contents):
        return {"type":"box", "layout":"vertical", "contents":contents, "backgroundColor":self.t['card'],
                "cornerRadius":"20px", "paddingAll":"lg", "margin":"lg"}
    
    def welcome(self):
        games = [
            ['🧠','ذكاء','ذكاء'], ['🎨','لون','لون'], ['🔤','ترتيب','ترتيب'],
            ['✏️','تكوين','تكوين'], ['⛓️','سلسلة','سلسلة'], ['⚡','أسرع','أسرع'],
            ['🎯','لعبة','لعبة'], ['🤔','خمن','خمن'], ['↔️','ضد','ضد'],
            ['💖','توافق','توافق'], ['🎵','أغنية','أغنية']
        ]
        rows = [{"type":"box", "layout":"horizontal", "spacing":"sm", "margin":"sm",
                "contents":[self._btn(*g) for g in games[i:i+3]]} for i in range(0, len(games), 3)]
        
        return {"type":"bubble", "size":"mega", "body":{"type":"box", "layout":"vertical",
            "backgroundColor":self.t['bg'], "paddingAll":"20px", "contents":[
                self._card([{"type":"text", "text":"🎮 Bot Mesh", "size":"xxl", "weight":"bold", 
                            "color":self.t['primary'], "align":"center"},
                           {"type":"text", "text":"بوت الألعاب الترفيهية", "size":"sm", 
                            "color":self.t['text2'], "align":"center"}]),
                *rows,
                {"type":"separator", "margin":"lg", "color":self.t['text2']+"30"},
                {"type":"box", "layout":"horizontal", "spacing":"sm", "margin":"lg", "contents":[
                    {"type":"button", "action":{"type":"message", "label":"🔑 انضم", "text":"انضم"},
                     "style":"primary", "color":self.t['primary'], "height":"sm"},
                    {"type":"button", "action":{"type":"message", "label":"👋 انسحب", "text":"انسحب"},
                     "style":"secondary", "height":"sm"}
                ]},
                {"type":"box", "layout":"horizontal", "spacing":"sm", "margin":"sm", "contents":[
                    {"type":"button", "action":{"type":"message", "label":"📊 نقاطي", "text":"نقاطي"},
                     "style":"secondary", "height":"sm"},
                    {"type":"button", "action":{"type":"message", "label":"🏆 صدارة", "text":"الصدارة"},
                     "style":"secondary", "height":"sm"}
                ]},
                {"type":"box", "layout":"horizontal", "spacing":"sm", "margin":"sm", "contents":[
                    {"type":"button", "action":{"type":"message", "label":"🎨 ثيم", "text":"ثيم"},
                     "style":"secondary", "height":"sm"},
                    {"type":"button", "action":{"type":"message", "label":"⏹️ إيقاف", "text":"إيقاف"},
                     "style":"secondary", "height":"sm"}
                ]}
            ]}}
    
    def stats(self, data, rank):
        pts, games, wins = data.get('points',0), data.get('games',0), data.get('wins',0)
        rate = (wins/games*100) if games>0 else 0
        lvl = '🌱مبتدئ' if pts<100 else '⭐متوسط' if pts<500 else '🔥محترف' if pts<1000 else '👑أسطوري'
        
        return {"type":"bubble", "size":"mega", "body":{"type":"box", "layout":"vertical",
            "backgroundColor":self.t['bg'], "paddingAll":"20px", "contents":[
                self._card([{"type":"text", "text":lvl, "size":"xl", "weight":"bold", "align":"center"},
                           {"type":"text", "text":f"المركز #{rank}" if rank else "غير مصنف",
                            "size":"sm", "color":self.t['text2'], "align":"center"}]),
                {"type":"box", "layout":"horizontal", "spacing":"md", "margin":"lg", "contents":[
                    self._stat('💰', str(pts), 'نقطة'), self._stat('🎮', str(games), 'لعبة')]},
                {"type":"box", "layout":"horizontal", "spacing":"md", "margin":"sm", "contents":[
                    self._stat('🏆', str(wins), 'فوز'), self._stat('📈', f"{rate:.0f}%", 'نسبة')]},
                {"type":"button", "action":{"type":"message", "label":"🎮 العب الآن", "text":"بداية"},
                 "style":"primary", "color":self.t['primary'], "height":"sm", "margin":"xl"}
            ]}}
    
    def _stat(self, emoji, val, lbl):
        return {"type":"box", "layout":"vertical", "flex":1, "backgroundColor":self.t['card'],
                "cornerRadius":"15px", "paddingAll":"md", "contents":[
                    {"type":"text", "text":emoji, "size":"xl", "align":"center"},
                    {"type":"text", "text":val, "size":"lg", "weight":"bold", "align":"center", "margin":"xs"},
                    {"type":"text", "text":lbl, "size":"xs", "color":self.t['text2'], "align":"center"}]}
    
    def leaderboard(self, leaders):
        medals = ['🥇','🥈','🥉']
        rows = []
        for i, u in enumerate(leaders[:10]):
            m = medals[i] if i<3 else f"#{i+1}"
            rows.append({"type":"box", "layout":"horizontal", "margin":"sm",
                "backgroundColor":self.t['card'] if i<3 else "transparent", "cornerRadius":"10px", "paddingAll":"sm",
                "contents":[
                    {"type":"text", "text":m, "size":"md", "flex":1},
                    {"type":"text", "text":u.get('name','لاعب'), "size":"md", "weight":"bold" if i<3 else "regular", "flex":3},
                    {"type":"text", "text":f"{u.get('points',0)}⭐", "size":"md", "color":self.t['primary'] if i<3 else self.t['text2'], "align":"end", "flex":2}
                ]})
        
        return {"type":"bubble", "size":"mega", "body":{"type":"box", "layout":"vertical",
            "backgroundColor":self.t['bg'], "paddingAll":"20px", "contents":[
                self._card([{"type":"text", "text":"🏆 لوحة الصدارة", "size":"xl", "weight":"bold", "align":"center"}]),
                *rows
            ]}}
    
    def themes(self):
        rows = [{"type":"box", "layout":"horizontal", "margin":"sm", "backgroundColor":self.t['card'],
                "cornerRadius":"15px", "paddingAll":"md", "action":{"type":"message", "text":f"ثيم:{k}"},
                "contents":[
                    {"type":"box", "layout":"vertical", "backgroundColor":THEMES[k]['primary'], 
                     "cornerRadius":"10px", "width":"40px", "height":"40px", "justifyContent":"center",
                     "contents":[{"type":"text", "text":THEMES[k]['name'][:2], "align":"center"}]},
                    {"type":"text", "text":THEMES[k]['name'], "size":"md", "weight":"bold", "margin":"md", "gravity":"center"}
                ]} for k in THEMES]
        
        return {"type":"bubble", "size":"mega", "body":{"type":"box", "layout":"vertical",
            "backgroundColor":self.t['bg'], "paddingAll":"20px", "contents":[
                self._card([{"type":"text", "text":"🎨 اختر الثيم", "size":"xl", "weight":"bold", "align":"center"}]),
                *rows
            ]}}

# ==================== إدارة الألعاب ====================
class GameManager:
    def __init__(self):
        self.users = set()
        self.games = {}
    
    def register(self, uid): self.users.add(uid)
    def unregister(self, uid): self.users.discard(uid)
    def is_registered(self, uid): return uid in self.users
    def start_game(self, gid, game, gtype): self.games[gid] = {'game': game, 'type': gtype}
    def get_game(self, gid): return self.games.get(gid)
    def end_game(self, gid): return self.games.pop(gid, None)

# ==================== اللعبة الأساسية ====================
class BaseGame:
    def __init__(self, line_api):
        self.api = line_api
        self.round = 0
        self.max_rounds = 5
        self.score = 0
        self.theme = 'soft'
    
    def set_theme(self, theme):
        self.theme = theme
    
    def get_builder(self):
        return FlexBuilder(self.theme)
    
    def start_game(self):
        self.round = 1
        return self.next_question()
    
    def next_question(self):
        return TextSendMessage(text="السؤال التالي...")
    
    def check_answer(self, txt, uid, name):
        return {'correct': False, 'points': 0, 'game_over': False}
    
    def game_over_msg(self, won):
        pts = self.score
        msg = f"{'🎉 فزت!' if won else '😊 انتهت اللعبة'}\n\n💰 النقاط: {pts}\n🎯 الجولات: {self.max_rounds}"
        return {'message': msg, 'points': pts, 'won': won, 'game_over': True,
                'response': TextSendMessage(text=msg)}

# ==================== الألعاب ====================
class IqGame(BaseGame):
    def __init__(self, line_api, **kwargs):
        super().__init__(line_api)
        self.questions = [
            {'q': 'ما هو الرقم التالي: 2, 4, 6, 8, __؟', 'a': ['10']},
            {'q': 'إذا كان 2+2=4، فكم 3+3؟', 'a': ['6']},
            {'q': 'كم عدد أيام الأسبوع؟', 'a': ['7', 'سبعة']},
            {'q': 'ما لون السماء؟', 'a': ['أزرق', 'ازرق']},
            {'q': 'كم عدد أصابع اليد؟', 'a': ['5', 'خمسة']}
        ]
        self.current_q = None
    
    def next_question(self):
        if self.round > self.max_rounds:
            return self.game_over_msg(self.score >= 30)
        self.current_q = random.choice(self.questions)
        return TextSendMessage(text=f"🧠 سؤال {self.round}/5\n\n{self.current_q['q']}")
    
    def check_answer(self, txt, uid, name):
        correct = any(ans in txt.lower() for ans in self.current_q['a'])
        pts = 10 if correct else 0
        self.score += pts
        self.round += 1
        
        if self.round > self.max_rounds:
            return self.game_over_msg(self.score >= 30)
        
        msg = f"{'✅ صحيح!' if correct else '❌ خطأ'} (+{pts})\n\n"
        return {'correct': correct, 'points': pts, 'game_over': False,
                'response': [TextSendMessage(text=msg), self.next_question()]}

class WordColorGame(BaseGame):
    def __init__(self, line_api, **kwargs):
        super().__init__(line_api)
        self.colors = ['أحمر', 'أزرق', 'أخضر', 'أصفر', 'أسود']
        self.current = None
    
    def next_question(self):
        if self.round > self.max_rounds:
            return self.game_over_msg(self.score >= 30)
        word = random.choice(self.colors)
        color = random.choice(self.colors)
        self.current = color
        return TextSendMessage(text=f"🎨 سؤال {self.round}/5\n\nما لون الكلمة؟\n\n{word}")
    
    def check_answer(self, txt, uid, name):
        correct = self.current in txt
        pts = 10 if correct else 0
        self.score += pts
        self.round += 1
        
        if self.round > self.max_rounds:
            return self.game_over_msg(self.score >= 30)
        
        msg = f"{'✅ صحيح!' if correct else f'❌ خطأ! اللون: {self.current}'} (+{pts})\n\n"
        return {'correct': correct, 'points': pts, 'game_over': False,
                'response': [TextSendMessage(text=msg), self.next_question()]}

class ScrambleWordGame(BaseGame):
    def __init__(self, line_api, **kwargs):
        super().__init__(line_api)
        self.words = [
            {'word': 'كتاب', 'scrambled': 'بتاك'},
            {'word': 'مدرسة', 'scrambled': 'سدرمة'},
            {'word': 'سيارة', 'scrambled': 'يسارة'},
            {'word': 'حاسوب', 'scrambled': 'سوحاب'},
            {'word': 'طالب', 'scrambled': 'لباط'}
        ]
        self.current = None
    
    def next_question(self):
        if self.round > self.max_rounds:
            return self.game_over_msg(self.score >= 30)
        self.current = random.choice(self.words)
        return TextSendMessage(text=f"🔤 سؤال {self.round}/5\n\nرتب الحروف:\n{self.current['scrambled']}")
    
    def check_answer(self, txt, uid, name):
        correct = self.current['word'] in txt
        pts = 10 if correct else 0
        self.score += pts
        self.round += 1
        
        if self.round > self.max_rounds:
            return self.game_over_msg(self.score >= 30)
        
        msg = f"{'✅ صحيح!' if correct else f'❌ خطأ! الكلمة: {self.current["word"]}'} (+{pts})\n\n"
        return {'correct': correct, 'points': pts, 'game_over': False,
                'response': [TextSendMessage(text=msg), self.next_question()]}

# (يمكن إضافة باقي الألعاب بنفس الطريقة)

# ==================== Flask App ====================
app = Flask(__name__)
line_api = LineBotApi(Config.LINE_TOKEN)
handler = WebhookHandler(Config.LINE_SECRET)
db = DB(Config.DB_PATH)
gm = GameManager()

GAMES = {
    'ذكاء': IqGame,
    'لون': WordColorGame,
    'ترتيب': ScrambleWordGame,
}

def get_name(uid):
    try: return line_api.get_profile(uid).display_name
    except: return 'لاعب'

def get_theme(uid):
    u = db.get_user(uid)
    return u['theme'] if u else 'soft'

@app.route('/')
def home():
    return f'''<html dir="rtl"><head><meta charset="utf-8"><style>
body{{font-family:sans-serif;background:linear-gradient(135deg,#667eea,#764ba2);
min-height:100vh;display:flex;align-items:center;justify-content:center;margin:0}}
.c{{background:#fff;border-radius:25px;padding:40px;text-align:center;box-shadow:0 20px 60px rgba(0,0,0,0.3)}}
h1{{color:#667eea;margin:0 0 20px;font-size:2.5em}}
.s{{background:#d4edda;color:#155724;padding:20px;border-radius:15px;margin:20px 0;font-weight:bold}}
</style></head><body><div class="c">
<h1>🎮 Bot Mesh</h1>
<div class="s">✅ يعمل بنجاح</div>
<p>👥 {len(gm.users)} لاعب نشط</p>
<p>🎯 {len(GAMES)} لعبة</p>
<small>Created by Abeer Aldosari © 2025</small>
</div></body></html>'''

@app.route('/health')
def health():
    return jsonify({'status':'ok', 'users':len(gm.users), 'games':len(GAMES)})

@app.route('/callback', methods=['POST'])
def callback():
    sig = request.headers.get('X-Line-Signature')
    if not sig: abort(400)
    try: handler.handle(request.get_data(as_text=True), sig)
    except InvalidSignatureError: abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def on_message(event):
    try:
        uid = event.source.user_id
        txt = event.message.text.strip()
        gid = getattr(event.source, 'group_id', uid)
        name = get_name(uid)
        theme = get_theme(uid)
        builder = FlexBuilder(theme)
        
        # لا يرد إلا على الأوامر أو إذا كان في لعبة
        if txt in ['@botmesh', 'بداية', 'مساعدة']:
            gm.register(uid)
            line_api.reply_message(event.reply_token, FlexSendMessage(alt_text='القائمة', contents=builder.welcome()))
        
        elif txt == 'انضم':
            if not gm.is_registered(uid):
                gm.register(uid)
                line_api.reply_message(event.reply_token, FlexSendMessage(alt_text='مرحباً', contents=builder.welcome()))
            else:
                line_api.reply_message(event.reply_token, TextSendMessage(text='✅ أنت مسجل!'))
        
        elif txt == 'انسحب':
            gm.unregister(uid)
            line_api.reply_message(event.reply_token, FlexSendMessage(alt_text='وداعاً', contents=builder.welcome()))
        
        elif txt == 'نقاطي':
            u = db.get_user(uid)
            if u:
                data = {'points': u['points'], 'games': u['games'], 'wins': u['wins']}
                rank = db.rank(uid)
                line_api.reply_message(event.reply_token, FlexSendMessage(alt_text='نقاطي', contents=builder.stats(data, rank)))
            else:
                line_api.reply_message(event.reply_token, TextSendMessage(text='❌ لم تلعب بعد'))
        
        elif txt == 'الصدارة':
            leaders = db.leaderboard()
            line_api.reply_message(event.reply_token, FlexSendMessage(alt_text='الصدارة', contents=builder.leaderboard(leaders)))
        
        elif txt == 'ثيم':
            line_api.reply_message(event.reply_token, FlexSendMessage(alt_text='الثيمات', contents=builder.themes()))
        
        elif txt.startswith('ثيم:'):
            theme = txt.split(':')[1]
            if theme in THEMES:
                db.set_theme(uid, theme)
                line_api.reply_message(event.reply_token, TextSendMessage(text=f'✅ تم التغيير إلى {THEMES[theme]["name"]}'))
        
        elif txt == 'إيقاف':
            if gm.get_game(gid):
                gm.end_game(gid)
                line_api.reply_message(event.reply_token, TextSendMessage(text='⏹️ تم إيقاف اللعبة'))
        
        elif txt in GAMES:
            if not gm.is_registered(uid):
                line_api.reply_message(event.reply_token, TextSendMessage(text='❌ اكتب "انضم" أولاً'))
            elif gm.get_game(gid):
                line_api.reply_message(event.reply_token, TextSendMessage(text='⚠️ يوجد لعبة نشطة'))
            else:
                game = GAMES[txt](line_api)
                game.set_theme(theme)
                gm.start_game(gid, game, txt)
                resp = game.start_game()
                line_api.reply_message(event.reply_token, resp)
        
        elif gm.get_game(gid) and gm.is_registered(uid):
            # إجابة في لعبة نشطة
            game_data = gm.get_game(gid)
            game = game_data['game']
            result = game.check_answer(txt, uid, name)
            
            if result.get('game_over'):
                db.update(uid, name, result['points'], result['won'], game_data['type'])
                gm.end_game(gid)
            
            line_api.reply_message(event.reply_token, result['response'])
    
    except Exception as e:
        logger.error(f'Error: {e}', exc_info=True)

@handler.add(FollowEvent)
def on_follow(event):
    uid = event.source.user_id
    gm.register(uid)
    builder = FlexBuilder('soft')
    line_api.reply_message(event.reply_token, FlexSendMessage(alt_text='مرحباً', contents=builder.welcome()))

if __name__ == '__main__':
    logger.info('🎮 Bot Mesh Started')
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
