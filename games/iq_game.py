"""
لعبة أسئلة الذكاء - نسخة محسّنة AI ▫️▪️
"""
from linebot.models import TextSendMessage
from .base_game import BaseGame
import random
import difflib

class IqGame(BaseGame):
    """لعبة أسئلة الذكاء المحسّنة AI ▫️▪️"""
    
    def __init__(self, line_bot_api, ai_generate_question=None, ai_check_answer=None):
        """
        ai_generate_question: دالة تولد سؤال جديد، يجب أن ترجع dict {q: "", a: "", hint: ""}
        ai_check_answer: دالة تتحقق من الإجابة، ترجع True إذا الإجابة صحيحة أو مقاربة
        """
        super().__init__(line_bot_api, questions_count=5)
        self.ai_generate_question = ai_generate_question
        self.ai_check_answer = ai_check_answer
        
        # قائمة أسئلة أولية (يمكن للـ AI توليد المزيد لاحقًا)
        self.questions = [
            {"q": "ما هو الشيء الذي يمشي بلا أرجل ويبكي بلا عيون؟", "a": "السحاب", "hint": "▫️ يُرى في السماء ويجلب المطر ▪️"},
            {"q": "ما هو الشيء الذي له رأس ولا يملك عيون؟", "a": "الدبوس", "hint": "▫️ أداة صغيرة للتثبيت ▪️"},
            {"q": "شيء موجود في السماء إذا أضفت له حرفاً أصبح في الأرض؟", "a": "نجم", "hint": "▫️ يضيء ليلاً ▪️"},
        ]
        random.shuffle(self.questions)

    def start_game(self):
        self.current_question = 0
        self.game_active = True
        return self.get_question()

    def generate_question(self):
        """توليد سؤال جديد باستخدام AI إذا موجود"""
        if self.ai_generate_question:
            new_q = self.ai_generate_question()
            if new_q and "q" in new_q and "a" in new_q:
                return new_q
        # fallback إذا لم يكن AI متاحًا
        return random.choice(self.questions)

    def get_question(self):
        q_data = self.generate_question()
        self.current_answer = q_data["a"]
        self._current_hint = q_data.get("hint", f"▫️ الإجابة تبدأ بـ '{self.current_answer[0]}' ▪️")
        message = f"▫️ سؤال ذكاء ({self.current_question + 1}/{self.questions_count}) ▪️\n\n"
        message += f"▫️ {q_data['q']} ▪️\n\n"
        message += "▫️ اكتب الإجابة أو:\n▫️ لمح - للحصول على تلميح\n▫️ جاوب - لمعرفة الإجابة ▪️"
        return TextSendMessage(text=message)

    def get_hint(self):
        return self._current_hint

    def reveal_answer(self):
        return f"▫️ الإجابة الصحيحة: {self.current_answer} ▪️"

    def check_answer(self, user_answer, user_id, display_name):
        if not self.game_active:
            return None

        normalized_answer = self.normalize_text(user_answer)

        if normalized_answer == "لمح":
            hint = self.get_hint()
            return {"message": hint, "response": TextSendMessage(text=hint), "points": 0}

        if normalized_answer == "جاوب":
            reveal = self.reveal_answer()
            next_q = self.next_question()
            message = f"{reveal}\n\n" + (next_q.text if hasattr(next_q, 'text') else "")
            return {"message": message, "response": TextSendMessage(text=message), "points": 0}

        # تحقق من الإجابة
        normalized_correct = self.normalize_text(self.current_answer)
        valid = False

        # 1- إذا الإجابة مطابقة تمامًا بعد التطبيع
        if normalized_answer == normalized_correct:
            valid = True
        # 2- إذا الإجابة مشابهة تقريبًا (تصحيح أخطاء صغيرة)
        elif difflib.SequenceMatcher(None, normalized_answer, normalized_correct).ratio() > 0.8:
            valid = True
        # 3- التحقق باستخدام AI إذا موجود
        elif self.ai_check_answer:
            valid = self.ai_check_answer(self.current_answer, user_answer)

        if not valid:
            return {"message": "▫️ إجابة غير صحيحة ▪️", "response": TextSendMessage(text="▫️ إجابة غير صحيحة ▪️"), "points": 0}

        points = self.add_score(user_id, display_name, 10)
        next_q = self.next_question()
        message = f"✅ إجابة صحيحة يا {display_name} ▪️\n+{points} نقطة\n\n"
        if hasattr(next_q, 'text'):
            message += next_q.text
        return {"message": message, "response": TextSendMessage(text=message), "points": points}
