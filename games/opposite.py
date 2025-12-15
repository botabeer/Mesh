import random
from games.base import BaseGame
from config import Config


class OppositeGame(BaseGame):
    def __init__(self, db, theme: str = "light"):
        super().__init__(db, theme)
        
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
            "عالي": ["منخفض"],
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
            "صحيح": ["خطا", "خاطي"],
            "حي": ["ميت"],
            "نور": ["ظلام"],
            "فوق": ["تحت"],
            "يمين": ["يسار"],
            "امام": ["خلف"],
            "داخل": ["خارج"],
            "صباح": ["مساء"],
            "كثير": ["قليل"]
        }
        
        self.questions = list(self.opposites.keys())
        random.shuffle(self.questions)

    def get_question(self):
        word = self.questions[self.current_q % len(self.questions)]
        self.current_answer = self.opposites[word]
        
        hint = f"السؤال {self.current_q + 1}/{self.total_q}"
        return self.build_question_flex(f"ما عكس\n\n{word}", hint)

    def check_answer(self, answer: str) -> bool:
        normalized = Config.normalize(answer)
        return any(Config.normalize(a) == normalized for a in self.current_answer)
