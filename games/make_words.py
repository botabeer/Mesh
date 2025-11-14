import random
from itertools import permutations

USE_AI = False
AI_MODEL = None

class LettersWordsGame:
    def __init__(self, ai_model=None):
        global USE_AI, AI_MODEL
        if ai_model:
            USE_AI = True
            AI_MODEL = ai_model

        # الحروف المتاحة لتكوين الأسئلة
        self.letters_pool = ["ت", "ف", "ا", "ح", "ب", "ك", "ل", "م", "ر", "ش"]

        self.current_letters = []
        self.valid_words = set()
        self.used_words = set()
        self.tries = 3

    def generate_question(self):
        """توليد سؤال جديد"""
        self.current_letters = random.sample(self.letters_pool, 5)
        self.used_words = set()
        self.tries = 3

        # توليد كل الكلمات الممكنة من الحروف (حتى 5 حروف)
        all_words = set()
        for length in range(2, 6):
            for p in permutations(self.current_letters, length):
                word = "".join(p)
                all_words.add(word)

        self.valid_words = all_words

        return f"🔤 كوّن كلمة باستخدام هذه الحروف:\n{' '.join(self.current_letters)}\n\nلديك 3 محاولات!"

    def check_answer(self, answer):
        """فحص الإجابة"""
        normalized = answer.strip()

        # فحص التكرار
        if normalized in self.used_words:
            return {"correct": False, "message": "❗ تم استخدام هذه الكلمة سابقًا", "points": 0}

        # فحص التكوين من الحروف
        if normalized not in self.valid_words:
            self.tries -= 1
            msg = f"❌ كلمة غير صحيحة\nالمتبقي: {self.tries} محاولة"
            return {"correct": False, "message": msg, "points": 0}

        # إذا صحيحة
        self.used_words.add(normalized)

        # إضافة نقاط
        points = len(normalized) * 2

        # فوز تلقائي
        if len(self.used_words) >= 3:
            new_q = self.generate_question()
            return {
                "correct": True,
                "message": f" ممتاز! جمعت 3 كلمات صحيحة\n+20 نقطة\n\n{new_q}",
                "points": 20
            }

        remaining = 3 - len(self.used_words)

        return {
            "correct": True,
            "message": f"✓ كلمة صحيحة: {normalized}\nباقي {remaining} كلمات!",
            "points": points
        }
