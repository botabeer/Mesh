import random
from linebot.models import TextSendMessage

class GuessGame:
    def __init__(self):
        self.number = None
        self.scores = {}

    def start_game(self):
        self.number = random.randint(1, 50)
        return TextSendMessage(text="🎯 خمن الرقم بين 1 و 50")

    def check_answer(self, answer, user_id, display_name):
        if not self.number:
            return None
        try:
            num = int(answer)
        except:
            return TextSendMessage(text="⚠️ يجب أن يكون الرقم صحيحاً")

        if num == self.number:
            points = 10
            self.scores[user_id] = self.scores.get(user_id, 0) + points
            msg = f"✔️ صحيح يا {display_name}! الرقم كان {self.number}\n+{points} نقاط"
            self.number = None
            return {"points": points, "won": True, "message": msg, "game_over": False}
        elif num < self.number:
            return TextSendMessage(text="⬆️ أكبر من هذا الرقم")
        else:
            return TextSendMessage(text="⬇️ أصغر من هذا الرقم")

    def get_score(self, user_id):
        return self.scores.get(user_id, 0)
