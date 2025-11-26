"""
🧠 لعبة الذكاء - Bot Mesh v7.0
ألغاز ذكية ومتنوعة
Created by: Abeer Aldosari © 2025
"""

from games.base_game import BaseGame
import random
from typing import Dict, Any, Optional


class IqGame(BaseGame):
    """لعبة الذكاء والألغاز"""

    def __init__(self, line_bot_api=None):
        super().__init__(line_bot_api, questions_count=5)
        self.game_name = "ذكاء"
        self.game_icon = "🧠"
        
        # قاعدة الألغاز
        self.riddles = [
            {"q": "ما يمشي بلا أرجل ويبكي بلا عيون؟", "a": ["السحاب", "الغيم", "سحاب", "غيم"]},
            {"q": "له رأس ولا عين له؟", "a": ["الدبوس", "دبوس", "المسمار", "مسمار"]},
            {"q": "كلما زاد نقص؟", "a": ["العمر", "عمر", "الوقت", "وقت"]},
            {"q": "يكتب ولا يقرأ؟", "a": ["القلم", "قلم"]},
            {"q": "له أسنان ولا يعض؟", "a": ["المشط", "مشط"]},
            {"q": "في الماء ولكن الماء يميته؟", "a": ["الملح", "ملح"]},
            {"q": "يتكلم بكل اللغات؟", "a": ["الصدى", "صدى"]},
            {"q": "يؤخذ منك قبل أن تعطيه؟", "a": ["الصورة", "صورة"]},
            {"q": "شيء يطير بلا جناح؟", "a": ["الوقت", "وقت", "الدخان", "دخان"]},
            {"q": "كلما أخذت منه كبر؟", "a": ["الحفرة", "حفرة"]},
            {"q": "يخترق الزجاج ولا يكسره؟", "a": ["الضوء", "ضوء"]},
            {"q": "يسمع بلا أذن ويتكلم بلا لسان؟", "a": ["الهاتف", "هاتف", "التلفون", "تلفون"]},
            {"q": "يجري ولا يمشي؟", "a": ["الماء", "ماء", "النهر", "نهر"]},
            {"q": "له عنق بلا رأس؟", "a": ["الزجاجة", "زجاجة"]},
            {"q": "يتبعك أينما ذهبت في النهار فقط؟", "a": ["الظل", "ظل"]}
        ]
        
        random.shuffle(self.riddles)
        self.used_riddles = []
        self.previous_question = None
        self.previous_answer = None

    def start_game(self):
        """بدء اللعبة"""
        self.current_question = 0
        self.game_active = True
        self.previous_question = None
        self.previous_answer = None
        self.answered_users.clear()
        return self.get_question()

    def get_question(self):
        """إنشاء سؤال مع واجهة Flex"""
        # اختيار لغز
        available = [r for r in self.riddles if r not in self.used_riddles]
        if not available:
            self.used_riddles = []
            available = self.riddles.copy()
        
        riddle = random.choice(available)
        self.used_riddles.append(riddle)
        
        self.current_answer = riddle["a"]
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
                            "text": "📝 اللغز السابق:",
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
                        "type": "text",
                        "text": "🧩 حل هذا اللغز:",
                        "size": "md",
                        "color": colors["text"],
                        "weight": "bold",
                        "align": "center"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": riddle["q"],
                                "size": "lg",
                                "color": colors["text"],
                                "wrap": True,
                                "align": "center",
                                "weight": "bold"
                            }
                        ],
                        "backgroundColor": colors["card"],
                        "cornerRadius": "20px",
                        "paddingAll": "25px"
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
        
        # أمر كشف الإجابة
        if normalized == "جاوب":
            answer_text = " أو ".join(self.current_answer)
            reveal = f"📝 الإجابة: {answer_text}"
            
            # حفظ السؤال والجواب
            riddle = self.used_riddles[-1] if self.used_riddles else None
            if riddle:
                self.previous_question = riddle["q"]
                self.previous_answer = answer_text
            
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
        for correct in self.current_answer:
            if self.normalize_text(correct) == normalized:
                points = self.add_score(user_id, display_name, 10)
                
                # حفظ السؤال والجواب
                riddle = self.used_riddles[-1] if self.used_riddles else None
                if riddle:
                    self.previous_question = riddle["q"]
                    self.previous_answer = correct
                
                # الانتقال للسؤال التالي
                self.current_question += 1
                self.answered_users.clear()
                
                if self.current_question >= self.questions_count:
                    result = self.end_game()
                    result['points'] = points
                    result['message'] = f"✅ صحيح يا {display_name}!\n+{points} نقطة\n\n{result.get('message', '')}"
                    return result
                
                next_q = self.get_question()
                success_msg = f"✅ صحيح يا {display_name}!\n+{points} نقطة"
                
                return {
                    'message': success_msg,
                    'response': next_q,
                    'points': points
                }
        
        return {
            'message': "❌ إجابة غير صحيحة، حاول مرة أخرى",
            'response': self._create_text_message("❌ إجابة غير صحيحة، حاول مرة أخرى"),
            'points': 0
        }

    def get_game_info(self) -> Dict[str, Any]:
        """معلومات اللعبة"""
        return {
            "name": "لعبة الذكاء",
            "emoji": "🧠",
            "description": "ألغاز ذكية ومتنوعة",
            "questions_count": self.questions_count,
            "supports_hint": True,
            "supports_reveal": True,
            "active": self.game_active,
            "current_question": self.current_question,
            "players_count": len(self.scores)
        }
