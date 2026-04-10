import random
from games.base_game import BaseGame


class OppositeGame(BaseGame):
    def __init__(self, line_bot_api, difficulty=3, theme='light'):
        super().__init__(line_bot_api, difficulty=difficulty, theme=theme)
        self.game_name = "ضد"
        self.supports_hint = True
        self.supports_reveal = True

        self.opposites = {
            "كبير": ["صغير"], "طويل": ["قصير"], "سريع": ["بطيء"],
            "ساخن": ["بارد"], "نظيف": ["وسخ"], "جديد": ["قديم"],
            "صعب": ["سهل"], "قوي": ["ضعيف"], "غني": ["فقير"],
            "سعيد": ["حزين"], "جميل": ["قبيح"], "ثقيل": ["خفيف"],
            "عالي": ["منخفض"], "واسع": ["ضيق"], "طيب": ["خبيث"],
            "شجاع": ["جبان"], "ذكي": ["غبي"], "بعيد": ["قريب"],
            "فوق": ["تحت"], "يمين": ["يسار"], "اول": ["اخر"],
            "كثير": ["قليل"], "رطب": ["جاف"], "مبتسم": ["عابس"],
            "نشيط": ["كسول"], "صادق": ["كاذب"], "لين": ["قاسي"],
            "مضيء": ["مظلم"], "حلو": ["مر"], "ناعم": ["خشن"],
            "صحيح": ["خطا"], "داخل": ["خارج"], "مفتوح": ["مغلق"],
            "ممتلئ": ["فارغ"], "شتاء": ["صيف"], "ليل": ["نهار"],
            "شرق": ["غرب"], "شمال": ["جنوب"], "امن": ["خطر"],
            "سلام": ["حرب"], "فرح": ["حزن"], "حياة": ["موت"],
            "صحة": ["مرض"], "نور": ["ظلام"], "حق": ["باطل"],
            "خير": ["شر"], "ذكر": ["انثى"]
        }

        self.questions_list = list(self.opposites.items())
        random.shuffle(self.questions_list)
        self.used_indices = []

    def get_question(self):
        available = [i for i in range(len(self.questions_list)) if i not in self.used_indices]
        if not available:
            self.used_indices = []
            random.shuffle(self.questions_list)
            available = list(range(len(self.questions_list)))

        idx = random.choice(available)
        self.used_indices.append(idx)

        word, answers = self.questions_list[idx]
        self.current_answer = answers
        self.previous_question = f"ما عكس: {word}"

        return self.build_question_message(f"ما عكس كلمة:\n{word}")

    def check_answer(self, user_answer, user_id, display_name):
        if not self.game_active or user_id in self.answered_users:
            return None

        normalized = self.normalize_text(user_answer)

        if normalized == "ايقاف":
            return self.handle_withdrawal(user_id, display_name)

        if self.supports_hint and normalized == "لمح":
            hint_answer = self.current_answer[0]
            return {"response": self.build_text_message(
                f"يبدا ب: {hint_answer[0]}\nعدد الحروف: {len(hint_answer)}"
            ), "points": 0}

        if self.supports_reveal and normalized == "جاوب":
            return self.handle_reveal()

        for correct in self.current_answer:
            if self.normalize_text(correct) == normalized:
                return self.handle_correct_answer(user_id, display_name)

        return None
