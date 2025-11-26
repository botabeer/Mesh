"""
القاعدة الأساسية لجميع الألعاب
تم إنشاء هذا البوت بواسطة عبير الدوسري © 2025
"""

import re
from collections import defaultdict
from datetime import datetime


class BaseGame:
    """الفئة الأساسية لجميع الألعاب"""

    def __init__(self, name, total_rounds=10, time_limit_minutes=10):
        self.name = name
        self.total_rounds = total_rounds
        self.current_round = 0
        self.scores = defaultdict(int)
        self.answered_users = set()
        self.current_answer = None
        self.game_active = False
        self.started_at = None
        self.time_limit_minutes = time_limit_minutes

    # ==========================
    # أدوات مساعدة
    # ==========================

    def is_expired(self, minutes=None):
        limit = minutes or self.time_limit_minutes
        if not self.started_at:
            return False
        return (datetime.now() - self.started_at).total_seconds() > limit * 60

    def normalize_text(self, text):
        if not text:
            return ""
        text = text.strip().lower()
        text = re.sub(r'^ال', '', text)

        replacements = {
            'أ': 'ا', 'إ': 'ا', 'آ': 'ا',
            'ة': 'ه', 'ى': 'ي', 'ؤ': 'و', 'ئ': 'ي'
        }
        for old, new in replacements.items():
            text = text.replace(old, new)

        text = re.sub(r'[\u064B-\u065F\u0670]', '', text)
        return text

    # ==========================
    # دورة اللعبة
    # ==========================

    def start(self):
        self.current_round = 1
        self.scores.clear()
        self.answered_users.clear()
        self.game_active = True
        self.started_at = datetime.now()

    def get_question(self):
        """
        يجب أن تعيد:
        {
            'text': نص السؤال,
            'round': رقم الجولة,
            'total_rounds': إجمالي الجولات
        }
        """
        raise NotImplementedError

    def check_answer(self, user_answer, user_id, display_name):
        if not self.game_active:
            return {'game_over': True}

        if user_id in self.answered_users:
            return {'ignored': True}

        normalized_user = self.normalize_text(user_answer)
        normalized_correct = self.normalize_text(str(self.current_answer))

        if normalized_user == normalized_correct:
            self.add_score(user_id, display_name, 10)
            return self._next_step(correct=True)
        else:
            self.answered_users.add(user_id)
            return {'correct': False}

    def _next_step(self, correct=False):
        if self.current_round >= self.total_rounds:
            return self.end_game()

        self.current_round += 1
        self.answered_users.clear()
        return {
            'game_over': False,
            'next_question': self.get_question()
        }

    # ==========================
    # النتائج
    # ==========================

    def add_score(self, user_id, display_name, points=10):
        self.scores[display_name] += points
        self.answered_users.add(user_id)

    def end_game(self):
        self.game_active = False

        if not self.scores:
            return {
                'game_over': True,
                'points': 0,
                'summary': "انتهت اللعبة بدون مشاركات"
            }

        sorted_scores = sorted(
            self.scores.items(),
            key=lambda x: x[1],
            reverse=True
        )

        winner_name, winner_score = sorted_scores[0]

        return {
            'game_over': True,
            'winner': winner_name,
            'points': winner_score,
            'leaderboard': sorted_scores
        }

    # ==========================
    # أدوات اختيارية
    # ==========================

    def get_hint(self):
        if not self.current_answer:
            return None
        answer = str(self.current_answer)
        part = len(answer) // 3
        return answer[:part] + "..."

    def reveal_answer(self):
        if not self.current_answer:
            return None
        return str(self.current_answer)
