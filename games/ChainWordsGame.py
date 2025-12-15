import random
from games.base import BaseGame
from config import Config


class ChainWordsGame(BaseGame):
    """لعبة سلسلة الكلمات - كل كلمة تبدأ بآخر حرف من الكلمة السابقة"""
    
    def __init__(self, db, theme: str = "light"):
        super().__init__(db, theme)
        
        # بنك كلمات للعبة
        self.words = [
            "سياره", "تفاح", "قلم", "نجم", "كتاب", "باب", "رمل", "لعبه",
            "حديقه", "ورد", "دفتر", "معلم", "منزل", "شمس", "سفر", "رحله",
            "هدف", "فرح", "حلم", "مدرسه", "طالب", "بحر", "رمال", "ليل",
            "لون", "نور", "رسم", "موسيقى", "يوم", "مطر", "ريح", "حب",
            "بيت", "تلفون", "نافذه", "هاتف", "فيل", "لوحه", "هديه", "توت"
        ]
        
        # اختيار كلمة بداية عشوائية
        self.last_word = random.choice(self.words)
        
        # الكلمات المستخدمة في الجولة الحالية
        self.used = {self.last_word}
        
        # عداد المحاولات الخاطئة
        self.wrong_attempts = 0
        self.max_wrong = 2

    def get_question(self):
        """عرض السؤال مع الحرف المطلوب"""
        # آخر حرف من الكلمة السابقة
        last_letter = self.last_word[-1]
        
        hint = (
            f"السؤال {self.current_q + 1}/{self.total_q}\n"
            f"الكلمة السابقة: {self.last_word}\n"
            f"ابدأ بحرف: {last_letter}"
        )
        
        return self.build_question_flex(
            "اكتب كلمة جديدة",
            hint
        )

    def check_answer(self, answer: str) -> bool:
        """التحقق من الإجابة"""
        normalized = Config.normalize(answer)
        
        # التحقق من طول الكلمة
        if len(normalized) < 2:
            return False
        
        # الحرف المطلوب (آخر حرف من الكلمة السابقة)
        required_letter = Config.normalize(self.last_word[-1])
        first_letter = normalized[0]
        
        # التحقق من أن الكلمة تبدأ بالحرف الصحيح
        if first_letter != required_letter:
            return False
        
        # التحقق من عدم تكرار الكلمة
        if normalized in self.used:
            return False
        
        # إضافة الكلمة للمستخدمة
        self.used.add(normalized)
        
        # تحديث آخر كلمة
        self.last_word = answer.strip()
        
        return True
