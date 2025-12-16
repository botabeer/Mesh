import random
from games.base import BaseGame
from config import Config


class WordColorGame(BaseGame):
    def __init__(self, db, theme: str = "light"):
        super().__init__(db, theme)
        self.game_name = "الوان"
        
        self.colors = [
            "احمر", "ازرق", "اخضر", "اصفر", 
            "برتقالي", "بنفسجي", "وردي", "بني"
        ]

    def get_question(self):
        word = random.choice(self.colors)
        
        if random.random() < 0.7:
            color = random.choice([c for c in self.colors if c != word])
        else:
            color = word
        
        self.current_answer = color
        
        hint = f"السؤال {self.current_q + 1}/{self.total_q} - اجب باسم اللون وليس الكلمة"
        question = f"ما لون هذه الكلمة\n\nالكلمة: {word}\n\nتخيل انها مكتوبة بلون {color}"
        
        return self.build_question_flex(question, hint)

    def check_answer(self, answer: str) -> bool:
        normalized = Config.normalize(answer)
        correct = Config.normalize(self.current_answer)
        return normalized == correct
