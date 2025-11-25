"""
لعبة الأضداد - النسخة المحسنة النهائية
Created by: Abeer Aldosari © 2025

الميزات:
✅ AI أولاً مع Fallback قوي
✅ قاعدة أضداد غنية ومتنوعة
✅ واجهة Flex احترافية
✅ تشفير عربي مثالي
✅ أداء محسن
"""

from games.base_game import BaseGame
import random
import difflib
from typing import Dict, Any, Optional


class OppositeGame(BaseGame):
    """لعبة الأضداد المحسنة مع AI"""

    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, questions_count=5)
        self.game_name = "أضداد"
        self.game_icon = "↔️"

        # قاعدة أضداد محسنة ومتنوعة
        self.fallback_opposites = [
            {"word": "كبير", "opposite": ["صغير"]},
            {"word": "طويل", "opposite": ["قصير"]},
            {"word": "سريع", "opposite": ["بطيء"]},
            {"word": "قوي", "opposite": ["ضعيف"]},
            {"word": "حار", "opposite": ["بارد"]},
            {"word": "نظيف", "opposite": ["قذر", "وسخ"]},
            {"word": "سهل", "opposite": ["صعب"]},
            {"word": "جميل", "opposite": ["قبيح"]},
            {"word": "غني", "opposite": ["فقير"]},
            {"word": "ثقيل", "opposite": ["خفيف"]},
            {"word": "عميق", "opposite": ["ضحل", "سطحي"]},
            {"word": "واسع", "opposite": ["ضيق"]},
            {"word": "مظلم", "opposite": ["مضيء", "مشرق"]},
            {"word": "رطب", "opposite": ["جاف", "ناشف"]},
            {"word": "قديم", "opposite": ["جديد", "حديث"]},
            {"word": "بعيد", "opposite": ["قريب"]},
            {"word": "مرتفع", "opposite": ["منخفض"]},
            {"word": "مبكر", "opposite": ["متأخر"]},
            {"word": "فوق", "opposite": ["تحت"]},
            {"word": "داخل", "opposite": ["خارج"]},
            {"word": "يمين", "opposite": ["يسار", "شمال"]},
            {"word": "صاعد", "opposite": ["نازل", "هابط"]},
            {"word": "ساخن", "opposite": ["بارد"]},
            {"word": "ناعم", "opposite": ["خشن"]},
            {"word": "حلو", "opposite": ["مر", "حامض"]}
        ]

        random.shuffle(self.fallback_opposites)
        self.used_words = []
        self.previous_question = None
        self.previous_answer = None

    def generate_question_with_ai(self):
        """توليد سؤال بالذكاء الاصطناعي مع Fallback"""
        question_data = None

        # محاولة AI أولاً
        if self.ai_generate_question:
            try:
                question_data = self.ai_generate_question()
                if question_data and "word" in question_data and "opposite" in question_data:
                    # تأكد من أن الإجابة قائمة
                    if not isinstance(question_data["opposite"], list):
                        question_data["opposite"] = [str(question_data["opposite"])]
                    return question_data
            except Exception as e:
                print(f"⚠️ AI generation failed, using fallback: {e}")

        # Fallback للأضداد المخزنة
        available = [w for w in self.fallback_opposites if w not in self.used_words]
        if not available:
            self.used_words = []
            available = self.fallback_opposites.copy()

        question_data = random.choice(available)
        self.used_words.append(question_data)
        return question_data

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
        self.current_answer = q_data["opposite"]

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
                            "text": f"✅ الضد: {self.previous_answer}",
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
                        "text": "↔️ ما هو عكس هذه الكلمة؟",
                        "size": "md",
                        "color": colors["text"],
                        "weight": "bold",
                        "align": "center",
                        "wrap": True
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": q_data["word"],
                                "size": "xxl",
                                "color": colors["primary"],
                                "weight": "bold",
                                "align": "center"
                            }
                        ],
                        "backgroundColor": colors["card"],
                        "cornerRadius": "20px",
                        "paddingAll": "30px"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "💡 فكر في المعنى المعاكس تماماً",
                                "size": "sm",
                                "color": colors["text2"],
                                "align": "center",
                                "wrap": True
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

        # فحص مباشر
        for correct in self.current_answer:
            normalized_correct = self.normalize_text(correct)

            # تطابق كامل
            if normalized_user == normalized_correct:
                return True

            # تطابق جزئي
            if normalized_user in normalized_correct or normalized_correct in normalized_user:
                return True

            # تشابه نصي (85% أو أكثر)
            ratio = difflib.SequenceMatcher(None, normalized_user, normalized_correct).ratio()
            if ratio > 0.85:
                return True

        # محاولة AI للتحقق
        if self.ai_check_answer:
            try:
                for correct in self.current_answer:
                    if self.ai_check_answer(correct, user_answer):
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
            answer_text = " أو ".join(self.current_answer)
            reveal = f"📝 الإجابة: {answer_text}"

            # حفظ السؤال والجواب
            q_data = self.generate_question_with_ai()
            self.previous_question = q_data["word"]
            self.previous_answer = answer_text

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
            q_data = self.generate_question_with_ai()
            self.previous_question = q_data["word"]
            self.previous_answer = self.current_answer[0]

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
        if not self.current_answer or len(self.current_answer[0]) < 2:
            return "💡 فكر في الضد"

        first_answer = self.current_answer[0]
        return f"💡 يبدأ بحرف: {first_answer[0]}\n📏 عدد الحروف: {len(first_answer)}"

    def get_game_info(self) -> Dict[str, Any]:
        """معلومات اللعبة"""
        return {
            "name": "لعبة الأضداد",
            "emoji": "↔️",
            "description": "اكتشف عكس الكلمة مع دعم AI",
            "questions_count": self.questions_count,
            "supports_hint": True,
            "supports_reveal": True,
            "active": self.game_active,
            "current_question": self.current_question,
            "players_count": len(self.scores),
            "ai_enabled": self.ai_generate_question is not None
        }
