import random
import logging
from linebot.v3.messaging import FlexMessage, FlexContainer, QuickReply, QuickReplyItem, MessageAction
from config import Config

logger = logging.getLogger(__name__)


class MafiaGame:
    """لعبة المافيا - نسخة كاملة ومحسّنة"""
    
    def __init__(self, db, theme: str = "light"):
        self.db = db
        self.theme = theme
        self.players = {}
        self.phase = "registration"
        self.day = 0
        self.votes = {}
        self.night_actions = {}
        self.game_active = False
        self.game_name = "مافيا"
        self.user_id = None
        self.alive_players = []
        self.dead_players = []

    def _c(self):
        return Config.get_theme(self.theme)
    
    def _quick_reply(self):
        return QuickReply(items=[
            QuickReplyItem(action=MessageAction(label="البداية", text="بداية")),
            QuickReplyItem(action=MessageAction(label="العاب", text="العاب"))
        ])

    def _create_bubble(self, title, texts, buttons=None):
        """إنشاء بطاقة أنيقة"""
        c = self._c()
        contents = [{
            "type": "text", "text": title, "weight": "bold",
            "size": "xl", "color": c['primary'], "align": "center"
        }]
        
        if len(texts) > 0:
            contents.append({"type": "separator", "margin": "lg", "color": c["border"]})
        
        for t in texts:
            contents.append({
                "type": "text", "text": t, "size": "md",
                "color": c['text'], "wrap": True, "margin": "md"
            })
        
        if buttons:
            contents.append({"type": "separator", "margin": "lg", "color": c["border"]})
            contents.extend(buttons)
        
        return FlexMessage(
            alt_text=title,
            contents=FlexContainer.from_dict({
                "type": "bubble", "size": "mega",
                "body": {
                    "type": "box", "layout": "vertical",
                    "contents": contents,
                    "backgroundColor": c['bg'],
                    "paddingAll": "24px"
                }
            }),
            quickReply=self._quick_reply()
        )

    def registration_flex(self):
        """شاشة التسجيل"""
        c = self._c()
        buttons = [
            {"type": "button", "action": {"type": "message", "label": "انضم", "text": "انضم مافيا"},
             "style": "primary", "color": c['success'], "height": "md", "margin": "md"},
            {"type": "button", "action": {"type": "message", "label": "بدء اللعبة", "text": "بدء مافيا"},
             "style": "secondary", "height": "sm", "margin": "sm"}
        ]
        
        texts = [
            f"اللاعبون المسجلون: {len(self.players)}",
            "الحد الادنى: 4 لاعبين",
            "الحد الاقصى: 12 لاعب"
        ]
        
        return self._create_bubble("لعبة المافيا", texts, buttons)

    def start(self, user_id: str):
        """بدء اللعبة"""
        self.phase = "registration"
        self.game_active = True
        self.user_id = user_id
        self.players = {}
        self.alive_players = []
        self.dead_players = []
        return self.registration_flex()

    def check(self, text: str, user_id: str):
        """معالجة الأوامر"""
        cmd = Config.normalize(text)
        
        if cmd == "انضم مافيا":
            user = self.db.get_user(user_id) if self.db else None
            name = user['name'] if user else f"لاعب{len(self.players)+1}"
            return self.add_player(user_id, name)
            
        if cmd == "بدء مافيا":
            return self.assign_roles()
        
        if cmd == "الحاله":
            return self.show_status()
        
        return None

    def add_player(self, user_id, name):
        """إضافة لاعب"""
        if self.phase != "registration":
            return {"response": self._create_bubble("خطأ", ["التسجيل مغلق"], None), "game_over": False}
        
        if user_id in self.players:
            return {"response": self._create_bubble("خطأ", ["انت مسجل بالفعل"], None), "game_over": False}
        
        if len(self.players) >= 12:
            return {"response": self._create_bubble("خطأ", ["اللعبة ممتلئة"], None), "game_over": False}
        
        self.players[user_id] = {"name": name, "role": None, "alive": True, "voted_for": None}
        return {"response": self.registration_flex(), "game_over": False}

    def assign_roles(self):
        """توزيع الأدوار"""
        if len(self.players) < 4:
            return {"response": self._create_bubble("خطأ", ["يجب 4 لاعبين على الاقل"], None), "game_over": False}
        
        num_players = len(self.players)
        num_mafia = max(1, num_players // 4)
        
        roles = ["mafia"] * num_mafia + ["detective", "doctor"]
        roles += ["citizen"] * (num_players - len(roles))
        
        random.shuffle(roles)
        
        for uid, role in zip(self.players.keys(), roles):
            self.players[uid]["role"] = role
        
        self.alive_players = list(self.players.keys())
        self.phase = "night"
        self.day = 1
        
        c = self._c()
        texts = [
            "تم توزيع الأدوار",
            f"عدد المافيا: {num_mafia}",
            f"عدد المحققين: 1",
            f"عدد الأطباء: 1",
            f"عدد المواطنين: {num_players - num_mafia - 2}",
            "",
            "ستصلك رسالة خاصة بدورك"
        ]
        
        buttons = [
            {"type": "button", "action": {"type": "message", "label": "الحالة", "text": "الحاله"},
             "style": "primary", "color": c["primary"], "height": "sm", "margin": "md"},
            {"type": "button", "action": {"type": "message", "label": "البداية", "text": "بداية"},
             "style": "secondary", "height": "sm", "margin": "sm"}
        ]
        
        return {
            "response": self._create_bubble("بدأت اللعبة", texts, buttons),
            "game_over": True,
            "won": True
        }

    def show_status(self):
        """عرض حالة اللعبة"""
        c = self._c()
        
        alive = [self.players[uid]["name"] for uid in self.alive_players]
        dead = [self.players[uid]["name"] for uid in self.dead_players]
        
        texts = [
            f"اليوم: {self.day}",
            f"المرحلة: {self.phase}",
            "",
            f"الأحياء ({len(alive)}):",
            ", ".join(alive) if alive else "لا احد",
            "",
            f"الموتى ({len(dead)}):",
            ", ".join(dead) if dead else "لا احد"
        ]
        
        return {"response": self._create_bubble("حالة اللعبة", texts, None), "game_over": False}
