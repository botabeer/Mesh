import random
from games.base import BaseGame
from config import Config


class LettersGame(BaseGame):
    """لعبة الحروف - اذكر كلمة تبدأ بالحرف المطلوب"""

    def __init__(self, db, theme: str = "light"):
        super().__init__(db, theme)
        self.game_name = "حرف"

        self.letters = [
            "ا", "ب", "ت", "ث", "ج", "ح", "خ",
            "د", "ذ", "ر", "ز", "س", "ش",
            "ص", "ض", "ط", "ظ", "ع", "غ",
            "ف", "ق", "ك", "ل", "م", "ن",
            "ه", "و", "ي"
        ]

        random.shuffle(self.letters)
        self.current_letter = None

    def get_question(self):
        idx = self.current_q % len(self.letters)
        self.current_letter = self.letters[idx]

        text = f"اذكر كلمة تبدأ بحرف:\n\n{self.current_letter}"
        hint = "اكتب أي كلمة صحيحة"

        return self.build_question_flex(text, hint)

    def check_answer(self, answer: str) -> bool:
        if not answer:
            return False

        normalized = Config.normalize(answer)
        return normalized.startswith(self.current_letter)
