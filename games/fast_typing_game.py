"""
لعبة الكتابة السريعة - النسخة المحسنة النهائية
Created by: Abeer Aldosari © 2025

الميزات:
✅ اختبار سرعة ودقة الكتابة
✅ عبارات متنوعة وممتعة
✅ واجهة Flex احترافية
✅ تشفير عربي مثالي
✅ مكافأة السرعة
✅ بدون دعم لمح (طبيعة اللعبة)
"""

from games.base_game import BaseGame
import random
from datetime import datetime
from typing import Dict, Any, Optional


class FastTypingGame(BaseGame):
    """لعبة الكتابة السريعة المحسنة"""

    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, questions_count=5)
        self.game_name = "كتابة سريعة"
        self.game_icon = "⚡"
        self.supports_hint = False
        self.supports_reveal = True

        # عبارات الكتابة
        self.phrases = [
            "السرعة والدقة مهمتان",
            "التركيز هو مفتاح النجاح",
            "الممارسة تصنع الإتقان",
            "الوقت من ذهب",
            "اكتب بسرعة ودقة",
            "التحدي يبدأ الآن",
            "هيا اثبت مهارتك",
            "السرعة مع الدقة",
            "لا تستسلم أبداً",
            "النجاح يحتاج صبر",
            "الإبداع لا حدود له",
            "كن الأفضل دائماً",
            "التميز هو هدفنا",
            "احلم واسعى وحقق",
            "المثابرة طريق النجاح",
            "كل لحظة ثمينة",
            "التفاؤل سر السعادة",
            "اجعل يومك مميزاً",
            "الأمل نور الحياة",
            "ثق بنفسك دائماً"
        ]

        random.shuffle(self.phrases)
        self.used_phrases = []
        self.question_start_time = None
        self.previous_question = None
        self.previous_answer = None

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
        # اختيار عبارة
        available = [p for p in self.phrases if p not in self.used_phrases]
        if not available:
            self.used_phrases = []
            available = self.phrases.copy()

        phrase = random.choice(available)
        self.used_phrases.append(phrase)

        self.current_answer = phrase
        self.question_start_time = datetime.now()

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
                            "text": "📝 العبارة السابقة:",
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
                            "text": f"✅ {self.previous_answer}",
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
                "spacing": "lg",
                "contents": previous_section + [
                    {
                        "type": "text",
                        "text": "⚡ اكتب النص التالي بالضبط:",
                        "size": "md",
                        "color": colors["text"],
                        "weight": "bold",
                        "align": "center",
                        "wrap": True
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "md",
                        "contents": [
                            {
                                "type": "text",
                                "text": phrase,
                                "size": "xl",
                                "color": colors["primary"],
                                "weight": "bold",
                                "align": "center",
                                "wrap": True
                            }
                        ],
                        "backgroundColor": colors["card"],
                        "cornerRadius": "20px",
                        "paddingAll": "25px"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "xs",
                        "contents": [
                            {
                                "type": "text",
                                "text": "💡 نصائح:",
                                "size": "sm",
                                "color": colors["text"],
                                "weight": "bold"
                            },
                            {
                                "type": "text",
                                "text": "• اكتب بدقة وسرعة\n• احذر من الأخطاء الإملائية\n• أقل من 5 ثوانٍ = نقاط إضافية!",
                                "size": "xs",
                                "color": colors["text2"],
                                "wrap": True
                            }
                        ],
                        "backgroundColor": colors["card"],
                        "cornerRadius": "15px",
                        "paddingAll": "15px"
                    },
                    {
                        "type": "text",
                        "text": "💡 اكتب 'جاوب' لتخطي السؤال",
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

    def check_answer(self, user_answer: str, user_id: str, display_name: str) -> Optional[Dict[str, Any]]:
        """فحص الإجابة مع قياس السرعة"""
        if not self.game_active or user_id in self.answered_users:
            return None

        text = user_answer.strip()
        normalized = self.normalize_text(text)

        # رفض أمر لمح
        if normalized == 'لمح':
            msg = "❌ هذه اللعبة لا تدعم التلميحات\n⚡ اكتب النص بالضبط!"
            return {
                'message': msg,
                'response': self._create_text_message(msg),
                'points': 0
            }

        # أمر تخطي السؤال
        if normalized == 'جاوب':
            reveal = f"📝 العبارة: {self.current_answer}"

            # حفظ السؤال والجواب
            self.previous_question = self.current_answer
            self.previous_answer = "تم التخطي"

            # الانتقال للسؤال التالي
            self.current_question += 1
            self.answered_users.clear()

            if self.current_question >= self.questions_count:
                result = self.end_game()
                result['message'] = f"{reveal}\n\n{result.get('message', '')}"
                return result

            next_q = self.get_question()
            return {'message': reveal, 'response': next_q, 'points': 0}

        # حساب الوقت المستغرق
        time_taken = (datetime.now() - self.question_start_time).total_seconds() if self.question_start_time else 0

        # فحص التطابق التام
        is_correct = text == self.current_answer

        if is_correct:
            # النقاط الأساسية
            points = 10

            # مكافأة السرعة (أقل من 5 ثوانٍ)
            speed_bonus = 0
            if time_taken < 5:
                speed_bonus = 5
                points += speed_bonus

            points = self.add_score(user_id, display_name, points)

            # حفظ السؤال والجواب
            if speed_bonus > 0:
                self.previous_question = self.current_answer
                self.previous_answer = f"أنجزت في {time_taken:.1f}ث مع مكافأة!"
            else:
                self.previous_question = self.current_answer
                self.previous_answer = f"أنجزت في {time_taken:.1f}ث"

            # الانتقال للسؤال التالي
            self.current_question += 1
            self.answered_users.clear()

            if self.current_question >= self.questions_count:
                result = self.end_game()
                result['points'] = points
                if speed_bonus > 0:
                    result['message'] = f"🎉 ممتاز! أنجزتها في {time_taken:.1f} ثانية!\n⭐ +{speed_bonus} نقاط إضافية للسرعة!\n+{points} نقطة\n\n{result.get('message', '')}"
                else:
                    result['message'] = f"✅ صحيح! الوقت: {time_taken:.1f} ثانية\n+{points} نقطة\n\n{result.get('message', '')}"
                return result

            next_q = self.get_question()
            if speed_bonus > 0:
                success_msg = f"🎉 ممتاز يا {display_name}!\n⚡ أنجزتها في {time_taken:.1f} ثانية\n⭐ +{speed_bonus} نقاط إضافية للسرعة!\n+{points} نقطة"
            else:
                success_msg = f"✅ صحيح يا {display_name}!\n⏱️ الوقت: {time_taken:.1f} ثانية\n+{points} نقطة"

            return {
                'message': success_msg,
                'response': next_q,
                'points': points
            }

        return {
            'message': f"❌ خطأ! راجع الكتابة بدقة\n⏱️ الوقت: {time_taken:.1f}ث",
            'response': self._create_text_message(f"❌ خطأ إملائي! راجع النص مرة أخرى\n⏱️ استغرقت {time_taken:.1f} ثانية"),
            'points': 0
        }

    def get_game_info(self) -> Dict[str, Any]:
        """معلومات اللعبة"""
        return {
            "name": "لعبة الكتابة السريعة",
            "emoji": "⚡",
            "description": "اختبر سرعة ودقة كتابتك!",
            "questions_count": self.questions_count,
            "supports_hint": False,
            "supports_reveal": True,
            "active": self.game_active,
            "current_question": self.current_question,
            "players_count": len(self.scores)
        }
