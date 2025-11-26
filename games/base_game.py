"""
Bot Mesh v7.0 - Base Game Engine
تم إنشاء هذا النظام بواسطة عبير الدوسري © 2025

هذا الملف هو الأساس الذي ترث منه جميع الألعاب
"""

from datetime import datetime


class BaseGame:
    """
    الفئة الأساسية لجميع الألعاب
    """

    name = "لعبة"
    total_rounds = 5
    points_per_correct = 10
    timeout_minutes = 10

    def __init__(self):
        self.started_at = None
        self.current_round = 0
        self.score = 0
        self.questions = []
        self.finished = False

    # ---------------------------------------------------------
    # دورة حياة اللعبة
    # ---------------------------------------------------------

    def start(self):
        """
        بدء اللعبة
        """
        self.started_at = datetime.now()
        self.current_round = 1
        self.score = 0
        self.finished = False
        self.prepare_questions()

    def prepare_questions(self):
        """
        يجب إعادة تعريفها في كل لعبة
        تقوم بتحميل الأسئلة في self.questions
        """
        raise NotImplementedError("يجب تعريف prepare_questions داخل اللعبة")

    def get_question(self):
        """
        جلب السؤال الحالي
        """
        if self.current_round > self.total_rounds:
            self.finished = True
            return None

        index = self.current_round - 1
        if index < len(self.questions):
            return {
                "text": self.questions[index],
                "round": self.current_round,
                "total_rounds": self.total_rounds
            }

        self.finished = True
        return None

    # ---------------------------------------------------------
    # التحقق من الإجابة
    # ---------------------------------------------------------

    def check_answer(self, user_text, user_id=None, username=None):
        """
        التحقق من إجابة اللاعب
        يجب إعادة تعريفها في كل لعبة
        """
        raise NotImplementedError("يجب تعريف check_answer داخل اللعبة")

    def correct(self):
        """
        عند الإجابة الصحيحة
        """
        self.score += self.points_per_correct
        self.current_round += 1

        if self.current_round > self.total_rounds:
            self.finished = True
            return {
                "correct": True,
                "game_over": True,
                "points": self.score
            }

        return {
            "correct": True,
            "next_question": self.get_question(),
            "points": self.points_per_correct
        }

    def wrong(self, message="إجابة غير صحيحة"):
        """
        عند الخطأ
        """
        return {
            "correct": False,
            "message": message
        }

    # ---------------------------------------------------------
    # انتهاء اللعبة
    # ---------------------------------------------------------

    def is_expired(self, timeout_minutes=None):
        """
        التحقق من انتهاء المهلة
        """
        if not self.started_at:
            return False

        if timeout_minutes is None:
            timeout_minutes = self.timeout_minutes

        diff = datetime.now() - self.started_at
        return diff.total_seconds() > timeout_minutes * 60

    def end(self):
        """
        إنهاء اللعبة يدويًا
        """
        self.finished = True
        return {
            "game_over": True,
            "points": self.score
        }
