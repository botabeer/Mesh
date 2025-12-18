import re
from games.base import BaseGame
from linebot.v3.messaging import FlexMessage, FlexContainer, QuickReply, QuickReplyItem, MessageAction
from config import Config

class CompatibilityGame(BaseGame):
    def __init__(self, db, theme="light"):
        super().__init__(db, theme)
        self.game_name = "لعبة التوافق"
        self.supports_hint = False
        self.supports_reveal = False
        self.total_q = 1

    # --- عرض السؤال ---
    def get_question(self):
        question = "أرسل اسمين بينهما 'و'\nمثال: اسم و اسم"
        return self.build_input_flex(question)

    # --- التحقق من الإجابة ---
    def check_answer(self, answer: str):
        name1, name2 = self._parse_names(answer)
        if not name1 or not name2:
            return self.build_input_flex(
                "الرجاء كتابة اسمين صحيحين بينهما 'و'\nمثال: اسم و اسم"
            )

        percentage = self._calculate_compatibility(name1, name2)
        message = self._get_message(percentage)
        text = f"{name1} و {name2}\nنسبة التوافق: {percentage}%\n{message}"

        # إرسال سلسلة FlexMessage لمحاكاة Progress Bar متدرج
        return self.build_progress_steps(text, percentage)

    # --- Helpers ---
    def _normalize_name(self, name: str) -> str:
        name = name.strip()
        name = re.sub(r'[ـ]', '', name)
        name = re.sub(r'\s+', ' ', name)
        return name

    def _is_valid_name(self, name: str) -> bool:
        return bool(re.fullmatch(r'[ء-يA-Za-z\s]+', name))

    def _parse_names(self, text: str):
        text = self._normalize_name(text)
        parts = re.split(r'\s*و\s*', text)
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
        return 40 + (seed % 61)  # من 40 إلى 100

    def _get_message(self, percentage: int) -> str:
        if percentage >= 90:
            return "توافق ممتاز جداً"
        elif percentage >= 80:
            return "توافق عالي"
        elif percentage >= 65:
            return "توافق جيد"
        elif percentage >= 50:
            return "توافق متوسط"
        else:
            return "توافق منخفض"

    # --- FlexMessage للسؤال ---
    def build_input_flex(self, prompt: str):
        c = self._c()
        contents = [
            {"type": "text", "text": self.game_name, "weight": "bold", "size": "lg", "color": c["text"], "align": "center"},
            {"type": "text", "text": prompt, "wrap": True, "align": "center", "size": "md", "color": c["text_secondary"], "margin": "md"},
            {"type": "text", "text": "مثال: اسم و اسم", "wrap": True, "align": "center", "size": "sm", "color": c["text_tertiary"], "margin": "md"}
        ]

        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {"type": "box", "layout": "vertical", "contents": contents, "backgroundColor": c["card"], "paddingAll": "24px"}
        }

        return FlexMessage(alt_text=self.game_name, contents=FlexContainer.from_dict(bubble), quickReply=self._qr())

    # --- إنشاء Progress Bar متدرج ---
    def build_progress_steps(self, text: str, percentage: int):
        steps = min(percentage, 100)
        step_size = max(1, steps // 10)
        messages = []

        for i in range(0, steps + 1, step_size):
            messages.append(self.build_result_flex(text, i))

        return messages

    # --- FlexMessage للنتيجة + Progress Bar + زر إعادة ---
    def build_result_flex(self, text: str, percentage: int = None):
        c = self._c()
        contents = [
            {"type": "text", "text": self.game_name, "weight": "bold", "size": "lg", "color": c["text"], "align": "center"},
            {"type": "text", "text": text, "wrap": True, "align": "center", "size": "md", "color": c["text_secondary"], "margin": "md"}
        ]

        if percentage is not None:
            if percentage >= 90:
                bar_color = "#FF4C4C"  # أحمر - ممتاز جداً
            elif percentage >= 80:
                bar_color = "#A64CFF"  # بنفسجي - عالي
            elif percentage >= 65:
                bar_color = "#4C6EFF"  # أزرق - جيد
            elif percentage >= 50:
                bar_color = "#A0A0A0"  # رمادي - متوسط
            else:
                bar_color = "#000000"  # أسود - منخفض

            contents.append({
                "type": "box",
                "layout": "vertical",
                "margin": "lg",
                "contents": [
                    {"type": "box", "layout": "horizontal", "backgroundColor": c["card_secondary"], "height": "20px", "cornerRadius": "10px",
                     "contents": [{"type": "box", "layout": "vertical", "backgroundColor": bar_color, "width": f"{percentage}%", "cornerRadius": "10px"}]}
                ]
            })

        # زر إعادة
        contents.append({
            "type": "box",
            "layout": "horizontal",
            "margin": "md",
            "contents": [
                {"type": "button", "action": {"type": "message", "label": "إعادة", "text": "ابدأ التوافق"}, "style": "primary", "color": c["button_primary"], "height": "sm", "flex": 1}
            ]
        })

        bubble = {"type": "bubble", "size": "mega", "body": {"type": "box", "layout": "vertical", "contents": contents, "backgroundColor": c["card"], "paddingAll": "24px"}}
        return FlexMessage(alt_text=self.game_name, contents=FlexContainer.from_dict(bubble), quickReply=self._qr())

    def finish(self):
        return None
