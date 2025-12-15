from abc import ABC, abstractmethod
from linebot.v3.messaging import FlexMessage, FlexContainer, TextMessage
from config import Config

class BaseGame(ABC):
    def __init__(self, db, theme="light"):
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
        if not self.db.get_user(user_id):
            return None

        cmd = Config.normalize(answer)
        if cmd in ("بدايه", "العاب", "نقاطي", "الصداره", "تغيير", "تغيير_الثيم"):
            return None

        if cmd == "انسحب":
            return {"response": TextMessage(text="تم الانسحاب"), "game_over": True}

        try:
            is_correct = self.check_answer(answer)
        except Exception:
            return None

        if not is_correct:
            return None

        self.score += 1
        self.current_q += 1

        if self.current_q >= self.total_q:
            return self._game_over()

        return {"response": self.get_question(), "game_over": False}

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
                        "text": "انتهت اللعبة",
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
                                "text": f"النتيجة {self.score}/{self.total_q}",
                                "size": "lg",
                                "weight": "bold",
                                "color": c["text"],
                                "align": "center"
                            },
                            {
                                "type": "text",
                                "text": f"+{self.score} نقطة",
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
                            "label": "البداية",
                            "text": "بدايه"
                        },
                        "style": "primary",
                        "color": c["primary"],
                        "margin": "md"
                    }
                ]
            }
        }
        
        return {
            "response": FlexMessage(
                alt_text="انتهت اللعبة",
                contents=FlexContainer.from_dict(flex)
            ),
            "game_over": True
        }

    def build_question_flex(self, question_text: str, hint: str = ""):
        c = self._c()
        contents = [
            {
                "type": "text",
                "text": question_text,
                "size": "xl",
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
        
        contents.extend([
            {"type": "separator", "margin": "md", "color": c["border"]},
            {
                "type": "button",
                "action": {"type": "message", "label": "انسحب", "text": "انسحب"},
                "style": "secondary",
                "height": "sm",
                "margin": "md"
            }
        ])
        
        return FlexMessage(
            alt_text="سؤال",
            contents=FlexContainer.from_dict({
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": contents,
                    "backgroundColor": c["bg"],
                    "paddingAll": "20px"
                }
            })
        )
