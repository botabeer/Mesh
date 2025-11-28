"""
لعبة التخمين - Bot Mesh v7.3 Compatible
Created by: Abeer Aldosari © 2025
"""

from games.base_game import BaseGame
import random
from typing import Dict, Any, Optional, List


class GuessGame(BaseGame):
    """لعبة التخمين"""

    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, questions_count=5)
        self.game_name = "تخمين"
        self.game_icon = "🔮"
        self.supports_hint = True
        self.supports_reveal = True

        # قاعدة البيانات
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

        question_text = (
            f"الفئة: {q_data['category']}\n"
            f"يبدأ بحرف: {q_data['letter']}"
        )

        return self.build_question_flex(
            question_text=question_text,
            additional_info="اكتب 'لمح' للتلميح أو 'جاوب' للإجابة"
        )

    def check_answer(self, user_answer: str, user_id: str, display_name: str) -> Optional[Dict[str, Any]]:
        if not self.game_active or user_id in self.answered_users:
            return None

        normalized = self.normalize_text(user_answer)

        # التلميح
        if normalized == "لمح":
            hint = self.get_hint()
            return {
                "message": hint,
                "response": self._create_text_message(hint),
                "points": 0
            }

        # كشف الإجابة
        if normalized == "جاوب":
            answers_text = " أو ".join(self.current_answer)

            q_data = self.questions_list[self.current_question % len(self.questions_list)]
            self.previous_question = q_data
            self.previous_answer = answers_text

            self.current_question += 1
            self.answered_users.clear()

            if self.current_question >= self.questions_count:
                result = self.end_game()
                result["message"] = f"الإجابة: {answers_text}\n\n{result.get('message','')}"
                return result

            return {
                "message": f"الإجابة: {answers_text}",
                "response": self.get_question(),
                "points": 0
            }

        # التحقق من الإجابة
        for correct_answer in self.current_answer:
            if self.normalize_text(correct_answer) == normalized:
                points = self.add_score(user_id, display_name, 10)

                q_data = self.questions_list[self.current_question % len(self.questions_list)]
                self.previous_question = q_data
                self.previous_answer = correct_answer

                self.current_question += 1
                self.answered_users.clear()

                if self.current_question >= self.questions_count:
                    result = self.end_game()
                    result["points"] = points
                    result["message"] = (
                        f"إجابة صحيحة يا {display_name}\n"
                        f"الكلمة: {correct_answer}\n"
                        f"+{points} نقطة\n\n"
                        f"{result.get('message', '')}"
                    )
                    return result

                return {
                    "message": (
                        f"إجابة صحيحة يا {display_name}\n"
                        f"الكلمة: {correct_answer}\n"
                        f"+{points} نقطة"
                    ),
                    "response": self.get_question(),
                    "points": points
                }

        return {
            "message": "إجابة غير صحيحة، حاول مرة أخرى",
            "response": self._create_text_message("إجابة غير صحيحة، حاول مرة أخرى"),
            "points": 0
        }

    def get_game_info(self) -> Dict[str, Any]:
        return {
            "name": self.game_name,
            "description": "خمّن الكلمة من الفئة والحرف الأول",
            "questions_count": self.questions_count,
            "supports_hint": True,
            "supports_reveal": True,
            "active": self.game_active,
            "current_question": self.current_question,
            "players_count": len(self.scores),
            "categories_count": len(self.items)
        }
