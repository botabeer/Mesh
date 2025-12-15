import random
from games.base import BaseGame
from config import Config


class LettersWordsGame(BaseGame):
    """لعبة تكوين كلمات من مجموعة أحرف"""
    
    def __init__(self, db, theme: str = "light"):
        super().__init__(db, theme)
        
        # مجموعات الأحرف المختلفة
        self.letter_sets = [
            ["ق", "ل", "م", "ع", "ر", "ب"],  # قلم، علم، عرب
            ["س", "ا", "ر", "ه", "ي", "م"],  # سارة، سهر، مريم
            ["ك", "ت", "ا", "ب", "م", "ل"],  # كتاب، كلام، ملك
            ["د", "ر", "س", "ه", "م", "ا"],  # درس، مدرسة، سهم
            ["ح", "د", "ي", "ق", "ه", "ر"],  # حديقة، حدر، قدر
            ["ن", "و", "ر", "ا", "ل", "م"],  # نور، منار، رمال
            ["ش", "م", "س", "ا", "ل", "ر"],  # شمس، رمال، سر
            ["ب", "ح", "ر", "ا", "ل", "م"],  # بحر، رمال، حرب
            ["ج", "ب", "ل", "ا", "ر", "م"],  # جبل، رمال، مربع
            ["ف", "ر", "ح", "ا", "ل", "م"]   # فرح، مرح، حرف
        ]
        random.shuffle(self.letter_sets)
        
        # الكلمات التي تم إيجادها في السؤال الحالي
        self.found_words = set()
        
        # عدد الكلمات المطلوبة
        self.required = 3
        
        self.current_letters = None

    def get_question(self):
        """عرض السؤال مع الأحرف"""
        # اختيار مجموعة أحرف
        self.current_letters = self.letter_sets[self.current_q % len(self.letter_sets)]
        self.current_answer = self.current_letters
        
        # إعادة تعيين الكلمات المكتشفة
        self.found_words.clear()
        
        # عرض الأحرف
        letters_display = ' - '.join(self.current_letters)
        
        hint = (
            f"السؤال {self.current_q + 1}/{self.total_q}\n"
            f"مطلوب {self.required} كلمات صحيحة\n"
            f"وجدت: {len(self.found_words)}"
        )
        
        question_text = (
            f"كوّن كلمات من هذه الأحرف:\n\n"
            f"{letters_display}\n\n"
            f"يمكنك استخدام كل حرف أكثر من مرة"
        )
        
        return self.build_question_flex(question_text, hint)

    def check_answer(self, answer: str) -> bool:
        """التحقق من الإجابة"""
        normalized = Config.normalize(answer)
        
        # التحقق من طول الكلمة
        if len(normalized) < 2:
            return False
        
        # التحقق من عدم تكرار الكلمة
        if normalized in self.found_words:
            return False
        
        # التحقق من أن جميع أحرف الكلمة موجودة في المجموعة المتاحة
        available_letters = [Config.normalize(letter) for letter in self.current_letters]
        
        # نسمح باستخدام كل حرف عدة مرات
        for char in normalized:
            if char not in available_letters:
                return False
        
        # إضافة الكلمة للمكتشفة
        self.found_words.add(normalized)
        
        # التحقق من الوصول للعدد المطلوب
        if len(self.found_words) >= self.required:
            return True
        
        # إذا لم نصل للعدد المطلوب، نعتبرها إجابة جزئية صحيحة
        # لكن لا ننتقل للسؤال التالي
        return False
