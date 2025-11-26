"""
Bot Mesh - Base Game
تم إنشاء هذا البوت بواسطة عبير الدوسري © 2025
"""

from linebot.v3.messaging import FlexMessage, FlexContainer, TextMessage
from typing import Dict, Any, Optional


class BaseGame:
    """
    القاعدة العامة لجميع الألعاب
    مطابقة لجميع الشروط المتفق عليها
    """

    def __init__(self, game_name="لعبة", questions_count=5,
                 supports_hint=True, supports_answer=True,
                 supports_timer=False):
        self.game_name = game_name
        self.questions_count = questions_count
        self.supports_hint = supports_hint
        self.supports_answer = supports_answer
        self.supports_timer = supports_timer

        self.current_question = 0
        self.current_answer = None
        self.previous_answer = None

        self.game_active = True
        self.first_correct_user = None

        self.scores = {}
        self.answered_this_round = False

    # =====================================================
    # تحكم اللعبة
    # =====================================================

    def start(self):
        self.current_question = 1
        self.scores.clear()
        self.first_correct_user = None
        self.answered_this_round = False
        self.previous_answer = None
        return self.get_question()

    def stop(self):
        return self.build_game_over_message()

    def is_expired(self, minutes: int) -> bool:
        return False

    # =====================================================
    # الإجابات
    # =====================================================

    def check_answer(self, user_answer: str, user_id: str, user_name: str):
        if not self.game_active or self.answered_this_round:
            return None

        if self.normalize(user_answer) == self.normalize(self.current_answer):
            self.answered_this_round = True
            self.first_correct_user = user_name
            self.scores[user_name] = self.scores.get(user_name, 0) + 1
            self.previous_answer = self.current_answer
            return self.next_question()

        return None

    # =====================================================
    # الأسئلة
    # =====================================================

    def get_question(self):
        raise NotImplementedError("يجب تنفيذ get_question داخل كل لعبة")

    def next_question(self):
        if self.current_question >= self.questions_count:
            return self.build_game_over_message()

        self.current_question += 1
        self.answered_this_round = False
        return self.get_question()

    # =====================================================
    # اللمح
    # =====================================================

    def get_hint(self):
        if not self.supports_hint or not self.current_answer:
            return TextMessage(text="لا يوجد لمح في هذه اللعبة")

        answer = str(self.current_answer)
        first_letter = answer[0]
        length = len(answer)

        return TextMessage(
            text=f"أول حرف: {first_letter}\nعدد الحروف: {length}"
        )

    # =====================================================
    # بناء واجهة السؤال
    # =====================================================

    def build_question_flex(self, question_text: str):
        buttons = []

        if self.supports_hint:
            buttons.append(self._button("لمح", "لمح"))

        if self.supports_answer:
            buttons.append(self._button("جاوب", "جاوب"))

        buttons.append(self._button("إيقاف", "إيقاف"))

        progress_bar = "".join(["▪️" if i < self.current_question else "▫️"
                                 for i in range(self.questions_count)])

        body_contents = [
            self._text(self.game_name, "xl", True),
            self._text(f"جولة {self.current_question} من {self.questions_count}", "sm"),
            self._text(progress_bar, "md"),
        ]

        if self.previous_answer:
            body_contents.append(
                self._text(f"جواب سابق: {self.previous_answer}", "sm")
            )

        body_contents.append(self._text(question_text, "lg", True))

        bubble = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": body_contents
            },
            "footer": {
                "type": "box",
                "layout": "horizontal",
                "spacing": "sm",
                "contents": buttons
            }
        }

        return FlexMessage(
            alt_text=self.game_name,
            contents=FlexContainer.from_dict(bubble)
        )

    # =====================================================
    # نهاية اللعبة
    # =====================================================

    def build_game_over_message(self):
        self.game_active = False

        if not self.scores:
            winner = "لا يوجد"
            points = 0
        else:
            winner, points = max(self.scores.items(), key=lambda x: x[1])

        bubble = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    self._text("انتهت اللعبة", "xl", True),
                    self._text(f"الفائز: {winner}", "lg"),
                    self._text(f"النقاط: {points}", "lg"),
                ]
            },
            "footer": {
                "type": "box",
                "layout": "horizontal",
                "spacing": "sm",
                "contents": [
                    self._button("إعادة", f"لعبة {self.game_name}"),
                    self._button("بداية", "بداية")
                ]
            }
        }

        return FlexMessage(
            alt_text="نتيجة اللعبة",
            contents=FlexContainer.from_dict(bubble)
        )

    # =====================================================
    # أدوات مساعدة
    # =====================================================

    def normalize(self, text):
        if not text:
            return ""
        text = text.strip().lower()
        text = text.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا")
        text = text.replace("ة", "ه").replace("ى", "ي")
        return text

    def _button(self, label, text):
        return {
            "type": "button",
            "action": {"type": "message", "label": label, "text": text}
        }

    def _text(self, text, size="md", bold=False):
        return {
            "type": "text",
            "text": text,
            "size": size,
            "weight": "bold" if bold else "regular",
            "wrap": True
        }
