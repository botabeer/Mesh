from abc import ABC, abstractmethod
from linebot.v3.messaging import (
    FlexMessage,
    FlexContainer,
    QuickReply,
    QuickReplyItem,
    MessageAction
)
from config import Config


class BaseGame(ABC):
    """القاعدة الموحدة لجميع الالعاب"""

    QUESTIONS_PER_GAME = 5

    def __init__(self, db, theme="light"):
        self.db = db
        self.theme = theme
        self.total_q = self.QUESTIONS_PER_GAME
        self.current_q = 0
        self.score = 0
        self.user_id = None
        self.current_answer = None
        self.game_name = "لعبة"
        self.supports_hint = True
        self.supports_reveal = True

    # ================== Helpers ==================

    def _c(self):
        return Config.get_theme(self.theme)

    def _qr(self):
        return QuickReply(items=[
            QuickReplyItem(action=MessageAction(label="القائمة", text="بداية")),
            QuickReplyItem(action=MessageAction(label="العاب", text="العاب")),
            QuickReplyItem(action=MessageAction(label="نقاطي", text="نقاطي")),
            QuickReplyItem(action=MessageAction(label="الصدارة", text="الصدارة")),
            QuickReplyItem(action=MessageAction(label="ايقاف", text="ايقاف")),
            QuickReplyItem(action=MessageAction(label="مساعدة", text="مساعدة"))
        ])

    # Alias لتفادي كسر الألعاب القديمة
    def _quick_reply(self):
        return self._qr()

    def _safe_text(self, text: str, fallback: str = " "):
        """منع ارسال text فارغ لـ LINE"""
        if isinstance(text, str) and text.strip():
            return text
        return fallback

    # ================== Abstract ==================

    @abstractmethod
    def get_question(self):
        pass

    @abstractmethod
    def check_answer(self, answer: str) -> bool:
        pass

    # ================== Game Flow ==================

    def start(self, user_id: str):
        self.user_id = user_id
        self.current_q = 0
        self.score = 0
        return self.get_question()

    def restore(self, progress: dict):
        self.score = progress.get("score", 0)
        self.current_q = progress.get("current_q", 0)

    def on_stop(self, user_id: str):
        self.db.save_game_progress(user_id, {
            "game": self.game_name,
            "score": self.score,
            "current_q": self.current_q
        })

    def check(self, answer: str, user_id: str):
        if user_id != self.user_id:
            return None

        cmd = Config.normalize(answer)

        if cmd in {"بدايه", "بداية", "مساعده", "مساعدة", "العاب"}:
            return None

        if cmd in ("ايقاف", "ايقاف اللعبة"):
            return {"response": self._pause_message(), "game_over": True}

        if self.supports_hint and cmd == "لمح":
            hint = self._get_hint()
            if hint:
                return {"response": self._hint_message(hint), "game_over": False}

        if self.supports_reveal and cmd == "جاوب":
            return {"response": self._reveal_message(), "game_over": False, "skip": True}

        try:
            correct = self.check_answer(answer)
        except Exception:
            return None

        if not correct:
            return None

        self.score += 1
        if self.db and self.db.get_user(user_id):
            self.db.add_points(user_id, 1)

        self.current_q += 1

        if self.current_q >= self.total_q:
            won = self.score == self.total_q
            if self.db and self.db.get_user(user_id):
                self.db.finish_game(user_id, won)

            return {
                "response": self._game_over_message(),
                "game_over": True,
                "won": won
            }

        return {"response": self.get_question(), "game_over": False}

    # ================== Messages ==================

    def _get_hint(self):
        ans = self.current_answer[0] if isinstance(self.current_answer, list) else str(self.current_answer)
        if len(ans) > 2:
            return f"يبدأ بـ {ans[0]}\nعدد الحروف {len(ans)}"
        return f"{ans[0]}_"

    def _hint_message(self, hint: str):
        c = self._c()
        bubble = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "تلميح", "weight": "bold", "align": "center"},
                    {"type": "separator"},
                    {"type": "text", "text": self._safe_text(hint), "wrap": True, "align": "center"}
                ],
                "backgroundColor": c["bg"]
            }
        }
        return FlexMessage(
            alt_text="تلميح",
            contents=FlexContainer.from_dict(bubble),
            quickReply=self._qr()
        )

    def _reveal_message(self):
        c = self._c()
        ans = " أو ".join(self.current_answer) if isinstance(self.current_answer, list) else str(self.current_answer)

        self.current_q += 1
        if self.current_q >= self.total_q:
            return self._game_over_message()

        bubble = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "الإجابة", "weight": "bold", "align": "center"},
                    {"type": "separator"},
                    {"type": "text", "text": self._safe_text(ans), "wrap": True, "align": "center"}
                ],
                "backgroundColor": c["bg"]
            }
        }

        msg = FlexMessage(
            alt_text="الإجابة",
            contents=FlexContainer.from_dict(bubble),
            quickReply=self._qr()
        )

        return msg

    def _pause_message(self):
        c = self._c()
        bubble = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "تم حفظ تقدمك", "weight": "bold", "align": "center"},
                    {"type": "separator"},
                    {"type": "text", "text": f"النقاط: {self.score}", "align": "center"},
                    {"type": "text", "text": f"{self.current_q}/{self.total_q}", "align": "center"}
                ],
                "backgroundColor": c["bg"]
            }
        }
        return FlexMessage(
            alt_text="تم الإيقاف",
            contents=FlexContainer.from_dict(bubble),
            quickReply=self._qr()
        )

    def _game_over_message(self):
        c = self._c()
        won = self.score == self.total_q

        bubble = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "انتهت اللعبة", "weight": "bold", "align": "center"},
                    {"type": "separator"},
                    {"type": "text",
                     "text": "فوز كامل " if won else f"{self.score}/{self.total_q}",
                     "align": "center"},
                ],
                "backgroundColor": c["bg"]
            }
        }

        return FlexMessage(
            alt_text="النتيجة",
            contents=FlexContainer.from_dict(bubble),
            quickReply=self._qr()
        )

    # ================== Question Builder ==================

    def build_question_flex(self, question_text: str, hint: str = None):
        c = self._c()

        contents = [
            {"type": "text", "text": self._safe_text(self.game_name), "weight": "bold", "align": "center"},
            {"type": "text", "text": f"{self.current_q + 1}/{self.total_q}", "size": "xs", "align": "center"},
            {"type": "separator"},
            {"type": "text", "text": self._safe_text(question_text), "wrap": True, "align": "center"}
        ]

        if hint:
            contents.append({
                "type": "text",
                "text": self._safe_text(hint),
                "size": "xs",
                "align": "center"
            })

        if self.supports_hint and self.supports_reveal:
            contents.append({
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {"type": "button", "action": {"type": "message", "label": "لمح", "text": "لمح"}},
                    {"type": "button", "action": {"type": "message", "label": "جاوب", "text": "جاوب"}}
                ]
            })

        bubble = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": contents,
                "backgroundColor": c["bg"]
            }
        }

        return FlexMessage(
            alt_text=self.game_name,
            contents=FlexContainer.from_dict(bubble),
            quickReply=self._qr()
        )
