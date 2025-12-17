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
        self.game_icon = "🎮"
        self.supports_hint = True
        self.supports_reveal = True

    def _c(self):
        return Config.get_theme(self.theme)

    def _qr(self):
        items = ["بداية", "العاب", "نقاطي", "الصدارة", "ايقاف"]
        return QuickReply(items=[QuickReplyItem(action=MessageAction(label=i, text=i)) for i in items])

    def _safe_text(self, text, fallback=" "):
        if isinstance(text, str) and text.strip():
            return text
        return fallback

    def _separator(self, margin="md"):
        c = self._c()
        return {"type": "separator", "margin": margin, "color": c["border"]}

    def _glass_box(self, contents, padding="16px", margin="none"):
        c = self._c()
        return {
            "type": "box",
            "layout": "vertical",
            "contents": contents,
            "backgroundColor": c["glass"],
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

    def restore(self, progress):
        self.score = progress.get("score", 0)
        self.current_q = progress.get("current_q", 0)

    def on_stop(self, user_id):
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
        except:
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
            return {"response": self._game_over_message(), "game_over": True, "won": won}

        return {"response": self.get_question(), "game_over": False}

    def _get_hint(self):
        ans = self.current_answer[0] if isinstance(self.current_answer, list) else str(self.current_answer)
        if len(ans) > 2:
            return f"يبدا بـ {ans[0]}\nعدد الحروف {len(ans)}"
        return f"{ans[0]}_"

    def _hint_message(self):
        c = self._c()
        hint = self._get_hint()
        
        contents = [
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": "💡",
                        "size": "xl",
                        "flex": 0
                    },
                    {
                        "type": "text",
                        "text": "تلميح",
                        "size": "lg",
                        "weight": "bold",
                        "color": c["text"],
                        "flex": 1,
                        "margin": "md"
                    }
                ]
            },
            self._separator(),
            self._glass_box([
                {
                    "type": "text",
                    "text": self._safe_text(hint),
                    "size": "md",
                    "color": c["text"],
                    "wrap": True,
                    "align": "center",
                    "weight": "bold"
                }
            ], "20px", "md")
        ]
        
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
        return FlexMessage(alt_text="تلميح", contents=FlexContainer.from_dict(bubble), quickReply=self._qr())

    def _reveal_message(self):
        c = self._c()
        ans = " او ".join(self.current_answer) if isinstance(self.current_answer, list) else str(self.current_answer)
        self.current_q += 1
        
        if self.current_q >= self.total_q:
            return self._game_over_message()
        
        contents = [
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": "✓",
                        "size": "xl",
                        "color": c["success"],
                        "flex": 0
                    },
                    {
                        "type": "text",
                        "text": "الاجابة الصحيحة",
                        "size": "lg",
                        "weight": "bold",
                        "color": c["text"],
                        "flex": 1,
                        "margin": "md"
                    }
                ]
            },
            self._separator(),
            self._glass_box([
                {
                    "type": "text",
                    "text": self._safe_text(ans),
                    "size": "lg",
                    "color": c["primary"],
                    "wrap": True,
                    "align": "center",
                    "weight": "bold"
                }
            ], "20px", "md"),
            {
                "type": "text",
                "text": f"السؤال التالي {self.current_q + 1}/{self.total_q}",
                "size": "xs",
                "color": c["text_tertiary"],
                "align": "center",
                "margin": "lg"
            }
        ]
        
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
        return FlexMessage(alt_text="الاجابة", contents=FlexContainer.from_dict(bubble), quickReply=self._qr())

    def _pause_message(self):
        c = self._c()
        
        contents = [
            {
                "type": "text",
                "text": "⏸",
                "size": "xxl",
                "align": "center",
                "color": c["warning"]
            },
            {
                "type": "text",
                "text": "تم حفظ تقدمك",
                "size": "xl",
                "weight": "bold",
                "color": c["text"],
                "align": "center",
                "margin": "md"
            },
            self._separator("lg"),
            self._glass_box([
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": str(self.score),
                                    "size": "xl",
                                    "weight": "bold",
                                    "color": c["success"],
                                    "align": "center"
                                },
                                {
                                    "type": "text",
                                    "text": "النقاط",
                                    "size": "xs",
                                    "color": c["text_secondary"],
                                    "align": "center"
                                }
                            ],
                            "flex": 1
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": f"{self.current_q}/{self.total_q}",
                                    "size": "xl",
                                    "weight": "bold",
                                    "color": c["primary"],
                                    "align": "center"
                                },
                                {
                                    "type": "text",
                                    "text": "التقدم",
                                    "size": "xs",
                                    "color": c["text_secondary"],
                                    "align": "center"
                                }
                            ],
                            "flex": 1
                        }
                    ]
                }
            ], "16px", "lg"),
            {
                "type": "text",
                "text": "يمكنك العودة لاحقا لاستكمال اللعبة",
                "size": "xs",
                "color": c["text_tertiary"],
                "align": "center",
                "wrap": True,
                "margin": "lg"
            }
        ]
        
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
        return FlexMessage(alt_text="تم الايقاف", contents=FlexContainer.from_dict(bubble), quickReply=self._qr())

    def _game_over_message(self):
        c = self._c()
        won = self.score == self.total_q
        
        contents = [
            {
                "type": "text",
                "text": "🏆" if won else "🎮",
                "size": "xxl",
                "align": "center"
            },
            {
                "type": "text",
                "text": "فوز رائع" if won else "انتهت اللعبة",
                "size": "xxl",
                "weight": "bold",
                "color": c["success"] if won else c["text"],
                "align": "center",
                "margin": "md"
            },
            self._separator("lg"),
            self._glass_box([
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": f"{self.score}/{self.total_q}",
                            "size": "xxl",
                            "weight": "bold",
                            "color": c["success"] if won else c["primary"],
                            "align": "center"
                        },
                        {
                            "type": "text",
                            "text": "اجابة صحيحة",
                            "size": "sm",
                            "color": c["text_secondary"],
                            "align": "center",
                            "margin": "sm"
                        }
                    ]
                }
            ], "24px", "lg"),
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "button",
                        "action": {
                            "type": "message",
                            "label": "لعب مرة اخرى",
                            "text": self.game_name
                        },
                        "style": "primary",
                        "color": c["primary"],
                        "height": "sm",
                        "flex": 1
                    },
                    {
                        "type": "button",
                        "action": {
                            "type": "message",
                            "label": "البداية",
                            "text": "بداية"
                        },
                        "style": "secondary",
                        "height": "sm",
                        "flex": 1
                    }
                ],
                "spacing": "sm",
                "margin": "lg"
            }
        ]
        
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
        return FlexMessage(alt_text="النتيجة", contents=FlexContainer.from_dict(bubble), quickReply=self._qr())

    def build_question_flex(self, question_text, hint=None):
        c = self._c()
        
        contents = [
            # Header
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": self.game_icon,
                        "size": "xl",
                        "flex": 0
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": self._safe_text(self.game_name),
                                "weight": "bold",
                                "size": "lg",
                                "color": c["text"]
                            },
                            {
                                "type": "text",
                                "text": f"السؤال {self.current_q + 1} من {self.total_q}",
                                "size": "xs",
                                "color": c["text_secondary"]
                            }
                        ],
                        "flex": 1,
                        "margin": "md"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": str(self.score),
                                "size": "xl",
                                "weight": "bold",
                                "color": c["success"],
                                "align": "center"
                            },
                            {
                                "type": "text",
                                "text": "نقطة",
                                "size": "xs",
                                "color": c["text_tertiary"],
                                "align": "center"
                            }
                        ],
                        "backgroundColor": c["glass"],
                        "cornerRadius": "12px",
                        "paddingAll": "8px",
                        "flex": 0,
                        "width": "60px"
                    }
                ]
            },
            self._separator("lg")
        ]
        
        # Hint if provided
        if hint:
            contents.append({
                "type": "text",
                "text": self._safe_text(hint),
                "size": "xs",
                "color": c["text_tertiary"],
                "align": "center",
                "margin": "md"
            })
        
        # Question box
        contents.append(
            self._glass_box([
                {
                    "type": "text",
                    "text": self._safe_text(question_text),
                    "wrap": True,
                    "align": "center",
                    "size": "lg",
                    "color": c["text"],
                    "weight": "bold"
                }
            ], "24px", "lg")
        )
        
        # Action buttons
        button_contents = []
        
        if self.supports_hint:
            button_contents.append({
                "type": "button",
                "action": {"type": "message", "label": "💡 تلميح", "text": "لمح"},
                "style": "secondary",
                "flex": 1,
                "height": "sm"
            })
        
        if self.supports_reveal:
            button_contents.append({
                "type": "button",
                "action": {"type": "message", "label": "✓ الاجابة", "text": "جاوب"},
                "style": "secondary",
                "flex": 1,
                "height": "sm"
            })
        
        button_contents.append({
            "type": "button",
            "action": {"type": "message", "label": "⏸ ايقاف", "text": "ايقاف"},
            "style": "secondary",
            "flex": 1,
            "height": "sm"
        })
        
        if button_contents:
            contents.append({
                "type": "box",
                "layout": "horizontal",
                "contents": button_contents,
                "spacing": "sm",
                "margin": "lg"
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
