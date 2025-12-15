import random
from games.base import BaseGame
from config import Config

class GuessGame(BaseGame):
    def __init__(self, db, theme: str = "light"):
        super().__init__(db, theme)
        
        self.items = {
            "المطبخ": {"ق": ["قدر", "قلايه", "قارورة"], "م": ["ملعقه", "مغرفه", "مقلاه"]},
            "غرفة النوم": {"س": ["سرير", "ستاره"], "م": ["مراه", "مخده", "مصباح"]},
            "المدرسه": {"ق": ["قلم", "قرطاسيه"], "ك": ["كتاب", "كراسه"]},
            "الفواكه": {"ت": ["تفاح", "تمر", "توت"], "م": ["موز", "مشمش"]},
            "الحيوانات": {"ق": ["قطه", "قرد"], "ف": ["فيل", "فهد"]}
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
        
        text = f"الفئة {q_data['category']}\n\nيبدا بحرف {q_data['letter']}"
        hint = f"السؤال {self.current_q + 1}/{self.total_q}"
        return self.build_question_flex(text, hint)
    
    def check_answer(self, answer: str) -> bool:
        normalized = Config.normalize(answer)
        return any(Config.normalize(a) == normalized for a in self.current_answer)
