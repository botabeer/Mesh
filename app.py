"""Bot Mesh v2.0 - Professional Gaming Bot | Abeer Aldosari © 2025"""
import os,sys,asyncio,logging,importlib
from datetime import datetime
from typing import Dict,Optional,Any
from flask import Flask,request,abort,jsonify
from linebot import LineBotApi,WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent,TextMessage,TextSendMessage,FlexSendMessage
from config import Config,THEMES,Theme
from database import Database
from flex_builder import FlexBuilder

logging.basicConfig(level=logging.DEBUG if Config.DEBUG else logging.INFO,
    format='%(asctime)s-%(levelname)s-%(message)s')
logger=logging.getLogger(__name__)

# Load games
GAMES_FOLDER="games"
def snake_to_camel(n):return"".join(w.capitalize()for w in n.split("_"))
def load_games():
    games={}
    if not os.path.exists(GAMES_FOLDER):return games
    for f in os.listdir(GAMES_FOLDER):
        if f.endswith("_game.py")and not f.startswith("__"):
            m=f[:-3];c=snake_to_camel(m)
            try:
                mod=importlib.import_module(f"{GAMES_FOLDER}.{m}")
                if cls:=getattr(mod,c,None):games[c]=cls;logger.info(f"✅ {c}")
            except Exception as e:logger.warning(f"⚠️ {c}: {e}")
    return games

GAMES_LOADED=load_games()
AVAILABLE_GAMES={k:v for k,v in Config.GAME_MAP.items()if v['class']in GAMES_LOADED}

# Flask & LINE
app=Flask(__name__)
app.config['JSON_AS_ASCII']=False
line_bot_api=LineBotApi(Config.LINE_CHANNEL_ACCESS_TOKEN)
handler=WebhookHandler(Config.LINE_CHANNEL_SECRET)
db=Database(Config.DB_PATH,Config.DB_NAME)

# AI
current_key_idx=0
USE_AI=bool(Config.GEMINI_API_KEYS)
def get_gemini_key():return Config.GEMINI_API_KEYS[current_key_idx]if Config.GEMINI_API_KEYS else None
def switch_key():
    global current_key_idx
    if len(Config.GEMINI_API_KEYS)>1:current_key_idx=(current_key_idx+1)%len(Config.GEMINI_API_KEYS);return True
    return False

# Metrics
class M:
    def __init__(self):self.r=self.g=0;self.s=datetime.now()
    def get(self):u=(datetime.now()-self.s).total_seconds();return{'r':self.r,'g':self.g,'u':f"{int(u//3600)}h"}
metrics=M()

# Game Manager
class GM:
    def __init__(self):self.a={};self.u=set();self.t={}
    def is_registered(self,i):return i in self.u
    def register(self,i):self.u.add(i)
    def unregister(self,i):self.u.discard(i)
    def create_game(self,i,g,t):self.a[i]={'game':g,'type':t,'created':datetime.now()}
    def get_game(self,i):return self.a.get(i)
    def end_game(self,i):return self.a.pop(i,None)
    def is_active(self,i):return i in self.a
    def set_theme(self,i,t):self.t[i]=t
    def get_theme(self,i):return self.t.get(i,'white')
gm=GM()

# Helpers
def get_name(uid):
    try:return line_bot_api.get_profile(uid).display_name
    except:return"لاعب"
def get_builder(uid):b=FlexBuilder();b.set_theme(gm.get_theme(uid));return b

