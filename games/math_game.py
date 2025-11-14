import random
from linebot.models import TextSendMessage

class MathGame:
    def __init__(self):
        self.current_answer = None
        self.scores = {}

    def start_game(self):
        a = random.randint(1, 20)
        b = random.randint(1, 20)
        self.current_answer = a + b
        return TextSendMessage(text=f"➕ احسب: {a} + {b}")

    def check_answer(self, answer, user_id, display_name):
        if self.current_answer is None:
            return None
        try:
            num = int(answer)
        except:
            return TextSendMessage(text="⚠️ يجب إدخال رقم صحيح")
        if num == self.current_answer:
            points = 10
            self.scores[user_id] = self.scores.get(user_id, 0) + points
            self.current_answer = None
            msg = f"✔️ صحيح يا {display_name}!\n+{points} نقاط"
            return {"points": points, "won": True, "message": msg, "game_over": False}
        return TextSendMessage(text="❌ خطأ حاول مرة أخرى")

    def get_score(self, user_id):
        return self.scores.get(user_id, 0)
