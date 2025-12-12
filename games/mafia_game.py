from games.base_game import BaseGame
from linebot.v3.messaging import FlexMessage, FlexContainer, TextMessage
import random
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class MafiaGame(BaseGame):
    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, questions_count=1)
        self.game_name = "مافيا"
        self.supports_hint = False
        self.supports_reveal = False

        self.players = {}
        self.phase = "registration"
        self.day = 0
        self.votes = {}
        self.night_actions = {}

    def start_game(self):
        self.phase = "registration"
        self.players = {}
        self.votes = {}
        self.night_actions = {}
        self.day = 0
        self.game_active = True
        logger.info("بدء لعبة المافيا - مرحلة التسجيل")
        return self.registration_flex()

    def registration_flex(self):
        c = self.get_theme_colors()
        return FlexMessage(
            alt_text="لعبة المافيا - التسجيل",
            contents=FlexContainer.from_dict({
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "text", "text": "لعبة المافيا", "weight": "bold", "size": "xl", "color": c['primary'], "align": "center"},
                        {"type": "text", "text": f"اللاعبون المسجلون: {len(self.players)}", "size": "md", "color": c['text'], "align": "center", "margin": "md"},
                        {"type": "text", "text": "الحد الادنى: 4 لاعبين", "size": "sm", "color": c['text3'], "align": "center"},
                        {"type": "separator", "margin": "lg"},
                        {"type": "button", "action": {"type": "message", "label": "انضم للعبة", "text": "انضم مافيا"}, "style": "primary", "color": c['primary'], "height": "sm", "margin": "md"},
                        {"type": "button", "action": {"type": "message", "label": "بدء اللعبة", "text": "بدء مافيا"}, "style": "secondary", "height": "sm", "margin": "sm"},
                        {"type": "button", "action": {"type": "message", "label": "شرح اللعبة", "text": "شرح مافيا"}, "style": "secondary", "height": "sm", "margin": "sm"}
                    ],
                    "backgroundColor": c['card'],
                    "paddingAll": "20px"
                }
            })
        )

    def explanation_flex(self):
        c = self.get_theme_colors()
        return FlexMessage(
            alt_text="شرح لعبة المافيا",
            contents=FlexContainer.from_dict({
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "text", "text": "شرح لعبة المافيا", "weight": "bold", "size": "xl", "color": c['primary'], "align": "center"},
                        {"type": "text", "text": "الفكرة: المافيا يحاول يقتل، المواطنون يكتشفون المافيا", "size": "sm", "color": c['text'], "wrap": True, "margin": "md"},
                        {"type": "text", "text": "الادوار: المافيا يقتل، المحقق يفحص، الدكتور يحمي", "size": "sm", "color": c['text'], "wrap": True, "margin": "md"},
                        {"type": "text", "text": "المواطنون يناقشون ويصوتون في القروب", "size": "sm", "color": c['text'], "wrap": True, "margin": "md"},
                        {"type": "button", "action": {"type": "message", "label": "رجوع", "text": "مافيا"}, "style": "primary", "color": c['primary'], "height": "sm", "margin": "md"}
                    ],
                    "backgroundColor": c['card'],
                    "paddingAll": "20px"
                }
            })
        )

    def add_player(self, user_id, name):
        if self.phase != "registration":
            return {"response": TextMessage(text="اللعبة بدأت بالفعل")}
        if user_id in self.players:
            return {"response": TextMessage(text="انت مسجل بالفعل")}
        self.players[user_id] = {"name": name, "role": None, "alive": True}
        logger.info(f"لاعب جديد انضم: {name}")
        return {"response": self.registration_flex()}

    def assign_roles(self, line_api):
        if len(self.players) < 4:
            return {"response": TextMessage(text="نحتاج 4 لاعبين على الاقل")}
        
        roles = ["mafia", "detective", "doctor"] + ["citizen"] * (len(self.players) - 3)
        random.shuffle(roles)
        
        for uid, role in zip(self.players.keys(), roles):
            self.players[uid]["role"] = role
            self.send_role_private(uid, role, line_api)
        
        self.phase = "night"
        self.day = 1
        logger.info(f"تم توزيع الادوار على {len(self.players)} لاعب")
        return {"response": [TextMessage(text="تم توزيع الادوار بنجاح\nتحقق من رسائلك الخاصة لمعرفة دورك"), self.night_flex()]}

    def send_role_private(self, user_id, role, line_api):
        c = self.get_theme_colors()
        role_info = {
            "mafia": {"title": "المافيا", "desc": "اقتل شخص كل ليلة بارسال 'اقتل [الاسم]'", "color": "#8B0000"},
            "detective": {"title": "المحقق", "desc": "افحص شخص كل ليلة بارسال 'افحص [الاسم]'", "color": "#1E90FF"},
            "doctor": {"title": "الدكتور", "desc": "احم شخص او نفسك بارسال 'احمي [الاسم]' او 'احمي نفسي'", "color": "#32CD32"},
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
                        {"type": "text", "text": info["title"], "weight": "bold", "size": "xl", "color": "#FFFFFF", "align": "center", "backgroundColor": info["color"], "paddingAll": "15px"},
                        {"type": "text", "text": info["desc"], "size": "sm", "color": c["text"], "wrap": True, "margin": "md"}
                    ],
                    "backgroundColor": c["card"],
                    "paddingAll": "10px"
                }
            })
        )
        try:
            line_api.push_message(user_id, flex)
        except Exception as e:
            logger.error(f"خطأ في ارسال الدور للاعب {user_id}: {e}")

    def night_flex(self):
        c = self.get_theme_colors()
        return FlexMessage(
            alt_text=f"الليل - اليوم {self.day}",
            contents=FlexContainer.from_dict({
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "text", "text": f"الليل - اليوم {self.day}", "weight": "bold", "size": "xl", "color": "#FFFFFF", "align": "center", "backgroundColor": c['primary'], "paddingAll": "15px"},
                        {"type": "text", "text": "الادوار الخاصة استخدموا قدراتكم الان في الخاص", "size": "sm", "color": c['text'], "margin": "md", "wrap": True},
                        {"type": "button", "action": {"type": "message", "label": "انهاء الليل", "text": "انهاء الليل"}, "style": "primary", "color": c['primary'], "margin": "md"}
                    ],
                    "paddingAll": "10px",
                    "backgroundColor": c['card']
                }
            })
        )

    def process_night(self):
        mafia_target = self.night_actions.get("mafia_target")
        doctor_target = self.night_actions.get("doctor_target")
        
        if mafia_target and mafia_target != doctor_target:
            self.players[mafia_target]["alive"] = False
            victim_name = self.players[mafia_target]["name"]
            msg = f"طلع الصباح وتم اكتشاف جثة {victim_name}"
        else:
            msg = "طلع الصباح ولم يقتل احد الليلة الماضية"
        
        self.night_actions = {}
        self.phase = "day"
        winner = self.check_winner()
        if winner:
            return winner
        return {"response": [TextMessage(text=msg), self.day_flex()]}

    def day_flex(self):
        c = self.get_theme_colors()
        return FlexMessage(
            alt_text=f"النهار - اليوم {self.day}",
            contents=FlexContainer.from_dict({
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "text", "text": f"النهار - اليوم {self.day}", "weight": "bold", "size": "xl", "color": "#FFFFFF", "align": "center", "backgroundColor": c['primary'], "paddingAll": "15px"},
                        {"type": "text", "text": "ناقشوا وصوتوا لاكتشاف المافيا", "size": "sm", "color": c['text'], "margin": "md"},
                        {"type": "button", "action": {"type": "message", "label": "فتح صندوق التصويت", "text": "تصويت مافيا"}, "style": "primary", "color": c['primary'], "margin": "md"}
                    ],
                    "paddingAll": "10px",
                    "backgroundColor": c['card']
                }
            })
        )

    def voting_flex(self):
        c = self.get_theme_colors()
        alive = [p for p in self.players.values() if p["alive"]]
        buttons = []
        for p in alive[:10]:
            buttons.append({"type": "button", "action": {"type": "message", "label": p["name"], "text": f"صوت {p['name']}"}, "style": "secondary", "height": "sm", "margin": "xs"})
        buttons.append({"type": "button", "action": {"type": "message", "label": "انهاء التصويت", "text": "انهاء التصويت"}, "style": "primary", "color": c['primary'], "margin": "md"})
        
        return FlexMessage(
            alt_text="التصويت",
            contents=FlexContainer.from_dict({
                "type": "bubble",
                "body": {"type": "box", "layout": "vertical", "contents": buttons, "paddingAll": "10px", "backgroundColor": c['card']}
            })
        )

    def vote(self, user_id, target_name):
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
        if not self.votes:
            self.phase = "night"
            self.day += 1
            return {"response": [TextMessage(text="لا توجد اصوات"), self.night_flex()]}
        
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
        return {"response": [TextMessage(text=f"تم اعدام {killed_name}"), self.night_flex()]}

    def check_winner(self):
        mafia_count = sum(1 for p in self.players.values() if p["alive"] and p["role"] == "mafia")
        citizen_count = sum(1 for p in self.players.values() if p["alive"] and p["role"] != "mafia")
        if mafia_count == 0:
            self.phase = "ended"
            self.game_active = False
            return {"response": self.winner_flex("المواطنون"), "game_over": True}
        if mafia_count >= citizen_count:
            self.phase = "ended"
            self.game_active = False
            return {"response": self.winner_flex("المافيا"), "game_over": True}
        return None

    def winner_flex(self, winner_team):
        c = self.get_theme_colors()
        roles_content = []
        for uid, p in self.players.items():
            role_name = {"mafia": "المافيا", "detective": "المحقق", "doctor": "الدكتور", "citizen": "مواطن"}[p["role"]]
            role_color = {"mafia": "#8B0000", "detective": "#1E90FF", "doctor": "#32CD32", "citizen": "#808080"}[p["role"]]
            status = "حي" if p["alive"] else "ميت"
            status_color = c['success'] if p["alive"] else c['text3']
            roles_content.append({
                "type": "box",
                "layout": "baseline",
                "contents": [
                    {"type": "text", "text": p["name"], "size": "sm", "flex": 3, "color": c['text']},
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
                    {"type": "text", "text": f"انتهت اللعبة\nالفريق الفائز: {winner_team}", "weight": "bold", "size": "xl", "color": c['success'], "align": "center"},
                    {"type": "box", "layout": "vertical", "contents": roles_content, "margin": "md"}
                ], "paddingAll": "10px", "backgroundColor": c['card']}
            })
        )

    def check_answer(self, text, user_id, display_name):
        text = text.strip()
        
        if text == "انضم مافيا":
            return self.add_player(user_id, display_name)
        if text == "بدء مافيا":
            return self.assign_roles(self.line_bot_api)
        if text == "شرح مافيا":
            return {"response": self.explanation_flex()}
        if text == "انهاء الليل" and self.phase == "night":
            return self.process_night()
        if text == "تصويت مافيا" and self.phase == "day":
            self.phase = "voting"
            return {"response": self.voting_flex()}
        if text.startswith("صوت ") and self.phase == "voting":
            target_name = text.replace("صوت ", "").strip()
            return self.vote(user_id, target_name)
        if text == "انهاء التصويت" and self.phase == "voting":
            return self.end_voting()
        
        player_role = self.players.get(user_id, {}).get("role")
        
        if text.startswith("اقتل ") and player_role == "mafia" and self.phase == "night":
            target_name = text.replace("اقتل ", "").strip()
            for uid, p in self.players.items():
                if p["name"] == target_name and p["alive"] and uid != user_id:
                    self.night_actions["mafia_target"] = uid
                    return {"response": TextMessage(text=f"تم اختيار {target_name} للقتل")}
            return {"response": TextMessage(text="اسم اللاعب غير صحيح او اللاعب ميت")}
        
        if text.startswith("افحص ") and player_role == "detective" and self.phase == "night":
            target_name = text.replace("افحص ", "").strip()
            for uid, p in self.players.items():
                if p["name"] == target_name and p["alive"] and uid != user_id:
                    result = "هذا الشخص هو المافيا" if p["role"] == "mafia" else "هذا الشخص بريء"
                    return {"response": TextMessage(text=f"نتيجة الفحص:\n{target_name}: {result}")}
            return {"response": TextMessage(text="اسم اللاعب غير صحيح او اللاعب ميت")}
        
        if text.startswith("احمي ") and player_role == "doctor" and self.phase == "night":
            target_name = text.replace("احمي ", "").strip()
            if target_name == "نفسي":
                self.night_actions["doctor_target"] = user_id
                return {"response": TextMessage(text="تم حماية نفسك")}
            for uid, p in self.players.items():
                if p["name"] == target_name and p["alive"]:
                    self.night_actions["doctor_target"] = uid
                    return {"response": TextMessage(text=f"تم حماية {target_name}")}
            return {"response": TextMessage(text="اسم اللاعب غير صحيح او اللاعب ميت")}
        
        return None

    def get_question(self):
        return self.start_game()
