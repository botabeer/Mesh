import random
import logging
from linebot.v3.messaging import FlexMessage, FlexContainer, TextMessage, QuickReply, QuickReplyItem, MessageAction
from config import Config

logger = logging.getLogger(__name__)


class MafiaGame:
    """لعبة المافيا - نسخة محسّنة مع رسائل خاصة"""
    
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
        self.group_id = None

    def _c(self):
        return Config.get_theme(self.theme)
    
    def _quick_reply(self):
        return QuickReply(items=[
            QuickReplyItem(action=MessageAction(label="البداية", text="بداية")),
            QuickReplyItem(action=MessageAction(label="العاب", text="العاب"))
        ])

    def _create_bubble(self, title, texts, buttons=None):
        """انشاء بطاقة منسقة"""
        c = self._c()
        contents = [{
            "type": "text", "text": title, "weight": "bold",
            "size": "xl", "color": c['primary'], "align": "center"
        }]
        
        if len(texts) > 0:
            contents.append({"type": "separator", "margin": "lg", "color": c["border"]})
        
        for t in texts:
            contents.append({
                "type": "text", "text": t, "size": "sm",
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
                    "paddingAll": "20px", "spacing": "none"
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
            "الحد الاقصى: 12 لاعب",
            "",
            "ملاحظة مهمة: يجب اضافة البوت كصديق لاستقبال الدور في الخاص"
        ]
        
        return self._create_bubble("لعبة المافيا", texts, buttons)

    def game_instructions(self):
        """شرح اللعبة"""
        c = self._c()
        texts = [
            "طريقة اللعب:",
            "",
            "في القروب:",
            "- التصويت على اللاعبين نهارا",
            "- مناقشة الاحداث",
            "",
            "في الخاص:",
            "- ستصلك رسالة بدورك",
            "- المافيا: اختر ضحية",
            "- المحقق: اسأل عن لاعب",
            "- الطبيب: احمي لاعبا",
            "",
            "ملاحظة: يجب اضافة البوت كصديق لاستقبال الرسائل الخاصة"
        ]
        return self._create_bubble("شرح اللعبة", texts, None)

    def players_list_flex(self):
        """عرض قائمة اللاعبين"""
        c = self._c()
        
        alive = [self.players[uid]["name"] for uid in self.alive_players]
        dead = [self.players[uid]["name"] for uid in self.dead_players]
        
        texts = [
            f"اليوم: {self.day}",
            f"المرحلة: {self.phase}",
            "",
            f"الاحياء ({len(alive)}):",
            ", ".join(alive) if alive else "لا احد",
            "",
            f"الموتى ({len(dead)}):",
            ", ".join(dead) if dead else "لا احد"
        ]
        
        buttons = []
        if self.phase == "day":
            for i, uid in enumerate(self.alive_players[:5]):
                buttons.append({
                    "type": "button",
                    "action": {"type": "message", "label": self.players[uid]["name"], "text": f"صوت {self.players[uid]['name']}"},
                    "style": "secondary", "height": "sm", "margin": "xs"
                })
        
        return self._create_bubble("حالة اللعبة", texts, buttons if buttons else None)

    def private_role_message(self, user_id, role):
        """رسالة الدور الخاصة"""
        c = self._c()
        
        role_info = {
            "mafia": ("انت من المافيا", "اختر ضحية كل ليلة", c["danger"]),
            "detective": ("انت المحقق", "اسأل عن لاعب كل ليلة", c["info"]),
            "doctor": ("انت الطبيب", "احمي لاعبا كل ليلة", c["success"]),
            "citizen": ("انت مواطن", "شارك في التصويت نهارا", c["text"])
        }
        
        title, desc, color = role_info.get(role, ("دورك", "غير معروف", c["text"]))
        
        contents = [
            {"type": "text", "text": title, "weight": "bold", "size": "xl", "color": color, "align": "center"},
            {"type": "separator", "margin": "lg", "color": c["border"]},
            {"type": "text", "text": desc, "size": "md", "color": c["text"], "wrap": True, "margin": "lg"},
            {"type": "text", "text": "راقب رسائلك الخاصة كل ليلة", "size": "xs", "color": c["text_tertiary"], "margin": "md"}
        ]
        
        bubble = {
            "type": "bubble", "size": "mega",
            "body": {
                "type": "box", "layout": "vertical",
                "contents": contents,
                "backgroundColor": c['bg'],
                "paddingAll": "20px", "spacing": "none"
            }
        }
        
        return FlexMessage(alt_text="دورك", contents=FlexContainer.from_dict(bubble))

    def night_action_buttons(self, user_id):
        """ازرار اختيار الفعل الليلي"""
        c = self._c()
        role = self.players[user_id]["role"]
        
        if role == "mafia":
            title = "اختر ضحية"
        elif role == "detective":
            title = "اسأل عن لاعب"
        elif role == "doctor":
            title = "احمي لاعبا"
        else:
            return None
        
        contents = [
            {"type": "text", "text": title, "weight": "bold", "size": "lg", "color": c['primary'], "align": "center"},
            {"type": "separator", "margin": "md", "color": c["border"]}
        ]
        
        for uid in self.alive_players:
            if uid != user_id:
                contents.append({
                    "type": "button",
                    "action": {"type": "message", "label": self.players[uid]["name"], "text": f"اختر {self.players[uid]['name']}"},
                    "style": "secondary", "height": "sm", "margin": "xs"
                })
        
        bubble = {
            "type": "bubble", "size": "mega",
            "body": {
                "type": "box", "layout": "vertical",
                "contents": contents,
                "backgroundColor": c['bg'],
                "paddingAll": "20px", "spacing": "none"
            }
        }
        
        return FlexMessage(alt_text=title, contents=FlexContainer.from_dict(bubble))

    def start(self, user_id: str):
        """بدء اللعبة"""
        self.phase = "registration"
        self.game_active = True
        self.user_id = user_id
        self.players = {}
        self.alive_players = []
        self.dead_players = []
        
        return [self.registration_flex(), self.game_instructions()]

    def check(self, text: str, user_id: str):
        """معالجة الاوامر"""
        cmd = Config.normalize(text)
        
        if cmd == "انضم مافيا":
            return self.add_player(user_id)
            
        if cmd == "بدء مافيا":
            return self.assign_roles()
        
        if cmd == "الحاله" or cmd == "الحالة":
            return {"response": self.players_list_flex(), "game_over": False}
        
        if cmd == "شرح":
            return {"response": self.game_instructions(), "game_over": False}
        
        return None

    def add_player(self, user_id):
        """اضافة لاعب"""
        if self.phase != "registration":
            return {"response": self._create_bubble("خطأ", ["التسجيل مغلق"], None), "game_over": False}
        
        if user_id in self.players:
            return {"response": self._create_bubble("خطأ", ["انت مسجل بالفعل"], None), "game_over": False}
        
        if len(self.players) >= 12:
            return {"response": self._create_bubble("خطأ", ["اللعبة ممتلئة"], None), "game_over": False}
        
        user = self.db.get_user(user_id) if self.db else None
        name = user['name'] if user else f"لاعب{len(self.players)+1}"
        
        self.players[user_id] = {"name": name, "role": None, "alive": True, "voted_for": None}
        return {"response": self.registration_flex(), "game_over": False}

    def assign_roles(self):
        """توزيع الادوار"""
        if len(self.players) < 4:
            return {"response": self._create_bubble("خطأ", ["يجب 4 لاعبين على الاقل"], None), "game_over": False}
        
        num_players = len(self.players)
        num_mafia = max(1, num_players // 4)
        
        roles = ["mafia"] * num_mafia + ["detective", "doctor"]
        roles += ["citizen"] * (num_players - len(roles))
        
        random.shuffle(roles)
        
        messages = []
        for uid, role in zip(self.players.keys(), roles):
            self.players[uid]["role"] = role
            messages.append(TextMessage(text=f"@{uid} دورك: {role}"))
        
        self.alive_players = list(self.players.keys())
        self.phase = "night"
        self.day = 1
        
        c = self._c()
        texts = [
            "تم توزيع الادوار",
            f"عدد المافيا: {num_mafia}",
            f"عدد المحققين: 1",
            f"عدد الاطباء: 1",
            f"عدد المواطنين: {num_players - num_mafia - 2}",
            "",
            "تحقق من رسائلك الخاصة لمعرفة دورك"
        ]
        
        buttons = [
            {"type": "button", "action": {"type": "message", "label": "الحالة", "text": "الحاله"},
             "style": "primary", "color": c["primary"], "height": "sm", "margin": "md"}
        ]
        
        return {
            "response": [self._create_bubble("بدأت اللعبة", texts, buttons)] + messages,
            "game_over": False
        }

    def show_status(self):
        """عرض حالة اللعبة"""
        return {"response": self.players_list_flex(), "game_over": False}
