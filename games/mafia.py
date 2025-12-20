import random
import logging
from linebot.v3.messaging import FlexMessage, FlexContainer, QuickReply, QuickReplyItem, MessageAction
from config import Config
from ui import UI

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
        self.supports_hint = False
        self.supports_reveal = False
        
    def _c(self):
        return UI.get_theme(self.theme)
    
    def _qr(self):
        items = ["الحالة", "شرح", "بداية", "العاب", "مساعدة"]
        return QuickReply(items=[QuickReplyItem(action=MessageAction(label=i, text=i)) for i in items])
    
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
            body.append({"type": "separator", "margin": "lg", "color": c["border"]})
            body.extend(buttons)
        
        body.append({
            "type": "text",
            "text": "Bot Mesh | 2025",
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
    
    def _glass_box(self, contents, padding="16px", margin="lg"):
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
    
    def _button(self, label, text):
        c = self._c()
        return {
            "type": "button",
            "action": {"type": "message", "label": label, "text": text},
            "style": "secondary",
            "color": c["button"],
            "height": "sm"
        }
    
    def help_screen(self):
        c = self._c()
        contents = [
            self._glass_box([
                {"type": "text", "text": "كيف تلعب المافيا؟", "weight": "bold", "color": c["text"], "size": "md", "align": "center"},
                {"type": "separator", "margin": "md", "color": c["border"]},
                {"type": "text", "text": "1. اكتب: انضم مافيا للتسجيل", "size": "sm", "color": c["text"], "margin": "md", "wrap": True},
                {"type": "text", "text": "2. يجب 4 لاعبين على الاقل", "size": "sm", "color": c["text"], "margin": "xs", "wrap": True},
                {"type": "text", "text": "3. اكتب: بدء مافيا لبدء اللعبة", "size": "sm", "color": c["text"], "margin": "xs", "wrap": True}
            ]),
            self._glass_box([
                {"type": "text", "text": "في القروب:", "weight": "bold", "color": c["text"], "size": "sm"},
                {"type": "text", "text": "- التسجيل والتصويت", "size": "xs", "color": c["text_secondary"], "margin": "xs", "wrap": True},
                {"type": "text", "text": "- النقاش بين اللاعبين", "size": "xs", "color": c["text_secondary"], "margin": "xs", "wrap": True},
                {"type": "text", "text": "- مشاهدة من مات", "size": "xs", "color": c["text_secondary"], "margin": "xs", "wrap": True}
            ]),
            self._glass_box([
                {"type": "text", "text": "في الخاص:", "weight": "bold", "color": c["text"], "size": "sm"},
                {"type": "text", "text": "- ستعرف دورك (مافيا/محقق/طبيب/مواطن)", "size": "xs", "color": c["text_secondary"], "margin": "xs", "wrap": True},
                {"type": "text", "text": "- المافيا: اختر من تقتل ليلا", "size": "xs", "color": c["text_secondary"], "margin": "xs", "wrap": True},
                {"type": "text", "text": "- المحقق: اسأل عن اي لاعب", "size": "xs", "color": c["text_secondary"], "margin": "xs", "wrap": True},
                {"type": "text", "text": "- الطبيب: اختر من تحمي", "size": "xs", "color": c["text_secondary"], "margin": "xs", "wrap": True}
            ]),
            self._glass_box([
                {"type": "text", "text": "ملاحظة مهمة", "weight": "bold", "color": "#DC2626", "size": "sm", "align": "center"},
                {"type": "text", "text": "يجب اضافة البوت كصديق ليصلك دورك في الخاص", "size": "xs", "color": c["text"], "margin": "xs", "wrap": True, "align": "center"}
            ])
        ]
        
        action_buttons = [
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    self._button("انضم", "انضم مافيا"),
                    self._button("بدء", "بدء مافيا")
                ],
                "spacing": "sm",
                "margin": "md"
            }
        ]
        
        return self._create_bubble("شرح لعبة المافيا", contents, action_buttons)
    
    def registration_screen(self):
        c = self._c()
        contents = [
            self._glass_box([
                {"type": "text", "text": f"اللاعبون المسجلون: {len(self.players)}", "size": "md", "color": c["text"], "weight": "bold", "align": "center"},
                {"type": "text", "text": f"الحد الادنى: {self.MIN_PLAYERS} - الحد الاقصى: {self.MAX_PLAYERS}", "size": "xs", "color": c["text_secondary"], "align": "center", "margin": "sm"}
            ], "20px")
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
        
        contents.append(self._glass_box([
            {"type": "text", "text": "ملاحظة: يجب اضافة البوت كصديق", "size": "xs", "color": "#DC2626", "align": "center", "wrap": True}
        ], "12px", "md"))
        
        action_buttons = [
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    self._button("انضم", "انضم مافيا"),
                    self._button("بدء", "بدء مافيا"),
                    self._button("شرح", "شرح")
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
            from linebot.v3.messaging import TextMessage
            return TextMessage(text="حدث خطأ في بدء اللعبة")
    
    def add_player(self, user_id):
        try:
            from linebot.v3.messaging import TextMessage
            
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
            from linebot.v3.messaging import TextMessage
            return {"response": TextMessage(text="حدث خطأ"), "game_over": False}
    
    def assign_roles(self):
        try:
            from linebot.v3.messaging import TextMessage
            
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
            
            message = f"بدأت اللعبة!\nعدد اللاعبين: {num_players}\nعدد المافيا: {num_mafia}\n\nالمرحلة: الليل\n\nتحقق من رسائلك الخاصة لمعرفة دورك!"
            return {"response": TextMessage(text=message), "game_over": False}
        except Exception as e:
            logger.error(f"Error in assign_roles: {e}")
            from linebot.v3.messaging import TextMessage
            return {"response": TextMessage(text="حدث خطأ"), "game_over": False}
    
    def get_status(self):
        c = self._c()
        
        alive_names = [self.players[uid]["name"] for uid in self.alive_players]
        dead_names = [self.players[uid]["name"] for uid in self.dead_players]
        
        contents = [
            self._glass_box([
                {"type": "text", "text": f"المرحلة: {self.phase}", "size": "md", "color": c["text"], "align": "center"},
                {"type": "text", "text": f"اليوم: {self.day}", "size": "sm", "color": c["text_secondary"], "align": "center", "margin": "xs"}
            ], "16px")
        ]
        
        if alive_names:
            alive_list = [{"type": "text", "text": f"- {name}", "size": "sm", "color": c["text"], "margin": "xs"} for name in alive_names]
            contents.append(self._glass_box([{"type": "text", "text": "الاحياء:", "size": "sm", "color": c["text"], "weight": "bold"}] + alive_list, "12px", "md"))
        
        if dead_names:
            dead_list = [{"type": "text", "text": f"- {name}", "size": "sm", "color": c["text_tertiary"], "margin": "xs"} for name in dead_names]
            contents.append(self._glass_box([{"type": "text", "text": "الموتى:", "size": "sm", "color": c["text_tertiary"], "weight": "bold"}] + dead_list, "12px", "md"))
        
        return self._create_bubble("حالة اللعبة", contents, None)
    
    def check(self, text, user_id):
        try:
            cmd = Config.normalize(text)
            
            if cmd == "شرح":
                return {"response": self.help_screen(), "game_over": False}
            
            if self.phase == "registration":
                if cmd == "انضم مافيا":
                    return self.add_player(user_id)
                elif cmd == "بدء مافيا":
                    return self.assign_roles()
                elif cmd in ("الحاله", "الحالة", "حالة"):
                    return {"response": self.get_status(), "game_over": False}
            
            return None
        except Exception as e:
            logger.error(f"Error in check: {e}")
            return None
    
    def check_answer(self, answer):
        return False
