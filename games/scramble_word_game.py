“””
لعبة الكلمة المبعثرة - ستايل زجاجي احترافي
Created by: Abeer Aldosari © 2025
✅ دعم فردي + فريقين
✅ إصلاح جميع الأخطاء
“””

from games.base_game import BaseGame
import random

class ScrambleWordGame(BaseGame):
“”“لعبة الكلمة المبعثرة”””

```
def __init__(self, line_bot_api):
    super().__init__(line_bot_api, questions_count=5)
    self.game_name = "كلمة مبعثرة"
    self.game_icon = "▪️"

    self.words = [
        "مدرسة","كتاب","قلم","باب","نافذة","طاولة","كرسي","سيارة","طائرة","قطار","سفينة",
        "دراجة","تفاحة","موز","برتقال","عنب","بطيخ","فراولة","شمس","قمر","نجمة","سماء",
        "بحر","جبل","نهر","أسد","نمر","فيل","زرافة","حصان","غزال","ورد","شجرة","زهرة",
        "عشب","ورقة","منزل","مسجد","حديقة","ملعب","مطعم","مكتبة","صديق","عائلة","أخ",
        "أخت","والد","والدة","مطر","ريح"
    ]

    random.shuffle(self.words)
    self.used_words = []

def scramble_word(self, word: str) -> str:
    letters = list(word)
    attempts = 0
    while attempts < 10:
        random.shuffle(letters)
        scrambled = ''.join(letters)
        if scrambled != word:
            return scrambled
        attempts += 1
    return word[::-1]

def start_game(self):
    self.current_question = 0
    self.game_active = True
    self.previous_question = None
    self.previous_answer = None
    self.answered_users.clear()
    self.used_words = []
    return self.get_question()

def get_question(self):
    available = [w for w in self.words if w not in self.used_words]
    if not available:
        self.used_words = []
        available = self.words.copy()

    word = random.choice(available)
    self.used_words.append(word)
    self.current_answer = word
    scrambled = self.scramble_word(word)

    colors = self.get_theme_colors()

    previous_section = []
    if self.previous_question and self.previous_answer:
        previous_section = [
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "الكلمة السابقة:", "size": "xs", "color": colors["text2"], "weight": "bold"},
                    {"type": "text", "text": self.previous_question, "size": "xs", "color": colors["text2"], "wrap": True},
                    {"type": "text", "text": f"الجواب: {self.previous_answer}", "size": "xs", "color": colors["success"], "wrap": True}
                ],
                "backgroundColor": colors["card"],
                "cornerRadius": "15px",
                "paddingAll": "12px",
                "margin": "md"
            }
        ]

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
                    "contents": [{"type": "text", "text": letter, "size": "xl", "weight": "bold", "color": colors["primary"], "align": "center"}],
                    "backgroundColor": colors["card"],
                    "cornerRadius": "15px",
                    "paddingAll": "15px",
                    "flex": 1
                }
                for letter in chunk
            ]
        }
        letter_boxes.append(row)

    # ✅ إضافة hint info فقط في الوضع الفردي
    hint_section = []
    if not self.team_mode:
        hint_section = [
            {"type": "text", "text": "💡 لمح | جاوب", "size": "xs", "color": colors["text2"], "align": "center", "margin": "md"}
        ]

    flex_content = {
        "type": "bubble",
        "size": "kilo",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": self.game_name, "size": "xxl", "weight": "bold", "color": colors["text"], "align": "center"},
                {"type": "text", "text": f"سؤال {self.current_question + 1} من {self.questions_count}", "size": "sm", "color": colors["text2"], "align": "center"},
                {"type": "separator", "margin": "lg"}
            ] + previous_section + [
                {"type": "text", "text": "رتب الحروف لتكوين كلمة", "size": "md", "color": colors["text"], "weight": "bold", "align": "center"}
            ] + letter_boxes + [
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [{"type": "text", "text": f"عدد الحروف: {len(word)}", "size": "sm", "color": colors["text2"], "align": "center"}],
                    "backgroundColor": colors["card"],
                    "cornerRadius": "15px",
                    "paddingAll": "15px",
                    "margin": "lg"
                }
            ] + hint_section,
            "backgroundColor": colors["bg"],
            "paddingAll": "24px"
        },
        "styles": {"body": {"backgroundColor": colors["bg"]}}
    }

    return self._create_flex_with_buttons(self.game_name, flex_content)

def check_answer(self, user_answer: str, user_id: str, display_name: str):
    if not self.game_active:
        return None

    normalized = self.normalize_text(user_answer)

    # ✅ منع غير المنضمين في وضع الفريقين
    if self.team_mode and user_id not in self.joined_users:
        return None

    # ✅ تعطيل لمح وجاوب في وضع الفريقين
    if self.team_mode:
        if normalized == self.normalize_text(self.current_answer):
            team = self.get_user_team(user_id)
            if not team:
                team = self.assign_to_team(user_id)
            
            points = self.add_team_score(team, 10)
            self.previous_question = self.scramble_word(self.current_answer)
            self.previous_answer = self.current_answer
            self.current_question += 1
            self.answered_users.clear()

            if self.current_question >= self.questions_count:
                return self.end_game()

            return {'message': f"تم التسجيل للفريق {team}\n+10 نقاط", 'response': self.get_question(), 'points': 10}

        return None

    # ✅ الوضع الفردي كما هو
    if user_id in self.answered_users:
        return None

    if normalized == "لمح":
        hint = f"تبدأ بـ {self.current_answer[0]} وتنتهي بـ {self.current_answer[-1]}"
        return {'message': hint, 'response': self._create_text_message(hint), 'points': 0}

    if normalized == "جاوب":
        reveal = f"الإجابة: {self.current_answer}"
        self.previous_question = self.scramble_word(self.current_answer)
        self.previous_answer = self.current_answer
        self.current_question += 1
        self.answered_users.clear()

        if self.current_question >= self.questions_count:
            result = self.end_game()
            result['message'] = f"{reveal}\n{result.get('message', '')}"
            return result

        return {'message': reveal, 'response': self.get_question(), 'points': 0}

    if normalized == self.normalize_text(self.current_answer):
        points = self.add_score(user_id, display_name, 10)
        self.previous_question = self.scramble_word(self.current_answer)
        self.previous_answer = self.current_answer
        self.current_question += 1
        self.answered_users.clear()

        if self.current_question >= self.questions_count:
            result = self.end_game()
            result['points'] = points
            result['message'] = f"إجابة صحيحة\n+{points} نقطة\n{result.get('message', '')}"
            return result

        return {'message': f"إجابة صحيحة\n+{points} نقطة", 'response': self.get_question(), 'points': points}

    return {'message': "إجابة غير صحيحة", 'response': self._create_text_message("إجابة غير صحيحة"), 'points': 0}
