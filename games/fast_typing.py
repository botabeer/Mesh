import random
import time
from games.base import BaseGame


class FastTypingGame(BaseGame):
    """لعبة اسرع مع توقيت"""
    
    def __init__(self, db, theme: str = "light"):
        super().__init__(db, theme)
        self.game_name = "اسرع"
        self.time_limit = 10
        self.start_time = None
        
        self.phrases = [
            "سبحان الله", "الحمد لله", "الله اكبر", "لا اله الا الله",
            "استغفر الله العظيم", "لا حول ولا قوة الا بالله", "بسم الله الرحمن الرحيم",
            "اللهم صل على محمد", "رب اغفر لي", "يا رب العالمين",
            "الصبر مفتاح الفرج", "من جد وجد", "العلم نور", "الوقت كالسيف",
            "العقل السليم في الجسم السليم", "اتق الله حيثما كنت", "قل خيرا او اصمت",
            "الصدق منجاة", "الكذب مهلكة", "الامانة صفة المؤمنين",
            "العمل عبادة", "طلب العلم فريضة", "النظافة من الايمان",
            "التواضع من شيم الكرام", "الكتاب خير جليس", "القراءة غذاء العقل",
            "الحكمة ضالة المؤمن", "العدل اساس الملك", "الظلم ظلمات",
            "الرفق ما كان في شيء الا زانه", "البر لا يبلى", "الاحسان الى الناس",
            "صلة الرحم تزيد في العمر", "بر الوالدين", "احترام الكبير",
            "العطف على الصغير", "مساعدة المحتاج", "اطعام الطعام",
            "الكلمة الطيبة صدقة", "التبسم في وجه اخيك صدقة", "ازالة الاذى عن الطريق",
            "حفظ اللسان", "غض البصر", "الصلاة عماد الدين",
            "الزكاة تطهر المال", "الصوم جنة", "الحج ركن من اركان الاسلام",
            "قراءة القران", "ذكر الله", "الدعاء مخ العبادة",
            "التوبة باب مفتوح", "الاستغفار يمحو الذنوب", "الصدقة تطفئ الخطيئة",
            "العفو عند المقدرة", "الصفح الجميل", "الحلم سيد الاخلاق"
        ]
        random.shuffle(self.phrases)
        self.used = []

    def get_question(self):
        """إنشاء سؤال مع توقيت"""
        available = [p for p in self.phrases if p not in self.used]
        if not available:
            self.used = []
            available = self.phrases.copy()

        phrase = random.choice(available)
        self.used.append(phrase)
        self.current_answer = phrase
        self.start_time = time.time()

        hint = f"اكتب بسرعة - {self.time_limit} ثانية"
        return self.build_question_flex(phrase, hint)

    def check_answer(self, answer: str) -> bool:
        """التحقق مع الوقت"""
        if self.start_time is None:
            return False
        
        elapsed = time.time() - self.start_time
        
        if elapsed > self.time_limit:
            return False
        
        return answer.strip() == self.current_answer
