from abc import ABC, abstractmethod
from linebot.v3.messaging import FlexMessage, FlexContainer, QuickReply, QuickReplyItem, MessageAction
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
        self.game_name = "لعبة"

    def _c(self):
        return Config.get_theme(self.theme)

    def _qr(self):
        items = ["بداية", "العاب", "ايقاف"]
        return QuickReply(items=[QuickReplyItem(action=MessageAction(label=i, text=i)) for i in items])

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

    def build_question_flex(self, question_text, hint=None):
        c = self._c()

        contents = [
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "flex": 1,
                        "contents": [
                            {"type": "text", "text": self.game_name, "weight": "bold", "size": "lg", "color": c["text"]},
                            {"type": "text", "text": f"السؤال {self.current_q + 1}/{self.total_q}", "size": "xs", "color": c["text_secondary"]}
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "width": "60px",
                        "backgroundColor": c["glass"],
                        "cornerRadius": "12px",
                        "paddingAll": "8px",
                        "contents": [
                            {"type": "text", "text": str(self.score), "size": "xl", "weight": "bold", "color": c["success"], "align": "center"},
                            {"type": "text", "text": "نقطة", "size": "xs", "color": c["text_tertiary"], "align": "center"}
                        ]
                    }
                ]
            },
            {"type": "separator", "margin": "lg"}
        ]

        if hint:
            contents.append({
                "type": "text",
                "text": hint,
                "size": "xs",
                "color": c["text_tertiary"],
                "align": "center",
                "margin": "md"
            })

        contents.append({
            "type": "box",
            "layout": "vertical",
            "backgroundColor": c["glass"],
            "cornerRadius": "12px",
            "paddingAll": "24px",
            "margin": "lg",
            "contents": [
                {
                    "type": "text",
                    "text": question_text,
                    "wrap": True,
                    "align": "center",
                    "size": "lg",
                    "weight": "bold",
                    "color": c["text"]
                }
            ]
        })

        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": contents,
                "backgroundColor": c["card"],
                "paddingAll": "24px"
            }
        }

        return FlexMessage(
            alt_text=self.game_name,
            contents=FlexContainer.from_dict(bubble),
            quickReply=self._qr()
        )
