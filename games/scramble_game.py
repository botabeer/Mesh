"""
games/scramble_game.py - لعبة ترتيب الحروف
"""

import random
from .base_game import BaseGame

class ScrambleGame(BaseGame):
    """لعبة ترتيب الحروف المبعثرة"""
    
    WORDS = [
        {'word': 'مدرسة', 'hint': 'مكان للتعلم'},
        {'word': 'سيارة', 'hint': 'وسيلة نقل'},
        {'word': 'طائرة', 'hint': 'تطير في السماء'},
        {'word': 'كتاب', 'hint': 'نقرأ فيه'},
        {'word': 'قلم', 'hint': 'نكتب به'},
        {'word': 'شمس', 'hint': 'تضيء النهار'},
        {'word': 'قمر', 'hint': 'يضيء الليل'},
        {'word': 'بحر', 'hint': 'ماء مالح'},
        {'word': 'جبل', 'hint': 'مرتفع من الأرض'},
        {'word': 'نهر', 'hint': 'ماء عذب يجري'},
        {'word': 'زهرة', 'hint': 'نبات جميل'},
        {'word': 'شجرة', 'hint': 'نبات كبير'},
        {'word': 'طفل', 'hint': 'صغير السن'},
        {'word': 'منزل', 'hint': 'نسكن فيه'},
        {'word': 'حديقة', 'hint': 'مكان للنباتات'},
        {'word': 'مستشفى', 'hint': 'مكان للعلاج'},
        {'word': 'مطعم', 'hint': 'نأكل فيه'},
        {'word': 'ملعب', 'hint': 'نلعب فيه'},
    ]
    
    def __init__(self):
        super().__init__()
        self.name = "لعبة ترتيب الحروف"
        self.description = "رتب الحروف لتكوين كلمة صحيحة"
        self.current_word_data = None
        self.scrambled = []
        self._load_word()
    
    def _load_word(self):
        """تحميل كلمة جديدة"""
        self.current_word_data = random.choice(self.WORDS)
        word = self.current_word_data['word']
        self.current_answer = word
        
        # بعثرة الحروف
        letters = list(word)
        while True:
            random.shuffle(letters)
            if ''.join(letters) != word:  # تأكد من أنها مختلفة
                break
        self.scrambled = letters
    
    def start(self):
        """بدء اللعبة"""
        question = "رتب هذه الحروف لتكوين كلمة صحيحة"
        return self.create_game_screen(question, self.scrambled)
    
    def check_answer(self, answer: str) -> tuple:
        """التحقق من الإجابة"""
        answer = answer.strip()
        
        if answer == self.current_answer:
            points = self.calculate_points()
            # مكافأة للكلمات الطويلة
            if len(self.current_answer) >= 5:
                points += 5
            return True, points
        
        return False, 0
    
    def get_hint(self) -> str:
        """الحصول على تلميح"""
        self.hint_used = True
        hint = self.current_word_data['hint']
        first_letter = self.current_answer[0]
        return f"{hint} - تبدأ بـ '{first_letter}'"
    
    def get_solution(self) -> str:
        """الحصول على الحل"""
        return self.current_answer
    
    def next_round(self):
        """الانتقال للجولة التالية"""
        super().next_round()
        self._load_word()