# Commands
class C:
    def __init__(self):
        self.c={'مساعدة':self.help,'help':self.help,'انضم':self.join,'تسجيل':self.join,
            'انسحب':self.leave,'خروج':self.leave,'نقاطي':self.stats,'احصائياتي':self.stats,
            'الصدارة':self.leaderboard,'إيقاف':self.stop,'ايقاف':self.stop,'ثيم':self.theme_menu}
    def handle(self,e,u,t,g,n):
        if t.startswith('ثيم:'):self.set_theme(e,u,t.split(':')[1]);return True
        if cmd:=self.c.get(t):cmd(e,u,g,n);return True
        return False
    def help(self,e,u,*a):b=get_builder(u);line_bot_api.reply_message(e.reply_token,FlexSendMessage(alt_text="المساعدة",contents=b.create_help_menu()))
    def join(self,e,u,g,n):
        if gm.is_registered(u):line_bot_api.reply_message(e.reply_token,TextSendMessage(text=f"✅ أنت مسجل يا {n}\n\nاختر لعبة من الأزرار الثابتة أسفل الشاشة"))
        else:gm.register(u);b=get_builder(u);line_bot_api.reply_message(e.reply_token,FlexSendMessage(alt_text="مرحباً",contents=b.create_help_menu()))
    def leave(self,e,u,*a):
        if gm.is_registered(u):gm.unregister(u);line_bot_api.reply_message(e.reply_token,TextSendMessage(text="👋 تم الانسحاب بنجاح\n\nاكتب 'انضم' للعودة"))
        else:line_bot_api.reply_message(e.reply_token,TextSendMessage(text="❌ أنت غير مسجل"))
    def stats(self,e,u,*a):
        asyncio.run(db.initialize());user=asyncio.run(db.get_user(u));rank=asyncio.run(db.get_user_rank(u))if user else 0
        is_reg=gm.is_registered(u)
        d={'total_points':user.total_points,'games_played':user.games_played,'wins':user.wins,'is_registered':is_reg}if user else{'total_points':0,'games_played':0,'wins':0,'is_registered':is_reg}
        b=get_builder(u);line_bot_api.reply_message(e.reply_token,FlexSendMessage(alt_text="نقاطي",contents=b.create_stats_card(d,rank)))
    def leaderboard(self,e,u,*a):
        asyncio.run(db.initialize());l=asyncio.run(db.get_leaderboard())
        d=[{'display_name':x.display_name,'total_points':x.total_points}for x in l]
        b=get_builder(u);line_bot_api.reply_message(e.reply_token,FlexSendMessage(alt_text="الصدارة",contents=b.create_leaderboard(d)))
    def stop(self,e,u,g,*a):
        if gm.is_active(g):d=gm.end_game(g);line_bot_api.reply_message(e.reply_token,TextSendMessage(text=f"⏹️ تم إيقاف لعبة {d['type']}"))
        else:line_bot_api.reply_message(e.reply_token,TextSendMessage(text="❌ لا توجد لعبة نشطة"))
    def theme_menu(self,e,u,*a):b=get_builder(u);line_bot_api.reply_message(e.reply_token,FlexSendMessage(alt_text="الثيمات",contents=b.create_theme_selector()))
    def set_theme(self,e,u,t):
        gm.set_theme(u,t)
        tn={'white':'⚪ أبيض','black':'⚫ أسود','gray':'🔘 رمادي','purple':'💜 بنفسجي','blue':'💙 أزرق','pink':'🌸 وردي','mint':'🍃 نعناعي'}
        line_bot_api.reply_message(e.reply_token,TextSendMessage(text=f"✅ تم تغيير الثيم إلى {tn.get(t,t)}"))
cmds=C()

# Game functions
def start_game(gid,gc,gt,uid,e):
    try:
        ai_games=['IqGame','WordColorGame','LettersWordsGame','HumanAnimalPlantGame']
        g=gc(line_bot_api,use_ai=USE_AI,get_api_key=get_gemini_key,switch_key=switch_key)if gc.__name__ in ai_games else gc(line_bot_api)
        gm.create_game(gid,g,gt);r=g.start_game();line_bot_api.reply_message(e.reply_token,r);metrics.g+=1;return True
    except Exception as ex:logger.error(f"❌ {ex}");line_bot_api.reply_message(e.reply_token,TextSendMessage(text="❌ خطأ في بدء اللعبة"));return False

def handle_answer(e,u,t,g,n):
    if not(d:=gm.get_game(g)):return
    game,gt=d['game'],d['type']
    try:
        if r:=game.check_answer(t,u,n):
            if(p:=r.get('points',0))>0:asyncio.run(db.initialize());asyncio.run(db.update_user_score(u,n,p,r.get('won',False),gt))
            if r.get('game_over'):gm.end_game(g)
            line_bot_api.reply_message(e.reply_token,r.get('response',TextSendMessage(text=r.get('message',''))))
    except Exception as ex:logger.error(f"❌ {ex}")

