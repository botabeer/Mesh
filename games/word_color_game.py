import random
from linebot.models import TextSendMessage

class WordColorGame:
    def __init__(self):
        self.words = ["أحمر", "أزرق", "أخضر", "أصفر", "وردي", "برتقالي"]
        self.current_word = None
        self.current_color = None
        self.scores = {}
        self.hint_used = False

    def start_game(self):
        self.current_word = random.choice(self.words)
        self.current_color = random.choice(self.words)
        self.hint_used = False
        text = f"🎨 كلمة اللون: **{self.current_word}** مكتوبة بلون **{self.current_color}**، ما هو اللون الصحيح؟"
        return TextSendMessage(text=text)

    def check_answer(self, answer, user_id, display_name):
        if not self.current_color:
            return None
        if answer.strip() == self.current_color:
            points = 10 if not self.hint_used else 5
            self.scores[user_id] = self.scores.get(user_id, 0) + points
            new_q = self.start_game()
            msg = (
                f"✔️ إجابة صحيحة يا {display_name}!\n"
                f"اللون الصحيح: {self.current_color}\n"
                f"+{points} نقاط (النقاط الحالية: {self.scores[user_id]})\n\n"
                f"{new_q.text}"
            )
            return {"points": points, "won": True, "message": msg, "response": new_q, "game_over": False}
        return None

    def get_hint(self):
        self.hint_used = True
        if not self.current_color:
            return "لا توجد لعبة حالياً"
        return f"💡 التلميح: أول حرف من اللون هو '{self.current_color[0]}'"

    def reveal_answer(self):
        ans = self.current_color
        self.current_color = None
        self.current_word = None
        return f"🔍 الإجابة الصحيحة: {ans}"

    def get_score(self, user_id):
        return self.scores.get(user_id, 0)
