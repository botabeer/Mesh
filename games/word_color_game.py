from games.base_game import BaseGame
import random
import time
from typing import Dict, Any, Optional


class WordColorGame(BaseGame):
    """لعبة ألوان - اختبار Stroop"""

    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, questions_count=5)
        self.game_name = "ألوان"
        self.game_icon = ""
        self.supports_hint = True
        self.supports_reveal = True

        self.round_time = 15
        self.round_start_time = None

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
        self.round_start_time = time.time()

        theme_colors = self.get_theme_colors()
        display_color = self.word_colors[color_name]

        additional_info = f"الوقت {self.round_time} ثانية"
        
        base_flex = self.build_question_flex(
            question_text=f"ما لون هذه الكلمة؟\n\n{word}",
            additional_info=additional_info
        )
        
        flex_dict = base_flex.contents.to_dict()
        
        for content in flex_dict['body']['contents']:
            if content.get('type') == 'box' and 'contents' in content:
                for item in content['contents']:
                    if item.get('type') == 'text' and word in item.get('text', ''):
                        item['text'] = f"ما لون هذه الكلمة؟"
                        content['contents'].append({
                            "type": "text",
                            "text": word,
                            "size": "xxl",
                            "weight": "bold",
                            "color": display_color,
                            "align": "center",
                            "margin": "lg"
                        })
                        break
        
        return self._create_flex_with_buttons(self.game_name, flex_dict)

    def _time_expired(self) -> bool:
        if not self.round_start_time:
            return False
        return (time.time() - self.round_start_time) > self.round_time

    def check_answer(self, user_answer: str, user_id: str, display_name: str) -> Optional[Dict[str, Any]]:
        if not self.game_active:
            return None

        if self._time_expired():
            correct_answer = self.current_answer[0]
            self.previous_question = f"كلمة {self.current_word} ملونة بـ"
            self.previous_answer = correct_answer
            self.current_question += 1
            self.answered_users.clear()

            if self.current_question >= self.questions_count:
                result = self.end_game()
                result["message"] = f"انتهى الوقت\nالإجابة: {correct_answer}\n\n{result.get('message', '')}"
                return result

            return {
                "message": f"انتهى الوقت\nالإجابة: {correct_answer}",
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
            total_points = 1

            if self.team_mode:
                team = self.get_user_team(user_id)
                if not team:
                    team = self.assign_to_team(user_id)
                self.add_team_score(team, total_points)
            else:
                self.add_score(user_id, display_name, total_points)

            self.previous_question = f"كلمة {self.current_word} ملونة بـ"
            self.previous_answer = self.current_answer[0]

            self.answered_users.add(user_id)
            self.current_question += 1
            self.answered_users.clear()

            if self.current_question >= self.questions_count:
                result = self.end_game()
                result["points"] = total_points
                return result

            return {
                "message": f"صحيح\n+{total_points} نقطة",
                "response": self.get_question(),
                "points": total_points
            }

        return {
            "message": "خطأ",
            "response": self._create_text_message("خطأ"),
            "points": 0
        }
