"""
games/chain_game.py - لعبة سلسلة الكلمات
"""

import random
from .base_game import BaseGame

class ChainGame(BaseGame):
    """لعبة سلسلة الكلمات - كل كلمة تبدأ بالحرف الأخير من السابقة"""
    
    STARTER_WORDS = ['شمس', 'قمر', 'بحر', 'نهر', 'جبل', 'سماء', 'أرض', 'ماء', 'هواء', 'نار']
    
    # قاموس للتحقق من الكلمات (يمكن توسيعه)
    VALID_WORDS = {
        'س': ['سماء', 'سيارة', 'سمك', 'سعيد', 'سوق', 'سرير', 'ساعة', 'سلام', 'سفينة'],
        'ر': ['رجل', 'ريح', 'رمل', 'رسالة', 'رحلة', 'رائع', 'رخيص', 'رقم', 'رمان'],
        'ل': ['ليل', 'لون', 'لعبة', 'لبن', 'ليمون', 'لحم', 'لغة', 'لوحة', 'لؤلؤ'],
        'م': ['ماء', 'منزل', 'مدرسة', 'مسجد', 'موز', 'ملعب', 'مطبخ', 'مفتاح', 'ملك'],
        'ء': ['ماء', 'سماء', 'هواء', 'دواء', 'غذاء', 'بناء', 'شتاء', 'صحراء'],
        'ي': ['يد', 'يوم', 'ياسمين'],
        'ة': ['سيارة', 'طائرة', 'لعبة', 'رسالة', 'مدرسة', 'حديقة', 'شجرة', 'زهرة'],
        'ن': ['نهر', 'نجم', 'نور', 'نبات', 'نافذة', 'نملة', 'نسر', 'نخلة'],
        'ا': ['أسد', 'أرض', 'أمل', 'أخ', 'أب', 'أم'],
        'ب': ['بحر', 'بيت', 'باب', 'برتقال', 'بنت', 'بستان', 'بطيخ'],
        'ت': ['تفاح', 'تمر', 'ترس', 'تاج', 'تراب'],
        'ث': ['ثلج', 'ثعلب', 'ثوب', 'ثمرة'],
        'ج': ['جبل', 'جمل', 'جنة', 'جسر', 'جدار', 'جزيرة'],
        'ح': ['حب', 'حديقة', 'حصان', 'حمام', 'حليب'],
        'خ': ['خبز', 'خيل', 'خيمة', 'خريف', 'خضار'],
        'د': ['دار', 'دجاج', 'دب', 'دفتر', 'دواء'],
        'ذ': ['ذهب', 'ذيل', 'ذرة'],
        'ز': ['زهرة', 'زيتون', 'زرافة', 'زجاج'],
        'ش': ['شمس', 'شجرة', 'شتاء', 'شاي', 'شارع'],
        'ص': ['صباح', 'صحراء', 'صقر', 'صديق'],
        'ض': ['ضوء', 'ضفدع', 'ضيف'],
        'ط': ['طائر', 'طفل', 'طعام', 'طريق', 'طماطم'],
        'ظ': ['ظل', 'ظهر', 'ظرف'],
        'ع': ['عين', 'عسل', 'عصفور', 'علم', 'عنب'],
        'غ': ['غابة', 'غزال', 'غيمة', 'غراب'],
        'ف': ['فراشة', 'فيل', 'فاكهة', 'فجر', 'فصل'],
        'ق': ['قمر', 'قلم', 'قلب', 'قطة', 'قهوة'],
        'ك': ['كتاب', 'كلب', 'كرسي', 'كوب', 'كهف'],
        'ه': ['هواء', 'هلال', 'هدية', 'هرم'],
        'و': ['ورد', 'وردة', 'وجه', 'ولد'],
    }
    
    def __init__(self):
        super().__init__()
        self.name = "لعبة سلسلة الكلمات"
        self.description = "اكتب كلمة تبدأ بالحرف الأخير"
        self.chain = []
        self.last_letter = ''
        self._start_chain()
    
    def _start_chain(self):
        """بدء سلسلة جديدة"""
        starter = random.choice(self.STARTER_WORDS)
        self.chain = [starter]
        self.last_letter = self._get_last_letter(starter)
    
    def _get_last_letter(self, word):
        """الحصول على الحرف الأخير (مع معالجة التاء المربوطة)"""
        last = word[-1]
        if last == 'ة':
            return 'ت'  # أو يمكن قبول 'ة' أيضاً
        return last
    
    def start(self):
        """بدء اللعبة"""
        question = f"الكلمة: {self.chain[-1]}\n\nاكتب كلمة تبدأ بحرف '{self.last_letter}'"
        return self.create_game_screen(question)
    
    def check_answer(self, answer: str) -> tuple:
        """التحقق من الإجابة"""
        answer = answer.strip()
        
        # التحقق من أن الكلمة تبدأ بالحرف الصحيح
        if not answer:
            return False, 0
        
        first_letter = answer[0]
        if first_letter != self.last_letter and not (self.last_letter == 'ت' and first_letter == 'ة'):
            return False, 0
        
        # التحقق من أن الكلمة ليست مكررة
        if answer in self.chain:
            return False, 0
        
        # التحقق من أن الكلمة طولها مناسب
        if len(answer) < 2:
            return False, 0
        
        # إضافة الكلمة للسلسلة
        self.chain.append(answer)
        self.last_letter = self._get_last_letter(answer)
        
        points = self.calculate_points()
        # مكافأة للكلمات الطويلة
        if len(answer) >= 5:
            points += 5
        # مكافأة للسلسلة الطويلة
        if len(self.chain) >= 5:
            points += 3
        
        return True, points
    
    def get_hint(self) -> str:
        """الحصول على تلميح"""
        self.hint_used = True
        if self.last_letter in self.VALID_WORDS:
            examples = self.VALID_WORDS[self.last_letter]
            valid = [w for w in examples if w not in self.chain]
            if valid:
                return f"مثال: {random.choice(valid)[:2]}..."
        return f"ابحث عن كلمة تبدأ بـ '{self.last_letter}'"
    
    def get_solution(self) -> str:
        """الحصول على الحل"""
        if self.last_letter in self.VALID_WORDS:
            examples = self.VALID_WORDS[self.last_letter]
            valid = [w for w in examples if w not in self.chain]
            if valid:
                return f"أمثلة: {', '.join(valid[:3])}"
        return f"أي كلمة تبدأ بـ '{self.last_letter}'"
    
    def next_round(self):
        """الانتقال للجولة التالية"""
        super().next_round()
        # استمرار السلسلة أو بدء جديدة
        if len(self.chain) >= 10:
            self._start_chain()
