"""
لعبة الكتابة السريعة - Bot Mesh v9.0 FINAL
Created by: Abeer Aldosari © 2025
✅ بدون لمح/جاوب (لعبة سرعة)
✅ مع مؤقت 20 ثانية
"""

from games.base_game import BaseGame
import random
import time
from typing import Dict, Any, Optional


class FastTypingGame(BaseGame):
    """لعبة الكتابة السريعة"""

    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, questions_count=5)
        self.game_name = "كتابة سريعة"
        self.game_icon = "⚡"
        self.supports_hint = False  # ❌ لعبة سرعة
        self.supports_reveal = False  # ❌ لعبة سرعة

        self.round_time = 20  # ⏱️ 20 ثانية
        self.round_start_time = None

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
            "التوبة بداية جديدة",
            "لا حول ولا قوة إلا بالله"
        ]

        random.shuffle(self.phrases)
        self.used_phrases = []

    def start_game(self):
        self.current_question = 0
        self.game_active = True
        self.answered_users.clear()
        self.used_phrases.clear()
        return self.get_question()

    def get_question(self):
        available = [p for p in self.phrases if p not in self.used_phrases]
        if not available:
            self.used_phrases.clear()
            available = self.phrases.copy()

        phrase = random.choice(available)
        self.used_phrases.append(phrase)
        self.current_answer = phrase
        self.round_start_time = time.time()

        additional_info = f"⏱️ {self.round_time} ثانية\nاكتب النص بالضبط"

        return self.build_question_flex(
            question_text=phrase,
            additional_info=additional_info
        )

    def _time_expired(self) -> bool:
        if not self.round_start_time:
            return False
        return (time.time() - self.round_start_time) > self.round_time

    def check_answer(self, user_answer: str, user_id: str, display_name: str) -> Optional[Dict[str, Any]]:
        if not self.game_active:
            return None

        # التحقق من الوقت
        if self._time_expired():
            self.current_question += 1
            self.answered_users.clear()

            if self.current_question >= self.questions_count:
                result = self.end_game()
                result["message"] = f"⏱️ انتهى الوقت!\n\n{result.get('message', '')}"
                return result

            return {
                "message": "⏱️ انتهى الوقت!",
                "response": self.get_question(),
                "points": 0
            }

        if user_id in self.answered_users:
            return None

        if self.team_mode and user_id not in self.joined_users:
            return None

        text = user_answer.strip()

        # حساب الزمن
        time_taken = time.time() - self.round_start_time

        # التحقق من التطابق التام
        if text == self.current_answer:
            self.answered_users.add(user_id)

            # نقاط حسب الزمن
            base_points = 10
            if time_taken <= 5:
                speed_bonus = 10
            elif time_taken <= 10:
                speed_bonus = 5
            else:
                speed_bonus = 0
            
            total_points = base_points + speed_bonus

            if self.team_mode:
                team = self.get_user_team(user_id)
                if not team:
                    team = self.assign_to_team(user_id)
                self.add_team_score(team, total_points)
            else:
                self.add_score(user_id, display_name, total_points)

            self.current_question += 1
            self.answered_users.clear()

            if self.current_question >= self.questions_count:
                result = self.end_game()
                result["points"] = total_points
                return result

            msg = f"✅ صحيح!\n⏱️ {time_taken:.1f}s\n+{total_points} نقطة"
            return {
                "message": msg,
                "response": self.get_question(),
                "points": total_points
            }

        return {
            "message": f"❌ خطأ (⏱️ {time_taken:.1f}s)",
            "response": self._create_text_message(f"❌ خطأ (⏱️ {time_taken:.1f}s)"),
            "points": 0
        }
