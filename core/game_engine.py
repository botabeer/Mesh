"""
Bot Mesh v7.0 - Unified Game Engine
محرك ألعاب موحد واحترافي
Created by: Enhanced System © 2025
"""

import random
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Callable
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)


class GameMode(Enum):
    """أنواع أوضاع اللعب"""
    SINGLE = "فردي"
    GROUP = "مجموعة"


class GameStatus(Enum):
    """حالات اللعبة"""
    WAITING = "waiting"
    ACTIVE = "active"
    PAUSED = "paused"
    FINISHED = "finished"
    EXPIRED = "expired"


@dataclass
class PlayerScore:
    """بيانات نقاط اللاعب"""
    user_id: str
    username: str
    points: int = 0
    correct_answers: int = 0
    wrong_answers: int = 0
    hints_used: int = 0
    time_taken: float = 0.0
    last_answer_time: Optional[datetime] = None

    def add_points(self, points: int):
        self.points += points
        self.correct_answers += 1
        self.last_answer_time = datetime.now()

    def record_wrong(self):
        self.wrong_answers += 1
        self.last_answer_time = datetime.now()

    def use_hint(self):
        self.hints_used += 1


@dataclass
class Question:
    """بنية السؤال الموحدة"""
    question: str
    answer: Any  # يمكن أن يكون str أو List[str] أو int
    hint: Optional[str] = None
    category: Optional[str] = None
    difficulty: int = 1
    metadata: Dict[str, Any] = field(default_factory=dict)

    def check_answer(self, user_answer: str) -> bool:
        """فحص الإجابة مع دعم الإجابات المتعددة"""
        user_answer = self._normalize(user_answer)
        
        if isinstance(self.answer, list):
            return any(user_answer == self._normalize(ans) for ans in self.answer)
        else:
            return user_answer == self._normalize(str(self.answer))

    @staticmethod
    def _normalize(text: str) -> str:
        """تطبيع النص للمقارنة"""
        return text.strip().lower().replace('أ', 'ا').replace('ى', 'ي').replace('ة', 'ه')


