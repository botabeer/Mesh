"""
لعبة سلسلة الكلمات - نسخة إنتاج نهائية
Created by: Abeer Aldosari © 2025
"""

from games.base_game import BaseGame
import random
import time
from typing import Dict, Any, Optional


class ChainWordsGame(BaseGame):
    """لعبة سلسلة الكلمات - فردي + فريقين + وقت + صدارة"""

    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, questions_count=5)
        self.game_name = "سلسلة كلمات"
        self.game_icon = "🔗"
        self.supports_hint = False
        self.supports_reveal = False

        # كلمات البداية (أساسية + 50 إضافية)
        self.starting_words = [
            "سيارة","تفاح","قلم","نجم","كتاب","باب","رمل","لعبة","حديقة","ورد",
            "دفتر","معلم","منزل","شمس","سفر","رياضة","علم","مدرسة","طائرة","عصير",

            "بحر","سماء","طريق","جبل","مدينة","شجرة","حاسب","هاتف","ساعة","مطر",
            "زهرة","سرير","مطبخ","نافذة","مفتاح","مصباح","وسادة","بطارية","لوحة",
            "حقيبة","مزرعة","قطار","مكتبة","مستشفى","ملعب","مسبح","مقهى","مكتب","مطار"
        ]

        self.last_word = None
        self.used_words = set()

        # ⏱️ نظام الوقت
        self.round_time = 25
        self.round_start_time = None

        # 👥 نظام الفريقين
        self.team_mode = False
        self.teams = {"A": set(), "B": set()}
        self.team_scores = {"A": 0, "B": 0}

    # =========================
    # بدء اللعبة
    # =========================
    def start_game(self):
        self.current_question = 0
        self.game_active = True
        self.last_word = random.choice(self.starting_words)
        self.used_words = {self.normalize_text(self.last_word)}
        self.answered_users.clear()
        self.round_start_time = time.time()

        self._auto_detect_mode()
        return self.get_question()

    # =========================
    # تحديد فردي أو فريقين تلقائياً
    # =========================
    def _auto_detect_mode(self):
        if self.session_type == "group":
            self.team_mode = True
            self.teams = {"A": set(), "B": set()}
            self.team_scores = {"A": 0, "B": 0}
        else:
            self.team_mode = False

    # =========================
    # عرض السؤال
    # =========================
    def get_question(self):
        required_letter = self.last_word[-1]
        self.round_start_time = time.time()
        colors = self.get_theme_colors()

        subtitle = f"⏱️ {self.round_time} ثانية"
        if self.team_mode:
            subtitle = f"فريق A: {self.team_scores['A']} | فريق B: {self.team_scores['B']}"

        flex_content = {
            "type": "bubble",
            "size": "kilo",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text","text": f"{self.game_icon} {self.game_name}","weight": "bold","size": "xl","align": "center"},
                    {"type": "text","text": subtitle,"size": "sm","align": "center","margin": "xs"},
                    {"type": "separator","margin": "lg"},
                    {"type": "text","text": "الكلمة السابقة","size": "sm","align": "center"},
                    {"type": "text","text": self.last_word,"size": "xxl","weight": "bold","align": "center","margin": "md"},
                    {"type": "separator","margin": "lg"},
                    {"type": "text","text": f"ابدأ بحرف: {required_letter}","size": "lg","weight": "bold","align": "center"},
                ]
            }
        }

        return self._create_flex_with_buttons("سلسلة الكلمات", flex_content)

    # =========================
    # التحقق من الوقت
    # =========================
    def _time_expired(self):
        return (time.time() - self.round_start_time) > self.round_time

    # =========================
    # معالجة الإجابات
    # =========================
    def check_answer(self, user_answer: str, user_id: str, display_name: str) -> Optional[Dict[str, Any]]:
        if not self.game_active:
            return None

        if self._time_expired():
            self.current_question += 1
            self.answered_users.clear()
            return {
                "message": "⏱️ انتهى الوقت",
                "response": self.get_question(),
                "points": 0
            }

        normalized_answer = self.normalize_text(user_answer)

        if normalized_answer in self.used_words:
            return {"message": "❌ الكلمة مستخدمة من قبل","response": self._create_text_message("❌ الكلمة مستخدمة من قبل"),"points": 0}

        required_letter = self.normalize_text(self.last_word[-1])

        if normalized_answer and normalized_answer[0] == required_letter and len(normalized_answer) >= 2:
            self.used_words.add(normalized_answer)
            self.last_word = user_answer.strip()
            self.current_question += 1
            self.answered_users.clear()

            # ===== نقاط فردي =====
            if not self.team_mode:
                points = self.add_score(user_id, display_name, 10)

            # ===== نقاط الفرق =====
            else:
                team = self.get_user_team(user_id)
                if not team:
                    team = self.assign_user_to_team(user_id)

                self.team_scores[team] += 10
                points = 10
                self.save_team_score(team, self.team_scores[team])

            if self.current_question >= self.questions_count:
                return self.end_game()

            return {
                "message": f"✅ صحيح +{points}",
                "response": self.get_question(),
                "points": points
            }

        return {
            "message": f"❌ يجب أن تبدأ الكلمة بحرف {required_letter}",
            "response": self._create_text_message(f"❌ يجب أن تبدأ الكلمة بحرف {required_letter}"),
            "points": 0
        }

    # =========================
    # توزيع الفريقين
    # =========================
    def assign_user_to_team(self, user_id):
        if len(self.teams["A"]) <= len(self.teams["B"]):
            self.teams["A"].add(user_id)
            return "A"
        else:
            self.teams["B"].add(user_id)
            return "B"

    def get_user_team(self, user_id):
        if user_id in self.teams["A"]:
            return "A"
        if user_id in self.teams["B"]:
            return "B"
        return None

    # =========================
    # الصدارة + SQLite
    # =========================
    def save_team_score(self, team, score):
        try:
            self.db.execute(
                "INSERT INTO team_scores(game, team, score) VALUES (?, ?, ?)",
                (self.game_name, team, score)
            )
            self.db.commit()
        except:
            pass

    # =========================
    # نهاية اللعبة
    # =========================
    def end_game(self):
        self.game_active = False

        if not self.team_mode:
            leaderboard = self.get_leaderboard()
            return {
                "message": f"🏆 انتهت اللعبة\n{leaderboard}",
                "points": 0
            }

        winner = "A" if self.team_scores["A"] > self.team_scores["B"] else "B"
        return {
            "message": f"🏆 الفريق الفائز: {winner}\nA: {self.team_scores['A']} | B: {self.team_scores['B']}",
            "points": 0
        }
