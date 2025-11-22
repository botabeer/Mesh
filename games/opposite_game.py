from linebot.models import TextSendMessage
from .base_game import BaseGame
import random

class OppositeGame(BaseGame):
    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, questions_count=10)
        
        self.opposites = [
            {"word": "كبير", "opposite": "صغير"},
            {"word": "طويل", "opposite": "قصير"},
            {"word": "سريع", "opposite": "بطيء"},
            {"word": "ساخن", "opposite": "بارد"},
            {"word": "جديد", "opposite": "قديم"},
            {"word": "سهل", "opposite": "صعب"},
            {"word": "قوي", "opposite": "ضعيف"},
            {"word": "ثقيل", "opposite": "خفيف"},
            {"word": "جميل", "opposite": "قبيح"},
            {"word": "سعيد", "opposite": "حزين"},
        ]
        random.shuffle(self.opposites)
    
    def start_game(self):
        self.current_question = 0
        self.game_active = True
        return self.get_question()
    
    def get_question(self):
        pair = self.opposites[self.current_question % len(self.opposites)]
        self.current_answer = pair["opposite"]
        
        message = f"↔️ ضد الكلمة ({self.current_question + 1}/{self.questions_count})\n\n"
        message += f"📝 ما هو ضد:\n\n『 {pair['word']} 』"
        
        return TextSendMessage(text=message)
    
    def check_answer(self, user_answer, user_id, display_name):
        if not self.game_active:
            return None
        
        if self.normalize_text(user_answer) == self.normalize_text(self.current_answer):
            points = self.add_score(user_id, display_name, 10)
            next_q = self.next_question()
            
            if isinstance(next_q, dict) and next_q.get('game_over'):
                next_q['points'] = points
                return next_q
            
            message = f"✅ صحيح!\n+{points} نقطة\n\n"
            if hasattr(next_q, 'text'):
                message += next_q.text
            
            return {'message': message, 'response': TextSendMessage(text=message), 'points': points}
        
        return None
