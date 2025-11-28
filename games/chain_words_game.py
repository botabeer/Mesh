"""
لعبة سلسلة الكلمات - ستايل زجاجي احترافي
Created by: Abeer Aldosari © 2025
"""

from games.base_game import BaseGame
import random
from typing import Dict, Any, Optional


class ChainWordsGame(BaseGame):
    """لعبة سلسلة الكلمات"""

    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, questions_count=5)
        self.game_name = "سلسلة كلمات"
        self.game_icon = "🔗"
        self.supports_hint = False
        self.supports_reveal = False

        self.starting_words = [
            "سيارة", "تفاح", "قلم", "نجم", "كتاب", "باب", "رمل",
            "لعبة", "حديقة", "ورد", "دفتر", "معلم", "منزل", "شمس",
            "سفر", "رياضة", "علم", "مدرسة", "طائرة", "عصير"
        ]
        self.last_word = None
        self.used_words = set()

    def start_game(self):
        self.current_question = 0
        self.game_active = True
        self.last_word = random.choice(self.starting_words)
        self.used_words.add(self.normalize_text(self.last_word))
        self.answered_users.clear()
        return self.get_question()

    def get_question(self):
        colors = self.get_theme_colors()
        required_letter = self.last_word[-1]

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
                            {"type": "text", "text": f"سؤال {self.current_question + 1} من {self.questions_count}", "size": "sm", "color": colors["text2"], "align": "center", "margin": "xs"}
                        ]
                    },
                    {"type": "separator", "margin": "lg", "color": colors["shadow1"]},
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {"type": "text", "text": "📝 الكلمة السابقة:", "size": "sm", "color": colors["text2"], "align": "center"},
                            {"type": "text", "text": self.last_word, "size": "xxl", "weight": "bold", "color": colors["primary"], "align": "center", "margin": "md"}
                        ],
                        "backgroundColor": colors["card"],
                        "cornerRadius": "20px",
                        "paddingAll": "20px",
                        "margin": "lg"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {"type": "text", "text": "🔤 اكتب كلمة تبدأ بحرف:", "size": "md", "color": colors["text"], "align": "center"},
                            {"type": "text", "text": required_letter, "size": "xxl", "weight": "bold", "color": colors["primary"], "align": "center", "margin": "sm"}
                        ],
                        "backgroundColor": colors["card"],
                        "cornerRadius": "20px",
                        "paddingAll": "20px",
                        "margin": "md"
                    },
                    {"type": "text", "text": "⚠️ لا تكرر الكلمات", "size": "xs", "color": colors["text2"], "align": "center", "margin": "md"},
                    {"type": "button", "action": {"type": "message", "label": "⛔ إيقاف", "text": "إيقاف"}, "style": "primary", "height": "sm", "color": colors["error"], "margin": "xl"}
                ],
                "backgroundColor": colors["bg"],
                "paddingAll": "24px",
                "spacing": "none"
            },
            "styles": {"body": {"backgroundColor": colors["bg"]}}
        }

        return self._create_flex_with_buttons("سلسلة الكلمات", flex_content)

    def check_answer(self, user_answer: str, user_id: str, display_name: str) -> Optional[Dict[str, Any]]:
        if not self.game_active:
            return None

        normalized_answer = self.normalize_text(user_answer)

        if normalized_answer in ['لمح', 'جاوب']:
            return {'message': "❌ هذه اللعبة لا تدعم التلميحات", 'response': self._create_text_message("❌ هذه اللعبة لا تدعم التلميحات"), 'points': 0}

        if normalized_answer in self.used_words:
            return {'message': f"❌ الكلمة '{user_answer}' مستخدمة من قبل!", 'response': self._create_text_message(f"❌ الكلمة '{user_answer}' مستخدمة من قبل!"), 'points': 0}

        required_letter = self.normalize_text(self.last_word[-1])
        if normalized_answer and normalized_answer[0] == required_letter and len(normalized_answer) >= 2:
            self.used_words.add(normalized_answer)
            self.last_word = user_answer.strip()
            points = self.add_score(user_id, display_name, 10)
            self.current_question += 1
            self.answered_users.clear()

            if self.current_question >= self.questions_count:
                result = self.end_game()
                result['points'] = points
                result['message'] = f"✅ ممتاز يا {display_name}!\n+{points} نقطة\n\n{result.get('message', '')}"
                return result

            return {'message': f"✅ ممتاز يا {display_name}!\n+{points} نقطة", 'response': self.get_question(), 'points': points}

        return {'message': f"❌ الكلمة يجب أن تبدأ بحرف '{required_letter}'", 'response': self._create_text_message(f"❌ الكلمة يجب أن تبدأ بحرف '{required_letter}'"), 'points': 0}
