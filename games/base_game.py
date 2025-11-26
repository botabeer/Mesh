from datetime import datetime


class BaseGame:
    """
    الكلاس الأساسي لجميع الألعاب
    يجب أن ترث منه كل لعبة
    """

    name = "لعبة"
    total_rounds = 5
    time_limit_seconds = 60

    def __init__(self):
        self.current_round = 0
        self.start_time = None
        self.points = 0
        self.finished = False

    # ============================================================
    # تشغيل اللعبة
    # ============================================================

    def start(self):
        self.start_time = datetime.now()
        self.current_round = 1
        self.points = 0
        self.finished = False

    # ============================================================
    # إرجاع السؤال الحالي
    # ============================================================

    def get_question(self):
        """
        يجب إعادة قاموس بهذا الشكل:
        {
            "text": "نص السؤال",
            "round": رقم الجولة,
            "total_rounds": عدد الجولات
        }
        """
        raise NotImplementedError("يجب تنفيذ دالة get_question في الكلاس الابن")

    # ============================================================
    # فحص الإجابة
    # ============================================================

    def check_answer(self, answer: str, user_id: str, username: str):
        """
        يجب إعادة قاموس بهذا الشكل:

        عند استمرار اللعبة:
        {
            "correct": True أو False,
            "next_question": {...},
            "points": عدد النقاط
        }

        عند نهاية اللعبة:
        {
            "game_over": True,
            "points": مجموع النقاط
        }
        """
        raise NotImplementedError("يجب تنفيذ دالة check_answer في الكلاس الابن")

    # ============================================================
    # التحقق من انتهاء الوقت
    # ============================================================

    def is_expired(self, timeout_minutes: int):
        if not self.start_time:
            return False

        delta = datetime.now() - self.start_time
        return delta.total_seconds() > (timeout_minutes * 60)

    # ============================================================
    # إنهاء اللعبة
    # ============================================================

    def end_game(self):
        self.finished = True
        return {
            "game_over": True,
            "points": self.points
        }
