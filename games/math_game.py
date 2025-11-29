"""
لعبة الرياضيات - Bot Mesh v13.0 FINAL
Created by: Abeer Aldosari © 2025
✅ نقطة واحدة فقط
✅ عرض السؤال السابق
"""

from games.base_game import BaseGame
import random
import time
from typing import Dict, Any, Optional


class MathGame(BaseGame):
    """لعبة الرياضيات"""

    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, questions_count=5)
        self.game_name = "رياضيات"
        self.game_icon = "▪️"
        self.supports_hint = True
        self.supports_reveal = True

        self.round_time = 25
        self.round_start_time = None

        self.difficulty_levels = {
            1: {"name": "سهل", "min": 1, "max": 20, "ops": ['+', '-']},
            2: {"name": "متوسط", "min": 10, "max": 50, "ops": ['+', '-', '×']},
            3: {"name": "صعب", "min": 20, "max": 100, "ops": ['+', '-', '×']},
            4: {"name": "صعب جداً", "min": 50, "max": 200, "ops": ['+', '-', '×']},
            5: {"name": "خبير", "min": 100, "max": 500, "ops": ['+', '-', '×', '÷']}
        }

        self.current_question_data = None

    def generate_math_question(self):
        level = min(self.current_question + 1, 5)
        config = self.difficulty_levels[level]
        operation = random.choice(config["ops"])

        if operation == '+':
            a = random.randint(config["min"], config["max"])
            b = random.randint(config["min"], config["max"])
            answer = a + b
            question = f"{a} + {b} = ؟"
        elif operation == '-':
            a = random.randint(config["min"] + 10, config["max"])
            b = random.randint(config["min"], a - 1)
            answer = a - b
            question = f"{a} - {b} = ؟"
        elif operation == '×':
            max_factor = min(20, config["max"] // 10)
            a = random.randint(2, max_factor)
            b = random.randint(2, max_factor)
            answer = a * b
            question = f"{a} × {b} = ؟"
        else:
            result = random.randint(2, 20)
            divisor = random.randint(2, 15)
            a = result * divisor
            answer = result
            question = f"{a} ÷ {divisor} = ؟"

        return {
            "question": question,
            "answer": str(answer),
            "level": level,
            "level_name": config["name"]
        }

    def start_game(self):
        self.current_question = 0
        self.game_active = True
        self.previous_question = None
        self.previous_answer = None
        self.answered_users.clear()
        return self.get_question()

    def get_question(self):
        q_data = self.generate_math_question()
        self.current_question_data = q_data
        self.current_answer = q_data["answer"]
        self.round_start_time = time.time()

        if self.can_use_hint() and self.can_reveal_answer():
            additional_info = f"⏱️ {self.round_time} ثانية | المستوى: {q_data['level_name']}\n▪️ اكتب 'لمح' أو 'جاوب'"
        else:
            additional_info = f"⏱️ {self.round_time} ثانية | المستوى: {q_data['level_name']}"

        return self.build_question_flex(
            question_text=q_data["question"],
            additional_info=additional_info
        )

    def _time_expired(self) -> bool:
        if not self.round_start_time:
            return False
        return (time.time() - self.round_start_time) > self.round_time

    def check_answer(self, user_answer: str, user_id: str, display_name: str) -> Optional[Dict[str, Any]]:
        if not self.game_active:
            return None

        if self._time_expired():
            self.previous_question = self.current_question_data["question"] if self.current_question_data else None
            self.previous_answer = self.current_answer
            self.current_question += 1
            self.answered_users.clear()

            if self.current_question >= self.questions_count:
                result = self.end_game()
                result["message"] = f"⏱️ انتهى الوقت!\n▪️ الإجابة: {self.current_answer}\n\n{result.get('message', '')}"
                return result

            return {
                "message": f"⏱️ انتهى الوقت!\n▪️ الإجابة: {self.current_answer}",
                "response": self.get_question(),
                "points": 0
            }

        if user_id in self.answered_users:
            return None

        if self.team_mode and user_id not in self.joined_users:
            return None

        answer = user_answer.strip()
        normalized = self.normalize_text(answer)

        if self.can_use_hint() and normalized == "لمح":
            hint = f"▪️ الجواب من {len(self.current_answer)} خانات"
            return {
                "message": hint,
                "response": self._create_text_message(hint),
                "points": 0
            }

        if self.can_reveal_answer() and normalized == "جاوب":
            reveal = f"▪️ الجواب: {self.current_answer}"
            self.previous_question = self.current_question_data["question"] if self.current_question_data else None
            self.previous_answer = self.current_answer
            self.current_question += 1
            self.answered_users.clear()

            if self.current_question >= self.questions_count:
                result = self.end_game()
                result["message"] = f"{reveal}\n\n{result.get('message', '')}"
                return result

            return {
                "message": reveal,
                "response": self.get_question(),
                "points": 0
            }

        if self.team_mode and normalized in ["لمح", "جاوب"]:
            return None

        try:
            user_num = int(answer)
        except:
            return {
                "message": "▪️ يرجى إدخال رقم صحيح",
                "response": self._create_text_message("▪️ يرجى إدخال رقم صحيح"),
                "points": 0
            }

        if user_num == int(self.current_answer):
            total_points = 1

            if self.team_mode:
                team = self.get_user_team(user_id)
                if not team:
                    team = self.assign_to_team(user_id)
                self.add_team_score(team, total_points)
            else:
                self.add_score(user_id, display_name, total_points)

            self.previous_question = self.current_question_data["question"] if self.current_question_data else None
            self.previous_answer = self.current_answer

            self.current_question += 1
            self.answered_users.clear()

            if self.current_question >= self.questions_count:
                result = self.end_game()
                result["points"] = total_points
                return result

            return {
                "message": f"▪️ إجابة صحيحة!\n+{total_points} نقطة",
                "response": self.get_question(),
                "points": total_points
            }

        return {
            "message": "▪️ إجابة خاطئة",
            "response": self._create_text_message("▪️ إجابة خاطئة"),
            "points": 0
        }
