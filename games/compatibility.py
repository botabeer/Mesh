import re
import hashlib
from games.base import BaseGame
from config import Config

class CompatibilityGame(BaseGame):
    def __init__(self, db, theme="light"):
        super().__init__(db, theme)
        self.game_name = "توافق"
        self.supports_hint = False
        self.supports_reveal = False
        self.total_q = 1
        self.current_answer = None

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
        """حساب نسبة التوافق بطريقة ذكية ومتسقة"""
        # توحيد النصوص
        n1 = Config.normalize(name1.lower())
        n2 = Config.normalize(name2.lower())
        
        # ترتيب الاسماء لضمان نفس النتيجة
        names = sorted([n1, n2])
        combined = f"{names[0]}|{names[1]}"
        
        # استخدام hash للحصول على رقم ثابت
        hash_obj = hashlib.md5(combined.encode('utf-8'))
        hash_int = int(hash_obj.hexdigest(), 16)
        
        # حساب نسبة من 50% الى 99%
        base_percentage = 50
        range_percentage = 49
        percentage = base_percentage + (hash_int % range_percentage)
        
        # اضافة عامل التشابه في الحروف
        common_letters = set(n1) & set(n2)
        similarity_bonus = min(len(common_letters) * 2, 10)
        
        final_percentage = min(percentage + similarity_bonus, 99)
        
        return final_percentage

    def _get_compatibility_message(self, percentage: int) -> str:
        """رسالة مناسبة حسب النسبة"""
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
            {"type": "text", "text": "لعبة التوافق", "size": "xl", "weight": "bold", "color": c["text"], "align": "center"},
            {"type": "separator", "margin": "md", "color": c["border"]},
            {"type": "box", "layout": "vertical", "contents": [
                {"type": "text", "text": "اكتب اسمين بينهما كلمة و", "size": "md", "color": c["text"], "align": "center", "wrap": True, "margin": "md"},
                {"type": "text", "text": "مثال: اسم و اسم", "size": "sm", "color": c["text_secondary"], "align": "center", "margin": "xs"}
            ], "backgroundColor": c["card_secondary"], "cornerRadius": "12px", "paddingAll": "16px", "margin": "lg"},
            {"type": "text", "text": "للترفيه فقط - بدون نقاط", "size": "xs", "color": c["text_tertiary"], "align": "center", "margin": "md"}
        ]
        
        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": contents,
                "backgroundColor": c["card"],
                "paddingAll": "24px"
            }
        }
        
        from linebot.v3.messaging import FlexMessage, FlexContainer
        return FlexMessage(
            alt_text="لعبة التوافق",
            contents=FlexContainer.from_dict(bubble)
        )

    def check_answer(self, answer: str) -> bool:
        name1, name2 = self._parse_names(answer)
        if not name1 or not name2:
            return False

        percentage = self._calculate_compatibility(name1, name2)
        message = self._get_compatibility_message(percentage)
        
        self.current_answer = f"نسبة التوافق بين {name1} و {name2}\n\n{percentage}%\n\n{message}"
        return True
