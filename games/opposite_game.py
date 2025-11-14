import random
from linebot.models import TextSendMessage, QuickReply, QuickReplyButton, MessageAction
from utils.helpers import normalize_text

class OppositeGameAdvanced:
    def __init__(self, line_bot_api):
        self.line_bot_api = line_bot_api
        self.current_word = None
        self.current_opposite = None
        self.hint_used = False
        self.scores = {}  # حفظ النقاط لكل لاعب

        # قاموس الأضداد
        self.opposites = {
            "ساخن": "بارد",
            "كبير": "صغير",
            "طويل": "قصير",
            "سريع": "بطيء",
            "قوي": "ضعيف",
            "غني": "فقير",
            "جميل": "قبيح",
            "نظيف": "قذر",
            "سهل": "صعب",
            "قريب": "بعيد",
            "عالي": "منخفض",
            "واسع": "ضيق",
            "جديد": "قديم",
            "مبتسم": "عابس",
            "نشيط": "كسول",
            "شجاع": "جبان",
            "أبيض": "أسود",
            "نهار": "ليل",
            "صيف": "شتاء",
            "بداية": "نهاية"
        }

    # ---------------- بدء اللعبة ----------------
    def start_game(self):
        self.current_word = random.choice(list(self.opposites.keys()))
        self.current_opposite = self.opposites[self.current_word]
        self.hint_used = False

        quick_reply = QuickReply(items=[
            QuickReplyButton(action=MessageAction(label="تلميح", text="تلميح")),
            QuickReplyButton(action=MessageAction(label="كشف الإجابة", text="كشف الإجابة")),
            QuickReplyButton(action=MessageAction(label="سؤال جديد", text="سؤال جديد"))
        ])

        text = f"↔️ ما هو عكس:\n\n{self.current_word}\n\n━━━━━━━━━━━━━━\nاكتب الكلمة المعاكسة"
        return TextSendMessage(text=text, quick_reply=quick_reply)

    # ---------------- فحص الإجابة ----------------
    def check_answer(self, answer, user_id, display_name):
        if not self.current_opposite:
            return None

        normalized_answer = normalize_text(answer)
        normalized_opposite = normalize_text(self.current_opposite)

        if normalized_answer == normalized_opposite:
            points = 10
            if self.hint_used:
                points = 5

            # تحديث نقاط اللاعب
            self.scores[user_id] = self.scores.get(user_id, 0) + points

            new_question = self.start_game()
            message = f"✓ إجابة صحيحة يا {display_name}\n\nعكس {self.current_word} هو {self.current_opposite}\n+{points} نقطة\n\nالنقاط الحالية: {self.scores[user_id]}\n\n{new_question.text}"

            return {
                'points': points,
                'won': True,
                'message': message,
                'response': new_question,
                'game_over': False
            }

        return None

    # ---------------- التلميح ----------------
    def get_hint(self):
        if not self.current_opposite:
            return "لا يوجد سؤال حالي"

        self.hint_used = True
        first_letter = self.current_opposite[0]
        letter_count = len(self.current_opposite)

        return f"💡 التلميح\n\nأول حرف: {first_letter}\nعدد الحروف: {letter_count}\n\n⚠️ سيتم خصم 5 نقاط"

    # ---------------- كشف الإجابة ----------------
    def reveal_answer(self):
        if not self.current_opposite:
            return "لا يوجد سؤال حالي"

        answer = f"عكس {self.current_word} هو {self.current_opposite}"
        self.current_word = None
        self.current_opposite = None

        return f"الإجابة الصحيحة:\n{answer}"

    # ---------------- الحصول على نقاط اللاعب ----------------
    def get_score(self, user_id):
        return self.scores.get(user_id, 0)
