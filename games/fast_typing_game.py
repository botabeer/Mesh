"""
لعبة الكتابة السريعة - إصدار تنافسي متكامل
Created by: Abeer Aldosari © 2025
"""

from games.base_game import BaseGame
import random
from datetime import datetime
from typing import Dict, Any, Optional


class FastTypingGame(BaseGame):
    """لعبة الكتابة السريعة التنافسية"""

    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, questions_count=5)
        self.game_name = "كتابة سريعة"
        self.game_icon = "⚡"

        self.supports_hint = False
        self.supports_reveal = False

        # 50 عبارة (أذكار + أدعية + حكم)
        self.phrases = [
            "سبحان الله", "الحمد لله", "لا إله إلا الله", "الله أكبر",
            "استغفر الله", "حسبي الله ونعم الوكيل", "لا حول ولا قوة إلا بالله",
            "اللهم صل على محمد", "اللهم اغفر لي", "اللهم ارحمنا",
            "رضيت بالله رباً", "اليقين لا يزول بالشك", "الصبر مفتاح الفرج",
            "التوكل على الله", "الأمل حياة", "الصدق نجاة",
            "كل تأخيرة فيها خيرة", "من جد وجد", "الصمت حكمة",
            "النية أساس العمل", "بر الوالدين طريق الجنة",
            "القناعة كنز", "الدعاء سلاح المؤمن",
            "راحة البال كنز", "الإخلاص سر النجاح",
            "العمل عبادة", "التواضع رفعة",
            "من صبر ظفر", "العلم نور",
            "ذكر الله طمأنينة", "الحكمة ضالة المؤمن",
            "من توكل كُفي", "البسمة صدقة",
            "القلب إذا صلح", "لا تيأس أبداً",
            "الخير قادم", "الثبات نجاح",
            "السعي عبادة", "العفو قوة",
            "الزهد راحة", "العدل أساس الملك",
            "الإحسان حياة", "الوفاء شيمة",
            "الرضا سر الراحة", "التفاؤل عبادة",
            "الأمانة شرف", "الصبر جميل",
            "ذكر الله حياة", "الصدق أمان"
        ]

        random.shuffle(self.phrases)
        self.used_phrases = []
        self.question_start_time = None

    # =========================
    # بدء اللعبة
    # =========================
    def start_game(self):
        self.current_question = 0
        self.game_active = True
        self.previous_question = None
        self.previous_answer = None
        self.answered_users.clear()
        return self.get_question()

    # =========================
    # عرض السؤال
    # =========================
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

        flex_content = {
            "type": "bubble",
            "size": "kilo",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": self.game_name, "size": "xl",
                     "weight": "bold", "color": colors["text"], "align": "center"},
                    {"type": "text", "text": f"جولة {self.current_question + 1} من {self.questions_count}",
                     "size": "sm", "color": colors["text2"], "align": "center"},

                    {"type": "separator", "margin": "lg"},

                    {"type": "text", "text": "اكتب العبارة التالية كما هي ⏱️",
                     "size": "md", "color": colors["text"], "align": "center"},

                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {"type": "text", "text": phrase, "size": "xl",
                             "color": colors["primary"], "weight": "bold",
                             "align": "center", "wrap": True}
                        ],
                        "backgroundColor": colors["card"],
                        "cornerRadius": "20px",
                        "paddingAll": "24px",
                        "margin": "lg"
                    },

                    {"type": "text",
                     "text": "أسرع إجابة صحيحة تحصد نقاطاً أعلى",
                     "size": "xs", "align": "center", "color": colors["text2"]},

                    {"type": "button",
                     "action": {"type": "message", "label": "إيقاف", "text": "إيقاف"},
                     "style": "primary", "color": colors["error"], "margin": "lg"}
                ],
                "paddingAll": "24px"
            }
        }

        return self._create_flex_with_buttons(self.game_name, flex_content)

    # =========================
    # التحقق من الإجابة
    # =========================
    def check_answer(self, user_answer: str, user_id: str, display_name: str):

        if not self.game_active or user_id in self.answered_users:
            return None

        text = user_answer.strip()

        time_taken = (datetime.now() - self.question_start_time).total_seconds()

        # ✅ إجابة صحيحة
        if text == self.current_answer:

            base_points = 10
            speed_bonus = 5 if time_taken <= 5 else 0
            total_points = base_points + speed_bonus

            # ✅ وضع الفريقين
            if self.is_team_mode:
                team = self.get_team_of_user(user_id)
                points = self.add_team_score(team, total_points)
            else:
                points = self.add_score(user_id, display_name, total_points)

            self.previous_question = self.current_answer
            self.previous_answer = f"{time_taken:.1f} ثانية"

            self.answered_users.add(user_id)
            self.current_question += 1
            self.answered_users.clear()

            # ✅ نهاية اللعبة
            if self.current_question >= self.questions_count:
                return self.end_game_with_leaderboard(points)

            return {
                'message': f"صحيح ⏱️ {time_taken:.1f}ث +{total_points} نقطة",
                'response': self.get_question(),
                'points': total_points
            }

        # ❌ خطأ
        return {
            'message': f"خطأ إملائي ⏱️ {time_taken:.1f}ث",
            'response': self._create_text_message("الإجابة غير مطابقة تماماً"),
            'points': 0
        }

    # =========================
    # معلومات اللعبة
    # =========================
    def get_game_info(self) -> Dict[str, Any]:
        info = super().get_game_info()
        info.update({
            "description": "لعبة سرعة ودقة بنظام تنافسي فردي أو فرق",
            "phrases_count": len(self.phrases),
            "supports_teams": True,
            "supports_timer": True,
            "supports_leaderboard": True
        })
        return info
