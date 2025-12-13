import sqlite3
import logging
from datetime import datetime
from typing import Dict, List, Optional
from contextlib import contextmanager
from linebot.v3.messaging import FlexMessage, FlexContainer, TextMessage, QuickReply, QuickReplyItem, MessageAction

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# ---------------- Database ---------------- #
class Database:
    """SQLite database handler مع دعم النقاط، الثيم، التسجيل، النقاط المؤقتة."""
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.init_db()

    @contextmanager
    def _get_connection(self):
        conn = sqlite3.connect(self.db_path, timeout=10)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            conn.close()

    def init_db(self):
        try:
            with self._get_connection() as conn:
                c = conn.cursor()
                c.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        user_id TEXT PRIMARY KEY,
                        name TEXT NOT NULL,
                        points INTEGER DEFAULT 0,
                        temp_points INTEGER DEFAULT 0,
                        is_registered INTEGER DEFAULT 0,
                        theme TEXT DEFAULT 'فاتح',
                        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                        last_active TEXT DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                c.execute("CREATE INDEX IF NOT EXISTS idx_users_points ON users(points DESC)")
                c.execute("CREATE INDEX IF NOT EXISTS idx_users_registered ON users(is_registered)")
        except Exception as e:
            logger.error(f"Database initialization error: {e}")

    def get_user(self, user_id: str) -> Optional[Dict]:
        try:
            with self._get_connection() as conn:
                c = conn.cursor()
                c.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
                row = c.fetchone()
                return dict(row) if row else None
        except Exception as e:
            logger.error(f"Get user error: {e}")
            return None

    def create_user(self, user_id: str, name: str, is_registered: int = 0, theme: str = "فاتح"):
        try:
            with self._get_connection() as conn:
                c = conn.cursor()
                c.execute("INSERT OR IGNORE INTO users (user_id,name,is_registered,theme) VALUES (?,?,?,?)",
                          (user_id,name,is_registered,theme))
        except Exception as e:
            logger.error(f"Create user error: {e}")

    def update_user(self, user_id: str, **kwargs):
        try:
            with self._get_connection() as conn:
                c = conn.cursor()
                updates, values = [], []
                for k,v in kwargs.items():
                    if k in ['name','points','temp_points','is_registered','theme']:
                        updates.append(f"{k}=?")
                        values.append(v)
                if updates:
                    updates.append("last_active=?")
                    values.append(datetime.utcnow().isoformat())
                    query=f"UPDATE users SET {', '.join(updates)} WHERE user_id=?"
                    values.append(user_id)
                    c.execute(query,values)
        except Exception as e:
            logger.error(f"Update user error: {e}")

    def add_points(self,user_id:str,points:int,name:str="Unknown",temp:bool=False):
        user=self.get_user(user_id)
        if not user:
            self.create_user(user_id,name,is_registered=1)
        elif name!="Unknown" and user.get("name")!=name:
            self.update_user(user_id,name=name)
        field="temp_points" if temp else "points"
        try:
            with self._get_connection() as conn:
                c=conn.cursor()
                c.execute(f"UPDATE users SET {field}={field}+?,last_active=? WHERE user_id=?",
                          (points,datetime.utcnow().isoformat(),user_id))
        except Exception as e:
            logger.error(f"Add points error: {e}")

    def reset_temp_points(self):
        try:
            with self._get_connection() as conn:
                c=conn.cursor()
                c.execute("UPDATE users SET temp_points=0")
        except Exception as e:
            logger.error(f"Reset temp points error: {e}")

    def get_leaderboard(self,limit:int=20,include_temp:bool=False)->List[tuple]:
        try:
            with self._get_connection() as conn:
                c=conn.cursor()
                if include_temp:
                    c.execute("SELECT name,points+temp_points AS total_points FROM users WHERE is_registered=1 ORDER BY total_points DESC LIMIT ?",(limit,))
                    return [(r['name'],r['total_points']) for r in c.fetchall()]
                else:
                    c.execute("SELECT name,points FROM users WHERE is_registered=1 ORDER BY points DESC LIMIT ?",(limit,))
                    return [(r['name'],r['points']) for r in c.fetchall()]
        except Exception as e:
            logger.error(f"Get leaderboard error: {e}")
            return []

