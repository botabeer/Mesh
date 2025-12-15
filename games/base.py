from abc import ABC, abstractmethod
from linebot.v3.messaging import FlexMessage, FlexContainer, TextMessage
from config import Config


class BaseGame(ABC):
    def __init__(self, db, theme: str = "light"):
        self.db = db
        self.theme = theme
        self.current_q = 0
        self.total_q = 5
        self.score = 0
        self.user_id = None
        self.current_answer = None

    def _c(self):
        return Config.get_theme(self.theme)

    @abstractmethod
    def get_question(self):
        pass

    @abstractmethod
    def check_answer(self, answer: str) -> bool:
        pass

    def start(self, user_id: str):
        self.user_id = user_id
        self.current_q = 0
        self.score = 0
        return self.get_question()

    def check(self, answer: str, user_id: str):
        try:
            is_correct = self.check_answer(answer)
        except Exception:
            return {
                "response": TextMessage(text="اجابه غير صالحه"),
                "game_over": False
            }

        if not is_correct:
            return {
                "response": TextMessage(text="اجابه خاطئه"),
                "game_over": False
            }

        self.score += 1
        self.current_q += 1

        if self.current_q >= self.total_q:
            return self._game_over()

        return {
            "response": self.get_question(),
            "game_over": False
        }

    def _game_over(self):
        c = self._c()
        won = self.score == self.total_q

        self.db.add_points(self.user_id, self.score)
        self.db.finish_game(self.user_id, won)

        flex = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": c["bg"],
                "paddingAll": "20px",
                "contents": [
                    {
                        "type": "text",
                        "text": "انتهت اللعبه",
                        "size": "xl",
                        "weight": "bold",
                        "color": c["primary"],
                        "align": "center"
                    },
                    {"type": "separator", "margin": "md"},
                    {
                        "type": "box",
                        "layout": "vertical",
                        "backgroundColor": c["glass"],
                        "cornerRadius": "16px",
                        "paddingAll": "16px",
                        "margin": "md",
                        "contents": [
                            {
                                "type": "text",
                                "text": f"النتيجه: {self.score}/{self.total_q}",
                                "size": "lg",
                                "weight": "bold",
                                "color": c["text"],
                                "align": "center"
                            },
                            {
                                "type": "text",
                                "text": f"+{self.score} نقطه",
                                "size": "md",
                                "color": c["success"],
                                "align": "center",
                                "margin": "sm"
                            }
                        ]
                    },
                    {"type": "separator", "margin": "md"},
                    {
                        "type": "button",
                        "action": {
                            "type": "message",
                            "label": "القائمه",
                            "text": "بدايه"
                        },
                        "style": "primary",
                        "margin": "md"
                    }
                ]
            }
        }

        return {
            "response": FlexMessage(
                alt_text="انتهت اللعبه",
                contents=FlexContainer.from_dict(flex)
            ),
            "game_over": True
        }

    def build_question_flex(self, question: str, hint: str = None):
        c = self._c()
        contents = [
            {
                "type": "text",
                "text": question,
                "size": "lg",
                "weight": "bold",
                "color": c["text"],
                "align": "center",
                "wrap": True
            }
        ]

        if hint:
            contents.append({
                "type": "text",
                "text": hint,
                "size": "sm",
                "color": c["text_tertiary"],
                "align": "center",
                "margin": "md"
            })

        flex = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": c["bg"],
                "paddingAll": "20px",
                "contents": contents
            }
        }

        return FlexMessage(
            alt_text="سؤال",
            contents=FlexContainer.from_dict(flex)
        )
