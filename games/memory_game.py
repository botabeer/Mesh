import random
from linebot.models import TextSendMessage

class MemoryGame:
    def __init__(self):
        self.sequence = []
        self.scores = {}

    def start_game(self):
        self.sequence = [random.randint(0, 9) for _ in range(5)]
        return TextSendMessage(text=f"🧠 تذكر الأرقام التالية: {''.join(map(str, self.sequence))}")

    def check_answer(self, answer, user_id, display_name):
        if ''.join(map(str, self.sequence)) == answer.strip():
            points = 10
            self.scores[user_id] = self.scores.get(user_id, 0) + points
            self.sequence = []
            msg = f"✔️ صحيح يا {display_name}!\n+{points} نقاط"
            return {"points": points, "won": True, "message": msg, "game_over": False}
        return TextSendMessage(text="❌ خطأ حاول مرة أخرى")

    def get_score(self, user_id):
        return self.scores.get(user_id, 0)
