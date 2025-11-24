"""
لعبة ضد الكلمة - نسخة محدثة ومحسّنة
Created by: Abeer Aldosari © 2025

تحديثات:
- استيراد صحيح من games.base_game
- قاعدة بيانات موسّعة من الأضداد
- نظام تلميحات محسّن
- دعم AI اختياري
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


class OppositeGame(BaseGame):
    """
    لعبة ضد الكلمة - أوجد عكس الكلمة
    
    الميزات:
    - قاعدة بيانات موسّعة (20+ كلمة)
    - دعم AI اختياري
    - نظام تلميحات ذكي
    - تتبع النقاط والإحصائيات
    - رسائل Flex حديثة بتصميم Neumorphism
    - دعم 6 ثيمات مختلفة
    """
    
    def __init__(self, line_bot_api, use_ai=False, ai_generate_question=None, ai_check_answer=None):
        """
        تهيئة اللعبة
        
        المعاملات:
            line_bot_api: واجهة LINE Bot API
            use_ai: استخدام AI (اختياري)
            ai_generate_question: دالة توليد أسئلة بالـ AI
            ai_check_answer: دالة التحقق من الإجابات بالـ AI
        """
        # استدعاء الكلاس الأساسي
        super().__init__(line_bot_api, questions_count=5)
        
        # إعدادات AI
        self.use_ai = use_ai
        self.ai_generate_question = ai_generate_question
        self.ai_check_answer = ai_check_answer
        
        # تفعيل ميزات التلميح والكشف
        self.supports_hint = True
        self.supports_reveal = True
        
        # قاعدة بيانات الأضداد (موسّعة)
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
            {"word": "مشغول", "opposite": "فارغ"},
            {"word": "صاعد", "opposite": "نازل"},
            {"word": "داخل", "opposite": "خارج"},
            {"word": "أعلى", "opposite": "أسفل"},
            {"word": "يمين", "opposite": "يسار"},
            {"word": "نهار", "opposite": "ليل"}
        ]
        
        random.shuffle(self.default_opposites)
        
        self.current_word = None

    def start_game(self) -> Any:
        """
        بدء اللعبة وإرجاع أول سؤال
        
        العودة:
            FlexMessage: السؤال الأول
        """
        self.current_question = 0
        self.game_active = True
        return self.get_question()

    def generate_question(self) -> Dict[str, str]:
        """
        توليد سؤال (باستخدام AI أو القائمة الافتراضية)
        
        العودة:
            dict: سؤال وإجابة {"word": "...", "opposite": "..."}
        """
        # محاولة استخدام AI أولاً
        if self.use_ai and self.ai_generate_question:
            try:
                new_question = self.ai_generate_question()
                if new_question and 'word' in new_question and 'opposite' in new_question:
                    return new_question
            except Exception:
                pass  # Fallback للقائمة الافتراضية
        
        # استخدام القائمة الافتراضية
        return self.default_opposites[self.current_question % len(self.default_opposites)]

    def get_question(self) -> Any:
        """
        إنشاء وإرجاع رسالة Flex للسؤال
        
        العودة:
            FlexMessage: السؤال بتصميم Neumorphism
        """
        # توليد السؤال
        q_data = self.generate_question()
        self.current_word = q_data['word']
        self.current_answer = q_data['opposite']
        
        # الحصول على ألوان الثيم الحالي
        colors = self.get_theme_colors()
        
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
                        "text": "↔️ ضد الكلمة",
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
                        "text": "ما هو ضد:",
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
                                "text": f"『 {self.current_word} 』",
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
                        "text": "🤔 فكر في العكس...",
                        "size": "sm",
                        "color": colors["text2"],
                        "align": "center",
                        "margin": "lg"
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
        
        return self._create_flex_with_buttons("ضد الكلمة", flex_content)

    def get_hint(self) -> str:
        """
        الحصول على تلميح للسؤال الحالي
        
        العودة:
            str: التلميح
        """
        if not self.current_answer:
            return "💡 لا يوجد تلميح متاح"
        
        first_char = self.current_answer[0]
        length = len(self.current_answer)
        
        hint = f"💡 تلميح: الإجابة تبدأ بـ '{first_char}'"
        hint += f"\n🔢 عدد الحروف: {length}"
        
        return hint

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
            reveal = f"📝 الإجابة الصحيحة: {self.current_answer}"
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
        
        # 2. استخدام AI للتحقق (إن توفر)
        elif self.use_ai and self.ai_check_answer:
            try:
                is_valid = self.ai_check_answer(self.current_answer, user_answer)
            except Exception:
                pass
        
        # 3. مطابقة جزئية (80% تشابه)
        if not is_valid:
            ratio = difflib.SequenceMatcher(None, normalized_answer, normalized_correct).ratio()
            if ratio > 0.8:
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
        success_message = f"✅ صحيح يا {display_name}!\n📝 {self.current_word} ↔️ {self.current_answer}\n+{points} نقطة"
        
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
            "name": "لعبة ضد الكلمة",
            "emoji": "↔️",
            "description": "أوجد عكس الكلمة",
            "questions_count": self.questions_count,
            "words_count": len(self.default_opposites),
            "supports_ai": self.use_ai,
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
    print("✅ ملف لعبة ضد الكلمة جاهز للاستخدام!")
    print("📝 تأكد من استخدام: from games.base_game import BaseGame")
