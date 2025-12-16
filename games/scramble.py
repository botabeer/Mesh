import random
from games.base import BaseGame
from config import Config


class ScrambleGame(BaseGame):
    """لعبة ترتيب مع مستويات صعوبة"""
    
    def __init__(self, db, theme: str = "light"):
        super().__init__(db, theme)
        self.game_name = "ترتيب"
        
        self.levels = {
            1: [
                "قلم", "كتاب", "باب", "نافذه", "سرير", "كرسي", "طاوله", "مكتب",
                "تفاح", "موز", "برتقال", "عنب", "شمس", "قمر", "نجم", "بحر"
            ],
            2: [
                "مدرسه", "جامعه", "مكتبه", "مستشفى", "حديقه", "ملعب", "سوق", "مطعم",
                "طائره", "سياره", "قطار", "حافله", "دراجه", "مركب", "باخره", "غواصه"
            ],
            3: [
                "حاسوب", "تلفون", "تلفزيون", "ثلاجه", "غسالة", "مكيف", "مروحه", "سخان",
                "اسد", "نمر", "فيل", "زرافه", "قرد", "حصان", "جمل", "غزال"
            ],
            4: [
                "معلومات", "تكنولوجيا", "انترنت", "برمجه", "تطبيق", "موقع", "منصه", "نظام",
                "مهندس", "طبيب", "معلم", "محامي", "صحفي", "كاتب", "رسام", "نحات"
            ],
            5: [
                "استقلال", "ديمقراطيه", "جمهوريه", "ملكيه", "برلمان", "حكومه", "وزاره", "سفاره",
                "مسؤوليه", "انضباط", "احترام", "تعاون", "صداقه", "امانه", "صدق", "وفاء"
            ]
        }
        
        self.all_words = []
        for words in self.levels.values():
            self.all_words.extend(words)
        random.shuffle(self.all_words)
        self.used = []

    def _get_difficulty(self):
        """تحديد مستوى الصعوبة حسب السؤال"""
        if self.current_q < 1:
            return 1
        elif self.current_q < 2:
            return 2
        elif self.current_q < 3:
            return 3
        elif self.current_q < 4:
            return 4
        else:
            return 5

    def _scramble(self, word: str, difficulty: int) -> str:
        """خلط الحروف حسب الصعوبة"""
        letters = list(word)
        attempts = difficulty * 3
        
        for _ in range(attempts):
            random.shuffle(letters)
            scrambled = ''.join(letters)
            if scrambled != word:
                return ' '.join(scrambled)
        
        return ' '.join(word[::-1])

    def get_question(self):
        """إنشاء سؤال حسب المستوى"""
        difficulty = self._get_difficulty()
        words = self.levels.get(difficulty, self.all_words)
        
        available = [w for w in words if w not in self.used]
        if not available:
            self.used = []
            available = words.copy()

        word = random.choice(available)
        self.used.append(word)
        self.current_answer = word

        scrambled = self._scramble(word, difficulty)
        hint = f"المستوى {difficulty} - رتب الحروف"
        return self.build_question_flex(scrambled, hint)

    def check_answer(self, answer: str) -> bool:
        """التحقق من الإجابة"""
        return Config.normalize(answer) == Config.normalize(self.current_answer)
