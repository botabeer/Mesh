import random
from games.base import BaseGame
from config import Config

class HumanAnimalPlantGame(BaseGame):
    def __init__(self, db, theme: str = "light"):
        super().__init__(db, theme)
        self.letters = list("ابتجحدرزسشصطعفقكلمنهوي")
        random.shuffle(self.letters)
        self.categories = ["انسان", "حيوان", "نبات", "جماد", "بلاد"]
        self.current_category = None
        self.current_letter = None

    def get_question(self):
        self.current_letter = self.letters[self.current_q % len(self.letters)]
        self.current_category = random.choice(self.categories)
        self.current_answer = self.current_letter
        
        hint = f"السؤال {self.current_q + 1}/{self.total_q}"
        return self.build_question_flex(
            f"الفئه {self.current_category}\n\nالحرف {self.current_letter}",
            hint
        )

    def check_answer(self, answer: str) -> bool:
        normalized = Config.normalize(answer)
        if len(normalized) < 2:
            return False
        return normalized[0] == Config.normalize(self.current_letter)[0]
