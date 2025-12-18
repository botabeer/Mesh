from abc import ABC, abstractmethod
import logging
from linebot.v3.messaging import (
    FlexMessage,
    FlexContainer,
    QuickReply,
    QuickReplyItem,
    MessageAction
)
from config import Config

logger = logging.getLogger(__name__)


class BaseGame(ABC):
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
        self.game_icon = "🎮"

        self.supports_hint = True
        self.supports_reveal = True

    def _c(self):
        return Config.get_theme(self.theme)

    def _qr(self):
        items = ["بداية", "العاب", "نقاطي", "الصدارة", "ايقاف"]
        return QuickReply(
            items=[QuickReplyItem(action=MessageAction(label=i, text=i)) for i in items]
        )

    def _safe_text(self, text, fallback=" "):
        if isinstance(text, str) and text.strip():
            return text
        return fallback

    def _separator(self, margin="md"):
        return {
            "type": "separator",
            "margin": margin
        }

    def _glass_box(self, contents, padding="16px", margin="none"):
        c = self._c()
        bg_color = c["card_secondary"] if self.theme == "light" else "#1A202C"
        return {
            "type": "box",
            "layout": "vertical",
            "contents": contents,
            "backgroundColor": bg_color,
            "cornerRadius": "16px",
            "paddingAll": padding,
            "spacing": "sm",
            "margin": margin
        }

    @abstractmethod
    def get_question(self):
        pass

    @abstractmethod
    def check_answer(self, answer):
        pass

    def start(self, user_id):
        self.user_id = user_id
        self.current_q = 0
        self.score = 0
        return self.get_question()

    def restore(self, user_id, progress):
        self.user_id = user_id
        self.score = progress.get("score", 0)
        self.current_q = progress.get("current_q", 0)

    def on_stop(self, user_id):
        if not self.db:
            return
        self.db.save_game_progress(user_id, {
            "game": self.game_name,
            "score": self.score,
            "current_q": self.current_q
        })

    def check(self, answer, user_id):
        if user_id != self.user_id:
            return None

        cmd = Config.normalize(answer)

        if cmd in {"بدايه", "بداية", "مساعده", "مساعدة", "العاب"}:
            return None

        if cmd in {"ايقاف", "ايقاف اللعبة"}:
            return {
                "response": self._pause_message(),
                "game_over": True
            }

        if self.supports_hint and cmd == "لمح":
            hint = self._get_hint()
            return {
                "response": self._hint_message(hint),
                "game_over": False
            }

        if self.supports_reveal and cmd == "جاوب":
            return {
                "response": self._reveal_message(),
                "game_over": False,
                "skip": True
            }

        try:
            correct = self.check_answer(answer)
        except Exception:
            logger.exception("check_answer failed")
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

        return {
            "response": self.get_question(),
            "game_over": False
        }

    def _get_hint(self):
        if not self.current_answer:
            return "لا يوجد تلميح"

        ans = (
            self.current_answer[0]
            if isinstance(self.current_answer, list)
            else str(self.current_answer)
        )

        if len(ans) > 2:
            return f"يبدأ بـ {ans[0]}\nعدد الحروف {len(ans)}"

        return f"{ans[0]}_"

    def _hint_message(self, hint):
        c = self._c()

        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": c["card"],
                "paddingAll": "24px",
                "contents": [
                    {
                        "type": "text",
                        "text": "تلميح",
                        "weight": "bold",
                        "size": "lg",
                        "color": c["text"],
                        "align": "center"
                    },
                    self._separator(),
                    self._glass_box([
                        {
                            "type": "text",
                            "text": self._safe_text(hint),
                            "wrap": True,
                            "align": "center",
                            "weight": "bold",
                            "color": c["text"]
                        }
                    ], "20px", "lg")
                ]
            }
        }

        return FlexMessage(
            alt_text="تلميح",
            contents=FlexContainer.from_dict(bubble),
            quickReply=self._qr()
        )

    def _reveal_message(self):
        c = self._c()

        ans = (
            " أو ".join(self.current_answer)
            if isinstance(self.current_answer, list)
            else str(self.current_answer)
        )

        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": c["card"],
                "paddingAll": "24px",
                "contents": [
                    {
                        "type": "text",
                        "text": "الإجابة الصحيحة",
                        "weight": "bold",
                        "size": "lg",
                        "color": c["text"],
                        "align": "center"
                    },
                    self._separator(),
                    self._glass_box([
                        {
                            "type": "text",
                            "text": self._safe_text(ans),
                            "wrap": True,
                            "align": "center",
                            "weight": "bold",
                            "color": c["primary"]
                        }
                    ], "20px", "lg")
                ]
            }
        }

        return FlexMessage(
            alt_text="الإجابة",
            contents=FlexContainer.from_dict(bubble),
            quickReply=self._qr()
        )

    def _pause_message(self):
        c = self._c()

        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": c["card"],
                "paddingAll": "24px",
                "contents": [
                    {
                        "type": "text",
                        "text": "تم حفظ تقدمك",
                        "size": "xl",
                        "weight": "bold",
                        "color": c["text"],
                        "align": "center"
                    },
                    self._separator("lg"),
                    {
                        "type": "text",
                        "text": f"{self.score}/{self.total_q}",
                        "size": "xl",
                        "weight": "bold",
                        "align": "center",
                        "color": c["success"]
                    }
                ]
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
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": c["card"],
                "paddingAll": "24px",
                "contents": [
                    {
                        "type": "text",
                        "text": "فوز رائع" if won else "انتهت اللعبة",
                        "size": "xxl",
                        "weight": "bold",
                        "color": c["success"] if won else c["text"],
                        "align": "center"
                    },
                    self._separator("lg"),
                    {
                        "type": "text",
                        "text": f"{self.score}/{self.total_q}",
                        "size": "xxl",
                        "weight": "bold",
                        "align": "center",
                        "color": c["primary"]
                    }
                ]
            }
        }

        return FlexMessage(
            alt_text="النتيجة",
            contents=FlexContainer.from_dict(bubble),
            quickReply=self._qr()
        )
