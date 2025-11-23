"""
لعبة الكلمة واللون - محسنة
Created by: Abeer Aldosari © 2025
"""
from .base_game import BaseGame
import random
import difflib
from config import POINTS_PER_CORRECT, POINTS_PER_WIN

class WordColorGame(BaseGame):
    """لعبة الكلمة واللون - Stroop Effect"""
    
    def __init__(self, line_api):
        super().__init__(line_api, rounds=10)
        
        self.colors = {
            "أحمر": "🔴", "أزرق": "🔵", "أخضر": "🟢", 
            "أصفر": "🟡", "برتقالي": "🟠", "أرجواني": "🟣",
            "بني": "🟤", "أسود": "⚫", "أبيض": "⚪"
        }
        self.color_names = list(self.colors.keys())
    
    def start_game(self):
        self.current_round = 0
        return self.generate_question()

    def generate_question(self):
        word_color = random.choice(self.color_names)
        display_color = random.choice(self.color_names)
        
        # أحيانًا نفس اللون
        if random.random() < 0.3:
            display_color = word_color
        
        self.current_answer = display_color
        color_emoji = self.colors[display_color]
        
        question = f"ما لون الدائرة؟\n\nالكلمة: {word_color}\nالدائرة: {color_emoji}"
        extra_info = "💡 اكتب لون الدائرة وليس الكلمة!"
        
        return self.build_question_flex("كلمة ولون 🎨", question, extra_info)

    def check_answer(self, answer, uid, name):
        normalized = self.normalize_text(answer)
        
        if normalized == 'لمح':
            first_char = self.current_answer[0]
            length = len(self.current_answer)
            hint = f"💡 أول حرف '{first_char}' وعدد الحروف {length}"
            return {'points': 0, 'won': False, 'response': self.build_question_flex("كلمة ولون 🎨", hint, "اكتب لون الدائرة")}
        
        if normalized == 'جاوب':
            self.current_round += 1
            is_final = self.current_round >= self.rounds
            if is_final:
                return {'points': 0, 'won': False, 'response': self.build_result_flex("انتهت اللعبة", f"اللون: {self.current_answer}", 0, True)}
            return {'points': 0, 'won': False, 'response': self.generate_question()}
        
        correct = self.normalize_text(self.current_answer)
        if normalized == correct or difflib.SequenceMatcher(None, normalized, correct).ratio() > 0.75:
            points = POINTS_PER_CORRECT
            self.add_player_score(uid, points)
            self.current_round += 1
            is_final = self.current_round >= self.rounds
            
            if is_final:
                return {'points': points, 'won': True, 'response': self.build_result_flex(name, f"اللون: {self.current_answer}", points, True)}
            return {'points': points, 'won': False, 'response': self.generate_question()}
        
        return None
