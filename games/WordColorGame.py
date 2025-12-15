import random
from games.base import BaseGame
from config import Config


class WordColorGame(BaseGame):
    """لعبة تخمين لون الكلمة - تحدي ستروب"""
    
    def __init__(self, db, theme: str = "light"):
        super().__init__(db, theme)
        
        # الألوان المتاحة
        self.colors = [
            "احمر", "ازرق", "اخضر", "اصفر", 
            "برتقالي", "بنفسجي", "وردي", "بني"
        ]

    def get_question(self):
        """عرض السؤال - كلمة لون بلون مختلف"""
        # اختيار كلمة (اسم لون)
        word = random.choice(self.colors)
        
        # اختيار اللون الفعلي (70% احتمال أن يكون مختلف)
        if random.random() < 0.7:
            # لون مختلف عن الكلمة
            color = random.choice([c for c in self.colors if c != word])
        else:
            # نفس اللون (لجعلها أصعب)
            color = word
        
        # الإجابة الصحيحة هي اللون وليس الكلمة
        self.current_answer = color
        
        hint = (
            f"السؤال {self.current_q + 1}/{self.total_q}\n"
            f"أجب باسم اللون وليس الكلمة!"
        )
        
        question_text = (
            f"ما لون هذه الكلمة؟\n\n"
            f"الكلمة: {word}\n"
            f"(تخيل أنها مكتوبة بلون {color})"
        )
        
        return self.build_question_flex(question_text, hint)

    def check_answer(self, answer: str) -> bool:
        """التحقق من اللون"""
        normalized = Config.normalize(answer)
        correct = Config.normalize(self.current_answer)
        
        return normalized == correct
