"""
لعبة الكتابة السريعة
Created by: Abeer Aldosari © 2025
LINE Compatible - Neumorphism Soft Design
"""

from games.base_game import BaseGame
import random
from datetime import datetime
from typing import Dict, Any, Optional


class FastTypingGame(BaseGame):
    """لعبة الكتابة السريعة"""
    
    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, questions_count=5)
        self.supports_hint = False
        self.supports_reveal = False
        
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
            "التواضع زينة العلم"
        ]
        random.shuffle(self.sentences)
        
        self.start_time = None
        self.time_taken = 0
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
        sentence = self.sentences[self.current_question % len(self.sentences)]
        self.current_answer = sentence
        self.start_time = datetime.now()
        
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
                                "text": "⚡ كتابة سريعة",
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
                        "text": "اكتب بسرعة ودقة:",
                        "size": "sm",
                        "color": colors["text2"],
                        "align": "center"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": f"« {sentence} »",
                                "size": "lg",
                                "color": colors["text"],
                                "align": "center",
                                "wrap": True,
                                "weight": "bold"
                            }
                        ],
                        "backgroundColor": colors["card"],
                        "cornerRadius": "15px",
                        "paddingAll": "25px"
                    },
                    {
                        "type": "text",
                        "text": "⏱️ أسرع إجابة صحيحة تفوز!",
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
                                "color": colors["text"],
                                "wrap": True
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
                        "type": "text",
                        "text": "⚠️ لا تدعم: لمح • جاوب",
                        "size": "xxs",
                        "color": "#FF6B6B",
                        "align": "center"
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
        
        return self._create_flex_message("كتابة سريعة", flex_content)

    def check_answer(self, user_answer: str, user_id: str, display_name: str) -> Optional[Dict[str, Any]]:
        if not self.game_active:
            return None

        answer = user_answer.strip()
        normalized = self.normalize_text(answer)
        
        if normalized in ['لمح', 'جاوب']:
            msg = "❌ هذه اللعبة لا تدعم التلميحات أو كشف الإجابة"
            return {'message': msg, 'response': self._create_text_message(msg), 'points': 0}

        if answer != self.current_answer:
            return {
                "message": "❌ إجابة غير صحيحة\n⚠️ يجب كتابة الجملة بالضبط",
                "response": self._create_text_message("❌ إجابة غير صحيحة\n⚠️ يجب كتابة الجملة بالضبط"),
                "points": 0
            }

        self.time_taken = (datetime.now() - self.start_time).total_seconds()
        
        if self.time_taken <= 5:
            points = 20
        elif self.time_taken <= 10:
            points = 15
        elif self.time_taken <= 20:
            points = 10
        else:
            points = 5
        
        self.last_correct_answer = self.current_answer
        points = self.add_score(user_id, display_name, points)
        next_question = self.next_question()
        
        if isinstance(next_question, dict) and next_question.get('game_over'):
            next_question['points'] = points
            next_question['message'] = f"✅ ممتاز يا {display_name}!\n⏱️ الوقت: {self.time_taken:.1f}ث\n+{points} نقطة\n\n{next_question.get('message','')}"
            return next_question
        
        success_message = f"✅ ممتاز يا {display_name}!\n⏱️ الوقت: {self.time_taken:.1f}ث\n+{points} نقطة"
        
        return {
            "message": success_message,
            "response": next_question,
            "points": points
        }

    def get_game_info(self) -> Dict[str, Any]:
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
