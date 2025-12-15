import random
from games.base import BaseGame
from config import Config


class ChainWordsGame(BaseGame):
    def __init__(self, db, theme: str = "light"):
        super().__init__(db, theme)
        
        self.words = [
            "سياره", "تفاح", "قلم", "نجم", "كتاب", "باب", "رمل", "لعبه",
            "حديقه", "ورد", "دفتر", "معلم", "منزل", "شمس", "سفر"
        ]
        self.last_word = random.choice(self.words)
        self.used = {self.last_word}

    def get_question(self):
        letter = self.last_word[0]
        hint = f"السؤال {self.current_q + 1}/{self.total_q}\nابدا بحرف {letter}"
        return self.build_question_flex("كلمه جديده", hint)

    def check_answer(self, answer: str) -> bool:
        normalized = Config.normalize(answer)
        
        if len(normalized) < 2:
            return False
        
        required = Config.normalize(self.last_word[-1])
        
        if normalized[0] == required and normalized not in self.used:
            self.used.add(normalized)
            self.last_word = normalized
            return True
        
        return False
