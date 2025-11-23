"""
لعبة سلسلة الكلمات - محسنة
Created by: Abeer Aldosari © 2025
"""
from .base_game import BaseGame
import random
from config import POINTS_PER_CORRECT, POINTS_PER_WIN

class ChainWordsGame(BaseGame):
    def __init__(self, line_api):
        super().__init__(line_api, rounds=5)
        self.starting_words = [
            "سيارة", "تفاح", "قلم", "نجم", "كتاب", "باب", "رمل", 
            "لعبة", "حديقة", "ورد", "دفتر", "معلم", "منزل", "شمس"
        ]
        self.last_word = None
        self.used_words = set()

    def start_game(self):
        self.current_round = 0
        self.last_word = random.choice(self.starting_words)
        self.used_words.add(self.normalize_text(self.last_word))
        return self.generate_question()

    def generate_question(self):
        required_letter = self.last_word[-1]
        
        question = f"الكلمة السابقة: {self.last_word}\n\n اكتب كلمة تبدأ بحرف: {required_letter}"
        extra_info = "⚠️ لا تكرر الكلمات المستخدمة"
        
        return self.build_question_flex("سلسلة الكلمات 🔗", question, extra_info)

    def check_answer(self, answer, uid, name):
        normalized_answer = self.normalize_text(answer)
        
        if normalized_answer in self.used_words:
            hint = f"❌ الكلمة '{answer}' مستخدمة من قبل!"
            return {'points': 0, 'won': False, 'response': self.build_question_flex("سلسلة الكلمات 🔗", hint, "جرب كلمة أخرى")}
        
        required_letter = self.last_word[-1]
        if normalized_answer and normalized_answer[0] == self.normalize_text(required_letter) and len(normalized_answer) >= 2:
            self.used_words.add(normalized_answer)
            self.last_word = answer.strip()
            points = POINTS_PER_CORRECT
            self.add_player_score(uid, points)
            
            self.current_round += 1
            is_final = self.current_round >= self.rounds
            
            if is_final:
                return {'points': points, 'won': True, 'response': self.build_result_flex(name, f"الكلمة الأخيرة: {self.last_word}", points, True)}
            
            return {'points': points, 'won': False, 'response': self.generate_question()}
        
        return None
