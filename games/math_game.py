"""
🔢 لعبة الرياضيات - Bot Mesh v3.2
أسئلة حسابية ذكية مع صعوبة متدرجة
Created by: Abeer Aldosari © 2025
"""

from games.base_game import BaseGame
import random
from typing import Dict, Any, Optional


class MathGame(BaseGame):
    """لعبة الرياضيات المحسّنة"""

    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, questions_count=5)
        self.game_name = "رياضيات"
        self.game_icon = "🔢"
        
        # مستويات الصعوبة المتدرجة
        self.difficulty_levels = {
            1: {
                "name": "سهل",
                "min": 1,
                "max": 20,
                "ops": ['+', '-']
            },
            2: {
                "name": "متوسط",
                "min": 10,
                "max": 50,
                "ops": ['+', '-', '×']
            },
            3: {
                "name": "صعب",
                "min": 20,
                "max": 100,
                "ops": ['+', '-', '×']
            },
            4: {
                "name": "صعب جداً",
                "min": 50,
                "max": 200,
                "ops": ['+', '-', '×']
            },
            5: {
                "name": "خبير",
                "min": 100,
                "max": 500,
                "ops": ['+', '-', '×', '÷']
            }
        }
        
        self.current_question_data = None

    def generate_math_question(self):
        """توليد سؤال رياضي حسب المستوى"""
        level = min(self.current_question + 1, 5)
        config = self.difficulty_levels[level]
        
        operation = random.choice(config["ops"])
        
        if operation == '+':
            a = random.randint(config["min"], config["max"])
            b = random.randint(config["min"], config["max"])
            answer = a + b
            question = f"{a} + {b} = ؟"
            
        elif operation == '-':
            a = random.randint(config["min"] + 10, config["max"])
            b = random.randint(config["min"], a - 1)
            answer = a - b
            question = f"{a} - {b} = ؟"
            
        elif operation == '×':
            max_factor = min(20, config["max"] // 10)
            a = random.randint(2, max_factor)
            b = random.randint(2, max_factor)
            answer = a * b
            question = f"{a} × {b} = ؟"
            
        else:  # ÷
            result = random.randint(2, 20)
            divisor = random.randint(2, 15)
            a = result * divisor
            answer = result
            question = f"{a} ÷ {divisor} = ؟"
        
        return {
            "question": question,
            "answer": str(answer),
            "level": level,
            "level_name": config["name"]
        }

    def start_game(self):
        """بدء اللعبة"""
        self.current_question = 0
        self.game_active = True
        self.previous_question = None
        self.previous_answer = None
        self.answered_users.clear()
        return self.get_question()

    def get_question(self):
        """إنشاء سؤال مع واجهة Flex احترافية"""
        q_data = self.generate_math_question()
        self.current_question_data = q_data
        self.current_answer = q_data["answer"]
        
        colors = self.get_theme_colors()
        
        # محتوى الـ body
        body_contents = []
        
        # قسم السؤال السابق
        if self.previous_question and self.previous_answer:
            body_contents.extend([
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "📝 السؤال السابق:",
                            "size": "xs",
                            "color": colors["text2"],
                            "weight": "bold"
                        },
                        {
                            "type": "text",
                            "text": self.previous_question,
                            "size": "xs",
                            "color": colors["text2"],
                            "wrap": True,
                            "margin": "xs"
                        },
                        {
                            "type": "text",
                            "text": f"✅ الجواب: {self.previous_answer}",
                            "size": "xs",
                            "color": colors["success"],
                            "wrap": True,
                            "margin": "xs"
                        }
                    ],
                    "backgroundColor": colors["card"],
                    "cornerRadius": "15px",
                    "paddingAll": "12px",
                    "margin": "md"
                },
                {"type": "separator", "color": colors["shadow1"], "margin": "md"}
            ])
        
        # مستوى الصعوبة
        body_contents.append({
            "type": "text",
            "text": f"📊 المستوى: {q_data['level_name']}",
            "size": "sm",
            "color": colors["primary"],
            "weight": "bold",
            "align": "center"
        })
        
        # السؤال
        body_contents.append({
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": q_data["question"],
                    "size": "xxl",
                    "color": colors["text"],
                    "weight": "bold",
                    "align": "center"
                }
            ],
            "backgroundColor": colors["card"],
            "cornerRadius": "20px",
            "paddingAll": "30px",
            "margin": "md"
        })
        
        # معلومة إضافية
        body_contents.append({
            "type": "text",
            "text": "💡 اكتب 'لمح' للتلميح أو 'جاوب' للإجابة",
            "size": "xs",
            "color": colors["text2"],
            "align": "center",
            "wrap": True,
            "margin": "md"
        })
        
        # بناء الـ Flex
        flex_content = {
            "type": "bubble",
            "size": "mega",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": f"{self.game_icon} {self.game_name}",
                                "size": "xl",
                                "weight": "bold",
                                "color": colors["text"],
                                "flex": 3
                            },
                            {
                                "type": "text",
                                "text": f"جولة {self.current_question + 1}/{self.questions_count}",
                                "size": "sm",
                                "color": colors["text2"],
                                "align": "end",
                                "flex": 2
                            }
                        ]
                    }
                ],
                "backgroundColor": colors["bg"],
                "paddingAll": "20px"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": body_contents,
                "backgroundColor": colors["bg"],
                "paddingAll": "15px"
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "spacing": "sm",
                        "contents": [
                            {
                                "type": "button",
                                "action": {"type": "message", "label": "💡 لمح", "text": "لمح"},
                                "style": "secondary",
                                "height": "sm",
                                "color": colors["shadow1"]
                            },
                            {
                                "type": "button",
                                "action": {"type": "message", "label": "🔍 جاوب", "text": "جاوب"},
                                "style": "secondary",
                                "height": "sm",
                                "color": colors["shadow1"]
                            }
                        ]
                    },
                    {
                        "type": "button",
                        "action": {"type": "message", "label": "⛔ إيقاف", "text": "إيقاف"},
                        "style": "primary",
                        "height": "sm",
                        "color": colors["error"]
                    }
                ],
                "backgroundColor": colors["bg"],
                "paddingAll": "15px"
            },
            "styles": {
                "body": {"backgroundColor": colors["bg"]},
                "footer": {"backgroundColor": colors["bg"]}
            }
        }
        
        return self._create_flex_with_buttons(
            f"{self.game_name} - جولة {self.current_question + 1}",
            flex_content
        )

    def check_answer(self, user_answer: str, user_id: str, display_name: str) -> Optional[Dict[str, Any]]:
        """فحص الإجابة"""
        if not self.game_active:
            return None
        
        # التحقق من أن المستخدم لم يجب على هذا السؤال
        if user_id in self.answered_users:
            return None
        
        answer = user_answer.strip().replace(',', '').replace('،', '').replace(' ', '')
        normalized = self.normalize_text(answer)
        
        # معالجة التلميح
        if normalized == "لمح":
            hint = f"💡 الإجابة عدد من {len(self.current_answer)} خانات"
            return {
                'message': hint,
                'response': self._create_text_message(hint),
                'points': 0
            }
        
        # معالجة كشف الإجابة
        if normalized == "جاوب":
            reveal = f"🔢 الإجابة: {self.current_answer}"
            
            # حفظ السؤال والإجابة
            if self.current_question_data:
                self.previous_question = self.current_question_data["question"]
                self.previous_answer = self.current_answer
            
            # الانتقال للسؤال التالي
            self.current_question += 1
            self.answered_users.clear()
            
            if self.current_question >= self.questions_count:
                result = self.end_game()
                result['message'] = f"{reveal}\n\n{result.get('message', '')}"
                return result
            
            next_q = self.get_question()
            return {
                'message': reveal,
                'response': next_q,
                'points': 0
            }
        
        # التحقق من أن الإجابة رقم
        try:
            user_num = int(answer)
            correct_num = int(self.current_answer)
        except ValueError:
            return {
                'message': "❌ الرجاء إدخال رقم صحيح فقط",
                'response': self._create_text_message("❌ الرجاء إدخال رقم صحيح فقط"),
                'points': 0
            }
        
        # فحص الإجابة
        if user_num == correct_num:
            points = self.add_score(user_id, display_name, 10)
            
            if points == 0:  # المستخدم أجاب من قبل
                return None
            
            # حفظ السؤال والإجابة
            if self.current_question_data:
                self.previous_question = self.current_question_data["question"]
                self.previous_answer = self.current_answer
            
            # الانتقال للسؤال التالي
            self.current_question += 1
            self.answered_users.clear()
            
            if self.current_question >= self.questions_count:
                result = self.end_game()
                result['points'] = points
                result['message'] = f"✅ صحيح يا {display_name}!\n🔢 {self.current_answer}\n+{points} نقطة\n\n{result.get('message', '')}"
                return result
            
            next_q = self.get_question()
            success_msg = f"✅ صحيح يا {display_name}!\n🔢 {self.current_answer}\n+{points} نقطة"
            
            return {
                'message': success_msg,
                'response': next_q,
                'points': points
            }
        
        # إجابة خاطئة
        return {
            'message': "❌ إجابة غير صحيحة، حاول مرة أخرى",
            'response': self._create_text_message("❌ إجابة غير صحيحة، حاول مرة أخرى"),
            'points': 0
        }

    def get_game_info(self) -> Dict[str, Any]:
        """معلومات اللعبة"""
        info = super().get_game_info()
        info.update({
            "description": "أسئلة حسابية مع صعوبة متدرجة",
            "levels": len(self.difficulty_levels)
        })
        return info
