"""
لعبة أسئلة الذكاء - مع مؤشر التقدم
Created by: Abeer Aldosari © 2025
"""

from games.base_game import BaseGame
import random
import difflib
from typing import Dict, Any, Optional


class IqGame(BaseGame):
    """لعبة أسئلة الذكاء مع مؤشر تقدم مرئي"""
    
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

    def get_progress_indicator(self) -> str:
        """إنشاء مؤشر التقدم 🟢⚪⚪⚪⚪"""
        progress = ""
        for i in range(self.questions_count):
            if i < self.current_question:
                progress += "🟢"
            elif i == self.current_question:
                progress += "🔵"
            else:
                progress += "⚪"
        return progress

    def get_question(self) -> Any:
        question_data = self.generate_question()
        self.current_answer = question_data["a"]
        colors = self.get_theme_colors()
        
        progress = self.get_progress_indicator()
        
        flex_content = {
            "type": "bubble",
            "size": "kilo",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": f"▪️ الجولة {self.current_question + 1} من {self.questions_count}  {progress}",
                        "size": "sm",
                        "color": "#FFFFFF",
                        "weight": "bold"
                    },
                    {
                        "type": "separator",
                        "color": "#FFFFFF"
                    },
                    {
                        "type": "text",
                        "text": "🕹️ اللعبة: الذكاء",
                        "size": "md",
                        "color": "#FFFFFF",
                        "weight": "bold"
                    }
                ],
                "backgroundColor": colors["primary"],
                "paddingAll": "15px"
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
                        "type": "text",
                        "text": "✅ الإجابة الصحيحة للجولة السابقة:",
                        "size": "xs",
                        "weight": "bold",
                        "color": "#333333"
                    },
                    {
                        "type": "text",
                        "text": f"▫️ {self.last_correct_answer if self.last_correct_answer else '- (لا يوجد بعد)'}",
                        "size": "sm",
                        "color": "#666666",
                        "wrap": True
                    },
                    {
                        "type": "separator"
                    },
                    {
                        "type": "text",
                        "text": "🎮 الأوامر المتاحة:",
                        "size": "xs",
                        "weight": "bold",
                        "color": "#333333"
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "spacing": "xs",
                        "contents": [
                            {"type": "button", "action": {"type": "message", "label": "▫️ لمح", "text": "لمح"},
                             "style": "secondary", "height": "sm"},
                            {"type": "button", "action": {"type": "message", "label": "▫️ جاوب", "text": "جاوب"},
                             "style": "secondary", "height": "sm"}
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "spacing": "xs",
                        "contents": [
                            {"type": "button", "action": {"type": "message", "label": "▫️ إيقاف", "text": "إيقاف"},
                             "style": "primary", "color": "#FF5555", "height": "sm"}
                        ]
                    }
                ]
            },
            "styles": {
                "body": {"backgroundColor": colors["bg"]},
                "header": {"backgroundColor": colors["primary"]}
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
                "message": "▫️ إجابة غير صحيحة ▪️",
                "response": self._create_text_message("▫️ إجابة غير صحيحة ▪️"),
                "points": 0
            }

        # حفظ الإجابة الصحيحة
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
