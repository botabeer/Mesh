"""
لعبة عامة (إنسان حيوان نبات جماد بلاد) - النسخة المحسنة النهائية
Created by: Abeer Aldosari © 2025

الميزات:
✅ AI أولاً مع Fallback قوي
✅ قاعدة بيانات شاملة
✅ واجهة Flex احترافية
✅ تشفير عربي مثالي
✅ أداء محسن
"""

from games.base_game import BaseGame
import random
from typing import Dict, Any, Optional


class Game(BaseGame):
    """لعبة عامة المحسنة مع AI"""

    def __init__(self):
        super().__init__(questions_count=5)
        self.game_name = "لعبة"
        self.game_icon = "🎯"

        self.letters = list("ابتجحدرزسشصطعفقكلمنهوي")
        random.shuffle(self.letters)
        self.categories = ["إنسان", "حيوان", "نبات", "جماد", "بلاد"]

        # قاعدة بيانات محسنة
        self.fallback_answers = {
            "إنسان": {
                "أ": ["أحمد", "أمل", "أسامة", "أمير"],
                "ب": ["بدر", "بسمة"],
                "ت": ["تامر", "تالا"],
                "ج": ["جمال", "جميلة"],
                "ح": ["حسن", "حنان"],
                "د": ["داود", "دانة"],
                "ر": ["رامي", "ريم"],
                "ز": ["زياد", "زينب"],
                "س": ["سامي", "سارة"],
                "ش": ["شادي", "شهد"],
                "ص": ["صالح", "صفاء"],
                "ط": ["طارق", "طيبة"],
                "ع": ["عادل", "عائشة"],
                "ف": ["فهد", "فاطمة"],
                "ق": ["قاسم", "قمر"],
                "ك": ["كريم", "كوثر"],
                "ل": ["ليث", "لينا"],
                "م": ["محمد", "مريم"],
                "ن": ["نادر", "نورة"],
                "ه": ["هاني", "هند"],
                "و": ["وليد", "وفاء"],
                "ي": ["ياسر", "ياسمين"]
            },
            "حيوان": {
                "أ": ["أسد", "أرنب"],
                "ب": ["بقرة", "بطة"],
                "ج": ["جمل", "جراد"],
                "ح": ["حصان", "حمار"],
                "د": ["دب", "ديك"],
                "ر": ["رخم", "راكون"],
                "ز": ["زرافة", "زواحف"],
                "س": ["سمكة", "سلحفاة"],
                "ش": ["شاة", "شامبانزي"],
                "ص": ["صقر", "صرصور"],
                "ط": ["طاووس", "طائر"],
                "ع": ["عصفور", "عقرب"],
                "ف": ["فيل", "فأر"],
                "ق": ["قرد", "قط"],
                "ك": ["كلب", "كنغر"],
                "ل": ["ليث", "لبوة"],
                "م": ["ماعز", "ماموث"],
                "ن": ["نمر", "نحلة"],
                "ه": ["هر", "هدهد"],
                "و": ["وحيد القرن", "ورل"],
                "ي": ["يمامة", "يعسوب"]
            },
            "نبات": {
                "ت": ["تفاح", "توت"],
                "ج": ["جزر", "جوز"],
                "ر": ["رمان", "ريحان"],
                "ز": ["زيتون", "زنجبيل"],
                "ع": ["عنب", "عرعر"],
                "ن": ["نعناع", "نخيل"],
                "م": ["موز", "مشمش"],
                "ب": ["برتقال", "بطيخ"],
                "ف": ["فراولة", "فجل"],
                "خ": ["خس", "خيار"],
                "ش": ["شمام", "شعير"],
                "ل": ["ليمون", "لوز"]
            },
            "جماد": {
                "ب": ["باب", "بيت"],
                "ت": ["تلفاز", "ترابيزة"],
                "س": ["سيارة", "سرير"],
                "ك": ["كرسي", "كتاب"],
                "ق": ["قلم", "قميص"],
                "م": ["مفتاح", "مرآة"],
                "ش": ["شباك", "شنطة"],
                "ط": ["طاولة", "طبق"]
            },
            "بلاد": {
                "أ": ["الأردن", "الإمارات"],
                "ب": ["البحرين", "بريطانيا"],
                "ت": ["تركيا", "تونس"],
                "ج": ["الجزائر", "جيبوتي"],
                "س": ["السعودية", "سوريا"],
                "ع": ["عمان", "العراق"],
                "ف": ["فرنسا", "فلسطين"],
                "ق": ["قطر", "قبرص"],
                "ك": ["الكويت", "كندا"],
                "ل": ["لبنان", "ليبيا"],
                "م": ["مصر", "المغرب"],
                "ي": ["اليمن", "اليابان"]
            }
        }

        self.current_category = None
        self.current_letter = None
        self.previous_question = None
        self.previous_answer = None

    def generate_question_with_ai(self):
        """توليد سؤال بالذكاء الاصطناعي مع Fallback"""
        question_data = None

        # محاولة AI أولاً
        if self.ai_generate_question:
            try:
                question_data = self.ai_generate_question()
                if question_data and "category" in question_data and "letter" in question_data:
                    return question_data
            except Exception as e:
                print(f"⚠️ AI generation failed, using fallback: {e}")

        # Fallback
        self.current_letter = self.letters[self.current_question % len(self.letters)]
        self.current_category = random.choice(self.categories)

        return {
            "category": self.current_category,
            "letter": self.current_letter
        }

    def start(self):
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
        self.current_category = q_data["category"]
        self.current_letter = q_data["letter"]

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
                            "text": "📝 السؤال السابق:",
                            "size": "xs",
                            "color": colors["text2"],
                            "weight": "bold"
                        },
                        {
                            "type": "text",
                            "text": f"{self.previous_question['category']} - {self.previous_question['letter']}",
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
                        "align": "center",
                        "margin": "xs"
                    }
                ],
                "backgroundColor": colors["bg"],
                "paddingAll": "20px"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": previous_section + [
                    {
                        "type": "text",
                        "text": f"▫️ الفئة: {self.current_category}",
                        "size": "md",
                        "color": colors["text"],
                        "align": "center",
                        "margin": "md"
                    },
                    {
                        "type": "text",
                        "text": f"▫️ الحرف: {self.current_letter}",
                        "size": "xxl",
                        "weight": "bold",
                        "color": colors["primary"],
                        "align": "center",
                        "margin": "md"
                    },
                    {
                        "type": "text",
                        "text": "💡 اكتب 'جاوب' للكشف عن إجابة مقترحة",
                        "size": "xs",
                        "color": colors["text2"],
                        "align": "center",
                        "margin": "md",
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

        return self._create_flex_with_buttons("لعبة عامة", flex_content)

    def check_answer(self, user_answer: str, user_id: str, display_name: str) -> Optional[Dict[str, Any]]:
        """فحص الإجابة"""
        if not self.game_active or user_id in self.answered_users:
            return None

        normalized_answer = self.normalize_text(user_answer)

        # أمر "جاوب"
        if normalized_answer == "جاوب":
            suggested = None
            if self.current_category in self.fallback_answers and self.current_letter in self.fallback_answers[self.current_category]:
                suggested = random.choice(self.fallback_answers[self.current_category][self.current_letter])

            reveal = f"▫️ إجابة مقترحة: {suggested}" if suggested else f"▫️ أي كلمة تبدأ بحرف {self.current_letter}"

            # حفظ السؤال والجواب
            self.previous_question = {"category": self.current_category, "letter": self.current_letter}
            self.previous_answer = suggested if suggested else "لا توجد"

            # الانتقال للسؤال التالي
            self.current_question += 1
            self.answered_users.clear()

            if self.current_question >= self.questions_count:
                result = self.end_game()
                result['message'] = f"{reveal}\n\n{result.get('message', '')}"
                return result

            next_q = self.get_question()
            return {'message': reveal, 'response': next_q, 'points': 0}

        # تحقق من الحرف
        if not normalized_answer or normalized_answer[0] != self.normalize_text(self.current_letter):
            msg = f"▫️ يجب أن تبدأ الكلمة بحرف {self.current_letter} ▪️"
            return {
                'message': msg,
                'response': self._create_text_message(msg),
                'points': 0
            }

        if len(normalized_answer) < 2:
            msg = "▫️ الكلمة قصيرة جداً ▪️"
            return {
                'message': msg,
                'response': self._create_text_message(msg),
                'points': 0
            }

        # تحقق من قاعدة البيانات أو AI
        valid = False
        if self.current_category in self.fallback_answers and self.current_letter in self.fallback_answers[self.current_category]:
            valid = normalized_answer in [self.normalize_text(a) for a in self.fallback_answers[self.current_category][self.current_letter]]

        if not valid and self.ai_check_answer:
            try:
                valid = self.ai_check_answer(self.current_category, user_answer)
            except:
                pass

        if not valid:
            msg = "▫️ إجابة غير صحيحة ▪️"
            return {
                'message': msg,
                'response': self._create_text_message(msg),
                'points': 0
            }

        points = self.add_score(user_id, display_name, 10)

        # حفظ السؤال والجواب
        self.previous_question = {"category": self.current_category, "letter": self.current_letter}
        self.previous_answer = user_answer

        # الانتقال للسؤال التالي
        self.current_question += 1
        self.answered_users.clear()

        if self.current_question >= self.questions_count:
            result = self.end_game()
            result['points'] = points
            result['message'] = f"▫️ إجابة صحيحة يا {display_name} ▪️\n+{points} نقطة\n\n{result.get('message', '')}"
            return result

        next_q = self.get_question()
        msg = f"▫️ إجابة صحيحة يا {display_name} ▪️\n+{points} نقطة"

        return {
            'message': msg,
            'response': next_q,
            'points': points
        }

    def get_game_info(self) -> Dict[str, Any]:
        """معلومات اللعبة"""
        return {
            "name": "لعبة عامة",
            "emoji": "🎯",
            "description": "اكتب كلمة تبدأ بالحرف المحدد في الفئة المختارة مع دعم AI",
            "questions_count": self.questions_count,
            "supports_hint": False,
            "supports_reveal": True,
            "active": self.game_active,
            "current_question": self.current_question,
            "players_count": len(self.scores),
            "ai_enabled": self.ai_generate_question is not None
        }
