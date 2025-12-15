import random
from games.base import BaseGame
from config import Config


class WordColorGame(BaseGame):
    def __init__(self, db, theme: str = "light"):
        super().__init__(db, theme)
        
        self.colors = ["احمر", "ازرق", "اخضر", "اصفر", "برتقالي", "بنفسجي", "وردي", "بني"]

    def get_question(self):
        word = random.choice(self.colors)
        
        if random.random() < 0.7:
            color = random.choice([c for c in self.colors if c != word])
        else:
            color = word
        
        self.current_answer = color
        
        hint = f"السؤال {self.current_q + 1}/{self.total_q}\nاجب باسم اللون"
        return self.build_question_flex(f"ما لون هذه الكلمه\n\n{word}", hint)

    def check_answer(self, answer: str) -> bool:
        return Config.normalize(answer) == Config.normalize(self.current_answer)
