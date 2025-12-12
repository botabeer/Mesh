from games.base_game import BaseGame
from typing import Dict, Any, Optional
import re


class CompatibilityGame(BaseGame):
    """لعبة توافق"""

    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, questions_count=1)
        self.game_name = "توافق"
        self.supports_hint = False
        self.supports_reveal = False

    def is_valid_text(self, text: str) -> bool:
        """التحقق من أن النص أسماء فقط"""
        return not bool(re.search(r"[@#0-9A-Za-z!$%^&*()_+=\[\]{};:'\"\\|,.<>/?~`]", text))

    def parse_names(self, text: str) -> tuple:
        """معالجة الأسماء"""
        text = ' '.join(text.split())
        if ' و ' in text:
            parts = text.split(' و ', 1)
            name1 = parts[0].strip()
            name2 = parts[1].strip() if len(parts) > 1 else ""
            return (name1, name2) if name1 and name2 else (None, None)
        words = text.split()
        if 'و' in words:
            idx = words.index('و')
            name1 = ' '.join(words[:idx]).strip()
            name2 = ' '.join(words[idx+1:]).strip()
            return (name1, name2) if name1 and name2 else (None, None)
        return (None, None)

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
        """رسالة التوافق"""
        if percentage >= 90:
            return "توافق عالي جداً"
        elif percentage >= 75:
            return "توافق عالي"
        elif percentage >= 60:
            return "توافق جيد"
        elif percentage >= 45:
            return "توافق متوسط"
        return "توافق منخفض"

    def start_game(self):
        """بدء اللعبة"""
        self.game_active = True
        return self.get_question()

    def get_question(self):
        """واجهة إدخال الأسماء"""
        return self.build_question_flex(
            question_text="أدخل اسمين بينهما (و)",
            additional_info="مثال: ميش و عبير"
        )

    def check_answer(self, user_answer: str, user_id: str, display_name: str) -> Optional[Dict[str, Any]]:
        """التحقق من الإجابة"""
        if not self.game_active:
            return None

        text = user_answer.strip()
        name1, name2 = self.parse_names(text)

        if not name1 or not name2:
            from linebot.v3.messaging import TextMessage
            return {
                'response': TextMessage(text="الصيغة غير صحيحة\nاكتب: اسم و اسم\nمثال: ميش و عبير"),
                'points': 0
            }

        if not self.is_valid_text(name1) or not self.is_valid_text(name2):
            from linebot.v3.messaging import TextMessage
            return {
                'response': TextMessage(text="غير مسموح بإدخال رموز او أرقام\nاكتب اسمين نصيين فقط"),
                'points': 0
            }

        percentage = self.calculate_compatibility(name1, name2)
        message_text = self.get_compatibility_message(percentage)
        colors = self.get_theme_colors()

        flex_content = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "نتيجة التوافق",
                        "size": "xxl",
                        "weight": "bold",
                        "color": colors["primary"],
                        "align": "center"
                    },
                    {"type": "separator", "margin": "lg", "color": colors["border"]},
                    {
                        "type": "text",
                        "text": f"{name1} و {name2}",
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
                        "paddingAll": "24px",
                        "backgroundColor": colors["card"],
                        "margin": "xl"
                    },
                    {
                        "type": "text",
                        "text": message_text,
                        "size": "lg",
                        "color": colors["text"],
                        "align": "center",
                        "wrap": True,
                        "margin": "md",
                        "weight": "bold"
                    },
                    {"type": "separator", "margin": "xl", "color": colors["border"]},
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "spacing": "md",
                        "margin": "xl",
                        "contents": [
                            {
                                "type": "button",
                                "action": {"type": "message", "label": "إعادة", "text": "توافق"},
                                "style": "primary",
                                "height": "sm"
                            },
                            {
                                "type": "button",
                                "action": {"type": "message", "label": "البداية", "text": "بداية"},
                                "style": "secondary",
                                "height": "sm"
                            }
                        ]
                    }
                ],
                "paddingAll": "24px",
                "spacing": "sm",
                "backgroundColor": colors["bg"]
            }
        }

        from linebot.v3.messaging import FlexMessage, FlexContainer
        result_message = FlexMessage(alt_text="نتيجة التوافق", contents=FlexContainer.from_dict(flex_content))
        self.game_active = False

        return {'response': result_message, 'points': 0, 'game_over': True}
