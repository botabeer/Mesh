"""
لعبة التوافق - محسنة
Created by: Abeer Aldosari © 2025
"""
from .base_game import BaseGame
from config import POINTS_PER_CORRECT, POINTS_PER_WIN

class CompatibilityGame(BaseGame):
    def __init__(self, line_api):
        super().__init__(line_api, rounds=1)
    
    def calculate_compatibility(self, name1, name2):
        name1_clean = self.normalize_text(name1)
        name2_clean = self.normalize_text(name2)
        combined = ''.join(sorted(name1_clean + name2_clean))
        seed = sum(ord(c) * (i+1) for i, c in enumerate(combined))
        return (seed % 81) + 20
    
    def get_message(self, percentage):
        if percentage >= 90: return "توافق رائع جداً! علاقة مثالية ✨"
        elif percentage >= 75: return "توافق ممتاز! علاقة قوية 💪"
        elif percentage >= 60: return "توافق جيد! علاقة واعدة 🌟"
        elif percentage >= 45: return "توافق متوسط! يحتاج عمل 🔧"
        else: return "توافق ضعيف! قد تكون هناك تحديات ⚠️"
    
    def start_game(self):
        question = "اكتب اسمين مفصولين بمسافة\n\nمثال: أحمد سارة"
        return self.build_question_flex("لعبة التوافق 💕", question, "")
    
    def generate_question(self):
        return self.start_game()

    def check_answer(self, answer, uid, name):
        names = answer.strip().split()
        if len(names) < 2:
            hint = "يرجى كتابة اسمين مفصولين بمسافة"
            return {'points': 0, 'won': False, 'response': self.build_question_flex("لعبة التوافق 💕", hint, "")}
        
        name1, name2 = names[0], names[1]
        percentage = self.calculate_compatibility(name1, name2)
        message_text = self.get_message(percentage)
        
        result = f"{name1} 💕 {name2}\n\n نسبة التوافق: {percentage}%\n\n{message_text}"
        points = 5
        self.add_player_score(uid, points)
        
        return {'points': points, 'won': True, 'response': self.build_result_flex(name, result, points, True)}
