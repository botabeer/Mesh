"""
games/iq_game.py - لعبة أسئلة الذكاء
"""

import random
from .base_game import BaseGame

class IQGame(BaseGame):
    """لعبة أسئلة الذكاء والألغاز"""
    
    QUESTIONS = [
        {'q': 'ما الذي له رأس ولا عين له؟', 'a': ['دبوس', 'مسمار', 'ابرة'], 'hint': 'أداة حادة'},
        {'q': 'ما الذي يمشي بلا أرجل؟', 'a': ['الماء', 'الهواء', 'الوقت', 'الساعة'], 'hint': 'يتحرك باستمرار'},
        {'q': 'كلما أخذت منه كبر؟', 'a': ['الحفرة', 'حفرة'], 'hint': 'في الأرض'},
        {'q': 'ما الذي يرتفع ولا ينزل؟', 'a': ['العمر', 'السن'], 'hint': 'يزداد مع الزمن'},
        {'q': 'له أسنان ولا يعض؟', 'a': ['المشط', 'مشط'], 'hint': 'للشعر'},
        {'q': 'ما الذي إذا دخل الماء لا يبتل؟', 'a': ['الضوء', 'النور'], 'hint': 'يضيء'},
        {'q': 'شيء يوجد في السماء وإذا أضفت إليه حرفاً أصبح في الأرض؟', 'a': ['نجم', 'منجم'], 'hint': 'يلمع ليلاً'},
        {'q': 'ما هو الشيء الذي لا يمشي إلا بالضرب؟', 'a': ['المسمار', 'مسمار'], 'hint': 'أداة بناء'},
        {'q': 'أخت خالك وليست خالتك؟', 'a': ['أمك', 'امك', 'الأم', 'الام'], 'hint': 'أقرب الناس'},
        {'q': 'ما هو الشيء الذي يسمع بلا أذن ويتكلم بلا لسان؟', 'a': ['الهاتف', 'التلفون', 'الجوال'], 'hint': 'جهاز اتصال'},
        {'q': '2 + 2 × 2 = ؟', 'a': ['6', '٦'], 'hint': 'تذكر ترتيب العمليات'},
        {'q': 'ما نصف نصف المئة؟', 'a': ['25', '٢٥', 'خمسة وعشرون'], 'hint': 'نصف 50'},
        {'q': 'إذا كان اليوم الخميس، ما هو اليوم بعد 3 أيام؟', 'a': ['الأحد', 'احد', 'الاحد'], 'hint': 'بداية الأسبوع'},
        {'q': 'كم عدد أحرف كلمة "خمسة"؟', 'a': ['4', '٤', 'أربعة', 'اربعة'], 'hint': 'عد الحروف'},
        {'q': 'ما هو الحيوان الذي يحمل بيته على ظهره؟', 'a': ['السلحفاة', 'سلحفاة', 'الحلزون', 'حلزون'], 'hint': 'بطيء الحركة'},
        {'q': 'ما هو أكبر كوكب في المجموعة الشمسية؟', 'a': ['المشتري', 'مشتري', 'جوبيتر'], 'hint': 'كوكب غازي عملاق'},
        {'q': 'كم عدد أيام السنة الكبيسة؟', 'a': ['366', '٣٦٦'], 'hint': 'أكثر من 365'},
        {'q': 'ما العنصر الأكثر وفرة في الكون؟', 'a': ['الهيدروجين', 'هيدروجين'], 'hint': 'أخف العناصر'},
    ]
    
    def __init__(self):
        super().__init__()
        self.name = "أسئلة الذكاء"
        self.description = "اختبر ذكاءك!"
        self.points_per_answer = 15
        self.used_questions = []
        self._load_question()
    
    def _load_question(self):
        """تحميل سؤال جديد"""
        available = [q for q in self.QUESTIONS if q['q'] not in self.used_questions]
        if not available:
            self.used_questions = []
            available = self.QUESTIONS
        
        self.current_question = random.choice(available)
        self.used_questions.append(self.current_question['q'])
        self.current_answer = self.current_question['a'][0]
    
    def start(self):
        """بدء اللعبة"""
        return self.create_game_screen(self.current_question['q'])
    
    def check_answer(self, answer: str) -> tuple:
        """التحقق من الإجابة"""
        answer = answer.strip().lower()
        valid_answers = [a.lower() for a in self.current_question['a']]
        
        if answer in valid_answers:
            points = self.calculate_points()
            return True, points
        
        # التحقق من التشابه
        for valid in valid_answers:
            if answer in valid or valid in answer:
                points = self.calculate_points() - 2  # خصم بسيط للإجابة غير الدقيقة
                return True, max(points, 5)
        
        return False, 0
    
    def get_hint(self) -> str:
        """الحصول على تلميح"""
        self.hint_used = True
        return self.current_question['hint']
    
    def get_solution(self) -> str:
        """الحصول على الحل"""
        return self.current_answer
    
    def next_round(self):
        """الانتقال للجولة التالية"""
        super().next_round()
        self._load_question()
