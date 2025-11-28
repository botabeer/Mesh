"""
لعبة لون الكلمة (Stroop Effect) - ستايل زجاجي احترافي
Created by: Abeer Aldosari © 2025
"""

from games.base_game import BaseGame
import random
from typing import Dict, Any, Optional


class WordColorGame(BaseGame):
    """لعبة لون الكلمة (Stroop Test)"""

    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, questions_count=5)
        self.game_name = "لون الكلمة"
        self.game_icon = "🎨"
        self.supports_hint = False
        self.supports_reveal = False

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

    def start_game(self):
        self.current_question = 0
        self.game_active = True
        self.previous_question = None
        self.previous_answer = None
        self.answered_users.clear()
        return self.get_question()

    def get_question(self):
        word = random.choice(self.color_names)
        color_name = random.choice([c for c in self.color_names if c != word]) if random.random() < 0.7 else word
        self.current_answer = color_name
        color_hex = self.colors[color_name]

        colors = self.get_theme_colors()
        
        previous_section = []
        if self.previous_question and self.previous_answer:
            previous_section = [
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "text", "text": "الكلمة السابقة:", "size": "xs", "color": colors["text2"], "weight": "bold"},
                        {"type": "text", "text": self.previous_question, "size": "xs", "color": colors["text2"], "wrap": True, "margin": "xs"},
                        {"type": "text", "text": f"✅ اللون كان: {self.previous_answer}", "size": "xs", "color": colors["success"], "wrap": True, "margin": "xs"}
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
            "size": "kilo",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {"type": "text", "text": f"{self.game_icon} {self.game_name}", "size": "xl", "weight": "bold", "color": colors["text"], "align": "center"},
                            {"type": "text", "text": f"جولة {self.current_question + 1} من {self.questions_count}", "size": "sm", "color": colors["text2"], "align": "center", "margin": "sm"}
                        ]
                    },
                    {"type": "separator", "margin": "lg", "color": colors["shadow1"]}
                ] + previous_section + [
                    {"type": "text", "text": "📝 ما لون هذه الكلمة؟", "size": "md", "color": colors["text"], "weight": "bold", "align": "center", "margin": "lg"},
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [{"type": "text", "text": word, "size": "xxl", "weight": "bold", "color": color_hex, "align": "center"}],
                        "backgroundColor": colors["card"],
                        "cornerRadius": "20px",
                        "paddingAll": "30px",
                        "margin": "md"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [{"type": "text", "text": "⚠️ اكتب اسم اللون، وليس الكلمة!", "size": "sm", "color": "#FF5555", "wrap": True, "align": "center"}],
                        "backgroundColor": colors["card"],
                        "cornerRadius": "15px",
                        "paddingAll": "15px",
                        "margin": "lg"
                    },
                    {"type": "button", "action": {"type": "message", "label": "⛔ إيقاف", "text": "إيقاف"}, "style": "primary", "height": "sm", "color": colors["error"], "margin": "xl"}
                ],
                "backgroundColor": colors["bg"],
                "paddingAll": "24px"
            },
            "styles": {"body": {"backgroundColor": colors["bg"]}}
        }

        return self._create_flex_with_buttons(f"{self.game_name}", flex_content)

    def check_answer(self, user_answer: str, user_id: str, display_name: str):
        if not self.game_active or user_id in self.answered_users:
            return None

        normalized = self.normalize_text(user_answer)

        if normalized in ['لمح', 'جاوب']:
            return {'message': "❌ هذه اللعبة لا تدعم التلميحات\n🎨 ركز على اللون!", 'response': self._create_text_message("❌ هذه اللعبة لا تدعم التلميحات"), 'points': 0}

        normalized_correct = self.normalize_text(self.current_answer)
        is_correct = normalized == normalized_correct

        if is_correct:
            points = self.add_score(user_id, display_name, 10)
            self.previous_question = "كلمة ملونة"
            self.previous_answer = self.current_answer
            self.current_question += 1
            self.answered_users.clear()

            if self.current_question >= self.questions_count:
                result = self.end_game()
                result['points'] = points
                result['message'] = f"✅ ممتاز يا {display_name}!\n+{points} نقطة\n\n{result.get('message', '')}"
                return result

            return {'message': f"✅ ممتاز يا {display_name}!\n+{points} نقطة", 'response': self.get_question(), 'points': points}

        return {'message': "❌ إجابة غير صحيحة، ركز على اللون!", 'response': self._create_text_message("❌ إجابة غير صحيحة"), 'points': 0}
