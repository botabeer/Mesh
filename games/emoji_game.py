from linebot.models import TextSendMessage
from .base_game import BaseGame
import random

class EmojiGame(BaseGame):
    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, questions_count=10)
        
        self.emojis = [
            {"emoji": "🚗", "answer": "سيارة"},
            {"emoji": "✈️", "answer": "طائرة"},
            {"emoji": "🏠", "answer": "بيت"},
            {"emoji": "📱", "answer": "هاتف"},
            {"emoji": "💻", "answer": "حاسوب"},
            {"emoji": "📚", "answer": "كتاب"},
            {"emoji": "⚽", "answer": "كرة"},
            {"emoji": "🍎", "answer": "تفاحة"},
            {"emoji": "🌙", "answer": "قمر"},
            {"emoji": "☀️", "answer": "شمس"},
            {"emoji": "🐱", "answer": "قطة"},
            {"emoji": "🐶", "answer": "كلب"},
            {"emoji": "🦁", "answer": "أسد"},
            {"emoji": "🎂", "answer": "كعكة"},
            {"emoji": "☕", "answer": "قهوة"},
        ]
        random.shuffle(self.emojis)
    
    def start_game(self):
        self.current_question = 0
        self.game_active = True
        return self.get_question()
    
    def get_question(self):
        emoji_data = self.emojis[self.current_question % len(self.emojis)]
        self.current_answer = emoji_data["answer"]
        
        message = f"😀 خمن الإيموجي ({self.current_question + 1}/{self.questions_count})\n\n"
        message += f"『 {emoji_data['emoji']} 』\n\n"
        message += "اكتب اسم الشيء"
        
        return TextSendMessage(text=message)
    
    def check_answer(self, user_answer, user_id, display_name):
        if not self.game_active:
            return None
        
        normalized = self.normalize_text(user_answer)
        correct = self.normalize_text(self.current_answer)
        
        if normalized == correct or normalized in correct:
            points = self.add_score(user_id, display_name, 10)
            next_q = self.next_question()
            
            if isinstance(next_q, dict) and next_q.get('game_over'):
                next_q['points'] = points
                return next_q
            
            message = f"✅ ممتاز يا {display_name}!\n+{points} نقطة\n\n"
            if hasattr(next_q, 'text'):
                message += next_q.text
            
            return {'message': message, 'response': TextSendMessage(text=message), 'points': points}
        
        return None
