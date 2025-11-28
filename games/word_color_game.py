"""
لعبة لون الكلمة (Stroop Effect) - ستايل زجاجي احترافي
نسخة متوافقة مع اللعب الفردي + وضع فريقين في المجموعات
Created by: Abeer Aldosari © 2025
"""

from games.base_game import BaseGame
import random


class WordColorGame(BaseGame):
    """لعبة لون الكلمة (Stroop Test)"""

    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, questions_count=5)
        self.game_name = "لون"
        self.game_icon = "🎨"

        # دعم الأوضاع
        self.team_mode = False
        self.joined_players = []
        self.teams = {"A": [], "B": []}
        self.team_scores = {"A": 0, "B": 0}

        self.colors = {
            "أحمر": "#E53E3E",
            "أزرق": "#3182CE",
            "أخضر": "#38A169",
            "أصفر": "#D69E2E",
            "برتقالي": "#DD6B20",
            "بنفسجي": "#805AD5",
            "وردي": "#D53F8C",
            "بني": "#8B4513"
        }
        self.color_names = list(self.colors.keys())

    # ==============================
    # بدء اللعبة
    # ==============================
    def start_game(self):
        self.current_question = 0
        self.game_active = True
        self.previous_question = None
        self.previous_answer = None
        self.answered_users.clear()

        # تصفير وضع الفريقين
        self.team_mode = False
        self.joined_players = []
        self.teams = {"A": [], "B": []}
        self.team_scores = {"A": 0, "B": 0}

        return self.get_question()

    # ==============================
    # بدء وضع فريقين
    # ==============================
    def start_team_mode(self):
        self.team_mode = True
        self.joined_players = []
        self.teams = {"A": [], "B": []}
        self.team_scores = {"A": 0, "B": 0}
        return self._create_text_message("✅ تم تفعيل وضع فريقين\n✍️ اكتب (انضم) للدخول")

    def split_teams(self):
        for i, player in enumerate(self.joined_players):
            if i % 2 == 0:
                self.teams["A"].append(player)
            else:
                self.teams["B"].append(player)

    # ==============================
    # توليد السؤال
    # ==============================
    def get_question(self):
        word = random.choice(self.color_names)
        color_name = random.choice([c for c in self.color_names if c != word]) if random.random() < 0.7 else word
        self.current_answer = color_name

        colors = self.get_theme_colors()

        text = f"🎨 ما لون هذه الكلمة؟\n\n{word}"

        return self._create_text_message(text)

    # ==============================
    # التحقق من الإجابة
    # ==============================
    def check_answer(self, user_answer: str, user_id: str, display_name: str):

        # ======================
        # أوامر الفريقين
        # ======================
        if user_answer == "فريقين":
            return {"response": self.start_team_mode(), "points": 0}

        if user_answer == "انضم" and self.team_mode:
            if user_id not in self.joined_players:
                self.joined_players.append(user_id)
                return {"response": self._create_text_message(f"✅ {display_name} انضم"), "points": 0}
            return None

        if user_answer == "انسحب" and self.team_mode:
            if user_id in self.joined_players:
                self.joined_players.remove(user_id)
                for t in self.teams.values():
                    if user_id in t:
                        t.remove(user_id)
                return {"response": self._create_text_message(f"❌ {display_name} انسحب"), "points": 0}
            return None

        # ======================
        # تجاهل غير المنضمين
        # ======================
        if self.team_mode and user_id not in self.joined_players:
            return None

        normalized = self.normalize_text(user_answer)
        normalized_correct = self.normalize_text(self.current_answer)
        is_correct = normalized == normalized_correct

        # ======================
        # تقسيم الفرق أول مرة
        # ======================
        if self.team_mode and not self.teams["A"] and not self.teams["B"]:
            self.split_teams()

        # ======================
        # في حالة الإجابة الصحيحة
        # ======================
        if is_correct:
            team = None
            if self.team_mode:
                team = "A" if user_id in self.teams["A"] else "B"
                self.team_scores[team] += 1
            else:
                self.add_score(user_id, display_name, 10)

            self.current_question += 1
            self.answered_users.clear()

            if self.current_question >= self.questions_count:
                self.game_active = False

                if self.team_mode:
                    winner = "A" if self.team_scores["A"] > self.team_scores["B"] else "B"
                    return {
                        "response": self._create_text_message(
                            f"🏆 انتهت اللعبة\n"
                            f"فريق A: {self.team_scores['A']} نقطة\n"
                            f"فريق B: {self.team_scores['B']} نقطة\n"
                            f"🎉 الفائز: فريق {winner}"
                        ),
                        "points": 0
                    }

                return {
                    "response": self._create_text_message("✅ انتهت اللعبة"),
                    "points": 10
                }

            return {
                "response": self.get_question(),
                "points": 10
            }

        # ======================
        # في حالة الخطأ
        # ======================
        return {
            "response": self._create_text_message("❌ إجابة غير صحيحة"),
            "points": 0
        }
