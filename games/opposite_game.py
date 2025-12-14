from games.base_game import BaseGame
import random
from typing import Dict, Any, Optional

class OppositeGame(BaseGame):
    """لعبة ضد محسّنة"""

    def __init__(self, line_bot_api=None):
        super().__init__(line_bot_api, questions_count=5)
        self.game_name = "ضد"
        self.supports_hint = True
        self.supports_reveal = True

        self.opposites = {
            "كبير": ["صغير", "قصير"],
            "طويل": ["قصير"],
            "سريع": ["بطيء"],
            "ساخن": ["بارد", "مثلج"],
            "نظيف": ["وسخ", "قذر"],
            "جديد": ["قديم"],
            "صعب": ["سهل", "بسيط"],
            "قوي": ["ضعيف"],
            "غني": ["فقير"],
            "سعيد": ["حزين"],
            "جميل": ["قبيح"],
            "ثقيل": ["خفيف"],
            "عالي": ["منخفض"],
            "واسع": ["ضيق"],
            "قريب": ["بعيد"],
            "مفتوح": ["مغلق"],
            "نهار": ["ليل"],
            "شمس": ["قمر"],
            "شتاء": ["صيف"],
            "شرق": ["غرب"],
            "أبيض": ["أسود"],
            "حلو": ["مر", "حامض"],
            "حار": ["بارد"],
            "صحيح": ["خطأ", "خاطئ"],
            "حي": ["ميت"],
            "نور": ["ظلام"],
            "فوق": ["تحت"],
            "يمين": ["يسار"],
            "أمام": ["خلف"],
            "داخل": ["خارج"],
            "صباح": ["مساء"],
            "كثير": ["قليل"],
            "عميق": ["سطحي"],
            "ممتلئ": ["فارغ"],
            "ناعم": ["خشن"],
            "واضح": ["غامض"],
            "نشيط": ["كسول"],
            "صامت": ["صاخب"],
            "رخيص": ["غالي"]
        }

        self.questions_list = list(self.opposites.keys())
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
        word = self.questions_list[self.current_question % len(self.questions_list)]
        self.current_answer = self.opposites.get(word, [])
        return self.build_question_flex(
            question_text=f"ما هو عكس:\n\n{word}",
            additional_info=None
        )

    def check_answer(self, user_answer: str, user_id: str, display_name: str) -> Optional[Dict[str, Any]]:
        if not self.game_active or user_id in self.answered_users:
            return None

        normalized = self.normalize_text(user_answer.strip())

        # أمر لمّح
        if self.can_use_hint() and normalized == "لمح":
            if self.current_answer:
                hint = f"تبدأ بـ {self.current_answer[0][0]}\nعدد الحروف: {len(self.current_answer[0])}"
            else:
                hint = "فكر جيداً، أي إجابة مقبولة"
            return {"message": hint, "points": 0}

        # أمر جاوب
        if self.can_reveal_answer() and normalized == "جاوب":
            answers_text = " أو ".join(self.current_answer) if self.current_answer else "أي إجابة صحيحة مقبولة"
            word = self.questions_list[self.current_question % len(self.questions_list)]
            self.previous_question = f"عكس {word}"
            self.previous_answer = answers_text
            self.current_question += 1
            self.answered_users.clear()
            if self.current_question >= self.questions_count:
                result = self.end_game()
                result["message"] = f"الإجابة: {answers_text}\n\nانتهت اللعبة"
                return result
            return {"message": f"الإجابة: {answers_text}", "response": self.get_question(), "points": 0}

        # قبول أي إجابة كإجابة صحيحة
        self.answered_users.add(user_id)
        points = 1
        self.add_score(user_id, display_name, points)

        word = self.questions_list[self.current_question % len(self.questions_list)]
        self.previous_question = f"عكس {word}"
        self.previous_answer = normalized
        self.current_question += 1
        self.answered_users.clear()

        if self.current_question >= self.questions_count:
            result = self.end_game()
            result["points"] = points
            return result

        return {"message": f"صحيح +{points}", "response": self.get_question(), "points": points}
