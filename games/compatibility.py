import re
from linebot.v3.messaging import FlexMessage, FlexContainer, QuickReply, QuickReplyItem, MessageAction
from config import Config


class CompatibilityGame:
    def __init__(self, db, theme="light"):
        self.db = db
        self.theme = theme
        self.game_name = "لعبة التوافق"
        self.supports_hint = False
        self.supports_reveal = False
        self.total_q = 1
        self.current_answer = None

    def _c(self):
        return Config.get_theme(self.theme)

    def _qr(self):
        items = ["سؤال", "منشن", "تحدي", "اعتراف", "شخصية", "حكمة", "موقف", "بداية", "العاب", "مساعدة"]
        return QuickReply(items=[QuickReplyItem(action=MessageAction(label=i, text=i)) for i in items])

    def _normalize_name(self, name: str) -> str:
        name = name.strip()
        name = re.sub(r'[ـ]', '', name)
        name = re.sub(r'\s+', ' ', name)
        return name

    def _is_valid_name(self, name: str) -> bool:
        return bool(re.fullmatch(r'[ء-يA-Za-z\s]+', name))

    def _parse_names(self, text: str):
        text = self._normalize_name(text)
        parts = re.split(r'\s+و\s+', text)
        if len(parts) != 2:
            return None, None
        name1, name2 = parts[0].strip(), parts[1].strip()
        if not name1 or not name2:
            return None, None
        if not self._is_valid_name(name1) or not self._is_valid_name(name2):
            return None, None
        return name1, name2

    def _calculate_compatibility(self, name1: str, name2: str) -> int:
        n1 = name1.lower()
        n2 = name2.lower()
        names = sorted([n1, n2])
        combined = f"{names[0]}|{names[1]}"
        seed = sum((i + 1) * ord(c) for i, c in enumerate(combined))
        return 40 + (seed % 61)

    def _get_level_color(self, percentage: int):
        if percentage >= 90:
            return "red", "ممتاز جداً"
        elif percentage >= 80:
            return "purple", "عالي"
        elif percentage >= 65:
            return "blue", "جيد"
        elif percentage >= 50:
            return "gray", "متوسط"
        else:
            return "black", "منخفض"

    def get_question(self):
        question = "اكتب اسمين بينهما كلمة و\nمثال: اسم و اسم"
        contents = [
            {"type": "text", "text": question, "wrap": True, "align": "center", "size": "lg"}
        ]
        return self._create_bubble("لعبة التوافق", contents)

    def check_answer(self, answer: str) -> FlexMessage:
        name1, name2 = self._parse_names(answer)
        if not name1 or not name2:
            return self._create_bubble("خطأ", [{"type":"text","text":"الرجاء كتابة اسمين بينهما كلمة و\nمثال: اسم و اسم","wrap":True,"align":"center","size":"md"}])

        percentage = self._calculate_compatibility(name1, name2)
        color, level_text = self._get_level_color(percentage)

        self.current_answer = f"{name1} و {name2}\nنسبة التوافق: {percentage}%\n{level_text}"

        return self.build_result_flex(name1, name2, percentage, color, level_text)

    def _create_bubble(self, title, contents=None, buttons=None):
        c = self._c()
        if not contents or len(contents) == 0:
            contents = [{"type": "text", "text": "لا توجد بيانات لعرضها", "size": "md", "align": "center"}]
        if buttons:
            contents.extend(buttons)
        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {"type": "box", "layout": "vertical", "contents": contents, "paddingAll": "24px", "backgroundColor": c.get("card", "#FFFFFF")}
        }
        return FlexMessage(alt_text=title, contents=FlexContainer.from_dict(bubble), quickReply=self._qr())

    def build_result_flex(self, name1, name2, percentage, color, level_text):
        c = self._c()
        # عداد بصري
        progress_bar = {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": f"{percentage}%", "align": "center", "weight": "bold", "color": color},
                {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                        {"type": "filler"},
                        {"type": "box", "layout": "vertical", "contents": [], "backgroundColor": color, "height": "8px", "flex": percentage},
                        {"type": "filler"}
                    ]
                }
            ],
            "spacing": "sm",
            "margin": "md"
        }

        contents = [
            {"type": "text", "text": f"{name1} و {name2}", "wrap": True, "align": "center", "size": "lg", "weight": "bold"},
            progress_bar,
            {"type": "text", "text": f"التوافق: {level_text}", "align": "center", "weight": "bold", "size": "md", "color": color}
        ]

        return self._create_bubble(self.game_name, contents)
