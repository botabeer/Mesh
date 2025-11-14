import random
from linebot.models import TextSendMessage
from utils.helpers import normalize_text

class RiddleGame:
    def __init__(self):
        self.current_riddle = None
        self.current_answer = None
        self.scores = {}
        self.riddles = [
            {"q": "ما الشيء الذي كلما أخذت منه يكبر؟", "a": "الحفرة"},
            {"q": "ما هو الشيء الذي له أسنان ولا يعض؟", "a": "المشط"},
            {"q": "ما هو الشيء الذي يكتب ولا يقرأ؟", "a": "القلم"}
        ]

    def start_game(self):
        r = random.choice(self.riddles)
        self.current_riddle = r["q"]
        self.current_answer = r["a"]
        return TextSendMessage(text=f"🕵️ لغز:\n{self.current_riddle}")

    def check_answer(self, answer, user_id, display_name):
        if not self.current_answer:
            return None
        if normalize_text(answer) == normalize_text(self.current_answer):
            points = 10
            self.scores[user_id] = self.scores.get(user_id, 0) + points
            self.current_riddle = None
            self.current_answer = None
            return {"points": points, "won": True, "message": f"✔️ صحيح يا {display_name}!\n+{points} نقاط", "game_over": False}
        return None

    def reveal_answer(self):
        ans = self.current_answer
        self.current_riddle = None
        self.current_answer = None
        return f"🔍 الإجابة الصحيحة: {ans}"

    def get_score(self, user_id):
        return self.scores.get(user_id, 0)
