"""
لعبة لون الكلمة (Stroop Effect) - Bot Mesh v9.0 FINAL
Created by: Abeer Aldosari © 2025
✅ بدون لمح/جاوب (لعبة بصرية)
✅ مع مؤقت 15 ثانية
✅ 5 جولات ثم الفائز
"""

from games.base_game import BaseGame
import random
import time
from typing import Dict, Any, Optional


class WordColorGame(BaseGame):
    """لعبة لون الكلمة - اختبار Stroop"""

    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, questions_count=5)
        self.game_name = "لون"
        self.game_icon = "🎨"
        self.supports_hint = False  # ❌ لعبة بصرية
        self.supports_reveal = False  # ❌ لعبة بصرية

        self.round_time = 15  # ⏱️ 15 ثانية
        self.round_start_time = None

        self.colors = {
            "أحمر": "#E53E3E",
            "أزرق": "#3182CE",
            "أخضر": "#38A169",
            "أصفر": "#D69E2E",
            "برتقالي": "#DD6B20",
            "بنفسجي": "#805AD5",
            "وردي": "#D53F8C",
            "بني": "#8B4513"
        }
        self.color_names = list(self.colors.keys())

    def start_game(self):
        self.current_question = 0
        self.game_active = True
        self.previous_question = None
        self.previous_answer = None
        self.answered_users.clear()
        return self.get_question()

    def get_question(self):
        # اختيار كلمة ولون
        word = random.choice(self.color_names)
        color_name = random.choice([c for c in self.color_names if c != word]) if random.random() < 0.7 else word
        self.current_answer = [color_name]
        self.round_start_time = time.time()

        colors = self.get_theme_colors()
        display_color = self.colors[color_name]

        question_text = f"ما لون هذه الكلمة؟\n\n{word}"
        additional_info = f"⏱️ {self.round_time} ثانية"

        # نستخدم TextMessage بدلاً من Flex لأن Flex لا يدعم الألوان المخصصة
        msg = self._create_text_message(
            f"🎨 {self.game_name}\n"
            f"سؤال {self.current_question + 1} من {self.questions_count}\n\n"
            f"{question_text}\n\n"
            f"{additional_info}"
        )
        return msg

    def _time_expired(self) -> bool:
        if not self.round_start_time:
            return False
        return (time.time() - self.round_start_time) > self.round_time

    def check_answer(self, user_answer: str, user_id: str, display_name: str) -> Optional[Dict[str, Any]]:
        if not self.game_active:
            return None

        # التحقق من الوقت
        if self._time_expired():
            correct_answer = self.current_answer[0]
            self.current_question += 1
            self.answered_users.clear()

            if self.current_question >= self.questions_count:
                result = self.end_game()
                result["message"] = f"⏱️ انتهى الوقت!\nالإجابة: {correct_answer}\n\n{result.get('message', '')}"
                return result

            return {
                "message": f"⏱️ انتهى الوقت!\nالإجابة: {correct_answer}",
                "response": self.get_question(),
                "points": 0
            }

        if user_id in self.answered_users:
            return None

        if self.team_mode and user_id not in self.joined_users:
            return None

        normalized = self.normalize_text(user_answer)
        correct = self.normalize_text(self.current_answer[0])

        if normalized == correct:
            # حساب النقاط مع بونص الوقت
            base_points = 10
            elapsed = int(time.time() - self.round_start_time)
            remaining = max(0, self.round_time - elapsed)
            time_bonus = remaining  # نقطة لكل ثانية متبقية
            total_points = base_points + time_bonus

            if self.team_mode:
                team = self.get_user_team(user_id)
                if not team:
                    team = self.assign_to_team(user_id)
                self.add_team_score(team, total_points)
            else:
                self.add_score(user_id, display_name, total_points)

            self.answered_users.add(user_id)
            self.current_question += 1
            self.answered_users.clear()

            if self.current_question >= self.questions_count:
                result = self.end_game()
                result["points"] = total_points
                return result

            return {
                "message": f"✅ صحيح!\n+{total_points} نقطة",
                "response": self.get_question(),
                "points": total_points
            }

        return {
            "message": "❌ خطأ",
            "response": self._create_text_message("❌ خطأ"),
            "points": 0
        }
