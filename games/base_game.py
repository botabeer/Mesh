from abc import ABC, abstractmethod
from linebot.models import TextSendMessage, FlexSendMessage
from ui_components import create_game_card, COLORS
from config import POINTS

class BaseGame(ABC):
    """الكلاس الأساسي لجميع الألعاب"""
    
    def __init__(self, line_bot_api):
        self.line_bot_api = line_bot_api
        self.current_question = None
        self.correct_answer = None
        self.attempts = 0
        self.max_attempts = 3
        
    @abstractmethod
    def generate_question(self):
        """توليد سؤال جديد"""
        pass
    
    @abstractmethod
    def check_answer(self, answer, user_id, display_name):
        """فحص الإجابة"""
        pass
    
    def start_game(self):
        """بدء اللعبة"""
        self.generate_question()
        return FlexSendMessage(
            alt_text=self.get_game_name(),
            contents=create_game_card(
                self.get_game_name(),
                self.current_question,
                self.get_options() if hasattr(self, 'get_options') else None
            )
        )
    
    @abstractmethod
    def get_game_name(self):
        """اسم اللعبة"""
        pass
    
    def calculate_points(self, is_correct, time_taken=None):
        """حساب النقاط"""
        if not is_correct:
            return 0
        
        points = POINTS['correct_answer']
        
        if self.attempts == 1:
            points = POINTS['perfect_answer']
        elif time_taken and time_taken < 5:
            points = POINTS['fast_answer']
        
        return points
