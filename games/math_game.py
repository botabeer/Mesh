"""
لعبة الرياضيات - نسخة محدثة ومحسّنة
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
from typing import Dict, Any, Optional


class MathGame(BaseGame):
    """
    لعبة الرياضيات - حل مسائل رياضية بسيطة
    
    الميزات:
    - 3 مستويات صعوبة (سهل، متوسط، صعب)
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
        
        # إعدادات اللعبة
        self.operations = ['+', '-', '×', '÷']
        self.difficulty = 'easy'
        
        # تفعيل ميزات التلميح والكشف
        self.supports_hint = True
        self.supports_reveal = True

    def start_game(self) -> Any:
        """
        بدء اللعبة وإرجاع أول سؤال
        
        العودة:
            FlexMessage: السؤال الأول
        """
        self.current_question = 0
        self.game_active = True
        return self.get_question()

    def generate_question(self) -> Dict[str, Any]:
        """
        توليد سؤال رياضي عشوائي
        
        العودة:
            dict: سؤال وإجابة ومستوى صعوبة
        """
        # تحديد مستوى الصعوبة حسب الجولة
        if self.current_question < 2:
            self.difficulty = 'easy'
        elif self.current_question < 4:
            self.difficulty = 'medium'
        else:
            self.difficulty = 'hard'
        
        # توليد الأرقام حسب الصعوبة
        if self.difficulty == 'easy':
            num1 = random.randint(1, 20)
            num2 = random.randint(1, 20)
            operations = ['+', '-']
        elif self.difficulty == 'medium':
            num1 = random.randint(10, 50)
            num2 = random.randint(10, 50)
            operations = ['+', '-', '×']
        else:
            num1 = random.randint(20, 100)
            num2 = random.randint(2, 20)
            operations = ['+', '-', '×', '÷']
        
        operation = random.choice(operations)
        
        # حساب الإجابة
        if operation == '+':
            answer = num1 + num2
        elif operation == '-':
            if num1 < num2:
                num1, num2 = num2, num1
            answer = num1 - num2
        elif operation == '×':
            answer = num1 * num2
        else:  # ÷
            num1 = num2 * random.randint(2, 10)
            answer = num1 // num2
        
        return {
            'question': f"{num1} {operation} {num2} = ؟",
            'answer': str(answer),
            'difficulty': self.difficulty,
            'num1': num1,
            'num2': num2,
            'operation': operation
        }

    def get_question(self) -> Any:
        """
        إنشاء وإرجاع رسالة Flex للسؤال
        
        العودة:
            FlexMessage: السؤال بتصميم Neumorphism
        """
        # توليد السؤال
        question_data = self.generate_question()
        self.current_answer = question_data["answer"]
        self.current_question_data = question_data
        
        # الحصول على ألوان الثيم الحالي
        colors = self.get_theme_colors()
        
        # أيقونة حسب الصعوبة
        difficulty_emoji = {
            'easy': '⭐',
            'medium': '⭐⭐',
            'hard': '⭐⭐⭐'
        }
        
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
                        "text": "🔢 لعبة الرياضيات",
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
                                "text": question_data["question"],
                                "size": "xxl",
                                "color": colors["text"],
                                "align": "center",
                                "wrap": True,
                                "weight": "bold"
                            }
                        ],
                        "backgroundColor": colors["card"],
                        "cornerRadius": "20px",
                        "paddingAll": "30px",
                        "margin": "md"
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": f"{difficulty_emoji[self.difficulty]} {self.difficulty.upper()}",
                                "size": "xs",
                                "color": colors["text2"],
                                "align": "center",
                                "flex": 1
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
        
        return self._create_flex_with_buttons("لعبة الرياضيات", flex_content)

    def get_hint(self) -> str:
        """
        الحصول على تلميح للسؤال الحالي
        
        العودة:
            str: التلميح
        """
        if not hasattr(self, 'current_question_data'):
            return "💡 لا يوجد تلميح متاح"
        
        q_data = self.current_question_data
        answer = int(self.current_answer)
        
        # تلميحات مختلفة حسب العملية
        if q_data['operation'] == '+':
            hint = f"💡 اجمع {q_data['num1']} + {q_data['num2']}"
        elif q_data['operation'] == '-':
            hint = f"💡 اطرح {q_data['num2']} من {q_data['num1']}"
        elif q_data['operation'] == '×':
            hint = f"💡 اضرب {q_data['num1']} × {q_data['num2']}"
        else:
            hint = f"💡 اقسم {q_data['num1']} ÷ {q_data['num2']}"
        
        # إضافة تلميح عن نطاق الإجابة
        if answer < 10:
            hint += f"\n🔢 الإجابة أقل من 10"
        elif answer < 50:
            hint += f"\n🔢 الإجابة بين 10 و 50"
        else:
            hint += f"\n🔢 الإجابة أكبر من 50"
        
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
        normalized_answer = self.normalize_text(user_answer.strip())

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
        # إزالة المسافات والرموز غير الرقمية
        try:
            user_number = int(normalized_answer.replace(' ', ''))
            correct_number = int(self.current_answer)
            is_valid = (user_number == correct_number)
        except ValueError:
            # إجابة غير رقمية
            return {
                "message": "❌ يجب أن تكون الإجابة رقماً",
                "response": self._create_text_message("❌ يجب أن تكون الإجابة رقماً"),
                "points": 0
            }

        # إجابة خاطئة
        if not is_valid:
            return {
                "message": "▫️ إجابة غير صحيحة ▪️",
                "response": self._create_text_message("▫️ إجابة غير صحيحة ▪️"),
                "points": 0
            }

        # ===== إجابة صحيحة =====
        # حساب النقاط حسب الصعوبة
        difficulty_bonus = {
            'easy': 10,
            'medium': 15,
            'hard': 20
        }
        points = difficulty_bonus.get(self.difficulty, 10)
        points = self.add_score(user_id, display_name, points)
        
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
            "name": "لعبة الرياضيات",
            "emoji": "🔢",
            "description": "حل مسائل رياضية بسيطة",
            "questions_count": self.questions_count,
            "difficulty_levels": 3,
            "supports_hint": self.supports_hint,
            "supports_reveal": self.supports_reveal,
            "active": self.game_active,
            "current_question": self.current_question,
            "players_count": len(self.scores)
        }


# ============================================================================
# Alias للـ IqGame إذا أردت استخدام نفس الكود
# ============================================================================
# (محذوف لأن MathGame مستقلة)


# ============================================================================
# مثال على الاستخدام
# ============================================================================
if __name__ == "__main__":
    """
    مثال على كيفية استخدام اللعبة
    """
    print("✅ ملف لعبة الرياضيات جاهز للاستخدام!")
    print("📝 تأكد من استخدام: from games.base_game import BaseGame")
