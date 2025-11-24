"""
لعبة أسئلة الذكاء - مع مؤشر تقدم احترافي
Created by: Abeer Aldosari © 2025
LINE Compatible - Neumorphism Soft Design
"""

from games.base_game import BaseGame
import random
import difflib
from typing import Dict, Any, Optional


class IqGame(BaseGame):
    """لعبة أسئلة الذكاء مع مؤشر تقدم مرئي احترافي"""
    
    def __init__(self, line_bot_api, ai_generate_question=None, ai_check_answer=None):
        super().__init__(line_bot_api, questions_count=5)
        self.ai_generate_question = ai_generate_question
        self.ai_check_answer = ai_check_answer
        self.supports_hint = True
        self.supports_reveal = True
        
        self.questions = [
            {"q": "ما هو الشيء الذي يمشي بلا أرجل ويبكي بلا عيون؟", "a": "السحاب"},
            {"q": "ما هو الشيء الذي له رأس ولا يملك عيون؟", "a": "الدبوس"},
            {"q": "شيء موجود في السماء إذا أضفت له حرفاً أصبح في الأرض؟", "a": "نجم"},
            {"q": "ما هو الشيء الذي كلما زاد نقص؟", "a": "العمر"},
            {"q": "ما هو الشيء الذي يكتب ولا يقرأ؟", "a": "القلم"},
            {"q": "له أوراق وليس شجرة؟", "a": "الكتاب"},
            {"q": "ما هو الشيء الذي يسمع بلا أذن ويتكلم بلا لسان؟", "a": "الهاتف"},
            {"q": "له عين واحدة ولا يرى؟", "a": "الإبرة"},
            {"q": "ما هو الشيء الذي يوجد في كل شيء؟", "a": "الاسم"},
            {"q": "أخت خالك وليست خالتك؟", "a": "أمك"}
        ]
        random.shuffle(self.questions)
        self.last_correct_answer = None

    def start_game(self) -> Any:
        self.current_question = 0
        self.game_active = True
        self.last_correct_answer = None
        return self.get_question()

    def generate_question(self) -> Dict[str, str]:
        if self.ai_generate_question:
            try:
                new_question = self.ai_generate_question()
                if new_question and "q" in new_question and "a" in new_question:
                    return new_question
            except Exception:
                pass
        return self.questions[self.current_question % len(self.questions)]

    def get_progress_bar(self) -> Dict:
        """إنشاء شريط تقدم احترافي"""
        colors = self.get_theme_colors()
        progress_boxes = []
        
        for i in range(self.questions_count):
            if i < self.current_question:
                # مكتمل - أخضر
                progress_boxes.append({
                    "type": "box",
                    "layout": "vertical",
                    "contents": [],
                    "width": f"{100//self.questions_count}%",
                    "height": "6px",
                    "backgroundColor": "#10B981",
                    "cornerRadius": "3px"
                })
            elif i == self.current_question:
                # حالي - أزرق
                progress_boxes.append({
                    "type": "box",
                    "layout": "vertical",
                    "contents": [],
                    "width": f"{100//self.questions_count}%",
                    "height": "6px",
                    "backgroundColor": colors["primary"],
                    "cornerRadius": "3px"
                })
            else:
                # قادم - رمادي
                progress_boxes.append({
                    "type": "box",
                    "layout": "vertical",
                    "contents": [],
                    "width": f"{100//self.questions_count}%",
                    "height": "6px",
                    "backgroundColor": "#E5E7EB",
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
        self.current_answer = question_data["a"]
        colors = self.get_theme_colors()
        
        progress_bar = self.get_progress_bar()
        
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
                                "text": "🧠 لعبة الذكاء",
                                "weight": "bold",
                                "size": "lg",
                                "color": "#FFFFFF",
                                "flex": 0
                            },
                            {
                                "type": "text",
                                "text": f"{self.current_question + 1}/{self.questions_count}",
                                "size": "sm",
                                "color": "#FFFFFF",
                                "align": "end"
                            }
                        ]
                    },
                    progress_bar
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
                                "text": question_data["q"],
                                "size": "md",
                                "color": colors["text"],
                                "wrap": True,
                                "weight": "bold"
                            }
                        ],
                        "backgroundColor": colors["card"],
                        "cornerRadius": "15px",
                        "paddingAll": "20px"
                    },
                    {
                        "type": "text",
                        "text": "💭 فكر جيداً...",
                        "size": "xs",
                        "color": colors["text2"],
                        "align": "center"
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
        
        return self._create_flex_message("لعبة الذكاء", flex_content)

    def check_answer(self, user_answer: str, user_id: str, display_name: str) -> Optional[Dict[str, Any]]:
        if not self.game_active:
            return None

        normalized_answer = self.normalize_text(user_answer)

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

        normalized_correct = self.normalize_text(self.current_answer)
        is_valid = False

        if normalized_answer == normalized_correct:
            is_valid = True
        elif difflib.SequenceMatcher(None, normalized_answer, normalized_correct).ratio() > 0.8:
            is_valid = True
        elif self.ai_check_answer:
            try:
                is_valid = self.ai_check_answer(self.current_answer, user_answer)
            except Exception:
                pass

        if not is_valid:
            return {
                "message": "❌ إجابة غير صحيحة",
                "response": self._create_text_message("❌ إجابة غير صحيحة، حاول مرة أخرى"),
                "points": 0
            }

        self.last_correct_answer = self.current_answer
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

    def get_game_info(self) -> Dict[str, Any]:
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
