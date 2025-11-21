"""
games/base_game.py - القاعدة الأساسية لجميع الألعاب
"""

from abc import ABC, abstractmethod
from config import Config
from flex_messages import FlexDesign

class BaseGame(ABC):
    """القاعدة الأساسية لجميع الألعاب"""
    
    def __init__(self):
        self.name = "لعبة"
        self.description = ""
        self.current_round = 1
        self.max_rounds = Config.DEFAULT_ROUNDS
        self.points_per_answer = Config.POINTS_CORRECT
        self.hint_used = False
        self.current_question = None
        self.current_answer = None
    
    @abstractmethod
    def start(self):
        """بدء اللعبة - يجب تنفيذه في كل لعبة"""
        pass
    
    @abstractmethod
    def check_answer(self, answer: str) -> tuple:
        """التحقق من الإجابة - يرجع (صحيح/خطأ, النقاط)"""
        pass
    
    @abstractmethod
    def get_hint(self) -> str:
        """الحصول على تلميح"""
        pass
    
    @abstractmethod
    def get_solution(self) -> str:
        """الحصول على الحل"""
        pass
    
    def next_round(self):
        """الانتقال للجولة التالية"""
        self.current_round += 1
        self.hint_used = False
    
    def is_finished(self) -> bool:
        """هل انتهت اللعبة؟"""
        return self.current_round >= self.max_rounds
    
    def calculate_points(self, base_points: int = None) -> int:
        """حساب النقاط مع خصم التلميح"""
        points = base_points or self.points_per_answer
        if self.hint_used:
            points -= Config.HINT_PENALTY
        return max(points, 1)
    
    def get_progress(self) -> str:
        """الحصول على التقدم"""
        return f"الجولة {self.current_round} من {self.max_rounds}"
    
    def create_game_screen(self, question: str, letters: list = None) -> dict:
        """إنشاء شاشة اللعبة"""
        return FlexDesign.game_screen(
            self.name, question, letters,
            self.current_round, self.max_rounds
        )
