"""
لعبة ترتيب الحروف - نسخة محدثة ومحسّنة
Created by: Abeer Aldosari © 2025

تحديثات:
- استيراد صحيح من games.base_game
- نظام تلميحات وكشف إجابات محسّن
- دعم ثيمات ديناميكية
- رسائل Flex حديثة بتصميم Neumorphism
"""

# ============================================================================
# الاستيراد الصحيح
# ============================================================================
from games.base_game import BaseGame  # ✅ صحيح

import random
import difflib
from typing import Dict, Any, Optional


class ScrambleWordGame(BaseGame):
    """
    لعبة ترتيب الحروف
    
    الميزات:
    - قاعدة بيانات موسّعة من الكلمات
    - نظام تلميحات ذكي
    - تتبع النقاط والإحصائيات
    - رسائل Flex حديثة بتصميم Neumorphism
    - دعم 6 ثيمات مختلفة
    """
    
    def __init__(self, line_bot_api):
        """
        تهيئة اللعبة
        
        المعاملات:
            line_bot_api: واجهة LINE Bot API
        """
        # استدعاء الكلاس الأساسي
        super().__init__(line_bot_api, questions_count=5)
        
        # تفعيل ميزات التلميح والكشف
        self.supports_hint = True
        self.supports_reveal = True
        
        # قاعدة بيانات الكلمات
        self.words_list = [
            {"word": "مدرسة", "hint": "مكان للتعليم"},
            {"word": "كتاب", "hint": "نقرأ فيه"},
            {"word": "حاسوب", "hint": "جهاز إلكتروني"},
            {"word": "هاتف", "hint": "نستخدمه للاتصال"},
            {"word": "مطبخ", "hint": "نطبخ فيه"},
            {"word": "سيارة", "hint": "وسيلة مواصلات"},
            {"word": "طائرة", "hint": "تطير في السماء"},
            {"word": "حديقة", "hint": "مكان فيه أشجار"},
            {"word": "مستشفى", "hint": "نذهب إليه عند المرض"},
            {"word": "مكتبة", "hint": "مكان للكتب"},
            {"word": "مطار", "hint": "تُقلع منه الطائرات"},
            {"word": "جامعة", "hint": "للتعليم العالي"},
            {"word": "صيدلية", "hint": "نشتري منها الدواء"},
            {"word": "مسجد", "hint": "بيت من بيوت الله"},
            {"word": "ملعب", "hint": "نلعب فيه كرة القدم"}
        ]
        random.shuffle(self.words_list)
        
        self.current_hint = None
        self.scrambled_word = None

    def scramble_word(self, word: str) -> str:
        """
        خلط حروف الكلمة
        
        المعاملات:
            word: الكلمة المراد خلطها
            
        العودة:
            str: الكلمة المخلوطة
        """
        letters = list(word)
        scrambled = letters.copy()
        attempts = 20
        
        while scrambled == letters and attempts > 0:
            random.shuffle(scrambled)
            attempts -= 1
        
        return ''.join(scrambled)

    def start_game(self) -> Any:
        """
        بدء اللعبة وإرجاع أول سؤال
        
        العودة:
            FlexMessage: السؤال الأول
        """
        self.current_question = 0
        self.game_active = True
        return self.get_question()

    def get_question(self) -> Any:
        """
        إنشاء وإرجاع رسالة Flex للسؤال
        
        العودة:
            FlexMessage: السؤال بتصميم Neumorphism
        """
        # اختيار كلمة
        word_data = self.words_list[self.current_question % len(self.words_list)]
        self.current_answer = word_data['word']
        self.current_hint = word_data['hint']
        self.scrambled_word = self.scramble_word(self.current_answer)
        
        # الحصول على ألوان الثيم الحالي
        colors = self.get_theme_colors()
        
        # تنسيق الحروف المخلوطة
        formatted_letters = ' - '.join(self.scrambled_word)
        
        # بناء محتوى Flex Message
        flex_content = {
            "type": "bubble",
            "size": "kilo",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "🔤 ترتيب الحروف",
                        "size": "xl",
                        "weight": "bold",
                        "color": colors["text"],
                        "align": "center"
                    },
                    {
                        "type": "text",
                        "text": f"سؤال {self.current_question + 1} من {self.questions_count}",
                        "size": "sm",
                        "color": colors["text2"],
                        "align": "center",
                        "margin": "sm"
                    }
                ],
                "backgroundColor": colors["bg"],
                "paddingAll": "20px"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "رتب الحروف لتكوين كلمة:",
                        "size": "md",
                        "color": colors["text"],
                        "align": "center",
                        "margin": "md"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": formatted_letters,
                                "size": "xxl",
                                "color": colors["primary"],
                                "align": "center",
                                "wrap": True,
                                "weight": "bold"
                            }
                        ],
                        "backgroundColor": colors["card"],
                        "cornerRadius": "20px",
                        "paddingAll": "25px",
                        "margin": "lg"
                    },
                    {
                        "type": "text",
                        "text": f"🔢 {len(self.current_answer)} حروف",
                        "size": "sm",
                        "color": colors["text2"],
                        "align": "center",
                        "margin": "md"
                    },
                    {
                        "type": "separator",
                        "margin": "lg"
                    },
                    {
                        "type": "text",
                        "text": "💡 اكتب 'لمح' للتلميح\n📝 اكتب 'جاوب' للكشف عن الإجابة",
                        "size": "xs",
                        "color": colors["text2"],
                        "align": "center",
                        "margin": "md",
                        "wrap": True
                    }
                ],
                "backgroundColor": colors["bg"],
                "paddingAll": "15px"
            },
            "styles": {
                "body": {
                    "backgroundColor": colors["bg"]
                }
            }
        }
        
        return self._create_flex_with_buttons("ترتيب الحروف", flex_content)

    def get_hint(self) -> str:
        """
        الحصول على تلميح للسؤال الحالي
        
        العودة:
            str: التلميح
        """
        if not self.current_hint:
            return "💡 لا يوجد تلميح متاح"
        
        hint_text = f"💡 {self.current_hint}"
        
        # إضافة تلميح عن أول حرف
        if self.current_answer:
            hint_text += f"\n🔤 الكلمة تبدأ بحرف '{self.current_answer[0]}'"
        
        return hint_text

    def check_answer(self, user_answer: str, user_id: str, display_name: str) -> Optional[Dict[str, Any]]:
        """
        التحقق من إجابة اللاعب
        
        المعاملات:
            user_answer: إجابة المستخدم
            user_id: معرف المستخدم
            display_name: اسم المستخدم
            
        العودة:
            dict: نتيجة الإجابة أو None إذا كانت خاطئة
        """
        # التحقق من حالة اللعبة
        if not self.game_active:
            return None

        # تنظيم الإجابة
        normalized_answer = self.normalize_text(user_answer)

        # ===== معالجة أمر التلميح =====
        if normalized_answer == "لمح":
            hint = self.get_hint()
            return {
                "message": hint,
                "response": self._create_text_message(hint),
                "points": 0
            }

        # ===== معالجة أمر كشف الإجابة =====
        if normalized_answer == "جاوب":
            reveal = self.reveal_answer()
            next_question = self.next_question()
            
            if isinstance(next_question, dict) and next_question.get('game_over'):
                next_question['message'] = f"{reveal}\n\n{next_question.get('message','')}"
                return next_question
            
            return {
                'message': reveal,
                'response': next_question,
                'points': 0
            }

        # ===== التحقق من صحة الإجابة =====
        normalized_correct = self.normalize_text(self.current_answer)
        is_valid = False

        # 1. مطابقة تامة
        if normalized_answer == normalized_correct:
            is_valid = True
        
        # 2. مطابقة جزئية (80% تشابه)
        elif difflib.SequenceMatcher(None, normalized_answer, normalized_correct).ratio() > 0.8:
            is_valid = True

        # إجابة خاطئة
        if not is_valid:
            return {
                "message": "▫️ إجابة غير صحيحة ▪️",
                "response": self._create_text_message("▫️ إجابة غير صحيحة ▪️"),
                "points": 0
            }

        # ===== إجابة صحيحة =====
        points = self.add_score(user_id, display_name, 10)
        
        # الانتقال للسؤال التالي
        next_question = self.next_question()
        
        # التحقق من انتهاء اللعبة
        if isinstance(next_question, dict) and next_question.get('game_over'):
            next_question['points'] = points
            return next_question
        
        # رسالة النجاح
        success_message = f"✅ إجابة صحيحة يا {display_name}!\n📝 الكلمة: {self.current_answer}\n+{points} نقطة"
        
        return {
            "message": success_message,
            "response": next_question,
            "points": points
        }

    def get_game_info(self) -> Dict[str, Any]:
        """
        الحصول على معلومات اللعبة
        
        العودة:
            dict: معلومات اللعبة
        """
        return {
            "name": "لعبة ترتيب الحروف",
            "emoji": "🔤",
            "description": "رتب الحروف لتكوين كلمة",
            "questions_count": self.questions_count,
            "words_count": len(self.words_list),
            "supports_hint": self.supports_hint,
            "supports_reveal": self.supports_reveal,
            "active": self.game_active,
            "current_question": self.current_question,
            "players_count": len(self.scores)
        }


# ============================================================================
# مثال على الاستخدام
# ============================================================================
if __name__ == "__main__":
    """
    مثال على كيفية استخدام اللعبة
    """
    print("✅ ملف لعبة ترتيب الحروف جاهز للاستخدام!")
    print("📝 تأكد من استخدام: from games.base_game import BaseGame")
