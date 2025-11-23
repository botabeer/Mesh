"""
لعبة التخمين - محسنة
Created by: Abeer Aldosari © 2025
"""
from .base_game import BaseGame
import random
from config import POINTS_PER_CORRECT, POINTS_PER_WIN

class GuessGame(BaseGame):
    def __init__(self, line_api):
        super().__init__(line_api, rounds=5)
        self.items = {
            "المطبخ": {"ق": ["قدر", "قلاية"], "م": ["ملعقة", "مغرفة"], "س": ["سكين", "صحن"]},
            "غرفة النوم": {"س": ["سرير"], "و": ["وسادة"], "م": ["مرآة", "مخدة"]},
            "المدرسة": {"ق": ["قلم"], "د": ["دفتر"], "ك": ["كتاب"], "م": ["مسطرة"]},
            "الفواكه": {"ت": ["تفاح", "تمر"], "م": ["موز"], "ع": ["عنب"]},
            "الحيوانات": {"ق": ["قطة"], "س": ["سنجاب"], "ف": ["فيل"]}
        }
        self.questions_list = []
        for cat, letters in self.items.items():
            for letter, words in letters.items():
                if words:
                    self.questions_list.append({"category": cat, "letter": letter, "answers": words})
        random.shuffle(self.questions_list)
    
    def start_game(self):
        self.current_round = 0
        return self.generate_question()

    def generate_question(self):
        q_data = self.questions_list[self.current_round % len(self.questions_list)]
        self.current_answer = q_data["answers"]
        
        question = f"الفئة: {q_data['category']}\nيبدأ بحرف: {q_data['letter']}"
        extra_info = "💡 خمن الكلمة\n• جاوب: لمعرفة الإجابة"
        
        return self.build_question_flex("تخمين الكلمة 🔮", question, extra_info)

    def check_answer(self, answer, uid, name):
        normalized = self.normalize_text(answer)
        
        if normalized == "جاوب":
            answers_text = " أو ".join(self.current_answer)
            self.current_round += 1
            is_final = self.current_round >= self.rounds
            if is_final:
                return {'points': 0, 'won': False, 'response': self.build_result_flex("انتهت اللعبة", f"الإجابة: {answers_text}", 0, True)}
            return {'points': 0, 'won': False, 'response': self.generate_question()}
        
        for correct_answer in self.current_answer:
            if self.normalize_text(correct_answer) == normalized:
                points = POINTS_PER_CORRECT
                self.add_player_score(uid, points)
                self.current_round += 1
                is_final = self.current_round >= self.rounds
                
                if is_final:
                    return {'points': points, 'won': True, 'response': self.build_result_flex(name, correct_answer, points, True)}
                return {'points': points, 'won': False, 'response': self.generate_question()}
        
        return None
