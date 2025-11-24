"""
لعبة الكتابة السريعة - نسخة محدثة ومحسّنة
Created by: Abeer Aldosari © 2025

تحديثات:
- استيراد صحيح من games.base_game
- نظام تتبع الوقت محسّن
- دعم ثيمات ديناميكية
- رسائل Flex حديثة بتصميم Neumorphism
"""

# ============================================================================
# الاستيراد الصحيح
# ============================================================================
from games.base_game import BaseGame  # ✅ صحيح

import random
from datetime import datetime
from typing import Dict, Any, Optional


class FastTypingGame(BaseGame):
    """
    لعبة الكتابة السريعة
    
    الميزات:
    - قاعدة بيانات موسّعة من الجمل
    - تتبع الوقت بدقة
    - نظام نقاط يعتمد على السرعة
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
        
        # إعدادات اللعبة
        self.supports_hint = False  # لا تدعم التلميح (اللعبة تعتمد على الكتابة الدقيقة)
        self.supports_reveal = False  # لا تدعم كشف الإجابة
        
        # قاعدة بيانات الجمل
        self.sentences = [
            "سبحان الله وبحمده",
            "الحمد لله رب العالمين",
            "الله أكبر",
            "لا حول ولا قوة إلا بالله",
            "العلم نور والجهل ظلام",
            "الصبر مفتاح الفرج",
            "الوقت كالسيف إن لم تقطعه قطعك",
            "التعاون أساس النجاح",
            "المعرفة قوة والعمل حياة",
            "التواضع زينة العلم",
            "الصدق منجاة والكذب مهلكة",
            "احترم تُحترم",
            "الإتقان من الإيمان",
            "من جد وجد ومن زرع حصد",
            "العقل السليم في الجسم السليم"
        ]
        random.shuffle(self.sentences)
        
        self.start_time = None
        self.time_taken = 0

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
        # اختيار جملة
        sentence = self.sentences[self.current_question % len(self.sentences)]
        self.current_answer = sentence
        self.start_time = datetime.now()
        
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
                        "text": "⚡ كتابة سريعة",
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
                        "text": "اكتب بسرعة ودقة:",
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
                                "text": f"« {sentence} »",
                                "size": "xl",
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
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": "⏱️",
                                "size": "lg",
                                "flex": 0
                            },
                            {
                                "type": "text",
                                "text": "أسرع إجابة صحيحة تفوز!",
                                "size": "sm",
                                "color": colors["text2"],
                                "flex": 1,
                                "margin": "sm"
                            }
                        ],
                        "margin": "lg"
                    },
                    {
                        "type": "separator",
                        "margin": "lg"
                    },
                    {
                        "type": "text",
                        "text": "⚠️ لا تدعم: لمح • جاوب",
                        "size": "xxs",
                        "color": "#FF6B6B",
                        "align": "center",
                        "margin": "md"
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
        
        return self._create_flex_with_buttons("كتابة سريعة", flex_content)

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

        # تنظيف الإجابة (بدون normalize لأننا نريد المطابقة الدقيقة)
        answer = user_answer.strip()

        # رفض أوامر لمح/جاوب
        normalized = self.normalize_text(answer)
        if normalized in ['لمح', 'جاوب']:
            msg = "❌ هذه اللعبة لا تدعم التلميحات أو كشف الإجابة"
            return {
                'message': msg,
                'response': self._create_text_message(msg),
                'points': 0
            }

        # ===== التحقق من صحة الإجابة =====
        # مطابقة دقيقة
        if answer != self.current_answer:
            return {
                "message": "▫️ إجابة غير صحيحة ▪️\n⚠️ يجب كتابة الجملة بالضبط",
                "response": self._create_text_message("▫️ إجابة غير صحيحة ▪️\n⚠️ يجب كتابة الجملة بالضبط"),
                "points": 0
            }

        # ===== إجابة صحيحة =====
        # حساب الوقت المستغرق
        self.time_taken = (datetime.now() - self.start_time).total_seconds()
        
        # حساب النقاط بناءً على السرعة
        if self.time_taken <= 5:
            points = 20  # سريع جداً
        elif self.time_taken <= 10:
            points = 15  # سريع
        elif self.time_taken <= 20:
            points = 10  # متوسط
        else:
            points = 5   # بطيء
        
        points = self.add_score(user_id, display_name, points)
        
        # الانتقال للسؤال التالي
        next_question = self.next_question()
        
        # التحقق من انتهاء اللعبة
        if isinstance(next_question, dict) and next_question.get('game_over'):
            next_question['points'] = points
            next_question['message'] = f"✅ ممتاز يا {display_name}!\n⏱️ الوقت: {self.time_taken:.1f}ث\n+{points} نقطة\n\n{next_question.get('message','')}"
            return next_question
        
        # رسالة النجاح
        success_message = f"✅ ممتاز يا {display_name}!\n⏱️ الوقت: {self.time_taken:.1f}ث\n+{points} نقطة"
        
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
            "name": "لعبة الكتابة السريعة",
            "emoji": "⚡",
            "description": "اكتب الجملة بسرعة ودقة",
            "questions_count": self.questions_count,
            "sentences_count": len(self.sentences),
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
    print("✅ ملف لعبة الكتابة السريعة جاهز للاستخدام!")
    print("📝 تأكد من استخدام: from games.base_game import BaseGame")
