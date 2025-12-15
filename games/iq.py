import random
from games.base import BaseGame


class IqGame(BaseGame):
    """لعبة الذكاء - الغاز"""
    
    def __init__(self, db, theme: str = "light"):
        super().__init__(db, theme)
        
        self.riddles = [
            {"q": "ما الشيء الذي يمشي بلا ارجل ويبكي بلا عيون", "a": ["السحاب", "الغيم", "سحاب", "غيم"]},
            {"q": "له راس ولكن لا عين له", "a": ["الدبوس", "المسمار", "دبوس", "مسمار"]},
            {"q": "شيء كلما زاد نقص", "a": ["العمر", "الوقت", "عمر", "وقت"]},
            {"q": "يكتب ولا يقرا ابدا", "a": ["القلم", "قلم"]},
            {"q": "له اسنان كثيره ولكنه لا يعض", "a": ["المشط", "مشط"]},
            {"q": "يوجد في الماء ولكن الماء يميته", "a": ["الملح", "ملح"]},
            {"q": "يتكلم بجميع اللغات دون ان يتعلمها", "a": ["الصدي", "صدي"]},
            {"q": "شيء كلما اخذت منه كبر", "a": ["الحفره", "حفره"]},
            {"q": "يخترق الزجاج ولا يكسره", "a": ["الضوء", "النور", "ضوء", "نور"]},
            {"q": "يسمع بلا اذن ويتكلم بلا لسان", "a": ["الهاتف", "الجوال", "هاتف", "جوال"]}
        ]
        random.shuffle(self.riddles)
        self.used_riddles = []
    
    def get_question(self):
        available = [r for r in self.riddles if r not in self.used_riddles]
        if not available:
            self.used_riddles = []
            available = self.riddles.copy()
        
        riddle = random.choice(available)
        self.used_riddles.append(riddle)
        self.current_answer = riddle["a"]
        
        hint = f"السؤال {self.current_q + 1}/{self.total_q}"
        return self.build_question_flex(riddle["q"], hint)
    
    def check_answer(self, answer: str) -> bool:
        normalized = Config.normalize(answer)
        return any(Config.normalize(a) == normalized for a in self.current_answer)
