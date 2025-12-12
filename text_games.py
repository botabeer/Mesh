"""
العاب نصية - Bot Mesh
العاب لا تتطلب اجابات صحيحة
"""

from games.base_game import BaseGame
from linebot.v3.messaging import FlexMessage, FlexContainer
import random
from typing import Dict, Any, Optional
from pathlib import Path


class TextGame(BaseGame):
    """قاعدة موحدة للألعاب النصية"""

    def __init__(self, line_bot_api, file_name: str, game_name: str):
        super().__init__(line_bot_api, questions_count=1)
        self.game_name = game_name
        self.supports_hint = False
        self.supports_reveal = False

        # تحميل العناصر مرة واحدة فقط
        self.items = self._load_items(file_name)
        if not self.items:
            self.items = [f"{game_name} - لا يوجد محتوى"]

        random.shuffle(self.items)
        self.used_items = []

    # ----------------------------------------------------------------------

    def _load_items(self, file_name: str) -> list:
        """تحميل العناصر من ملف نصي"""
        try:
            # مجلد الألعاب
            base_path = Path(__file__).parent
            file_path = base_path / file_name

            # fallback إذا تم تشغيل البوت من جذر المشروع
            if not file_path.exists():
                file_path = Path("games") / file_name

            if not file_path.exists():
                return []

            with open(file_path, "r", encoding="utf-8") as f:
                return [line.strip() for line in f if line.strip()]

        except Exception as e:
            print(f"Error loading {file_name}: {e}")
            return []

    # ----------------------------------------------------------------------

    def start_game(self):
        """بدء اللعبة"""
        self.game_active = True
        return self.get_question()

    # ----------------------------------------------------------------------

    def _pick_random_item(self) -> str:
        """اختيار عنصر جديد غير مكرر"""
        available = [x for x in self.items if x not in self.used_items]

        if not available:
            self.used_items.clear()
            random.shuffle(self.items)
            available = self.items.copy()

        item = random.choice(available)
        self.used_items.append(item)
        return item

    # ----------------------------------------------------------------------

    def get_question(self):
        """بناء رسالة اللعبة"""
        item = self._pick_random_item()
        colors = self.get_theme_colors()

        flex_dict = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "paddingAll": "24px",
                "backgroundColor": colors["bg"],
                "contents": [
                    {
                        "type": "text",
                        "text": self.game_name,
                        "size": "xxl",
                        "weight": "bold",
                        "color": colors["primary"],
                        "align": "center"
                    },
                    {"type": "separator", "margin": "lg", "color": colors["border"]},

                    # بطاقة المحتوى
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "lg",
                        "paddingAll": "20px",
                        "cornerRadius": "15px",
                        "backgroundColor": colors["card"],
                        "borderColor": colors["primary"],
                        "borderWidth": "2px",
                        "contents": [
                            {
                                "type": "text",
                                "text": item,
                                "size": "lg",
                                "weight": "bold",
                                "color": colors["text"],
                                "align": "center",
                                "wrap": True
                            }
                        ]
                    },

                    {"type": "separator", "margin": "xl", "color": colors["border"]},

                    # أزرار التحكم
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "spacing": "sm",
                        "margin": "lg",
                        "contents": [
                            {
                                "type": "button",
                                "style": "primary",
                                "height": "sm",
                                "color": colors["primary"],
                                "action": {
                                    "type": "message",
                                    "label": "اعادة",
                                    "text": self.game_name
                                }
                            },
                            {
                                "type": "button",
                                "style": "secondary",
                                "height": "sm",
                                "action": {
                                    "type": "message",
                                    "label": "بداية",
                                    "text": "بداية"
                                }
                            }
                        ]
                    }
                ]
            }
        }

        return FlexMessage(
            alt_text=f"{self.game_name}: {item[:50]}",
            contents=FlexContainer.from_dict(flex_dict)
        )

    # ----------------------------------------------------------------------

    def check_answer(self, user_answer: str, user_id: str,
                     display_name: str) -> Optional[Dict[str, Any]]:
        """الألعاب النصية لا تتطلب فحص إجابات"""
        return None


# ========== الألعاب الجاهزة ==========

class QuestionGame(TextGame):
    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, "questions.txt", "سؤال")


class MentionGame(TextGame):
    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, "mentions.txt", "منشن")


class ChallengeGame(TextGame):
    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, "challenges.txt", "تحدي")


class ConfessionGame(TextGame):
    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, "confessions.txt", "اعتراف")
