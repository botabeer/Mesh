import random
from games.base import BaseGame
from config import Config

class ScrambleGame(BaseGame):
    def __init__(self, db, theme: str = "light"):
        super().__init__(db, theme)
        
        self.words = [
            "مدرسه", "كتاب", "قلم", "باب", "نافذه",
            "طاوله", "كرسي", "سياره", "طائره", "قطار",
            "تفاحه", "موز", "برتقال", "عنب", "بطيخ",
            "شمس", "قمر", "نجمه", "سماء", "بحر",
            "جبل", "نهر", "اسد", "نمر", "فيل",
            "زرافه", "حصان", "ورد", "شجره", "زهره",
            "حديقه", "مطبخ", "غرفه", "بيت", "مكتب",
            "تلفون", "حاسوب", "لابتوب", "شاشه", "لوحه"
        ]
        random.shuffle(self.words)
        self.used = []

    def _scramble(self, word: str) -> str:
        letters = list(word)
        for _ in range(10):
            random.shuffle(letters)
            if ''.join(letters) != word:
                return ' '.join(letters)
        return ' '.join(word[::-1])

    def get_question(self):
        available = [w for w in self.words if w not in self.used]
        if not available:
            self.used = []
            available = self.words.copy()

        word = random.choice(available)
        self.used.append(word)
        self.current_answer = word

        scrambled = self._scramble(word)
        hint = f"رتب الحروف"
        return self.build_question_flex(scrambled, hint)

    def check_answer(self, answer: str) -> bool:
        return Config.normalize(answer) == Config.normalize(self.current_answer)
