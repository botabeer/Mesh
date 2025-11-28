"""
لعبة تكوين الكلمات - ستايل زجاجي احترافي
Created by: Abeer Aldosari © 2025
"""

from games.base_game import BaseGame
import random
from typing import Dict, Any, Optional


class LettersWordsGame(BaseGame):
    """لعبة تكوين الكلمات - فردي + فريقين"""

    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, questions_count=5)
        self.game_name = "تكوين"
        self.game_icon = "▫️"

        self.letter_sets = [
            {"letters": ["ق", "ل", "م", "ع", "ر", "ب"], "words": ["قلم", "عمل", "علم", "قلب", "رقم"]},
            {"letters": ["س", "ا", "ر", "ة", "ي", "م"], "words": ["سيارة", "سير", "مسار", "سارية"]},
            {"letters": ["ك", "ت", "ا", "ب", "م", "ل"], "words": ["كتاب", "كتب", "مكتب", "ملك"]},
            {"letters": ["د", "ر", "س", "ة", "م", "ا"], "words": ["مدرسة", "درس", "مدرس"]},
            {"letters": ["ح", "د", "ي", "ق", "ة", "ر"], "words": ["حديقة", "حديد", "قرد", "دقيق"]},
            {"letters": ["ب", "ي", "ت", "ك", "م", "ن"], "words": ["بيت", "كتب", "نبت", "بنت"]},
            {"letters": ["ش", "م", "س", "ي", "ر", "ع"], "words": ["شمس", "مسير", "عرش", "سير"]},
            {"letters": ["ن", "ج", "م", "ا", "ل", "ر"], "words": ["نجم", "جمال", "رجل", "نمر"]},
        ]

        random.shuffle(self.letter_sets)
        self.current_set = None
        self.found_words = set()
        self.required_words = 3

    # ----------------------------
    # بداية اللعبة
    # ----------------------------
    def start_game(self):
        self.current_question = 0
        self.game_active = True
        self.found_words.clear()
        self.previous_question = None
        self.previous_answer = None
        self.answered_users.clear()
        return self.get_question()

    # ----------------------------
    # سؤال جديد
    # ----------------------------
    def get_question(self):
        q_data = self.letter_sets[self.current_question % len(self.letter_sets)]
        self.current_set = q_data
        self.current_answer = q_data["words"]
        self.found_words.clear()

        colors = self.get_theme_colors()
        letters_display = ' - '.join(q_data["letters"])

        flex_content = {
            "type": "bubble",
            "size": "kilo",
            "body": {
                "type": "box",
                "layout": "vertical",
                "paddingAll": "24px",
                "backgroundColor": colors["bg"],
                "contents": [
                    {
                        "type": "text",
                        "text": self.game_name,
                        "size": "xl",
                        "weight": "bold",
                        "color": colors["text"],
                        "align": "center"
                    },
                    {
                        "type": "text",
                        "text": f"سؤال {self.current_question + 1} من {self.questions_count}",
                        "size": "sm",
                        "color": colors["text2"],
                        "align": "center",
                        "margin": "sm"
                    },
                    {
                        "type": "separator",
                        "margin": "lg",
                        "color": colors["shadow1"]
                    },
                    {
                        "type": "text",
                        "text": "كوّن كلمات من الحروف التالية:",
                        "size": "md",
                        "color": colors["text"],
                        "align": "center",
                        "margin": "lg"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "backgroundColor": colors["card"],
                        "cornerRadius": "20px",
                        "paddingAll": "20px",
                        "margin": "md",
                        "contents": [
                            {
                                "type": "text",
                                "text": letters_display,
                                "size": "xl",
                                "weight": "bold",
                                "color": colors["primary"],
                                "align": "center",
                                "wrap": True
                            }
                        ]
                    },
                    {
                        "type": "text",
                        "text": f"عدد الكلمات المطلوب: {self.required_words}",
                        "size": "sm",
                        "color": colors["text2"],
                        "align": "center",
                        "margin": "md"
                    }
                ]
            }
        }

        return self._create_flex_with_buttons("تكوين", flex_content)

    # ----------------------------
    # فحص الإجابة (فردي + فريقين)
    # ----------------------------
    def check_answer(self, user_answer: str, user_id: str, display_name: str):

        if not self.game_active:
            return None

        normalized = self.normalize_text(user_answer)

        # ============================
        # وضع الفريقين
        # ============================
        if self.team_mode_active:

            if user_id not in self.team_players:
                return None  # غير منضم

            if user_id in self.answered_users:
                return None

            team_id = self.team_players[user_id]

            valid_words = [self.normalize_text(w) for w in self.current_answer]

            if normalized not in valid_words or normalized in self.found_words:
                return None

            self.found_words.add(normalized)
            self.answered_users.add(user_id)
            self.add_team_score(team_id, 10)

            # اكتمال الجولة
            if len(self.found_words) >= self.required_words:
                self.previous_question = self.current_set["letters"]
                self.previous_answer = " • ".join(self.current_answer)

                self.current_question += 1
                self.found_words.clear()
                self.answered_users.clear()

                if self.current_question >= self.questions_count:
                    return self.end_team_game()

                return {
                    'message': "تم الانتقال للجولة التالية",
                    'response': self.get_question(),
                    'points': 0
                }

            return None

        # ============================
        # الوضع الفردي
        # ============================

        if normalized == 'لمح':
            remaining = [w for w in self.current_answer if self.normalize_text(w) not in self.found_words]
            if remaining:
                word = remaining[0]
                hint = f"تلميح: الكلمة من {len(word)} حروف وأولها '{word[0]}'"
            else:
                hint = "لا توجد تلميحات"
            return {'message': hint, 'response': self._create_text_message(hint), 'points': 0}

        if normalized == 'جاوب':
            words = " • ".join(self.current_answer)
            self.previous_question = self.current_set["letters"]
            self.previous_answer = words
            self.current_question += 1
            self.answered_users.clear()
            self.found_words.clear()

            if self.current_question >= self.questions_count:
                result = self.end_game()
                result['message'] = words
                return result

            return {'message': words, 'response': self.get_question(), 'points': 0}

        valid_words = [self.normalize_text(w) for w in self.current_answer]
        is_valid = normalized in valid_words and normalized not in self.found_words

        if not is_valid:
            return None

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
                result['message'] = words
                return result

            return {'message': "تم الانتقال للجولة التالية", 'response': self.get_question(), 'points': points}

        remaining = self.required_words - len(self.found_words)
        return {
            'message': f"صحيح • تبقى {remaining} كلمات",
            'response': self._create_text_message(f"تبقى {remaining} كلمات"),
            'points': points
        }
