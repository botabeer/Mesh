from games.base_game import BaseGame
import random
from typing import Dict, Any, Optional


class WordColorGame(BaseGame):
    """لعبة لون - اختبار Stroop محسّن"""

    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, questions_count=5)
        self.game_name = "لون"
        self.supports_hint = True
        self.supports_reveal = True

        self.word_colors = {
            "أحمر": "#E53E3E",
            "أزرق": "#3182CE",
            "أخضر": "#38A169",
            "أصفر": "#D69E2E",
            "برتقالي": "#DD6B20",
            "بنفسجي": "#805AD5",
            "وردي": "#D53F8C",
            "بني": "#8B4513"
        }
        self.color_names = list(self.word_colors.keys())
        self.current_word = None
        self.current_color_name = None

    def start_game(self):
        self.current_question = 0
        self.game_active = True
        self.previous_question = None
        self.previous_answer = None
        self.answered_users.clear()
        return self.get_question()

    def get_question(self):
        word = random.choice(self.color_names)
        color_name = random.choice([c for c in self.color_names if c != word]) if random.random() < 0.7 else word

        self.current_word = word
        self.current_color_name = color_name
        self.current_answer = [color_name]

        return self.build_question_flex(
            question_text=f"ما لون هذه الكلمة\n\n{word}"
        )

    def check_answer(self, user_answer: str, user_id: str, display_name: str) -> Optional[Dict[str, Any]]:
        if not self.game_active:
            return None

        if self.team_mode and user_id not in self.joined_users:
            return None

        if user_id in self.answered_users:
            return None

        normalized = self.normalize_text(user_answer)

        # تلميح
        if self.can_use_hint() and normalized == "لمح":
            hint = f"يبدأ بـ {self.current_answer[0][0]} | عدد الحروف {len(self.current_answer[0])}"
            return {"message": hint, "response": self._create_text_message(hint), "points": 0}

        # كشف الإجابة
        if self.can_reveal_answer() and normalized == "جاوب":
            reveal = f"الإجابة: {self.current_answer[0]}"
            self.previous_question = f"كلمة {self.current_word} ملونة بـ"
            self.previous_answer = self.current_answer[0]
            self.current_question += 1
            self.answered_users.clear()
            if self.current_question >= self.questions_count:
                result = self.end_game()
                result["message"] = f"{reveal}\n\n{result.get('message', '')}"
                return result
            return {"message": reveal, "response": self.get_question(), "points": 0}

        correct = self.normalize_text(self.current_answer[0])

        if normalized == correct:
            total_points = 1
            if self.team_mode:
                team = self.get_user_team(user_id) or self.assign_to_team(user_id)
                self.add_team_score(team, total_points)
            else:
                self.add_score(user_id, display_name, total_points)

            self.previous_question = f"كلمة {self.current_word} ملونة بـ"
            self.previous_answer = self.current_answer[0]
            self.current_question += 1
            self.answered_users.clear()

            if self.current_question >= self.questions_count:
                result = self.end_game()
                result["points"] = total_points
                return result

            return {"message": f"صحيح +{total_points}", "response": self.get_question(), "points": total_points}

        return None
