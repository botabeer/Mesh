"""
لعبة التوافق v7.0 - للترفيه فقط
تم إنشاء هذا البوت بواسطة عبير الدوسري © 2025

Features:
✅ No Points
✅ No Hints/Reveal
✅ One Round Only
✅ Clean UI
"""

from games.base_game import BaseGame
from typing import Dict, Any, Optional

class CompatibilityGame(BaseGame):
    """لعبة التوافق - للترفيه فقط"""

    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, questions_count=1)
        self.game_name = "توافق"
        self.supports_hint = False
        self.supports_reveal = False

    def calculate_compatibility(self, name1: str, name2: str) -> int:
        """حساب نسبة التوافق"""
        n1 = self.normalize_text(name1)
        n2 = self.normalize_text(name2)
        names = sorted([n1, n2])
        combined = ''.join(names)
        seed = sum(ord(c) * (i + 1) for i, c in enumerate(combined))
        return (seed % 81) + 20

    def get_compatibility_message(self, percentage: int) -> str:
        """رسالة التوافق"""
        if percentage >= 90:
            return "توافق رائع"
        elif percentage >= 75:
            return "توافق ممتاز"
        elif percentage >= 60:
            return "توافق جيد"
        elif percentage >= 45:
            return "توافق متوسط"
        else:
            return "توافق ضعيف"

    def start_game(self):
        self.current_question = 0
        self.game_active = True
        return self.get_question()

    def get_question(self):
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
                        "text": "لعبة التوافق",
                        "size": "xl",
                        "weight": "bold",
                        "color": colors["primary"],
                        "align": "center"
                    },
                    {
                        "type": "text",
                        "text": "للترفيه فقط",
                        "size": "sm",
                        "color": colors["text2"],
                        "align": "center"
                    }
                ],
                "backgroundColor": colors["card"],
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
                                "text": "اكتب اسمين مفصولين بمسافة",
                                "size": "lg",
                                "color": colors["text"],
                                "align": "center",
                                "wrap": True,
                                "weight": "bold"
                            },
                            {
                                "type": "text",
                                "text": "مثال: ميش عبير",
                                "size": "md",
                                "color": colors["primary"],
                                "align": "center",
                                "margin": "md"
                            }
                        ],
                        "backgroundColor": colors["card"],
                        "cornerRadius": "15px",
                        "paddingAll": "20px"
                    }
                ],
                "backgroundColor": colors["bg"],
                "paddingAll": "15px"
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "button",
                        "action": {"type": "message", "label": "إيقاف", "text": "إيقاف"},
                        "style": "primary",
                        "height": "sm",
                        "color": colors["error"]
                    }
                ],
                "backgroundColor": colors["card"],
                "paddingAll": "12px"
            }
        }

        return self._create_flex_with_buttons("لعبة التوافق", flex_content)

    def check_answer(self, user_answer: str, user_id: str, display_name: str) -> Optional[Dict[str, Any]]:
        if not self.game_active:
            return None

        names = user_answer.strip().split()

        if len(names) < 2:
            return {
                'response': self._create_text_message("يرجى كتابة اسمين مفصولين بمسافة"),
                'points': 0
            }

        name1, name2 = names[0], names[1]
        percentage = self.calculate_compatibility(name1, name2)
        message_text = self.get_compatibility_message(percentage)

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
                        "text": "نتيجة التوافق",
                        "size": "xl",
                        "weight": "bold",
                        "color": colors["primary"],
                        "align": "center"
                    }
                ],
                "backgroundColor": colors["card"],
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
                                "text": f"{name1} و {name2}",
                                "size": "xl",
                                "weight": "bold",
                                "color": colors["text"],
                                "align": "center",
                                "wrap": True
                            },
                            {"type": "separator", "margin": "lg", "color": colors["shadow1"]},
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
                                "color": colors["primary"],
                                "align": "center"
                            },
                            {
                                "type": "text",
                                "text": message_text,
                                "size": "md",
                                "color": colors["text"],
                                "align": "center",
                                "wrap": True,
                                "margin": "md"
                            }
                        ],
                        "backgroundColor": colors["card"],
                        "cornerRadius": "15px",
                        "paddingAll": "20px"
                    }
                ],
                "backgroundColor": colors["bg"],
                "paddingAll": "15px"
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "spacing": "sm",
                        "contents": [
                            {
                                "type": "button",
                                "action": {"type": "message", "label": "إعادة", "text": "لعبة توافق"},
                                "style": "primary",
                                "height": "sm",
                                "color": colors["primary"]
                            }
                        ]
                    }
                ],
                "backgroundColor": colors["card"],
                "paddingAll": "12px"
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
            "name": "لعبة التوافق",
            "description": "للترفيه فقط - بدون نقاط",
            "questions_count": 1,
            "supports_hint": False,
            "supports_reveal": False,
            "active": self.game_active
        }
