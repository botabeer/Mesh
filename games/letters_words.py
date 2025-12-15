import random
from games.base import BaseGame
from config import Config


class LettersWordsGame(BaseGame):
    def __init__(self, db, theme: str = "light"):
        super().__init__(db, theme)
        
        self.letter_sets = [
            ["ق", "ل", "م", "ع", "ر", "ب"],
            ["س", "ا", "ر", "ه", "ي", "م"],
            ["ك", "ت", "ا", "ب", "م", "ل"],
            ["د", "ر", "س", "ه", "م", "ا"],
            ["ح", "د", "ي", "ق", "ه", "ر"]
        ]
        random.shuffle(self.letter_sets)
        
        self.found_words = set()
        self.required = 3

    def get_question(self):
        letters = self.letter_sets[self.current_q % len(self.letter_sets)]
        self.current_answer = letters
        self.found_words.clear()
        
        letters_display = ' '.join(letters)
        hint = f"السؤال {self.current_q + 1}/{self.total_q}\nمطلوب {self.required} كلمات"
        return self.build_question_flex(f"كون كلمات من\n\n{letters_display}", hint)

    def check_answer(self, answer: str) -> bool:
        normalized = Config.normalize(answer)
        
        if len(normalized) < 2 or normalized in self.found_words:
            return False
        
        self.found_words.add(normalized)
        
        if len(self.found_words) >= self.required:
            return True
        
        return False
