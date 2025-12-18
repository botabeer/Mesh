import random
import logging
from linebot.v3.messaging import FlexMessage, FlexContainer

from config import Config

logger = logging.getLogger(__name__)

class MafiaGameProfessional:
    MIN_PLAYERS = 4
    MAX_PLAYERS = 12

    def __init__(self, db, theme="light"):
        self.db = db
        self.theme = theme
        self.players = {}  # user_id -> {"name": str, "role": str, "alive": bool}
        self.phase = "registration"
        self.day = 0
        self.votes = {}
        self.night_actions = {}
        self.alive_players = []
        self.dead_players = []
        self.game_active = False
        self.mafia_list = []
        self.detective = None
        self.doctor = None

    # ----- Theme/colors -----
    def _c(self):
        return Config.get_theme(self.theme)

    # ----- Glass box wrapper -----
    def _glass_box(self, contents, padding="16px", margin="none"):
        c = self._c()
        bg_color = c.get("card_secondary", "#F5F5F5")
        return {
            "type": "box",
            "layout": "vertical",
            "contents": contents,
            "backgroundColor": bg_color,
            "cornerRadius": "16px",
            "paddingAll": padding,
            "spacing": "sm",
            "margin": margin
        }

    # ----- Flex bubble builder -----
    def _create_bubble(self, title, contents=None):
        c = self._c()
        if not contents:
            contents = [{"type": "text", "text": "لا توجد بيانات لعرضها", "size": "md", "align": "center"}]
        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {"type": "box", "layout": "vertical", "contents": contents, "paddingAll": "24px", "backgroundColor": c.get("card", "#FFFFFF")}
        }
        return FlexMessage(alt_text=title, contents=FlexContainer.from_dict(bubble))

    # ----- تسجيل اللاعبين عبر Flex -----
    def registration_screen(self):
        c = self._c()
        player_names = [p["name"] for p in self.players.values()]
        contents = [
            self._glass_box([
                {"type":"text","text":f"اللاعبون المسجلون: {len(player_names)}","size":"md","weight":"bold","align":"center"},
                {"type":"text","text":f"الحد الأدنى: {self.MIN_PLAYERS} لاعبين","size":"xs","color":c.get("text_secondary","#888888"),"align":"center"},
                {"type":"text","text":f"الحد الأقصى: {self.MAX_PLAYERS} لاعبين","size":"xs","color":c.get("text_tertiary","#AAAAAA"),"align":"center"},
            ], "20px", "lg")
        ]
        # قائمة لاعبين مسجلين
        if player_names:
            contents.append(self._glass_box([
                {"type":"text","text":"اللاعبون الحاليون:","size":"sm","weight":"bold","color":c.get("text_secondary","#888888")},
                {"type":"text","text":" - " + "\n - ".join(player_names),"size":"xs","color":c.get("text","#000000"),"wrap":True,"margin":"sm"}
            ],"12px","md"))
        # أزرار Flex للانضمام والبدء والشرح
        buttons = [
            {"type":"button","action":{"type":"message","label":"انضم","text":"انضم مافيا"},"style":"primary","color":c.get("button_primary","#1DB446"),"height":"sm","margin":"sm"},
            {"type":"button","action":{"type":"message","label":"بدء اللعبة","text":"بدء مافيا"},"style":"primary","color":c.get("button_primary","#1DB446"),"height":"sm","margin":"sm"},
            {"type":"button","action":{"type":"message","label":"شرح","text":"شرح"},"style":"secondary","height":"sm","margin":"sm"}
        ]
        contents.extend(buttons)
        return self._create_bubble("تسجيل المافيا", contents)

    # ----- شاشة اختيار لاعب لأي إجراء Flex -----
    def player_selection_screen(self, action_label, player_ids):
        if not player_ids:
            return self._create_bubble("اختيار لاعب", [{"type":"text","text":"لا يوجد لاعبين للاختيار","align":"center"}])
        buttons = []
        for uid in player_ids:
            name = self.players[uid]["name"]
            buttons.append({"type":"button","action":{"type":"message","label":name,"text":f"{action_label}:{uid}"},"style":"primary","height":"sm","margin":"sm"})
        return self._create_bubble(f"اختر لاعب لـ {action_label}", buttons)

    # ----- شرح اللعبة Flex -----
    def instructions_screen(self):
        instructions = (
            "شرح اللعبة:\n"
            "• في القروب: النقاش والتصويت\n"
            "• المافيا: تختار ضحية بالخاص للبوت\n"
            "• المحقق: يسأل عن لاعب بالخاص للبوت\n"
            "• الطبيب: يحمي لاعب بالخاص للبوت\n"
            "• المواطن: يصوت ويناقش في القروب\n"
            "ملاحظة: أضف البوت كصديق لتصلك رسائل دورك الخاصة."
        )
        return self._create_bubble("شرح المافيا", [self._glass_box([{"type":"text","text":instructions,"wrap":True,"size":"sm"}])])

    # ----- بدء اللعبة وتوزيع الأدوار Flex -----
    def start_game(self):
        if len(self.players) < self.MIN_PLAYERS:
            return self._create_bubble("خطأ", [{"type":"text","text":f"يجب أن يكون هناك على الأقل {self.MIN_PLAYERS} لاعبين"}])
        # توزيع الأدوار
        num_players = len(self.players)
        num_mafia = max(1, num_players // 4)
        roles = ["mafia"] * num_mafia + ["detective", "doctor"]
        roles += ["citizen"] * (num_players - len(roles))
        random.shuffle(roles)
        for uid, role in zip(self.players.keys(), roles):
            self.players[uid]["role"] = role
            self.players[uid]["alive"] = True
            if role == "mafia":
                self.mafia_list.append(uid)
            elif role == "detective":
                self.detective = uid
            elif role == "doctor":
                self.doctor = uid
        self.alive_players = list(self.players.keys())
        self.dead_players = []
        self.phase = "night"
        self.day = 1
        return self._create_bubble("بدأت اللعبة", [{"type":"text","text":"تم توزيع الأدوار"}])

    # ----- عملية الليل Flex -----
    def night_phase(self):
        # كل لاعب يحصل على Flex للإجراء حسب دوره
        night_messages = []
        for uid in self.alive_players:
            role = self.players[uid]["role"]
            if role == "mafia":
                # اختيار ضحية
                targets = [p for p in self.alive_players if p not in self.mafia_list]
                night_messages.append(self.player_selection_screen("قتل", targets))
            elif role == "doctor":
                # حماية لاعب
                night_messages.append(self.player_selection_screen("حماية", self.alive_players))
            elif role == "detective":
                # التحقيق على لاعب
                targets = [p for p in self.alive_players if p != uid]
                night_messages.append(self.player_selection_screen("تحقيق", targets))
        return night_messages

    # ----- عملية النهار Flex -----
    def day_phase(self):
        # التصويت على الإقصاء
        return self.player_selection_screen("صوت", self.alive_players)

    # ----- نافذة النهاية Flex -----
    def game_over_screen(self):
        c = self._c()
        contents = [{"type":"text","text":"انتهت اللعبة","size":"xl","weight":"bold","align":"center"}]
        # ملخص اللاعبين
        summary = []
        for p in self.players.values():
            state = "حي" if p["alive"] else "ميت"
            summary.append(f"{p['name']}: {p['role']} ({state})")
        contents.append(self._glass_box([{"type":"text","text":"الأدوار:\n"+"\n".join(summary),"wrap":True,"size":"sm"}]))
        # زر إعادة اللعب
        buttons = [{"type":"button","action":{"type":"message","label":"لعب مرة اخرى","text":"مافيا"},"style":"primary","color":c.get("button_primary","#1DB446"),"height":"sm"}]
        contents.extend(buttons)
        return self._create_bubble("انتهت اللعبة", contents)
