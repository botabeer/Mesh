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
    QUESTIONS_PER_GAME = 5

    def __init__(self, db, theme="light"):
        self.db = db
        self.theme = theme
        self.total_q = self.QUESTIONS_PER_GAME
        self.current_q = 0
        self.score = 0
        self.user_id = None
        self.current_answer = None

    # ===============================
    # Helpers
    # ===============================
    def _c(self):
        return Config.get_theme(self.theme)

    def _quick_reply(self):
        return QuickReply(items=[
            QuickReplyItem(
                action=MessageAction(label="انسحب", text="انسحب")
            ),
            QuickReplyItem(
                action=MessageAction(label="البداية", text="بداية")
            )
        ])

    # ===============================
    # Abstract
    # ===============================
    @abstractmethod
    def get_question(self):
        pass

    @abstractmethod
    def check_answer(self, answer: str) -> bool:
        pass

    # ===============================
    # Lifecycle
    # ===============================
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

    # ===============================
    # Core Logic
    # ===============================
    def check(self, answer: str, user_id: str):
        # أمان إضافي
        if user_id != self.user_id:
            return None

        if not self.db.get_user(user_id):
            return None

        cmd = Config.normalize(answer)

        # تجاهل الأوامر العامة
        if cmd in Config.MAIN_COMMANDS:
            return None

        # انسحاب
        if cmd == "انسحب":
            return {
                "response": self._pause_message(),
                "game_over": True
            }

        # تحقق من الإجابة
        try:
            correct = self.check_answer(answer)
        except Exception:
            return None

        if not correct:
            return None

        self.score += 1
        self.current_q += 1

        # نهاية اللعبة
        if self.current_q >= self.total_q:
            return {
                "response": self._game_over_message(),
                "game_over": True,
                "won": self.score == self.total_q
            }

        return {
            "response": self.get_question(),
            "game_over": False
        }

    # ===============================
    # UI
    # ===============================
    def _pause_message(self):
        c = self._c()

        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": c["bg"],
                "paddingAll": "20px",
                "spacing": "md",
                "contents": [
                    {
                        "type": "text",
                        "text": "تم حفظ تقدمك",
                        "size": "xl",
                        "weight": "bold",
                        "align": "center",
                        "color": c["primary"]
                    },
                    {
                        "type": "separator",
                        "margin": "lg",
                        "color": c["border"]
                    },
                    {
                        "type": "text",
                        "text": f"النقاط: {self.score}",
                        "align": "center",
                        "color": c["success"]
                    },
                    {
                        "type": "text",
                        "text": f"الأسئلة: {self.current_q}/{self.total_q}",
                        "align": "center",
                        "size": "sm",
                        "color": c["text_secondary"]
                    }
                ]
            }
        }

        return FlexMessage(
            alt_text="تم حفظ التقدم",
            contents=FlexContainer.from_dict(bubble)
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
                "backgroundColor": c["bg"],
                "paddingAll": "20px",
                "spacing": "md",
                "contents": [
                    {
                        "type": "text",
                        "text": "انتهت اللعبة",
                        "size": "xxl",
                        "weight": "bold",
                        "align": "center",
                        "color": c["primary"]
                    },
                    {
                        "type": "separator",
                        "margin": "lg",
                        "color": c["border"]
                    },
                    {
                        "type": "text",
                        "text": "فوز كامل" if won else f"النتيجة {self.score}/{self.total_q}",
                        "size": "xl",
                        "align": "center",
                        "color": c["success"] if won else c["warning"]
                    },
                    {
                        "type": "separator",
                        "margin": "lg",
                        "color": c["border"]
                    },
                    {
                        "type": "button",
                        "action": {
                            "type": "message",
                            "label": "العاب",
                            "text": "العاب"
                        },
                        "style": "primary",
                        "color": c["primary"]
                    }
                ]
            }
        }

        return FlexMessage(
            alt_text="انتهت اللعبة",
            contents=FlexContainer.from_dict(bubble)
        )

    # ===============================
    # Question Builder
    # ===============================
    def build_question_flex(self, question_text: str, hint: str = ""):
        c = self._c()

        contents = [
            {
                "type": "text",
                "text": f"السؤال {self.current_q + 1}",
                "size": "sm",
                "color": c["text_secondary"],
                "align": "center"
            },
            {
                "type": "separator",
                "margin": "md",
                "color": c["border"]
            },
            {
                "type": "text",
                "text": question_text,
                "size": "xl",
                "weight": "bold",
                "wrap": True,
                "align": "center",
                "color": c["text"]
            }
        ]

        if hint:
            contents.append({
                "type": "text",
                "text": hint,
                "size": "sm",
                "align": "center",
                "color": c["text_tertiary"],
                "margin": "md"
            })

        contents.append({
            "type": "text",
            "text": "اكتب الإجابة في الدردشة",
            "size": "xs",
            "align": "center",
            "color": c["text_secondary"],
            "margin": "lg"
        })

        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": c["bg"],
                "paddingAll": "20px",
                "spacing": "md",
                "contents": contents
            }
        }

        return FlexMessage(
            alt_text="سؤال اللعبة",
            contents=FlexContainer.from_dict(bubble),
            quickReply=self._quick_reply()
        )
