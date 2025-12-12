from games.base_game import BaseGame
import random
from typing import Dict, Any, Optional


class RouletteGame(BaseGame):
    """لعبة روليت"""

    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, questions_count=5)
        self.game_name = "روليت"
        self.supports_hint = True
        self.supports_reveal = True

        self.roulette_numbers = list(range(0, 37))
        self.red_numbers = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
        self.black_numbers = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
        
        self.current_spin_result = None
        self.last_spin_result = None

    def start_game(self):
        """بدء اللعبة"""
        self.current_question = 0
        self.game_active = True
        self.previous_question = None
        self.previous_answer = None
        self.answered_users.clear()
        self.scores.clear()
        return self.get_question()

    def spin_roulette(self):
        """تدوير الروليت"""
        return random.choice(self.roulette_numbers)

    def get_color(self, number: int) -> str:
        """الحصول على لون الرقم"""
        if number == 0:
            return "أخضر"
        elif number in self.red_numbers:
            return "أحمر"
        else:
            return "أسود"

    def get_question(self):
        """الحصول على سؤال"""
        self.current_spin_result = self.spin_roulette()
        result_color = self.get_color(self.current_spin_result)

        return self.build_question_flex(
            question_text=f"تدور الروليت\n\n{self.current_spin_result}\n{result_color}",
            additional_info="خمن ماذا سيكون\nرقم - لون - زوجي/فردي - نطاق"
        )

    def check_answer(self, user_answer: str, user_id: str, display_name: str) -> Optional[Dict[str, Any]]:
        """التحقق من الإجابة"""
        if not self.game_active or user_id in self.answered_users:
            return None

        normalized = self.normalize_text(user_answer)

        if self.can_use_hint() and normalized == "لمح":
            result_color = self.get_color(self.current_spin_result)
            is_even = self.current_spin_result % 2 == 0 and self.current_spin_result != 0
            hint = f"اللون: {result_color}\n"
            hint += "زوجي" if is_even else "فردي" if self.current_spin_result != 0 else "صفر"
            return {"message": hint, "points": 0}

        if self.can_reveal_answer() and normalized == "جاوب":
            reveal = f"الرقم: {self.current_spin_result}\nاللون: {self.get_color(self.current_spin_result)}"
            self.previous_question = "تخمين الروليت"
            self.previous_answer = reveal
            self.last_spin_result = self.current_spin_result
            self.current_question += 1
            self.answered_users.clear()

            if self.current_question >= self.questions_count:
                result = self.end_game()
                result["message"] = f"{reveal}\n\nانتهت اللعبة"
                return result

            return {"message": reveal, "response": self.get_question(), "points": 0}

        won = False
        win_type = ""
        
        try:
            guess_number = int(user_answer.strip())
            if 0 <= guess_number <= 36 and guess_number == self.current_spin_result:
                won = True
                win_type = "رقم مباشر"
        except ValueError:
            pass
        
        if not won:
            result_color = self.get_color(self.current_spin_result)
            if normalized in ["احمر", "اسود"]:
                if (normalized == "احمر" and result_color == "أحمر") or \
                   (normalized == "اسود" and result_color == "أسود"):
                    won = True
                    win_type = "لون"
        
        if not won and self.current_spin_result != 0:
            is_even = self.current_spin_result % 2 == 0
            if (normalized == "زوجي" and is_even) or (normalized == "فردي" and not is_even):
                won = True
                win_type = "زوجي/فردي"
        
        if not won:
            if normalized in ["منخفض", "صغير"] and 1 <= self.current_spin_result <= 18:
                won = True
                win_type = "نطاق منخفض"
            elif normalized in ["مرتفع", "كبير"] and 19 <= self.current_spin_result <= 36:
                won = True
                win_type = "نطاق مرتفع"

        if won:
            total_points = 1

            self.add_score(user_id, display_name, total_points)

            self.previous_question = "تخمين الروليت"
            self.previous_answer = f"{self.current_spin_result} - {self.get_color(self.current_spin_result)}"
            self.last_spin_result = self.current_spin_result
            self.current_question += 1
            self.answered_users.clear()

            if self.current_question >= self.questions_count:
                result = self.end_game()
                result["points"] = total_points
                return result

            return {
                "message": f"صحيح - {win_type} +{total_points}",
                "response": self.get_question(),
                "points": total_points
            }

        return None
