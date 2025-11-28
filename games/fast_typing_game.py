"""
لعبة الكتابة السريعة - ستايل زجاجي احترافي
Created by: Abeer Aldosari © 2025
"""

from games.base_game import BaseGame
import random
from datetime import datetime
from typing import Dict, Any, Optional


class FastTypingGame(BaseGame):
    """لعبة الكتابة السريعة"""

    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, questions_count=5)
        self.game_name = "كتابة سريعة"
        self.game_icon = "⚡"
        self.supports_hint = False
        self.supports_reveal = True

        self.phrases = [
            "السرعة والدقة مهمتان", "التركيز هو مفتاح النجاح",
            "الممارسة تصنع الإتقان", "الوقت من ذهب",
            "اكتب بسرعة ودقة", "التحدي يبدأ الآن",
            "هيا اثبت مهارتك", "السرعة مع الدقة",
            "لا تستسلم أبداً", "النجاح يحتاج صبر",
            "الإبداع لا حدود له", "كن الأفضل دائماً",
            "التميز هو هدفنا", "احلم واسعى وحقق",
            "المثابرة طريق النجاح", "كل لحظة ثمينة"
        ]
        random.shuffle(self.phrases)
        self.used_phrases = []
        self.question_start_time = None

    def start_game(self):
        self.current_question = 0
        self.game_active = True
        self.previous_question = None
        self.previous_answer = None
        self.answered_users.clear()
        return self.get_question()

    def get_question(self):
        available = [p for p in self.phrases if p not in self.used_phrases]
        if not available:
            self.used_phrases = []
            available = self.phrases.copy()

        phrase = random.choice(available)
        self.used_phrases.append(phrase)
        self.current_answer = phrase
        self.question_start_time = datetime.now()

        colors = self.get_theme_colors()
        
        previous_section = []
        if self.previous_question and self.previous_answer:
            previous_section = [
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "text", "text": "العبارة السابقة:", "size": "xs", "color": colors["text2"], "weight": "bold"},
                        {"type": "text", "text": self.previous_question, "size": "xs", "color": colors["text2"], "wrap": True, "margin": "xs"},
                        {"type": "text", "text": f"✅ {self.previous_answer}", "size": "xs", "color": colors["success"], "wrap": True, "margin": "xs"}
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
                            {"type": "text", "text": f"{self.game_icon} {self.game_name}", "size": "xl", "weight": "bold", "color": colors["text"], "align": "center"},
                            {"type": "text", "text": f"جولة {self.current_question + 1} من {self.questions_count}", "size": "sm", "color": colors["text2"], "align": "center", "margin": "sm"}
                        ]
                    },
                    {"type": "separator", "margin": "lg", "color": colors["shadow1"]}
                ] + previous_section + [
                    {"type": "text", "text": "⚡ اكتب النص التالي بالضبط:", "size": "md", "color": colors["text"], "weight": "bold", "align": "center", "wrap": True, "margin": "lg"},
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [{"type": "text", "text": phrase, "size": "xl", "color": colors["primary"], "weight": "bold", "align": "center", "wrap": True}],
                        "backgroundColor": colors["card"],
                        "cornerRadius": "20px",
                        "paddingAll": "25px",
                        "margin": "md"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {"type": "text", "text": "💡 نصائح:", "size": "sm", "color": colors["text"], "weight": "bold"},
                            {"type": "text", "text": "• اكتب بدقة وسرعة\n• احذر من الأخطاء\n• أقل من 5 ثوانٍ = نقاط إضافية!", "size": "xs", "color": colors["text2"], "wrap": True, "margin": "xs"}
                        ],
                        "backgroundColor": colors["card"],
                        "cornerRadius": "15px",
                        "paddingAll": "15px",
                        "margin": "lg"
                    },
                    {"type": "text", "text": "💡 اكتب 'جاوب' لتخطي السؤال", "size": "xs", "color": colors["text2"], "align": "center", "wrap": True, "margin": "md"},
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "spacing": "sm",
                        "contents": [{"type": "button", "action": {"type": "message", "label": "جاوب", "text": "جاوب"}, "style": "secondary", "height": "sm", "color": colors["shadow1"]}],
                        "margin": "lg"
                    },
                    {"type": "button", "action": {"type": "message", "label": "إيقاف", "text": "إيقاف"}, "style": "primary", "height": "sm", "color": colors["error"], "margin": "sm"}
                ],
                "backgroundColor": colors["bg"],
                "paddingAll": "24px"
            },
            "styles": {"body": {"backgroundColor": colors["bg"]}}
        }

        return self._create_flex_with_buttons(f"{self.game_name}", flex_content)

    def check_answer(self, user_answer: str, user_id: str, display_name: str):
        if not self.game_active or user_id in self.answered_users:
            return None

        text = user_answer.strip()
        normalized = self.normalize_text(text)

        if normalized == 'لمح':
            return {'message': "❌ هذه اللعبة لا تدعم التلميحات", 'response': self._create_text_message("❌ هذه اللعبة لا تدعم التلميحات"), 'points': 0}

        if normalized == 'جاوب':
            reveal = f"📝 العبارة: {self.current_answer}"
            self.previous_question = self.current_answer
            self.previous_answer = "تم التخطي"
            self.current_question += 1
            self.answered_users.clear()

            if self.current_question >= self.questions_count:
                result = self.end_game()
                result['message'] = f"{reveal}\n\n{result.get('message', '')}"
                return result

            return {'message': reveal, 'response': self.get_question(), 'points': 0}

        time_taken = (datetime.now() - self.question_start_time).total_seconds() if self.question_start_time else 0

        if text == self.current_answer:
            points = 10
            speed_bonus = 5 if time_taken < 5 else 0
            points += speed_bonus
            points = self.add_score(user_id, display_name, points)

            if speed_bonus > 0:
                self.previous_question = self.current_answer
                self.previous_answer = f"أنجزت في {time_taken:.1f}ث مع مكافأة!"
            else:
                self.previous_question = self.current_answer
                self.previous_answer = f"أنجزت في {time_taken:.1f}ث"

            self.current_question += 1
            self.answered_users.clear()

            if self.current_question >= self.questions_count:
                result = self.end_game()
                result['points'] = points
                msg = f"🎉 ممتاز! {time_taken:.1f} ثانية!\n⭐ +{speed_bonus} إضافية!\n+{points} نقطة\n\n{result.get('message', '')}" if speed_bonus else f"✅ صحيح! {time_taken:.1f}ث\n+{points} نقطة\n\n{result.get('message', '')}"
                result['message'] = msg
                return result

            msg = f"🎉 ممتاز يا {display_name}!\n⚡ {time_taken:.1f}ث\n⭐ +{speed_bonus} إضافية!\n+{points} نقطة" if speed_bonus else f"✅ صحيح يا {display_name}!\n⏱️ {time_taken:.1f}ث\n+{points} نقطة"
            return {'message': msg, 'response': self.get_question(), 'points': points}

        return {'message': f"❌ خطأ! ⏱️ {time_taken:.1f}ث", 'response': self._create_text_message(f"❌ خطأ إملائي! ⏱️ {time_taken:.1f}ث"), 'points': 0}
