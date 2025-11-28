"""
لعبة تكوين الكلمات - ستايل زجاجي احترافي
Created by: Abeer Aldosari © 2025
"""

from games.base_game import BaseGame
import random
from typing import Dict, Any, Optional


class LettersWordsGame(BaseGame):
    """لعبة تكوين الكلمات"""

    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, questions_count=5)
        self.game_name = "تكوين"
        self.game_icon = "📝"

        self.letter_sets = [
            {"letters": ["ق", "ل", "م", "ع", "ر", "ب"], "words": ["قلم", "عمل", "علم", "قلب", "رقم"]},
            {"letters": ["س", "ا", "ر", "ة", "ي", "م"], "words": ["سيارة", "سير", "مسار", "سارية"]},
            {"letters": ["ك", "ت", "ا", "ب", "م", "ل"], "words": ["كتاب", "كتب", "مكتب", "ملك"]},
            {"letters": ["د", "ر", "س", "ة", "م", "ا"], "words": ["مدرسة", "درس", "مدرس"]},
            {"letters": ["ح", "د", "ي", "ق", "ة", "ر"], "words": ["حديقة", "حديد", "قرد", "دقيق"]},
            {"letters": ["ب", "ي", "ت", "ك", "م", "ن"], "words": ["بيت", "كتب", "نبت", "بنت"]},
            {"letters": ["ش", "م", "س", "ي", "ر", "ع"], "words": ["شمس", "مسير", "عرش", "سير"]},
            {"letters": ["ن", "ج", "م", "ا", "ل", "ر"], "words": ["نجم", "جمال", "رجل", "نمر"]}
        ]
        random.shuffle(self.letter_sets)
        self.current_set = None
        self.found_words = set()
        self.required_words = 3

    def start_game(self):
        self.current_question = 0
        self.game_active = True
        self.found_words.clear()
        self.previous_question = None
        self.previous_answer = None
        self.answered_users.clear()
        return self.get_question()

    def get_question(self):
        q_data = self.letter_sets[self.current_question % len(self.letter_sets)]
        self.current_set = q_data
        self.current_answer = q_data["words"]
        self.found_words.clear()

        colors = self.get_theme_colors()
        letters_display = ' - '.join(q_data["letters"])
        
        previous_section = []
        if self.previous_question and self.previous_answer:
            previous_section = [
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "text", "text": "الحروف السابقة:", "size": "xs", "color": colors["text2"], "weight": "bold"},
                        {"type": "text", "text": ' - '.join(self.previous_question), "size": "xs", "color": colors["text2"], "wrap": True, "margin": "xs"},
                        {"type": "text", "text": f"✅ الكلمات: {self.previous_answer}", "size": "xs", "color": colors["success"], "wrap": True, "margin": "xs"}
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
                            {"type": "text", "text": f"سؤال {self.current_question + 1} من {self.questions_count}", "size": "sm", "color": colors["text2"], "align": "center", "margin": "sm"}
                        ]
                    },
                    {"type": "separator", "margin": "lg", "color": colors["shadow1"]}
                ] + previous_section + [
                    {"type": "text", "text": "استخدم الحروف لتكوين كلمات:", "size": "md", "color": colors["text"], "align": "center", "wrap": True, "weight": "bold", "margin": "lg"},
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [{"type": "text", "text": letters_display, "size": "xl", "weight": "bold", "color": colors["primary"], "align": "center", "wrap": True}],
                        "backgroundColor": colors["card"],
                        "cornerRadius": "20px",
                        "paddingAll": "20px",
                        "margin": "md"
                    },
                    {"type": "text", "text": f"يجب إيجاد {self.required_words} كلمات", "size": "sm", "color": colors["text2"], "align": "center", "margin": "md"},
                    {"type": "text", "text": "💡 اكتب 'لمح' للتلميح أو 'جاوب' للإجابة", "size": "xs", "color": colors["text2"], "align": "center", "wrap": True, "margin": "md"},
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "spacing": "sm",
                        "contents": [
                            {"type": "button", "action": {"type": "message", "label": "لمح", "text": "لمح"}, "style": "secondary", "height": "sm", "color": colors["shadow1"]},
                            {"type": "button", "action": {"type": "message", "label": "جاوب", "text": "جاوب"}, "style": "secondary", "height": "sm", "color": colors["shadow1"]}
                        ],
                        "margin": "lg"
                    },
                    {"type": "button", "action": {"type": "message", "label": "إيقاف", "text": "إيقاف"}, "style": "primary", "height": "sm", "color": colors["error"], "margin": "sm"}
                ],
                "backgroundColor": colors["bg"],
                "paddingAll": "24px"
            },
            "styles": {"body": {"backgroundColor": colors["bg"]}}
        }

        return self._create_flex_with_buttons("تكوين الكلمات", flex_content)

    def check_answer(self, user_answer: str, user_id: str, display_name: str):
        if not self.game_active:
            return None

        answer = user_answer.strip()
        normalized = self.normalize_text(answer)

        if normalized == 'لمح':
            remaining = [w for w in self.current_answer if self.normalize_text(w) not in self.found_words]
            if remaining:
                word = remaining[0]
                hint = f"💡 الكلمة من {len(word)} حروف وأولها '{word[0]}'"
            else:
                hint = "لا توجد تلميحات"
            return {'message': hint, 'response': self._create_text_message(hint), 'points': 0}

        if normalized == 'جاوب':
            words = " • ".join(self.current_answer)
            msg = f"📝 الكلمات الممكنة:\n{words}"
            self.previous_question = self.current_set["letters"]
            self.previous_answer = words
            self.current_question += 1
            self.answered_users.clear()
            self.found_words.clear()

            if self.current_question >= self.questions_count:
                result = self.end_game()
                result['message'] = f"{msg}\n\n{result.get('message','')}"
                return result

            return {'message': msg, 'response': self.get_question(), 'points': 0}

        valid_words = [self.normalize_text(w) for w in self.current_answer]
        is_valid = normalized in valid_words and normalized not in self.found_words

        if not is_valid:
            return {'message': "❌ إجابة غير صحيحة أو مكررة", 'response': self._create_text_message("❌ إجابة غير صحيحة أو مكررة"), 'points': 0}

        self.found_words.add(normalized)
        points = self.add_score(user_id, display_name, 10)

        if len(self.found_words) >= self.required_words:
            words = " • ".join(self.current_answer)
            self.previous_question = self.current_set["letters"]
            self.previous_answer = words
            self.current_question += 1
            self.answered_users.clear()
            self.found_words.clear()

            if self.current_question >= self.questions_count:
                result = self.end_game()
                result['points'] = points
                result['message'] = f"✅ أحسنت يا {display_name}!\n+{points} نقطة\n\n{result.get('message','')}"
                return result

            return {'message': f"✅ أحسنت يا {display_name}!\n+{points} نقطة", 'response': self.get_question(), 'points': points}

        remaining = self.required_words - len(self.found_words)
        return {'message': f"✅ صحيح!\n+{points} نقطة\nتبقى {remaining} كلمات", 'response': self._create_text_message(f"✅ صحيح!\n+{points} نقطة\nتبقى {remaining} كلمات"), 'points': points}
