"""
لعبة أسئلة الذكاء - نسخة محدثة ومحسّنة
Created by: Abeer Aldosari © 2025

هذا مثال كامل لملف لعبة محدث مع جميع الإصلاحات المطبقة
"""

# ============================================================================
# الاستيراد الصحيح - استخدم هذا في جميع ملفات الألعاب
# ============================================================================
from games.base_game import BaseGame  # ✅ صحيح
# from .base_game import BaseGame      # ❌ خطأ - لا تستخدم هذا

import random
import difflib
from typing import Dict, Any, Optional


class IqGame(BaseGame):
    """
    لعبة أسئلة الذكاء مع دعم AI وثيمات ديناميكية
    
    الميزات:
    - دعم اختياري للـ AI (Gemini)
    - 6 ثيمات مختلفة
    - نظام تلميحات وكشف إجابات
    - تتبع النقاط والإحصائيات
    - رسائل Flex حديثة بتصميم Neumorphism
    """
    
    def __init__(self, line_bot_api, ai_generate_question=None, ai_check_answer=None):
        """
        تهيئة اللعبة
        
        المعاملات:
            line_bot_api: واجهة LINE Bot API
            ai_generate_question: دالة توليد أسئلة بالـ AI (اختياري)
            ai_check_answer: دالة التحقق من الإجابات بالـ AI (اختياري)
        """
        # استدعاء الكلاس الأساسي
        super().__init__(line_bot_api, questions_count=5)
        
        # إعداد AI (اختياري)
        self.ai_generate_question = ai_generate_question
        self.ai_check_answer = ai_check_answer
        
        # تفعيل ميزات التلميح والكشف
        self.supports_hint = True
        self.supports_reveal = True
        
        # قائمة أسئلة افتراضية (تُستخدم إذا لم يتوفر AI)
        self.questions = [
            {
                "q": "ما هو الشيء الذي يمشي بلا أرجل ويبكي بلا عيون؟",
                "a": "السحاب"
            },
            {
                "q": "ما هو الشيء الذي له رأس ولا يملك عيون؟",
                "a": "الدبوس"
            },
            {
                "q": "شيء موجود في السماء إذا أضفت له حرفاً أصبح في الأرض؟",
                "a": "نجم"
            },
            {
                "q": "ما هو الشيء الذي كلما زاد نقص؟",
                "a": "العمر"
            },
            {
                "q": "ما هو الشيء الذي يكتب ولا يقرأ؟",
                "a": "القلم"
            },
            {
                "q": "له أوراق وليس شجرة؟",
                "a": "الكتاب"
            },
            {
                "q": "ما هو الشيء الذي يسمع بلا أذن ويتكلم بلا لسان؟",
                "a": "الهاتف"
            },
            {
                "q": "له عين واحدة ولا يرى؟",
                "a": "الإبرة"
            },
            {
                "q": "ما هو الشيء الذي يوجد في كل شيء؟",
                "a": "الاسم"
            },
            {
                "q": "أخت خالك وليست خالتك؟",
                "a": "أمك"
            }
        ]
        
        # خلط الأسئلة لتنوع اللعبة
        random.shuffle(self.questions)

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
            dict: سؤال وإجابة {"q": "...", "a": "..."}
        """
        # محاولة استخدام AI أولاً
        if self.ai_generate_question:
            try:
                new_question = self.ai_generate_question()
                if new_question and "q" in new_question and "a" in new_question:
                    return new_question
            except Exception as e:
                # تسجيل الخطأ والرجوع للقائمة الافتراضية
                import logging
                logging.warning(f"AI question generation failed: {e}")
        
        # استخدام القائمة الافتراضية
        return self.questions[self.current_question % len(self.questions)]

    def get_question(self) -> Any:
        """
        إنشاء وإرجاع رسالة Flex للسؤال
        
        العودة:
            FlexMessage: السؤال بتصميم Neumorphism
        """
        # توليد السؤال
        question_data = self.generate_question()
        self.current_answer = question_data["a"]
        
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
                        "text": "🧠 لعبة الذكاء",
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
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": question_data["q"],
                                "size": "lg",
                                "color": colors["text"],
                                "align": "center",
                                "wrap": True,
                                "weight": "bold"
                            }
                        ],
                        "backgroundColor": colors["card"],
                        "cornerRadius": "20px",
                        "paddingAll": "25px",
                        "margin": "md"
                    },
                    {
                        "type": "text",
                        "text": "💭 فكر جيداً...",
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
        
        # إرجاع Flex Message
        return self._create_flex_with_buttons("لعبة الذكاء", flex_content)

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
            
            # إذا انتهت اللعبة
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
        
        # 3. استخدام AI للتحقق (إن توفر)
        elif self.ai_check_answer:
            try:
                is_valid = self.ai_check_answer(self.current_answer, user_answer)
            except Exception as e:
                import logging
                logging.warning(f"AI answer check failed: {e}")

        # إجابة خاطئة
        if not is_valid:
            return {
                "message": "▫️ إجابة غير صحيحة ▪️",
                "response": self._create_text_message("▫️ إجابة غير صحيحة ▪️"),
                "points": 0
            }

        # ===== إجابة صحيحة =====
        # إضافة النقاط
        points = self.add_score(user_id, display_name, 10)
        
        # الانتقال للسؤال التالي
        next_question = self.next_question()
        
        # التحقق من انتهاء اللعبة
        if isinstance(next_question, dict) and next_question.get('game_over'):
            next_question['points'] = points
            return next_question
        
        # رسالة النجاح
        success_message = f"✅ إجابة صحيحة يا {display_name}!\n+{points} نقطة"
        
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
            "name": "لعبة الذكاء",
            "emoji": "🧠",
            "description": "اختبر ذكاءك بحل الألغاز",
            "questions_count": self.questions_count,
            "supports_ai": bool(self.ai_generate_question),
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
    from linebot.v3.messaging import MessagingApi
    
    # إنشاء instance من API (يتطلب token حقيقي)
    # api = MessagingApi(channel_access_token="your_token")
    
    # إنشاء instance من اللعبة
    # game = IqGame(api)
    
    # بدء اللعبة
    # first_question = game.start_game()
    
    # التحقق من إجابة
    # result = game.check_answer("السحاب", "U123", "أحمد")
    
    print("✅ ملف اللعبة جاهز للاستخدام!")
    print("📝 تأكد من استخدام: from games.base_game import BaseGame")
