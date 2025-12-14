from games.base_game import BaseGame
import random
from typing import Dict, Any, Optional

class ScrambleWordGame(BaseGame):
    """لعبة ترتيب محسّنة"""

    def __init__(self, line_bot_api=None):
        super().__init__(line_bot_api, questions_count=5)
        self.game_name = "ترتيب"
        self.supports_hint = True
        self.supports_reveal = True

        self.words = [
            "مدرسة", "كتاب", "قلم", "باب", "نافذة", "طاولة", "كرسي", "سيارة",
            "طائرة", "قطار", "تفاحة", "موز", "برتقال", "عنب", "بطيخ", "شمس",
            "قمر", "نجمة", "سماء", "بحر", "جبل", "نهر", "أسد", "نمر", "فيل",
            "زرافة", "حصان", "ورد", "شجرة", "زهرة", "منزل", "مسجد", "حديقة",
            "ملعب", "مطعم", "مكتبة", "صديق", "عائلة", "مطر", "ريح", "برق",
            "غيم", "ثلج", "نار", "ماء", "هواء", "صخرة", "رمل", "غابة"
        ]
        random.shuffle(self.words)
        self.used_words = []
        self.current_scrambled = None
        self.current_answer = None

    def scramble_word(self, word: str) -> str:
        letters = list(word)
        attempts = 0
        while attempts < 10:
            random.shuffle(letters)
            scrambled = ' '.join(letters)
            if scrambled.replace(' ', '') != word:
                return scrambled
            attempts += 1
        return ' '.join(word[::-1])

    def start_game(self):
        self.current_question = 0
        self.game_active = True
        self.previous_question = None
        self.previous_answer = None
        self.answered_users.clear()
        self.used_words.clear()
        return self.get_question()

    def get_question(self):
        available = [w for w in self.words if w not in self.used_words]
        if not available:
            self.used_words.clear()
            available = self.words.copy()

        word = random.choice(available)
        self.used_words.append(word)
        self.current_answer = word
        self.current_scrambled = self.scramble_word(word)

        return self.build_question_flex(
            question_text=f"رتب الحروف:\n\n{self.current_scrambled}",
            additional_info=f"عدد الحروف: {len(word)}"
        )

    def check_answer(self, user_answer: str, user_id: str, display_name: str) -> Optional[Dict[str, Any]]:
        if not self.game_active or user_id in self.answered_users:
            return None

        normalized = self.normalize_text(user_answer.strip())

        # أمر لمّح
        if self.can_use_hint() and normalized == "لمح":
            hint = f"تبدأ بـ {self.current_answer[0]}\nعدد الحروف: {len(self.current_answer)}"
            return {"message": hint, "points": 0}

        # أمر جاوب
        if self.can_reveal_answer() and normalized == "جاوب":
            reveal = f"الإجابة: {self.current_answer}"
            self.previous_question = self.current_scrambled
            self.previous_answer = self.current_answer
            self.current_question += 1
            self.answered_users.clear()
            if self.current_question >= self.questions_count:
                result = self.end_game()
                result["message"] = f"{reveal}\n\nانتهت اللعبة"
                return result
            return {"message": reveal, "response": self.get_question(), "points": 0}

        # قبول أي إجابة صحيحة حتى لو مش موجودة مسبقًا
        self.answered_users.add(user_id)
        points = 1
        self.add_score(user_id, display_name, points)

        self.previous_question = self.current_scrambled
        self.previous_answer = normalized
        self.current_question += 1
        self.answered_users.clear()

        if self.current_question >= self.questions_count:
            result = self.end_game()
            result["points"] = points
            return result

        return {"message": f"صحيح +{points}", "response": self.get_question(), "points": points}
