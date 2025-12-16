import random
from games.base import BaseGame
from config import Config


class OppositeGame(BaseGame):
    """لعبة ضد - 50 كلمة وعكسها"""
    
    def __init__(self, db, theme: str = "light"):
        super().__init__(db, theme)
        self.game_name = "ضد"
        
        self.opposites = {
            "كبير": ["صغير", "قصير"],
            "طويل": ["قصير"],
            "سريع": ["بطيء"],
            "ساخن": ["بارد", "مثلج"],
            "نظيف": ["وسخ", "قذر"],
            "جديد": ["قديم"],
            "صعب": ["سهل", "بسيط"],
            "قوي": ["ضعيف"],
            "غني": ["فقير"],
            "سعيد": ["حزين"],
            "جميل": ["قبيح"],
            "ثقيل": ["خفيف"],
            "عالي": ["منخفض", "واطي"],
            "واسع": ["ضيق"],
            "قريب": ["بعيد"],
            "مفتوح": ["مغلق"],
            "نهار": ["ليل"],
            "شمس": ["قمر"],
            "شتاء": ["صيف"],
            "شرق": ["غرب"],
            "ابيض": ["اسود"],
            "حلو": ["مر", "حامض"],
            "حار": ["بارد"],
            "صحيح": ["خطا", "خاطي", "غلط"],
            "حي": ["ميت"],
            "نور": ["ظلام", "ظلمه"],
            "فوق": ["تحت"],
            "يمين": ["يسار", "شمال"],
            "امام": ["خلف", "وراء"],
            "داخل": ["خارج"],
            "صباح": ["مساء"],
            "كثير": ["قليل"],
            "اول": ["اخر", "اخير"],
            "سماء": ["ارض"],
            "ذكر": ["انثى"],
            "ليل": ["نهار"],
            "رطب": ["جاف", "ناشف"],
            "ممتلئ": ["فارغ"],
            "رفيع": ["سميك", "عريض"],
            "ناعم": ["خشن"],
            "صلب": ["طري", "لين"],
            "مستقيم": ["معوج", "منحني"],
            "مظلم": ["مضيء", "منير"],
            "هادئ": ["صاخب", "عالي"],
            "نشيط": ["كسول", "خامل"],
            "ذكي": ["غبي", "احمق"],
            "شجاع": ["جبان"],
            "كريم": ["بخيل"],
            "صادق": ["كاذب"],
            "امين": ["خائن"]
        }
        
        self.questions = list(self.opposites.keys())
        random.shuffle(self.questions)

    def get_question(self):
        """اختيار كلمة"""
        word = self.questions[self.current_q % len(self.questions)]
        self.current_answer = self.opposites[word]
        
        hint = "ما عكس الكلمة"
        return self.build_question_flex(word, hint)

    def check_answer(self, answer: str) -> bool:
        """التحقق من الإجابة"""
        normalized = Config.normalize(answer)
        return any(Config.normalize(a) == normalized for a in self.current_answer)
