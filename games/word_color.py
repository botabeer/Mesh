import random
from games.base import BaseGame
from config import Config
from linebot.v3.messaging import FlexMessage, FlexContainer


class WordColorGame(BaseGame):
    def __init__(self, db, theme="light"):
        super().__init__(db, theme)
        self.game_name = "لون"
        self.supports_hint = False
        self.supports_reveal = False

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

    def get_question(self):
        word = random.choice(self.color_names)

        if random.random() < 0.7:
            color_name = random.choice([c for c in self.color_names if c != word])
        else:
            color_name = word

        self.current_answer = color_name

        c = self._c()
        hex_color = self.colors[color_name]

        contents = [
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "flex": 1,
                        "contents": [
                            {"type": "text", "text": self._safe_text(self.game_name), "weight": "bold", "size": "lg", "color": c["text"]},
                            {"type": "text", "text": f"السؤال {self.current_q + 1}/{self.total_q}", "size": "xs", "color": c["text_secondary"]}
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "width": "60px",
                        "backgroundColor": c["card_secondary"],
                        "cornerRadius": "12px",
                        "paddingAll": "8px",
                        "contents": [
                            {"type": "text", "text": str(self.score), "size": "xl", "weight": "bold", "color": c["text"], "align": "center"},
                            {"type": "text", "text": "نقطة", "size": "xs", "color": c["text_tertiary"], "align": "center"}
                        ]
                    }
                ]
            },
            {"type": "separator", "margin": "lg", "color": c["border"]},
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
                "backgroundColor": c["card_secondary"],
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
            {"type": "separator", "margin": "lg", "color": c["border"]},
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "button",
                        "action": {"type": "message", "label": "ايقاف", "text": "ايقاف"},
                        "style": "secondary",
                        "color": c["button"],
                        "height": "sm"
                    }
                ],
                "margin": "md"
            }
        ]

        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": contents,
                "paddingAll": "20px",
                "backgroundColor": c["card"]
            }
        }

        return FlexMessage(
            alt_text=self.game_name,
            contents=FlexContainer.from_dict(bubble),
            quickReply=self._qr()
        )

    def check_answer(self, answer):
        return Config.normalize(answer) == Config.normalize(self.current_answer)
