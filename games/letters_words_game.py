"""
لعبة تكوين الكلمات - نسخة AI ▫️▪️
"""
from linebot.models import TextSendMessage, FlexSendMessage
from .base_game import BaseGame
import random
import difflib

class LettersWordsGame(BaseGame):
    """لعبة تكوين كلمات من حروف معينة - AI Version"""
    
    def __init__(self, line_bot_api, use_ai=False, ai_generate_words=None, ai_check_answer=None):
        """
        ai_generate_words: دالة تولد مجموعة كلمات جديدة من الحروف، ترجع dict {"letters": [], "words": []}
        ai_check_answer: دالة تتحقق من صحة الإجابة (مقاربة أو خطأ إملائي)
        """
        super().__init__(line_bot_api, questions_count=5)
        self.use_ai = use_ai
        self.ai_generate_words = ai_generate_words
        self.ai_check_answer = ai_check_answer
        
        # مجموعات الحروف والكلمات المبدئية
        self.letter_sets = [
            {"letters": ["ق", "ل", "م", "ع", "ر", "ب"], "words": ["قلم", "عمل", "علم", "قلب", "رقم", "مقر"]},
            {"letters": ["س", "ا", "ر", "ة", "ي", "م"], "words": ["سيارة", "سارية", "رئيس", "سير", "مسار"]},
        ]
        random.shuffle(self.letter_sets)
        self.found_words = set()
        self.required_words = 3
        self.theme = "white"

    def set_theme(self, theme_name: str):
        self.theme = theme_name

    def generate_letters_set(self):
        """توليد مجموعة حروف وكلمات باستخدام AI إذا متاح"""
        if self.use_ai and self.ai_generate_words:
            new_set = self.ai_generate_words()
            if new_set and "letters" in new_set and "words" in new_set:
                return new_set
        # fallback على المجموعات المبدئية
        return random.choice(self.letter_sets)

    def get_question(self):
        self.current_set = self.generate_letters_set()
        self.current_answer = self.current_set["words"]
        self.found_words.clear()
        # بناء FlexMessage كما في النسخة الأصلية
        # ... (نفس الكود السابق لبناء FlexSendMessage)
        return FlexSendMessage(alt_text="لعبة تكوين الكلمات", contents={})  # ضع هنا flex_content

    def check_answer(self, user_answer, user_id, display_name):
        if not self.game_active:
            return None

        answer = user_answer.strip()

        # تلميح
        if answer == 'لمح':
            remaining = [w for w in self.current_answer if self.normalize_text(w) not in self.found_words]
            if remaining:
                word = remaining[0]
                hint = f"💡 الكلمة من {len(word)} حروف وأولها '{word[0]}'"
            else:
                hint = "لا توجد تلميحات"
            return {'message': hint, 'response': TextSendMessage(text=hint), 'points': 0}

        # الحل
        if answer in ['جاوب', 'تم', 'التالي']:
            if len(self.found_words) >= self.required_words or answer == 'جاوب':
                words = " • ".join(self.current_answer[:5])
                msg = f"📝 الكلمات الممكنة:\n{words}"
                return self._next_question(msg=msg)
            else:
                remaining = self.required_words - len(self.found_words)
                return {'message': f"❌ تبقى {remaining} كلمات",
                        'response': TextSendMessage(text=f"❌ تبقى {remaining} كلمات"), 'points': 0}

        normalized = self.normalize_text(answer)
        valid_words = [self.normalize_text(w) for w in self.current_answer]

        # تحقق باستخدام AI أو التشابه
        is_valid = False
        if normalized in valid_words and normalized not in self.found_words:
            is_valid = True
        elif self.ai_check_answer:
            for w in self.current_answer:
                if self.ai_check_answer(w, answer):
                    is_valid = True
                    break
        else:
            for w in valid_words:
                if difflib.SequenceMatcher(None, normalized, w).ratio() > 0.8:
                    is_valid = True
                    break

        if not is_valid:
            return {'message': f"▫️ إجابة غير صحيحة ▪️",
                    'response': TextSendMessage(text=f"▫️ إجابة غير صحيحة ▪️"),
                    'points': 0}

        self.found_words.add(normalized)
        points = self.add_score(user_id, display_name, 10)
        if len(self.found_words) >= self.required_words:
            return self._next_question(points=points, msg=f"🎉 أحسنت يا {display_name}!\n+{points} نقطة")
        remaining = self.required_words - len(self.found_words)
        msg = f"✅ صحيح!\n+{points} نقطة\n\n⏳ تبقى {remaining} كلمات"
        return {'message': msg, 'response': TextSendMessage(text=msg), 'points': points}

    def _next_question(self, points=0, msg=""):
        self.current_question += 1
        if self.current_question >= self.questions_count:
            self.game_active = False
            final_msg = f"{msg}\n\n🏁 انتهت اللعبة!" if msg else "🏁 انتهت اللعبة!"
            return {'message': final_msg, 'response': TextSendMessage(text=final_msg),
                    'game_over': True, 'points': points}
        next_q = self.get_question()
        return {'message': msg, 'response': next_q, 'points': points}
