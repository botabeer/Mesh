import random
from linebot.models import TextSendMessage
from utils.helpers import normalize_text

class GuessGame:
    def __init__(self):
        self.number = None
        self.scores = {}
        self.hint_used = False

    def start_game(self):
        self.number = random.randint(1, 50)
        self.hint_used = False
        text = "🎯 خمن الرقم بين 1 و 50!"
        return TextSendMessage(text=text)

    def check_answer(self, answer, user_id, display_name):
        if self.number is None:
            return None
        try:
            guess = int(answer)
        except ValueError:
            return None

        if guess == self.number:
            points = 10 if not self.hint_used else 5
            self.scores[user_id] = self.scores.get(user_id, 0) + points
            new_q = self.start_game()
            msg = (
                f"✔️ أحسنت يا {display_name}! الرقم الصحيح كان: {self.number}\n"
                f"+{points} نقاط (النقاط الحالية: {self.scores[user_id]})\n\n"
                f"{new_q.text}"
            )
            return {"points": points, "won": True, "message": msg, "response": new_q, "game_over": False}

        return None

    def get_hint(self):
        self.hint_used = True
        if self.number is None:
            return "لا توجد لعبة حالياً"
        hint = "أكبر من " if random.choice([True, False]) else "أصغر من "
        hint += str(self.number + random.randint(-5, 5))
        return f"💡 تلميح: الرقم {hint}"

    def reveal_answer(self):
        ans = self.number
        self.number = None
        return f"🔍 الرقم الصحيح هو: {ans}"

    def get_score(self, user_id):
        return self.scores.get(user_id, 0)
