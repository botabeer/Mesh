"""
لعبة الذكاء - مثال
ضع هذا الملف في مجلد games/
"""

import random
from base_game import Game

class IqGame(Game):
    """🧠 لعبة الذكاء"""
    
    def __init__(self, mode="فردي"):
        super().__init__("ذكاء", mode)
        self.questions = [
            {"q": "ما يمشي بلا أرجل ويبكي بلا عيون؟", "a": ["السحاب", "الغيم", "سحاب", "غيم"]},
            {"q": "له رأس ولا عين له؟", "a": ["الدبوس", "دبوس", "المسمار", "مسمار"]},
            {"q": "كلما زاد نقص؟", "a": ["العمر", "عمر", "الوقت", "وقت"]},
            {"q": "يكتب ولا يقرأ؟", "a": ["القلم", "قلم"]},
            {"q": "له أسنان ولا يعض؟", "a": ["المشط", "مشط"]},
            {"q": "في الماء ولكن الماء يميته؟", "a": ["الملح", "ملح"]},
            {"q": "يتكلم بكل اللغات؟", "a": ["الصدى", "صدى"]},
            {"q": "يؤخذ منك قبل أن تعطيه؟", "a": ["الصورة", "صورة"]},
        ]
        random.shuffle(self.questions)
    
    def generate_question(self):
        q_data = self.questions[(self.current_round - 1) % len(self.questions)]
        self.current_question = q_data["q"]
        self.current_answer = q_data["a"]
    
    def _check_answer_logic(self, answer):
        answer = answer.strip().lower()
        for correct in self.current_answer:
            if answer == correct.lower():
                return True
        return False
