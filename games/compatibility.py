import re
from linebot.v3.messaging import FlexMessage, FlexContainer
from config import Config


class CompatibilityGame:
    """لعبة التوافق - للترفيه فقط بدون نقاط"""

    def __init__(self, db, theme: str = "light"):
        self.db = db
        self.theme = theme
        self.game_active = False

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
            return "توافق عالي جداً!"
        if percentage >= 75:
            return "توافق عالي!"
        if percentage >= 60:
            return "توافق جيد!"
        if percentage >= 45:
            return "توافق متوسط!"
        return "توافق منخفض!"

    def start(self, user_id: str):
        self.game_active = True
        return self.get_question()

    def get_question(self):
        c = self._c()
        
        contents = [
            {"type": "text", "text": "لعبة التوافق", "size": "xxl",
             "weight": "bold", "color": c["primary"], "align": "center"},
            {"type": "separator", "margin": "lg", "color": c["border"]},
            {"type": "text", "text": "أدخل اسمين مفصولين بـ (و)", "size": "lg",
             "weight": "bold", "color": c["text"], "align": "center", "wrap": True},
            {"type": "text", "text": "مثال: محمد و سارة", "size": "sm",
             "color": c["text_tertiary"], "align": "center", "margin": "md"},
            {"type": "text", "text": "أحرف عربية أو إنجليزية فقط", "size": "xs",
             "color": c["warning"], "align": "center", "margin": "sm", "wrap": True},
            {"type": "separator", "margin": "lg", "color": c["border"]},
            {"type": "button", "action": {"type": "message", "label": "البداية", "text": "بدايه"},
             "style": "secondary", "height": "sm", "margin": "md"}
        ]

        return FlexMessage(
            alt_text="لعبة التوافق",
            contents=FlexContainer.from_dict({
                "type": "bubble",
                "body": {"type": "box", "layout": "vertical", "contents": contents,
                         "backgroundColor": c["bg"], "paddingAll": "20px"}
            })
        )

    def check(self, user_answer: str, user_id: str):
        if not self.game_active:
            return None

        name1, name2 = self.parse_names(user_answer)
        from linebot.v3.messaging import TextMessage

        if not name1 or not name2:
            return {
                'response': TextMessage(text="الصيغة غير صحيحة\nاكتب: اسم و اسم\nمثال: محمد و سارة"),
                'game_over': False
            }

        if not self.is_valid_text(name1) or not self.is_valid_text(name2):
            return {
                'response': TextMessage(text="غير مسموح بإدخال رموز أو أرقام\nاكتب أسماء نصية فقط"),
                'game_over': False
            }

        percentage = self.calculate_compatibility(name1, name2)
        message_text = self.get_compatibility_message(percentage)
        c = self._c()

        if percentage >= 75:
            bar_color = "#FF1493"
        elif percentage >= 50:
            bar_color = "#FF69B4"
        else:
            bar_color = "#FFB6C1"

        flex_content = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "نتيجة التوافق", "size": "xl",
                     "weight": "bold", "color": c["primary"], "align": "center"},
                    {"type": "separator", "margin": "md", "color": c["border"]},
                    {"type": "text", "text": f"{name1} و {name2}", "size": "lg",
                     "weight": "bold", "color": c["text"], "align": "center", "margin": "md"},
                    {"type": "text", "text": f"{percentage}%", "size": "xxl",
                     "weight": "bold", "color": bar_color, "align": "center", "margin": "md"},
                    {"type": "box", "layout": "vertical", "backgroundColor": c["glass"],
                     "cornerRadius": "10px", "height": "20px", "margin": "md",
                     "contents": [
                         {"type": "box", "layout": "vertical",
                          "backgroundColor": bar_color,
                          "cornerRadius": "10px",
                          "width": f"{percentage}%",
                          "height": "20px",
                          "contents": []}
                     ]},
                    {"type": "text", "text": message_text, "size": "md",
                     "color": c["text"], "align": "center", "wrap": True, "margin": "md"},
                    {"type": "separator", "margin": "md", "color": c["border"]},
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "spacing": "md",
                        "margin": "md",
                        "contents": [
                            {"type": "button", "action": {"type": "message",
                                                          "label": "إعادة", "text": "توافق"},
                             "style": "primary", "color": c["primary"], "height": "sm"},
                            {"type": "button", "action": {"type": "message",
                                                          "label": "البداية", "text": "بدايه"},
                             "style": "secondary", "height": "sm"}
                        ]
                    }
                ],
                "paddingAll": "20px",
                "spacing": "sm",
                "backgroundColor": c["bg"]
            }
        }

        result_message = FlexMessage(
            alt_text="نتيجة التوافق",
            contents=FlexContainer.from_dict(flex_content)
        )

        self.game_active = False
        return {'response': result_message, 'game_over': True}
