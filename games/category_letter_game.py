import random
from games.base_game import BaseGame


class CategoryGame(BaseGame):
    def __init__(self, line_bot_api, theme='light'):
        super().__init__(line_bot_api, theme=theme)
        self.game_name = "فئه"
        self.questions_count = 5
        self.supports_hint = True
        self.supports_reveal = True

        self.challenges = [
            {"category": "المطبخ", "letter": "ق", "answers": ["قدر", "قلاية"]},
            {"category": "حيوان", "letter": "ب", "answers": ["بطة", "بقرة"]},
            {"category": "فاكهة", "letter": "ت", "answers": ["تفاح", "توت"]},
            {"category": "بلاد", "letter": "س", "answers": ["سعودية", "سوريا"]},
            {"category": "اسم ولد", "letter": "م", "answers": ["محمد", "مصطفى"]},
            {"category": "اسم بنت", "letter": "ف", "answers": ["فاطمة", "فرح"]},
            {"category": "نبات", "letter": "ز", "answers": ["زيتون", "زهرة"]},
            {"category": "جماد", "letter": "ك", "answers": ["كرسي", "كتاب"]},
            {"category": "مهنة", "letter": "ط", "answers": ["طبيب", "طباخ"]},
            {"category": "لون", "letter": "ا", "answers": ["احمر", "ازرق"]},
            {"category": "رياضة", "letter": "ك", "answers": ["كرة", "كاراتيه"]},
            {"category": "مدينة", "letter": "ج", "answers": ["جدة", "جازان"]},
            {"category": "طعام", "letter": "ر", "answers": ["رز", "رمان"]},
            {"category": "شراب", "letter": "ق", "answers": ["قهوة", "قمر الدين"]},
            {"category": "اثاث", "letter": "س", "answers": ["سرير", "سجادة"]},
            {"category": "ملابس", "letter": "ث", "answers": ["ثوب", "ثياب"]},
            {"category": "حشرة", "letter": "ن", "answers": ["نملة", "نحلة"]},
            {"category": "طائر", "letter": "ح", "answers": ["حمامة", "حسون"]},
            {"category": "زهرة", "letter": "و", "answers": ["ورد", "ورقة"]},
            {"category": "معدن", "letter": "ذ", "answers": ["ذهب", "ذرة"]},
            {"category": "سيارة", "letter": "م", "answers": ["مرسيدس", "مازدا"]},
            {"category": "عضو جسم", "letter": "ي", "answers": ["يد", "ياقة"]},
            {"category": "دولة", "letter": "ل", "answers": ["لبنان", "ليبيا"]},
            {"category": "حلوى", "letter": "ب", "answers": ["بسبوسة", "بقلاوة"]},
            {"category": "ادوات مدرسية", "letter": "د", "answers": ["دفتر", "دبوس"]},
            {"category": "وسيلة مواصلات", "letter": "ح", "answers": ["حافلة", "حمار"]},
            {"category": "شهر", "letter": "ر", "answers": ["رمضان", "رجب"]},
            {"category": "كوكب", "letter": "ز", "answers": ["زهرة", "زحل"]},
            {"category": "بحر", "letter": "ا", "answers": ["احمر", "اسود"]},
            {"category": "عاصمة", "letter": "ب", "answers": ["بغداد", "بيروت"]},
            {"category": "دواء", "letter": "ا", "answers": ["اسبرين", "انسولين"]},
            {"category": "جهاز منزلي", "letter": "غ", "answers": ["غسالة", "غلاية"]},
            {"category": "حلوى شعبية", "letter": "ك", "answers": ["كنافة", "كعك"]},
            {"category": "الة موسيقية", "letter": "ع", "answers": ["عود", "عصا"]},
            {"category": "مكان عبادة", "letter": "م", "answers": ["مسجد", "معبد"]}
        ]
        self.used_challenges = []

    def get_question(self):
        available = [c for c in self.challenges if c not in self.used_challenges]
        if not available:
            self.used_challenges = []
            available = self.challenges.copy()
            random.shuffle(available)

        challenge = random.choice(available)
        self.used_challenges.append(challenge)
        self.current_answer = challenge["answers"]

        return self.build_question_message(
            f"الفئة: {challenge['category']}\nالحرف: {challenge['letter']}",
            "اكتب اي كلمة مناسبة"
        )

    def check_answer(self, user_answer, user_id, display_name):
        if not self.game_active or user_id in self.answered_users:
            return None

        normalized = self.normalize_text(user_answer)

        if normalized == "ايقاف":
            return self.handle_withdrawal(user_id, display_name)

        if self.supports_hint and normalized == "لمح":
            sample = self.current_answer[0]
            return {"response": self.build_text_message(
                f"يبدا بحرف: {sample[0]}\nعدد الحروف: {len(sample)}"
            ), "points": 0}

        if self.supports_reveal and normalized == "جاوب":
            answers = " - ".join(self.current_answer)
            self.previous_answer = answers
            self.current_question += 1
            self.answered_users.clear()
            if self.current_question >= self.questions_count:
                return self.end_game()
            return {"response": self.get_question(), "points": 0, "next_question": True}

        valid_answers = [self.normalize_text(a) for a in self.current_answer]
        if normalized in valid_answers:
            return self.handle_correct_answer(user_id, display_name)

        return None
