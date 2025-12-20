import random
import logging
from linebot.v3.messaging import FlexMessage, FlexContainer, QuickReply, QuickReplyItem, MessageAction, TextMessage
from config import Config

logger = logging.getLogger(__name__)

class MafiaGame:
    MIN_PLAYERS = 4
    MAX_PLAYERS = 12
    
    def __init__(self, db, theme="light"):
        self.db = db
        self.theme = theme
        self.game_name = "مافيا"
        self.players = {}
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
        self.voted_players = []
        
    def _c(self):
        return Config.get_theme(self.theme)
    
    def _qr(self):
        items = ["سؤال", "منشن", "تحدي", "اعتراف", "شخصية", "حكمة", "موقف", "بداية", "العاب", "مساعدة"]
        return QuickReply(items=[QuickReplyItem(action=MessageAction(label=i, text=i)) for i in items])
    
    def _separator(self, margin="md"):
        c = self._c()
        return {"type": "separator", "margin": margin, "color": c["border"]}
    
    def _glass_box(self, contents, padding="16px", margin="none"):
        c = self._c()
        return {
            "type": "box",
            "layout": "vertical",
            "contents": contents,
            "backgroundColor": c["card"],
            "cornerRadius": "12px",
            "paddingAll": padding,
            "spacing": "sm",
            "margin": margin
        }
    
    def _create_bubble(self, title, contents, buttons=None):
        c = self._c()
        body = [
            {"type": "text", "text": "Bot Mesh", "size": "xxl", "weight": "bold", "color": c["text"], "align": "center"},
            {"type": "separator", "margin": "lg", "color": c["border"]},
            {"type": "text", "text": title, "size": "lg", "weight": "bold", "color": c["text"], "align": "center", "margin": "lg"},
            {"type": "separator", "margin": "lg", "color": c["border"]}
        ]
        body.extend(contents)
        
        if buttons:
            body.append(self._separator("lg"))
            body.extend(buttons)
        
        body.append({
            "type": "text",
            "text": "Bot Mesh | 2025 عبير الدوسري",
            "size": "xxs",
            "color": c["text_secondary"],
            "align": "center",
            "margin": "lg"
        })
        
        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": body,
                "backgroundColor": c["bg"],
                "paddingAll": "24px"
            }
        }
        return FlexMessage(alt_text=title, contents=FlexContainer.from_dict(bubble), quickReply=self._qr())
    
    def registration_screen(self):
        c = self._c()
        contents = [
            self._glass_box([
                {"type": "text", "text": f"اللاعبون المسجلون: {len(self.players)}", "size": "md", "color": c["text"], "weight": "bold", "align": "center"},
                {"type": "text", "text": f"الحد الادنى: {self.MIN_PLAYERS} - الحد الاقصى: {self.MAX_PLAYERS}", "size": "xs", "color": c["text_secondary"], "align": "center", "margin": "sm"}
            ], "20px", "lg")
        ]
        
        if self.players:
            player_list = []
            for uid, pdata in list(self.players.items())[:10]:
                player_list.append({
                    "type": "text",
                    "text": f"- {pdata['name']}",
                    "size": "sm",
                    "color": c["text"],
                    "margin": "xs"
                })
            contents.append(self._glass_box(player_list, "12px", "md"))
        
        action_buttons = [
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {"type": "button", "action": {"type": "message", "label": "انضم", "text": "انضم مافيا"}, "style": "secondary", "color": c["button"], "height": "sm", "flex": 1},
                    {"type": "button", "action": {"type": "message", "label": "بدء", "text": "بدء مافيا"}, "style": "secondary", "color": c["button"], "height": "sm", "flex": 1}
                ],
                "spacing": "sm",
                "margin": "md"
            }
        ]
        
        return self._create_bubble("لعبة المافيا - التسجيل", contents, action_buttons)
    
    def start(self, user_id):
        try:
            self.phase = "registration"
            self.game_active = True
            self.players = {}
            self.alive_players = []
            self.dead_players = []
            self.day = 0
            self.votes = {}
            self.night_actions = {}
            self.mafia_list = []
            self.detective = None
            self.doctor = None
            self.voted_players = []
            return self.registration_screen()
        except Exception as e:
            logger.error(f"Error in start: {e}")
            return TextMessage(text="حدث خطأ في بدء اللعبة")
    
    def add_player(self, user_id):
        try:
            c = self._c()
            
            if self.phase != "registration":
                return {"response": TextMessage(text="التسجيل مغلق الان"), "game_over": False}
            
            if user_id in self.players:
                return {"response": TextMessage(text="انت مسجل بالفعل"), "game_over": False}
            
            if len(self.players) >= self.MAX_PLAYERS:
                return {"response": TextMessage(text="اللعبة ممتلئة"), "game_over": False}
            
            user = self.db.get_user(user_id)
            name = user["name"] if user else f"لاعب{len(self.players)+1}"
            self.players[user_id] = {"name": name, "role": None, "alive": True}
            
            return {"response": self.registration_screen(), "game_over": False}
        except Exception as e:
            logger.error(f"Error in add_player: {e}")
            return {"response": TextMessage(text="حدث خطأ"), "game_over": False}
    
    def assign_roles(self):
        try:
            c = self._c()
            
            if len(self.players) < self.MIN_PLAYERS:
                return {"response": TextMessage(text=f"يجب {self.MIN_PLAYERS} لاعبين على الاقل"), "game_over": False}
            
            num_players = len(self.players)
            num_mafia = max(1, num_players // 4)
            
            roles = ["mafia"] * num_mafia + ["detective", "doctor"] + ["citizen"] * (num_players - num_mafia - 2)
            random.shuffle(roles)
            
            for uid, role in zip(list(self.players.keys()), roles):
                self.players[uid]["role"] = role
                if role == "mafia":
                    self.mafia_list.append(uid)
                elif role == "detective":
                    self.detective = uid
                elif role == "doctor":
                    self.doctor = uid
            
            self.alive_players = list(self.players.keys())
            self.phase = "night"
            self.day = 1
            
            message = f"بدأت اللعبة!\nعدد اللاعبين: {num_players}\nعدد المافيا: {num_mafia}\n\nالمرحلة: الليل"
            return {"response": TextMessage(text=message), "game_over": False}
        except Exception as e:
            logger.error(f"Error in assign_roles: {e}")
            return {"response": TextMessage(text="حدث خطأ"), "game_over": False}
    
    def check(self, text, user_id):
        try:
            cmd = Config.normalize(text)
            
            if self.phase == "registration":
                if cmd == "انضم مافيا":
                    return self.add_player(user_id)
                elif cmd == "بدء مافيا":
                    return self.assign_roles()
                elif cmd in ("الحاله", "الحالة", "حالة"):
                    return {"response": self.get_status(), "game_over": False}
            
            elif self.phase == "voting":
                if cmd.startswith("صوت "):
                    target_name = text[4:].strip()
                    return self.cast_vote(user_id, target_name)
            
            elif self.phase == "night":
                return self.night_phase_action(user_id, text)
            
            return None
        except Exception as e:
            logger.error(f"Error in check: {e}")
            return None
    
    def get_status(self):
        c = self._c()
        
        alive_names = [self.players[uid]["name"] for uid in self.alive_players]
        dead_names = [self.players[uid]["name"] for uid in self.dead_players]
        
        contents = [
            self._glass_box([
                {"type": "text", "text": f"المرحلة: {self.phase}", "size": "md", "color": c["text"], "align": "center"},
                {"type": "text", "text": f"اليوم: {self.day}", "size": "sm", "color": c["text_secondary"], "align": "center", "margin": "xs"}
            ], "16px", "lg")
        ]
        
        if alive_names:
            alive_list = [{"type": "text", "text": f"- {name}", "size": "sm", "color": c["text"], "margin": "xs"} for name in alive_names]
            contents.append(self._glass_box([{"type": "text", "text": "الاحياء:", "size": "sm", "color": c["text"], "weight": "bold"}] + alive_list, "12px", "md"))
        
        if dead_names:
            dead_list = [{"type": "text", "text": f"- {name}", "size": "sm", "color": c["text_tertiary"], "margin": "xs"} for name in dead_names]
            contents.append(self._glass_box([{"type": "text", "text": "الموتى:", "size": "sm", "color": c["text_tertiary"], "weight": "bold"}] + dead_list, "12px", "md"))
        
        return self._create_bubble("حالة اللعبة", contents, None)
    
    def night_phase_action(self, user_id, text):
        try:
            if user_id not in self.alive_players:
                return None
            
            role = self.players[user_id]["role"]
            
            if role == "mafia":
                target_name = text.strip()
                if target_name in [self.players[uid]["name"] for uid in self.alive_players if uid != user_id]:
                    self.night_actions.setdefault("mafia_targets", []).append(target_name)
                    return {"response": TextMessage(text=f"تم اختيار {target_name}"), "game_over": False}
            
            elif role == "detective":
                target_name = text.strip()
                for uid, pdata in self.players.items():
                    if pdata["name"] == target_name:
                        role_name = "مافيا" if pdata["role"] == "mafia" else "مواطن"
                        return {"response": TextMessage(text=f"{target_name} هو {role_name}"), "game_over": False}
            
            elif role == "doctor":
                target_name = text.strip()
                if target_name in [self.players[uid]["name"] for uid in self.alive_players]:
                    self.night_actions["doctor_target"] = target_name
                    return {"response": TextMessage(text=f"تم حماية {target_name}"), "game_over": False}
            
            return None
        except Exception as e:
            logger.error(f"Error in night_phase_action: {e}")
            return None
    
    def cast_vote(self, user_id, target_name):
        try:
            if user_id not in self.alive_players or user_id in self.voted_players:
                return None
            
            if target_name not in [self.players[uid]["name"] for uid in self.alive_players if uid != user_id]:
                return {"response": TextMessage(text="لاعب غير صالح"), "game_over": False}
            
            self.votes[user_id] = target_name
            self.voted_players.append(user_id)
            
            if len(self.votes) >= len(self.alive_players):
                return self.resolve_voting()
            
            return {"response": TextMessage(text=f"تم التصويت على {target_name}"), "game_over": False}
        except Exception as e:
            logger.error(f"Error in cast_vote: {e}")
            return None
    
    def resolve_voting(self):
        try:
            counts = {}
            for target in self.votes.values():
                counts[target] = counts.get(target, 0) + 1
            
            max_votes = max(counts.values())
            voted_out = random.choice([name for name, count in counts.items() if count == max_votes])
            
            for uid, pdata in self.players.items():
                if pdata["name"] == voted_out:
                    self.players[uid]["alive"] = False
                    self.alive_players.remove(uid)
                    self.dead_players.append(uid)
                    eliminated_role = pdata["role"]
                    break
            
            self.votes = {}
            self.voted_players = []
            self.day += 1
            self.phase = "night"
            
            winner = self.check_win()
            if winner:
                return self.end_game(winner)
            
            message = f"{voted_out} خرج من اللعبة\nالدور: {eliminated_role}"
            return {"response": TextMessage(text=message), "game_over": False}
        except Exception as e:
            logger.error(f"Error in resolve_voting: {e}")
            return None
    
    def check_win(self):
        mafia_alive = [uid for uid in self.mafia_list if self.players[uid]["alive"]]
        citizens_alive = [uid for uid in self.alive_players if uid not in self.mafia_list]
        
        if not mafia_alive:
            return "المواطنين"
        if len(mafia_alive) >= len(citizens_alive):
            return "المافيا"
        return None
    
    def end_game(self, winner):
        try:
            c = self._c()
            
            result_list = []
            for uid, pdata in self.players.items():
                status = "حي" if pdata["alive"] else "ميت"
                result_list.append({
                    "type": "text",
                    "text": f"{pdata['name']} - {pdata['role']} - {status}",
                    "size": "sm",
                    "color": c["text"] if pdata["alive"] else c["text_tertiary"],
                    "margin": "xs"
                })
            
            contents = [
                self._glass_box([
                    {"type": "text", "text": f"الفائز: {winner}", "size": "lg", "color": c["text"], "weight": "bold", "align": "center"}
                ], "16px", "lg"),
                self._glass_box(result_list, "12px", "md")
            ]
            
            self.phase = "finished"
            self.game_active = False
            
            return {"response": self._create_bubble("انتهت اللعبة", contents, None), "game_over": True}
        except Exception as e:
            logger.error(f"Error in end_game: {e}")
            return {"response": TextMessage(text="انتهت اللعبة"), "game_over": True}
