import re
from linebot.v3.messaging import FlexMessage, FlexContainer, QuickReply, QuickReplyItem, MessageAction
from config import Config


class CompatibilityGame:
    def __init__(self, db, theme: str = "light"):
        self.db = db
        self.theme = theme
        self.game_active = False
        self.game_name = "توافق"
        self.user_id = None

    def _c(self):
        return Config.get_theme(self.theme)
    
    def _qr(self):
        items = ["سؤال", "منشن", "تحدي", "اعتراف", "شخصية", "حكمة", "موقف", "بداية", "العاب", "مساعدة"]
        return QuickReply(items=[QuickReplyItem(action=MessageAction(label=i, text=i)) for i in items])

    def normalize_name(self, name: str) -> str:
        return ' '.join(name.strip().split())

    def is_valid_text(self, text: str) -> bool:
        return bool(re.match(r'^[ء-يa-zA-Z\s]+$', text))

    def parse_names(self, text: str):
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
        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "Bot Mesh", "size": "xxl", "weight": "bold", "color": c["primary"], "align": "center"},
                    {"type": "separator", "margin": "lg", "color": c["border"]},
                    {"type": "text", "text": "لعبة التوافق", "size": "lg", "weight": "bold", "color": c["text"], "align": "center", "margin": "lg"},
                    {
                        "type": "box", "layout": "vertical",
                        "backgroundColor": c["card_secondary"], "cornerRadius": "12px",
                        "paddingAll": "16px", "margin": "lg", "spacing": "sm",
                        "contents": [
                            {"type": "text", "text": "ادخل اسمين مفصولين بـ و", "size": "md", "weight": "bold", "color": c["text"], "wrap": True, "align": "center"},
                            {"type": "text", "text": "مثال: اسم و اسم", "size": "sm", "color": c["text_tertiary"], "margin": "sm", "align": "center"}
                        ]
                    },
                    {"type": "separator", "margin": "lg", "color": c["border"]},
                    {"type": "button", "action": {"type": "message", "label": "البداية", "text": "بداية"}, "style": "secondary", "color": c["button_secondary"], "height": "sm", "margin": "md"},
                    {
                        "type": "text",
                        "text": "Bot Mesh | عبير الدوسري 2025",
                        "size": "xxs",
                        "color": c["text_tertiary"],
                        "align": "center",
                        "margin": "lg"
                    }
                ],
                "backgroundColor": c["card"], "paddingAll": "20px", "spacing": "md"
            }
        }

        return FlexMessage(alt_text="لعبة التوافق", contents=FlexContainer.from_dict(bubble), quickReply=self._qr())

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

        bar_color = "#000000" if self.theme == "light" else "#FFFFFF"

        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "Bot Mesh", "size": "xxl", "weight": "bold", "color": c["primary"], "align": "center"},
                    {"type": "separator", "margin": "lg", "color": c["border"]},
                    {"type": "text", "text": "نتيجة التوافق", "size": "lg", "weight": "bold", "color": c["text"], "align": "center", "margin": "lg"},
                    {"type": "text", "text": f"{name1} و {name2}", "size": "md", "weight": "bold", "color": c["text"], "align": "center", "margin": "md"},
                    {"type": "text", "text": f"{percentage}%", "size": "xxl", "weight": "bold", "color": c["text"], "align": "center", "margin": "md"},
                    {
                        "type": "box", "layout": "vertical",
                        "backgroundColor": c["card_secondary"], "cornerRadius": "10px",
                        "height": "20px", "margin": "md",
                        "contents": [{
                            "type": "box", "layout": "vertical",
                            "backgroundColor": bar_color, "cornerRadius": "10px",
                            "width": f"{percentage}%", "height": "20px", "contents": []
                        }]
                    },
                    {"type": "text", "text": message_text, "size": "md", "color": c["text_secondary"], "align": "center", "wrap": True, "margin": "md"},
                    {"type": "separator", "margin": "lg", "color": c["border"]},
                    {
                        "type": "box", "layout": "horizontal", "spacing": "sm", "margin": "md",
                        "contents": [
                            {"type": "button", "action": {"type": "message", "label": "اعادة", "text": "توافق"}, "style": "secondary", "color": c["button_secondary"], "height": "sm", "flex": 1},
                            {"type": "button", "action": {"type": "message", "label": "البداية", "text": "بداية"}, "style": "primary", "color": c["button_primary"], "height": "sm", "flex": 1}
                        ]
                    },
                    {
                        "type": "text",
                        "text": "Bot Mesh | عبير الدوسري 2025",
                        "size": "xxs",
                        "color": c["text_tertiary"],
                        "align": "center",
                        "margin": "lg"
                    }
                ],
                "paddingAll": "20px", "spacing": "md", "backgroundColor": c["card"]
            }
        }

        self.game_active = False
        
        return {
            'response': FlexMessage(alt_text="نتيجة التوافق", contents=FlexContainer.from_dict(bubble), quickReply=self._qr()),
            'game_over': True,
            'won': True
        }
