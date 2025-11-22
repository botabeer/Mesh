from linebot.models import TextSendMessage
from .base_game import BaseGame
import random

class MemoryGame(BaseGame):
    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, questions_count=10)
        self.sequence_type = "numbers"
    
    def generate_sequence(self, length):
        if self.sequence_type == "numbers":
            return [str(random.randint(0, 9)) for _ in range(length)]
        words = ["قلم", "كتاب", "شجرة", "بيت", "سيارة", "قطة", "كلب", "زهرة", "نجم", "قمر"]
        return random.sample(words, min(length, len(words)))
    
    def start_game(self):
        self.current_question = 0
        self.game_active = True
        return self.get_question()
    
    def get_question(self):
        length = 3 + (self.current_question // 2)
        self.sequence_type = "numbers" if self.current_question % 2 == 0 else "words"
        
        sequence = self.generate_sequence(length)
        self.current_answer = " ".join(sequence)
        
        message = f"🧠 اختبار الذاكرة ({self.current_question + 1}/{self.questions_count})\n\n"
        message += f"👀 احفظ هذه السلسلة:\n\n"
        message += f"『 {' - '.join(sequence)} 』\n\n"
        message += "📝 اكتب السلسلة بنفس الترتيب"
        
        return TextSendMessage(text=message)
    
    def check_answer(self, user_answer, user_id, display_name):
        if not self.game_active:
            return None
        
        user_cleaned = user_answer.replace('-', ' ').strip()
        user_cleaned = ' '.join(user_cleaned.split())
        
        if user_cleaned.lower() == self.current_answer.lower():
            points = self.add_score(user_id, display_name, 10)
            next_q = self.next_question()
            
            if isinstance(next_q, dict) and next_q.get('game_over'):
                next_q['points'] = points
                return next_q
            
            message = f"✅ ذاكرة قوية يا {display_name}!\n+{points} نقطة\n\n"
            if hasattr(next_q, 'text'):
                message += next_q.text
            
            return {'message': message, 'response': TextSendMessage(text=message), 'points': points}
        
        return None
