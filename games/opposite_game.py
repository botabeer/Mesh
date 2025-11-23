from linebot.models import TextSendMessage, FlexSendMessage
from .base_game import BaseGame
import random
import difflib

class OppositeGameAI(BaseGame):
    """لعبة ضد الكلمة - نسخة AI ▫️▪️"""
    
    def __init__(self, line_bot_api, questions_count=10, use_ai=False, ai_generate_question=None, ai_check_answer=None):
        """
        ai_generate_question: دالة تولد سؤال {'word': 'كلمة', 'opposite': 'ضد الكلمة'}
        ai_check_answer: دالة تتحقق من صحة الإجابة (تشابه/أخطاء إملائية)
        """
        super().__init__(line_bot_api, questions_count)
        self.use_ai = use_ai
        self.ai_generate_question = ai_generate_question
        self.ai_check_answer = ai_check_answer
        self.found_words = set()
        
        # قاعدة مبدئية للكلمات وضدها
        self.default_opposites = [
            {"word": "كبير", "opposite": "صغير"},
            {"word": "طويل", "opposite": "قصير"},
            {"word": "سريع", "opposite": "بطيء"},
            {"word": "ساخن", "opposite": "بارد"},
            {"word": "جديد", "opposite": "قديم"},
            {"word": "سهل", "opposite": "صعب"},
            {"word": "قوي", "opposite": "ضعيف"},
            {"word": "ثقيل", "opposite": "خفيف"},
            {"word": "جميل", "opposite": "قبيح"},
            {"word": "سعيد", "opposite": "حزين"},
            {"word": "نظيف", "opposite": "وسخ"},
            {"word": "فاتح", "opposite": "غامق"},
            {"word": "ممتلئ", "opposite": "فارغ"},
            {"word": "هادئ", "opposite": "صاخب"},
            {"word": "غالي", "opposite": "رخيص"},
            {"word": "قريب", "opposite": "بعيد"},
            {"word": "مشرق", "opposite": "مظلم"},
            {"word": "سليم", "opposite": "مريض"},
            {"word": "صادق", "opposite": "كاذب"},
            {"word": "مشغول", "opposite": "فارغ"}
        ]
        random.shuffle(self.default_opposites)

    def start_game(self):
        self.current_question = 0
        self.game_active = True
        return self.get_question()

    def generate_question(self):
        """توليد سؤال باستخدام AI أو fallback للقائمة المبدئية"""
        if self.use_ai and self.ai_generate_question:
            q = self.ai_generate_question()
            if q and 'word' in q and 'opposite' in q:
                return q
        return self.default_opposites[self.current_question % len(self.default_opposites)]

    def get_question(self):
        q_data = self.generate_question()
        self.current_word = q_data['word']
        self.current_answer = q_data['opposite']
        self.found_words.clear()

        flex_content = {
            "type": "bubble",
            "size": "kilo",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "↔️ لعبة ضد الكلمة", "size": "lg", "weight": "bold", "align": "center", "color": "#FFFFFF"},
                    {"type": "text", "text": f"سؤال {self.current_question + 1} من {self.questions_count}", "size": "xs", "align": "center", "color": "#E0E0E0"}
                ],
                "backgroundColor": "#667EEA",
                "paddingAll": "15px"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": f"📝 ما هو ضد:\n『 {self.current_word} 』", "size": "md", "weight": "bold", "align": "center"},
                    {"type": "text", "text": "💡 اكتب 'لمح' للحصول على تلميح أو 'جاوب' للكشف عن الإجابة", "size": "xs", "align": "center", "color": "#7F8C8D"},
                ],
                "paddingAll": "15px",
                "backgroundColor": "#F1F5F9",
                "cornerRadius": "15px",
                "margin": "md"
            }
        }

        return FlexSendMessage(alt_text="لعبة ضد الكلمة", contents=flex_content)

    def check_answer(self, user_answer, user_id, display_name):
        if not self.game_active:
            return None

        answer = user_answer.strip()

        # تلميح
        if answer == 'لمح':
            hint = f"💡 تلميح: الإجابة تبدأ بـ '{self.current_answer[0]}'"
            return {'message': hint, 'response': TextSendMessage(text=hint), 'points': 0}

        # كشف الإجابة
        if answer in ['جاوب', 'تم', 'التالي']:
            reveal = f"📝 الإجابة الصحيحة: {self.current_answer}"
            return self._next_question(msg=reveal)

        normalized = self.normalize_text(answer)
        correct_normalized = self.normalize_text(self.current_answer)

        # التحقق من الإجابة باستخدام AI أو التشابه
        is_correct = False
        if normalized == correct_normalized:
            is_correct = True
        elif self.ai_check_answer and self.ai_check_answer(self.current_answer, answer):
            is_correct = True
        else:
            # تشابه جزئي بنسبة > 80%
            ratio = difflib.SequenceMatcher(None, normalized, correct_normalized).ratio()
            if ratio > 0.8:
                is_correct = True

        if not is_correct:
            return {'message': "▫️ إجابة غير صحيحة ▪️",
                    'response': TextSendMessage(text="▫️ إجابة غير صحيحة ▪️"),
                    'points': 0}

        points = self.add_score(user_id, display_name, 10)
        msg = f"✅ صحيح يا {display_name}!\n+{points} نقطة"
        return self._next_question(points=points, msg=msg)

    def _next_question(self, points=0, msg=""):
        self.current_question += 1
        if self.current_question >= self.questions_count:
            self.game_active = False
            final_msg = f"{msg}\n\n🏁 انتهت اللعبة!" if msg else "🏁 انتهت اللعبة!"
            return {'message': final_msg, 'response': TextSendMessage(text=final_msg),
                    'game_over': True, 'points': points}
        next_q = self.get_question()
        return {'message': msg, 'response': next_q, 'points': points}
