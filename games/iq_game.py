"""
لعبة أسئلة الذكاء - محسنة
Created by: Abeer Aldosari © 2025
"""
from .base_game import BaseGame
import random
import difflib

class IqGame(BaseGame):
    """لعبة أسئلة الذكاء"""
    
    def __init__(self, line_api):
        super().__init__(line_api, rounds=5)
        
        self.questions = [
            {"q": "ما هو الشيء الذي يمشي بلا أرجل ويبكي بلا عيون؟", "a": "السحاب", "hint": "يُرى في السماء ويجلب المطر"},
            {"q": "ما هو الشيء الذي له رأس ولا يملك عيون؟", "a": "الدبوس", "hint": "أداة صغيرة للتثبيت"},
            {"q": "شيء موجود في السماء إذا أضفت له حرفاً أصبح في الأرض؟", "a": "نجم", "hint": "يضيء ليلاً، أضف حرف الميم"},
            {"q": "ما الشيء الذي كلما زاد نقص؟", "a": "العمر", "hint": "يمر بالإنسان ولا يعود"},
            {"q": "له عين ولا يرى؟", "a": "الإبرة", "hint": "تستخدم في الخياطة"},
            {"q": "ما هو الشيء الذي يكتب ولا يقرأ؟", "a": "القلم", "hint": "أداة للكتابة"},
            {"q": "ما الشيء الذي له أسنان ولا يعض؟", "a": "المشط", "hint": "يستخدم للشعر"},
            {"q": "ما هو الشيء الذي يسمع بلا أذن ويتكلم بلا لسان؟", "a": "الهاتف", "hint": "جهاز اتصال"},
            {"q": "ما الشيء الذي له أربع أرجل ولا يمشي؟", "a": "الكرسي", "hint": "نجلس عليه"},
            {"q": "ما الذي يقرصك ولا تراه؟", "a": "الجوع", "hint": "شعور في المعدة"},
            {"q": "ما الشيء الذي إذا أكلته كله تستفيد وإذا أكلت نصفه تموت؟", "a": "السمسم", "hint": "حبوب صغيرة"},
            {"q": "حامل ومحمول نصفه ناشف ونصفه مبلول؟", "a": "السفينة", "hint": "تسير في البحر"},
            {"q": "ما الشيء الذي إذا لمسته صاح؟", "a": "الجرس", "hint": "يصدر صوتاً عند اللمس"}
        ]
        random.shuffle(self.questions)

    def start_game(self):
        """بدء اللعبة"""
        self.current_round = 0
        return self.generate_question()

    def generate_question(self):
        """توليد سؤال جديد"""
        q_data = self.questions[self.current_round % len(self.questions)]
        self.current_answer = q_data['a']
        self.current_hint = q_data['hint']
        
        extra_info = "💡 فكر جيداً\n• لمح: للحصول على تلميح\n• جاوب: لمعرفة الإجابة"
        
        return self.build_question_flex("سؤال ذكاء 🧠", q_data['q'], extra_info)

    def check_answer(self, answer, uid, name):
        """فحص الإجابة"""
        normalized = self.normalize_text(answer)
        
        # تلميح
        if normalized == 'لمح':
            hint = f"💡 {self.current_hint}"
            return {
                'points': 0,
                'won': False,
                'response': self.build_question_flex(
                    "سؤال ذكاء 🧠",
                    hint,
                    "فكر جيداً"
                )
            }
        
        # عرض الإجابة
        if normalized == 'جاوب':
            self.current_round += 1
            is_final = self.current_round >= self.rounds
            
            if is_final:
                return {
                    'points': 0,
                    'won': False,
                    'response': self.build_result_flex(
                        "انتهت اللعبة",
                        f"الإجابة: {self.current_answer}",
                        0,
                        True
                    )
                }
            
            next_q = self.generate_question()
            return {
                'points': 0,
                'won': False,
                'response': next_q
            }
        
        # التحقق من الإجابة
        correct_normalized = self.normalize_text(self.current_answer)
        
        # مقارنة مع تحمل الأخطاء
        if (normalized == correct_normalized or 
            difflib.SequenceMatcher(None, normalized, correct_normalized).ratio() > 0.75):
            
            points = POINTS_PER_CORRECT
            self.add_player_score(uid, points)
            
            self.current_round += 1
            is_final = self.current_round >= self.rounds
            
            if is_final:
                return {
                    'points': points,
                    'won': True,
                    'response': self.build_result_flex(
                        name,
                        f"الإجابة: {self.current_answer}",
                        points,
                        True
                    )
                }
            
            next_q = self.generate_question()
            return {
                'points': points,
                'won': False,
                'response': next_q
            }
        
        return None
