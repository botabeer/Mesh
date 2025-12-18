import random
from games.base import BaseGame
from config import Config


class HumanAnimalGame(BaseGame):
    def __init__(self, db, theme: str = "light"):
        super().__init__(db, theme)
        self.game_name = "لعبه"
        
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
        question = f"الفئة: {self.current_category}\n\nالحرف: {self.current_letter}\n\nاكتب كلمة من فئة {self.current_category} تبدأ بحرف {self.current_letter}"
        
        return self.build_question_flex(question, hint)

    def check_answer(self, answer: str) -> bool:
        normalized = Config.normalize(answer)
        
        if len(normalized) < 2:
            return False
        
        first_letter = normalized[0]
        required_letter = Config.normalize(self.current_letter)[0]
        
        return first_letter == required_letter
