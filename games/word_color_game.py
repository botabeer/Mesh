"""
لعبة الكلمة واللون - Stroop Effect
Created by: Abeer Aldosari © 2025
LINE Compatible - Neumorphism Soft Design
"""

from games.base_game import BaseGame
import random
import difflib
from typing import Dict, Any, Optional


class WordColorGame(BaseGame):
    """لعبة الكلمة واللون - Stroop Effect"""
    
    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, questions_count=5)
        self.supports_hint = True
        self.supports_reveal = True
        
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
        self.last_correct_answer = None

    def start_game(self) -> Any:
        self.current_question = 0
        self.game_active = True
        self.last_correct_answer = None
        return self.get_question()

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
        self.word_color = random.choice(self.color_names)
        self.display_color = random.choice(self.color_names)
        
        if random.random() < 0.3:
            self.display_color = self.word_color
        
        self.current_answer = self.display_color
        color_emoji = self.colors[self.display_color]
        
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
                                "text": "🎨 كلمة ولون",
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
                        "type": "text",
                        "text": "ما لون الدائرة؟",
                        "size": "md",
                        "color": colors["text"],
                        "align": "center",
                        "weight": "bold"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "md",
                        "contents": [
                            {
                                "type": "text",
                                "text": f"الكلمة: {self.word_color}",
                                "size": "sm",
                                "color": colors["text"],
                                "align": "center"
                            },
                            {
                                "type": "text",
                                "text": color_emoji,
                                "size": "xxl",
                                "align": "center"
                            }
                        ],
                        "backgroundColor": colors["card"],
                        "cornerRadius": "15px",
                        "paddingAll": "25px"
                    },
                    {
                        "type": "text",
                        "text": "⚠️ اكتب لون الدائرة وليس الكلمة!",
                        "size": "xs",
                        "color": "#FF6B6B",
                        "align": "center",
                        "wrap": True
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
        
        return self._create_flex_message("كلمة ولون", flex_content)

    def get_hint(self) -> str:
        if not self.current_answer:
            return "💡 لا يوجد تلميح متاح"
        
        first_char = self.current_answer[0]
        length = len(self.current_answer)
        
        hint = f"💡 أول حرف '{first_char}' وعدد الحروف {length}"
        hint += f"\n🎨 ركز على لون الدائرة {self.colors[self.display_color]} وليس الكلمة!"
        
        return hint

    def check_answer(self, user_answer: str, user_id: str, display_name: str) -> Optional[Dict[str, Any]]:
        if not self.game_active:
            return None

        normalized_answer = self.normalize_text(user_answer)

        if normalized_answer == "لمح":
            hint = self.get_hint()
            return {"message": hint, "response": self._create_text_message(hint), "points": 0}

        if normalized_answer == "جاوب":
            self.last_correct_answer = self.current_answer
            reveal = f"🎨 اللون الصحيح: {self.current_answer}"
            next_question = self.next_question()
            
            if isinstance(next_question, dict) and next_question.get('game_over'):
                next_question['message'] = f"{reveal}\n\n{next_question.get('message','')}"
                return next_question
            
            return {'message': reveal, 'response': next_question, 'points': 0}

        normalized_correct = self.normalize_text(self.current_answer)
        is_valid = False

        if normalized_answer == normalized_correct:
            is_valid = True
        elif difflib.SequenceMatcher(None, normalized_answer, normalized_correct).ratio() > 0.75:
            is_valid = True

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
        
        success_message = f"✅ إجابة صحيحة يا {display_name}!\n🎨 اللون: {self.current_answer}\n+{points} نقطة"
        
        return {
            "message": success_message,
            "response": next_question,
            "points": points
        }

    def get_game_info(self) -> Dict[str, Any]:
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
