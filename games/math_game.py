import random
from linebot.models import TextSendMessage
from utils.helpers import normalize_text

class MathGame:
    def __init__(self):
        self.current_question = None
        self.answer = None
        self.scores = {}
        self.hint_used = False

    def start_game(self):
        a = random.randint(1, 20)
        b = random.randint(1, 20)
        self.answer = a + b
        self.hint_used = False
        text = f"➕ احسب: {a} + {b} = ?"
        return TextSendMessage(text=text)

    def check_answer(self, answer, user_id, display_name):
        if not self.answer:
            return None
        try:
            guess = int(answer)
        except ValueError:
            return None
        if guess == self.answer:
            points = 10 if not self.hint_used else 5
            self.scores[user_id] = self.scores.get(user_id, 0) + points
            new_q = self.start_game()
            msg = (
                f"✔️ أحسنت يا {display_name}! الإجابة الصحيحة: {self.answer}\n"
                f"+{points} نقاط (النقاط الحالية: {self.scores[user_id]})\n\n"
                f"{new_q.text}"
            )
            return {"points": points, "won": True, "message": msg, "response": new_q, "game_over": False}
        return None

    def get_hint(self):
        self.hint_used = True
        return f"💡 تلميح: الإجابة قريبة من {self.answer - 1} أو {self.answer + 1}"

    def reveal_answer(self):
        ans = self.answer
        self.answer = None
        return f"🔍 الإجابة الصحيحة: {ans}"

    def get_score(self, user_id):
        return self.scores.get(user_id, 0)
