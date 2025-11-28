"""
نظام التوافق المستقل - Production Ready
Created by: Abeer Aldosari © 2025
✅ نظام مستقل (ليس لعبة)
✅ بدون نقاط
✅ بدون لمح / جاوب
✅ بدون فرق
✅ يقبل اسمين فقط بصيغة: اسم و اسم
✅ لا يقبل منشن أو رموز
✅ واجهة نتيجة مخصصة
"""

from games.base_game import BaseGame
from typing import Dict, Any, Optional
import re

class CompatibilitySystem(BaseGame):
    """نظام مستقل لحساب التوافق بين اسمين"""

    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, questions_count=1)
        self.game_name = "نظام التوافق"
        self.supports_hint = False
        self.supports_reveal = False
        self.game_active = False

    # ------------------------------------
    # التحقق من أن النص أسماء فقط
    # ------------------------------------
    def is_valid_text(self, text: str) -> bool:
        # يمنع: المنشن - الأرقام - الرموز - الإيموجي
        if re.search(r"[@#0-9A-Za-z!$%^&*()_+=\[\]{};:'\"\\|,.<>/?~`✅❌🎯🧠🏆🥇]", text):
            return False
        return True

    # ------------------------------------
    # حساب نسبة التوافق
    # ------------------------------------
    def calculate_compatibility(self, name1: str, name2: str) -> int:
        n1 = self.normalize_text(name1)
        n2 = self.normalize_text(name2)

        names = sorted([n1, n2])
        combined = ''.join(names)

        seed = sum(ord(c) * (i + 1) for i, c in enumerate(combined))
        percentage = (seed % 81) + 20  # من 20% إلى 100%

        return percentage

    # ------------------------------------
    # رسالة التوافق
    # ------------------------------------
    def get_compatibility_message(self, percentage: int) -> str:
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

    # ------------------------------------
    # بدء النظام
    # ------------------------------------
    def start_game(self):
        self.game_active = True
        return self.get_question()

    # ------------------------------------
    # واجهة الإدخال
    # ------------------------------------
    def get_question(self):
        colors = self.get_theme_colors()

        flex_content = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "نظام التوافق", "size": "xxl",
                     "weight": "bold", "color": colors["text"], "align": "center"},

                    {"type": "text", "text": "أدخل اسمين بينهما (و)",
                     "size": "sm", "color": colors["text2"],
                     "align": "center", "margin": "md"},

                    {"type": "separator", "margin": "xl", "color": colors["border"]},

                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {"type": "text", "text": "مثال:",
                             "size": "sm", "color": colors["text2"],
                             "align": "center"},

                            {"type": "text", "text": "ميش و عبير",
                             "size": "lg", "weight": "bold",
                             "color": colors["primary"],
                             "align": "center", "margin": "sm"}
                        ],
                        "cornerRadius": "20px",
                        "paddingAll": "20px",
                        "margin": "lg"
                    },

                    {"type": "text",
                     "text": "يقبل نصوص فقط بدون رموز أو منشن",
                     "size": "xs", "color": colors["text2"],
                     "align": "center", "wrap": True, "margin": "lg"}
                ],
                "paddingAll": "24px",
                "spacing": "md"
            }
        }

        return self._create_flex_with_buttons("نظام التوافق", flex_content)

    # ------------------------------------
    # معالجة الإدخال
    # ------------------------------------
    def check_answer(self, user_answer: str, user_id: str,
                     display_name: str) -> Optional[Dict[str, Any]]:

        if not self.game_active:
            return None

        text = user_answer.strip()

        # يجب أن يحتوي على "و"
        if "و" not in text:
            return {
                'response': self._create_text_message(
                    "الصيغة غير صحيحة\nاكتب: اسم و اسم\nمثال: ميش و عبير"
                ),
                'points': 0
            }

        parts = [p.strip() for p in text.split("و")]

        if len(parts) != 2:
            return {
                'response': self._create_text_message(
                    "يرجى كتابة اسمين فقط بصيغة:\nاسم و اسم"
                ),
                'points': 0
            }

        name1, name2 = parts

        # تحقق من النصوص فقط
        if not self.is_valid_text(name1) or not self.is_valid_text(name2):
            return {
                'response': self._create_text_message(
                    "❌ غير مسموح بإدخال رموز أو منشن\nاكتب اسمين نص فقط"
                ),
                'points': 0
            }

        # حساب النسبة
        percentage = self.calculate_compatibility(name1, name2)
        message_text = self.get_compatibility_message(percentage)

        colors = self.get_theme_colors()

        # --------------------------------
        # واجهة النتيجة المخصصة
        # --------------------------------
        flex_content = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [

                    {"type": "text", "text": "نتيجة التوافق",
                     "size": "xl", "weight": "bold",
                     "color": colors["text"], "align": "center"},

                    {"type": "separator", "margin": "lg", "color": colors["border"]},

                    {"type": "text", "text": f"{name1}  ×  {name2}",
                     "size": "lg", "weight": "bold",
                     "color": colors["text"], "align": "center",
                     "wrap": True, "margin": "lg"},

                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {"type": "text", "text": f"{percentage}%",
                             "size": "xxl", "weight": "bold",
                             "color": colors["primary"], "align": "center"}
                        ],
                        "cornerRadius": "25px",
                        "paddingAll": "26px",
                        "margin": "xl",
                        "backgroundColor": colors["card"]
                    },

                    {"type": "text", "text": message_text,
                     "size": "md", "color": colors["text"],
                     "align": "center", "wrap": True,
                     "margin": "lg"},

                    {"type": "text",
                     "text": f"نفس النتيجة لو كتبت: {name2} و {name1}",
                     "size": "xs", "color": colors["text2"],
                     "align": "center", "wrap": True,
                     "margin": "lg"},

                    {
                        "type": "button",
                        "action": {
                            "type": "message",
                            "label": "إعادة الحساب",
                            "text": "توافق"
                        },
                        "style": "primary",
                        "height": "sm",
                        "color": colors["primary"],
                        "margin": "xl"
                    }
                ],
                "paddingAll": "24px",
                "spacing": "md"
            }
        }

        result_message = self._create_flex_with_buttons("نتيجة التوافق", flex_content)

        self.game_active = False

        return {
            'response': result_message,
            'points': 0,
            'game_over': True
        }
