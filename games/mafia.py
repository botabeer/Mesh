import random
import logging
from datetime import datetime
from base import BaseGame
from linebot.v3.messaging import FlexMessage, FlexContainer, QuickReply, QuickReplyItem, MessageAction
from config import Config

logger = logging.getLogger(__name__)

class MafiaGame(BaseGame):
    """لعبة المافيا مبنية على BaseGame"""

    MIN_PLAYERS = 4
    MAX_PLAYERS = 12

    ROLES = ["mafia", "detective", "doctor", "citizen"]

    def __init__(self, db, theme="light"):
        super().__init__(db, theme)
        self.game_name = "مافيا"
        self.players = {}  # user_id -> {"name":str, "role":str, "alive":bool}
        self.phase = "registration"  # registration, day, night
        self.day = 0
        self.votes = {}  # user_id -> voted_user_id
        self.night_actions = {}  # role -> target_user_id
        self.alive_players = []
        self.dead_players = []
        self.game_active = False

    # ================= Flex Helpers =================
    def _quick_reply(self):
        items = [
            "العاب", "نقاطي", "الصدارة", "تحدي", "سؤال", "اعتراف",
            "منشن", "موقف", "حكمة", "شخصية", "مافيا", "مساعدة"
        ]
        return QuickReply(items=[QuickReplyItem(action=MessageAction(label=i, text=i)) for i in items])

    def _create_bubble(self, title, texts, buttons=None):
        c = self._c()
        contents = [{"type": "text", "text": title, "weight": "bold", "size": "xl", "color": c["primary"], "align": "center"}]
        for t in texts:
            contents.append({"type": "text", "text": t, "size": "sm", "color": c["text"], "wrap": True, "margin": "md"})
        if buttons:
            contents.append({"type": "separator", "margin": "lg", "color": c["border"]})
            contents.extend(buttons)
        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {"type": "box", "layout": "vertical", "contents": contents, "backgroundColor": c["bg"], "paddingAll": "20px"}
        }
        return FlexMessage(alt_text=title, contents=FlexContainer.from_dict(bubble), quickReply=self._quick_reply())

    # ================= Screens =================
    def registration_flex(self):
        texts = [
            f"اللاعبون المسجلون: {len(self.players)}",
            f"الحد الأدنى: {self.MIN_PLAYERS} لاعبين",
            f"الحد الأقصى: {self.MAX_PLAYERS} لاعبين",
            "أرسل 'انضم مافيا' للانضمام"
        ]
        buttons = [
            {"type": "button", "action": {"type": "message", "label": "انضم", "text": "انضم مافيا"}, "style": "primary", "margin": "md"},
            {"type": "button", "action": {"type": "message", "label": "بدء اللعبة", "text": "بدء مافيا"}, "style": "secondary", "margin": "sm"}
        ]
        return self._create_bubble("تسجيل المافيا", texts, buttons)

    def game_status_flex(self):
        alive = [self.players[uid]["name"] for uid in self.alive_players]
        dead = [self.players[uid]["name"] for uid in self.dead_players]
        texts = [
            f"اليوم: {self.day}",
            f"المرحلة: {self.phase}",
            f"الأحياء ({len(alive)}): {', '.join(alive) if alive else 'لا أحد'}",
            f"الموتى ({len(dead)}): {', '.join(dead) if dead else 'لا أحد'}"
        ]
        buttons = []
        if self.phase == "day":
            for uid in self.alive_players[:5]:
                buttons.append({
                    "type": "button",
                    "action": {"type": "message", "label": self.players[uid]["name"], "text": f"صوت {self.players[uid]['name']}"},
                    "style": "secondary",
                    "margin": "xs"
                })
        return self._create_bubble("حالة اللعبة", texts, buttons if buttons else None)

    def instructions_flex(self):
        texts = [
            "طريقة اللعب:",
            "- في القروب: النقاش والتصويت",
            "- في الخاص: استلام دورك",
            "- المافيا: اختر ضحية",
            "- المحقق: اسأل عن لاعب",
            "- الطبيب: احمي لاعبًا",
        ]
        return self._create_bubble("شرح المافيا", texts)

    # ================= Flow =================
    def start(self, user_id):
        self.phase = "registration"
        self.game_active = True
        self.players = {}
        self.alive_players = []
        self.dead_players = []
        self.day = 0
        return [self.registration_flex(), self.instructions_flex()]

    def check(self, text, user_id):
        cmd = Config.normalize(text)

        if cmd == "انضم مافيا":
            return self.add_player(user_id)
        if cmd == "بدء مافيا":
            return self.assign_roles()
        if cmd in ("الحاله", "الحالة"):
            return {"response": self.game_status_flex(), "game_over": False}
        if cmd == "شرح":
            return {"response": self.instructions_flex(), "game_over": False}

        return None

    # ================= Player Actions =================
    def add_player(self, user_id):
        if self.phase != "registration":
            return {"response": self._create_bubble("خطأ", ["التسجيل مغلق"]), "game_over": False}
        if user_id in self.players:
            return {"response": self._create_bubble("خطأ", ["أنت مسجل بالفعل"]), "game_over": False}
        if len(self.players) >= self.MAX_PLAYERS:
            return {"response": self._create_bubble("خطأ", ["اللعبة ممتلئة"]), "game_over": False}

        user = self.db.get_user(user_id)
        name = user["name"] if user else f"لاعب{len(self.players)+1}"
        self.players[user_id] = {"name": name, "role": None, "alive": True}
        return {"response": self.registration_flex(), "game_over": False}

    def assign_roles(self):
        if len(self.players) < self.MIN_PLAYERS:
            return {"response": self._create_bubble("خطأ", ["يجب 4 لاعبين على الأقل"]), "game_over": False}

        num_players = len(self.players)
        num_mafia = max(1, num_players // 4)
        roles = ["mafia"]*num_mafia + ["detective", "doctor"]
        roles += ["citizen"]*(num_players - len(roles))
        random.shuffle(roles)

        for uid, role in zip(self.players.keys(), roles):
            self.players[uid]["role"] = role

        self.alive_players = list(self.players.keys())
        self.phase = "night"
        self.day = 1

        texts = [f"تم توزيع الأدوار: {num_mafia} مافيا، تحقق من رسائلك الخاصة لمعرفة دورك"]
        return {"response": self._create_bubble("بدأت اللعبة", texts), "game_over": False}
