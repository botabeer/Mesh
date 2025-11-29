from games.base_game import BaseGame
from typing import Dict, Any, Optional
import re


class CompatibilitySystem(BaseGame):
    """نظام مستقل لحساب التوافق بين اسمين"""

    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, questions_count=1)
        self.game_name = "توافق"
        self.game_icon = "▫️"
        self.supports_hint = False
        self.supports_reveal = False

    def is_valid_text(self, text: str) -> bool:
        """التحقق من أن النص أسماء فقط (بدون رموز أو منشن)"""
        if re.search(r"[@#0-9A-Za-z!$%^&*()_+=\[\]{};:'\"\\|,.<>/?~`]", text):
            return False
        return True

    def calculate_compatibility(self, name1: str, name2: str) -> int:
        """حساب نسبة التوافق"""
        n1 = self.normalize_text(name1)
        n2 = self.normalize_text(name2)

        names = sorted([n1, n2])
        combined = ''.join(names)

        seed = sum(ord(c) * (i + 1) for i, c in enumerate(combined))
        percentage = (seed % 81) + 20

        return percentage

    def get_compatibility_message(self, percentage: int) -> str:
        """رسالة التوافق حسب النسبة"""
        if percentage >= 90:
            return "توافق عالي جداً"
        elif percentage >= 75:
            return "توافق عالي"
        elif percentage >= 60:
            return "توافق جيد"
        elif percentage >= 45:
            return "توافق متوسط"
        else:
            return "توافق منخفض"

    def start_game(self):
        """بدء النظام"""
        self.game_active = True
        return self.get_question()

    def get_question(self):
        """واجهة الإدخال"""
        colors = self.get_theme_colors()

        return self.build_question_flex(
            question_text="أدخل اسمين بينهما (و)\n\nمثال:\nميش و عبير",
            additional_info="تحذير: نصوص فقط، بدون رموز أو منشن"
        )

    def check_answer(self, user_answer: str, user_id: str, display_name: str) -> Optional[Dict[str, Any]]:
        if not self.game_active:
            return None

        text = user_answer.strip()

        if "و" not in text:
            return {
                'response': self._create_text_message(
                    "الصيغة غير صحيحة\n\n"
                    "اكتب: اسم و اسم\n"
                    "مثال: ميش و عبير"
                ),
                'points': 0
            }

        parts = [p.strip() for p in text.split("و")]

        if len(parts) != 2:
            return {
                'response': self._create_text_message(
                    "يرجى كتابة اسمين فقط\n\n"
                    "الصيغة: اسم و اسم"
                ),
                'points': 0
            }

        name1, name2 = parts

        if not self.is_valid_text(name1) or not self.is_valid_text(name2):
            return {
                'response': self._create_text_message(
                    "غير مسموح بإدخال:\n"
                    "- رموز\n"
                    "- منشن\n"
                    "- أرقام\n\n"
                    "اكتب اسمين نص فقط"
                ),
                'points': 0
            }

        if not name1 or not name2:
            return {
                'response': self._create_text_message(
                    "الأسماء لا يمكن أن تكون فارغة"
                ),
                'points': 0
            }

        percentage = self.calculate_compatibility(name1, name2)
        message_text = self.get_compatibility_message(percentage)

        colors = self.get_theme_colors()

        result_flex = {
            "type": "bubble",
            "size": "kilo",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": " نتيجة التوافق",
                        "size": "xl",
                        "weight": "bold",
                        "color": colors["primary"],
                        "align": "center"
                    },
                    
                    {
                        "type": "separator",
                        "margin": "lg"
                    },
                    
                    {
                        "type": "text",
                        "text": f"{name1}  🖤  {name2}",
                        "size": "lg",
                        "weight": "bold",
                        "color": colors["text"],
                        "align": "center",
                        "wrap": True,
                        "margin": "lg"
                    },
                    
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
                        "cornerRadius": "25px",
                        "paddingAll": "20px",
                        "margin": "xl"
                    },
                    
                    {
                        "type": "text",
                        "text": message_text,
                        "size": "md",
                        "color": colors["text"],
                        "align": "center",
                        "wrap": True,
                        "margin": "md"
                    },
                    
                    {
                        "type": "text",
                        "text": f"نفس النتيجة لو كتبت:\n{name2} و {name1}",
                        "size": "xs",
                        "color": colors["text2"],
                        "align": "center",
                        "wrap": True,
                        "margin": "lg"
                    },
                    
                    {
                        "type": "button",
                        "action": {
                            "type": "message",
                            "label": "إعادة الحساب",
                            "text": "توافق"
                        },
                        "style": "primary",
                        "height": "sm",
                        "margin": "xl"
                    }
                ],
                "paddingAll": "24px",
                "spacing": "sm"
            }
        }

        result_message = self._create_flex_with_buttons("نتيجة التوافق", result_flex)

        self.game_active = False

        return {
            'response': result_message,
            'points': 0,
            'game_over': True
        }

    def get_game_info(self) -> Dict[str, Any]:
        """معلومات النظام"""
        return {
            "name": self.game_name,
            "description": "نظام مستقل لحساب التوافق",
            "is_game": False,
            "supports_hint": False,
            "supports_reveal": False,
            "has_timer": False,
            "has_points": False,
            "team_mode": False
        }
