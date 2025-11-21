import random
from linebot.models import TextSendMessage

class OppositeGame:
    def __init__(self):
        self.current_word = None
        self.scores = {}
        self.words = {"كبير": "صغير", "سريع": "بطيء", "سعيد": "حزين"}

    def start_game(self):
        self.current_word, self.current_opposite = random.choice(list(self.words.items()))
        return TextSendMessage(text=f"🔄 اعطِ عكس الكلمة: {self.current_word}")

    def check_answer(self, answer, user_id, display_name):
        if answer == self.current_opposite:
            points = 10
            self.scores[user_id] = self.scores.get(user_id, 0) + points
            return {"points": points, "won": True, "message": f"✔️ صحيح يا {display_name}!\n+{points} نقاط", "game_over": False}
        return TextSendMessage(text="❌ خطأ حاول مرة أخرى")

    def get_score(self, user_id):
        return self.scores.get(user_id, 0)
