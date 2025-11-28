"""
لعبة إنسان حيوان نبات - ستايل زجاجي احترافي
Created by: Abeer Aldosari © 2025
"""

from games.base_game import BaseGame
import random
from typing import Dict, Any, Optional


class HumanAnimalPlantGame(BaseGame):
    """لعبة إنسان حيوان نبات"""

    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, questions_count=5)
        self.game_name = "إنسان حيوان نبات"
        self.game_icon = "🎯"

        self.letters = list("ابتجحدرزسشصطعفقكلمنهوي")
        random.shuffle(self.letters)
        self.categories = ["إنسان", "حيوان", "نبات", "جماد", "بلاد"]

        self.database = {
            "إنسان": {
                "أ": ["أحمد", "أمل"], "ب": ["بدر", "بسمة"], "ت": ["تامر", "تالا"], "ج": ["جمال"], "ح": ["حسن", "حنان"],
                "د": ["داود", "دانة"], "ر": ["رامي", "ريم"], "ز": ["زياد", "زينب"], "س": ["سامي", "سارة"],
                "ش": ["شادي", "شهد"], "ص": ["صالح", "صفاء"], "ط": ["طارق"], "ع": ["عادل", "عائشة"],
                "ف": ["فهد", "فاطمة"], "ق": ["قاسم", "قمر"], "ك": ["كريم", "كوثر"], "ل": ["ليث", "لينا"],
                "م": ["محمد", "مريم"], "ن": ["نادر", "نورة"], "ه": ["هاني", "هند"], "و": ["وليد", "وفاء"], "ي": ["ياسر", "ياسمين"]
            },
            "حيوان": {
                "أ": ["أسد", "أرنب"], "ب": ["بقرة", "بطة"], "ج": ["جمل"], "ح": ["حصان", "حمار"], "د": ["دب", "ديك"],
                "ر": ["رخم"], "ز": ["زرافة"], "س": ["سمكة", "سلحفاة"], "ش": ["شاة"], "ص": ["صقر"], "ط": ["طاووس"],
                "ع": ["عصفور", "عقرب"], "ف": ["فيل", "فأر"], "ق": ["قرد", "قط"], "ك": ["كلب"], "ل": ["ليث"],
                "م": ["ماعز"], "ن": ["نمر", "نحلة"], "ه": ["هر"], "و": ["وحيد القرن"], "ي": ["يمامة"]
            },
            "نبات": {
                "ت": ["تفاح", "توت"], "ج": ["جزر"], "ر": ["رمان"], "ز": ["زيتون"], "ع": ["عنب"], "ن": ["نعناع"],
                "م": ["موز", "مشمش"], "ب": ["برتقال", "بطيخ"], "ف": ["فراولة"], "خ": ["خس", "خيار"],
                "ش": ["شمام"], "ل": ["ليمون"], "أ": ["أناناس"], "د": ["دراق"], "ك": ["كرز"], "و": ["ورد"]
            },
            "جماد": {
                "ب": ["باب", "بيت"], "ت": ["تلفاز"], "س": ["سيارة", "سرير"], "ك": ["كرسي", "كتاب"],
                "ق": ["قلم", "قميص"], "م": ["مفتاح", "مرآة"], "ش": ["شباك"], "ط": ["طاولة", "طبق"],
                "ح": ["حائط"], "ف": ["فنجان"], "ن": ["نافذة"], "ص": ["صندوق"], "ل": ["لوحة"]
            },
            "بلاد": {
                "أ": ["الأردن", "الإمارات"], "ب": ["البحرين"], "ت": ["تركيا", "تونس"], "ج": ["الجزائر"],
                "س": ["السعودية", "سوريا"], "ع": ["عمان", "العراق"], "ف": ["فرنسا", "فلسطين"],
                "ق": ["قطر"], "ك": ["الكويت"], "ل": ["لبنان", "ليبيا"], "م": ["مصر", "المغرب"],
                "ي": ["اليمن", "اليابان"], "ا": ["إيطاليا", "إسبانيا"], "ه": ["الهند"]
            }
        }

        self.current_category = None
        self.current_letter = None

    def start_game(self):
        self.current_question = 0
        self.game_active = True
        self.previous_question = None
        self.previous_answer = None
        self.answered_users.clear()
        return self.get_question()

    def get_question(self):
        self.current_letter = self.letters[self.current_question % len(self.letters)]
        self.current_category = random.choice(self.categories)

        colors = self.get_theme_colors()
        
        previous_section = []
        if self.previous_question and self.previous_answer:
            previous_section = [
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "text", "text": "السؤال السابق:", "size": "xs", "color": colors["text2"], "weight": "bold"},
                        {"type": "text", "text": f"{self.previous_question['category']} - {self.previous_question['letter']}", "size": "xs", "color": colors["text2"], "wrap": True, "margin": "xs"},
                        {"type": "text", "text": f"✅ الجواب: {self.previous_answer}", "size": "xs", "color": colors["success"], "wrap": True, "margin": "xs"}
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
                            {"type": "text", "text": f"{self.game_icon} {self.game_name}", "size": "lg", "weight": "bold", "color": colors["text"], "align": "center"},
                            {"type": "text", "text": f"جولة {self.current_question + 1} من {self.questions_count}", "size": "xs", "color": colors["text2"], "align": "center", "margin": "xs"}
                        ]
                    },
                    {"type": "separator", "margin": "md", "color": colors["shadow1"]}
                ] + previous_section + [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {"type": "text", "text": "📂 الفئة:", "size": "sm", "color": colors["text2"], "weight": "bold"},
                            {"type": "text", "text": self.current_category, "size": "xxl", "color": colors["primary"], "weight": "bold", "align": "center", "margin": "sm"}
                        ],
                        "backgroundColor": colors["card"],
                        "cornerRadius": "20px",
                        "paddingAll": "20px",
                        "margin": "md"
                    },
                    {"type": "separator", "color": colors["shadow1"], "margin": "md"},
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {"type": "text", "text": "🔤 يبدأ بحرف:", "size": "sm", "color": colors["text2"], "weight": "bold"},
                            {"type": "text", "text": self.current_letter, "size": "xxl", "color": colors["primary"], "weight": "bold", "align": "center", "margin": "sm"}
                        ],
                        "backgroundColor": colors["card"],
                        "cornerRadius": "20px",
                        "paddingAll": "20px",
                        "margin": "md"
                    },
                    {"type": "text", "text": "💡 اكتب 'لمح' أو 'جاوب'", "size": "xs", "color": colors["text2"], "align": "center", "wrap": True, "margin": "md"},
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
                "paddingAll": "20px"
            },
            "styles": {"body": {"backgroundColor": colors["bg"]}}
        }

        return self._create_flex_with_buttons(f"{self.game_name}", flex_content)

    def validate_answer(self, normalized_answer: str) -> bool:
        if not normalized_answer or len(normalized_answer) < 2:
            return False
        required_letter = self.normalize_text(self.current_letter)
        if normalized_answer[0] != required_letter:
            return False
        if self.current_category in self.database:
            if self.current_letter in self.database[self.current_category]:
                valid_answers = [self.normalize_text(ans) for ans in self.database[self.current_category][self.current_letter]]
                if normalized_answer in valid_answers:
                    return True
        return True

    def get_suggested_answer(self) -> Optional[str]:
        if self.current_category in self.database:
            if self.current_letter in self.database[self.current_category]:
                answers = self.database[self.current_category][self.current_letter]
                if answers:
                    return random.choice(answers)
        return None

    def check_answer(self, user_answer: str, user_id: str, display_name: str):
        if not self.game_active or user_id in self.answered_users:
            return None

        normalized_answer = self.normalize_text(user_answer)

        if normalized_answer == "لمح":
            suggested = self.get_suggested_answer()
            hint = f"💡 مثال: {suggested[0]}{'_' * (len(suggested) - 1)}" if suggested else f"💡 ابحث عن {self.current_category} يبدأ بحرف {self.current_letter}"
            return {'message': hint, 'response': self._create_text_message(hint), 'points': 0}

        if normalized_answer == "جاوب":
            suggested = self.get_suggested_answer()
            reveal = f"📝 إجابة مقترحة: {suggested}" if suggested else f"📝 أي كلمة تبدأ بحرف {self.current_letter}"
            self.previous_question = {"category": self.current_category, "letter": self.current_letter}
            self.previous_answer = suggested if suggested else "لا توجد"
            self.current_question += 1
            self.answered_users.clear()

            if self.current_question >= self.questions_count:
                result = self.end_game()
                result['message'] = f"{reveal}\n\n{result.get('message', '')}"
                return result

            return {'message': reveal, 'response': self.get_question(), 'points': 0}

        is_valid = self.validate_answer(normalized_answer)

        if not is_valid:
            return {'message': f"❌ يجب أن تبدأ بحرف '{self.current_letter}'", 'response': self._create_text_message(f"❌ يجب أن تبدأ بحرف '{self.current_letter}'"), 'points': 0}

        points = self.add_score(user_id, display_name, 10)
        self.previous_question = {"category": self.current_category, "letter": self.current_letter}
        self.previous_answer = user_answer
        self.current_question += 1
        self.answered_users.clear()

        if self.current_question >= self.questions_count:
            result = self.end_game()
            result['points'] = points
            result['message'] = f"✅ صحيح يا {display_name}!\n+{points} نقطة\n\n{result.get('message', '')}"
            return result

        return {'message': f"✅ صحيح يا {display_name}!\n+{points} نقطة", 'response': self.get_question(), 'points': points}
