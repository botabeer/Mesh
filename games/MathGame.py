import random
from .base_game import BaseGame
from linebot.models import TextSendMessage

class MathGame(BaseGame):
    """لعبة الرياضيات"""
    
    def __init__(self, line_bot_api):
        super().__init__(line_bot_api)
    
    def get_game_name(self):
        return "الرياضيات السريعة"
    
    def generate_question(self):
        operations = ['+', '-', '*']
        op = random.choice(operations)
        
        if op == '*':
            num1 = random.randint(2, 12)
            num2 = random.randint(2, 12)
        else:
            num1 = random.randint(10, 99)
            num2 = random.randint(10, 99)
        
        if op == '+':
            self.correct_answer = str(num1 + num2)
        elif op == '-':
            self.correct_answer = str(num1 - num2)
        else:
            self.correct_answer = str(num1 * num2)
        
        self.current_question = f"🧮 احسب الناتج:\n\n{num1} {op} {num2} = ?"
    
    def check_answer(self, answer, user_id, display_name):
        answer = answer.strip()
        
        if answer == self.correct_answer:
            points = self.calculate_points(True)
            return {
                'message': f"🎉 إجابة صحيحة {display_name}!\n+{points} نقطة",
                'response': TextSendMessage(text=f"🎉 إجابة صحيحة {display_name}!\n+{points} نقطة"),
                'points': points,
                'won': True,
                'game_over': True
            }
        
        self.attempts += 1
        if self.attempts >= self.max_attempts:
            return {
                'message': f"❌ انتهت المحاولات\n\nالإجابة الصحيحة: {self.correct_answer}",
                'response': TextSendMessage(text=f"❌ انتهت المحاولات\n\nالإجابة الصحيحة: {self.correct_answer}"),
                'points': 0,
                'won': False,
                'game_over': True
            }
        
        return {
            'message': f"❌ خطأ! المحاولات المتبقية: {self.max_attempts - self.attempts}",
            'response': TextSendMessage(text=f"❌ خطأ! المحاولات المتبقية: {self.max_attempts - self.attempts}"),
            'points': 0,
            'won': False,
            'game_over': False
        }
