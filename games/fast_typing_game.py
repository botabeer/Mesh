"""
لعبة الكتابة السريعة - محسنة
Created by: Abeer Aldosari © 2025
"""
from .base_game import BaseGame
import random
from datetime import datetime
from config import POINTS_PER_CORRECT, POINTS_PER_WIN

class FastTypingGame(BaseGame):
    def __init__(self, line_api):
        super().__init__(line_api, rounds=5)
        self.sentences = [
            "سبحان الله", "الحمد لله", "الله أكبر", "لا حول ولا قوة",
            "العلم نور", "الصبر مفتاح", "الوقت كالسيف", "التعاون أساس النجاح",
            "المعرفة قوة", "التواضع زينة", "الصدق منجاة", "احترم تُحترم"
        ]
        random.shuffle(self.sentences)
        self.start_time = None
    
    def start_game(self):
        self.current_round = 0
        return self.generate_question()

    def generate_question(self):
        sentence = self.sentences[self.current_round % len(self.sentences)]
        self.current_answer = sentence
        self.start_time = datetime.now()
        
        question = f"اكتب بسرعة:\n\n« {sentence} »"
        extra_info = "⏱️ أسرع إجابة صحيحة تفوز!"
        
        return self.build_question_flex("كتابة سريعة ⚡", question, extra_info)

    def check_answer(self, answer, uid, name):
        if answer.strip() == self.current_answer:
            time_taken = (datetime.now() - self.start_time).total_seconds()
            points = POINTS_PER_CORRECT
            self.add_player_score(uid, points)
            
            self.current_round += 1
            is_final = self.current_round >= self.rounds
            
            if is_final:
                return {'points': points, 'won': True, 'response': self.build_result_flex(name, f"الوقت: {time_taken:.1f}ث", points, True)}
            return {'points': points, 'won': False, 'response': self.generate_question()}
        
        return None
