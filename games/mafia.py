import random
import logging
from linebot.v3.messaging import FlexMessage, FlexContainer, QuickReply, QuickReplyItem, MessageAction
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

    def _c(self):
        return Config.get_theme(self.theme)
    
    def _qr(self):
        items = ["سؤال", "منشن", "تحدي", "اعتراف", "شخصية", "حكمة", "موقف", "بداية", "العاب", "مساعدة"]
        return QuickReply(items=[QuickReplyItem(action=MessageAction(label=i, text=i)) for i in items])

    def _separator(self, margin="md"):
        return {"type": "separator", "margin": margin}

    def _glass_box(self, contents, padding="16px", margin="none"):
        c = self._c()
        bg_color = c["card_secondary"] if self.theme == "light" else "#1A202C"
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

    def _create_bubble(self, title, contents, buttons=None):
        c = self._c()
        
        body_contents = [
            {
                "type": "text",
                "text": title,
                "size": "xl",
                "weight": "bold",
                "color": c["primary"],
                "align": "center"
            },
            self._separator("lg")
        ]
        
        body_contents.extend(contents)
        
        if buttons:
            body_contents.append(self._separator("lg"))
            body_contents.extend(buttons)
        
        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": body_contents,
                "backgroundColor": c["card"],
                "paddingAll": "24px"
            }
        }
        
        return FlexMessage(
            alt_text=title,
            contents=FlexContainer.from_dict(bubble),
            quickReply=self._qr()
        )

    def registration_screen(self):
        c = self._c()
        
        contents = [
            self._glass_box([
                {
                    "type": "text",
                    "text": f"اللاعبون المسجلون: {len(self.players)}",
                    "size": "md",
                    "color": c["text"],
                    "weight": "bold",
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": f"الحد الأدنى: {self.MIN_PLAYERS} لاعبين",
                    "size": "xs",
                    "color": c["text_secondary"],
                    "align": "center",
                    "margin": "sm"
                },
                {
                    "type": "text",
                    "text": f"الحد الأقصى: {self.MAX_PLAYERS} لاعبين",
                    "size": "xs",
                    "color": c["text_tertiary"],
                    "align": "center",
                    "margin": "xs"
                }
            ], "20px", "lg")
        ]
        
        if self.players:
            player_names = [p["name"] for p in self.players.values()]
            contents.append(
                self._glass_box([
                    {
                        "type": "text",
                        "text": "اللاعبون:",
                        "size": "sm",
                        "color": c["text_secondary"],
                        "weight": "bold"
                    },
                    {
                        "type": "text",
                        "text": " - " + "\n - ".join(player_names),
                        "size": "xs",
                        "color": c["text"],
                        "wrap": True,
                        "margin": "sm"
                    }
                ], "12px", "md")
            )
        
        buttons = [
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "button",
                        "action": {"type": "message", "label": "انضم", "text": "انضم مافيا"},
                        "style": "primary",
                        "color": c["button_primary"],
                        "height": "sm",
                        "flex": 1
                    },
                    {
                        "type": "button",
                        "action": {"type": "message", "label": "بدء اللعبة", "text": "بدء مافيا"},
                        "style": "primary",
                        "color": c["button_primary"],
                        "height": "sm",
                        "flex": 1
                    }
                ],
                "spacing": "sm",
                "margin": "md"
            }
        ]
        
        return self._create_bubble("تسجيل المافيا", contents, buttons)

    def instructions_screen(self):
        c = self._c()
        
        contents = [
            self._glass_box([
                {
                    "type": "text",
                    "text": "طريقة اللعب",
                    "size": "md",
                    "color": c["text"],
                    "weight": "bold"
                },
                {
                    "type": "text",
                    "text": "• في القروب: النقاش والتصويت\n• المافيا: يختار ضحية\n• المحقق: يسأل عن لاعب\n• الطبيب: يحمي لاعبا\n• المواطن: يصوت ويناقش",
                    "size": "xs",
                    "color": c["text_secondary"],
                    "wrap": True,
                    "margin": "sm"
                }
            ], "16px", "lg")
        ]
        
        return self._create_bubble("شرح المافيا", contents, None)

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
            
            return self.registration_screen()
        except Exception as e:
            logger.error(f"Error in MafiaGame.start: {e}")
            from linebot.v3.messaging import TextMessage
            return TextMessage(text="حدث خطأ في بدء لعبة المافيا. حاول مرة أخرى.")

    def check(self, text, user_id):
        try:
            cmd = Config.normalize(text)

            if self.phase == "registration":
                if cmd == "انضم مافيا":
                    return self.add_player(user_id)
                elif cmd == "بدء مافيا":
                    return self.assign_roles()
                elif cmd in ("الحاله", "الحالة"):
                    return {"response": self.registration_screen(), "game_over": False}
                elif cmd == "شرح":
                    return {"response": self.instructions_screen(), "game_over": False}

            elif self.phase == "voting":
                if cmd.startswith("صوت "):
                    name = text[4:].strip()
                    return self.cast_vote(user_id, name)
                elif cmd in ("الحاله", "الحالة"):
                    return {"response": self.game_status_screen(), "game_over": False}

            return None
        except Exception as e:
            logger.error(f"Error in MafiaGame.check: {e}")
            return None

    def add_player(self, user_id):
        try:
            c = self._c()
            
            if self.phase != "registration":
                return {
                    "response": self._create_bubble("خطأ", [
                        self._glass_box([{
                            "type": "text",
                            "text": "التسجيل مغلق",
                            "size": "md",
                            "color": c["text"],
                            "align": "center"
                        }], "16px", "lg")
                    ], None),
                    "game_over": False
                }
            
            if user_id in self.players:
                return {
                    "response": self._create_bubble("خطأ", [
                        self._glass_box([{
                            "type": "text",
                            "text": "أنت مسجل بالفعل",
                            "size": "md",
                            "color": c["text"],
                            "align": "center"
                        }], "16px", "lg")
                    ], None),
                    "game_over": False
                }
            
            if len(self.players) >= self.MAX_PLAYERS:
                return {
                    "response": self._create_bubble("خطأ", [
                        self._glass_box([{
                            "type": "text",
                            "text": "اللعبة ممتلئة",
                            "size": "md",
                            "color": c["text"],
                            "align": "center"
                        }], "16px", "lg")
                    ], None),
                    "game_over": False
                }

            user = self.db.get_user(user_id)
            name = user["name"] if user else f"لاعب{len(self.players)+1}"
            self.players[user_id] = {"name": name, "role": None, "alive": True}
            
            return {"response": self.registration_screen(), "game_over": False}
        except Exception as e:
            logger.error(f"Error in add_player: {e}")
            return None

    def assign_roles(self):
        try:
            c = self._c()
            
            if len(self.players) < self.MIN_PLAYERS:
                return {
                    "response": self._create_bubble("خطأ", [
                        self._glass_box([{
                            "type": "text",
                            "text": f"يجب {self.MIN_PLAYERS} لاعبين على الأقل",
                            "size": "md",
                            "color": c["text"],
                            "align": "center"
                        }], "16px", "lg")
                    ], None),
                    "game_over": False
                }

            num_players = len(self.players)
            num_mafia = max(1, num_players // 4)
            
            roles = ["mafia"] * num_mafia + ["detective", "doctor"]
            roles += ["citizen"] * (num_players - len(roles))
            random.shuffle(roles)

            player_ids = list(self.players.keys())
            for uid, role in zip(player_ids, roles):
                self.players[uid]["role"] = role
                if role == "mafia":
                    self.mafia_list.append(uid)
                elif role == "detective":
                    self.detective = uid
                elif role == "doctor":
                    self.doctor = uid

            self.alive_players = player_ids.copy()
            self.phase = "night"
            self.day = 1

            response = self._create_bubble("بدأت اللعبة", [
                self._glass_box([{
                    "type": "text",
                    "text": f"تم توزيع الأدوار\n{num_mafia} مافيا في اللعبة",
                    "size": "md",
                    "color": c["text"],
                    "align": "center",
                    "wrap": True
                }], "16px", "lg")
            ], None)
            
            return {"response": response, "game_over": False}
        except Exception as e:
            logger.error(f"Error in assign_roles: {e}")
            return None

    def game_status_screen(self):
        c = self._c()
        
        alive = [self.players[uid]["name"] for uid in self.alive_players]
        dead = [self.players[uid]["name"] for uid in self.dead_players]
        
        contents = [
            self._glass_box([
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": f"{self.day}",
                                    "size": "xl",
                                    "weight": "bold",
                                    "color": c["primary"],
                                    "align": "center"
                                },
                                {
                                    "type": "text",
                                    "text": "اليوم",
                                    "size": "xs",
                                    "color": c["text_secondary"],
                                    "align": "center"
                                }
                            ],
                            "flex": 1
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": self.phase,
                                    "size": "md",
                                    "weight": "bold",
                                    "color": c["text"],
                                    "align": "center"
                                },
                                {
                                    "type": "text",
                                    "text": "المرحلة",
                                    "size": "xs",
                                    "color": c["text_secondary"],
                                    "align": "center"
                                }
                            ],
                            "flex": 1
                        }
                    ]
                }
            ], "16px", "lg")
        ]
        
        if alive:
            contents.append(
                self._glass_box([
                    {
                        "type": "text",
                        "text": f"الأحياء ({len(alive)}):",
                        "size": "sm",
                        "color": c["text"],
                        "weight": "bold"
                    },
                    {
                        "type": "text",
                        "text": " - " + "\n - ".join(alive),
                        "size": "xs",
                        "color": c["text"],
                        "wrap": True,
                        "margin": "sm"
                    }
                ], "12px", "md")
            )
        
        if dead:
            contents.append(
                self._glass_box([
                    {
                        "type": "text",
                        "text": f"الموتى ({len(dead)}):",
                        "size": "sm",
                        "color": c["text_secondary"],
                        "weight": "bold"
                    },
                    {
                        "type": "text",
                        "text": " - " + "\n - ".join(dead),
                        "size": "xs",
                        "color": c["text"],
                        "wrap": True,
                        "margin": "sm"
                    }
                ], "12px", "md")
            )
        
        return self._create_bubble("حالة اللعبة", contents, None)

    def cast_vote(self, user_id, target_name):
        try:
            if user_id not in self.alive_players:
                return None
            
            target_id = None
            for uid in self.alive_players:
                if Config.normalize(self.players[uid]["name"]) == Config.normalize(target_name):
                    target_id = uid
                    break
            
            if not target_id:
                return None
            
            self.votes[user_id] = target_id
            
            if len(self.votes) >= len(self.alive_players):
                return self.process_votes()
            
            c = self._c()
            response = self._create_bubble("تم التصويت", [
                self._glass_box([{
                    "type": "text",
                    "text": f"صوتك تم احتسابه\nعدد الأصوات: {len(self.votes)}/{len(self.alive_players)}",
                    "size": "md",
                    "color": c["text"],
                    "align": "center",
                    "wrap": True
                }], "16px", "lg")
            ], None)
            
            return {"response": response, "game_over": False}
        except Exception as e:
            logger.error(f"Error in cast_vote: {e}")
            return None

    def process_votes(self):
        try:
            vote_count = {}
            for target_id in self.votes.values():
                vote_count[target_id] = vote_count.get(target_id, 0) + 1
            
            if vote_count:
                eliminated = max(vote_count, key=vote_count.get)
                self.alive_players.remove(eliminated)
                self.dead_players.append(eliminated)
                self.players[eliminated]["alive"] = False
                
                eliminated_name = self.players[eliminated]["name"]
                eliminated_role = self.players[eliminated]["role"]
            else:
                eliminated_name = None
                eliminated_role = None
            
            self.votes = {}
            
            winner = self.check_winner()
            if winner:
                return {"response": self.game_over_screen(winner), "game_over": True}
            
            self.day += 1
            self.phase = "day"
            
            c = self._c()
            if eliminated_name:
                role_text = {
                    "mafia": "مافيا",
                    "detective": "محقق",
                    "doctor": "طبيب",
                    "citizen": "مواطن"
                }.get(eliminated_role, eliminated_role)
                
                response = self._create_bubble("نتيجة التصويت", [
                    self._glass_box([{
                        "type": "text",
                        "text": f"تم إقصاء: {eliminated_name}\nالدور: {role_text}",
                        "size": "md",
                        "color": c["text"],
                        "align": "center",
                        "wrap": True
                    }], "16px", "lg")
                ], None)
            else:
                response = self.game_status_screen()
            
            return {"response": response, "game_over": False}
        except Exception as e:
            logger.error(f"Error in process_votes: {e}")
            return None

    def check_winner(self):
        mafia_alive = sum(1 for uid in self.alive_players if self.players[uid]["role"] == "mafia")
        citizens_alive = len(self.alive_players) - mafia_alive
        
        if mafia_alive == 0:
            return "citizens"
        elif mafia_alive >= citizens_alive:
            return "mafia"
        return None

    def game_over_screen(self, winner):
        c = self._c()
        
        winner_text = "فاز المواطنون" if winner == "citizens" else "فازت المافيا"
        winner_color = c["text"] if winner == "citizens" else c["text_secondary"]
        
        contents = [
            {
                "type": "text",
                "text": winner_text,
                "size": "xxl",
                "weight": "bold",
                "color": winner_color,
                "align": "center"
            },
            self._glass_box([
                {
                    "type": "text",
                    "text": "ملخص اللعبة",
                    "size": "md",
                    "color": c["text"],
                    "weight": "bold",
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": f"عدد الأيام: {self.day}\nعدد اللاعبين: {len(self.players)}",
                    "size": "sm",
                    "color": c["text_secondary"],
                    "align": "center",
                    "margin": "sm"
                }
            ], "16px", "lg")
        ]
        
        buttons = [
            {
                "type": "button",
                "action": {"type": "message", "label": "لعب مرة اخرى", "text": "مافيا"},
                "style": "primary",
                "color": c["button_primary"],
                "height": "sm",
                "margin": "md"
            }
        ]
        
        return self._create_bubble("انتهت اللعبة", contents, buttons)
