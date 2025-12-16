import random
from games.base import BaseGame
from config import Config


class LettersWordsGame(BaseGame):
    def __init__(self, db, theme: str = "light"):
        super().__init__(db, theme)
        self.game_name = "كون كلمات"
        
        self.letter_sets = [
            ["ق", "ل", "م", "ع", "ر", "ب"],
            ["س", "ا", "ر", "ه", "ي", "م"],
            ["ك", "ت", "ا", "ب", "م", "ل"],
            ["د", "ر", "س", "ه", "م", "ا"],
            ["ح", "د", "ي", "ق", "ه", "ر"],
            ["ن", "و", "ر", "ا", "ل", "م"],
            ["ش", "م", "س", "ا", "ل", "ر"],
            ["ب", "ح", "ر", "ا", "ل", "م"],
            ["ج", "ب", "ل", "ا", "ر", "م"],
            ["ف", "ر", "ح", "ا", "ل", "م"]
        ]
        random.shuffle(self.letter_sets)
        
        self.found_words = set()
        self.required = 3
        self.current_letters = None

    def get_question(self):
        self.current_letters = self.letter_sets[self.current_q % len(self.letter_sets)]
        self.current_answer = self.current_letters
        self.found_words.clear()
        
        letters_display = ' - '.join(self.current_letters)
        hint = f"السؤال {self.current_q + 1}/{self.total_q} - مطلوب {self.required} كلمات"
        question = f"كون كلمات من هذه الاحرف:\n\n{letters_display}\n\nيمكنك استخدام كل حرف اكثر من مرة"
        
        return self.build_question_flex(question, hint)

    def check_answer(self, answer: str) -> bool:
        normalized = Config.normalize(answer)
        
        if len(normalized) < 2 or normalized in self.found_words:
            return False
        
        available_letters = [Config.normalize(letter) for letter in self.current_letters]
        
        for char in normalized:
            if char not in available_letters:
                return False
        
        self.found_words.add(normalized)
        return len(self.found_words) >= self.required
