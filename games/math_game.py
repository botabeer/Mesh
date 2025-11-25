"""
لعبة الرياضيات - النسخة المحسنة النهائية
Created by: Abeer Aldosari © 2025

الميزات:
✅ AI أولاً مع Fallback قوي
✅ مستويات صعوبة متدرجة
✅ واجهة Flex احترافية
✅ تشفير عربي مثالي
✅ أداء محسن
"""

from games.base_game import BaseGame
import random
from typing import Dict, Any, Optional


class MathGame(BaseGame):
    """لعبة الرياضيات المحسنة مع AI"""
    
    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, questions_count=5)
        self.game_name = "رياضيات"
        self.game_icon = "🔢"
        
        # مستويات الصعوبة
        self.difficulty_levels = {
            1: {"min": 1, "max": 20, "ops": ['+', '-'], "label": "سهل 🌱"},
            2: {"min": 10, "max": 50, "ops": ['+', '-', '×'], "label": "متوسط ⭐"},
            3: {"min": 20, "max": 100, "ops": ['+', '-', '×'], "label": "صعب 🔥"},
            4: {"min": 50, "max": 200, "ops": ['+', '-', '×'], "label": "صعب جداً 💪"},
            5: {"min": 100, "max": 500, "ops": ['+', '-', '×'], "label": "خبير 👑"}
        }
        
        self.previous_question = None
        self.previous_answer = None
    
    def generate_math_question(self, round_num):
        """توليد سؤال رياضي"""
        level = self.difficulty_levels[round_num]
        op = random.choice(level["ops"])
        
        if op == '+':
            a = random.randint(level["min"], level["max"])
            b = random.randint(level["min"], level["max"])
            question = f"{a} + {b} = ؟"
            answer = str(a + b)
        elif op == '-':
            a = random.randint(level["min"] + 10, level["max"])
            b = random.randint(level["min"], a - 1)
            question = f"{a} - {b} = ؟"
            answer = str(a - b)
        else:  # ×
            max_factor = min(20, level["max"] // 10)
            a = random.randint(2, max_factor)
            b = random.randint(2, max_factor)
            question = f"{a} × {b} = ؟"
            answer = str(a * b)
        
        return {"q": question, "a": answer, "level": level["label"]}
    
    def generate_question_with_ai(self):
        """توليد سؤال بالذكاء الاصطناعي مع Fallback"""
        question_data = None
        round_num = min(self.current_question + 1, 5)
        
        # محاولة AI أولاً
        if self.ai_generate_question:
            try:
                question_data = self.ai_generate_question()
                if question_data and "q" in question_data and "a" in question_data:
                    if "level" not in question_data:
                        question_data["level"] = self.difficulty_levels[round_num]["label"]
                    return question_data
            except Exception as e:
                print(f"⚠️ AI generation failed, using fallback: {e}")
        
        # Fallback
        return self.generate_math_question(round_num)
    
    def start_game(self):
        """بدء اللعبة"""
        self.current_question = 0
        self.game_active = True
        self.previous_question = None
        self.previous_answer = None
        self.answered_users.clear()
        return self.get_question()
    
    def get_question(self):
        """إنشاء سؤال مع واجهة Flex محسنة"""
        q_data = self.generate_question_with_ai()
        self.current_answer = q_data["a"]
        
        colors = self.get_theme_colors()
        
        # قسم السؤال السابق
        previous_section = []
        if self.previous_question and self.previous_answer:
            previous_section = [
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
            ]
        
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
                                "text": f"جولة {self.current_question + 1}/5",
                                "size": "sm",
                                "color": colors["text2"],
                                "align": "end",
                                "flex": 2
                            }
                        ]
                    },
                    {
                        "type": "text",
                        "text": f"المستوى: {q_data.get('level', 'متوسط')}",
                        "size": "xs",
                        "color": colors["primary"],
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
                "spacing": "md",
                "contents": previous_section + [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "❓ السؤال:",
                                "size": "sm",
                                "color": colors["text2"],
                                "weight": "bold"
                            },
                            {
                                "type": "text",
                                "text": q_data["q"],
                                "size": "xxl",
                                "color": colors["text"],
                                "wrap": True,
                                "margin": "md",
                                "weight": "bold",
                                "align": "center"
                            }
                        ],
                        "backgroundColor": colors["card"],
                        "cornerRadius": "20px",
                        "paddingAll": "20px"
                    },
                    {
                        "type": "text",
                        "text": "💡 اكتب 'لمح' للتلميح أو 'جاوب' للإجابة",
                        "size": "xs",
                        "color": colors["text2"],
                        "align": "center",
                        "wrap": True,
                        "margin": "md"
                    }
                ],
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
                                "action": {"type": "message", "label": "💡 لمّح", "text": "لمح"},
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
        
        return self._create_flex_with_buttons(f"{self.game_name} - جولة {self.current_question + 1}", flex_content)
    
    def check_answer(self, user_answer: str, user_id: str, display_name: str) -> Optional[Dict[str, Any]]:
        """فحص الإجابة"""
        if not self.game_active or user_id in self.answered_users:
            return None
        
        normalized = self.normalize_text(user_answer)
        
        # أمر التلميح
        if normalized == "لمح":
            hint = self.get_hint()
            return {
                'message': hint,
                'response': self._create_text_message(hint),
                'points': 0
            }
        
        # أمر الإجابة
        if normalized == "جاوب":
            reveal = f"📝 الإجابة: {self.current_answer}"
            
            # حفظ السؤال والجواب
            q_data = self.generate_question_with_ai()
            self.previous_question = q_data["q"]
            self.previous_answer = self.current_answer
            
            # الانتقال للسؤال التالي
            self.current_question += 1
            self.answered_users.clear()
            
            if self.current_question >= self.questions_count:
                result = self.end_game()
                result['message'] = f"{reveal}\n\n{result.get('message', '')}"
                return result
            
            next_q = self.get_question()
            return {'message': reveal, 'response': next_q, 'points': 0}
        
        # فحص الإجابة
        is_correct = False
        try:
            user_num = int(normalized.replace('،', '').replace(',', '').replace(' ', ''))
            correct_num = int(self.current_answer)
            is_correct = user_num == correct_num
        except:
            pass
        
        if is_correct:
            points = self.add_score(user_id, display_name, 10)
            
            # حفظ السؤال والجواب
            q_data = self.generate_question_with_ai()
            self.previous_question = q_data["q"]
            self.previous_answer = self.current_answer
            
            # الانتقال للسؤال التالي
            self.current_question += 1
            self.answered_users.clear()
            
            if self.current_question >= self.questions_count:
                result = self.end_game()
                result['points'] = points
                result['message'] = f"✅ إجابة صحيحة يا {display_name}!\n+{points} نقطة\n\n{result.get('message', '')}"
                return result
            
            next_q = self.get_question()
            success_msg = f"✅ إجابة صحيحة يا {display_name}!\n+{points} نقطة"
            
            return {
                'message': success_msg,
                'response': next_q,
                'points': points
            }
        
        return {
            'message': "❌ إجابة غير صحيحة",
            'response': self._create_text_message("❌ إجابة غير صحيحة، حاول مرة أخرى"),
            'points': 0
        }
    
    def get_hint(self):
        """تلميح ذكي محسن"""
        try:
            answer = int(self.current_answer)
            hints = []
            
            # زوجي أو فردي
            if answer % 2 == 0:
                hints.append("💡 العدد زوجي")
            else:
                hints.append("💡 العدد فردي")
            
            # نطاق العدد
            if answer < 10:
                hints.append("📊 العدد أصغر من 10")
            elif answer < 50:
                hints.append("📊 العدد بين 10 و 50")
            elif answer < 100:
                hints.append("📊 العدد بين 50 و 100")
            else:
                hints.append("📊 العدد أكبر من 100")
            
            return "\n".join(hints)
        except:
            return "💡 فكر جيداً"
    
    def get_game_info(self) -> Dict[str, Any]:
        """معلومات اللعبة"""
        return {
            "name": "لعبة الرياضيات",
            "emoji": "🔢",
            "description": "مسائل رياضية متدرجة الصعوبة مع دعم AI",
            "questions_count": self.questions_count,
            "supports_hint": True,
            "supports_reveal": True,
            "active": self.game_active,
            "current_question": self.current_question,
            "players_count": len(self.scores),
            "ai_enabled": self.ai_generate_question is not None
        }
