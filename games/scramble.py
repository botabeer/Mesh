import random
from .base_game import BaseGame
from linebot.models import TextSendMessage

class ScrambleGame(BaseGame):
    """لعبة ترتيب الحروف"""
    
    def __init__(self, line_bot_api):
        super().__init__(line_bot_api)
        self.words = [
            'مدرسة', 'جامعة', 'مستشفى', 'مطعم', 'مكتبة',
            'حديقة', 'سوق', 'مطار', 'محطة', 'ملعب'
        ]
    
    def get_game_name(self):
        return "ترتيب الحروف"
    
    def generate_question(self):
        word = random.choice(self.words)
        self.correct_answer = word
        
        scrambled = list(word)
        random.shuffle(scrambled)
        scrambled_word = ''.join(scrambled)
        
        # تأكد من أن الكلمة مبعثرة فعلاً
        while scrambled_word == word:
            random.shuffle(scrambled)
            scrambled_word = ''.join(scrambled)
        
        self.current_question = f"🔤 رتب الحروف لتكوين كلمة صحيحة:\n\n{' - '.join(scrambled)}"
    
    def check_answer(self, answer, user_id, display_name):
        answer = answer.strip()
        
        if answer == self.correct_answer:
            points = self.calculate_points(True)
            return {
                'message': f"🎉 ممتاز {display_name}!\n\nالكلمة الصحيحة: {self.correct_answer}\n+{points} نقطة",
                'response': TextSendMessage(text=f"🎉 ممتاز {display_name}!\n\nالكلمة الصحيحة: {self.correct_answer}\n+{points} نقطة"),
                'points': points,
                'won': True,
                'game_over': True
            }
        
        self.attempts += 1
        if self.attempts >= self.max_attempts:
            return {
                'message': f"❌ انتهت المحاولات\n\nالكلمة الصحيحة: {self.correct_answer}",
                'response': TextSendMessage(text=f"❌ انتهت المحاولات\n\nالكلمة الصحيحة: {self.correct_answer}"),
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