# Routes
@app.route("/")
def home():
    s=metrics.get()
    return f'''<!DOCTYPE html><html dir="rtl"><head><meta charset="UTF-8"><title>Bot Mesh</title>
<style>body{{font-family:sans-serif;background:linear-gradient(135deg,#667eea,#764ba2);min-height:100vh;display:flex;align-items:center;justify-content:center;margin:0}}
.card{{background:#fff;border-radius:20px;padding:40px;max-width:500px;text-align:center;box-shadow:0 20px 60px rgba(0,0,0,0.3)}}
h1{{color:#667eea;margin-bottom:10px}}.status{{background:#d4edda;color:#155724;padding:10px;border-radius:10px;margin:20px 0}}
.stats{{display:grid;grid-template-columns:repeat(3,1fr);gap:15px;margin:20px 0}}.stat{{background:#f8f9fa;padding:15px;border-radius:10px}}
.stat-val{{font-size:2em;font-weight:bold;color:#667eea}}</style></head><body>
<div class="card"><h1>🎮 Bot Mesh</h1><div class="status">✅ يعمل بنجاح</div>
<div class="stats"><div class="stat"><div class="stat-val">{len(GAMES_LOADED)}</div>ألعاب</div>
<div class="stat"><div class="stat-val">{len(gm.u)}</div>لاعبين</div>
<div class="stat"><div class="stat-val">{s["r"]}</div>طلبات</div></div>
<p style="color:#666">Created by Abeer Aldosari © 2025</p></div></body></html>'''

@app.route("/health")
def health():return jsonify({'status':'healthy','version':Config.BOT_VERSION}),200

@app.route("/callback",methods=['POST'])
def callback():
    if not(sig:=request.headers.get('X-Line-Signature')):abort(400)
    body=request.get_data(as_text=True);metrics.r+=1
    try:handler.handle(body,sig)
    except InvalidSignatureError:abort(400)
    except Exception as e:logger.error(f"❌ {e}");abort(500)
    return'OK'

@handler.add(MessageEvent,message=TextMessage)
def handle_message(e):
    try:
        uid=e.source.user_id;text=e.message.text.strip();gid=getattr(e.source,'group_id',uid);name=get_name(uid)
        logger.info(f"📨 {name}: {text}")
        if cmds.handle(e,uid,text,gid,name):return
        if text in AVAILABLE_GAMES:
            if not gm.is_registered(uid):line_bot_api.reply_message(e.reply_token,TextSendMessage(text="❌ اكتب 'انضم' أولاً"));return
            gd=AVAILABLE_GAMES[text];gc=GAMES_LOADED.get(gd['class'])
            if not gc:line_bot_api.reply_message(e.reply_token,TextSendMessage(text="❌ اللعبة غير متاحة"));return
            if text=='توافق':g=gc(line_bot_api);gm.create_game(gid,g,text);line_bot_api.reply_message(e.reply_token,TextSendMessage(text="💖 لعبة التوافق!\n\nاكتب اسمين بمسافة\nمثال: ميش عبير"));return
            start_game(gid,gc,text,uid,e);return
        if gm.is_active(gid)and gm.is_registered(uid):handle_answer(e,uid,text,gid,name)
    except Exception as ex:logger.error(f"❌ {ex}",exc_info=True)

if __name__=="__main__":
    port=int(os.environ.get('PORT',5000))
    logger.info("="*50);logger.info("🎮 BOT MESH v2.0");logger.info("="*50)
    logger.info(f"🌐 Port: {port}");logger.info(f"🎯 Games: {len(GAMES_LOADED)}");logger.info(f"🎨 Themes: 7")
    logger.info("="*50);logger.info("Created by: Abeer Aldosari © 2025");logger.info("="*50)
    app.run(host='0.0.0.0',port=port,debug=Config.DEBUG)
