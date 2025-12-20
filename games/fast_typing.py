import random
import time
from games.base import BaseGame
from linebot.v3.messaging import FlexMessage, FlexContainer


class FastTypingGame(BaseGame):
    def __init__(self, db, theme="light"):
        super().__init__(db, theme)
        self.game_name = "اسرع"
        self.time_limit = 10
        self.start_time = None
        self.supports_hint = False
        self.supports_reveal = False
        self.time_expired_message_sent = False
        
        self.phrases = [
            "سبحان الله", "الحمد لله", "الله اكبر", "لا اله الا الله",
            "استغفر الله العظيم", "لا حول ولا قوة الا بالله", "بسم الله الرحمن الرحيم",
            "اللهم صل على محمد", "رب اغفر لي", "يا رب العالمين",
            "الصبر مفتاح الفرج", "من جد وجد", "العلم نور", "الوقت كالسيف",
            "العقل السليم في الجسم السليم", "اتق الله حيثما كنت", "قل خيرا او اصمت",
            "الصدق منجاة", "الكذب مهلكة", "الامانة صفة المؤمنين"
        ]
        random.shuffle(self.phrases)
        self.used = []

    def get_question(self):
        available = [p for p in self.phrases if p not in self.used]
        if not available:
            self.used = []
            available = self.phrases.copy()

        phrase = random.choice(available)
        self.used.append(phrase)
        self.current_answer = phrase
        self.start_time = time.time()
        self.time_expired_message_sent = False
        
        c = self._c()
        
        contents = [
            {"type": "box", "layout": "horizontal", "contents": [
                {"type": "box", "layout": "vertical", "contents": [
                    {"type": "text", "text": self._safe_text(self.game_name), "weight": "bold", "size": "lg", "color": c["text"]}
                ], "flex": 1},
                {"type": "box", "layout": "vertical", "contents": [
                    {"type": "text", "text": f"{self.current_q+1}/{self.total_q}", "size": "sm", "align": "end", "color": c["text_secondary"]}
                ], "flex": 0}
            ]},
            {"type": "separator", "margin": "md", "color": c["border"]},
            {
                "type": "box", "layout": "horizontal", "contents": [
                    {"type": "text", "text": f"الوقت: {self.time_limit} ثانية", "size": "xs", "color": c["text_tertiary"], "weight": "bold"}
                ], "margin": "md"
            },
            {
                "type": "box", "layout": "vertical", 
                "contents": [
                    {"type": "text", "text": self._safe_text(phrase), "wrap": True, "align": "center", "size": "md", "color": c["text"], "weight": "bold"}
                ],
                "backgroundColor": c["card_secondary"], "cornerRadius": "12px", "paddingAll": "16px", "margin": "md"
            },
            {
                "type": "text", "text": "اكتب بسرعة", "size": "xs", "align": "center", "margin": "sm", "color": c["text_tertiary"]
            },
            {"type": "separator", "margin": "lg", "color": c["border"]},
            {
                "type": "box", "layout": "horizontal", "contents": [
                    {
                        "type": "button",
                        "action": {"type": "message", "label": "ايقاف", "text": "ايقاف"},
                        "style": "secondary",
                        "color": c["button"],
                        "height": "sm"
                    }
                ], "margin": "md"
            }
        ]

        bubble = {"type": "bubble", "size": "mega", "body": {"type": "box", "layout": "vertical", "contents": contents, "backgroundColor": c["card"], "paddingAll": "20px"}}
        return FlexMessage(alt_text=self.game_name, contents=FlexContainer.from_dict(bubble), quickReply=self._qr())

    def check_answer(self, answer):
        if self.start_time is None:
            return False
        
        elapsed = time.time() - self.start_time
        
        if elapsed > self.time_limit:
            if not self.time_expired_message_sent:
                self.time_expired_message_sent = True
                self.error_message = "انتهى الوقت"
            return False
        
        return answer.strip() == self.current_answer
