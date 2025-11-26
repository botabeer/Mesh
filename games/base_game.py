# games/base_game.py
# تم إنشاء هذا البوت بواسطة عبير الدوسري © 2025

import time
from abc import ABC, abstractmethod


class BaseGame(ABC):
    """
    الكلاس الأساسي لجميع الألعاب
    يجب أن ترث منه كل لعبة داخل مجلد games
    """

    def __init__(self, name: str, total_rounds: int = 5, timeout_minutes: int = 10):
        self.name = name
        self.total_rounds = total_rounds
        self.timeout_minutes = timeout_minutes

        self.current_round = 0
        self.points = 0
        self.start_time = None
        self.finished = False

    # بدء اللعبة
    def start(self):
        self.start_time = time.time()
        self.current_round = 1
        self.finished = False
        self.points = 0

    # التحقق من انتهاء الوقت
    def is_expired(self, minutes: int = None):
        if not self.start_time:
            return False

        limit = minutes if minutes else self.timeout_minutes
        return (time.time() - self.start_time) > (limit * 60)

    # جلب السؤال الحالي
    def get_question(self):
        if self.finished:
            return None

        question_data = self.generate_question()

        return {
            "text": question_data["question"],
            "round": self.current_round,
            "total_rounds": self.total_rounds,
            "answer": question_data.get("answer")
        }

    # فحص الإجابة
    def check_answer(self, user_answer: str, user_id: str, username: str):
        if self.finished:
            return {"game_over": True, "points": self.points}

        result = self.evaluate_answer(user_answer)

        if result.get("correct"):
            self.points += result.get("points", 1)

        if self.current_round >= self.total_rounds:
            self.finished = True
            return {
                "game_over": True,
                "points": self.points
            }

        self.current_round += 1
        next_question = self.get_question()

        return {
            "game_over": False,
            "next_question": next_question
        }

    # ===============================
    # الدوال التي يجب تنفيذها في كل لعبة
    # ===============================

    @abstractmethod
    def generate_question(self) -> dict:
        """
        يجب أن ترجع:
        {
            "question": "نص السؤال",
            "answer": "الإجابة الصحيحة"
        }
        """
        pass

    @abstractmethod
    def evaluate_answer(self, user_answer: str) -> dict:
        """
        يجب أن ترجع:
        {
            "correct": True أو False,
            "points": عدد النقاط (اختياري)
        }
        """
        pass
