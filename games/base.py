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
        self.supports_hint = True
        self.supports_reveal = True

    def _c(self):
        return Config.get_theme(self.theme)

    def _qr(self):
        items = ["سؤال", "منشن", "تحدي", "اعتراف", "شخصية", "حكمة", "موقف", "بداية", "العاب", "مساعدة"]
        return QuickReply(items=[QuickReplyItem(action=MessageAction(label=i, text=i)) for i in items])
    
    def _safe_text(self, text):
        return str(text) if text else ""

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
            {"type": "text", "text": "Bot Mesh", "size": "xxl", "weight": "bold", "color": c["text"], "align": "center"},
            {"type": "separator", "margin": "lg", "color": c["border"]},
            {
                "type": "box",
                "layout": "horizontal",
                "margin": "lg",
                "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "flex": 1,
                        "contents": [
                            {"type": "text", "text": self._safe_text(self.game_name), "weight": "bold", "size": "lg", "color": c["text"]},
                            {"type": "text", "text": f"السؤال {self.current_q + 1}/{self.total_q}", "size": "xs", "color": c["text_secondary"]}
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "width": "60px",
                        "backgroundColor": c["card_secondary"],
                        "cornerRadius": "12px",
                        "paddingAll": "8px",
                        "contents": [
                            {"type": "text", "text": str(self.score), "size": "xl", "weight": "bold", "color": c["text"], "align": "center"},
                            {"type": "text", "text": "نقطة", "size": "xs", "color": c["text_tertiary"], "align": "center"}
                        ]
                    }
                ]
            },
            {"type": "separator", "margin": "lg", "color": c["border"]}
        ]

        if hint:
            contents.append({
                "type": "text",
                "text": self._safe_text(hint),
                "size": "xs",
                "color": c["text_tertiary"],
                "align": "center",
                "margin": "md"
            })

        contents.append({
            "type": "box",
            "layout": "vertical",
            "backgroundColor": c["card"],
            "cornerRadius": "12px",
            "paddingAll": "24px",
            "margin": "lg",
            "contents": [
                {
                    "type": "text",
                    "text": self._safe_text(question_text),
                    "wrap": True,
                    "align": "center",
                    "size": "lg",
                    "weight": "bold",
                    "color": c["text"]
                }
            ]
        })

        # ازرار التحكم
        button_contents = []
        if self.supports_hint:
            button_contents.append({
                "type": "button",
                "action": {"type": "message", "label": "لمح", "text": "لمح"},
                "style": "secondary",
                "color": c["button"],
                "height": "sm",
                "flex": 1
            })
        if self.supports_reveal:
            button_contents.append({
                "type": "button",
                "action": {"type": "message", "label": "جاوب", "text": "جاوب"},
                "style": "secondary",
                "color": c["button"],
                "height": "sm",
                "flex": 1
            })
        button_contents.append({
            "type": "button",
            "action": {"type": "message", "label": "ايقاف", "text": "ايقاف"},
            "style": "secondary",
            "color": c["button"],
            "height": "sm",
            "flex": 1
        })
        
        contents.append({"type": "separator", "margin": "lg", "color": c["border"]})
        contents.append({
            "type": "box",
            "layout": "horizontal",
            "contents": button_contents,
            "spacing": "sm",
            "margin": "md"
        })
        
        contents.append({
            "type": "text",
            "text": "Bot Mesh | 2025 عبير الدوسري",
            "size": "xxs",
            "color": c["text_secondary"],
            "align": "center",
            "margin": "lg"
        })

        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": contents,
                "backgroundColor": c["bg"],
                "paddingAll": "24px"
            }
        }

        return FlexMessage(
            alt_text=self.game_name,
            contents=FlexContainer.from_dict(bubble),
            quickReply=self._qr()
        )
    
    def get_hint(self):
        """اعطاء تلميح - اول حرف وعدد الحروف"""
        if not self.supports_hint or not self.current_answer:
            return None
        
        answer = str(self.current_answer[0]) if isinstance(self.current_answer, list) else str(self.current_answer)
        first_letter = answer[0] if answer else ""
        length = len(answer)
        
        return f"التلميح: {first_letter}{'_' * (length - 1)} ({length} حروف)"
    
    def reveal_answer(self):
        """كشف الاجابة الصحيحة"""
        if not self.supports_reveal or not self.current_answer:
            return None
        
        answer = self.current_answer[0] if isinstance(self.current_answer, list) else self.current_answer
        return f"الاجابة الصحيحة: {answer}"
