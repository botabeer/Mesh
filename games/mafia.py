import random
import logging
from linebot.v3.messaging import FlexMessage, FlexContainer
from config import Config

logger = logging.getLogger(__name__)


class MafiaGame:
    ROLE_INFO = {
        "mafia": {"title": "المافيا", "desc": "اقتل شخص كل ليلة", "color": "#8B0000"},
        "detective": {"title": "المحقق", "desc": "افحص شخص كل ليلة", "color": "#1E90FF"},
        "doctor": {"title": "الدكتور", "desc": "احم شخص كل ليلة", "color": "#32CD32"},
        "citizen": {"title": "مواطن", "desc": "ناقش وصوت", "color": "#808080"}
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
        self.game_name = "مافيا"
        self.user_id = None

    def _c(self):
        return Config.get_theme(self.theme)

    def _create_bubble(self, title, texts, buttons=None):
        c = self._c()
        contents = [{
            "type": "text", "text": title, "weight": "bold",
            "size": "xl", "color": c['primary'], "align": "center"
        }]
        
        for t in texts:
            contents.append({
                "type": "text", "text": t, "size": "sm",
                "color": c['text'], "wrap": True, "margin": "md"
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
            {"type": "button", "action": {"type": "message", "label": "انضم", "text": "انضم_مافيا"},
             "style": "primary", "color": c['primary'], "height": "sm", "margin": "md"},
            {"type": "button", "action": {"type": "message", "label": "بدء", "text": "بدء_مافيا"},
             "style": "secondary", "height": "sm", "margin": "sm"}
        ]
        return self._create_bubble(
            "لعبة المافيا",
            [f"اللاعبون: {len(self.players)}", "الحد الادنى: 4 لاعبين"],
            buttons
        )

    def start(self, user_id: str):
        self.phase = "registration"
        self.game_active = True
        self.user_id = user_id
        return self.registration_flex()

    def check(self, text: str, user_id: str):
        cmd = Config.normalize(text)
        
        if cmd == "انضم_مافيا":
            user = self.db.get_user(user_id)
            if not user:
                return None
            return self.add_player(user_id, user['name'])
            
        if cmd == "بدء_مافيا":
            return self.assign_roles()
        
        return None

    def add_player(self, user_id, name):
        if self.phase != "registration":
            return None
        if user_id in self.players:
            return None
        
        self.players[user_id] = {"name": name, "role": None, "alive": True}
        return {"response": self.registration_flex(), "game_over": False}

    def assign_roles(self):
        if len(self.players) < 4:
            return None
        
        roles = ["mafia", "detective", "doctor"] + ["citizen"] * (len(self.players) - 3)
        random.shuffle(roles)
        
        for uid, role in zip(self.players.keys(), roles):
            self.players[uid]["role"] = role
        
        self.phase = "night"
        self.day = 1
        
        c = self._c()
        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "بدأت اللعبة", "size": "xl",
                     "weight": "bold", "color": c["primary"], "align": "center"},
                    {"type": "separator", "margin": "lg", "color": c["border"]},
                    {"type": "button", "action": {"type": "message", "label": "البداية", "text": "بداية"},
                     "style": "primary", "color": c["primary"], "margin": "md"}
                ],
                "backgroundColor": c["bg"],
                "paddingAll": "20px"
            }
        }
        
        return {
            "response": FlexMessage(alt_text="بدأت اللعبة", contents=FlexContainer.from_dict(bubble)),
            "game_over": True,
            "won": True
        }
