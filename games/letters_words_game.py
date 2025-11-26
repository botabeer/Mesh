"""
لعبة تكوين الكلمات - النسخة المحسنة النهائية
Created by: Abeer Aldosari © 2025

الميزات:
✅ AI أولاً مع Fallback قوي
✅ مجموعات حروف متنوعة
✅ واجهة Flex احترافية
✅ تشفير عربي مثالي
✅ أداء محسن
"""

from games.base_game import BaseGame
import random
import difflib
from typing import Dict, Any, Optional


class LettersWordsGame(BaseGame):
    """لعبة تكوين الكلمات المحسنة مع AI"""

    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, questions_count=5)
        self.game_name = "تكوين كلمات"
        self.game_icon = "🔤"

        self.fallback_letter_sets = [
            {"letters": ["ق", "ل", "م", "ع", "ر", "ب"], "words": ["قلم", "عمل", "علم", "قلب", "رقم", "مقر"]},
            {"letters": ["س", "ا", "ر", "ة", "ي", "م"], "words": ["سيارة", "سارية", "رئيس", "سير", "مسار"]},
            {"letters": ["ك", "ت", "ا", "ب", "م", "ل"], "words": ["كتاب", "كتب", "مكتب", "كلام", "ملك"]},
            {"letters": ["د", "ر", "س", "ة", "م", "ا"], "words": ["مدرسة", "درس", "مدرس", "سادر"]},
            {"letters": ["ح", "د", "ي", "ق", "ة", "ر"], "words": ["حديقة", "حديد", "قرد", "دقيق"]},
            {"letters": ["ب", "ي", "ت", "ك", "م", "ن"], "words": ["بيت", "كتب", "نبت", "بنت"]},
            {"letters": ["ش", "م", "س", "ي", "ر", "ع"], "words": ["شمس", "مسير", "عرش", "سير"]},
            {"letters": ["ن", "ج", "م", "ا", "ل", "ر"], "words": ["نجم", "جمال", "رجل", "نمر"]}
        ]

        random.shuffle(self.fallback_letter_sets)
        self.current_set = None
        self.found_words = set()
        self.required_words = 3
        self.previous_question = None
        self.previous_answer = None

    def generate_question_with_ai(self):
        """توليد سؤال بالذكاء الاصطناعي مع Fallback"""
        question_data = None

        # محاولة AI أولاً
        if self.ai_generate_question:
            try:
                question_data = self.ai_generate_question()
                if question_data and "letters" in question_data and "words" in question_data:
                    return question_data
            except Exception as e:
                print(f"⚠️ AI generation failed, using fallback: {e}")

        # Fallback
        return self.fallback_letter_sets[self.current_question % len(self.fallback_letter_sets)]

    def start_game(self):
        """بدء اللعبة"""
        self.current_question = 0
        self.game_active = True
        self.found_words.clear()
        self.previous_question = None
        self.previous_answer = None
        self.answered_users.clear()
        return self.get_question()

    def get_question(self):
        """إنشاء سؤال مع واجهة Flex محسنة"""
        q_data = self.generate_question_with_ai()
        self.current_set = q_data
        self.current_answer = q_data["words"]
        self.found_words.clear()

        colors = self.get_theme_colors()
        letters_display = ' - '.join(q_data["letters"])

        # قسم السؤال السابق
        previous_section = []
        if self.previous_question and self.previous_answer:
            previous_section = [
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "📝 الحروف السابقة:",
                            "size": "xs",
                            "color": colors["text2"],
                            "weight": "bold"
                        },
                        {
                            "type": "text",
                            "text": ' - '.join(self.previous_question),
                            "size": "xs",
                            "color": colors["text2"],
                            "wrap": True,
                            "margin": "xs"
                        },
                        {
                            "type": "text",
                            "text": f"✅ الكلمات: {self.previous_answer}",
                            "size": "xs",
                            "color": colors["success"],
                            "wrap": True,
                            "margin": "xs"
                        }
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
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": f"{self.game_icon} {self.game_name}",
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
                        "align": "center"
                    }
                ],
                "backgroundColor": colors["bg"],
                "paddingAll": "20px"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "lg",
                "contents": previous_section + [
                    {
                        "type": "text",
                        "text": "استخدم الحروف التالية لتكوين الكلمات:",
                        "size": "md",
                        "color": colors["text"],
                        "align": "center",
                        "wrap": True
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
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
                        ],
                        "backgroundColor": colors["card"],
                        "cornerRadius": "20px",
                        "paddingAll": "20px"
                    },
                    {
                        "type": "text",
                        "text": f"يجب إيجاد {self.required_words} كلمات",
                        "size": "sm",
                        "color": colors["text2"],
                        "align": "center"
                    },
                    {
                        "type": "text",
                        "text": "💡 اكتب 'لمح' للتلميح أو 'جاوب' للإجابة",
                        "size": "xs",
                        "color": colors["text2"],
                        "align": "center",
                        "wrap": True
                    }
                ],
                "backgroundColor": colors["bg"],
                "paddingAll": "15px"
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "spacing": "sm",
                        "contents": [
                            {
                                "type": "button",
                                "action": {"type": "message", "label": "💡 لمّح", "text": "لمح"},
                                "style": "secondary",
                                "height": "sm",
                                "color": colors["shadow1"]
                            },
                            {
                                "type": "button",
                                "action": {"type": "message", "label": "🔍 جاوب", "text": "جاوب"},
                                "style": "secondary",
                                "height": "sm",
                                "color": colors["shadow1"]
                            }
                        ]
                    },
                    {
                        "type": "button",
                        "action": {"type": "message", "label": "⛔ إيقاف", "text": "إيقاف"},
                        "style": "primary",
                        "height": "sm",
                        "color": colors["error"]
                    }
                ],
                "backgroundColor": colors["bg"],
                "paddingAll": "15px"
            },
            "styles": {
                "body": {"backgroundColor": colors["bg"]},
                "footer": {"backgroundColor": colors["bg"]}
            }
        }

        return self._create_flex_with_buttons("تكوين الكلمات", flex_content)

    def check_answer(self, user_answer: str, user_id: str, display_name: str) -> Optional[Dict[str, Any]]:
        """فحص الإجابة"""
        if not self.game_active:
            return None

        answer = user_answer.strip()
        normalized = self.normalize_text(answer)

        # التلميح
        if normalized == 'لمح':
            remaining = [w for w in self.current_answer if self.normalize_text(w) not in self.found_words]
            if remaining:
                word = remaining[0]
                hint = f"💡 الكلمة من {len(word)} حروف وأولها '{word[0]}'"
            else:
                hint = "لا توجد تلميحات"
            return {
                'message': hint,
                'response': self._create_text_message(hint),
                'points': 0
            }

        # كشف الإجابة
        if normalized == 'جاوب':
            words = " • ".join(self.current_answer)
            msg = f"📝 الكلمات الممكنة:\n{words}"

            # حفظ السؤال والجواب
            self.previous_question = self.current_set["letters"]
            self.previous_answer = words

            # الانتقال للسؤال التالي
            self.current_question += 1
            self.answered_users.clear()
            self.found_words.clear()

            if self.current_question >= self.questions_count:
                result = self.end_game()
                result['message'] = f"{msg}\n\n{result.get('message','')}"
                return result

            next_q = self.get_question()
            return {'message': msg, 'response': next_q, 'points': 0}

        # التحقق من الإجابة
        valid_words = [self.normalize_text(w) for w in self.current_answer]
        is_valid = False

        if normalized in valid_words and normalized not in self.found_words:
            is_valid = True
        else:
            for w in valid_words:
                if difflib.SequenceMatcher(None, normalized, w).ratio() > 0.8:
                    if normalized not in self.found_words:
                        is_valid = True
                    break

        if not is_valid:
            return {
                'message': "❌ إجابة غير صحيحة أو مكررة",
                'response': self._create_text_message("❌ إجابة غير صحيحة أو مكررة"),
                'points': 0
            }

        self.found_words.add(normalized)
        points = self.add_score(user_id, display_name, 10)

        if len(self.found_words) >= self.required_words:
            # حفظ السؤال والجواب
            words = " • ".join(self.current_answer)
            self.previous_question = self.current_set["letters"]
            self.previous_answer = words

            # الانتقال للسؤال التالي
            self.current_question += 1
            self.answered_users.clear()
            self.found_words.clear()

            if self.current_question >= self.questions_count:
                result = self.end_game()
                result['points'] = points
                result['message'] = f"✅ أحسنت يا {display_name}!\n+{points} نقطة\n\n{result.get('message','')}"
                return result

            next_q = self.get_question()
            return {
                'message': f"✅ أحسنت يا {display_name}!\n+{points} نقطة",
                'response': next_q,
                'points': points
            }

        remaining = self.required_words - len(self.found_words)
        msg = f"✅ صحيح!\n+{points} نقطة\nتبقى {remaining} كلمات"
        return {
            'message': msg,
            'response': self._create_text_message(msg),
            'points': points
        }

    def get_game_info(self) -> Dict[str, Any]:
        """معلومات اللعبة"""
        return {
            "name": "لعبة تكوين الكلمات",
            "emoji": "🔤",
            "description": "كوّن كلمات من الحروف المعطاة مع دعم AI",
            "questions_count": self.questions_count,
            "required_words": self.required_words,
            "found_words_count": len(self.found_words),
            "supports_hint": True,
            "supports_reveal": True,
            "active": self.game_active,
            "current_question": self.current_question,
            "players_count": len(self.scores),
            "ai_enabled": self.ai_generate_question is not None
        }
