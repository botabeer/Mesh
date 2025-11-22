"""
Bot Mesh - Base Game Class (Enhanced)
Created by: Abeer Aldosari © 2025
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Set
from linebot.models import TextSendMessage
from dataclasses import dataclass, field
from datetime import datetime
import re


@dataclass
class GameResult:
    """نتيجة اللعبة"""
    message: str
    points: int = 0
    won: bool = False
    game_over: bool = False
    response: Any = None
    
    def __post_init__(self):
        if self.response is None:
            self.response = TextSendMessage(text=self.message)


@dataclass
class PlayerScore:
    """نقاط اللاعب"""
    user_id: str
    display_name: str
    points: int = 0
    correct_answers: int = 0
    wrong_answers: int = 0


class BaseGame(ABC):
    """الفئة الأساسية لجميع الألعاب"""
    
    def __init__(self, line_bot_api, questions_count: int = 10):
        self.line_bot_api = line_bot_api
        self.questions_count = questions_count
        self.current_question = 0
        self.current_answer: Optional[str] = None
        self.game_active = True
        self.scores: Dict[str, PlayerScore] = {}
        self.answered_users: Set[str] = set()
        self.created_at = datetime.now()
        self.last_activity = datetime.now()
    
    @abstractmethod
    def start_game(self) -> TextSendMessage:
        """بدء اللعبة - يجب تنفيذها في كل لعبة"""
        pass
    
    @abstractmethod
    def get_question(self) -> TextSendMessage:
        """الحصول على السؤال الحالي"""
        pass
    
    @abstractmethod
    def check_answer(self, user_answer: str, user_id: str, display_name: str) -> Optional[Dict[str, Any]]:
        """فحص إجابة المستخدم"""
        pass
    
    def normalize_text(self, text: str) -> str:
        """تطبيع النص العربي"""
        if not text:
            return ""
        
        # إزالة التشكيل
        arabic_diacritics = re.compile(r'[\u0617-\u061A\u064B-\u0652]')
        text = arabic_diacritics.sub('', text)
        
        # توحيد الألف
        text = re.sub(r'[إأآا]', 'ا', text)
        
        # توحيد الهاء والتاء المربوطة
        text = re.sub(r'[ة]', 'ه', text)
        
        # توحيد الياء
        text = re.sub(r'[ىئ]', 'ي', text)
        
        # إزالة المسافات الزائدة
        text = ' '.join(text.split())
        
        return text.strip()
    
    def add_score(self, user_id: str, display_name: str, points: int) -> int:
        """إضافة نقاط للاعب"""
        if user_id not in self.scores:
            self.scores[user_id] = PlayerScore(
                user_id=user_id,
                display_name=display_name
            )
        
        self.scores[user_id].points += points
        self.scores[user_id].correct_answers += 1
        self.answered_users.add(user_id)
        self.last_activity = datetime.now()
        
        return points
    
    def get_hint(self) -> str:
        """الحصول على تلميح"""
        if not self.current_answer:
            return "💡 لا يوجد تلميح متاح"
        
        answer = self.current_answer
        hint_chars = max(1, len(answer) // 3)
        
        return f"💡 تلميح: {answer[:hint_chars]}{'_' * (len(answer) - hint_chars)}"
    
    def reveal_answer(self) -> str:
        """كشف الإجابة"""
        return f"📝 الإجابة الصحيحة: {self.current_answer}"
    
    def next_question(self) -> Any:
        """الانتقال للسؤال التالي"""
        self.current_question += 1
        self.answered_users.clear()
        self.last_activity = datetime.now()
        
        if self.current_question >= self.questions_count:
            return self.end_game()
        
        return self.get_question()
    
    def end_game(self) -> Dict[str, Any]:
        """إنهاء اللعبة"""
        self.game_active = False
        
        # ترتيب اللاعبين حسب النقاط
        sorted_players = sorted(
            self.scores.values(),
            key=lambda x: x.points,
            reverse=True
        )
        
        # بناء رسالة النتائج
        message = "🏁 انتهت اللعبة!\n"
        message += "═" * 25 + "\n\n"
        
        if sorted_players:
            message += "🏆 النتائج النهائية:\n\n"
            
            medals = ["🥇", "🥈", "🥉"]
            for i, player in enumerate(sorted_players[:10]):
                medal = medals[i] if i < 3 else f"{i+1}."
                message += f"{medal} {player.display_name}: {player.points} نقطة\n"
            
            winner = sorted_players[0]
            message += f"\n🎉 مبروك {winner.display_name}!"
        else:
            message += "لم يشارك أحد في هذه اللعبة"
        
        return {
            'game_over': True,
            'message': message,
            'response': TextSendMessage(text=message),
            'points': 0,
            'won': True if sorted_players else False
        }
    
    def get_game_status(self) -> Dict[str, Any]:
        """حالة اللعبة"""
        return {
            'active': self.game_active,
            'question': f"{self.current_question + 1}/{self.questions_count}",
            'players': len(self.scores),
            'total_points': sum(p.points for p in self.scores.values()),
            'created_at': self.created_at.isoformat(),
            'last_activity': self.last_activity.isoformat()
        }
    
    def is_expired(self, timeout_minutes: int = 30) -> bool:
        """التحقق من انتهاء صلاحية اللعبة"""
        elapsed = (datetime.now() - self.last_activity).total_seconds() / 60
        return elapsed > timeout_minutes
