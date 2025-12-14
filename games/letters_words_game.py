from games.base_game import BaseGame
import random
from typing import Dict, Any, Optional
from linebot.v3.messaging import FlexMessage, FlexContainer, TextMessage

class LettersWordsGame(BaseGame):
    """لعبة تكوين: تقبل أي كلمة صحيحة"""

    def __init__(self, line_bot_api=None):
        super().__init__(line_bot_api, questions_count=5)
        self.game_name = "تكوين"
        self.supports_hint = True
        self.supports_reveal = True

        self.letter_sets = [
            {"letters": ["ق","ل","م","ع","ر","ب"]},
            {"letters": ["س","ا","ر","ة","ي","م"]},
            {"letters": ["ك","ت","ا","ب","م","ل"]},
            {"letters": ["د","ر","س","ة","م","ا"]},
            {"letters": ["ح","د","ي","ق","ة","ر"]}
        ]
        random.shuffle(self.letter_sets)
        self.current_set = None
        self.found_words = set()
        self.required_words = 3

    def start_game(self):
        self.current_question = 0
        self.game_active = True
        self.previous_question = None
        self.previous_answer = None
        self.answered_users.clear()
        self.found_words.clear()
        self.scores.clear()
        return self.get_question()

    def get_question(self):
        self.current_set = self.letter_sets[self.current_question % len(self.letter_sets)]
        self.found_words.clear()
        letters_display = " ".join(self.current_set["letters"])
        return self.build_question_flex(
            question_text=f"كون كلمات من:\n{letters_display}",
            additional_info=f"مطلوب {self.required_words} كلمات"
        )

    def check_answer(self, user_answer: str, user_id: str, display_name: str) -> Optional[Dict[str, Any]]:
        if not self.game_active:
            return None
        if self.team_mode and user_id not in self.joined_users:
            return None

        normalized = self.normalize_text(user_answer)
        if not normalized or len(normalized) < 1:
            return None

        # أمر لمّح
        if self.can_use_hint() and normalized == "لمح":
            example = user_answer[0] if user_answer else self.current_set["letters"][0]
            hint = f"تبدأ بحرف {example} | حاول تخمين كلمة"
            return {"message": hint, "points": 0}

        # أمر جاوب
        if self.can_reveal_answer() and normalized == "جاوب":
            reveal = "أي كلمة صالحة مقبولة"
            self.previous_question = " ".join(self.current_set["letters"])
            self.previous_answer = reveal
            self.current_question += 1
            self.answered_users.clear()
            self.found_words.clear()
            if self.current_question >= self.questions_count:
                winner_id, points = self.get_top_scorer()
                self.game_active = False
                return {
                    "response": TextMessage(text=f"انتهت اللعبة! الفائز: {winner_id} ({points} نقطة)"),
                    "points": 0,
                    "game_over": True
                }
            return {"message": reveal, "response": self.get_question(), "points": 0}

        # كل كلمة تعتبر صحيحة
        if normalized in self.found_words:
            return None  # لمنع التكرار

        self.found_words.add(normalized)
        points = 1
        if self.team_mode:
            team = self.get_user_team(user_id) or self.assign_to_team(user_id)
            self.add_team_score(team, points)
        else:
            self.add_score(user_id, display_name, points)

        if len(self.found_words) >= self.required_words:
            self.current_question += 1
            self.answered_users.clear()
            self.found_words.clear()
            if self.current_question >= self.questions_count:
                winner_id, points = self.get_top_scorer()
                self.game_active = False
                return {
                    "response": TextMessage(text=f"انتهت اللعبة! الفائز: {winner_id} ({points} نقطة)"),
                    "points": points,
                    "game_over": True
                }
            return {"message": f"تم +{points}", "response": self.get_question(), "points": points}

        remaining = self.required_words - len(self.found_words)
        return {"message": f"صحيح، تبقى {remaining} كلمات\n+{points}", "points": points}
