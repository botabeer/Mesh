from abc import ABC, abstractmethod
from linebot.v3.messaging import FlexMessage, FlexContainer, TextMessage
from config import Config


class BaseGame(ABC):
    """اللعبة الاساسية"""
    
    def __init__(self, db, theme: str = "light"):
        self.db = db
        self.theme = theme
        self.current_q = 0
        self.total_q = 5
        self.score = 0
        self.current_answer = None
    
    def _c(self):
        """الحصول على الالوان"""
        return Config.get_theme(self.theme)
    
    @abstractmethod
    def get_question(self):
        """الحصول على السؤال"""
        pass
    
    @abstractmethod
    def check_answer(self, answer: str) -> bool:
        """التحقق من الاجابة"""
        pass
    
    def start(self):
        """بدء اللعبة"""
        self.current_q = 0
        self.score = 0
        return self.get_question()
    
    def check(self, answer: str, user_id: str):
        """معالجة الاجابة"""
        is_correct = self.check_answer(answer)
        
        if is_correct:
            self.score += 1
            self.current_q += 1
            
            # اضافة نقاط
            self.db.add_points(user_id, 1, False)
            
            # انتهت اللعبة؟
            if self.current_q >= self.total_q:
                return self._game_over()
            
            # سؤال جديد
            return {
                "response": self.get_question(),
                "game_over": False
            }
        
        return None
    
    def _game_over(self):
        """نهاية اللعبة"""
        c = self._c()
        
        # تحديث الفوز
        if self.score == self.total_q:
            self.db.add_points("", 0, True)  # تسجيل فوز
        
        flex = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": c["bg"],
                "paddingAll": "20px",
                "contents": [
                    {"type": "text", "text": "انتهت اللعبة", "size": "xl", "weight": "bold", "color": c["primary"], "align": "center"},
                    {"type": "separator", "margin": "md", "color": c["border"]},
                    {"type": "box", "layout": "vertical", "backgroundColor": c["glass"], "cornerRadius": "16px", "paddingAll": "16px", "margin": "md", "contents": [
                        {"type": "text", "text": f"النتيجة: {self.score}/{self.total_q}", "size": "lg", "weight": "bold", "color": c["text"], "align": "center"},
                        {"type": "text", "text": f"+{self.score} نقطة", "size": "md", "color": c["success"], "align": "center", "margin": "sm"}
                    ]},
                    {"type": "separator", "margin": "md", "color": c["border"]},
                    {"type": "button", "action": {"type": "message", "label": "القائمة", "text": "بداية"}, "style": "primary", "color": c["primary"]}
                ]
            }
        }
        
        return {
            "response": FlexMessage(alt_text="انتهت اللعبة", contents=FlexContainer.from_dict(flex)),
            "game_over": True
        }
    
    def build_question_flex(self, question: str, hint: str = None):
        """بناء واجهة السؤال"""
        c = self._c()
        
        contents = [
            {"type": "text", "text": self.__class__.__name__.replace("Game", ""), "size": "md", "weight": "bold", "color": c["primary"], "align": "center"},
            {"type": "text", "text": f"السؤال {self.current_q + 1}/{self.total_q}", "size": "xs", "color": c["text_tertiary"], "align": "center", "margin": "xs"},
            {"type": "separator", "margin": "md", "color": c["border"]},
            {"type": "box", "layout": "vertical", "backgroundColor": c["glass"], "cornerRadius": "16px", "paddingAll": "20px", "margin": "md", "contents": [
                {"type": "text", "text": question, "size": "lg", "weight": "bold", "color": c["text"], "align": "center", "wrap": True}
            ]}
        ]
        
        if hint:
            contents.append({"type": "text", "text": hint, "size": "xs", "color": c["text_tertiary"], "align": "center", "margin": "sm"})
        
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
        
        return FlexMessage(alt_text="سؤال", contents=FlexContainer.from_dict(flex))
