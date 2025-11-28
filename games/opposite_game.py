"""
لعبة الأضداد - ستايل زجاجي احترافي
Created by: Abeer Aldosari © 2025
"""

from games.base_game import BaseGame
import random
from typing import Dict, Any, Optional


class OppositeGame(BaseGame):
    """لعبة الأضداد"""

    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, questions_count=5)
        self.game_name = "أضداد"
        self.game_icon = "↔️"

        self.opposites = [
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
            {"word": "فوق", "opposite": ["تحت"]},
            {"word": "داخل", "opposite": ["خارج"]},
            {"word": "ساخن", "opposite": ["بارد"]},
            {"word": "ناعم", "opposite": ["خشن"]},
            {"word": "حلو", "opposite": ["مر", "حامض"]}
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
                        {"type": "text", "text": "الكلمة السابقة:", "size": "xs", "color": colors["text2"], "weight": "bold"},
                        {"type": "text", "text": self.previous_question, "size": "xs", "color": colors["text2"], "wrap": True, "margin": "xs"},
                        {"type": "text", "text": f"✅ الضد: {self.previous_answer}", "size": "xs", "color": colors["success"], "wrap": True, "margin": "xs"}
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
                            {"type": "text", "text": self.game_name, "size": "xxl", "weight": "bold", "color": colors["text"], "align": "center"},
                            {"type": "text", "text": f"سؤال {self.current_question + 1} من {self.questions_count}", "size": "sm", "color": colors["text2"], "align": "center", "margin": "sm"}
                        ]
                    },
                    {"type": "separator", "margin": "xl", "color": colors["shadow1"]}
                ] + previous_section + [
                    {"type": "text", "text": "↔️ ما هو عكس هذه الكلمة؟", "size": "md", "color": colors["text"], "weight": "bold", "align": "center", "wrap": True, "margin": "lg"},
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [{"type": "text", "text": q_data["word"], "size": "xxl", "color": colors["primary"], "weight": "bold", "align": "center"}],
                        "backgroundColor": colors["card"],
                        "cornerRadius": "20px",
                        "paddingAll": "30px",
                        "margin": "md"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [{"type": "text", "text": "💡 فكر في المعنى المعاكس تماماً", "size": "sm", "color": colors["text2"], "align": "center", "wrap": True}],
                        "backgroundColor": colors["card"],
                        "cornerRadius": "15px",
                        "paddingAll": "15px",
                        "margin": "lg"
                    },
                    {"type": "text", "text": "💡 اكتب 'لمح' للتلميح أو 'جاوب' للإجابة", "size": "xs", "color": colors["text2"], "align": "center", "wrap": True, "margin": "md"},
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "spacing": "sm",
                        "contents": [
                            {"type": "button", "action": {"type": "message", "label": "لمح", "text": "لمح"}, "style": "secondary", "height": "sm", "color": colors["shadow1"]},
                            {"type": "button", "action": {"type": "message", "label": "جاوب", "text": "جاوب"}, "style": "secondary", "height": "sm", "color": colors["shadow1"]}
                        ],
                        "margin": "xl"
                    },
                    {"type": "button", "action": {"type": "message", "label": "إيقاف", "text": "إيقاف"}, "style": "primary", "height": "sm", "color": colors["error"], "margin": "sm"}
                ],
                "backgroundColor": colors["bg"],
                "paddingAll": "24px"
            },
            "styles": {"body": {"backgroundColor": colors["bg"]}}
        }
        
        return self._create_flex_with_buttons("أضداد", flex_content)

    def check_answer(self, user_answer: str, user_id: str, display_name: str):
        if not self.game_active or user_id in self.answered_users:
            return None

        normalized = self.normalize_text(user_answer)

        if normalized == "لمح":
            hint = f"💡 يبدأ بحرف: {self.current_answer[0][0]}\n📏 عدد الحروف: {len(self.current_answer[0])}"
            return {'message': hint, 'response': self._create_text_message(hint), 'points': 0}

        if normalized == "جاوب":
            answer_text = " أو ".join(self.current_answer)
            reveal = f"📝 الإجابة: {answer_text}"
            self.previous_question = self.used_words[-1]["word"]
            self.previous_answer = answer_text
            self.current_question += 1
            self.answered_users.clear()

            if self.current_question >= self.questions_count:
                result = self.end_game()
                result['message'] = f"{reveal}\n\n{result.get('message', '')}"
                return result

            return {'message': reveal, 'response': self.get_question(), 'points': 0}

        # التحقق من الإجابة
        for correct in self.current_answer:
            if normalized == self.normalize_text(correct):
                points = self.add_score(user_id, display_name, 10)
                self.previous_question = self.used_words[-1]["word"]
                self.previous_answer = correct
                self.current_question += 1
                self.answered_users.clear()

                if self.current_question >= self.questions_count:
                    result = self.end_game()
                    result['points'] = points
                    result['message'] = f"✅ صحيح يا {display_name}!\n+{points} نقطة\n\n{result.get('message', '')}"
                    return result

                return {'message': f"✅ صحيح يا {display_name}!\n+{points} نقطة", 'response': self.get_question(), 'points': points}

        return {'message': "❌ إجابة غير صحيحة", 'response': self._create_text_message("❌ إجابة غير صحيحة"), 'points': 0}
