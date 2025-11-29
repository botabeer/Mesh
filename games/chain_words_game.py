"""
لعبة سلسلة الكلمات (سلسلة) - Bot Mesh v13.0 FINAL
Created by: Abeer Aldosari © 2025
✅ نقطة واحدة فقط
✅ عرض السؤال السابق
"""

from games.base_game import BaseGame
import random
import time
from typing import Dict, Any, Optional


class ChainWordsGame(BaseGame):
    """لعبة سلسلة"""

    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, questions_count=5)
        self.game_name = "سلسلة"
        self.game_icon = "▪️"
        self.supports_hint = False
        self.supports_reveal = False

        self.round_time = 25
        self.round_start_time = None

        self.starting_words = [
            "سيارة","تفاح","قلم","نجم","كتاب","باب","رمل","لعبة","حديقة","ورد",
            "دفتر","معلم","منزل","شمس","سفر","رياضة","علم","مدرسة","طائرة","عصير",
            "بحر","سماء","طريق","جبل","مدينة","شجرة","حاسب","هاتف","ساعة","مطر",
            "زهرة","سرير","مطبخ","نافذة","مفتاح","مصباح","وسادة","بطارية","لوحة",
            "حقيبة","مزرعة","قطار","مكتبة","مستشفى","ملعب","مسبح","مقهى","مكتب","مطار"
        ]

        self.last_word = None
        self.used_words = set()

    def start_game(self):
        self.current_question = 0
        self.game_active = True
        self.previous_question = None
        self.previous_answer = None
        self.last_word = random.choice(self.starting_words)
        self.used_words = {self.normalize_text(self.last_word)}
        self.answered_users.clear()
        return self.get_question()

    def get_question(self):
        required_letter = self.last_word[-1]
        self.round_start_time = time.time()

        additional_info = f"⏱️ {self.round_time} ثانية\nابدأ بحرف: {required_letter}"

        return self.build_question_flex(
            question_text=f"الكلمة السابقة:\n{self.last_word}",
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
            self.previous_question = f"كلمة تبدأ بـ {self.last_word[-1]}"
            self.previous_answer = "انتهى الوقت"
            self.current_question += 1
            self.answered_users.clear()

            if self.current_question >= self.questions_count:
                result = self.end_game()
                result["message"] = f"⏱️ انتهى الوقت!\n\n{result.get('message', '')}"
                return result

            return {
                "message": "⏱️ انتهى الوقت!",
                "response": self.get_question(),
                "points": 0
            }

        if user_id in self.answered_users:
            return None

        if self.team_mode and user_id not in self.joined_users:
            return None

        normalized_answer = self.normalize_text(user_answer)

        if normalized_answer in self.used_words:
            return {
                "message": "▪️ الكلمة مستخدمة",
                "response": self._create_text_message("▪️ الكلمة مستخدمة"),
                "points": 0
            }

        required_letter = self.normalize_text(self.last_word[-1])

        if normalized_answer and normalized_answer[0] == required_letter and len(normalized_answer) >= 2:
            self.used_words.add(normalized_answer)
            
            self.previous_question = f"كلمة تبدأ بـ {self.last_word[-1]}"
            self.previous_answer = user_answer.strip()
            
            self.last_word = user_answer.strip()
            
            total_points = 1

            if self.team_mode:
                team = self.get_user_team(user_id)
                if not team:
                    team = self.assign_to_team(user_id)
                self.add_team_score(team, total_points)
            else:
                self.add_score(user_id, display_name, total_points)

            self.current_question += 1
            self.answered_users.clear()

            if self.current_question >= self.questions_count:
                result = self.end_game()
                result["points"] = total_points
                return result

            return {
                "message": f"▪️ صحيح!\n+{total_points} نقطة",
                "response": self.get_question(),
                "points": total_points
            }

        return {
            "message": f"▪️ يجب أن تبدأ بحرف {required_letter}",
            "response": self._create_text_message(f"▪️ يجب أن تبدأ بحرف {required_letter}"),
            "points": 0
        }
