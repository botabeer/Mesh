import random
import logging
from linebot.v3.messaging import (
    FlexMessage,
    FlexContainer,
    TextMessage,
    QuickReply,
    QuickReplyItem,
    MessageAction
)
from config import Config

logger = logging.getLogger(__name__)


class MafiaGame:
    """لعبة المافيا - نسخة آمنة لـ LINE"""

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

    # ================= Helpers =================

    def _c(self):
        return Config.get_theme(self.theme)

    def _safe_text(self, text: str, fallback: str = " "):
        if isinstance(text, str) and text.strip():
            return text
        return fallback

    def _quick_reply(self):
        return QuickReply(items=[
            QuickReplyItem(action=MessageAction(label="العاب", text="العاب")),
            QuickReplyItem(action=MessageAction(label="نقاطي", text="نقاطي")),
            QuickReplyItem(action=MessageAction(label="الصدارة", text="الصدارة")),
            QuickReplyItem(action=MessageAction(label="تحدي", text="تحدي")),
            QuickReplyItem(action=MessageAction(label="سؤال", text="سؤال")),
            QuickReplyItem(action=MessageAction(label="اعتراف", text="اعتراف")),
            QuickReplyItem(action=MessageAction(label="منشن", text="منشن")),
            QuickReplyItem(action=MessageAction(label="موقف", text="موقف")),
            QuickReplyItem(action=MessageAction(label="حكمة", text="حكمة")),
            QuickReplyItem(action=MessageAction(label="شخصية", text="شخصية")),
            QuickReplyItem(action=MessageAction(label="توافق", text="توافق")),
            QuickReplyItem(action=MessageAction(label="مافيا", text="مافيا")),
            QuickReplyItem(action=MessageAction(label="مساعدة", text="مساعدة"))
        ])

    def _create_bubble(self, title, texts, buttons=None):
        c = self._c()

        contents = [{
            "type": "text",
            "text": self._safe_text(title),
            "weight": "bold",
            "size": "xl",
            "color": c["primary"],
            "align": "center"
        }]

        clean_texts = [t for t in texts if isinstance(t, str) and t.strip()]
        if clean_texts:
            contents.append({"type": "separator", "margin": "lg", "color": c["border"]})

        for t in clean_texts:
            contents.append({
                "type": "text",
                "text": self._safe_text(t),
                "size": "sm",
                "color": c["text"],
                "wrap": True,
                "margin": "md"
            })

        if buttons:
            contents.append({"type": "separator", "margin": "lg", "color": c["border"]})
            contents.extend(buttons)

        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": contents,
                "backgroundColor": c["bg"],
                "paddingAll": "20px",
                "spacing": "none"
            }
        }

        return FlexMessage(
            alt_text=self._safe_text(title),
            contents=FlexContainer.from_dict(bubble),
            quickReply=self._quick_reply()
        )

    # ================= Screens =================

    def registration_flex(self):
        texts = [
            f"اللاعبون المسجلون: {len(self.players)}",
            "الحد الأدنى: 4 لاعبين",
            "الحد الأقصى: 12 لاعب",
            "ملاحظة: يجب إضافة البوت كصديق لاستقبال الدور في الخاص"
        ]

        c = self._c()
        buttons = [
            {
                "type": "button",
                "action": {"type": "message", "label": "انضم", "text": "انضم مافيا"},
                "style": "primary",
                "color": c["success"],
                "margin": "md"
            },
            {
                "type": "button",
                "action": {"type": "message", "label": "بدء اللعبة", "text": "بدء مافيا"},
                "style": "secondary",
                "margin": "sm"
            }
        ]

        return self._create_bubble("لعبة المافيا", texts, buttons)

    def game_instructions(self):
        texts = [
            "طريقة اللعب:",
            "في القروب: التصويت والمناقشة",
            "في الخاص: تصلك رسالة بدورك",
            "المافيا: اختر ضحية",
            "المحقق: اسأل عن لاعب",
            "الطبيب: احمي لاعبا",
            "يجب إضافة البوت كصديق"
        ]
        return self._create_bubble("شرح اللعبة", texts)

    def players_list_flex(self):
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
                    "action": {
                        "type": "message",
                        "label": self.players[uid]["name"],
                        "text": f"صوت {self.players[uid]['name']}"
                    },
                    "style": "secondary",
                    "margin": "xs"
                })

        return self._create_bubble("حالة اللعبة", texts, buttons if buttons else None)

    # ================= Flow =================

    def start(self, user_id: str):
        self.phase = "registration"
        self.game_active = True
        self.user_id = user_id
        self.players = {}
        self.alive_players = []
        self.dead_players = []
        return [self.registration_flex(), self.game_instructions()]

    def check(self, text: str, user_id: str):
        cmd = Config.normalize(text)

        if cmd == "انضم مافيا":
            return self.add_player(user_id)

        if cmd == "بدء مافيا":
            return self.assign_roles()

        if cmd in ("الحاله", "الحالة"):
            return {"response": self.players_list_flex(), "game_over": False}

        if cmd == "شرح":
            return {"response": self.game_instructions(), "game_over": False}

        return None

    def add_player(self, user_id):
        if self.phase != "registration":
            return {"response": self._create_bubble("خطأ", ["التسجيل مغلق"]), "game_over": False}

        if user_id in self.players:
            return {"response": self._create_bubble("خطأ", ["أنت مسجل بالفعل"]), "game_over": False}

        if len(self.players) >= 12:
            return {"response": self._create_bubble("خطأ", ["اللعبة ممتلئة"]), "game_over": False}

        user = self.db.get_user(user_id) if self.db else None
        name = user["name"] if user else f"لاعب{len(self.players) + 1}"

        self.players[user_id] = {"name": name, "role": None, "alive": True}
        return {"response": self.registration_flex(), "game_over": False}

    def assign_roles(self):
        if len(self.players) < 4:
            return {"response": self._create_bubble("خطأ", ["يجب 4 لاعبين على الأقل"]), "game_over": False}

        num_players = len(self.players)
        num_mafia = max(1, num_players // 4)

        roles = ["mafia"] * num_mafia + ["detective", "doctor"]
        roles += ["citizen"] * (num_players - len(roles))
        random.shuffle(roles)

        self.alive_players = list(self.players.keys())
        self.phase = "night"
        self.day = 1

        texts = [
            "تم توزيع الأدوار",
            f"عدد المافيا: {num_mafia}",
            "تحقق من رسائلك الخاصة لمعرفة دورك"
        ]

        return {
            "response": self._create_bubble("بدأت اللعبة", texts),
            "game_over": False
        }
