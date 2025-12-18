import re
from games.base import BaseGame
from config import Config


class CompatibilityGame(BaseGame):
    def __init__(self, db, theme="light"):
        super().__init__(db, theme)
        self.game_name = "لعبة التوافق"
        self.supports_hint = False
        self.supports_reveal = False
        self.total_q = 1

    def get_question(self):
        question = "اكتب اسمين وبينهما كلمة و\nمثال: محمد و فاطمة"
        return self.build_question_flex(question, None)

    def check_answer(self, answer: str) -> bool:
        name1, name2 = self._parse_names(answer)
        if not name1 or not name2:
            self.error_message = "الرجاء كتابة اسمين بينهما كلمة و\nمثال: اسم و اسم"
            return False

        percentage = self._calculate_compatibility(name1, name2)
        message = self._get_message(percentage)

        self.current_answer = (
            f"{name1} و {name2}\n"
            f"نسبة التوافق: {percentage}%\n"
            f"{message}"
        )
        return True

    def _normalize_name(self, name: str) -> str:
        name = name.strip()
        name = re.sub(r'[ـ]', '', name)
        name = re.sub(r'\s+', ' ', name)
        return name

    def _is_valid_name(self, name: str) -> bool:
        return bool(re.fullmatch(r'[ء-يA-Za-z\s]+', name))

    def _parse_names(self, text: str):
        if not re.fullmatch(r'[ء-يA-Za-z\s]+', text):
            return None, None

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

    def _get_message(self, percentage: int) -> str:
        if percentage >= 90:
            return "توافق ممتاز جدا"
        elif percentage >= 80:
            return "توافق عالي"
        elif percentage >= 65:
            return "توافق جيد"
        elif percentage >= 50:
            return "توافق متوسط"
        else:
            return "توافق منخفض"

    def finish(self):
        return None
