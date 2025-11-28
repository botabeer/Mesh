“””
لعبة الأضداد - ستايل زجاجي احترافي
Created by: Abeer Aldosari © 2025
✅ دعم فردي + فريقين
“””

from games.base_game import BaseGame
import random

class OppositeGame(BaseGame):
“”“لعبة الأضداد”””

```
def __init__(self, line_bot_api):
    super().__init__(line_bot_api, questions_count=5)
    self.game_name = "أضداد"
    self.game_icon = ""

    self.opposites = [
        {"word": "كبير", "opposite": ["صغير"]},
        {"word": "طويل", "opposite": ["قصير"]},
        {"word": "سريع", "opposite": ["بطيء"]},
        {"word": "قوي", "opposite": ["ضعيف"]},
        {"word": "حار", "opposite": ["بارد"]},
        {"word": "نظيف", "opposite": ["وسخ", "قذر"]},
        {"word": "سهل", "opposite": ["صعب"]},
        {"word": "جميل", "opposite": ["قبيح"]},
        {"word": "غني", "opposite": ["فقير"]},
        {"word": "ثقيل", "opposite": ["خفيف"]},
        {"word": "عميق", "opposite": ["سطحي"]},
        {"word": "واسع", "opposite": ["ضيق"]},
        {"word": "مظلم", "opposite": ["مضيء"]},
        {"word": "رطب", "opposite": ["جاف"]},
        {"word": "قديم", "opposite": ["جديد"]},
        {"word": "بعيد", "opposite": ["قريب"]},
        {"word": "مرتفع", "opposite": ["منخفض"]},
        {"word": "داخل", "opposite": ["خارج"]},
        {"word": "ناعم", "opposite": ["خشن"]},
        {"word": "حلو", "opposite": ["مر"]},
        {"word": "ذكي", "opposite": ["غبي"]},
        {"word": "نشط", "opposite": ["كسول"]},
        {"word": "مفتوح", "opposite": ["مغلق"]},
        {"word": "ممتلئ", "opposite": ["فارغ"]},
        {"word": "هادئ", "opposite": ["صاخب"]},
        {"word": "واضح", "opposite": ["غامض"]},
        {"word": "مستقيم", "opposite": ["منحني"]},
        {"word": "سعيد", "opposite": ["حزين"]},
        {"word": "سميك", "opposite": ["رفيع"]},
        {"word": "مشرق", "opposite": ["قاتم"]},
        {"word": "حاد", "opposite": ["غير حاد"]},
        {"word": "مبكر", "opposite": ["متأخر"]},
        {"word": "مجتهد", "opposite": ["مهمل"]},
        {"word": "خفيف", "opposite": ["ثقيل"]},
        {"word": "نشوان", "opposite": ["حزين"]},
        {"word": "صافي", "opposite": ["عكر"]},
        {"word": "بطيء", "opposite": ["سريع"]},
        {"word": "مؤدب", "opposite": ["وقح"]},
        {"word": "ثابت", "opposite": ["متغير"]},
        {"word": "قريب", "opposite": ["بعيد"]},
        {"word": "جاف", "opposite": ["رطب"]},
        {"word": "مرتب", "opposite": ["فوضوي"]},
        {"word": "نشاط", "opposite": ["خمول"]},
        {"word": "سريع الفهم", "opposite": ["بطيء الفهم"]},
        {"word": "منتظم", "opposite": ["عشوائي"]},
        {"word": "لطيف", "opposite": ["قاس"]},
    ]
    random.shuffle(self.opposites)
    self.used_words = []

def start_game(self):
    self.current_question = 0
    self.game_active = True
    self.previous_question = None
    self.previous_answer = None
    self.answered_users.clear()
    self.used_words = []
    return self.get_question()

def get_question(self):
    available = [w for w in self.opposites if w not in self.used_words]
    if not available:
        self.used_words = []
        available = self.opposites.copy()

    q_data = random.choice(available)
    self.used_words.append(q_data)
    self.current_answer = q_data["opposite"]

    colors = self.get_theme_colors()

    previous_section = []
    if self.previous_question and self.previous_answer:
        previous_section = [
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "الكلمة السابقة", "size": "xs", "color": colors["text2"]},
                    {"type": "text", "text": self.previous_question, "size": "xs", "color": colors["text2"]},
                    {"type": "text", "text": f"الضد: {self.previous_answer}", "size": "xs", "color": colors["success"]},
                ],
                "backgroundColor": colors["card"],
                "cornerRadius": "15px",
                "paddingAll": "12px",
                "margin": "md"
            }
        ]

    flex_content = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": self.game_name, "size": "xxl", "weight": "bold", "color": colors["text"], "align": "center"},
                {"type": "separator", "margin": "lg"}
            ] + previous_section + [
                {"type": "text", "text": "ما هو عكس هذه الكلمة؟", "size": "md", "color": colors["text"], "align": "center", "margin": "lg"},
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [{"type": "text", "text": q_data["word"], "size": "xxl", "weight": "bold", "align": "center"}],
                    "backgroundColor": colors["card"],
                    "cornerRadius": "20px",
                    "paddingAll": "30px",
                    "margin": "md"
                },
                {"type": "button",
                 "action": {"type": "message", "label": "إيقاف", "text": "إيقاف"},
                 "style": "primary",
                 "height": "sm",
                 "color": colors["error"],
                 "margin": "lg"}
            ],
            "backgroundColor": colors["bg"],
            "paddingAll": "24px"
        }
    }

    return self._create_flex_with_buttons(self.game_name, flex_content)

def check_answer(self, user_answer: str, user_id: str, display_name: str):
    if not self.game_active:
        return None

    # منع غير المنضمين في وضع الفريقين
    if self.team_mode and user_id not in self.joined_users:
        return None

    normalized = self.normalize_text(user_answer)

    # وضع فردي فقط يدعم لمح / جاوب
    if not self.team_mode:
        if normalized == "لمح":
            hint = f"يبدأ بحرف: {self.current_answer[0][0]}"
            return {'message': hint, 'response': self._create_text_message(hint), 'points': 0}

        if normalized == "جاوب":
            answer_text = " أو ".join(self.current_answer)
            reveal = f"الإجابة: {answer_text}"
            self.previous_question = self.used_words[-1]["word"]
            self.previous_answer = answer_text
            self.current_question += 1
            self.answered_users.clear()

            if self.current_question >= self.questions_count:
                result = self.end_game()
                result['message'] = f"{reveal}\n🏆 نهاية اللعبة"
                return result

            return {'message': reveal, 'response': self.get_question(), 'points': 0}

    # التحقق من الإجابة
    for correct in self.current_answer:
        if normalized == self.normalize_text(correct):

            if self.team_mode:
                team = self.get_user_team(user_id)
                if not team:
                    team = self.assign_to_team(user_id)
                self.add_team_score(team, 10)
                points = 10
            else:
                if user_id in self.answered_users:
                    return None
                points = self.add_score(user_id, display_name, 10)

            self.previous_question = self.used_words[-1]["word"]
            self.previous_answer = correct
            self.current_question += 1
            self.answered_users.clear()

            if self.current_question >= self.questions_count:
                result = self.end_game()
                result['points'] = points
                result['message'] = f"🏆 نهاية الجولة"
                return result

            return {
                'message': f"إجابة صحيحة\n+{points} نقطة",
                'response': self.get_question(),
                'points': points
            }

    return {
        'message': "إجابة غير صحيحة",
        'response': self._create_text_message("إجابة غير صحيحة"),
        'points': 0
    }
