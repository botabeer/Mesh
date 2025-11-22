"""
لعبة الرياضيات - Enhanced Version
Created by: Abeer Aldosari © 2025
"""
from linebot.models import TextSendMessage
from .base_game import BaseGame
import random


class MathGame(BaseGame):
    """لعبة العمليات الحسابية المحسنة"""
    
    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, questions_count=10)
        self.difficulty = 1
    
    def generate_question(self):
        """توليد سؤال رياضي"""
        max_num = 10 + (self.current_question * 5)
        
        operations = ['+', '-', '*']
        if self.current_question >= 5:
            operations.append('/')
        
        operation = random.choice(operations)
        
        if operation == '/':
            result = random.randint(2, max_num // 2)
            num2 = random.randint(2, 10)
            num1 = result * num2
            answer = result
        elif operation == '*':
            num1 = random.randint(1, min(12, max_num))
            num2 = random.randint(1, min(12, max_num))
            answer = num1 * num2
        elif operation == '-':
            num1 = random.randint(1, max_num)
            num2 = random.randint(1, num1)
            answer = num1 - num2
        else:  # +
            num1 = random.randint(1, max_num)
            num2 = random.randint(1, max_num)
            answer = num1 + num2
        
        return {
            "question": f"{num1} {operation} {num2}",
            "answer": str(answer),
            "num1": num1,
            "num2": num2,
            "operation": operation
        }
    
    def start_game(self):
        """بدء اللعبة"""
        self.current_question = 0
        self.game_active = True
        return self.get_question()
    
    def get_question(self):
        """الحصول على السؤال"""
        q_data = self.generate_question()
        self.current_answer = q_data["answer"]
        
        op_symbols = {'+': '➕', '-': '➖', '*': '✖️', '/': '➗'}
        op_symbol = op_symbols.get(q_data["operation"], q_data["operation"])
        
        message = f"🔢 رياضيات ({self.current_question + 1}/{self.questions_count})\n\n"
        message += f"📝 احسب:\n\n"
        message += f"『 {q_data['num1']} {op_symbol} {q_data['num2']} = ؟ 』\n\n"
        message += "💡 اكتب الناتج فقط"
        
        return TextSendMessage(text=message)
    
    def check_answer(self, user_answer, user_id, display_name):
        """فحص الإجابة"""
        if not self.game_active:
            return None
        
        if user_id in self.answered_users:
            return None
        
        if user_answer == 'جاوب':
            reveal = self.reveal_answer()
            next_q = self.next_question()
            
            if isinstance(next_q, dict) and next_q.get('game_over'):
                return next_q
            
            message = f"{reveal}\n\n"
            if hasattr(next_q, 'text'):
                message += next_q.text
            return {
                'message': message,
                'response': TextSendMessage(text=message),
                'points': 0
            }
        
        try:
            user_num = user_answer.strip().replace(',', '').replace(' ', '')
            
            if user_num == self.current_answer:
                points = self.add_score(user_id, display_name, 10)
                next_q = self.next_question()
                
                if isinstance(next_q, dict) and next_q.get('game_over'):
                    next_q['points'] = points
                    return next_q
                
                message = f"✅ صحيح يا {display_name}!\n+{points} نقطة\n\n"
                if hasattr(next_q, 'text'):
                    message += next_q.text
                
                return {
                    'message': message,
                    'response': TextSendMessage(text=message),
                    'points': points
                }
        except:
            pass
        
        return None
