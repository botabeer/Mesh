"""
لعبة إنسان حيوان نبات جماد بلاد - النسخة المحسنة النهائية
Created by: Abeer Aldosari © 2025

الميزات:
✅ 5 فئات: إنسان، حيوان، نبات، جماد، بلاد
✅ قاعدة بيانات شاملة لكل حرف
✅ واجهة Flex احترافية
✅ تشفير عربي مثالي
✅ دعم كامل للتلميحات
"""

from games.base_game import BaseGame
import random
from typing import Dict, Any, Optional


class HumanAnimalPlantGame(BaseGame):
    """لعبة إنسان حيوان نبات جماد بلاد المحسنة"""

    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, questions_count=5)
        self.game_name = "إنسان حيوان نبات"
        self.game_icon = "🎯"

        # الحروف المتاحة
        self.letters = list("ابتجحدرزسشصطعفقكلمنهوي")
        random.shuffle(self.letters)
        
        # الفئات
        self.categories = ["إنسان", "حيوان", "نبات", "جماد", "بلاد"]

        # قاعدة بيانات شاملة
        self.database = {
            "إنسان": {
                "أ": ["أحمد", "أمل", "أسامة", "أمير", "أسماء", "إبراهيم"],
                "ب": ["بدر", "بسمة", "باسم", "بشرى"],
                "ت": ["تامر", "تالا", "توفيق", "تماضر"],
                "ج": ["جمال", "جميلة", "جاسم", "جواد"],
                "ح": ["حسن", "حنان", "حامد", "حليمة"],
                "د": ["داود", "دانة", "دعاء", "ديانا"],
                "ر": ["رامي", "ريم", "رشيد", "رنا"],
                "ز": ["زياد", "زينب", "زكريا", "زهراء"],
                "س": ["سامي", "سارة", "سعيد", "سلمى"],
                "ش": ["شادي", "شهد", "شريف", "شيماء"],
                "ص": ["صالح", "صفاء", "صلاح", "صبا"],
                "ط": ["طارق", "طيبة", "طلال", "طاهر"],
                "ع": ["عادل", "عائشة", "عمر", "علي"],
                "ف": ["فهد", "فاطمة", "فيصل", "فريدة"],
                "ق": ["قاسم", "قمر", "قيس", "قسيمة"],
                "ك": ["كريم", "كوثر", "كمال", "كريمة"],
                "ل": ["ليث", "لينا", "لؤي", "لمياء"],
                "م": ["محمد", "مريم", "ماجد", "منى"],
                "ن": ["نادر", "نورة", "نبيل", "نجلاء"],
                "ه": ["هاني", "هند", "هيثم", "هالة"],
                "و": ["وليد", "وفاء", "وائل", "وسام"],
                "ي": ["ياسر", "ياسمين", "يوسف", "يسرى"]
            },
            "حيوان": {
                "أ": ["أسد", "أرنب", "أفعى"],
                "ب": ["بقرة", "بطة", "ببغاء"],
                "ج": ["جمل", "جراد", "جاموس"],
                "ح": ["حصان", "حمار", "حوت"],
                "د": ["دب", "ديك", "دولفين"],
                "ر": ["رخم", "راكون"],
                "ز": ["زرافة", "زواحف"],
                "س": ["سمكة", "سلحفاة", "سنجاب"],
                "ش": ["شاة", "شامبانزي"],
                "ص": ["صقر", "صرصور"],
                "ط": ["طاووس", "طائر"],
                "ع": ["عصفور", "عقرب", "عنكبوت"],
                "ف": ["فيل", "فأر", "فهد"],
                "ق": ["قرد", "قط", "قنفذ"],
                "ك": ["كلب", "كنغر"],
                "ل": ["ليث", "لبوة"],
                "م": ["ماعز", "ماموث"],
                "ن": ["نمر", "نحلة", "نسر"],
                "ه": ["هر", "هدهد"],
                "و": ["وحيد القرن", "ورل"],
                "ي": ["يمامة", "يعسوب"]
            },
            "نبات": {
                "ت": ["تفاح", "توت", "تمر"],
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
                "ل": ["ليمون", "لوز"],
                "أ": ["أناناس"],
                "د": ["دراق"],
                "ك": ["كرز", "كمثرى"],
                "و": ["ورد"]
            },
            "جماد": {
                "ب": ["باب", "بيت"],
                "ت": ["تلفاز", "ترابيزة"],
                "س": ["سيارة", "سرير"],
                "ك": ["كرسي", "كتاب"],
                "ق": ["قلم", "قميص"],
                "م": ["مفتاح", "مرآة"],
                "ش": ["شباك", "شنطة"],
                "ط": ["طاولة", "طبق"],
                "ح": ["حائط", "حقيبة"],
                "ف": ["فنجان"],
                "ن": ["نافذة"],
                "ص": ["صندوق"],
                "ل": ["لوحة"]
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
                "ي": ["اليمن", "اليابان"],
                "ش": ["الشام"],
                "ا": ["إيطاليا", "إسبانيا"],
                "ه": ["الهند", "هولندا"]
            }
        }

        self.current_category = None
        self.current_letter = None
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
        # اختيار حرف وفئة
        self.current_letter = self.letters[self.current_question % len(self.letters)]
        self.current_category = random.choice(self.categories)

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
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "📂 الفئة:",
                                "size": "sm",
                                "color": colors["text2"],
                                "weight": "bold"
                            },
                            {
                                "type": "text",
                                "text": self.current_category,
                                "size": "xxl",
                                "color": colors["primary"],
                                "weight": "bold",
                                "align": "center",
                                "margin": "sm"
                            }
                        ],
                        "backgroundColor": colors["card"],
                        "cornerRadius": "20px",
                        "paddingAll": "20px"
                    },
                    {"type": "separator", "color": colors["shadow1"]},
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "🔤 يبدأ بحرف:",
                                "size": "sm",
                                "color": colors["text2"],
                                "weight": "bold"
                            },
                            {
                                "type": "text",
                                "text": self.current_letter,
                                "size": "xxl",
                                "color": colors["primary"],
                                "weight": "bold",
                                "align": "center",
                                "margin": "sm"
                            }
                        ],
                        "backgroundColor": colors["card"],
                        "cornerRadius": "20px",
                        "paddingAll": "20px"
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

        return self._create_flex_with_buttons(
            f"{self.game_name} - جولة {self.current_question + 1}",
            flex_content
        )

    def check_answer(self, user_answer: str, user_id: str, display_name: str) -> Optional[Dict[str, Any]]:
        """فحص الإجابة"""
        if not self.game_active or user_id in self.answered_users:
            return None

        normalized_answer = self.normalize_text(user_answer)

        # أمر التلميح
        if normalized_answer == "لمح":
            hint = self.get_hint()
            return {
                'message': hint,
                'response': self._create_text_message(hint),
                'points': 0
            }

        # أمر كشف الإجابة
        if normalized_answer == "جاوب":
            suggested = self.get_suggested_answer()
            reveal = f"📝 إجابة مقترحة: {suggested}" if suggested else f"📝 أي كلمة تبدأ بحرف {self.current_letter}"

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

        # التحقق من الإجابة
        is_valid = self.validate_answer(normalized_answer)

        if not is_valid:
            msg = f"❌ يجب أن تبدأ الكلمة بحرف '{self.current_letter}'"
            return {
                'message': msg,
                'response': self._create_text_message(msg),
                'points': 0
            }

        # إجابة صحيحة
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
            result['message'] = f"✅ إجابة صحيحة يا {display_name}!\n+{points} نقطة\n\n{result.get('message', '')}"
            return result

        next_q = self.get_question()
        success_msg = f"✅ إجابة صحيحة يا {display_name}!\n+{points} نقطة"

        return {
            'message': success_msg,
            'response': next_q,
            'points': points
        }

    def validate_answer(self, normalized_answer: str) -> bool:
        """التحقق من صحة الإجابة"""
        if not normalized_answer or len(normalized_answer) < 2:
            return False

        # التحقق من الحرف الأول
        required_letter = self.normalize_text(self.current_letter)
        if normalized_answer[0] != required_letter:
            return False

        # التحقق من قاعدة البيانات
        if self.current_category in self.database:
            if self.current_letter in self.database[self.current_category]:
                valid_answers = [
                    self.normalize_text(ans) 
                    for ans in self.database[self.current_category][self.current_letter]
                ]
                if normalized_answer in valid_answers:
                    return True

        # قبول أي كلمة تبدأ بالحرف الصحيح (مرونة)
        return True

    def get_suggested_answer(self) -> Optional[str]:
        """الحصول على إجابة مقترحة"""
        if self.current_category in self.database:
            if self.current_letter in self.database[self.current_category]:
                answers = self.database[self.current_category][self.current_letter]
                if answers:
                    return random.choice(answers)
        return None

    def get_hint(self) -> str:
        """تلميح ذكي"""
        suggested = self.get_suggested_answer()
        if suggested:
            return f"💡 مثال: {suggested[0]}{'_' * (len(suggested) - 1)}"
        return f"💡 ابحث عن {self.current_category} يبدأ بحرف {self.current_letter}"

    def get_game_info(self) -> Dict[str, Any]:
        """معلومات اللعبة"""
        return {
            "name": "لعبة إنسان حيوان نبات جماد بلاد",
            "emoji": "🎯",
            "description": "اكتب كلمة من الفئة المحددة تبدأ بالحرف المطلوب",
            "questions_count": self.questions_count,
            "supports_hint": True,
            "supports_reveal": True,
            "active": self.game_active,
            "current_question": self.current_question,
            "players_count": len(self.scores),
            "categories": len(self.categories)
        }
