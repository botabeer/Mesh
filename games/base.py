from abc import ABC, abstractmethod
from linebot.v3.messaging import FlexMessage, FlexContainer, QuickReply, QuickReplyItem, MessageAction
from config import Config


class BaseGame(ABC):
    """القاعدة الموحدة لجميع الالعاب - بدون إيموجي"""
    
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
        """الحصول على الوان السمة"""
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

    @abstractmethod
    def get_question(self):
        """يجب تنفيذها في كل لعبة"""
        pass

    @abstractmethod
    def check_answer(self, answer: str) -> bool:
        """يجب تنفيذها في كل لعبة"""
        pass

    def start(self, user_id: str):
        """بدء اللعبة"""
        self.user_id = user_id
        self.current_q = 0
        self.score = 0
        return self.get_question()

    def restore(self, progress: dict):
        """استعادة التقدم"""
        self.score = progress.get("score", 0)
        self.current_q = progress.get("current_q", 0)

    def on_stop(self, user_id: str):
        """عند ايقاف اللعبة"""
        self.db.save_game_progress(user_id, {
            "game": self.game_name,
            "score": self.score,
            "current_q": self.current_q
        })

    def check(self, answer: str, user_id: str):
        """المنطق الاساسي للتحقق"""
        if user_id != self.user_id:
            return None

        cmd = Config.normalize(answer)

        # تجاهل الاوامر الرئيسية
        if cmd in {"بدايه", "بداية", "مساعده", "مساعدة", "العاب"}:
            return None

        # ايقاف
        if cmd in ("ايقاف", "ايقاف اللعبة"):
            return {"response": self._pause_message(), "game_over": True}

        # اللمح
        if self.supports_hint and cmd == "لمح":
            hint = self._get_hint()
            if hint:
                return {"response": self._hint_message(hint), "game_over": False}

        # الجواب
        if self.supports_reveal and cmd == "جاوب":
            return {"response": self._reveal_message(), "game_over": False, "skip": True}

        # التحقق من الاجابة
        try:
            correct = self.check_answer(answer)
        except:
            return None

        if not correct:
            return None

        # اجابة صحيحة
        self.score += 1
        if self.db and self.db.get_user(user_id):
            self.db.add_points(user_id, 1)
        self.current_q += 1

        # نهاية اللعبة
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

    def _get_hint(self):
        """الحصول على تلميح"""
        if isinstance(self.current_answer, list):
            ans = self.current_answer[0]
        else:
            ans = str(self.current_answer)
        
        if len(ans) > 2:
            return f"يبدأ بـ {ans[0]}\nعدد الحروف {len(ans)}"
        return f"حرفين: {ans[0]}_"

    def _hint_message(self, hint: str):
        """رسالة التلميح"""
        c = self._c()
        bubble = {
            "type": "bubble",
            "size": "kilo",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "تلميح", "size": "md", "weight": "bold", "color": c["primary"], "align": "center"},
                    {"type": "separator", "margin": "md", "color": c["border"]},
                    {"type": "text", "text": hint, "size": "sm", "color": c["text"], "wrap": True, "margin": "md", "align": "center"}
                ],
                "paddingAll": "md",
                "backgroundColor": c["bg"],
                "spacing": "none"
            }
        }
        return FlexMessage(alt_text="تلميح", contents=FlexContainer.from_dict(bubble), quickReply=self._qr())

    def _reveal_message(self):
        """رسالة الكشف عن الاجابة"""
        c = self._c()
        if isinstance(self.current_answer, list):
            ans = " او ".join(self.current_answer)
        else:
            ans = str(self.current_answer)
        
        self.current_q += 1
        
        if self.current_q >= self.total_q:
            return self._game_over_message()
        
        bubble = {
            "type": "bubble",
            "size": "kilo",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "الاجابة", "size": "md", "weight": "bold", "color": c["text"], "align": "center"},
                    {"type": "separator", "margin": "md", "color": c["border"]},
                    {"type": "text", "text": ans, "size": "sm", "color": c["text"], "wrap": True, "margin": "md", "align": "center"}
                ],
                "paddingAll": "md",
                "backgroundColor": c["bg"],
                "spacing": "none"
            }
        }
        
        msg = FlexMessage(alt_text="الاجابة", contents=FlexContainer.from_dict(bubble))
        next_q = self.get_question()
        return [msg, next_q]

    def _pause_message(self):
        """رسالة الايقاف"""
        c = self._c()
        bubble = {
            "type": "bubble",
            "size": "kilo",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "تم حفظ تقدمك", "size": "lg", "weight": "bold", "color": c["primary"], "align": "center"},
                    {"type": "separator", "margin": "md", "color": c["border"]},
                    {"type": "text", "text": f"النقاط {self.score}", "size": "sm", "color": c["text"], "align": "center", "margin": "md"},
                    {"type": "text", "text": f"الاسئلة {self.current_q}/{self.total_q}", "size": "xs", "color": c["text_secondary"], "align": "center"}
                ],
                "paddingAll": "md",
                "backgroundColor": c["bg"],
                "spacing": "none"
            }
        }
        return FlexMessage(alt_text="تم الايقاف", contents=FlexContainer.from_dict(bubble), quickReply=self._qr())

    def _game_over_message(self):
        """رسالة نهاية اللعبة"""
        c = self._c()
        won = self.score == self.total_q
        
        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "انتهت اللعبة", "size": "xl", "weight": "bold", "color": c["primary"], "align": "center"},
                    {"type": "separator", "margin": "lg", "color": c["border"]},
                    {"type": "text", "text": "فوز كامل" if won else f"النتيجة {self.score}/{self.total_q}", "size": "lg", "color": c["primary"] if won else c["text"], "align": "center", "margin": "lg"},
                    {"type": "separator", "margin": "lg", "color": c["border"]},
                    {"type": "button", "action": {"type": "message", "label": "العاب", "text": "العاب"}, "style": "primary", "color": c["primary"], "margin": "md"},
                    {"type": "button", "action": {"type": "message", "label": "البداية", "text": "بداية"}, "style": "secondary", "margin": "sm"}
                ],
                "paddingAll": "lg",
                "backgroundColor": c["bg"],
                "spacing": "none"
            }
        }
        return FlexMessage(alt_text="النتيجة", contents=FlexContainer.from_dict(bubble), quickReply=self._qr())

    def build_question_flex(self, question_text: str, hint: str = ""):
        """بناء سؤال Flex موحد"""
        c = self._c()
        
        contents = [
            {"type": "text", "text": self.game_name, "size": "lg", "weight": "bold", "color": c["primary"], "align": "center"},
            {"type": "text", "text": f"السؤال {self.current_q + 1}/{self.total_q}", "size": "xs", "color": c["text_tertiary"], "align": "center"},
            {"type": "separator", "margin": "md", "color": c["border"]},
            {"type": "text", "text": question_text, "size": "md", "weight": "bold", "color": c["text"], "wrap": True, "align": "center", "margin": "lg"}
        ]
        
        if hint:
            contents.append({"type": "text", "text": hint, "size": "xs", "color": c["text_secondary"], "align": "center", "margin": "sm"})
        
        contents.append({"type": "separator", "margin": "lg", "color": c["border"]})
        
        # ازرار اللمح والجواب
        if self.supports_hint and self.supports_reveal:
            contents.append({
                "type": "box",
                "layout": "horizontal",
                "spacing": "sm",
                "margin": "md",
                "contents": [
                    {"type": "button", "action": {"type": "message", "label": "لمح", "text": "لمح"}, "style": "secondary", "height": "sm"},
                    {"type": "button", "action": {"type": "message", "label": "جاوب", "text": "جاوب"}, "style": "secondary", "height": "sm"}
                ]
            })
        
        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": contents,
                "paddingAll": "lg",
                "backgroundColor": c["bg"],
                "spacing": "none"
            }
        }
        
        return FlexMessage(alt_text=self.game_name, contents=FlexContainer.from_dict(bubble), quickReply=self._qr())
