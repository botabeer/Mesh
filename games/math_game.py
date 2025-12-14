from games.base_game import BaseGame
import random
from typing import Dict, Any, Optional

class MathGame(BaseGame):
    """لعبة رياضيات محسّنة"""

    def __init__(self, line_bot_api=None):
        super().__init__(line_bot_api, questions_count=5)
        self.game_name = "رياضيات"
        self.supports_hint = True
        self.supports_reveal = True
        self.current_question_data = None

        self.difficulty_levels = {
            1: {"name": "سهل", "min": 1, "max": 20, "ops": ['+', '-']},
            2: {"name": "متوسط", "min": 10, "max": 50, "ops": ['+', '-', '×']},
            3: {"name": "صعب", "min": 20, "max": 100, "ops": ['+', '-', '×']},
            4: {"name": "صعب جداً", "min": 50, "max": 200, "ops": ['+', '-', '×']},
            5: {"name": "خبير", "min": 100, "max": 500, "ops": ['+', '-', '×', '÷']}
        }

    def generate_math_question(self):
        level = min(self.current_question + 1, 5)
        config = self.difficulty_levels[level]
        operation = random.choice(config["ops"])

        if operation == '+':
            a, b = random.randint(config["min"], config["max"]), random.randint(config["min"], config["max"])
            answer = a + b
            question = f"{a} + {b} = ؟"
        elif operation == '-':
            a = random.randint(config["min"] + 10, config["max"])
            b = random.randint(config["min"], a - 1)
            answer = a - b
            question = f"{a} - {b} = ؟"
        elif operation == '×':
            max_factor = min(20, config["max"] // 10)
            a, b = random.randint(2, max_factor), random.randint(2, max_factor)
            answer = a * b
            question = f"{a} × {b} = ؟"
        else:  # ÷
            divisor = random.randint(2, 15)
            result = random.randint(2, 20)
            a = result * divisor
            answer = result
            question = f"{a} ÷ {divisor} = ؟"

        return {"question": question, "answer": str(answer), "level": level, "level_name": config["name"]}

    def start_game(self):
        self.current_question = 0
        self.game_active = True
        self.previous_question = None
        self.previous_answer = None
        self.answered_users.clear()
        self.scores.clear()
        return self.get_question()

    def get_question(self):
        q_data = self.generate_math_question()
        self.current_question_data = q_data
        self.current_answer = q_data["answer"]

        return self.build_question_flex(
            question_text=q_data["question"],
            additional_info=f"المستوى: {q_data['level_name']}"
        )

    def check_answer(self, user_answer: str, user_id: str, display_name: str) -> Optional[Dict[str, Any]]:
        if not self.game_active or user_id in self.answered_users:
            return None

        normalized = self.normalize_text(user_answer.strip())

        # أمر لمّح
        if self.can_use_hint() and normalized == "لمح":
            hint = f"الجواب يتكون من {len(self.current_answer)} رقم{'s' if len(self.current_answer)>1 else ''}"
            return {"message": hint, "points": 0}

        # أمر جاوب
        if self.can_reveal_answer() and normalized == "جاوب":
            reveal = f"الجواب: {self.current_answer}"
            self.previous_question = self.current_question_data["question"]
            self.previous_answer = self.current_answer
            self.current_question += 1
            self.answered_users.clear()
            if self.current_question >= self.questions_count:
                winner_id, points = self.get_top_scorer()
                self.game_active = False
                return {"response": f"انتهت اللعبة! الفائز: {winner_id} ({points} نقطة)", "points": 0, "game_over": True}
            return {"message": reveal, "response": self.get_question(), "points": 0}

        try:
            user_num = int(normalized)
        except:
            return None

        if user_num == int(self.current_answer):
            points = 1
            self.add_score(user_id, display_name, points)
            self.previous_question = self.current_question_data["question"]
            self.previous_answer = self.current_answer
            self.current_question += 1
            self.answered_users.clear()
            if self.current_question >= self.questions_count:
                winner_id, points = self.get_top_scorer()
                self.game_active = False
                return {"response": f"انتهت اللعبة! الفائز: {winner_id} ({points} نقطة)", "points": points, "game_over": True}
            return {"message": f"صحيح +{points}", "response": self.get_question(), "points": points}

        return None
