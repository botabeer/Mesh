import random
from games.base import BaseGame
from config import Config


class ChainWordsGame(BaseGame):
    def __init__(self, db, theme="light"):
        super().__init__(db, theme)
        self.game_name = "سلسله"
        self.supports_hint = False
        self.supports_reveal = False
        
        self.words = [
            "سياره", "تفاح", "قلم", "نجم", "كتاب", "باب", "رمل", "لعبه",
            "حديقه", "ورد", "دفتر", "معلم", "منزل", "شمس", "سفر", "رحله",
            "هدف", "فرح", "حلم", "مدرسه", "طالب", "بحر", "رمال", "ليل",
            "لون", "نور", "رسم", "موسيقى", "يوم", "مطر", "ريح", "حب",
            "بيت", "تلفون", "نافذه", "هاتف", "فيل", "لوحه", "هديه", "توت"
        ]
        
        self.last_word = random.choice(self.words)
        self.used = {self.last_word}
        self.error_message = None

    def get_question(self):
        last_letter = self.last_word[-1]
        
        hint = f"السؤال {self.current_q + 1}/{self.total_q}"
        question = f"الكلمة السابقة: {self.last_word}\n\nابدا بحرف: {last_letter}"
        
        return self.build_question_flex(question, hint)

    def check_answer(self, answer):
        normalized = Config.normalize(answer)
        
        if len(normalized) < 2:
            self.error_message = "الكلمة قصيرة جدا"
            return False
        
        required_letter = Config.normalize(self.last_word[-1])
        first_letter = normalized[0]
        
        if first_letter != required_letter:
            self.error_message = f"يجب ان تبدأ الكلمة بحرف: {required_letter}"
            return False
        
        if normalized in self.used:
            self.error_message = "هذه الكلمة مستخدمة بالفعل"
            return False
        
        self.used.add(normalized)
        self.last_word = answer.strip()
        self.error_message = None
        
        return True
