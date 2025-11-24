"""
لعبة الكلمة واللون - نسخة محدثة ومحسّنة
Created by: Abeer Aldosari © 2025

تحديثات:
- استيراد صحيح من games.base_game
- نظام Stroop Effect محسّن
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


class WordColorGame(BaseGame):
    """
    لعبة الكلمة واللون - Stroop Effect
    
    الميزات:
    - تأثير Stroop (الكلمة vs اللون الفعلي)
    - 9 ألوان مختلفة
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
        
        # قاعدة بيانات الألوان
        self.colors = {
            "أحمر": "🔴",
            "أزرق": "🔵",
            "أخضر": "🟢",
            "أصفر": "🟡",
            "برتقالي": "🟠",
            "أرجواني": "🟣",
            "بني": "🟤",
            "أسود": "⚫",
            "أبيض": "⚪"
        }
        
        self.color_names = list(self.colors.keys())
        
        self.word_color = None
        self.display_color = None

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
        # اختيار ألوان
        self.word_color = random.choice(self.color_names)
        self.display_color = random.choice(self.color_names)
        
        # أحياناً نجعل اللون مطابق للكلمة (30% احتمال)
        if random.random() < 0.3:
            self.display_color = self.word_color
        
        self.current_answer = self.display_color
        color_emoji = self.colors[self.display_color]
        
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
                        "text": "🎨 كلمة ولون",
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
                        "text": "ما لون الدائرة؟",
                        "size": "lg",
                        "color": colors["text"],
                        "align": "center",
                        "weight": "bold",
                        "margin": "md"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": f"الكلمة: {self.word_color}",
                                "size": "md",
                                "color": colors["text"],
                                "align": "center",
                                "weight": "bold"
                            },
                            {
                                "type": "text",
                                "text": f"الدائرة: {color_emoji}",
                                "size": "xxl",
                                "align": "center",
                                "margin": "lg"
                            }
                        ],
                        "backgroundColor": colors["card"],
                        "cornerRadius": "20px",
                        "paddingAll": "25px",
                        "margin": "lg"
                    },
                    {
                        "type": "text",
                        "text": "⚠️ اكتب لون الدائرة وليس الكلمة!",
                        "size": "sm",
                        "color": "#FF6B6B",
                        "align": "center",
                        "margin": "lg",
                        "wrap": True
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
        
        return self._create_flex_with_buttons("كلمة ولون", flex_content)

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
        
        hint = f"💡 أول حرف '{first_char}' وعدد الحروف {length}"
        hint += f"\n🎨 ركز على لون الدائرة {self.colors[self.display_color]} وليس الكلمة!"
        
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
            reveal = f"🎨 اللون الصحيح: {self.current_answer}"
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
        
        # 2. مطابقة جزئية (75% تشابه)
        elif difflib.SequenceMatcher(None, normalized_answer, normalized_correct).ratio() > 0.75:
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
        success_message = f"✅ إجابة صحيحة يا {display_name}!\n🎨 اللون: {self.current_answer}\n+{points} نقطة"
        
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
            "name": "لعبة الكلمة واللون",
            "emoji": "🎨",
            "description": "اختبار Stroop Effect - ركز على اللون!",
            "questions_count": self.questions_count,
            "colors_count": len(self.colors),
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
    print("✅ ملف لعبة الكلمة واللون جاهز للاستخدام!")
    print("📝 تأكد من استخدام: from games.base_game import BaseGame")
