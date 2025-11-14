import random
from linebot.models import TextSendMessage
from utils.helpers import normalize_text

class HumanAnimalPlantGame:
    def __init__(self):
        self.categories = ["إنسان", "حيوان", "نبات"]
        self.current_letter = None
        self.scores = {}
        self.hint_used = False

    def start_game(self):
        self.current_letter = random.choice("ابتثجحخدذرزسشصضطظعغفقكلمنهوي")
        self.hint_used = False
        text = f"📝 لعبة الإنسان، الحيوان، النبات\nابدأ بكلمة تبدأ بالحرف: **{self.current_letter}**"
        return TextSendMessage(text=text)

    def check_answer(self, answer, category, user_id, display_name):
        if not self.current_letter:
            return None
        if normalize_text(answer).startswith(self.current_letter):
            points = 10 if not self.hint_used else 5
            self.scores[user_id] = self.scores.get(user_id, 0) + points
            return {"points": points, "won": True, "message": f"✔️ صحيح يا {display_name}!\n+{points} نقاط", "game_over": False}
        return None

    def get_hint(self):
        self.hint_used = True
        return f"💡 التلميح: الحرف هو '{self.current_letter}'"

    def reveal_answer(self):
        letter = self.current_letter
        self.current_letter = None
        return f"🔍 الحرف كان: {letter}"

    def get_score(self, user_id):
        return self.scores.get(user_id, 0)
