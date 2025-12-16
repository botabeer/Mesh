from abc import ABC, abstractmethod
from linebot.v3.messaging import FlexMessage, FlexContainer, QuickReply, QuickReplyItem, MessageAction
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

    def _quick_reply(self):
        return QuickReply(items=[
            QuickReplyItem(action=MessageAction(label="انسحب", text="انسحب")),
            QuickReplyItem(action=MessageAction(label="البداية", text="بداية"))
        ])

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
        
        if cmd in ("بداية", "بدايه", "العاب", "نقاطي", "الصدارة", "الصداره", "تغيير_الثيم", "مساعدة", "مساعده"):
            return None

        if cmd == "انسحب":
            self.db.save_game_progress(user_id, {
                "score": self.score,
                "current_q": self.current_q
            })
            return {"response": self._create_pause_message(), "game_over": True}

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

    def _create_pause_message(self):
        c = self._c()
        contents = [
            {
                "type": "text",
                "text": "تم حفظ تقدمك",
                "size": "xl",
                "weight": "bold",
                "color": c["primary"],
                "align": "center"
            },
            {"type": "separator", "margin": "lg", "color": c["border"]},
            {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": c["glass"],
                "cornerRadius": "12px",
                "paddingAll": "16px",
                "margin": "md",
                "contents": [
                    {
                        "type": "text",
                        "text": f"النقاط المكتسبة: {self.score}",
                        "size": "md",
                        "color": c["success"],
                        "align": "center"
                    },
                    {
                        "type": "text",
                        "text": f"الاسئلة المجابة: {self.current_q}/{self.total_q}",
                        "size": "sm",
                        "color": c["text_secondary"],
                        "align": "center",
                        "margin": "sm"
                    }
                ]
            },
            {"type": "separator", "margin": "lg", "color": c["border"]},
            {
                "type": "button",
                "action": {"type": "message", "label": "البداية", "text": "بداية"},
                "style": "primary",
                "color": c["primary"],
                "height": "sm",
                "margin": "md"
            }
        ]

        flex = {
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
            alt_text="تم حفظ تقدمك",
            contents=FlexContainer.from_dict(flex)
        )

    def _game_over(self):
        c = self._c()
        won = self.score == self.total_q
        self.db.add_points(self.user_id, self.score)
        self.db.finish_game(self.user_id, won)
        self.db.clear_game_progress(self.user_id)

        result_text = "فوز كامل" if won else f"النتيجة {self.score} من {self.total_q}"
        result_color = c["success"] if won else c["warning"]

        contents = [
            {
                "type": "text",
                "text": "انتهت اللعبة",
                "size": "xxl",
                "weight": "bold",
                "color": c["primary"],
                "align": "center"
            },
            {"type": "separator", "margin": "lg", "color": c["border"]},
            {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": c["glass"],
                "cornerRadius": "16px",
                "paddingAll": "16px",
                "margin": "md",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "text",
                        "text": result_text,
                        "size": "xl",
                        "weight": "bold",
                        "color": result_color,
                        "align": "center"
                    },
                    {
                        "type": "text",
                        "text": f"النقاط المكتسبة: {self.score}",
                        "size": "md",
                        "color": c["text_secondary"],
                        "align": "center",
                        "margin": "md"
                    }
                ]
            },
            {"type": "separator", "margin": "lg", "color": c["border"]},
            {
                "type": "box",
                "layout": "horizontal",
                "spacing": "sm",
                "margin": "md",
                "contents": [
                    {
                        "type": "button",
                        "action": {"type": "message", "label": "العاب", "text": "العاب"},
                        "style": "primary",
                        "color": c["primary"],
                        "height": "sm",
                        "flex": 1
                    },
                    {
                        "type": "button",
                        "action": {"type": "message", "label": "البداية", "text": "بداية"},
                        "style": "secondary",
                        "height": "sm",
                        "flex": 1
                    }
                ]
            }
        ]

        flex = {
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
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": f"السؤال {self.current_q + 1}",
                        "size": "sm",
                        "color": c["text_secondary"],
                        "flex": 1
                    },
                    {
                        "type": "text",
                        "text": f"النقاط {self.score}",
                        "size": "sm",
                        "color": c["success"],
                        "align": "end",
                        "flex": 1
                    }
                ]
            },
            {"type": "separator", "margin": "md", "color": c["border"]},
            {
                "type": "text",
                "text": question_text,
                "size": "xl",
                "weight": "bold",
                "color": c["text"],
                "align": "center",
                "wrap": True,
                "margin": "lg"
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
            {"type": "separator", "margin": "lg", "color": c["border"]},
            {
                "type": "text",
                "text": "ارسل الاجابة في الدردشة",
                "size": "xs",
                "color": c["text_secondary"],
                "align": "center",
                "margin": "md"
            }
        ])

        flex = {
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
            contents=FlexContainer.from_dict(flex),
            quickReply=self._quick_reply()
        )
