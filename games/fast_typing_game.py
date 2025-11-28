"""
لعبة الكتابة السريعة - إصدار تنافسي نهائي
Created by: Abeer Aldosari © 2025
"""

from games.base_game import BaseGame
import random
from datetime import datetime
from typing import Dict, Any, Optional


class FastTypingGame(BaseGame):
    """لعبة الكتابة السريعة - تنافس فردي + فريقين"""

    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, questions_count=5)
        self.game_name = "الكتابة السريعة"
        self.game_icon = "▪️"
        self.supports_hint = False
        self.supports_reveal = False

        # 50 مثال (أذكار - أدعية - حكم)
        self.phrases = [
            "سبحان الله",
            "الحمد لله",
            "الله أكبر",
            "لا إله إلا الله",
            "رب اغفر لي",
            "توكل على الله",
            "الصبر مفتاح الفرج",
            "من جد وجد",
            "العلم نور",
            "راحة القلب في الذكر",
            "اللهم اهدنا",
            "كن محسنا",
            "الدال على الخير كفاعله",
            "رب زدني علما",
            "اتق الله",
            "خير الأمور أوسطها",
            "اللهم اشف مرضانا",
            "التواضع رفعة",
            "الصدق منجاة",
            "الصمت حكمة",
            "اللهم ارزقني رضاك",
            "النية الصالحة بركة",
            "استغفر الله العظيم",
            "من صبر ظفر",
            "العمل عبادة",
            "القناعة كنز",
            "اللهم يسر أموري",
            "الرحمة قوة",
            "لا تحقرن من المعروف شيئا",
            "الصلاة نور",
            "الدعاء سلاح المؤمن",
            "العفو عند المقدرة",
            "ذكر الله حياة القلوب",
            "العدل أساس الملك",
            "الأمانة شرف",
            "اللهم بارك لنا",
            "اغتنم وقتك",
            "خير الناس أنفعهم",
            "اللهم ثبت قلبي",
            "الصبر جميل",
            "اللسان مرآة العقل",
            "احفظ الله يحفظك",
            "الخير في العطاء",
            "اللهم توفنا مسلمين",
            "السكينة في الطاعة",
            "اجعل نيتك لله",
            "الحق أحق أن يتبع",
            "اللهم حسن الخاتمة",
            "التوبة بداية جديدة"
        ]

        random.shuffle(self.phrases)
        self.used_phrases = []
        self.question_start_time = None

        # نظام الفريقين
        self.team_mode = False
        self.teams = {"A": set(), "B": set()}
        self.team_scores = {"A": 0, "B": 0}

    # -----------------------------
    # بدء اللعبة
    # -----------------------------
    def start_game(self, team_mode: bool = False):
        self.current_question = 0
        self.game_active = True
        self.answered_users.clear()
        self.used_phrases.clear()
        self.team_mode = team_mode
        self.team_scores = {"A": 0, "B": 0}
        return self.get_question()

    # -----------------------------
    # توليد السؤال
    # -----------------------------
    def get_question(self):
        available = [p for p in self.phrases if p not in self.used_phrases]
        if not available:
            self.used_phrases.clear()
            available = self.phrases.copy()

        phrase = random.choice(available)
        self.used_phrases.append(phrase)
        self.current_answer = phrase
        self.question_start_time = datetime.now()

        colors = self.get_theme_colors()

        info_text = (
            "⏱️ الجولة موقتة\n"
            "اكتب النص كما هو تماما\n"
        )

        if self.team_mode:
            info_text += "\nوضع فريقين مفعل"

        return self.build_question_flex(
            question_text=phrase,
            additional_info=info_text
        )

    # -----------------------------
    # فحص الإجابة
    # -----------------------------
    def check_answer(self, user_answer: str, user_id: str, display_name: str):
        if not self.game_active or user_id in self.answered_users:
            return None

        text = user_answer.strip()

        # حساب الزمن
        time_taken = (datetime.now() - self.question_start_time).total_seconds()

        # التحقق
        if text == self.current_answer:
            self.answered_users.add(user_id)

            # نقاط حسب الزمن
            base_points = 10
            speed_bonus = 5 if time_taken <= 5 else 0
            total_points = base_points + speed_bonus

            # توزيع النقاط
            if self.team_mode:
                team = self.get_user_team(user_id)
                self.team_scores[team] += total_points
            else:
                self.add_score(user_id, display_name, total_points)

            self.current_question += 1
            self.answered_users.clear()

            # انتهاء الجولات
            if self.current_question >= self.questions_count:
                return self.end_game()

            msg = f"✅ صحيح • ⏱️ {time_taken:.1f} ثانية"
            return {
                'message': msg,
                'response': self.get_question(),
                'points': total_points
            }

        return {
            'message': f"❌ خطأ • ⏱️ {time_taken:.1f} ثانية",
            'response': self._create_text_message(f"❌ خطأ • ⏱️ {time_taken:.1f} ثانية"),
            'points': 0
        }

    # -----------------------------
    # تحديد فريق اللاعب
    # -----------------------------
    def get_user_team(self, user_id: str):
        if user_id in self.teams["A"]:
            return "A"
        if user_id in self.teams["B"]:
            return "B"
        team = "A" if len(self.teams["A"]) <= len(self.teams["B"]) else "B"
        self.teams[team].add(user_id)
        return team

    # -----------------------------
    # إنهاء اللعبة مع الترتيب
    # -----------------------------
    def end_game(self):
        self.game_active = False

        if self.team_mode:
            a = self.team_scores["A"]
            b = self.team_scores["B"]

            if a > b:
                winner = "🏆 الفريق A"
            elif b > a:
                winner = "🏆 الفريق B"
            else:
                winner = "تعادل"

            message = (
                f"النتيجة النهائية 🏆\n"
                f"الفريق A: {a}\n"
                f"الفريق B: {b}\n\n"
                f"الفائز: {winner}"
            )

            return {
                "game_over": True,
                "points": max(a, b),
                "message": message
            }

        return super().end_game()
