"""
ملف كامل للعبة المافيا - Mafia Game
يشمل كل شيء: التسجيل، توزيع الأدوار، الليل والنهار، التصويت،
كشف الأدوار، إعلان الفائز، وأزرار ونوافذ Flex لتسهيل الاستخدام.
"""

import random
import logging
from linebot.v3.messaging import TextMessage, FlexMessage, FlexContainer

# إعداد اللوج
logger = logging.getLogger(__name__)

# إعدادات عامة
MAFIA_CONFIG = {
    "min_players": 4  # الحد الأدنى للعبة
}

COLORS = {
    "primary": "#2E8B57",
    "white": "#FFFFFF",
    "card_bg": "#F0F0F0",
    "text_dark": "#333333",
    "text_light": "#666666",
    "success": "#32CD32",
    "warning": "#FF4500",
    "border": "#DDDDDD"
}


class MafiaGame:
    """اللعبة كاملة في ملف واحد"""

    def __init__(self, line_bot_api):
        self.line_bot_api = line_bot_api
        self.players = {}  # user_id: {name, role, alive}
        self.phase = "registration"  # registration, night, day, voting, ended
        self.day = 0
        self.votes = {}
        self.night_actions = {}

    # ======== التسجيل والشروحات ========
    def start_game(self):
        """بدء التسجيل في اللعبة"""
        self.phase = "registration"
        self.players = {}
        self.votes = {}
        self.night_actions = {}
        self.day = 0
        logger.info("بدء لعبة المافيا - مرحلة التسجيل")
        return self.registration_flex()

    def registration_flex(self):
        """بطاقة التسجيل مع أزرار الانضمام وبدء اللعبة وشرحها"""
        return FlexMessage(
            alt_text="لعبة المافيا - التسجيل",
            contents=FlexContainer.from_dict({
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "text", "text": "لعبة المافيا", "weight": "bold", "size": "xl", "color": COLORS['white'], "align": "center"},
                        {"type": "text", "text": f"اللاعبون المسجلون: {len(self.players)}", "size": "md", "color": COLORS['text_dark'], "align": "center"},
                        {"type": "text", "text": f"الحد الأدنى: {MAFIA_CONFIG['min_players']} لاعبين", "size": "sm", "color": COLORS['text_light'], "align": "center"},
                        {"type": "separator", "margin": "lg"},
                        {"type": "button", "action": {"type": "message", "label": "انضم للعبة", "text": "انضم مافيا"}, "style": "primary", "color": COLORS['primary'], "height": "sm"},
                        {"type": "button", "action": {"type": "message", "label": "بدء اللعبة", "text": "بدء مافيا"}, "style": "secondary", "height": "sm", "margin": "sm"},
                        {"type": "button", "action": {"type": "message", "label": "شرح اللعبة", "text": "شرح مافيا"}, "style": "secondary", "height": "sm", "margin": "sm"}
                    ],
                    "backgroundColor": COLORS['card_bg'],
                    "paddingAll": "20px"
                }
            })
        )

    def explanation_flex(self):
        """بطاقة شرح اللعبة"""
        return FlexMessage(
            alt_text="شرح لعبة المافيا",
            contents=FlexContainer.from_dict({
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "text", "text": "شرح لعبة المافيا", "weight": "bold", "size": "xl", "color": COLORS['white'], "align": "center"},
                        {"type": "text", "text": "الفكرة: المافيا يحاول يقتل، المواطنون يكتشفون المافيا", "size": "sm", "color": COLORS['text_dark'], "wrap": True, "margin": "md"},
                        {"type": "text", "text": "الأدوار الخاصة: المافيا - يقتل، المحقق - يفحص، الدكتور - يحمي", "size": "sm", "color": COLORS['text_dark'], "wrap": True, "margin": "md"},
                        {"type": "text", "text": "المواطنون يناقشون ويصوتون في القروب", "size": "sm", "color": COLORS['text_dark'], "wrap": True, "margin": "md"},
                        {"type": "button", "action": {"type": "message", "label": "رجوع", "text": "مافيا"}, "style": "primary", "color": COLORS['primary'], "height": "sm", "margin": "md"}
                    ],
                    "backgroundColor": COLORS['card_bg'],
                    "paddingAll": "20px"
                }
            })
        )

    # ======== إدارة اللاعبين ========
    def add_player(self, user_id, name):
        """إضافة لاعب للعبة"""
        if self.phase != "registration":
            return {"response": TextMessage(text="اللعبة بدأت بالفعل")}
        if user_id in self.players:
            return {"response": TextMessage(text="أنت مسجل بالفعل")}
        self.players[user_id] = {"name": name, "role": None, "alive": True}
        logger.info(f"لاعب جديد انضم: {name}")
        return {"response": self.registration_flex()}

    def assign_roles(self):
        """توزيع الأدوار على اللاعبين"""
        if len(self.players) < MAFIA_CONFIG["min_players"]:
            return {"response": TextMessage(text=f"نحتاج {MAFIA_CONFIG['min_players']} لاعبين على الأقل")}
        roles = ["mafia", "detective", "doctor"] + ["citizen"] * (len(self.players) - 3)
        random.shuffle(roles)
        for uid, role in zip(self.players.keys(), roles):
            self.players[uid]["role"] = role
            self.send_role_private(uid, role)
        self.phase = "night"
        self.day = 1
        logger.info(f"تم توزيع الأدوار على {len(self.players)} لاعب")
        return {"response": [TextMessage(text="تم توزيع الأدوار بنجاح\nتحقق من رسائلك الخاصة لمعرفة دورك"), self.night_flex()]}

    def send_role_private(self, user_id, role):
        """إرسال الدور الخاص للاعب"""
        role_info = {
            "mafia": {"title": "المافيا", "desc": "اقتُل شخص كل ليلة بإرسال 'اقتل [الاسم]'", "color": "#8B0000"},
            "detective": {"title": "المحقق", "desc": "افحص شخص كل ليلة بإرسال 'افحص [الاسم]'", "color": "#1E90FF"},
            "doctor": {"title": "الدكتور", "desc": "احمِ شخص أو نفسك بإرسال 'احمي [الاسم]' أو 'احمي نفسي'", "color": "#32CD32"},
            "citizen": {"title": "مواطن", "desc": "ناقش وصوت في القروب لاكتشاف المافيا", "color": "#808080"}
        }
        info = role_info[role]
        flex = FlexMessage(
            alt_text="دورك السري",
            contents=FlexContainer.from_dict({
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "text", "text": info["title"], "weight": "bold", "size": "xl", "color": COLORS['white'], "align": "center", "backgroundColor": info["color"], "paddingAll": "15px"},
                        {"type": "text", "text": info["desc"], "size": "sm", "color": COLORS['text_dark'], "wrap": True, "margin": "md"}
                    ],
                    "backgroundColor": COLORS['card_bg'],
                    "paddingAll": "10px"
                }
            })
        )
        try:
            self.line_bot_api.push_message(user_id, flex)
        except Exception as e:
            logger.error(f"خطأ في إرسال الدور للاعب {user_id}: {e}")

    # ======== الليل ========
    def night_flex(self):
        """بطاقة الليل"""
        return FlexMessage(
            alt_text=f"الليل - اليوم {self.day}",
            contents=FlexContainer.from_dict({
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "text", "text": f"الليل - اليوم {self.day}", "weight": "bold", "size": "xl", "color": COLORS['white'], "align": "center", "backgroundColor": COLORS['primary'], "paddingAll": "15px"},
                        {"type": "text", "text": "الأدوار الخاصة استخدموا قدراتكم الآن في الخاص", "size": "sm", "color": COLORS['text_dark'], "margin": "md"},
                        {"type": "button", "action": {"type": "message", "label": "إنهاء الليل", "text": "إنهاء الليل"}, "style": "primary", "color": COLORS['primary'], "margin": "md"}
                    ],
                    "paddingAll": "10px"
                }
            })
        )

    def process_night(self):
        """معالجة أحداث الليل"""
        mafia_target = self.night_actions.get("mafia_target")
        doctor_target = self.night_actions.get("doctor_target")
        if mafia_target and mafia_target != doctor_target:
            self.players[mafia_target]["alive"] = False
            victim_name = self.players[mafia_target]["name"]
            msg = f"طلع الصباح وتم اكتشاف جثة {victim_name}"
        else:
            msg = "طلع الصباح ولم يقتل أحد الليلة الماضية"
        self.night_actions = {}
        self.phase = "day"
        winner = self.check_winner()
        if winner:
            return winner
        return {"response": [TextMessage(text=msg), self.day_flex()]}

    # ======== النهار والتصويت ========
    def day_flex(self):
        """بطاقة النهار"""
        alive_players = [p['name'] for p in self.players.values() if p['alive']]
        alive_text = "\n".join([f"- {name}" for name in alive_players])
        return FlexMessage(
            alt_text=f"النهار - اليوم {self.day}",
            contents=FlexContainer.from_dict({
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "text", "text": f"النهار - اليوم {self.day}", "weight": "bold", "size": "xl", "color": COLORS['white'], "align": "center", "backgroundColor": COLORS['primary'], "paddingAll": "15px"},
                        {"type": "text", "text": "ناقشوا وصوتوا لاكتشاف المافيا", "size": "sm", "color": COLORS['text_dark'], "margin": "md"},
                        {"type": "button", "action": {"type": "message", "label": "فتح صندوق التصويت", "text": "تصويت مافيا"}, "style": "primary", "color": COLORS['primary'], "margin": "md"}
                    ],
                    "paddingAll": "10px"
                }
            })
        )

    def voting_flex(self):
        """بطاقة التصويت"""
        alive = [p for p in self.players.values() if p["alive"]]
        buttons = []
        for p in alive[:10]:
            buttons.append({"type": "button", "action": {"type": "message", "label": p["name"], "text": f"صوت {p['name']}"}, "style": "secondary", "height": "sm", "margin": "xs"})
        buttons.append({"type": "button", "action": {"type": "message", "label": "إنهاء التصويت", "text": "إنهاء التصويت"}, "style": "primary", "color": COLORS['primary'], "margin": "md"})
        return FlexMessage(
            alt_text="التصويت",
            contents=FlexContainer.from_dict({
                "type": "bubble",
                "body": {"type": "box", "layout": "vertical", "contents": buttons, "paddingAll": "10px"}
            })
        )

    def vote(self, user_id, target_name):
        """تسجيل صوت اللاعب"""
        if self.phase != "voting":
            return {"response": TextMessage(text="لم يبدأ التصويت بعد")}
        if user_id not in self.players or not self.players[user_id]["alive"]:
            return {"response": TextMessage(text="لا يمكنك التصويت")}
        for uid, p in self.players.items():
            if p["name"] == target_name and p["alive"]:
                self.votes[user_id] = uid
                return {"response": TextMessage(text=f"تم تسجيل صوتك ضد {target_name}")}
        return {"response": TextMessage(text="اسم اللاعب غير صحيح")}

    def end_voting(self):
        """إنهاء التصويت وإعلان النتيجة"""
        if not self.votes:
            self.phase = "night"
            self.day += 1
            return {"response": [TextMessage(text="لا توجد أصوات"), self.night_flex()]}
        vote_counts = {}
        for voted_uid in self.votes.values():
            vote_counts[voted_uid] = vote_counts.get(voted_uid, 0) + 1
        killed_uid = max(vote_counts, key=vote_counts.get)
        self.players[killed_uid]["alive"] = False
        killed_name = self.players[killed_uid]["name"]
        self.votes = {}
        self.phase = "night"
        self.day += 1
        winner = self.check_winner()
        if winner:
            return winner
        return {"response": [TextMessage(text=f"تم إعدام {killed_name}"), self.night_flex()]}

    # ======== التحقق من الفائز ========
    def check_winner(self):
        """التحقق من وجود فائز"""
        mafia_count = sum(1 for p in self.players.values() if p["alive"] and p["role"] == "mafia")
        citizen_count = sum(1 for p in self.players.values() if p["alive"] and p["role"] != "mafia")
        if mafia_count == 0:
            self.phase = "ended"
            return {"response": self.winner_flex("المواطنون"), "game_over": True}
        if mafia_count >= citizen_count:
            self.phase = "ended"
            return {"response": self.winner_flex("المافيا"), "game_over": True}
        return None

    def winner_flex(self, winner_team):
        """بطاقة إعلان الفائز"""
        roles_content = []
        for uid, p in self.players.items():
            role_name = {"mafia": "المافيا", "detective": "المحقق", "doctor": "الدكتور", "citizen": "مواطن"}[p["role"]]
            role_color = {"mafia": "#8B0000", "detective": "#1E90FF", "doctor": "#32CD32", "citizen": "#808080"}[p["role"]]
            status = "حي" if p["alive"] else "ميت"
            status_color = COLORS['success'] if p["alive"] else COLORS['text_light']
            roles_content.append({
                "type": "box",
                "layout": "baseline",
                "contents": [
                    {"type": "text", "text": p["name"], "size": "sm", "flex": 3, "color": COLORS['text_dark']},
                    {"type": "text", "text": role_name, "size": "sm", "color": role_color, "flex": 2, "align": "center", "weight": "bold"},
                    {"type": "text", "text": status, "size": "xs", "color": status_color, "flex": 1, "align": "end"}
                ],
                "margin": "md"
            })
        return FlexMessage(
            alt_text="نتيجة اللعبة",
            contents=FlexContainer.from_dict({
                "type": "bubble",
                "body": {"type": "box", "layout": "vertical", "contents": [
                    {"type": "text", "text": f"انتهت اللعبة\nالفريق الفائز: {winner_team}", "weight": "bold", "size": "xl", "color": COLORS['success'], "align": "center"},
                    {"type": "box", "layout": "vertical", "contents": roles_content, "margin": "md"}
                ], "paddingAll": "10px"}
            })
        )

    # ======== معالجة الرسائل ========
    def check_answer(self, text, user_id, display_name):
        """معالجة جميع أوامر اللعبة"""
        text = text.strip()
        if text == "انضم مافيا":
            return self.add_player(user_id, display_name)
        if text == "بدء مافيا":
            return self.assign_roles()
        if text == "شرح مافيا":
            return {"response": self.explanation_flex()}
        if text == "إنهاء الليل" and self.phase == "night":
            return self.process_night()
        if text == "تصويت مافيا" and self.phase == "day":
            self.phase = "voting"
            return {"response": self.voting_flex()}
        if text.startswith("صوت ") and self.phase == "voting":
            target_name = text.replace("صوت ", "").strip()
            return self.vote(user_id, target_name)
        if text == "إنهاء التصويت" and self.phase == "voting":
            return self.end_voting()
        # أوامر خاصة باللاعبين
        player_role = self.players.get(user_id, {}).get("role")
        if text.startswith("اقتل ") and player_role == "mafia" and self.phase == "night":
            target_name = text.replace("اقتل ", "").strip()
            for uid, p in self.players.items():
                if p["name"] == target_name and p["alive"] and uid != user_id:
                    self.night_actions["mafia_target"] = uid
                    return {"response": TextMessage(text=f"تم اختيار {target_name} للقتل")}
            return {"response": TextMessage(text="اسم اللاعب غير صحيح أو اللاعب ميت")}
        if text.startswith("افحص ") and player_role == "detective" and self.phase == "night":
            target_name = text.replace("افحص ", "").strip()
            for uid, p in self.players.items():
                if p["name"] == target_name and p["alive"] and uid != user_id:
                    result = "هذا الشخص هو المافيا" if p["role"] == "mafia" else "هذا الشخص بريء"
                    return {"response": TextMessage(text=f"نتيجة الفحص:\n{target_name}: {result}")}
            return {"response": TextMessage(text="اسم اللاعب غير صحيح أو اللاعب ميت")}
        if text.startswith("احمي ") and player_role == "doctor" and self.phase == "night":
            target_name = text.replace("احمي ", "").strip()
            if target_name == "نفسي":
                self.night_actions["doctor_target"] = user_id
                return {"response": TextMessage(text="تم حماية نفسك")}
            for uid, p in self.players.items():
                if p["name"] == target_name and p["alive"]:
                    self.night_actions["doctor_target"] = uid
                    return {"response": TextMessage(text=f"تم حماية {target_name}")}
            return {"response": TextMessage(text="اسم اللاعب غير صحيح أو اللاعب ميت")}
        return None
