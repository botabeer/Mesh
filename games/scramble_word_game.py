from games.base_game import BaseGame
import random
import time
from typing import Dict, Any, Optional


class ScrambleWordGame(BaseGame):
    """لعبة كلمات"""

    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, questions_count=5)
        self.game_name = "كلمات"
        self.game_icon = "▫️"
        self.supports_hint = True
        self.supports_reveal = True

        self.round_time = 25
        self.round_start_time = None

        self.words = [
            "مدرسة","كتاب","قلم","باب","نافذة","طاولة","كرسي","سيارة","طائرة","قطار",
            "سفينة","دراجة","تفاحة","موز","برتقال","عنب","بطيخ","فراولة","شمس","قمر",
            "نجمة","سماء","بحر","جبل","نهر","أسد","نمر","فيل","زرافة","حصان",
            "غزال","ورد","شجرة","زهرة","عشب","ورقة","منزل","مسجد","حديقة","ملعب",
            "مطعم","مكتبة","صديق","عائلة","أخ","أخت","والد","والدة","مطر","ريح",
            "برق","رعد","غيم","ثلج","جليد","نار","ماء","هواء","تراب","صخرة",
            "رمل","وادي","صحراء","غابة","حقل","مزرعة","بستان","طريق","شارع","جسر",
            "نفق","ميدان","حديقة","متحف","سوق","محطة","مطار","ميناء","قرية","مدينة",
            "دولة","قارة","كوكب","نجم","فضاء","سماء","أرض","تلفاز","راديو","هاتف",
            "حاسوب","لوحة","مفتاح","قفل","ساعة","تقويم","صورة","مرآة","فرشاة","صابون"
        ]

        random.shuffle(self.words)
        self.used_words = []
        self.current_scrambled = None

    def scramble_word(self, word: str) -> str:
        letters = list(word)
        attempts = 0
        while attempts < 10:
            random.shuffle(letters)
            scrambled = ''.join(letters)
            if scrambled != word:
                return scrambled
            attempts += 1
        return word[::-1]

    def start_game(self):
        self.current_question = 0
        self.game_active = True
        self.previous_question = None
        self.previous_answer = None
        self.answered_users.clear()
        self.used_words = []
        return self.get_question()

    def get_question(self):
        available = [w for w in self.words if w not in self.used_words]
        if not available:
            self.used_words = []
            available = self.words.copy()

        word = random.choice(available)
        self.used_words.append(word)
        self.current_answer = word
        self.current_scrambled = self.scramble_word(word)
        self.round_start_time = time.time()

        if self.can_use_hint() and self.can_reveal_answer():
            additional_info = f"الوقت {self.round_time} ثانية\nعدد الحروف: {len(word)}\n اكتب 'لمح' أو 'جاوب'"
        else:
            additional_info = f"الوقت {self.round_time} ثانية\nعدد الحروف: {len(word)}"

        return self.build_question_flex(
            question_text=f"رتب الحروف:\n{self.current_scrambled}",
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
            self.previous_question = self.current_scrambled
            self.previous_answer = self.current_answer
            self.current_question += 1
            self.answered_users.clear()

            if self.current_question >= self.questions_count:
                result = self.end_game()
                result["message"] = f"انتهى الوقت\n الإجابة: {self.current_answer}\n\n{result.get('message', '')}"
                return result

            return {
                "message": f"انتهى الوقت\n الإجابة: {self.current_answer}",
                "response": self.get_question(),
                "points": 0
            }

        if user_id in self.answered_users:
            return None

        if self.team_mode and user_id not in self.joined_users:
            return None

        normalized = self.normalize_text(user_answer)

        if self.can_use_hint() and normalized == "لمح":
            hint = f"تبدأ بـ: {self.current_answer[0]}\nعدد الحروف: {len(self.current_answer)}"
            return {
                "message": hint,
                "response": self._create_text_message(hint),
                "points": 0
            }

        if self.can_reveal_answer() and normalized == "جاوب":
            reveal = f"الإجابة: {self.current_answer}"
            self.previous_question = self.current_scrambled
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

        if normalized == self.normalize_text(self.current_answer):
            total_points = 1

            if self.team_mode:
                team = self.get_user_team(user_id)
                if not team:
                    team = self.assign_to_team(user_id)
                self.add_team_score(team, total_points)
            else:
                self.add_score(user_id, display_name, total_points)

            self.previous_question = self.current_scrambled
            self.previous_answer = self.current_answer

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
