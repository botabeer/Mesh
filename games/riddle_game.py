‏import random
from linebot.models import TextSendMessage, QuickReply, QuickReplyButton, MessageAction
from utils.helpers import normalize_text

class RiddleGameAdvanced:
    def __init__(self, line_bot_api):
        self.line_bot_api = line_bot_api
        self.current_riddle = None
        self.current_answer = None
        self.hint_used = False
        self.scores = {}

        self.riddles = [
            {"q": "له أوراق وما هو بنبات، له جلد وما هو بحيوان؟", "a": "الكتاب"},
            {"q": "ما هو الشيء الذي نرميه بعد العصر؟", "a": "البرتقال"},
            {"q": "إذا دخل الماء لم يبتل؟", "a": "الضوء"},
            {"q": "له رقبة ولا رأس له؟", "a": "الزجاجة"},
            {"q": "أخت خالك وليست خالتك؟", "a": "أمي"},
        ]

    # ---------------- بدء اللعبة ----------------
    def start_game(self):
        self.current_riddle = random.choice(self.riddles)
        self.current_answer = self.current_riddle['a']
        self.hint_used = False

        quick_reply = QuickReply(items=[
            QuickReplyButton(action=MessageAction(label="تلميح", text="تلميح")),
            QuickReplyButton(action=MessageAction(label="كشف الإجابة", text="كشف الإجابة")),
            QuickReplyButton(action=MessageAction(label="سؤال جديد", text="سؤال جديد"))
        ])

        text = f"🤔 لغز\n\n{self.current_riddle['q']}\n\n━━━━━━━━━━━━━━\nما الحل؟"
        return TextSendMessage(text=text, quick_reply=quick_reply)

    # ---------------- فحص الإجابة ----------------
    def check_answer(self, answer, user_id, display_name):
        if not self.current_answer:
            return None

        if normalize_text(answer) in normalize_text(self.current_answer):
            points = 10
            if self.hint_used:
                points = 5

            # تحديث النقاط لكل لاعب
            self.scores[user_id] = self.scores.get(user_id, 0) + points

            new_riddle = self.start_game()
            msg = f"✓ صحيح يا {display_name}!\n\nالحل: {self.current_answer}\n+{points} نقطة\n\nالنقاط الحالية: {self.scores[user_id]}\n\n{new_riddle.text}"

            return {
                'points': points,
                'won': True,
                'message': msg,
                'response': new_riddle,
                'game_over': False
            }

        return None

    # ---------------- التلميح ----------------
    def get_hint(self):
        if not self.current_answer:
            return "لا يوجد لغز حالي"
        self.hint_used = True
        first_letter = self.current_answer[0]
        letter_count = len(self.current_answer)
        return f"💡 التلميح\n\nأول حرف: {first_letter}\nعدد الحروف: {letter_count}\n\n⚠️ سيتم خصم 5 نقاط"

    # ---------------- كشف الإجابة ----------------
    def reveal_answer(self):
        if not self.current_answer:
            return "لا يوجد لغز حالي"
        answer = self.current_answer
        self.current_riddle = None
        self.current_answer = None
        return f"الحل: {answer}"

    # ---------------- الحصول على نقاط اللاعب ----------------
    def get_score(self, user_id):
        return self.scores.get(user_id, 0)
