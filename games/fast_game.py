"""
games/fast_game.py - لعبة أسرع إجابة
"""

import random
import time
from .base_game import BaseGame

class FastGame(BaseGame):
    """لعبة أسرع إجابة - أول من يجيب يفوز"""
    
    QUESTIONS = [
        {'q': "اكتب كلمة تبدأ بحرف 'ع'", 'starts_with': 'ع', 'examples': ['عمر', 'علي', 'عائشة', 'عبد', 'عين', 'عسل', 'عقل']},
        {'q': "اكتب كلمة تبدأ بحرف 'س'", 'starts_with': 'س', 'examples': ['سماء', 'سعيد', 'سمك', 'سيارة', 'سوق']},
        {'q': "اكتب كلمة تبدأ بحرف 'م'", 'starts_with': 'م', 'examples': ['محمد', 'مدرسة', 'ماء', 'مسجد', 'موز']},
        {'q': "اكتب كلمة تبدأ بحرف 'ب'", 'starts_with': 'ب', 'examples': ['بيت', 'باب', 'برتقال', 'بحر', 'بنت']},
        {'q': "اكتب كلمة تبدأ بحرف 'ك'", 'starts_with': 'ك', 'examples': ['كتاب', 'كرسي', 'كلب', 'كبير', 'كريم']},
        {'q': "اكتب اسم فاكهة", 'category': 'fruit', 'examples': ['تفاح', 'موز', 'برتقال', 'عنب', 'مانجو', 'فراولة']},
        {'q': "اكتب اسم حيوان", 'category': 'animal', 'examples': ['أسد', 'قط', 'كلب', 'فيل', 'نمر', 'غزال']},
        {'q': "اكتب اسم بلد عربي", 'category': 'country', 'examples': ['مصر', 'السعودية', 'الإمارات', 'الأردن', 'لبنان']},
        {'q': "اكتب اسم لون", 'category': 'color', 'examples': ['أحمر', 'أزرق', 'أخضر', 'أصفر', 'أبيض', 'أسود']},
        {'q': "اكتب رقم بين 1 و 100", 'type': 'number', 'range': (1, 100)},
    ]
    
    def __init__(self):
        super().__init__()
        self.name = "لعبة أسرع إجابة"
        self.description = "أسرع من يجيب يفوز!"
        self.points_per_answer = 20
        self.answered = False
        self.start_time = None
        self._load_question()
    
    def _load_question(self):
        """تحميل سؤال جديد"""
        self.current_question = random.choice(self.QUESTIONS)
        self.answered = False
        self.start_time = time.time()
    
    def start(self):
        """بدء اللعبة"""
        return self.create_game_screen(self.current_question['q'])
    
    def check_answer(self, answer: str) -> tuple:
        """التحقق من الإجابة"""
        if self.answered:
            return False, 0
        
        answer = answer.strip()
        q = self.current_question
        is_correct = False
        
        # التحقق حسب نوع السؤال
        if 'starts_with' in q:
            is_correct = answer.startswith(q['starts_with']) and len(answer) >= 2
        elif 'category' in q:
            is_correct = answer in q['examples'] or len(answer) >= 2
        elif 'type' in q and q['type'] == 'number':
            try:
                num = int(answer)
                is_correct = q['range'][0] <= num <= q['range'][1]
            except:
                is_correct = False
        
        if is_correct:
            self.answered = True
            # مكافأة السرعة
            elapsed = time.time() - self.start_time
            points = self.calculate_points()
            if elapsed < 3:
                points += 10  # مكافأة السرعة الفائقة
            elif elapsed < 5:
                points += 5   # مكافأة السرعة
            return True, points
        
        return False, 0
    
    def get_hint(self) -> str:
        """الحصول على تلميح"""
        self.hint_used = True
        q = self.current_question
        if 'examples' in q:
            return f"مثال: {q['examples'][0]}"
        elif 'starts_with' in q:
            return f"ابدأ بحرف '{q['starts_with']}'"
        return "فكر بسرعة!"
    
    def get_solution(self) -> str:
        """الحصول على الحل"""
        q = self.current_question
        if 'examples' in q:
            return f"أمثلة: {', '.join(q['examples'][:3])}"
        return "لا يوجد حل محدد"
    
    def next_round(self):
        """الانتقال للجولة التالية"""
        super().next_round()
        self._load_question()
