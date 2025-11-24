"""
لعبة الرياضيات - مع مؤشر تقدم احترافي
Created by: Abeer Aldosari © 2025
LINE Compatible - Neumorphism Soft Design
"""

from games.base_game import BaseGame
import random
from typing import Dict, Any, Optional


class MathGame(BaseGame):
    """لعبة الرياضيات - حل مسائل رياضية بسيطة"""
    
    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, questions_count=5)
        self.operations = ['+', '-', '×', '÷']
        self.difficulty = 'easy'
        self.supports_hint = True
        self.supports_reveal = True
        self.current_question_data = None
        self.last_correct_answer = None

    def start_game(self) -> Any:
        self.current_question = 0
        self.game_active = True
        self.last_correct_answer = None
        return self.get_question()

    def generate_question(self) -> Dict[str, Any]:
        if self.current_question < 2:
            self.difficulty = 'easy'
        elif self.current_question < 4:
            self.difficulty = 'medium'
        else:
            self.difficulty = 'hard'
        
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
        
        if operation == '+':
            answer = num1 + num2
        elif operation == '-':
            if num1 < num2:
                num1, num2 = num2, num1
            answer = num1 - num2
        elif operation == '×':
            answer = num1 * num2
        else:
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

    def get_progress_bar(self) -> Dict:
        """شريط تقدم احترافي"""
        colors = self.get_theme_colors()
        progress_boxes = []
        
        for i in range(self.questions_count):
            if i < self.current_question:
                bg_color = "#10B981"
            elif i == self.current_question:
                bg_color = colors["primary"]
            else:
                bg_color = "#E5E7EB"
            
            progress_boxes.append({
                "type": "box",
                "layout": "vertical",
                "contents": [],
                "width": f"{100//self.questions_count}%",
                "height": "6px",
                "backgroundColor": bg_color,
                "cornerRadius": "3px"
            })
        
        return {
            "type": "box",
            "layout": "horizontal",
            "contents": progress_boxes,
            "spacing": "xs"
        }

    def get_question(self) -> Any:
        question_data = self.generate_question()
        self.current_answer = question_data["answer"]
        self.current_question_data = question_data
        colors = self.get_theme_colors()
        
        progress_bar = self.get_progress_bar()
        
        difficulty_info = {
            'easy': {'emoji': '⭐', 'text': 'سهل'},
            'medium': {'emoji': '⭐⭐', 'text': 'متوسط'},
            'hard': {'emoji': '⭐⭐⭐', 'text': 'صعب'}
        }
        
        diff = difficulty_info[self.difficulty]
        
        flex_content = {
            "type": "bubble",
            "size": "kilo",
            "header": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": "🔢 رياضيات",
                                "weight": "bold",
                                "size": "lg",
                                "color": "#FFFFFF",
                                "flex": 0
                            },
                            {
                                "type": "text",
                                "text": f"{diff['emoji']} {diff['text']}",
                                "size": "xs",
                                "color": "#FFFFFF",
                                "align": "end"
                            }
                        ]
                    },
                    progress_bar,
                    {
                        "type": "text",
                        "text": f"السؤال {self.current_question + 1} من {self.questions_count}",
                        "size": "xs",
                        "color": "#FFFFFF",
                        "align": "center"
                    }
                ],
                "backgroundColor": colors["primary"],
                "paddingAll": "20px"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "lg",
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
                                "weight": "bold"
                            }
                        ],
                        "backgroundColor": colors["card"],
                        "cornerRadius": "15px",
                        "paddingAll": "30px"
                    }
                ],
                "backgroundColor": colors["bg"],
                "paddingAll": "20px"
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "xs",
                        "contents": [
                            {
                                "type": "text",
                                "text": "✅ الإجابة السابقة:",
                                "size": "xxs",
                                "color": colors["text2"],
                                "weight": "bold"
                            },
                            {
                                "type": "text",
                                "text": self.last_correct_answer if self.last_correct_answer else "لا يوجد بعد",
                                "size": "xs",
                                "color": colors["text"]
                            }
                        ],
                        "backgroundColor": colors["card"],
                        "cornerRadius": "10px",
                        "paddingAll": "10px"
                    },
                    {
                        "type": "separator",
                        "color": colors["shadow1"]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "spacing": "xs",
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
                                "action": {"type": "message", "label": "📝 جاوب", "text": "جاوب"},
                                "style": "secondary",
                                "height": "sm",
                                "color": colors["shadow1"]
                            }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "spacing": "xs",
                        "contents": [
                            {
                                "type": "button",
                                "action": {"type": "message", "label": "⛔ إيقاف", "text": "إيقاف"},
                                "style": "primary",
                                "color": "#FF5555",
                                "height": "sm"
                            }
                        ]
                    },
                    {
                        "type": "separator",
                        "color": colors["shadow1"]
                    },
                    {
                        "type": "text",
                        "text": "تم إنشاؤه بواسطة عبير الدوسري © 2025",
                        "size": "xxs",
                        "color": colors["text2"],
                        "align": "center"
                    }
                ],
                "backgroundColor": colors["bg"],
                "paddingAll": "15px"
            },
            "styles": {
                "body": {"backgroundColor": colors["bg"]},
                "header": {"backgroundColor": colors["primary"]},
                "footer": {"backgroundColor": colors["bg"]}
            }
        }
        
        return self._create_flex_message("لعبة الرياضيات", flex_content)

    def get_hint(self) -> str:
        if not hasattr(self, 'current_question_data'):
            return "💡 لا يوجد تلميح متاح"
        
        q_data = self.current_question_data
        answer = int(self.current_answer)
        
        if q_data['operation'] == '+':
            hint = f"💡 اجمع {q_data['num1']} + {q_data['num2']}"
        elif q_data['operation'] == '-':
            hint = f"💡 اطرح {q_data['num2']} من {q_data['num1']}"
        elif q_data['operation'] == '×':
            hint = f"💡 اضرب {q_data['num1']} × {q_data['num2']}"
        else:
            hint = f"💡 اقسم {q_data['num1']} ÷ {q_data['num2']}"
        
        if answer < 10:
            hint += f"\n🔢 الإجابة أقل من 10"
        elif answer < 50:
            hint += f"\n🔢 الإجابة بين 10 و 50"
        else:
            hint += f"\n🔢 الإجابة أكبر من 50"
        
        return hint

    def check_answer(self, user_answer: str, user_id: str, display_name: str) -> Optional[Dict[str, Any]]:
        if not self.game_active:
            return None

        normalized_answer = self.normalize_text(user_answer.strip())

        if normalized_answer == "لمح":
            hint = self.get_hint()
            return {"message": hint, "response": self._create_text_message(hint), "points": 0}

        if normalized_answer == "جاوب":
            self.last_correct_answer = self.current_answer
            reveal = self.reveal_answer()
            next_question = self.next_question()
            
            if isinstance(next_question, dict) and next_question.get('game_over'):
                next_question['message'] = f"{reveal}\n\n{next_question.get('message','')}"
                return next_question
            
            return {'message': reveal, 'response': next_question, 'points': 0}

        try:
            user_number = int(normalized_answer.replace(' ', ''))
            correct_number = int(self.current_answer)
            is_valid = (user_number == correct_number)
        except ValueError:
            return {
                "message": "❌ يجب أن تكون الإجابة رقماً",
                "response": self._create_text_message("❌ يجب أن تكون الإجابة رقماً"),
                "points": 0
            }

        if not is_valid:
            return {
                "message": "❌ إجابة غير صحيحة",
                "response": self._create_text_message("❌ إجابة غير صحيحة، حاول مرة أخرى"),
                "points": 0
            }

        difficulty_bonus = {'easy': 10, 'medium': 15, 'hard': 20}
        points = difficulty_bonus.get(self.difficulty, 10)
        self.last_correct_answer = self.current_answer
        points = self.add_score(user_id, display_name, points)
        
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

    def get_game_info(self) -> Dict[str, Any]:
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
