from games.base_game import BaseGame
from linebot.v3.messaging import FlexMessage, FlexContainer, TextMessage
import random
import logging

logger = logging.getLogger(__name__)

class MafiaGame(BaseGame):
    ROLE_INFO = {
        "mafia": {
            "title": "المافيا",
            "desc": "اقتل شخص كل ليلة بارسال 'اقتل الاسم'",
            "color": "#8B0000"
        },
        "detective": {
            "title": "المحقق",
            "desc": "افحص شخص كل ليلة بارسال 'افحص الاسم'",
            "color": "#1E90FF"
        },
        "doctor": {
            "title": "الدكتور",
            "desc": "احم شخص او نفسك بارسال 'احمي الاسم' او 'احمي نفسي'",
            "color": "#32CD32"
        },
        "citizen": {
            "title": "مواطن",
            "desc": "ناقش وصوت في القروب لاكتشاف المافيا",
            "color": "#808080"
        }
    }

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
        self.game_active = False

    def _simple_flex(self, title, texts, buttons=None, bg_color=None):
        c = self.get_theme_colors()
        contents = [{
            "type": "text",
            "text": title,
            "weight": "bold",
            "size": "xl",
            "color": c['primary'],
            "align": "center"
        }]
        
        for t in texts:
            contents.append({
                "type": "text",
                "text": t,
                "size": "sm",
                "color": c['text'],
                "wrap": True,
                "margin": "md"
            })
        
        if buttons:
            contents.extend(buttons)
        
        return FlexMessage(
            alt_text=title,
            contents=FlexContainer.from_dict({
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": contents,
                    "backgroundColor": bg_color or c['card'],
                    "paddingAll": "15px"
                }
            })
        )

    def registration_flex(self):
        c = self.get_theme_colors()
        buttons = [
            {
                "type": "button",
                "action": {"type": "message", "label": "انضم للعبة", "text": "انضم مافيا"},
                "style": "primary",
                "color": c['primary'],
                "height": "sm",
                "margin": "md"
            },
            {
                "type": "button",
                "action": {"type": "message", "label": "بدء اللعبة", "text": "بدء مافيا"},
                "style": "secondary",
                "height": "sm",
                "margin": "sm"
            },
            {
                "type": "button",
                "action": {"type": "message", "label": "شرح اللعبة", "text": "شرح مافيا"},
                "style": "secondary",
                "height": "sm",
                "margin": "sm"
            }
        ]
        return self._simple_flex(
            "لعبة المافيا",
            [f"اللاعبون المسجلون: {len(self.players)}", "الحد الادنى: 4 لاعبين"],
            buttons
        )

    def explanation_flex(self):
        c = self.get_theme_colors()
        buttons = [{
            "type": "button",
            "action": {"type": "message", "label": "رجوع", "text": "مافيا"},
            "style": "primary",
            "color": c['primary'],
            "height": "sm",
            "margin": "md"
        }]
        texts = [
            "الفكرة: المافيا يحاول يقتل والمواطنون يكتشفون المافيا",
            "الادوار: المافيا يقتل والمحقق يفحص والدكتور يحمي",
            "المواطنون يناقشون ويصوتون في القروب"
        ]
        return self._simple_flex("شرح لعبة المافيا", texts, buttons)

    def night_flex(self):
        c = self.get_theme_colors()
        buttons = [{
            "type": "button",
            "action": {"type": "message", "label": "انهاء الليل", "text": "انهاء الليل"},
            "style": "primary",
            "color": c['primary'],
            "margin": "md"
        }]
        return self._simple_flex(
            f"الليل - اليوم {self.day}",
            ["الادوار الخاصة استخدموا قدراتكم الان في الخاص"],
            buttons,
            c['card']
        )

    def day_flex(self):
        c = self.get_theme_colors()
        buttons = [{
            "type": "button",
            "action": {"type": "message", "label": "فتح صندوق التصويت", "text": "تصويت مافيا"},
            "style": "primary",
            "color": c['primary'],
            "margin": "md"
        }]
        return self._simple_flex(
            f"النهار - اليوم {self.day}",
            ["ناقشوا وصوتوا لاكتشاف المافيا"],
            buttons,
            c['card']
        )

    def voting_flex(self):
        c = self.get_theme_colors()
        alive = [p for p in self.players.values() if p["alive"]]
        buttons = []
        
        for p in alive[:10]:
            buttons.append({
                "type": "button",
                "action": {"type": "message", "label": p["name"], "text": f"صوت {p['name']}"},
                "style": "secondary",
                "height": "sm",
                "margin": "xs"
            })
        
        buttons.append({
            "type": "button",
            "action": {"type": "message", "label": "انهاء التصويت", "text": "انهاء التصويت"},
            "style": "primary",
            "color": c['primary'],
            "margin": "md"
        })
        
        return self._simple_flex("التصويت", [], buttons)

    def winner_flex(self, winner_team):
        c = self.get_theme_colors()
        roles_content = []
        
        for p in self.players.values():
            role_name = self.ROLE_INFO[p["role"]]["title"]
            role_color = self.ROLE_INFO[p["role"]]["color"]
            status = "حي" if p["alive"] else "ميت"
            status_color = c['success'] if p["alive"] else c['text3']
            
            roles_content.append({
                "type": "box",
                "layout": "baseline",
                "margin": "md",
                "contents": [
                    {"type": "text", "text": p["name"], "size": "sm", "flex": 3, "color": c['text']},
                    {"type": "text", "text": role_name, "size": "sm", "color": role_color, "flex": 2, "align": "center", "weight": "bold"},
                    {"type": "text", "text": status, "size": "xs", "color": status_color, "flex": 1, "align": "end"}
                ]
            })
        
        return self._simple_flex(
            f"انتهت اللعبة\nالفريق الفائز: {winner_team}",
            [],
            roles_content,
            c['card']
        )

    def start_game(self):
        self.phase = "registration"
        self.game_active = True
        return self.registration_flex()

    def add_player(self, user_id, name):
        if self.phase != "registration":
            return {"response": TextMessage(text="اللعبة بدأت بالفعل")}
        if user_id in self.players:
            return {"response": TextMessage(text="انت مسجل بالفعل")}
        
        self.players[user_id] = {"name": name, "role": None, "alive": True}
        logger.info(f"Player joined: {name}")
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
        logger.info(f"Roles assigned to {len(self.players)} players")
        
        return {
            "response": [
                TextMessage(text="تم توزيع الادوار بنجاح\nتحقق من رسائلك الخاصة لمعرفة دورك"),
                self.night_flex()
            ]
        }

    def send_role_private(self, user_id, role, line_api):
        info = self.ROLE_INFO[role]
        c = self.get_theme_colors()
        
        flex = FlexMessage(
            alt_text="دورك السري",
            contents=FlexContainer.from_dict({
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "backgroundColor": c["card"],
                    "paddingAll": "10px",
                    "contents": [
                        {
                            "type": "text",
                            "text": info["title"],
                            "weight": "bold",
                            "size": "xl",
                            "color": "#FFFFFF",
                            "align": "center",
                            "backgroundColor": info["color"],
                            "paddingAll": "15px"
                        },
                        {
                            "type": "text",
                            "text": info["desc"],
                            "size": "sm",
                            "color": c["text"],
                            "wrap": True,
                            "margin": "md"
                        }
                    ]
                }
            })
        )
        
        try:
            line_api.push_message(user_id, flex)
        except Exception as e:
            logger.error(f"Error sending role to player {user_id}: {e}")

    def process_night(self):
        mafia_target = self.night_actions.get("mafia_target")
        doctor_target = self.night_actions.get("doctor_target")
        
        msg = "طلع الصباح ولم يقتل احد الليلة الماضية"
        
        if mafia_target and mafia_target != doctor_target:
            self.players[mafia_target]["alive"] = False
            victim_name = self.players[mafia_target]["name"]
            msg = f"طلع الصباح وتم اكتشاف جثة {victim_name}"
        
        self.night_actions.clear()
        self.phase = "day"
        
        winner = self.check_winner()
        if winner:
            return winner
        
        return {"response": [TextMessage(text=msg), self.day_flex()]}

    def vote(self, user_id, target_name):
        if self.phase != "voting":
            return {"response": TextMessage(text="ليس وقت التصويت الآن")}
        
        if user_id not in self.players or not self.players[user_id]["alive"]:
            return {"response": TextMessage(text="لا يمكنك التصويت")}
        
        target_id = None
        for uid, p in self.players.items():
            if p["name"] == target_name and p["alive"]:
                target_id = uid
                break
        
        if not target_id:
            return {"response": TextMessage(text="اللاعب غير موجود أو ميت")}
        
        self.votes[user_id] = target_id
        return {"response": TextMessage(text=f"تم تسجيل صوتك ضد {target_name}")}

    def end_voting(self):
        if self.phase != "voting":
            return {"response": TextMessage(text="ليس وقت التصويت")}
        
        if not self.votes:
            return {"response": TextMessage(text="لم يصوت أحد")}
        
        vote_counts = {}
        for target_id in self.votes.values():
            vote_counts[target_id] = vote_counts.get(target_id, 0) + 1
        
        max_votes = max(vote_counts.values())
        most_voted = [uid for uid, count in vote_counts.items() if count == max_votes]
        
        if len(most_voted) > 1:
            msg = "تعادل في الأصوات لم يتم إعدام أحد"
        else:
            executed_id = most_voted[0]
            self.players[executed_id]["alive"] = False
            executed_name = self.players[executed_id]["name"]
            executed_role = self.ROLE_INFO[self.players[executed_id]["role"]]["title"]
            msg = f"تم إعدام {executed_name}\nكان دوره: {executed_role}"
        
        self.votes.clear()
        self.phase = "night"
        self.day += 1
        
        winner = self.check_winner()
        if winner:
            return winner
        
        return {"response": [TextMessage(text=msg), self.night_flex()]}

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

    def get_question(self):
        return self.start_game()

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
            self.votes.clear()
            return {"response": self.voting_flex()}
        if text.startswith("صوت ") and self.phase == "voting":
            return self.vote(user_id, text.replace("صوت ", "").strip())
        if text == "انهاء التصويت" and self.phase == "voting":
            return self.end_voting()
        
        role = self.players.get(user_id, {}).get("role")
        
        if role == "mafia" and self.phase == "night" and text.startswith("اقتل "):
            target = text.replace("اقتل ", "").strip()
            for uid, p in self.players.items():
                if p["name"] == target and p["alive"] and uid != user_id:
                    self.night_actions["mafia_target"] = uid
                    return {"response": TextMessage(text=f"تم اختيار {target} للقتل")}
            return {"response": TextMessage(text="اسم اللاعب غير صحيح او اللاعب ميت")}
        
        if role == "detective" and self.phase == "night" and text.startswith("افحص "):
            target = text.replace("افحص ", "").strip()
            for uid, p in self.players.items():
                if p["name"] == target and p["alive"] and uid != user_id:
                    result = "هذا الشخص هو المافيا" if p["role"] == "mafia" else "هذا الشخص بريء"
                    return {"response": TextMessage(text=f"نتيجة الفحص:\n{target}: {result}")}
            return {"response": TextMessage(text="اسم اللاعب غير صحيح او اللاعب ميت")}
        
        if role == "doctor" and self.phase == "night" and text.startswith("احمي "):
            target = text.replace("احمي ", "").strip()
            if target == "نفسي":
                self.night_actions["doctor_target"] = user_id
                return {"response": TextMessage(text="تم حماية نفسك")}
            for uid, p in self.players.items():
                if p["name"] == target and p["alive"]:
                    self.night_actions["doctor_target"] = uid
                    return {"response": TextMessage(text=f"تم حماية {target}")}
            return {"response": TextMessage(text="اسم اللاعب غير صحيح او اللاعب ميت")}
        
        return None
