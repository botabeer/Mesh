import re
from linebot.v3.messaging import FlexMessage, FlexContainer
from config import Config


class CompatibilityGame:
    def __init__(self, db, theme: str = "light"):
        self.db = db
        self.theme = theme
        self.game_active = False
        self.game_name = "توافق"

    def _c(self):
        return Config.get_theme(self.theme)

    def normalize_name(self, name: str) -> str:
        return ' '.join(name.strip().split())

    def is_valid_text(self, text: str) -> bool:
        return bool(re.match(r'^[ء-يa-zA-Z\s]+$', text))

    def parse_names(self, text: str) -> tuple:
        text = ' '.join(text.strip().split())
        parts = re.split(r'\sو\s', text)
        if len(parts) == 2:
            name1, name2 = self.normalize_name(parts[0]), self.normalize_name(parts[1])
            if name1 and name2:
                return name1, name2
        return None, None

    def calculate_compatibility(self, name1: str, name2: str) -> int:
        names = sorted([self.normalize_name(name1), self.normalize_name(name2)])
        combined = ''.join(names)
        seed = sum(ord(c) * (i + 1) for i, c in enumerate(combined))
        return (seed % 81) + 20

    def get_compatibility_message(self, percentage: int) -> str:
        if percentage >= 90:
            return "توافق عالي جدا"
        if percentage >= 75:
            return "توافق عالي"
        if percentage >= 60:
            return "توافق جيد"
        if percentage >= 45:
            return "توافق متوسط"
        return "توافق منخفض"

    def start(self, user_id: str):
        self.game_active = True
        self.user_id = user_id
        return self.get_question()

    def get_question(self):
        c = self._c()
        contents = [
            {
                "type": "text",
                "text": "لعبة التوافق",
                "size": "xxl",
                "weight": "bold",
                "color": c["primary"],
                "align": "center"
            },
            {"type": "separator", "margin": "lg", "color": c["border"]},
            {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": c["glass"],
                "cornerRadius": "12px",
                "paddingAll": "16px",
                "margin": "md",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "text",
                        "text": "ادخل اسمين مفصولين بـ و",
                        "size": "md",
                        "weight": "bold",
                        "color": c["text"],
                        "wrap": True
                    },
                    {
                        "type": "text",
                        "text": "مثال: محمد و سارة",
                        "size": "sm",
                        "color": c["text_tertiary"],
                        "margin": "sm"
                    }
                ]
            },
            {"type": "separator", "margin": "lg", "color": c["border"]},
            {
                "type": "button",
                "action": {"type": "message", "label": "البداية", "text": "بداية"},
                "style": "secondary",
                "height": "sm",
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
                "backgroundColor": c["bg"],
                "paddingAll": "20px",
                "spacing": "md"
            }
        }

        return FlexMessage(
            alt_text="لعبة التوافق",
            contents=FlexContainer.from_dict(bubble)
        )

    def check(self, user_answer: str, user_id: str):
        if not self.game_active or user_id != self.user_id:
            return None

        name1, name2 = self.parse_names(user_answer)
        if not name1 or not name2:
            return None

        if not self.is_valid_text(name1) or not self.is_valid_text(name2):
            return None

        percentage = self.calculate_compatibility(name1, name2)
        message_text = self.get_compatibility_message(percentage)
        c = self._c()

        bar_color = "#FF1493" if percentage >= 75 else "#FF69B4" if percentage >= 50 else "#FFB6C1"

        flex_content = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "نتيجة التوافق",
                        "size": "xxl",
                        "weight": "bold",
                        "color": c["primary"],
                        "align": "center"
                    },
                    {"type": "separator", "margin": "lg", "color": c["border"]},
                    {
                        "type": "text",
                        "text": f"{name1} و {name2}",
                        "size": "lg",
                        "weight": "bold",
                        "color": c["text"],
                        "align": "center",
                        "margin": "md"
                    },
                    {
                        "type": "text",
                        "text": f"{percentage}%",
                        "size": "xxl",
                        "weight": "bold",
                        "color": bar_color,
                        "align": "center",
                        "margin": "md"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "backgroundColor": c["glass"],
                        "cornerRadius": "10px",
                        "height": "20px",
                        "margin": "md",
                        "contents": [{
                            "type": "box",
                            "layout": "vertical",
                            "backgroundColor": bar_color,
                            "cornerRadius": "10px",
                            "width": f"{percentage}%",
                            "height": "20px",
                            "contents": []
                        }]
                    },
                    {
                        "type": "text",
                        "text": message_text,
                        "size": "md",
                        "color": c["text_secondary"],
                        "align": "center",
                        "wrap": True,
                        "margin": "md"
                    },
                    {"type": "separator", "margin": "lg", "color": c["border"]},
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "spacing": "sm",
                        "margin": "md",
                        "contents": [
                            {
                                "type": "button",
                                "action": {"type": "message", "label": "اعادة", "text": "توافق"},
                                "style": "primary",
                                "color": c["primary"],
                                "height": "sm",
                                "flex": 1
                            },
                            {
                                "type": "button",
                                "action": {"type": "message", "label": "البداية", "text": "بداية"},
                                "style": "secondary",
                                "height": "sm",
                                "flex": 1
                            }
                        ]
                    }
                ],
                "paddingAll": "20px",
                "spacing": "md",
                "backgroundColor": c["bg"]
            }
        }

        self.game_active = False
        
        return {
            'response': FlexMessage(
                alt_text="نتيجة التوافق",
                contents=FlexContainer.from_dict(flex_content)
            ),
            'game_over': True,
            'won': True
        }
