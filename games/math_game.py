‏import random
‏from linebot.models import TextSendMessage

‏class MathGame:
‏    def __init__(self, line_bot_api):
‏        self.line_bot_api = line_bot_api
‏        self.answer = None
‏        self.question = None
    
‏    def start_game(self):
‏        a = random.randint(1, 20)
‏        b = random.randint(1, 20)
‏        op = random.choice(['+', '-', '*'])
        
‏        if op == '+':
‏            self.answer = a + b
‏        elif op == '-':
‏            self.answer = a - b
‏        else:
‏            self.answer = a * b
        
‏        self.question = f"{a} {op} {b}"
‏        text = f"🔢 حل المسألة\n\n{self.question} = ؟\n\n━━━━━━━━━━━━━━\nما الناتج؟"
‏        return TextSendMessage(text=text)
    
‏    def check_answer(self, answer, user_id, display_name):
‏        if self.answer is None:
‏            return None
        
‏        try:
‏            user_ans = int(answer.strip())
‏        except:
‏            return None
        
‏        if user_ans == self.answer:
‏            new_q = self.start_game()
‏            msg = f"✓ صحيح يا {display_name}!\n\n{self.question} = {self.answer}\n+10 نقطة\n\n{new_q.text}"
‏            return {'points': 10, 'won': True, 'message': msg, 'response': TextSendMessage(text=msg), 'game_over': False}
‏        return None
    
‏    def get_hint(self):
‏        return f"💡 فكر جيداً في العملية"
    
‏    def reveal_answer(self):
‏        ans = self.answer
‏        self.answer = None
‏        return f"الناتج: {ans}"
