# games/guess_game.py
import random
from linebot.models import TextSendMessage
from utils.helpers import normalize_text

class GuessGame:
    def __init__(self):
        self.current_number = None
        self.min_number = 1
        self.max_number = 100
        self.hint_used = False
        self.scores = {}

    # ---------------------------- بدء اللعبة ---------------------------- #
    def start_game(self):
        self.current_number = random.randint(self.min_number, self.max_number)
        self.hint_used = False
        text = (
            f"🎯 لعبة التخمين\n\n"
            f"اختر رقماً بين {self.min_number} و {self.max_number}\n"
            f"حاول أن تخمن الرقم الصحيح!"
        )
        return TextSendMessage(text=text)

    # ---------------------------- فحص الإجابة ---------------------------- #
    def check_answer(self, answer, user_id, display_name):
        if self.current_number is None:
            return None

        try:
            guess = int(answer)
        except ValueError:
            return None

        if guess == self.current_number:
            points = 10 if not self.hint_used else 5
            self.scores[user_id] = self.scores.get(user_id, 0) + points
            new_game = self.start_game()
            msg = (
                f"✔️ أحسنت يا {display_name}! الرقم الصحيح كان: {self.current_number}\n"
                f"+{points} نقاط (النقاط الحالية: {self.scores[user_id]})\n\n"
                f"🎮 جولة جديدة:\n{new_game.text}"
            )
            return {
                "points": points,
                "won": True,
                "message": msg,
                "response": new_game,
                "game_over": False
            }
        elif guess < self.current_number:
            return TextSendMessage(text="🔼 الرقم أكبر من تخمينك")
        else:
            return TextSendMessage(text="🔽 الرقم أصغر من تخمينك")

    # ---------------------------- التلميح ---------------------------- #
    def get_hint(self):
        if self.current_number is None:
            return "لا توجد لعبة حالياً"
        self.hint_used = True
        mid = (self.min_number + self.max_number) // 2
        hint_text = "الرقم أعلى من منتصف المدى" if self.current_number > mid else "الرقم أقل من منتصف المدى"
        return f"💡 تلميح: {hint_text} (خصم 5 نقاط إذا نجحت)"

    # ---------------------------- كشف الرقم ---------------------------- #
    def reveal_answer(self):
        if self.current_number is None:
            return "لا توجد لعبة حالياً"
        answer = self.current_number
        self.current_number = None
        return f"🔍 الرقم الصحيح كان: {answer}"

    # ---------------------------- النقاط ---------------------------- #
    def get_score(self, user_id):
        return self.scores.get(user_id, 0)
