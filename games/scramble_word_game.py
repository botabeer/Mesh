"""
لعبة الكلمة المبعثرة - النسخة المحسنة النهائية
Created by: Abeer Aldosari © 2025

الميزات:
✅ AI أولاً مع Fallback قوي
✅ خوارزمية بعثرة ذكية
✅ واجهة Flex احترافية
✅ تشفير عربي مثالي
✅ أداء محسن
"""

from games.base_game import BaseGame
import random
import difflib
from typing import Dict, Any, Optional


class ScrambleWordGame(BaseGame):
    """لعبة الكلمة المبعثرة المحسنة مع AI"""

    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, questions_count=5)
        self.game_name = "كلمة مبعثرة"
        self.game_icon = "🔤"

        # قاعدة كلمات محسنة ومتنوعة
        self.fallback_words = [
            "مدرسة", "كتاب", "قلم", "باب", "نافذة", "طاولة", "كرسي",
            "سيارة", "طائرة", "قطار", "سفينة", "دراجة",
            "تفاحة", "موز", "برتقال", "عنب", "بطيخ", "فراولة",
            "شمس", "قمر", "نجمة", "سماء", "بحر", "جبل", "نهر",
            "أسد", "نمر", "فيل", "زرافة", "حصان", "غزال",
            "ورد", "شجرة", "زهرة", "عشب", "ورقة",
            "منزل", "مسجد", "حديقة", "ملعب", "مطعم", "مكتبة",
            "صديق", "عائلة", "أخ", "أخت", "والد", "والدة",
            "كمبيوتر", "هاتف", "تلفاز", "ساعة", "راديو"
        ]

        random.shuffle(self.fallback_words)
        self.used_words = []
        self.previous_question = None
        self.previous_answer = None

    def scramble_word(self, word: str) -> str:
        """بعثرة الكلمة بطريقة ذكية"""
        letters = list(word)

        # محاولة بعثرة الكلمة حتى تختلف عن الأصل
        attempts = 0
        while attempts < 10:
            random.shuffle(letters)
            scrambled = ''.join(letters)
            if scrambled != word:
                return scrambled
            attempts += 1

        # إذا لم تنجح البعثرة، اعكس الكلمة
        return word[::-1]

    def generate_question_with_ai(self):
        """توليد سؤال بالذكاء الاصطناعي مع Fallback"""
        question_data = None

        # محاولة AI أولاً
        if self.ai_generate_question:
            try:
                question_data = self.ai_generate_question()
                if question_data and "word" in question_data:
                    return question_data
            except Exception as e:
                print(f"⚠️ AI generation failed, using fallback: {e}")

        # Fallback للكلمات المخزنة
        available = [w for w in self.fallback_words if w not in self.used_words]
        if not available:
            self.used_words = []
            available = self.fallback_words.copy()

        word = random.choice(available)
        self.used_words.append(word)

        return {"word": word}

    def start_game(self):
        """بدء اللعبة"""
        self.current_question = 0
        self.game_active = True
        self.previous_question = None
        self.previous_answer = None
        self.answered_users.clear()
        return self.get_question()

    def get_question(self):
        """إنشاء سؤال مع واجهة Flex محسنة"""
        q_data = self.generate_question_with_ai()
        word = q_data["word"]
        self.current_answer = word
        scrambled = self.scramble_word(word)

        colors = self.get_theme_colors()

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
                            "text": "📝 الكلمة السابقة:",
                            "size": "xs",
                            "color": colors["text2"],
                            "weight": "bold"
                        },
                        {
                            "type": "text",
                            "text": self.previous_question,
                            "size": "xs",
                            "color": colors["text2"],
                            "wrap": True,
                            "margin": "xs"
                        },
                        {
                            "type": "text",
                            "text": f"✅ الجواب: {self.previous_answer}",
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

        # بناء صناديق الحروف
        letter_boxes = []
        for i in range(0, len(scrambled), 4):
            chunk = scrambled[i:i+4]
            row = {
                "type": "box",
                "layout": "horizontal",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": letter,
                                "size": "xl",
                                "weight": "bold",
                                "color": colors["primary"],
                                "align": "center"
                            }
                        ],
                        "backgroundColor": colors["card"],
                        "cornerRadius": "15px",
                        "paddingAll": "15px",
                        "flex": 1
                    }
                    for letter in chunk
                ]
            }
            letter_boxes.append(row)

        flex_content = {
            "type": "bubble",
            "size": "mega",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": f"{self.game_icon} {self.game_name}",
                                "size": "xl",
                                "weight": "bold",
                                "color": colors["text"],
                                "flex": 3
                            },
                            {
                                "type": "text",
                                "text": f"جولة {self.current_question + 1}/5",
                                "size": "sm",
                                "color": colors["text2"],
                                "align": "end",
                                "flex": 2
                            }
                        ]
                    }
                ],
                "backgroundColor": colors["bg"],
                "paddingAll": "20px"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": previous_section + [
                    {
                        "type": "text",
                        "text": "🔄 رتب الحروف لتكوين كلمة صحيحة",
                        "size": "md",
                        "color": colors["text"],
                        "weight": "bold",
                        "align": "center",
                        "wrap": True
                    }
                ] + letter_boxes + [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": f"💡 الكلمة مكونة من {len(word)} حروف",
                                "size": "sm",
                                "color": colors["text2"],
                                "align": "center"
                            }
                        ],
                        "backgroundColor": colors["card"],
                        "cornerRadius": "15px",
                        "paddingAll": "15px"
                    },
                    {
                        "type": "text",
                        "text": "💡 اكتب 'لمح' للتلميح أو 'جاوب' للإجابة",
                        "size": "xs",
                        "color": colors["text2"],
                        "align": "center",
                        "wrap": True,
                        "margin": "md"
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

        return self._create_flex_with_buttons(f"{self.game_name} - جولة {self.current_question + 1}", flex_content)

    def check_answer_intelligently(self, user_answer: str) -> bool:
        """فحص ذكي للإجابة مع دعم AI"""
        normalized_user = self.normalize_text(user_answer)
        normalized_correct = self.normalize_text(self.current_answer)

        # تطابق كامل
        if normalized_user == normalized_correct:
            return True

        # تشابه نصي (90% أو أكثر)
        ratio = difflib.SequenceMatcher(None, normalized_user, normalized_correct).ratio()
        if ratio > 0.9:
            return True

        # محاولة AI للتحقق
        if self.ai_check_answer:
            try:
                if self.ai_check_answer(self.current_answer, user_answer):
                    return True
            except:
                pass

        return False

    def check_answer(self, user_answer: str, user_id: str, display_name: str) -> Optional[Dict[str, Any]]:
        """فحص الإجابة مع دعم كامل للتلميحات"""
        if not self.game_active or user_id in self.answered_users:
            return None

        normalized = self.normalize_text(user_answer)

        # أمر التلميح
        if normalized == "لمح":
            hint = self.get_hint()
            return {
                'message': hint,
                'response': self._create_text_message(hint),
                'points': 0
            }

        # أمر كشف الإجابة
        if normalized == "جاوب":
            reveal = f"📝 الإجابة: {self.current_answer}"

            # حفظ السؤال والجواب
            self.previous_question = self.scramble_word(self.current_answer)
            self.previous_answer = self.current_answer

            # الانتقال للسؤال التالي
            self.current_question += 1
            self.answered_users.clear()

            if self.current_question >= self.questions_count:
                result = self.end_game()
                result['message'] = f"{reveal}\n\n{result.get('message', '')}"
                return result

            next_q = self.get_question()
            return {'message': reveal, 'response': next_q, 'points': 0}

        # فحص الإجابة
        is_correct = self.check_answer_intelligently(user_answer)

        if is_correct:
            points = self.add_score(user_id, display_name, 10)

            # حفظ السؤال والجواب
            self.previous_question = self.scramble_word(self.current_answer)
            self.previous_answer = self.current_answer

            # الانتقال للسؤال التالي
            self.current_question += 1
            self.answered_users.clear()

            if self.current_question >= self.questions_count:
                result = self.end_game()
                result['points'] = points
                result['message'] = f"✅ إجابة صحيحة يا {display_name}!\n+{points} نقطة\n\n{result.get('message', '')}"
                return result

            next_q = self.get_question()
            success_msg = f"✅ إجابة صحيحة يا {display_name}!\n+{points} نقطة"

            return {
                'message': success_msg,
                'response': next_q,
                'points': points
            }

        return {
            'message': "❌ إجابة غير صحيحة، حاول مرة أخرى",
            'response': self._create_text_message("❌ إجابة غير صحيحة، حاول مرة أخرى"),
            'points': 0
        }

    def get_hint(self):
        """تلميح ذكي محسن"""
        if not self.current_answer or len(self.current_answer) < 2:
            return "💡 فكر جيداً"

        return f"💡 تبدأ بـ {self.current_answer[0]} وتنتهي بـ {self.current_answer[-1]}"

    def get_game_info(self) -> Dict[str, Any]:
        """معلومات اللعبة"""
        return {
            "name": "لعبة الكلمة المبعثرة",
            "emoji": "🔤",
            "description": "رتب الحروف المبعثرة لتكوين كلمة صحيحة مع دعم AI",
            "questions_count": self.questions_count,
            "supports_hint": True,
            "supports_reveal": True,
            "active": self.game_active,
            "current_question": self.current_question,
            "players_count": len(self.scores),
            "ai_enabled": self.ai_generate_question is not None
        }
