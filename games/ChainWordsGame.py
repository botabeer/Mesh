import random
from linebot.models import TextSendMessage
from utils.helpers import normalize_text

class ChainWordsGame:
    def __init__(self):
        self.last_letter = None
        self.used_words = set()
        self.scores = {}

    def start_game(self):
        self.last_letter = random.choice("ابتثجحخدذرزسشصضطظعغفقكلمنهوي")
        self.used_words.clear()
        return TextSendMessage(text=f"🔗 ابدأ سلسلة كلمات بحرف: {self.last_letter}")

    def check_answer(self, word, user_id, display_name):
        word_norm = normalize_text(word)
        if word_norm in self.used_words:
            return None
        if self.last_letter and not word_norm.startswith(self.last_letter):
            return None
        self.used_words.add(word_norm)
        self.last_letter = word_norm[-1]
        points = 10
        self.scores[user_id] = self.scores.get(user_id, 0) + points
        return {"points": points, "won": True, "message": f"✔️ صحيح! الكلمة: {word}", "next_letter": self.last_letter}

    def get_score(self, user_id):
        return self.scores.get(user_id, 0)
