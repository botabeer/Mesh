import random
from games.base import BaseGame
from config import Config
from linebot.v3.messaging import FlexMessage, FlexContainer


class WordColorGame(BaseGame):
    """لعبة الألوان - نسخة آمنة لـ LINE"""

    def __init__(self, db, theme: str = "light"):
        super().__init__(db, theme)
        self.game_name = "الوان"

        self.colors = {
            "احمر": "#DC2626",
            "ازرق": "#2563EB",
            "اخضر": "#16A34A",
            "اصفر": "#CA8A04",
            "برتقالي": "#EA580C",
            "بنفسجي": "#7C3AED",
            "وردي": "#DB2777",
            "بني": "#92400E"
        }

        self.color_names = list(self.colors.keys())

    # ================= Question =================

    def get_question(self):
        word = random.choice(self.color_names)

        # 70% لون مختلف
        if random.random() < 0.7:
            color_name = random.choice([c for c in self.color_names if c != word])
        else:
            color_name = word

        self.current_answer = color_name

        c = self._c()
        hex_color = self.colors[color_name]

        contents = [
            {
                "type": "text",
                "text": self._safe_text(self.game_name),
                "size": "lg",
                "weight": "bold",
                "color": c["primary"],
                "align": "center"
            },
            {
                "type": "text",
                "text": f"السؤال {self.current_q + 1}/{self.total_q}",
                "size": "xs",
                "color": c["text_tertiary"],
                "align": "center"
            },
            {"type": "separator", "margin": "md", "color": c["border"]},
            {
                "type": "text",
                "text": "ما لون هذه الكلمة؟",
                "size": "sm",
                "color": c["text_secondary"],
                "align": "center",
                "margin": "lg"
            },
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": self._safe_text(word),
                        "size": "xxl",
                        "weight": "bold",
                        "color": hex_color,
                        "align": "center"
                    }
                ],
                "cornerRadius": "12px",
                "paddingAll": "20px",
                "backgroundColor": c["card"],
                "borderWidth": "2px",
                "borderColor": hex_color,
                "margin": "lg"
            },
            {
                "type": "text",
                "text": "اكتب اسم اللون",
                "size": "xs",
                "color": c["text_tertiary"],
                "align": "center",
                "margin": "md"
            },
            {"type": "separator", "margin": "lg", "color": c["border"]}
        ]

        if self.supports_hint and self.supports_reveal:
            contents.append({
                "type": "box",
                "layout": "horizontal",
                "spacing": "sm",
                "margin": "md",
                "contents": [
                    {
                        "type": "button",
                        "action": {"type": "message", "label": "لمح", "text": "لمح"},
                        "style": "secondary"
                    },
                    {
                        "type": "button",
                        "action": {"type": "message", "label": "جاوب", "text": "جاوب"},
                        "style": "secondary"
                    }
                ]
            })

        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": contents,
                "paddingAll": "20px",
                "backgroundColor": c["bg"]
            }
        }

        return FlexMessage(
            alt_text=self.game_name,
            contents=FlexContainer.from_dict(bubble),
            quickReply=self._qr()
        )

    # ================= Answer =================

    def check_answer(self, answer: str) -> bool:
        return Config.normalize(answer) == Config.normalize(self.current_answer)
