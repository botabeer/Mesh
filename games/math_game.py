"""
لعبة الرياضيات - Bot Mesh v3.2
أسئلة حسابية ذكية مع صعوبة متدرجة
Created by: Abeer Aldosari © 2025
"""

from games.base_game import BaseGame
import random
from typing import Dict, Any, Optional


class MathGame(BaseGame):
    """لعبة الرياضيات المحسّنة"""

    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, questions_count=5)
        self.game_name = "رياضيات"
        self.game_icon = None

        self.team_mode = False
        self.team_a = set()
        self.team_b = set()

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
        colors = self.get_theme_colors()

        footer_buttons = []
        if not self.team_mode:
            footer_buttons = [
                {
                    "type": "button",
                    "action": {"type": "message", "label": "لمح", "text": "لمح"},
                    "style": "secondary",
                    "height": "sm",
                    "color": colors["shadow1"]
                },
                {
                    "type": "button",
                    "action": {"type": "message", "label": "جاوب", "text": "جاوب"},
                    "style": "secondary",
                    "height": "sm",
                    "color": colors["shadow1"]
                }
            ]

        flex_content = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": f"رياضيات ▫️ {q_data['level_name']}", "align": "center", "weight": "bold"},
                    {"type": "text", "text": q_data["question"], "align": "center", "size": "xl", "margin": "md"},
                ],
                "backgroundColor": colors["bg"],
                "paddingAll": "20px"
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": footer_buttons,
                "backgroundColor": colors["bg"]
            }
        }

        return self._create_flex_with_buttons("رياضيات", flex_content)

    def check_answer(self, user_answer: str, user_id: str, display_name: str):

        if not self.game_active:
            return None

        if self.team_mode:
            if user_id not in self.team_a and user_id not in self.team_b:
                return None

        if user_id in self.answered_users:
            return None

        answer = user_answer.strip()
        normalized = self.normalize_text(answer)

        if not self.team_mode:
            if normalized == "لمح":
                hint = f"الجواب من {len(self.current_answer)} خانات"
                return {'message': hint, 'response': self._create_text_message(hint), 'points': 0}

            if normalized == "جاوب":
                reveal = f"الجواب: {self.current_answer}"
                self.previous_question = self.current_question_data["question"]
                self.previous_answer = self.current_answer
                self.current_question += 1
                self.answered_users.clear()
                return {'message': reveal, 'response': self.get_question(), 'points': 0}

        try:
            user_num = int(answer)
        except:
            return None

        if user_num == int(self.current_answer):

            if self.team_mode:
                team = "A" if user_id in self.team_a else "B"
                self.add_team_score(team, 10)
                self.current_question += 1
                self.answered_users.clear()
                return {'message': f"نقطة لفريق {team}", 'response': self.get_question(), 'points': 0}

            points = self.add_score(user_id, display_name, 10)
            self.current_question += 1
            self.answered_users.clear()
            return {'message': f"إجابة صحيحة +{points}", 'response': self.get_question(), 'points': points}

        return None
