import random
from linebot.models import TextSendMessage
from utils.helpers import normalize_text

class LettersWordsGame:
    def __init__(self):
        self.current_word = None
        self.scores = {}
        self.hint_used = False
        self.words = ["تفاحة", "موز", "برتقال", "كرز", "عنب", "ليمون", "خوخ"]

    def start_game(self):
        self.current_word = random.choice(self.words)
        self.hint_used = False
        text = f"🔡 حدد الحروف الصحيحة:\nالكلمة: {self.current_word[0]} _ _ _ _"
        return TextSendMessage(text=text)

    def check_answer(self, answer, user_id, display_name):
        if not self.current_word:
            return None
        if normalize_text(answer) == normalize_text(self.current_word):
            points = 10 if not self.hint_used else 5
            self.scores[user_id] = self.scores.get(user_id, 0) + points
            new_game = self.start_game()
            msg = (f"✔️ صحيح يا {display_name}! الكلمة: {self.current_word}\n"
                   f"+{points} نقاط (النقاط الحالية: {self.scores[user_id]})\n{new_game.text}")
            return {"points": points, "won": True, "message": msg, "response": new_game, "game_over": False}
        return None

    def get_hint(self):
        if not self.current_word:
            return "لا توجد كلمة حالياً"
        self.hint_used = True
        return f"💡 التلميح: أول حرفين من الكلمة: {self.current_word[:2]}"

    def reveal_answer(self):
        ans = self.current_word
        self.current_word = None
        return f"🔍 الإجابة الصحيحة: {ans}"

    def get_score(self, user_id):
        return self.scores.get(user_id, 0)
