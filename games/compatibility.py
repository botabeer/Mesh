import re
import hashlib
from linebot.v3.messaging import FlexMessage, FlexContainer, QuickReply, QuickReplyItem, MessageAction

class CompatibilityGame:
    def __init__(self, db, theme="light"):
        self.db = db
        self.theme = theme
        self.game_name = "توافق"
        self.supports_hint = False
        self.supports_reveal = False
        self.total_q = 1
        self.current_answer = None

    def _c(self):
        from ui import UI
        return UI.get_theme(self.theme)

    def _qr(self):
        items = ["سؤال", "منشن", "تحدي", "اعتراف", "شخصيه", "حكمه", "موقف", "بدايه", "العاب", "مساعده"]
        return QuickReply(items=[QuickReplyItem(action=MessageAction(label=i, text=i)) for i in items])

    def _normalize_name(self, name: str) -> str:
        name = name.strip()
        name = re.sub(r'[ـ]', '', name)
        name = re.sub(r'\s+', ' ', name)
        return name

    def _is_valid_name(self, name: str) -> bool:
        return bool(re.fullmatch(r'[ء-يA-Za-z\s]+', name))

    def _parse_names(self, text: str):
        from config import Config
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
        from config import Config
        n1 = Config.normalize(name1.lower())
        n2 = Config.normalize(name2.lower())
        names = sorted([n1, n2])
        combined = f"{names[0]}|{names[1]}"
        hash_obj = hashlib.md5(combined.encode('utf-8'))
        hash_int = int(hash_obj.hexdigest(), 16)
        base_percentage = 50
        range_percentage = 49
        percentage = base_percentage + (hash_int % range_percentage)
        common_letters = set(n1) & set(n2)
        similarity_bonus = min(len(common_letters) * 2, 10)
        final_percentage = min(percentage + similarity_bonus, 99)
        return final_percentage

    def _get_compatibility_message(self, percentage: int) -> str:
        if percentage >= 90:
            return "توافق استثنائي"
        elif percentage >= 80:
            return "توافق ممتاز"
        elif percentage >= 70:
            return "توافق جيد جدا"
        elif percentage >= 60:
            return "توافق جيد"
        else:
            return "توافق متوسط"

    def get_question(self):
        c = self._c()
        contents = [
            {"type": "text", "text": "Bot Mesh", "size": "xxl", "weight": "bold", "color": c["text"], "align": "center"},
            {"type": "separator", "margin": "lg", "color": c["border"]},
            {"type": "text", "text": "لعبه التوافق", "size": "lg", "weight": "bold", "color": c["text"], "align": "center", "margin": "lg"},
            {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": c["card"],
                "cornerRadius": "12px",
                "paddingAll": "20px",
                "margin": "lg",
                "contents": [
                    {"type": "text", "text": "اكتب اسمين بينهما كلمه و", "size": "md", "color": c["text"], "align": "center", "wrap": True},
                    {"type": "text", "text": "مثال: اسم و اسم", "size": "sm", "color": c["text_secondary"], "align": "center", "margin": "md"}
                ]
            },
            {"type": "text", "text": "للترفيه فقط - بدون نقاط", "size": "xs", "color": c["text_tertiary"], "align": "center", "margin": "md"},
            {"type": "text", "text": "Bot Mesh | 2025 عبير الدوسري", "size": "xxs", "color": c["text_secondary"], "align": "center", "margin": "lg"}
        ]
        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": contents,
                "backgroundColor": c["bg"],
                "paddingAll": "24px"
            }
        }
        return FlexMessage(
            alt_text="لعبه التوافق",
            contents=FlexContainer.from_dict(bubble),
            quick_reply=self._qr()
        )

    def check_answer(self, answer: str) -> bool:
        name1, name2 = self._parse_names(answer)
        if not name1 or not name2:
            return False
        percentage = self._calculate_compatibility(name1, name2)
        message = self._get_compatibility_message(percentage)
        c = self._c()
        contents = [
            {"type": "text", "text": "Bot Mesh", "size": "xxl", "weight": "bold", "color": c["text"], "align": "center"},
            {"type": "separator", "margin": "lg", "color": c["border"]},
            {"type": "text", "text": "نسبه التوافق", "size": "lg", "weight": "bold", "color": c["text"], "align": "center", "margin": "lg"},
            {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": c["card"],
                "cornerRadius": "12px",
                "paddingAll": "20px",
                "margin": "lg",
                "contents": [
                    {"type": "text", "text": f"{name1} و {name2}", "size": "md", "color": c["text"], "align": "center", "wrap": True},
                    {"type": "text", "text": f"{percentage}%", "size": "xxl", "weight": "bold", "color": c["text"], "align": "center", "margin": "lg"},
                    {"type": "text", "text": message, "size": "sm", "color": c["text_secondary"], "align": "center", "margin": "md"}
                ]
            },
            {
                "type": "box",
                "layout": "horizontal",
                "spacing": "sm",
                "margin": "lg",
                "contents": [
                    {"type": "button", "action": {"type": "message", "label": "مره اخرى", "text": "توافق"}, "style": "secondary", "color": c["button"], "height": "sm"},
                    {"type": "button", "action": {"type": "message", "label": "بدايه", "text": "بدايه"}, "style": "secondary", "color": c["button"], "height": "sm"}
                ]
            },
            {"type": "text", "text": "Bot Mesh | 2025 عبير الدوسري", "size": "xxs", "color": c["text_secondary"], "align": "center", "margin": "lg"}
        ]
        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": contents,
                "backgroundColor": c["bg"],
                "paddingAll": "24px"
            }
        }
        self.current_answer = FlexMessage(
            alt_text="نتيجه التوافق",
            contents=FlexContainer.from_dict(bubble),
            quick_reply=self._qr()
        )
        return True
