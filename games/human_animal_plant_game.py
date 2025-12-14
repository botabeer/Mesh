from games.base_game import BaseGame
import random
from typing import Dict, Any, Optional
from linebot.v3.messaging import FlexMessage, FlexContainer, TextMessage

class HumanAnimalPlantGame(BaseGame):
    """لعبة إنسان - حيوان - نبات محسّنة: 5 جولات، دعم الثيم، لمّح وجاوب"""

    def __init__(self, line_bot_api=None):
        super().__init__(line_bot_api, questions_count=5)
        self.game_name = "إنسان-حيوان-نبات"
        self.supports_hint = True
        self.supports_reveal = True

        self.letters = list("ابتجحدرزسشصطعفقكلمنهوي")
        random.shuffle(self.letters)
        self.categories = ["إنسان", "حيوان", "نبات", "جماد", "بلاد"]

        self.database = {
            # قاعدة بيانات مبسطة لكل فئة وحرف مع كلمات محتملة
            "إنسان": {"م": ["محمد", "مريم"], "أ": ["أحمد", "أمل"], "ع": ["علي", "عمر"]},
            "حيوان": {"أ": ["أسد", "أرنب"], "ج": ["جمل", "جاموس"], "ح": ["حصان", "حمار"]},
            "نبات": {"ت": ["تفاح", "تمر"], "ب": ["بطيخ", "برتقال"], "ر": ["رمان", "ريحان"]},
            "جماد": {"ب": ["باب", "بيت"], "ت": ["تلفاز", "تاج"], "ج": ["جدار", "جسر"]},
            "بلاد": {"أ": ["أمريكا", "ألمانيا"], "ب": ["بريطانيا", "البرازيل"], "ت": ["تركيا", "تونس"]}
        }

        self.current_category = None
        self.current_letter = None

    def start_game(self):
        self.current_question = 0
        self.game_active = True
        self.previous_question = None
        self.previous_answer = None
        self.answered_users.clear()
        self.scores.clear()
        return self.get_question()

    def get_question(self):
        self.current_letter = self.letters[self.current_question % len(self.letters)]
        self.current_category = random.choice(self.categories)
        return self.build_question_flex(
            question_text=f"الفئة: {self.current_category}\nالحرف: {self.current_letter}",
            additional_info=f"السؤال {self.current_question+1}/{self.questions_count}"
        )

    def get_suggested_answer(self) -> Optional[str]:
        """إجابة مقترحة لأمر لمّح أو جاوب"""
        cat = self.current_category
        letter = self.current_letter
        if cat in self.database and letter in self.database[cat]:
            answers = self.database[cat][letter]
            if answers:
                return random.choice(answers)
        return None

    def validate_answer(self, normalized_answer: str) -> bool:
        """التحقق من صحة الإجابة"""
        if not normalized_answer or len(normalized_answer) < 2:
            return False
        return normalized_answer[0] == self.normalize_text(self.current_letter)

    def check_answer(self, user_answer: str, user_id: str, display_name: str) -> Optional[Dict[str, Any]]:
        if not self.game_active or user_id in self.answered_users:
            return None

        normalized = self.normalize_text(user_answer)

        # أمر لمّح
        if self.can_use_hint() and normalized == "لمح":
            suggested = self.get_suggested_answer()
            hint = f"تبدأ بـ {suggested[0]} | عدد الحروف: {len(suggested)}" if suggested else "فكر جيداً"
            return {"message": hint, "points": 0}

        # أمر جاوب
        if self.can_reveal_answer() and normalized == "جاوب":
            suggested = self.get_suggested_answer()
            reveal = suggested if suggested else "لا توجد إجابة ثابتة"
            self.previous_question = f"{self.current_category} - حرف {self.current_letter}"
            self.previous_answer = reveal
            self.current_question += 1
            self.answered_users.clear()
            if self.current_question >= self.questions_count:
                result = self.end_game()
                result["message"] = f"الإجابة: {reveal}\n\nانتهت اللعبة"
                return result
            return {"message": f"الإجابة: {reveal}", "response": self.get_question(), "points": 0}

        # التحقق من الإجابة الصحيحة
        if self.validate_answer(normalized):
            self.answered_users.add(user_id)
            total_points = 1
            if self.team_mode:
                team = self.get_user_team(user_id) or self.assign_to_team(user_id)
                self.add_team_score(team, total_points)
            else:
                self.add_score(user_id, display_name, total_points)

            self.previous_question = f"{self.current_category} - حرف {self.current_letter}"
            self.previous_answer = user_answer.strip()
            self.current_question += 1
            self.answered_users.clear()

            if self.current_question >= self.questions_count:
                winner_id, points = self.get_top_scorer()
                self.game_active = False
                return {
                    "response": TextMessage(text=f"انتهت اللعبة! الفائز: {winner_id} ({points} نقطة)"),
                    "points": total_points,
                    "game_over": True
                }

            return {"message": f"صحيح +{total_points}", "response": self.get_question(), "points": total_points}

        return None

    def build_question_flex(self, question_text: str, additional_info: str = None):
        """واجهة FlexMessage محسّنة مع دعم الثيم وأزرار لمّح / جاوب"""
        c = self.get_theme_colors()
        contents = [
            {"type": "text", "text": self.game_name, "size": "xxl", "weight": "bold", "color": c["primary"], "align": "center"},
            {"type": "text", "text": question_text, "size": "lg", "color": c["text"], "align": "center", "wrap": True, "margin": "md"}
        ]
        if additional_info:
            contents.append({"type": "text", "text": additional_info, "size": "sm", "color": c["info"], "align": "center", "margin": "md"})

        # أزرار لمّح / جاوب
        contents.append({"type": "box", "layout": "horizontal", "spacing": "sm", "margin": "lg", "contents": [
            {"type": "button", "action": {"type": "message", "label": "لمح", "text": "لمح"}, "style": "secondary", "height": "sm", "color": c["secondary"]},
            {"type": "button", "action": {"type": "message", "label": "جاوب", "text": "جاوب"}, "style": "secondary", "height": "sm", "color": c["secondary"]}
        ]})

        return FlexMessage(
            alt_text=f"{self.game_name} - جولة جديدة",
            contents=FlexContainer.from_dict({
                "type": "bubble",
                "body": {"type": "box", "layout": "vertical", "contents": contents, "paddingAll": "20px", "backgroundColor": c["bg"]}
            })
        )
