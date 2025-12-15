from abc import ABC, abstractmethod
from linebot.v3.messaging import FlexMessage, FlexContainer, TextMessage
from config import Config


class BaseGame(ABC):
    """الفئة الأساسية لكل الألعاب"""

    def __init__(self, db, theme: str = "light"):
        self.db = db
        self.theme = theme
        self.current_q = 0
        self.total_q = 5
        self.score = 0
        self.user_id = None
        self.current_answer = None

    def _c(self):
        """الحصول على ألوان الثيم"""
        return Config.get_theme(self.theme)

    @abstractmethod
    def get_question(self):
        """الحصول على سؤال - يجب تنفيذه في كل لعبة"""
        pass

    @abstractmethod
    def check_answer(self, answer: str) -> bool:
        """التحقق من الإجابة - يجب تنفيذه في كل لعبة"""
        pass

    # ---------------- Start / Check ----------------

    def start(self, user_id: str):
        """بدء اللعبة"""
        self.user_id = user_id
        self.current_q = 0
        self.score = 0
        return self._normalize_response(self.get_question())

    def check(self, answer: str, user_id: str):
        """فحص الإجابة وتحديث النتيجة"""
        try:
            is_correct = self.check_answer(answer)
        except Exception:
            return {
                "response": TextMessage(text="⚠️ إجابة غير صالحة"),
                "game_over": False
            }

        if not is_correct:
            return {
                "response": TextMessage(text="❌ إجابة خاطئة"),
                "game_over": False
            }

        self.score += 1
        self.current_q += 1

        if self.current_q >= self.total_q:
            return self._game_over()

        return {
            "response": self._normalize_response(self.get_question()),
            "game_over": False
        }

    # ---------------- Game Over ----------------

    def _game_over(self):
        """انتهاء اللعبة"""
        c = self._c()
        won = self.score == self.total_q

        # تحديث قاعدة البيانات
        self.db.add_points(self.user_id, self.score)
        self.db.finish_game(self.user_id, won)

        # تصميم الفلكس آمن
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
                                "text": f"النتيجة: {self.score}/{self.total_q}",
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
                            "label": "القائمة",
                            "text": "بداية"
                        },
                        "style": "primary",
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

    # ---------------- Question Builder ----------------

    def build_question_flex(self, question: str, hint: str = None):
        """بناء واجهة السؤال"""
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

    # ---------------- Utils ----------------

    def _normalize_response(self, response):
        """
        يضمن أن الاستجابة صالحة للإرسال عبر LINE
        """
        if response is None:
            return TextMessage(text="⚠️ استجابة غير صالحة")

        if isinstance(response, (TextMessage, FlexMessage)):
            return response

        if isinstance(response, str):
            return TextMessage(text=response)

        return TextMessage(text="⚠️ استجابة غير صالحة من اللعبة")
