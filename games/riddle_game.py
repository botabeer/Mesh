from linebot.models import TextSendMessage
from .base_game import BaseGame
import random

class RiddleGame(BaseGame):
    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, questions_count=10)
        
        self.riddles = [
            {"q": "ما هو الشيء الذي يخترق الزجاج ولا يكسره؟", "a": "الضوء"},
            {"q": "له أوراق ولكنه ليس شجرة؟", "a": "الكتاب"},
            {"q": "يسير بلا أقدام ويدخل الأذن؟", "a": "الصوت"},
            {"q": "ما هو الشيء الذي يزداد كلما أخذت منه؟", "a": "الحفرة"},
            {"q": "يمشي بلا أرجل ويبكي بلا أعين؟", "a": "السحاب"},
            {"q": "ما هو الشيء الذي كلما كبر صغر؟", "a": "الشمعة"},
            {"q": "له قلب ولا يخفق؟", "a": "الخس"},
            {"q": "ما هو الشيء الذي تذبحه وتبكي عليه؟", "a": "البصل"},
            {"q": "له عيون ولا يرى؟", "a": "الإبرة"},
            {"q": "له أسنان ولا يعض؟", "a": "المشط"},
        ]
        random.shuffle(self.riddles)
    
    def start_game(self):
        self.current_question = 0
        self.game_active = True
        return self.get_question()
    
    def get_question(self):
        riddle = self.riddles[self.current_question % len(self.riddles)]
        self.current_answer = riddle["a"]
        
        message = f"🎭 لغز ({self.current_question + 1}/{self.questions_count})\n\n"
        message += f"❓ {riddle['q']}\n\n"
        message += "• لمح - تلميح\n• جاوب - الإجابة"
        
        return TextSendMessage(text=message)
    
    def check_answer(self, user_answer, user_id, display_name):
        if not self.game_active:
            return None
        
        if user_answer == 'لمح':
            hint = self.get_hint()
            return {'message': hint, 'response': TextSendMessage(text=hint), 'points': 0}
        
        if user_answer == 'جاوب':
            reveal = self.reveal_answer()
            next_q = self.next_question()
            if isinstance(next_q, dict) and next_q.get('game_over'):
                return next_q
            message = f"{reveal}\n\n" + (next_q.text if hasattr(next_q, 'text') else "")
            return {'message': message, 'response': TextSendMessage(text=message), 'points': 0}
        
        if self.normalize_text(user_answer) in self.normalize_text(self.current_answer):
            points = self.add_score(user_id, display_name, 10)
            next_q = self.next_question()
            
            if isinstance(next_q, dict) and next_q.get('game_over'):
                next_q['points'] = points
                return next_q
            
            message = f"✅ ممتاز!\n+{points} نقطة\n\n"
            if hasattr(next_q, 'text'):
                message += next_q.text
            
            return {'message': message, 'response': TextSendMessage(text=message), 'points': points}
        
        return None
