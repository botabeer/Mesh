import random
import logging
from linebot.v3.messaging import FlexMessage, FlexContainer, TextMessage, QuickReply, QuickReplyItem, MessageAction
from config import Config

logger = logging.getLogger(__name__)

class MafiaGame:
    ROLE_INFO = {
        "mafia": {"title": "المافيا", "desc": "اقتل شخص كل ليلة", "color": "#8B0000"},
        "detective": {"title": "المحقق", "desc": "افحص شخص كل ليلة", "color": "#1E90FF"},
        "doctor": {"title": "الدكتور", "desc": "احم شخص كل ليلة", "color": "#32CD32"},
        "citizen": {"title": "مواطن", "desc": "ناقش وصوت لاكتشاف المافيا", "color": "#808080"}
    }

    def __init__(self, db, theme: str = "light"):
        self.db = db
        self.theme = theme
        self.players = {}
        self.phase = "registration"
        self.day = 0
        self.votes = {}
        self.night_actions = {}
        self.game_active = False

    def _c(self):
        return Config.get_theme(self.theme)

    def _simple_flex(self, title, texts, buttons=None):
        c = self._c()
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
                "size": "mega",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": contents,
                    "backgroundColor": c['bg'],
                    "paddingAll": "20px"
                }
            })
        )

    def registration_flex(self):
        c = self._c()
        buttons = [
            {"type": "separator", "margin": "lg"},
            {
                "type": "button",
                "action": {"type": "message", "label": "انضم", "text": "انضم_مافيا"},
                "style": "primary",
                "color": c['primary'],
                "height": "sm",
                "margin": "md"
            },
            {
                "type": "button",
                "action": {"type": "message", "label": "بدء", "text": "بدء_مافيا"},
                "style": "secondary",
                "height": "sm",
                "margin": "sm"
            },
            {
                "type": "button",
                "action": {"type": "message", "label": "شرح", "text": "شرح_مافيا"},
                "style": "secondary",
                "height": "sm",
                "margin": "sm"
            }
        ]
        return self._simple_flex(
            "لعبة المافيا",
            [f"اللاعبون: {len(self.players)}", "الحد الادنى: 4 لاعبين"],
            buttons
        )

    def explanation_flex(self):
        c = self._c()
        buttons = [
            {"type": "separator", "margin": "lg"},
            {
                "type": "button",
                "action": {"type": "message", "label": "رجوع", "text": "مافيا"},
                "style": "primary",
                "color": c['primary'],
                "height": "sm",
                "margin": "md"
            }
        ]
        texts = [
            "الفكرة: المافيا تحاول القتل والمواطنون يكتشفون المافيا",
            "",
            "الادوار:",
            "- المافيا: يقتل شخص كل ليلة",
            "- المحقق: يفحص شخص كل ليلة",
            "- الدكتور: يحمي شخص كل ليلة",
            "- المواطنون: يناقشون ويصوتون",
            "",
            "الاوامر:",
            "- اقتل الاسم (للمافيا)",
            "- افحص الاسم (للمحقق)",
            "- احمي الاسم او احمي نفسي (للدكتور)"
        ]
        return self._simple_flex("شرح لعبة المافيا", texts, buttons)

    def night_flex(self):
        c = self._c()
        buttons = [
            {"type": "separator", "margin": "lg"},
            {
                "type": "button",
                "action": {"type": "message", "label": "انهاء الليل", "text": "انهاء_الليل"},
                "style": "primary",
                "color": c['primary'],
                "margin": "md"
            }
        ]
        return self._simple_flex(
            f"الليل - اليوم {self.day}",
            ["الادوار الخاصة استخدموا قدراتكم في الخاص"],
            buttons
        )

    def day_flex(self):
        c = self._c()
        buttons = [
            {"type": "separator", "margin": "lg"},
            {
                "type": "button",
                "action": {"type": "message", "label": "فتح التصويت", "text": "تصويت_مافيا"},
                "style": "primary",
                "color": c['primary'],
                "margin": "md"
            }
        ]
        return self._simple_flex(
            f"النهار - اليوم {self.day}",
            ["ناقشوا وصوتوا لاكتشاف المافيا"],
            buttons
        )

    def voting_flex(self):
        c = self._c()
        alive = [p for p in self.players.values() if p["alive"]]
        buttons = [{"type": "separator", "margin": "lg"}]
        
        for p in alive[:10]:
            buttons.append({
                "type": "button",
                "action": {"type": "message", "label": p['name'], "text": f"صوت {p['name']}"},
                "style": "secondary",
                "height": "sm",
                "margin": "xs"
            })
        
        buttons.append({
            "type": "button",
            "action": {"type": "message", "label": "انهاء التصويت", "text": "انهاء_التصويت"},
            "style": "primary",
            "color": c['primary'],
            "margin": "md"
        })
        
        return self._simple_flex("التصويت", [], buttons)

    def winner_flex(self, winner_team):
        c = self._c()
        contents = [
            {
                "type": "text",
                "text": f"الفريق الفائز: {winner_team}",
                "weight": "bold",
                "size": "xl",
                "color": c['primary'],
                "align": "center"
            },
            {"type": "separator", "margin": "md"}
        ]
        
        for p in self.players.values():
            role_name = self.ROLE_INFO[p["role"]]["title"]
            status = "حي" if p["alive"] else "ميت"
            
            contents.append({
                "type": "box",
                "layout": "horizontal",
                "backgroundColor": c['glass'],
                "cornerRadius": "8px",
                "paddingAll": "8px",
                "margin": "sm",
                "contents": [
                    {"type": "text", "text": p["name"], "size": "sm", "flex": 3, "color": c['text']},
                    {"type": "text", "text": role_name, "size": "sm", "flex": 2, "align": "center"},
                    {"type": "text", "text": status, "size": "xs", "flex": 1, "align": "end"}
                ]
            })
        
        contents.extend([
            {"type": "separator", "margin": "lg"},
            {
                "type": "button",
                "action": {"type": "message", "label": "البداية", "text": "بداية"},
                "style": "primary",
                "color": c['primary'],
                "margin": "md"
            }
        ])
        
        return FlexMessage(
            alt_text="انتهت اللعبة",
            contents=FlexContainer.from_dict({
                "type": "bubble",
                "size": "mega",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": contents,
                    "backgroundColor": c['bg'],
                    "paddingAll": "20px"
                }
            })
        )

    def start(self, user_id: str):
        self.phase = "registration"
        self.game_active = True
        return {"response": self.registration_flex(), "game_over": False}

    def check(self, text: str, user_id: str):
        cmd = Config.normalize(text)
        
        if cmd == "انضم_مافيا":
            user = self.db.get_user(user_id)
            if not user:
                return None
            return self.add_player(user_id, user['name'])
            
        if cmd == "بدء_مافيا":
            return self.assign_roles()
            
        if cmd == "شرح_مافيا":
            return {"response": self.explanation_flex(), "game_over": False}
            
        if cmd == "انهاء_الليل" and self.phase == "night":
            return self.process_night()
            
        if cmd == "تصويت_مافيا" and self.phase == "day":
            self.phase = "voting"
            self.votes.clear()
            return {"response": self.voting_flex(), "game_over": False}
            
        if text.startswith("صوت ") and self.phase == "voting":
            return self.vote(user_id, text.replace("صوت ", "").strip())
            
        if cmd == "انهاء_التصويت" and self.phase == "voting":
            return self.end_voting()
        
        role = self.players.get(user_id, {}).get("role")
        
        if role == "mafia" and self.phase == "night" and text.startswith("اقتل "):
            target = text.replace("اقتل ", "").strip()
            for uid, p in self.players.items():
                if p["name"] == target and p["alive"] and uid != user_id:
                    self.night_actions["mafia_target"] = uid
                    return {"response": TextMessage(text=f"تم اختيار {target} للقتل"), "game_over": False}
            return {"response": TextMessage(text="اسم اللاعب غير صحيح او اللاعب ميت"), "game_over": False}
        
        if role == "detective" and self.phase == "night" and text.startswith("افحص "):
            target = text.replace("افحص ", "").strip()
            for uid, p in self.players.items():
                if p["name"] == target and p["alive"] and uid != user_id:
                    result = "هذا الشخص هو المافيا" if p["role"] == "mafia" else "هذا الشخص بريء"
                    return {"response": TextMessage(text=f"نتيجة الفحص: {target} - {result}"), "game_over": False}
            return {"response": TextMessage(text="اسم اللاعب غير صحيح او اللاعب ميت"), "game_over": False}
        
        if role == "doctor" and self.phase == "night" and text.startswith("احمي "):
            target = text.replace("احمي ", "").strip()
            if target == "نفسي":
                self.night_actions["doctor_target"] = user_id
                return {"response": TextMessage(text="تم حماية نفسك"), "game_over": False}
            for uid, p in self.players.items():
                if p["name"] == target and p["alive"]:
                    self.night_actions["doctor_target"] = uid
                    return {"response": TextMessage(text=f"تم حماية {target}"), "game_over": False}
            return {"response": TextMessage(text="اسم اللاعب غير صحيح او اللاعب ميت"), "game_over": False}
        
        return None

    def add_player(self, user_id, name):
        if self.phase != "registration":
            return {"response": TextMessage(text="اللعبة بدات بالفعل"), "game_over": False}
        if user_id in self.players:
            return {"response": TextMessage(text="انت مسجل بالفعل"), "game_over": False}
        
        self.players[user_id] = {"name": name, "role": None, "alive": True}
        logger.info(f"Player joined: {name}")
        return {"response": self.registration_flex(), "game_over": False}

    def assign_roles(self):
        if len(self.players) < 4:
            return {"response": TextMessage(text="نحتاج 4 لاعبين على الاقل"), "game_over": False}
        
        roles = ["mafia", "detective", "doctor"] + ["citizen"] * (len(self.players) - 3)
        random.shuffle(roles)
        
        for uid, role in zip(self.players.keys(), roles):
            self.players[uid]["role"] = role
            logger.info(f"Role assigned: {uid} -> {role}")
        
        self.phase = "night"
        self.day = 1
        logger.info(f"Roles assigned to {len(self.players)} players")
        
        return {
            "response": [
                TextMessage(text="تم توزيع الادوار - تحقق من رسائلك الخاصة لمعرفة دورك"),
                self.night_flex()
            ],
            "game_over": False
        }

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
        
        return {"response": [TextMessage(text=msg), self.day_flex()], "game_over": False}

    def vote(self, user_id, target_name):
        if self.phase != "voting":
            return {"response": TextMessage(text="ليس وقت التصويت الان"), "game_over": False}
        
        if user_id not in self.players or not self.players[user_id]["alive"]:
            return {"response": TextMessage(text="لا يمكنك التصويت"), "game_over": False}
        
        target_id = None
        for uid, p in self.players.items():
            if p["name"] == target_name and p["alive"]:
                target_id = uid
                break
        
        if not target_id:
            return {"response": TextMessage(text="اللاعب غير موجود او ميت"), "game_over": False}
        
        self.votes[user_id] = target_id
        return {"response": TextMessage(text=f"تم تسجيل صوتك ضد {target_name}"), "game_over": False}

    def end_voting(self):
        if self.phase != "voting":
            return {"response": TextMessage(text="ليس وقت التصويت"), "game_over": False}
        
        if not self.votes:
            return {"response": TextMessage(text="لم يصوت احد"), "game_over": False}
        
        vote_counts = {}
        for target_id in self.votes.values():
            vote_counts[target_id] = vote_counts.get(target_id, 0) + 1
        
        max_votes = max(vote_counts.values())
        most_voted = [uid for uid, count in vote_counts.items() if count == max_votes]
        
        if len(most_voted) > 1:
            msg = "تعادل في الاصوات - لم يتم اعدام احد"
        else:
            executed_id = most_voted[0]
            self.players[executed_id]["alive"] = False
            executed_name = self.players[executed_id]["name"]
            executed_role = self.ROLE_INFO[self.players[executed_id]["role"]]["title"]
            msg = f"تم اعدام {executed_name} - كان دوره: {executed_role}"
        
        self.votes.clear()
        self.phase = "night"
        self.day += 1
        
        winner = self.check_winner()
        if winner:
            return winner
        
        return {"response": [TextMessage(text=msg), self.night_flex()], "game_over": False}

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
