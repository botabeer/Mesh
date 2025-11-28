"""
لعبة التوافق - للترفيه فقط
تم إنشاء هذا البوت بواسطة عبير الدوسري © 2025

Features:
✅ جولة واحدة فقط
❌ بدون نقاط
❌ بدون لمح/جاوب
❌ بدون إعلان فائز
🎨 تصميم زجاجي احترافي
"""

from games.base_game import BaseGame
from typing import Dict, Any, Optional

class CompatibilityGame(BaseGame):
    """لعبة التوافق - حساب نسبة التوافق بين اسمين"""

    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, questions_count=1)
        self.game_name = "التوافق"
        self.supports_hint = False
        self.supports_reveal = False

    def calculate_compatibility(self, name1: str, name2: str) -> int:
        """حساب نسبة التوافق بين اسمين"""
        n1 = self.normalize_text(name1)
        n2 = self.normalize_text(name2)
        
        # ترتيب الأسماء لضمان نفس النتيجة
        names = sorted([n1, n2])
        combined = ''.join(names)
        
        # خوارزمية ذكية للحساب
        seed = sum(ord(c) * (i + 1) for i, c in enumerate(combined))
        return (seed % 81) + 20

    def get_compatibility_message(self, percentage: int) -> str:
        """رسالة التوافق"""
        if percentage >= 90:
            return "توافق عالي جداً! علاقة رائعة"
        elif percentage >= 75:
            return "توافق عالي! علاقة قوية"
        elif percentage >= 60:
            return "توافق جيد! علاقة واعدة"
        elif percentage >= 45:
            return "توافق متوسط! يحتاج عمل"
        else:
            return "توافق منخفض! قد تكون هناك تحديات"

    def start_game(self):
        self.current_question = 0
        self.game_active = True
        return self.get_question()

    def get_question(self):
        """واجهة إدخال الأسماء - تصميم زجاجي"""
        colors = self.get_theme_colors()

        flex_content = {
            "type": "bubble",
            "size": "kilo",
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
                                "text": "التوافق",
                                "size": "xxl",
                                "weight": "bold",
                                "color": colors["text"],
                                "align": "center"
                            },
                            {
                                "type": "text",
                                "text": "حساب نسبة التوافق",
                                "size": "sm",
                                "color": colors["text2"],
                                "align": "center",
                                "margin": "sm"
                            }
                        ],
                        "spacing": "xs",
                        "margin": "none",
                        "paddingAll": "0px"
                    },
                    {
                        "type": "separator",
                        "margin": "xl",
                        "color": colors["shadow1"]
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "أدخل اسمين لحساب نسبة التوافق",
                                "size": "md",
                                "color": colors["text"],
                                "align": "center",
                                "wrap": True,
                                "weight": "bold"
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "مثال: أحمد سارة",
                                        "size": "sm",
                                        "color": colors["primary"],
                                        "align": "center"
                                    }
                                ],
                                "backgroundColor": colors["card"],
                                "cornerRadius": "10px",
                                "paddingAll": "10px",
                                "margin": "md"
                            }
                        ],
                        "spacing": "md",
                        "margin": "xl"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "للترفيه فقط - بدون نقاط",
                                "size": "xs",
                                "color": colors["text2"],
                                "align": "center"
                            }
                        ],
                        "margin": "lg"
                    }
                ],
                "backgroundColor": colors["bg"],
                "paddingAll": "24px",
                "spacing": "none"
            },
            "styles": {
                "body": {
                    "backgroundColor": colors["bg"]
                }
            }
        }

        return self._create_flex_with_buttons("التوافق", flex_content)

    def check_answer(self, user_answer: str, user_id: str, display_name: str) -> Optional[Dict[str, Any]]:
        """معالجة الإجابة وإظهار النتيجة"""
        if not self.game_active:
            return None

        names = user_answer.strip().split()

        if len(names) < 2:
            return {
                'response': self._create_text_message("يرجى كتابة اسمين مفصولين بمسافة\nمثال: أحمد سارة"),
                'points': 0
            }

        name1, name2 = names[0], names[1]
        percentage = self.calculate_compatibility(name1, name2)
        message_text = self.get_compatibility_message(percentage)

        colors = self.get_theme_colors()

        # تصميم النتيجة - زجاجي احترافي
        flex_content = {
            "type": "bubble",
            "size": "kilo",
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
                                "text": "نتيجة التوافق",
                                "size": "xl",
                                "weight": "bold",
                                "color": colors["text"],
                                "align": "center"
                            }
                        ],
                        "spacing": "none",
                        "margin": "none"
                    },
                    {
                        "type": "separator",
                        "margin": "lg",
                        "color": colors["shadow1"]
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": f"{name1} و {name2}",
                                "size": "lg",
                                "weight": "bold",
                                "color": colors["text"],
                                "align": "center",
                                "wrap": True
                            }
                        ],
                        "margin": "lg"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": f"{percentage}%",
                                        "size": "xxl",
                                        "weight": "bold",
                                        "color": colors["primary"],
                                        "align": "center"
                                    }
                                ],
                                "backgroundColor": colors["card"],
                                "cornerRadius": "20px",
                                "paddingAll": "20px"
                            }
                        ],
                        "margin": "xl"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": message_text,
                                "size": "md",
                                "color": colors["text"],
                                "align": "center",
                                "wrap": True
                            }
                        ],
                        "backgroundColor": colors["card"],
                        "cornerRadius": "12px",
                        "paddingAll": "16px",
                        "margin": "lg"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": f"نفس النسبة لو كتبت: {name2} {name1}",
                                "size": "xs",
                                "color": colors["text2"],
                                "align": "center",
                                "wrap": True
                            }
                        ],
                        "margin": "lg"
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": "إعادة",
                                    "text": "توافق"
                                },
                                "style": "primary",
                                "height": "sm",
                                "color": colors["primary"]
                            }
                        ],
                        "margin": "xl"
                    }
                ],
                "backgroundColor": colors["bg"],
                "paddingAll": "24px",
                "spacing": "none"
            },
            "styles": {
                "body": {
                    "backgroundColor": colors["bg"]
                }
            }
        }

        result_message = self._create_flex_with_buttons("نتيجة التوافق", flex_content)
        self.game_active = False

        return {
            'response': result_message,
            'points': 0,  # بدون نقاط
            'game_over': True
        }

    def get_game_info(self) -> Dict[str, Any]:
        return {
            "name": "التوافق",
            "description": "حساب نسبة التوافق بين اسمين - للترفيه فقط",
            "questions_count": 1,
            "supports_hint": False,
            "supports_reveal": False,
            "active": self.game_active,
            "points": 0
        }
