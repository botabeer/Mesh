import random
from games.base_game import BaseGame


class ScrambleGame(BaseGame):
    def __init__(self, line_bot_api, difficulty=3, theme='light'):
        super().__init__(line_bot_api, difficulty=difficulty, theme=theme)
        self.game_name = "ترتيب"

        self.words = [
            "مدرسة", "كتاب", "قلم", "باب", "نافذة", "طاولة", "كرسي",
            "سيارة", "طائرة", "حديقة", "شجرة", "وردة", "فراشة",
            "سمكة", "نجمة", "قمر", "شمس", "سحابة", "مطر",
            "جبل", "بحر", "نهر", "صحراء", "جزيرة",
            "مدينة", "قرية", "بيت", "مسجد", "مستشفى", "جامعة",
            "مكتبة", "متحف", "سوق", "ملعب", "مسبح", "مطار",
            "جسر", "طريق", "شارع", "ميدان"
        ]

        random.shuffle(self.words)
        self.used_words = []

    def scramble_word(self, word):
        letters = list(word)
        for _ in range(10):
            random.shuffle(letters)
            if ''.join(letters) != word:
                break
        return " ".join(letters)

    def get_question(self):
        available = [w for w in self.words if w not in self.used_words]
        if not available:
            self.used_words = []
            available = self.words.copy()
            random.shuffle(available)

        word = random.choice(available)
        self.used_words.append(word)
        self.current_answer = word

        return self.build_question_message(
            f"رتب الحروف:\n{self.scramble_word(word)}"
        )

    def check_answer(self, user_answer, user_id, display_name):
        if not self.game_active or user_id in self.answered_users:
            return None

        normalized = self.normalize_text(user_answer)

        if normalized == "ايقاف":
            return self.handle_withdrawal(user_id, display_name)

        if self.supports_reveal and normalized == "جاوب":
            self.previous_answer = str(self.current_answer)
            self.current_question += 1
            self.answered_users.clear()
            if self.current_question >= self.questions_count:
                return self.end_game()
            return {"response": self.get_question(), "points": 0, "next_question": True}

        if normalized == self.normalize_text(str(self.current_answer)):
            return self.handle_correct_answer(user_id, display_name)

        return None
