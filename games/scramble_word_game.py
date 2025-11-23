from linebot.models import TextSendMessage, FlexSendMessage
from .base_game import BaseGame
import random
import difflib

class ScrambleWordGameAI(BaseGame):
    """لعبة ترتيب الحروف - نسخة AI"""
    
    def __init__(self, line_bot_api, questions_count=10, use_ai=False, ai_generate_word=None, ai_check_answer=None):
        """
        ai_generate_word: دالة تولد {'word': 'كلمة', 'hint': 'تلميح'}
        ai_check_answer: دالة تتحقق من صحة الإجابة (تشابه أو أخطاء إملائية)
        """
        super().__init__(line_bot_api, questions_count)
        self.use_ai = use_ai
        self.ai_generate_word = ai_generate_word
        self.ai_check_answer = ai_check_answer
        self.found_words = set()
        
        # كلمات مبدئية
        self.words_list = [
            {"word": "مدرسة", "hint": "مكان للتعليم"},
            {"word": "كتاب", "hint": "نقرأ فيه"},
            {"word": "حاسوب", "hint": "جهاز إلكتروني"},
            {"word": "هاتف", "hint": "نستخدمه للاتصال"},
            {"word": "مطبخ", "hint": "نطبخ فيه"},
            {"word": "سيارة", "hint": "وسيلة مواصلات"},
            {"word": "طائرة", "hint": "تطير في السماء"},
            {"word": "حديقة", "hint": "مكان فيه أشجار وزهور"},
            {"word": "مستشفى", "hint": "نذهب إليه عند المرض"},
            {"word": "مكتبة", "hint": "مكان للكتب"},
            {"word": "قلم", "hint": "نكتب به"},
            {"word": "دفتر", "hint": "نكتب عليه"},
            {"word": "معلم", "hint": "يعلم الطلاب"},
            {"word": "طالب", "hint": "يدرس في المدرسة"},
            {"word": "طبيب", "hint": "يعالج المرضى"},
            {"word": "شرطي", "hint": "يحمي الأمن"},
            {"word": "مهندس", "hint": "يصمم المباني"},
            {"word": "محامي", "hint": "يدافع عن الحقوق"},
            {"word": "صحفي", "hint": "يكتب الأخبار"},
            {"word": "رياضي", "hint": "يمارس الرياضة"}
        ]
        random.shuffle(self.words_list)

    def start_game(self):
        self.current_question = 0
        self.game_active = True
        return self.get_question()

    def generate_word(self):
        """توليد كلمة جديدة باستخدام AI أو fallback للقائمة المبدئية"""
        if self.use_ai and self.ai_generate_word:
            w = self.ai_generate_word()
            if w and 'word' in w and 'hint' in w:
                return w
        return self.words_list[self.current_question % len(self.words_list)]

    def scramble_word(self, word):
        letters = list(word)
        scrambled = letters.copy()
        attempts = 10
        while scrambled == letters and attempts > 0:
            random.shuffle(scrambled)
            attempts -= 1
        return ''.join(scrambled)

    def get_question(self):
        word_data = self.generate_word()
        self.current_answer = word_data['word']
        self.current_hint = word_data['hint']
        scrambled = self.scramble_word(self.current_answer)

        flex_content = {
            "type": "bubble",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "🔤 لعبة ترتيب الحروف", "size": "lg", "weight": "bold", "align": "center", "color": "#FFFFFF"},
                    {"type": "text", "text": f"سؤال {self.current_question + 1} من {self.questions_count}", "size": "xs", "align": "center", "color": "#E0E0E0"}
                ],
                "backgroundColor": "#667EEA",
                "paddingAll": "15px"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": f"الحروف: {' - '.join(scrambled)}", "size": "md", "weight": "bold", "align": "center"},
                    {"type": "text", "text": "💡 اكتب 'لمح' للحصول على تلميح أو 'جاوب' للكشف عن الإجابة", "size": "xs", "align": "center", "color": "#7F8C8D"}
                ],
                "paddingAll": "15px",
                "backgroundColor": "#F1F5F9",
                "cornerRadius": "15px",
                "margin": "md"
            }
        }

        return FlexSendMessage(alt_text="لعبة ترتيب الحروف", contents=flex_content)

    def check_answer(self, user_answer, user_id, display_name):
        if not self.game_active:
            return None

        answer = user_answer.strip()

        if answer == 'لمح':
            hint = f"💡 تلميح: {self.current_hint}"
            return {'message': hint, 'response': TextSendMessage(text=hint), 'points': 0}

        if answer in ['جاوب', 'تم', 'التالي']:
            reveal = f"📝 الإجابة الصحيحة: {self.current_answer}"
            return self._next_question(msg=reveal)

        normalized = self.normalize_text(answer)
        correct_normalized = self.normalize_text(self.current_answer)

        is_correct = False
        if normalized == correct_normalized:
            is_correct = True
        elif self.ai_check_answer and self.ai_check_answer(self.current_answer, answer):
            is_correct = True
        else:
            if difflib.SequenceMatcher(None, normalized, correct_normalized).ratio() > 0.8:
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
