import random
import time
from .base_game import BaseGame
from linebot.models import TextSendMessage

class FastTypingGame(BaseGame):
    """لعبة الكتابة السريعة"""
    
    def __init__(self, line_bot_api):
        super().__init__(line_bot_api)
        self.start_time = None
        self.sentences = [
            "السرعة في الكتابة مهارة مفيدة",
            "البرمجة فن وعلم في آن واحد",
            "التعلم المستمر طريق النجاح",
            "الإبداع لا حدود له",
            "المثابرة مفتاح التميز"
        ]
    
    def get_game_name(self):
        return "الكتابة السريعة"
    
    def generate_question(self):
        sentence = random.choice(self.sentences)
        self.correct_answer = sentence
        self.start_time = time.time()
        self.current_question = f"⚡ اكتب هذه الجملة بأسرع وقت:\n\n{sentence}"
    
    def check_answer(self, answer, user_id, display_name):
        answer = answer.strip()
        time_taken = time.time() - self.start_time
        
        if answer == self.correct_answer:
            points = self.calculate_points(True, time_taken)
            return {
                'message': f"🎉 ممتاز {display_name}!\n\n⏱️ الوقت: {time_taken:.1f} ثانية\n+{points} نقطة",
                'response': TextSendMessage(text=f"🎉 ممتاز {display_name}!\n\n⏱️ الوقت: {time_taken:.1f} ثانية\n+{points} نقطة"),
                'points': points,
                'won': True,
                'game_over': True
            }
        
        self.attempts += 1
        if self.attempts >= self.max_attempts:
            return {
                'message': f"❌ انتهت المحاولات\n\nالإجابة الصحيحة:\n{self.correct_answer}",
                'response': TextSendMessage(text=f"❌ انتهت المحاولات\n\nالإجابة الصحيحة:\n{self.correct_answer}"),
                'points': 0,
                'won': False,
                'game_over': True
            }
        
        return {
            'message': f"❌ خطأ! تحقق من الكتابة\nالمحاولات المتبقية: {self.max_attempts - self.attempts}",
            'response': TextSendMessage(text=f"❌ خطأ! تحقق من الكتابة\nالمحاولات المتبقية: {self.max_attempts - self.attempts}"),
            'points': 0,
            'won': False,
            'game_over': False
        }
