"""
لعبة التوافق - نسخة محسّنة بدون أزرار لمح/جاوب
Created by: Abeer Aldosari © 2025

التحسينات:
- لعبة ترفيهية بدون أزرار لمح/جاوب
- نفس النسبة لـ (اسم1 اسم2) أو (اسم2 اسم1)
- واجهة Flex احترافية
"""

from games.base_game import BaseGame
from typing import Dict, Any, Optional

class CompatibilityGame(BaseGame):
    """لعبة التوافق المحسّنة"""

    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, questions_count=1)
        self.supports_hint = False
        self.supports_reveal = False

    def calculate_compatibility(self, name1: str, name2: str) -> int:
        """حساب نسبة التوافق - نفس النسبة بغض النظر عن الترتيب"""
        # تطبيع الأسماء
        n1 = self.normalize_text(name1)
        n2 = self.normalize_text(name2)

        # ترتيب الأسماء أبجدياً لضمان نفس النسبة
        names = sorted([n1, n2])
        combined = ''.join(names)

        # حساب seed فريد
        seed = sum(ord(c) * (i + 1) for i, c in enumerate(combined))

        # نسبة بين 20 و 100
        return (seed % 81) + 20

    def get_compatibility_message(self, percentage: int) -> str:
        """رسالة التوافق"""
        if percentage >= 90:
            return "✨ توافق رائع جداً! علاقة مثالية 💕"
        elif percentage >= 75:
            return "💪 توافق ممتاز! علاقة قوية 💖"
        elif percentage >= 60:
            return "🌟 توافق جيد! علاقة واعدة 💗"
        elif percentage >= 45:
            return "🔧 توافق متوسط! يحتاج عمل 💛"
        else:
            return "⚠️ توافق ضعيف! قد تكون هناك تحديات 💔"

    def start_game(self):
        self.current_question = 0
        self.game_active = True
        return self.get_question()

    def get_question(self):
        """سؤال بسيط بدون أزرار"""
        colors = self.get_theme_colors()

        flex_content = {
            "type": "bubble",
            "size": "kilo",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "🖤 لعبة التوافق",
                        "size": "xl",
                        "weight": "bold",
                        "color": "#FF69B4",
                        "align": "center"
                    },
                    {
                        "type": "text",
                        "text": "اكتشف نسبة التوافق!",
                        "size": "sm",
                        "color": colors["text2"],
                        "align": "center",
                        "margin": "sm"
                    }
                ],
                "backgroundColor": colors["bg"],
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
                                "text": "📝 اكتب اسمين مفصولين بمسافة",
                                "size": "lg",
                                "color": colors["text"],
                                "align": "center",
                                "wrap": True,
                                "weight": "bold"
                            },
                            {
                                "type": "text",
                                "text": "مثال: أحمد سارة",
                                "size": "md",
                                "color": colors["primary"],
                                "align": "center",
                                "margin": "md"
                            }
                        ],
                        "backgroundColor": colors["card"],
                        "cornerRadius": "20px",
                        "paddingAll": "25px"
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": "💘",
                                "size": "xl",
                                "flex": 0
                            },
                            {
                                "type": "text",
                                "text": "النتيجة للترفيه فقط!\nسواء كتبت (أحمد سارة) أو (سارة أحمد) ستحصل على نفس النسبة",
                                "size": "xs",
                                "color": colors["text2"],
                                "flex": 1,
                                "margin": "sm",
                                "wrap": True
                            }
                        ]
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
                        "type": "button",
                        "action": {"type": "message", "label": "🏠 البداية", "text": "بداية"},
                        "style": "secondary",
                        "height": "sm"
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

        return self._create_flex_with_buttons("لعبة التوافق", flex_content)

    def check_answer(self, user_answer: str, user_id: str, display_name: str) -> Optional[Dict[str, Any]]:
        if not self.game_active:
            return None

        # تقسيم الأسماء
        names = user_answer.strip().split()

        if len(names) < 2:
            hint = "⚠️ يرجى كتابة اسمين مفصولين بمسافة\nمثال: أحمد سارة"
            return {
                'message': hint,
                'response': self._create_text_message(hint),
                'points': 0
            }

        name1, name2 = names[0], names[1]

        # حساب التوافق
        percentage = self.calculate_compatibility(name1, name2)
        message_text = self.get_compatibility_message(percentage)

        colors = self.get_theme_colors()

        # نافذة النتيجة
        flex_content = {
            "type": "bubble",
            "size": "kilo",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "🖤 نتيجة التوافق",
                        "size": "xl",
                        "weight": "bold",
                        "color": "#FFFFFF",
                        "align": "center"
                    }
                ],
                "backgroundColor": "#FF69B4",
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
                                "text": f"{name1} 💘 {name2}",
                                "size": "xl",
                                "weight": "bold",
                                "color": colors["text"],
                                "align": "center",
                                "wrap": True
                            },
                            {
                                "type": "separator",
                                "margin": "lg"
                            },
                            {
                                "type": "text",
                                "text": "نسبة التوافق:",
                                "size": "sm",
                                "color": colors["text2"],
                                "align": "center",
                                "margin": "md"
                            },
                            {
                                "type": "text",
                                "text": f"{percentage}%",
                                "size": "xxl",
                                "weight": "bold",
                                "color": "#FF69B4",
                                "align": "center",
                                "margin": "sm"
                            },
                            {
                                "type": "text",
                                "text": message_text,
                                "size": "md",
                                "color": colors["text"],
                                "align": "center",
                                "wrap": True,
                                "margin": "lg"
                            }
                        ],
                        "backgroundColor": colors["card"],
                        "cornerRadius": "20px",
                        "paddingAll": "25px"
                    },
                    {
                        "type": "text",
                        "text": f"✨ نفس النسبة لو كتبت: {name2} {name1}",
                        "size": "xs",
                        "color": colors["text2"],
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
                        "layout": "horizontal",
                        "spacing": "sm",
                        "contents": [
                            {
                                "type": "button",
                                "action": {"type": "message", "label": "🔄 إعادة", "text": "لعبة توافق"},
                                "style": "primary",
                                "height": "sm",
                                "color": "#FF69B4"
                            },
                            {
                                "type": "button",
                                "action": {"type": "message", "label": "🏠 البداية", "text": "بداية"},
                                "style": "secondary",
                                "height": "sm"
                            }
                        ]
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

        result_message = self._create_flex_with_buttons("نتيجة التوافق", flex_content)
        points = self.add_score(user_id, display_name, 5)
        self.game_active = False

        return {
            'message': f"🖤 نسبة التوافق: {percentage}%",
            'response': result_message,
            'points': points,
            'game_over': True
        }

    def get_game_info(self) -> Dict[str, Any]:
        return {
            "name": "لعبة التوافق",
            "emoji": "🖤",
            "description": "اكتشف نسبة التوافق بين اسمين",
            "questions_count": 1,
            "supports_hint": False,
            "supports_reveal": False,
            "active": self.game_active,
            "players_count": len(self.scores)
        }
