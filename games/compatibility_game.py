"""
لعبة التوافق - FIXED
Created by: Abeer Aldosari © 2025
✅ تعطي نسبة التوافق بشكل صحيح
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
        
        # خوارزمية حساب النسبة
        seed = sum(ord(c) * (i + 1) for i, c in enumerate(combined))
        percentage = (seed % 81) + 20  # نسبة بين 20% و 100%
        
        return percentage

    def get_compatibility_message(self, percentage: int) -> str:
        """رسالة التوافق حسب النسبة"""
        if percentage >= 90:
            return "توافق عالي جداً - علاقة رائعة"
        elif percentage >= 75:
            return "توافق عالي - علاقة قوية"
        elif percentage >= 60:
            return "توافق جيد - علاقة واعدة"
        elif percentage >= 45:
            return "توافق متوسط - يحتاج عمل"
        else:
            return "توافق منخفض - قد تكون هناك تحديات"

    def start_game(self):
        """بدء اللعبة"""
        self.current_question = 0
        self.game_active = True
        return self.get_question()

    def get_question(self):
        """واجهة إدخال الأسماء"""
        colors = self.get_theme_colors()

        flex_content = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "التوافق", "size": "xxl", "weight": "bold", 
                     "color": colors["text"], "align": "center"},
                    {"type": "text", "text": "حساب نسبة التوافق", "size": "sm", 
                     "color": colors["text2"], "align": "center", "margin": "sm"},
                    {"type": "separator", "margin": "xl", "color": colors["border"]},
                    
                    {
                        "type": "box", "layout": "vertical",
                        "contents": [
                            {"type": "text", "text": "أدخل اسمين لحساب نسبة التوافق", 
                             "size": "md", "color": colors["text"], "align": "center", "wrap": True, 
                             "weight": "bold"},
                            {"type": "text", "text": "مثال: ميش عبير", "size": "sm", 
                             "color": colors["primary"], "align": "center", "margin": "md"}
                        ],
                        "cornerRadius": "15px",
                        "paddingAll": "20px",
                        "margin": "lg"
                    },
                    
                    {"type": "text", "text": "للترفيه فقط - بدون نقاط", 
                     "size": "xs", "color": colors["text2"], "align": "center", "margin": "lg"}
                ],
                "paddingAll": "24px",
                "spacing": "md"
            }
        }

        return self._create_flex_with_buttons("التوافق", flex_content)

    def check_answer(self, user_answer: str, user_id: str, display_name: str) -> Optional[Dict[str, Any]]:
        """معالجة الإجابة وإظهار نسبة التوافق"""
        if not self.game_active:
            return None

        names = user_answer.strip().split()

        if len(names) < 2:
            return {
                'response': self._create_text_message("يرجى كتابة اسمين مفصولين بمسافة\nمثال: ميش عبير"),
                'points': 0
            }

        name1, name2 = names[0], names[1]
        
        # حساب نسبة التوافق
        percentage = self.calculate_compatibility(name1, name2)
        message_text = self.get_compatibility_message(percentage)

        colors = self.get_theme_colors()

        # تصميم النتيجة
        flex_content = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "نتيجة التوافق", "size": "xl", "weight": "bold", 
                     "color": colors["text"], "align": "center"},
                    {"type": "separator", "margin": "lg", "color": colors["border"]},
                    
                    {"type": "text", "text": f"{name1} و {name2}", "size": "lg", 
                     "weight": "bold", "color": colors["text"], "align": "center", 
                     "wrap": True, "margin": "lg"},
                    
                    {
                        "type": "box", "layout": "vertical",
                        "contents": [
                            {"type": "text", "text": f"{percentage}%", "size": "xxl", 
                             "weight": "bold", "color": colors["primary"], "align": "center"}
                        ],
                        "cornerRadius": "20px",
                        "paddingAll": "25px",
                        "margin": "xl"
                    },
                    
                    {"type": "text", "text": message_text, "size": "md",
                     "color": colors["text"], "align": "center", "wrap": True,
                     "margin": "lg"},
                    
                    {"type": "text", "text": f"نفس النسبة لو كتبت: {name2} {name1}", 
                     "size": "xs", "color": colors["text2"], "align": "center", 
                     "wrap": True, "margin": "lg"},
                    
                    {
                        "type": "button",
                        "action": {"type": "message", "label": "إعادة", "text": "توافق"},
                        "style": "primary", "height": "sm", "color": colors["primary"],
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
