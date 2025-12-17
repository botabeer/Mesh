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
        items = [
            "بداية", "العاب", "نقاطي", "الصدارة", "ثيم", "ايقاف", "مساعدة",
            "تحدي", "سؤال", "اعتراف", "منشن", "موقف", "حكمة", "شخصية"
        ]
        return QuickReply(items=[QuickReplyItem(action=MessageAction(label=i, text=i)) for i in items])

    def _safe_text(self, text, fallback=" "):
        if isinstance(text, str) and text.strip():
            return text
        return fallback

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
        self.db.save_game_progress(user_id, {"game": self.game_name, "score": self.score, "current_q": self.current_q})

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
            return f"يبدأ بـ {ans[0]}\nعدد الحروف {len(ans)}"
        return f"{ans[0]}_"

    def _hint_message(self, hint):
        c = self._c()
        contents = [
            {"type": "text", "text": "تلميح", "size": "lg", "weight": "bold", "color": c["primary"], "align": "center"},
            {"type": "separator", "margin": "md", "color": c["border"]},
            {"type": "box", "layout": "vertical", "contents": [
                {"type": "text", "text": self._safe_text(hint), "size": "md", "color": c["text"], "wrap": True, "align": "center"}
            ], "backgroundColor": c["glass"], "cornerRadius": "12px", "paddingAll": "16px", "margin": "lg"}
        ]
        bubble = {"type": "bubble", "size": "mega", "body": {"type": "box", "layout": "vertical", "contents": contents, "backgroundColor": c["bg"], "paddingAll": "20px"}}
        return FlexMessage(alt_text="تلميح", contents=FlexContainer.from_dict(bubble), quickReply=self._qr())

    def _reveal_message(self):
        c = self._c()
        ans = " أو ".join(self.current_answer) if isinstance(self.current_answer, list) else str(self.current_answer)
        self.current_q += 1
        if self.current_q >= self.total_q:
            return self._game_over_message()
        
        contents = [
            {"type": "text", "text": "الإجابة", "size": "lg", "weight": "bold", "color": c["primary"], "align": "center"},
            {"type": "separator", "margin": "md", "color": c["border"]},
            {"type": "box", "layout": "vertical", "contents": [
                {"type": "text", "text": self._safe_text(ans), "size": "md", "color": c["text"], "wrap": True, "align": "center"}
            ], "backgroundColor": c["glass"], "cornerRadius": "12px", "paddingAll": "16px", "margin": "lg"}
        ]
        bubble = {"type": "bubble", "size": "mega", "body": {"type": "box", "layout": "vertical", "contents": contents, "backgroundColor": c["bg"], "paddingAll": "20px"}}
        return FlexMessage(alt_text="الإجابة", contents=FlexContainer.from_dict(bubble), quickReply=self._qr())

    def _pause_message(self):
        c = self._c()
        contents = [
            {"type": "text", "text": "تم حفظ تقدمك", "size": "lg", "weight": "bold", "color": c["warning"], "align": "center"},
            {"type": "separator", "margin": "md", "color": c["border"]},
            {"type": "box", "layout": "vertical", "contents": [
                {"type": "text", "text": f"النقاط: {self.score}", "size": "md", "color": c["text"], "align": "center"},
                {"type": "text", "text": f"{self.current_q}/{self.total_q}", "size": "sm", "color": c["text_secondary"], "align": "center", "margin": "xs"}
            ], "backgroundColor": c["glass"], "cornerRadius": "12px", "paddingAll": "16px", "margin": "lg"}
        ]
        bubble = {"type": "bubble", "size": "mega", "body": {"type": "box", "layout": "vertical", "contents": contents, "backgroundColor": c["bg"], "paddingAll": "20px"}}
        return FlexMessage(alt_text="تم الإيقاف", contents=FlexContainer.from_dict(bubble), quickReply=self._qr())

    def _game_over_message(self):
        c = self._c()
        won = self.score == self.total_q
        contents = [
            {"type": "text", "text": "انتهت اللعبة", "size": "xl", "weight": "bold", "color": c["primary"], "align": "center"},
            {"type": "separator", "margin": "md", "color": c["border"]},
            {"type": "box", "layout": "vertical", "contents": [
                {"type": "text", "text": "فوز كامل" if won else f"النتيجة: {self.score}/{self.total_q}", "size": "lg", "color": c["success"] if won else c["text"], "align": "center", "weight": "bold"}
            ], "backgroundColor": c["glass"], "cornerRadius": "12px", "paddingAll": "20px", "margin": "lg"}
        ]
        bubble = {"type": "bubble", "size": "mega", "body": {"type": "box", "layout": "vertical", "contents": contents, "backgroundColor": c["bg"], "paddingAll": "20px"}}
        return FlexMessage(alt_text="النتيجة", contents=FlexContainer.from_dict(bubble), quickReply=self._qr())

    def build_question_flex(self, question_text, hint=None):
        c = self._c()
        contents = [
            {"type": "box", "layout": "horizontal", "contents": [
                {"type": "box", "layout": "vertical", "contents": [
                    {"type": "text", "text": self._safe_text(self.game_name), "weight": "bold", "size": "lg", "color": c["primary"]}
                ], "flex": 1},
                {"type": "box", "layout": "vertical", "contents": [
                    {"type": "text", "text": f"{self.current_q+1}/{self.total_q}", "size": "sm", "align": "end", "color": c["text_secondary"]}
                ], "flex": 0}
            ]},
            {"type": "separator", "margin": "md", "color": c["border"]}
        ]
        
        if hint:
            contents.append({
                "type": "text", "text": self._safe_text(hint), "size": "xs", "color": c["text_tertiary"], "align": "center", "margin": "md"
            })
        
        contents.append({
            "type": "box", "layout": "vertical", 
            "contents": [
                {"type": "text", "text": self._safe_text(question_text), "wrap": True, "align": "center", "size": "md", "color": c["text"], "weight": "bold"}
            ],
            "backgroundColor": c["glass"], "cornerRadius": "12px", "paddingAll": "16px", "margin": "lg"
        })
        
        if self.supports_hint and self.supports_reveal:
            contents.append({
                "type": "box", "layout": "horizontal", "spacing": "sm", "margin": "lg",
                "contents": [
                    {"type": "button", "action": {"type": "message", "label": "لمح", "text": "لمح"}, "style": "secondary", "flex": 1, "height": "sm"},
                    {"type": "button", "action": {"type": "message", "label": "جاوب", "text": "جاوب"}, "style": "secondary", "flex": 1, "height": "sm"}
                ]
            })
        
        bubble = {"type": "bubble", "size": "mega", "body": {"type": "box", "layout": "vertical", "contents": contents, "backgroundColor": c["bg"], "paddingAll": "20px"}}
        return FlexMessage(alt_text=self.game_name, contents=FlexContainer.from_dict(bubble), quickReply=self._qr())