# ---------------- UI Builder ---------------- #
class UIBuilder:
    """UI Builder ديناميكي حسب ثيم المستخدم: فاتح زجاجي 'فاتح', داكن زجاجي 'داكن'"""
    def __init__(self):
        self.themes={
            "فاتح":{"primary":"#007AFFCC","secondary":"#5AC8FACC","success":"#34C759CC","warning":"#FF9500CC",
                    "danger":"#FF3B30CC","bg":"#FFFFFF33","card":"#FFFFFF66","text":"#000000CC","text2":"#3C3C43CC",
                    "text3":"#8E8E93CC","border":"#E5E5EA66"},
            "داكن":{"primary":"#0A84FFCC","secondary":"#64D2FFCC","success":"#30D158CC","warning":"#FF9F0ACC",
                    "danger":"#FF453ACC","bg":"#1C1C1E33","card":"#2C2C2ECC","text":"#FFFFFFCC","text2":"#D1D1D6CC",
                    "text3":"#8E8E93CC","border":"#3A3A3C66"}
        }

    # Quick Reply ثابت
    def _get_quick_reply(self)->QuickReply:
        return QuickReply(items=[QuickReplyItem(action=MessageAction(label=l,text=l)) for l in ["بداية","العاب","نقاطي","الصدارة","مساعدة"]])

    # ألوان حسب المستخدم
    def _colors(self,user_theme:str="فاتح")->Dict[str,str]: return self.themes.get(user_theme,self.themes["فاتح"])
    def _create_flex(self,alt_text:str,contents:dict)->FlexMessage: return FlexMessage(alt_text=alt_text,contents=FlexContainer.from_dict(contents),quick_reply=self._get_quick_reply())
    def _create_text(self,text:str)->TextMessage: return TextMessage(text=text,quick_reply=self._get_quick_reply())
    def _build_buttons(self,actions:List[str],colors:Dict[str,str],primary=True)->List[dict]:
        rows=[]
        for i in range(0,len(actions),3):
            row={"type":"box","layout":"horizontal","spacing":"sm","margin":"md","contents":[]}
            for a in actions[i:i+3]: row["contents"].append({"type":"button","style":"primary" if primary else "secondary","height":"sm","color":colors["primary"] if primary else None,"action":{"type":"message","label":a,"text":a}})
            rows.append(row)
        return rows

    def welcome_card(self,display_name:str,is_registered:bool,points:int=0,user_theme:str="فاتح")->FlexMessage:
        c=self._colors(user_theme)
        status_text=f"مسجل | النقاط: {points}" if is_registered else "غير مسجل"
        status_color=c["success"] if is_registered else c["warning"]
        buttons=[{"type":"button","style":"primary","height":"sm","color":c["primary"],"action":{"type":"message","label":"العاب","text":"العاب"}},
                 {"type":"button","style":"secondary","height":"sm","action":{"type":"message","label":"نقاطي","text":"نقاطي"}},
                 {"type":"button","style":"secondary","height":"sm","action":{"type":"message","label":"الصدارة","text":"الصدارة"}}]
        if not is_registered: buttons.append({"type":"button","style":"secondary","height":"sm","action":{"type":"message","label":"تسجيل","text":"تسجيل"}})
        flex={"type":"bubble","size":"mega","body":{"type":"box","layout":"vertical","paddingAll":"20px","backgroundColor":c["card"],"contents":[
            {"type":"text","text":f"مرحبا {display_name}","size":"xl","weight":"bold","color":c["primary"],"align":"center"},
            {"type":"text","text":status_text,"size":"sm","color":status_color,"align":"center","margin":"md"},
            {"type":"separator","margin":"lg","color":c["border"]},
            {"type":"box","layout":"vertical","spacing":"sm","margin":"lg","contents":buttons}
        ]}}
        return self._create_flex("بداية",flex)

    def leaderboard_card(self,leaders:List[tuple],user_theme:str="فاتح")->FlexMessage:
        c=self._colors(user_theme);lc=[];medals=["🥇","🥈","🥉"]
        for i,(n,p) in enumerate(leaders[:10]): medal=medals[i] if i<3 else f"{i+1}."; lc.append({"type":"box","layout":"horizontal","margin":"sm","contents":[{"type":"text","text":medal,"size":"sm","color":c["text"],"flex":0},{"type":"text","text":n,"size":"sm","color":c["text"],"flex":3,"margin":"sm"},{"type":"text","text":str(p),"size":"sm","color":c["primary"],"weight":"bold","flex":1,"align":"end"}]})
        flex={"type":"bubble","size":"mega","body":{"type":"box","layout":"vertical","paddingAll":"20px","backgroundColor":c["card"],"contents":[{"type":"text","text":"لوحة الصدارة","size":"xl","weight":"bold","color":c["primary"],"align":"center"},{"type":"separator","margin":"lg","color":c["border"]},{"type":"box","layout":"vertical","margin":"lg","contents":lc}]}}
        return self._create_flex("لوحة الصدارة",flex)

    def text_game_screen(self,game_name:str,question:str,round_num:int,user_theme:str="فاتح")->FlexMessage:
        c=self._colors(user_theme)
        flex={"type":"bubble","size":"mega","body":{"type":"box","layout":"vertical","paddingAll":"20px","backgroundColor":c["card"],"contents":[
            {"type":"text","text":game_name,"size":"xl","weight":"bold","color":c["primary"],"align":"center"},
            {"type":"text","text":f"جولة {round_num}","size":"sm","color":c["text3"],"align":"center","margin":"xs"},
            {"type":"separator","margin":"md","color":c["border"]},
            {"type":"text","text":question,"size":"md","color":c["text"],"wrap":True,"margin":"md"},
            {"type":"separator","margin":"md","color":c["border"]},
            *self._build_buttons(["جاوب","لمح","وقف"],c,primary=False)
        ]}}
        return self._create_flex(game_name,flex)

    def game_over_screen(self,game_name:str,points:int,user_theme:str="فاتح")->FlexMessage:
        c=self._colors(user_theme)
        flex={"type":"bubble","size":"mega","body":{"type":"box","layout":"vertical","paddingAll":"20px","backgroundColor":c["card"],"contents":[
            {"type":"text","text":f"{game_name} انتهت","size":"xl","weight":"bold","color":c["primary"],"align":"center"},
            {"type":"text","text":f"نقاطك: {points}","size":"md","color":c["text"],"align":"center","margin":"md"},
            {"type":"separator","margin":"md","color":c["border"]},
            {"type":"button","style":"primary","height":"sm","margin":"md","color":c["primary"],"action":{"type":"message","label":"الرئيسية","text":"بداية"}}
        ]}}
        return self._create_flex(f"{game_name} انتهت",flex)

    def registration_prompt(self)->TextMessage: return self._create_text("أرسل اسمك للتسجيل في نظام النقاط")
    def registration_success(self,username:str,points:int,user_theme:str="فاتح")->TextMessage: return self._create_text(f"تم التسجيل بنجاح!\nالاسم: {username}\nالنقاط: {points}")
    def unregister_confirm(self,username:str,points:int,user_theme:str="فاتح")->TextMessage: return self._create_text(f"تم الانسحاب من النظام\nالاسم: {username}\nالنقاط المحفوظة: {points}")
    def game_stopped(self,game_name:str,user_theme:str="فاتح")->TextMessage: return self._create_text(f"تم إيقاف لعبة {game_name}")

# ---------------- Bot Helper ---------------- #
class BotHelper:
    """ربط Database و UIBuilder للأوامر بسهولة"""
    def __init__(self,db:Database,ui:UIBuilder):
        self.db=db
        self.ui=ui

    def handle_welcome(self,user_id:str,display_name:str)->FlexMessage:
        user=self.db.get_user(user_id)
        if not user: self.db.create_user(user_id,display_name,is_registered=0)
        user=self.db.get_user(user_id)
        return self.ui.welcome_card(display_name,bool(user.get("is_registered")),user.get("points",0),user.get("theme","فاتح"))

    def handle_leaderboard(self,limit:int=10,include_temp:bool=False)->FlexMessage:
        leaders=self.db.get_leaderboard(limit=limit,include_temp=include_temp)
        return self.ui.leaderboard_card(leaders)

    def add_points(self,user_id:str,points:int,name:str="Unknown"): self.db.add_points(user_id,points,name=name,temp=False)
    def add_temp_points(self,user_id:str,points:int,name:str="Unknown"): self.db.add_points(user_id,points,name=name,temp=True)
    def reset_temp_points(self): self.db.reset_temp_points()
