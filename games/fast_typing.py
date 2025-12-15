import random
from games.base import BaseGame


class FastTypingGame(BaseGame):
    def __init__(self, db, theme: str = "light"):
        super().__init__(db, theme)
        
        self.phrases = [
            "سبحان الله", "الحمد لله", "الله اكبر", "لا اله الا الله",
            "رب اغفر لي", "توكل على الله", "الصبر مفتاح الفرج", "من جد وجد",
            "العلم نور", "راحة القلب في الذكر", "اللهم اهدنا", "كن محسنا",
            "رب زدني علما", "اتق الله", "خير الامور اوسطها",
            "اللهم اشف مرضانا", "التواضع رفعه", "الصدق منجاه", "الصمت حكمه",
            "اللهم ارزقني رضاك", "النيه الصالحه بركه", "استغفر الله العظيم"
        ]
        random.shuffle(self.phrases)
        self.used = []

    def get_question(self):
        available = [p for p in self.phrases if p not in self.used]
        if not available:
            self.used = []
            available = self.phrases.copy()

        phrase = random.choice(available)
        self.used.append(phrase)
        self.current_answer = phrase

        hint = f"السؤال {self.current_q + 1}/{self.total_q}\nاكتب بالضبط"
        return self.build_question_flex(phrase, hint)

    def check_answer(self, answer: str) -> bool:
        return answer.strip() == self.current_answer
