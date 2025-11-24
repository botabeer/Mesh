"""
لعبة تكوين الكلمات - نسخة AI ▫️▪️
Created by: Abeer Aldosari © 2025

تحديثات:
- Flex Message Neumorphism
- دعم ثيمات ديناميكية
- تتبع النقاط لكل لاعب
- دعم AI لتوليد الكلمات والتحقق من الإجابة
"""

from games.base_game import BaseGame
import random
import difflib
from typing import Dict, Any, Optional

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
        
        self.letter_sets = [
            {"letters": ["ق", "ل", "م", "ع", "ر", "ب"], "words": ["قلم", "عمل", "علم", "قلب", "رقم", "مقر"]},
            {"letters": ["س", "ا", "ر", "ة", "ي", "م"], "words": ["سيارة", "سارية", "رئيس", "سير", "مسار"]},
        ]
        random.shuffle(self.letter_sets)
        self.current_set = None
        self.current_answer = []
        self.found_words = set()
        self.required_words = 3

    def generate_letters_set(self):
        """توليد مجموعة حروف وكلمات باستخدام AI إذا متاح"""
        if self.use_ai and self.ai_generate_words:
            new_set = self.ai_generate_words()
            if new_set and "letters" in new_set and "words" in new_set:
                return new_set
        return random.choice(self.letter_sets)

    def get_question(self) -> Any:
        """إنشاء Flex Message للسؤال الحالي"""
        colors = self.get_theme_colors()
        self.current_set = self.generate_letters_set()
        self.current_answer = self.current_set["words"]
        self.found_words.clear()
        
        letters_display = ' - '.join(self.current_set["letters"])
        
        flex_content = {
            "type": "bubble",
            "size": "kilo",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "📝 تكوين الكلمات", "size": "xl", "weight": "bold",
                     "color": colors["text"], "align": "center"},
                    {"type": "text", "text": f"سؤال {self.current_question+1} من {self.questions_count}",
                     "size": "sm", "color": colors["text2"], "align": "center", "margin": "xs"}
                ],
                "backgroundColor": colors["bg"],
                "paddingAll": "20px"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "🔤 استخدم الحروف التالية لتكوين الكلمات:", "size": "md",
                     "color": colors["text"], "align": "center", "margin": "md"},
                    {"type": "text", "text": letters_display, "size": "xxl", "weight": "bold",
                     "color": colors["primary"], "align": "center", "margin": "md"},
                    {"type": "text", "text": f"⚠️ يجب إيجاد {self.required_words} كلمات", "size": "sm",
                     "color": colors["text2"], "align": "center", "margin": "md"},
                    {"type": "text", "text": "💡 اكتب 'لمح' للتلميح، 'جاوب' للكشف عن الإجابات", "size": "xs",
                     "color": colors["text2"], "align": "center", "margin": "md", "wrap": True}
                ],
                "backgroundColor": colors["bg"],
                "paddingAll": "15px"
            },
            "styles": {"body": {"backgroundColor": colors["bg"]}}
        }
        return self._create_flex_with_buttons("تكوين الكلمات", flex_content)

    def check_answer(self, user_answer: str, user_id: str, display_name: str) -> Optional[Dict[str, Any]]:
        if not self.game_active:
            return None

        answer = user_answer.strip()

        # معالجة التلميح
        if answer == 'لمح':
            remaining = [w for w in self.current_answer if self.normalize_text(w) not in self.found_words]
            if remaining:
                word = remaining[0]
                hint = f"💡 الكلمة من {len(word)} حروف وأولها '{word[0]}'"
            else:
                hint = "لا توجد تلميحات"
            return {'message': hint, 'response': self._create_text_message(hint), 'points': 0}

        # معالجة كشف الإجابة
        if answer in ['جاوب', 'تم', 'التالي']:
            words = " • ".join(self.current_answer)
            msg = f"📝 الكلمات الممكنة:\n{words}"
            return self._next_question(msg=msg)

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
                    'response': self._create_text_message(f"▫️ إجابة غير صحيحة ▪️"),
                    'points': 0}

        self.found_words.add(normalized)
        points = self.add_score(user_id, display_name, 10)

        if len(self.found_words) >= self.required_words:
            return self._next_question(points=points, msg=f"🎉 أحسنت يا {display_name}!\n+{points} نقطة")

        remaining = self.required_words - len(self.found_words)
        msg = f"✅ صحيح!\n+{points} نقطة\n⏳ تبقى {remaining} كلمات"
        return {'message': msg, 'response': self._create_text_message(msg), 'points': points}

    def _next_question(self, points=0, msg=""):
        self.current_question += 1
        if self.current_question >= self.questions_count:
            self.game_active = False
            final_msg = f"{msg}\n\n🏁 انتهت اللعبة!" if msg else "🏁 انتهت اللعبة!"
            return {'message': final_msg, 'response': self._create_text_message(final_msg),
                    'game_over': True, 'points': points}
        next_q = self.get_question()
        return {'message': msg, 'response': next_q, 'points': points}

    def get_game_info(self) -> Dict[str, Any]:
        return {
            "name": "لعبة تكوين الكلمات",
            "emoji": "▫️▪️",
            "description": "كوّن كلمات من الحروف المعطاة",
            "questions_count": self.questions_count,
            "required_words": self.required_words,
            "found_words_count": len(self.found_words),
            "active": self.game_active,
            "current_question": self.current_question,
            "players_count": len(self.scores)
        }

# ============================================================================
# مثال على الاستخدام
# ============================================================================
if __name__ == "__main__":
    print("✅ ملف لعبة تكوين الكلمات جاهز للاستخدام!")
    print("📝 تأكد من استخدام: from games.base_game import BaseGame")
