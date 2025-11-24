"""
لعبة الرياضيات - نسخة محدثة ومحسّنة
Created by: Abeer Aldosari © 2025
"""

# ============================================================================
# الاستيراد الصحيح
# ============================================================================
from games.base_game import BaseGame  # ✅ صحيح

import random
from typing import Dict, Any, Optional


class MathGame(BaseGame):
    """
    لعبة الرياضيات مع دعم مستويات صعوبة ديناميكية
    
    الميزات:
    - 3 مستويات صعوبة (سهل، متوسط، صعب)
    - تصاعد تلقائي للصعوبة
    - عمليات حسابية متنوعة (+، -، ×، ÷)
    - خيارات متعددة للإجابة
    - رسائل Flex حديثة بتصميم Neumorphism
    """
    
    def __init__(self, line_bot_api):
        """
        تهيئة اللعبة
        
        المعاملات:
            line_bot_api: واجهة LINE Bot API
        """
        super().__init__(line_bot_api, questions_count=5)
        
        # تفعيل/تعطيل ميزات التلميح والكشف
        self.supports_hint = False  # لا تدعم التلميح (الإجابة رقمية)
        self.supports_reveal = True
        
        # إعدادات اللعبة
        self.operations = ['+', '-', '×', '÷']
        self.difficulty = 'easy'
        self.current_options = []

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
        توليد سؤال رياضي حسب مستوى الصعوبة
        
        العودة:
            dict: سؤال وإجابة وخيارات
        """
        # تحديد مستوى الصعوبة حسب السؤال الحالي
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
        
        # توليد خيارات خاطئة
        options = [str(answer)]
        while len(options) < 4:
            wrong = answer + random.randint(-10, 10)
            if wrong > 0 and str(wrong) not in options:
                options.append(str(wrong))
        random.shuffle(options)
        
        self.current_options = options
        
        return {
            'question': f"{num1} {operation} {num2} = ؟",
            'answer': str(answer),
            'options': options,
            'difficulty': self.difficulty
        }

    def get_question(self) -> Any:
        """
        إنشاء وإرجاع رسالة Flex للسؤال
        
        العودة:
            FlexMessage: السؤال بتصميم Neumorphism
        """
        question_data = self.generate_question()
        self.current_answer = question_data['answer']
        
        colors = self.get_theme_colors()
        
        # رموز الصعوبة
        difficulty_icons = {
            'easy': '🟢 سهل',
            'medium': '🟡 متوسط',
            'hard': '🔴 صعب'
        }
        
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
                    },
                    {
                        "type": "text",
                        "text": difficulty_icons[self.difficulty],
                        "size": "xs",
                        "color": colors["text2"],
                        "align": "center",
                        "margin": "xs"
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
                                "text": question_data['question'],
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
                        "type": "separator",
                        "margin": "lg"
                    },
                    {
                        "type": "text",
                        "text": "الخيارات:",
                        "size": "sm",
                        "color": colors["text2"],
                        "margin": "lg",
                        "weight": "bold"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": f"أ) {question_data['options'][0]}    ب) {question_data['options'][1]}",
                                "size": "md",
                                "color": colors["text"],
                                "margin": "sm"
                            },
                            {
                                "type": "text",
                                "text": f"ج) {question_data['options'][2]}    د) {question_data['options'][3]}",
                                "size": "md",
                                "color": colors["text"],
                                "margin": "sm"
                            }
                        ],
                        "backgroundColor": colors["card"],
                        "cornerRadius": "15px",
                        "paddingAll": "15px",
                        "margin": "md"
                    },
                    {
                        "type": "text",
                        "text": "📝 اكتب 'جاوب' للكشف عن الإجابة",
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
        if not self.game_active:
            return None

        normalized_answer = self.normalize_text(user_answer).strip()

        # معالجة أمر كشف الإجابة
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

        # التحقق من الإجابة
        if normalized_answer == self.current_answer:
            # إجابة صحيحة
            points = self.add_score(user_id, display_name, 10)
            next_question = self.next_question()
            
            if isinstance(next_question, dict) and next_question.get('game_over'):
                next_question['points'] = points
                return next_question
            
            success_message = f"✅ إجابة صحيحة يا {display_name}!\n+{points} نقطة"
            
            return {
                "message": success_message,
                "response": next_question,
                "points": points
            }
        
        # إجابة خاطئة
        return {
            "message": "❌ إجابة غير صحيحة",
            "response": self._create_text_message("❌ إجابة غير صحيحة"),
            "points": 0
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
            "supports_hint": self.supports_hint,
            "supports_reveal": self.supports_reveal,
            "active": self.game_active,
            "current_question": self.current_question,
            "players_count": len(self.scores),
            "difficulty": self.difficulty
        }


# ============================================================================
# مثال على الاستخدام
# ============================================================================
if __name__ == "__main__":
    print("✅ ملف لعبة الرياضيات جاهز للاستخدام!")
    print("📝 تأكد من استخدام: from games.base_game import BaseGame")
