"""
لعبة الكلمة المبعثرة - Bot Mesh v9.0 FINAL
Created by: Abeer Aldosari © 2025
✅ فردي: لمح (أول حرف + عدد الحروف) + جاوب + مؤقت
✅ فريقين: مؤقت فقط
"""

from games.base_game import BaseGame
import random
import time
from typing import Dict, Any, Optional


class ScrambleWordGame(BaseGame):
    """لعبة الكلمة المبعثرة"""

    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, questions_count=5)
        self.game_name = "كلمة مبعثرة"
        self.game_icon = "🔤"
        self.supports_hint = True
        self.supports_reveal = True

        self.round_time = 25  # ⏱️ 25 ثانية
        self.round_start_time = None

        self.words = [
            "مدرسة","كتاب","قلم","باب","نافذة","طاولة","كرسي","سيارة","طائرة","قطار",
            "سفينة","دراجة","تفاحة","موز","برتقال","عنب","بطيخ","فراولة","شمس","قمر",
            "نجمة","سماء","بحر","جبل","نهر","أسد","نمر","فيل","زرافة","حصان",
            "غزال","ورد","شجرة","زهرة","عشب","ورقة","منزل","مسجد","حديقة","ملعب",
            "مطعم","مكتبة","صديق","عائلة","أخ","أخت","والد","والدة","مطر","ريح",
            "برق","رعد","غيم","ثلج","جليد","نار","ماء","هواء","تراب"
        ]

        random.shuffle(self.words)
        self.used_words = []
        self.current_scrambled = None

    def scramble_word(self, word: str) -> str:
        """خلط حروف الكلمة"""
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

        # ✅ النص الإضافي حسب الوضع
        if self.team_mode:
            additional_info = f"⏱️ {self.round_time} ثانية\nعدد الحروف: {len(word)}"
        else:
            additional_info = f"⏱️ {self.round_time} ثانية\nعدد الحروف: {len(word)}\n💡 اكتب 'لمح' أو 'جاوب'"

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

        # التحقق من الوقت
        if self._time_expired():
            self.current_question += 1
            self.answered_users.clear()

            if self.current_question >= self.questions_count:
                result = self.end_game()
                result["message"] = f"⏱️ انتهى الوقت!\nالإجابة: {self.current_answer}\n\n{result.get('message', '')}"
                return result

            return {
                "message": f"⏱️ انتهى الوقت!\nالإجابة: {self.current_answer}",
                "response": self.get_question(),
                "points": 0
            }

        if user_id in self.answered_users:
            return None

        if self.team_mode and user_id not in self.joined_users:
            return None

        normalized = self.normalize_text(user_answer)

        # ✅ لمح وجاوب للفردي فقط
        if not self.team_mode:
            # التلميح
            if normalized == "لمح":
                hint = f"💡 تبدأ بـ: {self.current_answer[0]}\nعدد الحروف: {len(self.current_answer)}"
                return {
                    "message": hint,
                    "response": self._create_text_message(hint),
                    "points": 0
                }

            # كشف الإجابة
            if normalized == "جاوب":
                reveal = f"الإجابة: {self.current_answer}"
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

        # التحقق من الإجابة
        if normalized == self.normalize_text(self.current_answer):
            base_points = 10
            elapsed = int(time.time() - self.round_start_time)
            remaining = max(0, self.round_time - elapsed)
            time_bonus = max(0, remaining // 2)
            total_points = base_points + time_bonus

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
                "message": f"✅ صحيح!\n+{total_points} نقطة",
                "response": self.get_question(),
                "points": total_points
            }

        return {
            "message": "❌ خطأ",
            "response": self._create_text_message("❌ خطأ"),
            "points": 0
        }
