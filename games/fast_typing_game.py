import random
from linebot.models import TextSendMessage

class FastTypingGame:
    def __init__(self):
        self.phrases = ["الذكاء الاصطناعي ممتع", "لغة البرمجة بايثون", "مرحبا بك في اللعبة", "البرمجة ممتعة"]
        self.current_phrase = None
        self.scores = {}
        self.hint_used = False

    def start_game(self):
        self.current_phrase = random.choice(self.phrases)
        self.hint_used = False
        return TextSendMessage(text=f"⌨️ أعد كتابة الجملة التالية بسرعة:\n{self.current_phrase}")

    def check_answer(self, answer, user_id, display_name):
        if not self.current_phrase:
            return None
        if answer.strip() == self.current_phrase:
            points = 10 if not self.hint_used else 5
            self.scores[user_id] = self.scores.get(user_id, 0) + points
            new_game = self.start_game()
            msg = (f"✔️ رائع يا {display_name}! الجملة صحيحة.\n"
                   f"+{points} نقاط (النقاط الحالية: {self.scores[user_id]})\n{new_game.text}")
            return {"points": points, "won": True, "message": msg, "response": new_game, "game_over": False}
        return None

    def get_hint(self):
        if not self.current_phrase:
            return "لا توجد جملة حالياً"
        self.hint_used = True
        return f"💡 التلميح: أول ثلاث كلمات: {' '.join(self.current_phrase.split()[:3])}"

    def reveal_answer(self):
        ans = self.current_phrase
        self.current_phrase = None
        return f"🔍 الإجابة الصحيحة: {ans}"

    def get_score(self, user_id):
        return self.scores.get(user_id, 0)
