import re
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
        n1 = Config.normalize(name1)
        n2 = Config.normalize(name2)
        names = sorted([n1, n2])
        combined = f"{names[0]}|{names[1]}"
        seed = sum((i + 1) * ord(c) for i, c in enumerate(combined))
        return 40 + (seed % 61)

    def get_question(self):
        question = "اكتب اسمين بينهما كلمة و\nمثال: اسم و اسم"
        hint = "لعبة التوافق"
        return self.build_question_flex(question, hint)

    def check_answer(self, answer: str) -> bool:
        name1, name2 = self._parse_names(answer)
        if not name1 or not name2:
            return False

        percentage = self._calculate_compatibility(name1, name2)
        self.current_answer = f"{name1} و {name2}: {percentage}%"
        return True
