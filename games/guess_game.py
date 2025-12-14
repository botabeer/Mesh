from games.base_game import BaseGame
import random
from typing import Dict, Any, Optional
from linebot.v3.messaging import FlexMessage, FlexContainer, TextMessage

class GuessGame(BaseGame):
    """لعبة خمن محسّنة: 5 جولات، دعم الثيم، أمر لمّح وجاوب"""

    def __init__(self, line_bot_api=None):
        super().__init__(line_bot_api, questions_count=5)
        self.game_name = "خمن"
        self.supports_hint = True
        self.supports_reveal = True

        self.items = {
            "المطبخ": {"ق": ["قدر", "قلاية", "قارورة"], "م": ["ملعقة", "مغرفة", "مقلاة"]},
            "غرفة النوم": {"س": ["سرير", "ستارة"], "م": ["مرآة", "مخدة", "مصباح"]},
            "المدرسة": {"ق": ["قلم", "قرطاسية"], "ك": ["كتاب", "كراسة"]},
            "الفواكه": {"ت": ["تفاح", "تمر", "توت"], "م": ["موز", "مشمش"]},
            "الحيوانات": {"ق": ["قطة", "قرد"], "ف": ["فيل", "فهد"]}
        }

        self.questions_list = []
        for category, letters in self.items.items():
            for letter, words in letters.items():
                self.questions_list.append({
                    "category": category,
                    "letter": letter,
                    "answers": words
                })
        random.shuffle(self.questions_list)

    def start_game(self):
        self.current_question = 0
        self.game_active = True
        self.previous_question = None
        self.previous_answer = None
        self.answered_users.clear()
        self.scores.clear()
        return self.get_question()

    def get_question(self):
        q_data = self.questions_list[self.current_question % len(self.questions_list)]
        self.current_answer = q_data["answers"]
        return self.build_question_flex(
            question_text=f"الفئة: {q_data['category']}\nيبدأ بحرف: {q_data['letter']}",
            additional_info=f"السؤال {self.current_question+1}/{self.questions_count}"
        )

    def check_answer(self, user_answer: str, user_id: str, display_name: str) -> Optional[Dict[str, Any]]:
        if not self.game_active or user_id in self.answered_users:
            return None

        normalized = self.normalize_text(user_answer)

        # أمر لمّح
        if self.can_use_hint() and normalized == "لمح":
            first_answer = self.current_answer[0]
            hint = f"تبدأ بـ {first_answer[0]} | عدد الحروف: {len(first_answer)}"
            return {"message": hint, "points": 0}

        # أمر جاوب
        if self.can_reveal_answer() and normalized == "جاوب":
            answers_text = " او ".join(self.current_answer)
            q_data = self.questions_list[self.current_question % len(self.questions_list)]
            self.previous_question = f"{q_data['category']} - حرف {q_data['letter']}"
            self.previous_answer = answers_text
            self.current_question += 1
            self.answered_users.clear()

            if self.current_question >= self.questions_count:
                result = self.end_game()
                result["message"] = f"الإجابة: {answers_text}\n\nانتهت اللعبة"
                return result

            return {"message": f"الإجابة: {answers_text}", "response": self.get_question(), "points": 0}

        # التحقق من الإجابة الصحيحة
        for correct_answer in self.current_answer:
            if self.normalize_text(correct_answer) == normalized:
                self.add_score(user_id, display_name, 1)

                q_data = self.questions_list[self.current_question % len(self.questions_list)]
                self.previous_question = f"{q_data['category']} - حرف {q_data['letter']}"
                self.previous_answer = correct_answer
                self.current_question += 1
                self.answered_users.clear()

                if self.current_question >= self.questions_count:
                    winner_id, points = self.get_top_scorer()
                    self.game_active = False
                    return {
                        "response": TextMessage(text=f"انتهت اللعبة! الفائز: {winner_id} ({points} نقطة)"),
                        "points": 1,
                        "game_over": True
                    }

                return {"message": "صحيح +1", "response": self.get_question(), "points": 1}

        return None

    def build_question_flex(self, question_text: str, additional_info: str = None):
        """واجهة FlexMessage محسّنة مع دعم الثيم"""
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
