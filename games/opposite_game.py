from games.base_game import BaseGame
import random
import time
from typing import Dict, Any, Optional, List


class GuessGame(BaseGame):
    """لعبة التخمين - فردي + فريقين + عداد + صدارة"""

    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, questions_count=5)
        self.game_name = "تخمين"
        self.game_icon = "🔮"
        self.supports_hint = True
        self.supports_reveal = True

        # ✅ مؤقت
        self.time_limit = 25  # ثواني لكل سؤال
        self.question_start_time = None

        # ✅ فرق
        self.team_mode = False
        self.joined_users = set()
        self.user_teams = {}
        self.team_scores = {"team1": 0, "team2": 0}

        # البيانات
        self.items = {
            "المطبخ": {
                "ق": ["قدر", "قلاية"],
                "م": ["ملعقة", "مغرفة"],
                "س": ["سكين", "صحن"],
                "ط": ["طنجرة"],
                "ف": ["فرن", "فنجان"]
            },
            "غرفة النوم": {
                "س": ["سرير"],
                "و": ["وسادة"],
                "م": ["مرآة", "مخدة"],
                "خ": ["خزانة"],
                "ل": ["لحاف"]
            },
            "المدرسة": {
                "ق": ["قلم"],
                "د": ["دفتر"],
                "ك": ["كتاب"],
                "م": ["مسطرة", "ممحاة"],
                "س": ["سبورة"],
                "ح": ["حقيبة"]
            },
            "الفواكه": {
                "ت": ["تفاح", "تمر"],
                "م": ["موز", "مشمش"],
                "ع": ["عنب"],
                "ب": ["برتقال", "بطيخ"],
                "ر": ["رمان"],
                "ك": ["كمثرى"]
            },
            "الحيوانات": {
                "ق": ["قطة"],
                "س": ["سنجاب"],
                "ف": ["فيل"],
                "أ": ["أسد", "أرنب"],
                "ج": ["جمل"],
                "ن": ["نمر"]
            }
        }

        # إنشاء الأسئلة
        self.questions_list: List[Dict[str, Any]] = []
        for category, letters in self.items.items():
            for letter, words in letters.items():
                self.questions_list.append({
                    "category": category,
                    "letter": letter,
                    "answers": words
                })

        random.shuffle(self.questions_list)
        self.previous_question = None
        self.previous_answer = None

    # =========================
    # ✅ بدء اللعبة
    # =========================
    def start_game(self):
        self.current_question = 0
        self.game_active = True
        self.previous_question = None
        self.previous_answer = None
        self.answered_users.clear()
        self.scores.clear()

        self.team_scores = {"team1": 0, "team2": 0}
        self.question_start_time = time.time()

        return self.get_question()

    # =========================
    # ✅ عرض السؤال
    # =========================
    def get_question(self):
        q_data = self.questions_list[self.current_question % len(self.questions_list)]
        self.current_answer = q_data["answers"]

        self.question_start_time = time.time()

        remaining = self.time_limit
        timer_text = f"⏱️ {remaining} ثانية"

        question_text = (
            f"الفئة: {q_data['category']}\n"
            f"يبدأ بحرف: {q_data['letter']}\n\n"
            f"{timer_text}"
        )

        additional_info = None if self.team_mode else "اكتب 'لمح' أو 'جاوب'"

        return self.build_question_flex(
            question_text=question_text,
            additional_info=additional_info
        )

    # =========================
    # ✅ التلميح
    # =========================
    def get_hint(self) -> str:
        answer = self.current_answer[0]
        if len(answer) <= 2:
            return f"💡 {answer[0]}_"

        return f"💡 {answer[0]}{answer[1]}{'_' * (len(answer) - 2)}"

    # =========================
    # ✅ التحقق من الإجابة
    # =========================
    def check_answer(self, user_answer: str, user_id: str, display_name: str) -> Optional[Dict[str, Any]]:
        if not self.game_active:
            return None

        # ✅ التحقق من الوقت
        if time.time() - self.question_start_time > self.time_limit:
            answer_text = " أو ".join(self.current_answer)
            self.current_question += 1

            if self.current_question >= self.questions_count:
                result = self.end_game()
                result["message"] = f"⏱️ انتهى الوقت\nالإجابة: {answer_text}\n\n{result.get('message','')}"
                return result

            return {
                "message": f"⏱️ انتهى الوقت\nالإجابة: {answer_text}",
                "response": self.get_question(),
                "points": 0
            }

        if self.team_mode and user_id not in self.joined_users:
            return None

        normalized = self.normalize_text(user_answer)

        # ✅ فردي فقط
        if not self.team_mode:
            if normalized == "لمح":
                hint = self.get_hint()
                return {"message": hint, "response": self._create_text_message(hint), "points": 0}

            if normalized == "جاوب":
                answers_text = " أو ".join(self.current_answer)
                self.current_question += 1

                if self.current_question >= self.questions_count:
                    result = self.end_game()
                    result["message"] = f"الإجابة: {answers_text}\n\n{result.get('message','')}"
                    return result

                return {"message": answers_text, "response": self.get_question(), "points": 0}

        # ✅ التحقق الصحيح
        for correct in self.current_answer:
            if self.normalize_text(correct) == normalized:

                if self.team_mode:
                    team = self.get_user_team(user_id) or self.assign_to_team(user_id)
                    self.add_team_score(team, 10)
                    points = 10
                else:
                    points = self.add_score(user_id, display_name, 10)

                self.current_question += 1

                if self.current_question >= self.questions_count:
                    result = self.end_game()
                    result["points"] = points
                    return result

                return {
                    "message": f"✅ إجابة صحيحة\n+{points} نقطة",
                    "response": self.get_question(),
                    "points": points
                }

        return {
            "message": "❌ إجابة غير صحيحة",
            "response": self._create_text_message("❌ إجابة غير صحيحة"),
            "points": 0
        }

    # =========================
    # ✅ معلومات اللعبة
    # =========================
    def get_game_info(self) -> Dict[str, Any]:
        return {
            "name": self.game_name,
            "questions_count": self.questions_count,
            "supports_hint": True,
            "supports_reveal": True,
            "team_mode": self.team_mode,
            "time_limit": self.time_limit
        }
