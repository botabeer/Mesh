import random
from linebot.models import TextSendMessage, QuickReply, QuickReplyButton, MessageAction
from utils.helpers import normalize_text

class ScrambleWordGame:
    def __init__(self):
        self.current_word = None
        self.words = ["سيارة", "مدرسة", "كمبيوتر", "هاتف", "كرة",
                      "مستشفى", "نجمة", "حديقة", "سماء", "قمر",
                      "طيارة", "كتاب", "وردة", "شجرة", "بحر"]
        self.scores = {}
        self.hint_used = False

    def start_game(self):
        self.current_word = random.choice(self.words)
        scrambled = ''.join(random.sample(self.current_word, len(self.current_word)))
        self.hint_used = False
        quick_reply = QuickReply(items=[
            QuickReplyButton(action=MessageAction(label="تلميح", text="تلميح")),
            QuickReplyButton(action=MessageAction(label="كشف الإجابة", text="كشف الإجابة")),
            QuickReplyButton(action=MessageAction(label="كلمة جديدة", text="كلمة جديدة"))
        ])
        text = f"🔤 لعبة ترتيب الحروف:\nالكلمة المبعثرة: **{scrambled}**\nأعد ترتيبها للحصول على الكلمة الصحيحة!"
        return TextSendMessage(text=text, quick_reply=quick_reply)

    def check_answer(self, answer, user_id, display_name):
        if not self.current_word:
            return None
        if normalize_text(answer) == normalize_text(self.current_word):
            points = 10 if not self.hint_used else 5
            self.scores[user_id] = self.scores.get(user_id, 0) + points
            new_game = self.start_game()
            msg = (f"✔️ ممتاز يا {display_name}! الكلمة الصحيحة كانت: {self.current_word}\n"
                   f"+{points} نقاط (النقاط الحالية: {self.scores[user_id]})\n{new_game.text}")
            return {"points": points, "won": True, "message": msg, "response": new_game, "game_over": False}
        return None

    def get_hint(self):
        if not self.current_word:
            return "لا توجد كلمة حالياً"
        self.hint_used = True
        return f"💡 التلميح: أول حرف من الكلمة هو '{self.current_word[0]}'"

    def reveal_answer(self):
        ans = self.current_word
        self.current_word = None
        return f"🔍 الإجابة الصحيحة: {ans}"

    def get_score(self, user_id):
        return self.scores.get(user_id, 0)
