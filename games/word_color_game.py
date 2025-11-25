"""
لعبة لون الكلمة (Stroop Effect) - النسخة المحسنة النهائية
Created by: Abeer Aldosari © 2025

الميزات:
✅ تأثير Stroop الكلاسيكي
✅ ألوان متعددة ومتنوعة
✅ واجهة Flex احترافية
✅ تشفير عربي مثالي
✅ أداء محسن
✅ بدون دعم لمح/جاوب (طبيعة اللعبة)
"""

from games.base_game import BaseGame
import random
from typing import Dict, Any, Optional


class WordColorGame(BaseGame):
    """لعبة لون الكلمة المحسنة (Stroop Test)"""

    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, questions_count=5)
        self.game_name = "لون الكلمة"
        self.game_icon = "🎨"
        self.supports_hint = False
        self.supports_reveal = False

        # خريطة الألوان
        self.colors = {
            "أحمر": "#E53E3E",
            "أزرق": "#3182CE",
            "أخضر": "#38A169",
            "أصفر": "#D69E2E",
            "برتقالي": "#DD6B20",
            "بنفسجي": "#805AD5",
            "وردي": "#D53F8C",
            "بني": "#8B4513"
        }

        self.color_names = list(self.colors.keys())
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
        """إنشاء سؤال مع واجهة Flex محسنة"""
        # اختيار كلمة ولون (عادة مختلفين)
        word = random.choice(self.color_names)

        # 70% احتمالية عدم التطابق لجعل اللعبة تحديًا
        if random.random() < 0.7:
            color_name = random.choice([c for c in self.color_names if c != word])
        else:
            color_name = word

        self.current_answer = color_name
        color_hex = self.colors[color_name]

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
                            "text": "📝 الكلمة السابقة:",
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
                            "text": f"✅ اللون كان: {self.previous_answer}",
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
                        "text": "📝 ما لون هذه الكلمة؟",
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
                                "text": word,
                                "size": "xxl",
                                "weight": "bold",
                                "color": color_hex,
                                "align": "center"
                            }
                        ],
                        "backgroundColor": colors["card"],
                        "cornerRadius": "20px",
                        "paddingAll": "30px"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "⚠️ اكتب اسم اللون، وليس الكلمة!",
                                "size": "sm",
                                "color": "#FF5555",
                                "wrap": True,
                                "align": "center"
                            }
                        ],
                        "backgroundColor": colors["card"],
                        "cornerRadius": "15px",
                        "paddingAll": "15px"
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

        # رفض أوامر لمح/جاوب
        if normalized in ['لمح', 'جاوب']:
            msg = "❌ هذه اللعبة لا تدعم التلميحات\n🎨 ركز على اللون وليس الكلمة!"
            return {
                'message': msg,
                'response': self._create_text_message(msg),
                'points': 0
            }

        # فحص الإجابة
        normalized_correct = self.normalize_text(self.current_answer)
        is_correct = normalized == normalized_correct

        if is_correct:
            points = self.add_score(user_id, display_name, 10)

            # حفظ السؤال والجواب
            self.previous_question = "كلمة ملونة"
            self.previous_answer = self.current_answer

            # الانتقال للسؤال التالي
            self.current_question += 1
            self.answered_users.clear()

            if self.current_question >= self.questions_count:
                result = self.end_game()
                result['points'] = points
                result['message'] = f"✅ ممتاز يا {display_name}!\n+{points} نقطة\n\n{result.get('message', '')}"
                return result

            next_q = self.get_question()
            success_msg = f"✅ ممتاز يا {display_name}!\n+{points} نقطة"

            return {
                'message': success_msg,
                'response': next_q,
                'points': points
            }

        return {
            'message': "❌ إجابة غير صحيحة، ركز على اللون!",
            'response': self._create_text_message("❌ إجابة غير صحيحة، ركز على اللون وليس الكلمة!"),
            'points': 0
        }

    def get_game_info(self) -> Dict[str, Any]:
        """معلومات اللعبة"""
        return {
            "name": "لعبة لون الكلمة",
            "emoji": "🎨",
            "description": "اختبار Stroop - سمِّ اللون وليس الكلمة!",
            "questions_count": self.questions_count,
            "supports_hint": False,
            "supports_reveal": False,
            "active": self.game_active,
            "current_question": self.current_question,
            "players_count": len(self.scores)
        }
