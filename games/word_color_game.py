import random
from games.base_game import BaseGame
from linebot.v3.messaging import FlexMessage, FlexContainer


class WordColorGame(BaseGame):
    def __init__(self, line_bot_api, difficulty=3, theme='light'):
        super().__init__(line_bot_api, game_type="competitive", difficulty=difficulty, theme=theme)
        self.game_name = "لون"
        self.supports_hint = False
        self.supports_reveal = True

        self.colors = {
            "احمر": "#DC2626", "ازرق": "#2563EB", "اخضر": "#16A34A",
            "اصفر": "#CA8A04", "برتقالي": "#EA580C", "بنفسجي": "#7C3AED",
            "وردي": "#DB2777", "بني": "#92400E"
        }
        self.color_names = list(self.colors.keys())
        self.used_combinations = []

    def get_question(self):
        available = [(w, c) for w in self.color_names for c in self.color_names
                     if (w, c) not in self.used_combinations]
        if not available:
            self.used_combinations = []
            available = [(w, c) for w in self.color_names for c in self.color_names]

        if random.random() < 0.7:
            diff = [(w, c) for w, c in available if w != c]
            word, color_name = random.choice(diff if diff else available)
        else:
            same = [(w, c) for w, c in available if w == c]
            word, color_name = random.choice(same if same else available)

        self.used_combinations.append((word, color_name))
        self.current_answer = [color_name]
        hex_color = self.colors[color_name]
        c = self.get_theme_colors()
        progress = int((self.current_question / self.questions_count) * 100)

        bubble = {
            "type": "bubble", "size": "mega",
            "body": {
                "type": "box", "layout": "vertical",
                "paddingAll": "20px", "backgroundColor": c["bg"],
                "contents": [
                    {"type": "text", "text": self.game_name,
                     "size": "xl", "weight": "bold", "align": "center", "color": c["primary"]},
                    {
                        "type": "box", "layout": "horizontal", "margin": "sm",
                        "contents": [{
                            "type": "box", "layout": "vertical", "contents": [],
                            "width": f"{progress}%", "height": "4px",
                            "backgroundColor": c["success"], "cornerRadius": "2px"
                        }],
                        "height": "4px", "backgroundColor": c["border"], "cornerRadius": "2px"
                    },
                    {"type": "separator", "margin": "lg", "color": c["border"]},
                    {"type": "text", "text": "ما لون هذه الكلمة",
                     "size": "sm", "color": c["text2"], "align": "center", "margin": "lg"},
                    {
                        "type": "box", "layout": "vertical", "margin": "lg",
                        "backgroundColor": c["card"], "cornerRadius": "12px",
                        "paddingAll": "20px", "borderWidth": "2px", "borderColor": hex_color,
                        "contents": [{
                            "type": "text", "text": word,
                            "size": "xxl", "weight": "bold",
                            "color": hex_color, "align": "center"
                        }]
                    },
                    {"type": "text", "text": "اكتب اسم اللون الذي ترى به الكلمة",
                     "size": "xs", "color": c["text3"], "align": "center", "wrap": True, "margin": "md"}
                ]
            },
            "footer": {
                "type": "box", "layout": "horizontal",
                "spacing": "sm", "paddingAll": "12px", "backgroundColor": c["card"],
                "contents": [
                    {
                        "type": "button",
                        "action": {"type": "message", "label": "جاوب", "text": "جاوب"},
                        "style": "secondary", "height": "sm", "color": self.BUTTON_COLOR, "flex": 1
                    },
                    {
                        "type": "button",
                        "action": {"type": "message", "label": "ايقاف", "text": "ايقاف"},
                        "style": "secondary", "height": "sm", "color": self.BUTTON_COLOR, "flex": 1
                    }
                ]
            }
        }
        return FlexMessage(alt_text=self.game_name, contents=FlexContainer.from_dict(bubble))

    def check_answer(self, user_answer, user_id, display_name):
        if not self.game_active or user_id in self.answered_users:
            return None

        normalized = self.normalize_text(user_answer)

        if normalized == "ايقاف":
            return self.handle_withdrawal(user_id, display_name)

        if self.supports_reveal and normalized == "جاوب":
            return self.handle_reveal()

        if normalized == self.normalize_text(self.current_answer[0]):
            return self.handle_correct_answer(user_id, display_name)

        return None
