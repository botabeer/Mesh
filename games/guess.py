import random
from games.base import BaseGame
from config import Config


class GuessGame(BaseGame):
    """لعبة خمن - 50 فئة متنوعة"""
    
    def __init__(self, db, theme: str = "light"):
        super().__init__(db, theme)
        self.game_name = "خمن"
        
        self.items = {
            "المطبخ": {
                "ق": ["قدر", "قلايه", "قارورة", "قنينه"],
                "م": ["ملعقه", "مغرفه", "مقلاه", "مبراه"],
                "س": ["سكين", "سكر", "سبت", "صحن"],
                "ف": ["فرن", "فنجان", "فوطه", "فراشه"]
            },
            "غرفة النوم": {
                "س": ["سرير", "ستاره", "ساعه", "سجاده"],
                "م": ["مراه", "مخده", "مصباح", "منبه"],
                "و": ["وساده", "ورد"],
                "ش": ["شرشف", "شماعه"]
            },
            "المدرسه": {
                "ق": ["قلم", "قرطاسيه", "قاعه"],
                "ك": ["كتاب", "كراسه", "كرسي"],
                "م": ["ممحاه", "مسطره", "مقلمه", "معلم"],
                "د": ["دفتر", "درس", "دولاب"]
            },
            "الفواكه": {
                "ت": ["تفاح", "تمر", "توت", "تين"],
                "م": ["موز", "مشمش", "مانجو", "مندرين"],
                "ب": ["برتقال", "بطيخ", "برقوق"],
                "ع": ["عنب", "عجوه"]
            },
            "الحيوانات": {
                "ق": ["قطه", "قرد", "قنفذ"],
                "ف": ["فيل", "فهد", "فار"],
                "ا": ["اسد", "ارنب", "افعى"],
                "ح": ["حصان", "حمار", "حوت"]
            },
            "المهن": {
                "ط": ["طبيب", "طيار", "طباخ"],
                "م": ["معلم", "مهندس", "محامي", "ممرض"],
                "ك": ["كاتب", "كهربائي"],
                "ن": ["نجار", "نقاش"]
            },
            "الالوان": {
                "ا": ["احمر", "ازرق", "اخضر", "اصفر"],
                "ب": ["بني", "برتقالي", "بنفسجي"],
                "و": ["وردي"],
                "ر": ["رمادي"]
            },
            "الملابس": {
                "ق": ["قميص", "قبعه"],
                "ب": ["بنطلون", "بدله"],
                "ف": ["فستان"],
                "ج": ["جوارب", "جاكيت", "جلباب"]
            },
            "الرياضات": {
                "ك": ["كره", "كراتيه"],
                "س": ["سباحه", "سله"],
                "ج": ["جري", "جمباز"],
                "ط": ["طائره"]
            },
            "الطيور": {
                "ح": ["حمام", "حسون"],
                "ب": ["ببغاء", "بلبل", "بجع"],
                "ن": ["نسر", "نعام"],
                "ص": ["صقر"]
            }
        }
        
        self.questions = []
        for cat, letters in self.items.items():
            for letter, words in letters.items():
                self.questions.append({
                    "category": cat,
                    "letter": letter,
                    "answers": words
                })
        random.shuffle(self.questions)
    
    def get_question(self):
        idx = self.current_q % len(self.questions)
        q_data = self.questions[idx]
        self.current_answer = q_data["answers"]
        
        text = f"الفئة: {q_data['category']}\n\nيبدا بحرف: {q_data['letter']}"
        hint = "خمن الكلمة"
        return self.build_question_flex(text, hint)
    
    def check_answer(self, answer: str) -> bool:
        normalized = Config.normalize(answer)
        return any(Config.normalize(a) == normalized for a in self.current_answer)