class BaseGame(ABC):
    """
    محرك اللعبة الأساسي الموحد
    جميع الألعاب يجب أن ترث من هذا الكلاس
    """

    def __init__(
        self,
        game_id: str,
        game_name: str,
        game_icon: str,
        mode: GameMode = GameMode.SINGLE,
        max_rounds: int = 5,
        time_limit_per_question: int = 120,  # ثانية
        max_players: Optional[int] = None
    ):
        self.game_id = game_id
        self.game_name = game_name
        self.game_icon = game_icon
        self.mode = mode
        self.max_rounds = max_rounds
        self.time_limit_per_question = time_limit_per_question
        self.max_players = max_players

        # حالة اللعبة
        self.status = GameStatus.WAITING
        self.current_round = 0
        self.current_question: Optional[Question] = None
        
        # إدارة اللاعبين
        self.players: Dict[str, PlayerScore] = {}
        self.answered_this_round: set = set()
        
        # التوقيت
        self.created_at = datetime.now()
        self.started_at: Optional[datetime] = None
        self.question_start_time: Optional[datetime] = None
        self.last_activity = datetime.now()

        # إحصائيات
        self.total_questions_asked = 0
        self.total_correct_answers = 0
        self.total_hints_given = 0

    # ============================================================================
    # Abstract Methods - يجب تنفيذها في كل لعبة
    # ============================================================================

    @abstractmethod
    def generate_question(self) -> Question:
        """توليد سؤال جديد - يجب تنفيذها في كل لعبة"""
        pass

    # ============================================================================
    # Core Game Methods
    # ============================================================================

    def start(self) -> Dict[str, Any]:
        """بدء اللعبة"""
        if self.status != GameStatus.WAITING:
            raise ValueError("اللعبة قد بدأت بالفعل")

        self.status = GameStatus.ACTIVE
        self.started_at = datetime.now()
        self.current_round = 1
        
        return self._next_question()

    def add_player(self, user_id: str, username: str) -> bool:
        """إضافة لاعب جديد"""
        # في الوضع الفردي: لاعب واحد فقط
        if self.mode == GameMode.SINGLE and len(self.players) > 0:
            if user_id not in self.players:
                return False

        # في وضع المجموعة: التحقق من الحد الأقصى
        if self.max_players and len(self.players) >= self.max_players:
            if user_id not in self.players:
                return False

        if user_id not in self.players:
            self.players[user_id] = PlayerScore(user_id, username)
            logger.info(f"✅ انضم {username} إلى لعبة {self.game_name}")

        return True

    def submit_answer(self, user_id: str, username: str, answer: str) -> Dict[str, Any]:
        """إرسال إجابة"""
        self.last_activity = datetime.now()

        # التحقق من حالة اللعبة
        if self.status != GameStatus.ACTIVE:
            return self._error_response("اللعبة غير نشطة")

        # التحقق من السؤال الحالي
        if not self.current_question:
            return self._error_response("لا يوجد سؤال حالي")

        # إضافة اللاعب إذا لم يكن موجوداً
        if not self.add_player(user_id, username):
            return self._error_response("لا يمكنك الانضمام لهذه اللعبة")

        player = self.players[user_id]

        # التحقق من الإجابة المسبقة في هذه الجولة
        if self.mode == GameMode.GROUP and user_id in self.answered_this_round:
            return self._error_response("لقد أجبت في هذه الجولة")

        # حساب الوقت المستغرق
        time_taken = 0.0
        if self.question_start_time:
            time_taken = (datetime.now() - self.question_start_time).total_seconds()

        # فحص الإجابة
        is_correct = self.current_question.check_answer(answer)

        if is_correct:
            # حساب النقاط (مع مكافأة السرعة)
            points = self._calculate_points(time_taken)
            player.add_points(points)
            player.time_taken += time_taken
            self.answered_this_round.add(user_id)
            self.total_correct_answers += 1

            # الانتقال للسؤال التالي
            return self._handle_correct_answer(player, points)
        else:
            player.record_wrong()
            return self._error_response("❌ إجابة خاطئة، حاول مرة أخرى")

    def get_hint(self, user_id: str) -> Dict[str, Any]:
        """الحصول على تلميح"""
        if not self.current_question:
            return self._error_response("لا يوجد سؤال حالي")

        if user_id in self.players:
            self.players[user_id].use_hint()
            self.total_hints_given += 1

        hint_text = self.current_question.hint or self._generate_default_hint()
        
        return {
            "valid": True,
            "hint": hint_text,
            "message": hint_text
        }

    def reveal_answer(self) -> Dict[str, Any]:
        """كشف الإجابة والانتقال للسؤال التالي"""
        if not self.current_question:
            return self._error_response("لا يوجد سؤال حالي")

        answer_text = self._format_answer(self.current_question.answer)
        
        self.current_round += 1
        self.answered_this_round.clear()

        if self.current_round > self.max_rounds:
            return self._finish_game(f"الإجابة: {answer_text}")
        else:
            next_q = self._next_question()
            next_q["message"] = f"الإجابة: {answer_text}"
            return next_q

    def stop(self) -> Dict[str, Any]:
        """إيقاف اللعبة"""
        return self._finish_game("تم إيقاف اللعبة")

    # ============================================================================
    # Helper Methods
    # ============================================================================

    def _next_question(self) -> Dict[str, Any]:
        """الانتقال للسؤال التالي"""
        try:
            self.current_question = self.generate_question()
            self.question_start_time = datetime.now()
            self.answered_this_round.clear()
            self.total_questions_asked += 1

            return {
                "valid": True,
                "game_over": False,
                "question": {
                    "game": self.game_name,
                    "icon": self.game_icon,
                    "question": self.current_question.question,
                    "round": self.current_round,
                    "total_rounds": self.max_rounds,
                    "mode": self.mode.value,
                    "category": self.current_question.category,
                    "difficulty": self.current_question.difficulty
                }
            }
        except Exception as e:
            logger.error(f"❌ خطأ في توليد السؤال: {e}", exc_info=True)
            return self._error_response("حدث خطأ في توليد السؤال")

    def _handle_correct_answer(self, player: PlayerScore, points: int) -> Dict[str, Any]:
        """معالجة الإجابة الصحيحة"""
        self.current_round += 1

        if self.current_round > self.max_rounds:
            result = self._finish_game()
            result["points"] = points
            result["message"] = f"✅ إجابة صحيحة! +{points} نقطة\n\n" + result.get("message", "")
            return result
        else:
            next_q = self._next_question()
            next_q["points"] = points
            next_q["correct"] = True
            next_q["message"] = f"✅ إجابة صحيحة! +{points} نقطة"
            return next_q

    def _finish_game(self, prefix_message: str = "") -> Dict[str, Any]:
        """إنهاء اللعبة وحساب النتائج"""
        self.status = GameStatus.FINISHED
        results = self.get_results()

        message = prefix_message
        if message:
            message += "\n\n"
        
        message += f"🎮 انتهت اللعبة!\n\n"
        
        if results["winner"]:
            message += f"🏆 الفائز: {results['winner']['name']}\n"
            message += f"⭐ النقاط: {results['winner']['points']}\n"
            message += f"✅ إجابات صحيحة: {results['winner']['correct']}\n"

        return {
            "valid": True,
            "game_over": True,
            "results": results,
            "message": message
        }

    def _calculate_points(self, time_taken: float) -> int:
        """حساب النقاط مع مكافأة السرعة"""
        base_points = 10

        # مكافأة السرعة (أقل من 5 ثوانٍ)
        if time_taken < 5:
            return base_points + 5
        elif time_taken < 10:
            return base_points + 3
        elif time_taken < 15:
            return base_points + 1
        else:
            return base_points

    def _generate_default_hint(self) -> str:
        """توليد تلميح افتراضي"""
        if not self.current_question:
            return "💡 فكر جيداً"

        answer = self.current_question.answer
        if isinstance(answer, list):
            answer = answer[0]
        
        answer_str = str(answer)
        
        if len(answer_str) > 2:
            return f"💡 يبدأ بـ: {answer_str[0]}\n📏 الطول: {len(answer_str)} حرف"
        else:
            return f"💡 يبدأ بـ: {answer_str[0]}"

    def _format_answer(self, answer: Any) -> str:
        """تنسيق الإجابة للعرض"""
        if isinstance(answer, list):
            return " أو ".join(str(a) for a in answer)
        return str(answer)

    def _error_response(self, message: str) -> Dict[str, Any]:
        """رد خطأ موحد"""
        return {
            "valid": False,
            "message": message
        }

    def get_results(self) -> Dict[str, Any]:
        """الحصول على النتائج النهائية"""
        sorted_players = sorted(
            self.players.values(),
            key=lambda p: (p.points, p.correct_answers, -p.time_taken),
            reverse=True
        )

        results = {
            "winner": None,
            "players": [],
            "stats": {
                "total_questions": self.total_questions_asked,
                "total_correct": self.total_correct_answers,
                "total_hints": self.total_hints_given,
                "duration": (datetime.now() - self.started_at).total_seconds() if self.started_at else 0
            }
        }

        for player in sorted_players:
            player_data = {
                "name": player.username,
                "points": player.points,
                "correct": player.correct_answers,
                "wrong": player.wrong_answers,
                "hints": player.hints_used,
                "time": round(player.time_taken, 2)
            }
            results["players"].append(player_data)

        if results["players"]:
            results["winner"] = results["players"][0]

        return results

    def is_expired(self, max_minutes: int = 30) -> bool:
        """التحقق من انتهاء صلاحية اللعبة"""
        elapsed = (datetime.now() - self.last_activity).total_seconds() / 60
        return elapsed > max_minutes

    def get_status(self) -> Dict[str, Any]:
        """الحصول على حالة اللعبة"""
        return {
            "game_id": self.game_id,
            "game_name": self.game_name,
            "status": self.status.value,
            "mode": self.mode.value,
            "current_round": self.current_round,
            "max_rounds": self.max_rounds,
            "players_count": len(self.players),
            "created_at": self.created_at.isoformat(),
            "active_time": (datetime.now() - self.created_at).total_seconds()
        }
