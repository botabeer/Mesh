from games.base_game import BaseGame
from typing import Dict, Any, Optional
import re

class CompatibilityGame(BaseGame):
    """لعبة توافق (للترفيه فقط)"""

    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, questions_count=1)
        self.game_name = "توافق"
        self.supports_hint = False
        self.supports_reveal = False
        self.points_enabled = False
        self.game_active = False

    # ======================== Utilities ========================
    def normalize_name(self, name: str) -> str:
        """تنظيف الاسم من المسافات الزائدة"""
        return ' '.join(name.strip().split())

    def is_valid_text(self, text: str) -> bool:
        """التأكد أن الاسم نص فقط بدون رموز أو أرقام"""
        return not bool(re.search(r"[^ء-ي\s]", text))

    def parse_names(self, text: str) -> tuple:
        """استخراج الاسمين من النص المدخل"""
        text = ' '.join(text.strip().split())
        parts = re.split(r'\sو\s', text)
        if len(parts) == 2:
            name1, name2 = self.normalize_name(parts[0]), self.normalize_name(parts[1])
            if name1 and name2:
                return name1, name2
        return None, None

    def calculate_compatibility(self, name1: str, name2: str) -> int:
        """حساب نسبة التوافق بشكل ثابت لكل زوج أسماء"""
        names = sorted([self.normalize_name(name1), self.normalize_name(name2)])
        combined = ''.join(names)
        seed = sum(ord(c) * (i + 1) for i, c in enumerate(combined))
        return (seed % 81) + 20

    def get_compatibility_message(self, percentage: int) -> str:
        if percentage >= 90: return "توافق عالي جداً"
        if percentage >= 75: return "توافق عالي"
        if percentage >= 60: return "توافق جيد"
        if percentage >= 45: return "توافق متوسط"
        return "توافق منخفض"

    # ======================== Game Flow ========================
    def start_game(self):
        self.game_active = True
        return self.get_question()

    def get_question(self):
        """عرض واجهة إدخال الأسماء"""
        return self.build_question_flex(
            question_text="أدخل اسمين بينهما (و)",
            additional_info="مثال: ميش و عبير"
        )

    def check_answer(self, user_answer: str, user_id: str, display_name: str) -> Optional[Dict[str, Any]]:
        """معالجة الإجابة وعرض النتيجة"""
        if not self.game_active:
            return None

        name1, name2 = self.parse_names(user_answer)
        if not name1 or not name2:
            from linebot.v3.messaging import TextMessage
            return {'response': TextMessage(text="الصيغة غير صحيحة\nاكتب: اسم و اسم\nمثال: ميش و عبير"), 'points': 0}

        if not self.is_valid_text(name1) or not self.is_valid_text(name2):
            from linebot.v3.messaging import TextMessage
            return {'response': TextMessage(text="غير مسموح بإدخال رموز او أرقام\nاكتب اسمين نصيين فقط"), 'points': 0}

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
                    {"type": "text","text": "نتيجة التوافق","size": "xxl","weight": "bold","color": colors["primary"],"align": "center"},
                    {"type": "separator","margin": "lg","color": colors["border"]},
                    {"type": "text","text": f"{name1} و {name2}","size": "lg","weight": "bold","color": colors["text"],"align": "center","wrap": True,"margin": "lg"},
                    {"type": "box","layout": "vertical","contents":[{"type":"text","text": f"{percentage}%","size":"xxl","weight":"bold","color": colors["primary"],"align":"center"}],"cornerRadius":"25px","paddingAll":"24px","backgroundColor": colors["card"],"margin":"xl"},
                    {"type": "text","text": message_text,"size":"lg","color": colors["text"],"align":"center","wrap": True,"margin": "md","weight":"bold"},
                    {"type": "separator","margin": "xl","color": colors["border"]},
                    {"type": "box","layout": "horizontal","spacing": "md","margin": "xl","contents":[
                        {"type":"button","action":{"type":"message","label":"إعادة","text":"توافق"},"style":"primary","height":"sm"},
                        {"type":"button","action":{"type":"message","label":"البداية","text":"بداية"},"style":"secondary","height":"sm"}
                    ]}
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
