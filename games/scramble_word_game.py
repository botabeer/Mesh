import random
from linebot.models import TextSendMessage
from utils.helpers import normalize_text

class ScrambleWordGame:
    def __init__(self):
        self.current_word = None
        self.words = [
            "سيارة", "مدرسة", "كمبيوتر", "هاتف", "كرة",
            "مستشفى", "نجمة", "حديقة", "سماء", "قمر",
            "طيارة", "كتاب", "وردة", "شجرة", "بحر"
        ]

    def start_game(self):
        self.current_word = random.choice(self.words)
        scrambled = ''.join(random.sample(self.current_word, len(self.current_word)))

        text = (
            "🔤 **لعبة ترتيب الحروف**\n\n"
            f"الكلمة المبعثرة: **{scrambled}**\n\n"
            "أعد ترتيبها للحصول على الكلمة الصحيحة!"
        )

        return TextSendMessage(text=text)

    def check_answer(self, answer, user_id=None, display_name=None):
        if not self.current_word:
            return None

        if normalize_text(answer) == normalize_text(self.current_word):
            new_q = self.start_game()
            msg = (
                f"✔️ ممتاز! الكلمة الصحيحة كانت: {self.current_word}\n\n"
                f"🎮 كلمة جديدة:\n{new_q.text}"
            )
            return {
                'points': 10,
                'won': True,
                'message': msg,
                'response': TextSendMessage(text=msg),
                'game_over': False
            }

        return None

    def reveal_answer(self):
        ans = self.current_word
        self.current_word = None
        return f"🔍 الإجابة الصحيحة: {ans}"
