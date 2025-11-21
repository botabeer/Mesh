"""
games/letters_game.py - لعبة تكوين الكلمات
"""

import random
import json
import os
from .base_game import BaseGame

class LettersGame(BaseGame):
    """لعبة تكوين الكلمات من حروف معينة"""
    
    # مجموعات الحروف مع الكلمات الصحيحة
    LETTER_SETS = [
        {'letters': ['ق', 'ي', 'ر', 'ل', 'ر', 'ل'], 'words': ['قرر', 'ليرة', 'رير', 'قلي', 'يقر']},
        {'letters': ['ك', 'ت', 'ا', 'ب', 'ة', 'ل'], 'words': ['كتاب', 'كتب', 'تاب', 'بات', 'كتابة']},
        {'letters': ['س', 'م', 'ا', 'ء', 'ع', 'ل'], 'words': ['سماء', 'سما', 'علم', 'سام', 'عام']},
        {'letters': ['م', 'د', 'ر', 'س', 'ة', 'ت'], 'words': ['مدرسة', 'درس', 'مدرس', 'ستر', 'درست']},
        {'letters': ['ح', 'ب', 'ي', 'ب', 'ت', 'ي'], 'words': ['حبيب', 'حبيبتي', 'حب', 'بيت', 'يحب']},
        {'letters': ['ج', 'م', 'ي', 'ل', 'ة', 'ا'], 'words': ['جميل', 'جميلة', 'جمال', 'ميل', 'جام']},
        {'letters': ['ع', 'ر', 'ب', 'ي', 'ة', 'ل'], 'words': ['عربية', 'عربي', 'عرب', 'ربي', 'بير']},
        {'letters': ['س', 'ع', 'ا', 'د', 'ة', 'ي'], 'words': ['سعادة', 'سعيد', 'سعد', 'عيد', 'ساعد']},
    ]
    
    def __init__(self):
        super().__init__()
        self.name = "لعبة تكوين الكلمات"
        self.description = "كوّن كلمات من الحروف المعطاة"
        self.current_set = None
        self.letters = []
        self.valid_words = []
        self.found_words = []
        self.words_to_find = 3
        self._load_round()
    
    def _load_round(self):
        """تحميل جولة جديدة"""
        self.current_set = random.choice(self.LETTER_SETS)
        self.letters = self.current_set['letters'].copy()
        random.shuffle(self.letters)
        self.valid_words = self.current_set['words'].copy()
        self.found_words = []
    
    def start(self):
        """بدء اللعبة"""
        question = f"كوّن {self.words_to_find} كلمات من هذه الحروف\nاكتب كلمة واحدة في كل رسالة"
        return self.create_game_screen(question, self.letters)
    
    def check_answer(self, answer: str) -> tuple:
        """التحقق من الإجابة"""
        answer = answer.strip()
        
        # التحقق من الكلمة
        if answer in self.valid_words and answer not in self.found_words:
            self.found_words.append(answer)
            points = self.calculate_points()
            
            # مكافأة للكلمات الطويلة
            if len(answer) >= 5:
                points += 5
            elif len(answer) >= 4:
                points += 2
            
            return True, points
        
        return False, 0
    
    def get_hint(self) -> str:
        """الحصول على تلميح"""
        self.hint_used = True
        remaining = [w for w in self.valid_words if w not in self.found_words]
        if remaining:
            word = random.choice(remaining)
            return f"كلمة تبدأ بـ '{word[0]}' وطولها {len(word)} حروف"
        return "لقد وجدت كل الكلمات!"
    
    def get_solution(self) -> str:
        """الحصول على الحل"""
        remaining = [w for w in self.valid_words if w not in self.found_words]
        if remaining:
            return f"الكلمات المتبقية: {', '.join(remaining[:3])}"
        return "لقد وجدت كل الكلمات!"
    
    def next_round(self):
        """الانتقال للجولة التالية"""
        super().next_round()
        self._load_round()
    
    def is_finished(self) -> bool:
        """هل انتهت اللعبة؟"""
        return len(self.found_words) >= self.words_to_find or super().is_finished()
