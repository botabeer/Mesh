import random
from games.base import BaseGame
from config import Config


class HumanAnimalPlantGame(BaseGame):
    """لعبة إنسان حيوان نبات جماد بلاد"""
    
    def __init__(self, db, theme: str = "light"):
        super().__init__(db, theme)
        
        # الأحرف المتاحة
        self.letters = list("ابتجحدرزسشصطعفقكلمنهوي")
        random.shuffle(self.letters)
        
        # الفئات المختلفة
        self.categories = ["انسان", "حيوان", "نبات", "جماد", "بلاد"]
        
        self.current_category = None
        self.current_letter = None

    def get_question(self):
        """عرض السؤال مع الحرف والفئة"""
        # اختيار حرف (بالتناوب من القائمة)
        self.current_letter = self.letters[self.current_q % len(self.letters)]
        
        # اختيار فئة عشوائية
        self.current_category = random.choice(self.categories)
        
        # حفظ الإجابة المتوقعة (الحرف فقط للمقارنة)
        self.current_answer = self.current_letter
        
        hint = f"السؤال {self.current_q + 1}/{self.total_q}"
        
        question_text = (
            f"الفئة: {self.current_category}\n\n"
            f"الحرف: {self.current_letter}\n\n"
            f"اكتب كلمة من فئة {self.current_category} تبدأ بحرف {self.current_letter}"
        )
        
        return self.build_question_flex(question_text, hint)

    def check_answer(self, answer: str) -> bool:
        """التحقق من الإجابة"""
        normalized = Config.normalize(answer)
        
        # التحقق من طول الكلمة
        if len(normalized) < 2:
            return False
        
        # التحقق من أن الكلمة تبدأ بالحرف الصحيح
        first_letter = normalized[0]
        required_letter = Config.normalize(self.current_letter)[0]
        
        return first_letter == required_letter
