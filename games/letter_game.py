import random
from games.base_game import BaseGame


class LetterGame(BaseGame):
    def __init__(self, line_bot_api, difficulty=3, theme="light"):
        super().__init__(line_bot_api, difficulty=difficulty, theme=theme)
        self.game_name = "حرف"
        self.supports_hint = True
        self.supports_reveal = True

        self.questions_db = {
            "ا": [
                {"q": "من هو اول نبي", "a": ["ادم", "آدم"]},
                {"q": "ما اطول نهر في افريقيا", "a": ["النيل"]},
                {"q": "ما هو العضو المسؤول عن ضخ الدم", "a": ["القلب"]},
                {"q": "ما اسم الكوكب الاحمر", "a": ["المريخ"]},
            ],
            "ب": [
                {"q": "ما هي عاصمة العراق", "a": ["بغداد"]},
                {"q": "ما هي عاصمة الصين", "a": ["بكين"]},
                {"q": "ما هي عاصمة البحرين", "a": ["المنامة"]},
            ],
            "ت": [
                {"q": "ما هي عاصمة تونس", "a": ["تونس"]},
                {"q": "ما هي عاصمة تركيا", "a": ["انقرة"]},
                {"q": "ما اسم الطائر الذي لا يطير", "a": ["النعامة"]},
            ],
            "ج": [
                {"q": "ما هي عاصمة اليابان", "a": ["طوكيو"]},
                {"q": "ما الحيوان المعروف بسفينة الصحراء", "a": ["الجمل"]},
                {"q": "ما اسم اكبر محيط في العالم", "a": ["المحيط الهادئ", "الهادئ"]},
            ],
            "ح": [
                {"q": "ما المدينة السورية المشهورة بقلعتها", "a": ["حلب"]},
                {"q": "ما الحيوان المعروف ببطئه", "a": ["السلحفاة"]},
                {"q": "كم عدد حواس الانسان", "a": ["5", "خمسة"]},
            ],
            "د": [
                {"q": "ما هي عاصمة سوريا", "a": ["دمشق"]},
                {"q": "ما الحيوان المفترس الذي يعيش في البحر", "a": ["القرش"]},
                {"q": "ما اسم العاصمة السورية", "a": ["دمشق"]},
            ],
            "ر": [
                {"q": "ما هي عاصمة السعودية", "a": ["الرياض"]},
                {"q": "ما الشهر المبارك للمسلمين", "a": ["رمضان"]},
                {"q": "ما اسم اطول نهر في اوروبا", "a": ["الفولغا"]},
            ],
            "س": [
                {"q": "ما هي عاصمة السويد", "a": ["ستوكهولم"]},
                {"q": "ما الحيوان الزاحف ذو الصدفة", "a": ["السلحفاة"]},
                {"q": "من الصحابي الذي اشار بحفر الخندق", "a": ["سلمان الفارسي", "سلمان"]},
            ],
            "ش": [
                {"q": "ما المشروب الساخن المشهور", "a": ["الشاي"]},
                {"q": "ما الفصل البارد من السنة", "a": ["الشتاء"]},
                {"q": "ما اسم اللعبة المشهورة ذات المربعات", "a": ["الشطرنج"]},
            ],
            "ص": [
                {"q": "ما الطائر الجارح المشهور", "a": ["الصقر"]},
                {"q": "ما هي عاصمة اليمن", "a": ["صنعاء"]},
                {"q": "كم عدد الصلوات المفروضة", "a": ["5", "خمسة"]},
            ],
            "ط": [
                {"q": "ما الطائر ذو الالوان الجميلة", "a": ["الطاووس"]},
                {"q": "ما اسم العاصمة اليابانية", "a": ["طوكيو"]},
                {"q": "ما الخضار الحمراء المستديرة", "a": ["الطماطم"]},
            ],
            "ع": [
                {"q": "ما هي عاصمة الاردن", "a": ["عمان"]},
                {"q": "ما الحيوان الصحراوي ذو السنام", "a": ["الجمل"]},
                {"q": "ما اكبر عضو في جسم الانسان", "a": ["الجلد"]},
            ],
            "ف": [
                {"q": "ما الفاكهة الحمراء الصيفية", "a": ["الفراولة"]},
                {"q": "ما الحيوان المفترس السريع", "a": ["الفهد"]},
                {"q": "ما هي عاصمة فرنسا", "a": ["باريس"]},
            ],
            "ق": [
                {"q": "ما هي عاصمة مصر", "a": ["القاهرة"]},
                {"q": "ما المشروب الساخن المر", "a": ["القهوة"]},
                {"q": "ما العضو الذي يضخ الدم", "a": ["القلب"]},
            ],
            "ك": [
                {"q": "ما اسم الوعاء الذي نشرب فيه", "a": ["الكوب"]},
                {"q": "ما الاثاث الذي نجلس عليه", "a": ["الكرسي"]},
                {"q": "كم عدد الكواكب في المجموعة الشمسية", "a": ["8", "ثمانية"]},
            ],
            "ل": [
                {"q": "ما هي عاصمة لبنان", "a": ["بيروت"]},
                {"q": "ما الفاكهة الصفراء الحامضة", "a": ["الليمون"]},
                {"q": "ما العضو الذي نتذوق به", "a": ["اللسان"]},
            ],
            "م": [
                {"q": "ما العضو المسؤول عن التفكير", "a": ["المخ", "الدماغ"]},
                {"q": "ما اسم عاصمة المغرب", "a": ["الرباط"]},
                {"q": "ما هي عاصمة الامارات", "a": ["ابوظبي", "ابو ظبي"]},
            ],
            "ن": [
                {"q": "ما اكبر نهر في العالم", "a": ["النيل"]},
                {"q": "ما الطائر رمز الحرية", "a": ["النسر"]},
                {"q": "ما الحيوان رمز القوة", "a": ["النمر"]},
            ],
            "ه": [
                {"q": "ما الجهاز الذي نتكلم به", "a": ["الهاتف"]},
                {"q": "ما الشيء الذي نتنفسه", "a": ["الهواء"]},
                {"q": "ما اسم اكبر محيط في العالم", "a": ["الهادئ"]},
            ],
            "و": [
                {"q": "ما الزهرة الجميلة الملونة", "a": ["الوردة"]},
                {"q": "ما الطائر الابيض الجميل", "a": ["الحمامة"]},
            ],
            "ي": [
                {"q": "ما العضو الذي نمسك به الاشياء", "a": ["اليد"]},
                {"q": "ما اسم اول يوم في الاسبوع", "a": ["الاحد"]},
                {"q": "ما البلد المشهور بالساموراي", "a": ["اليابان"]},
            ]
        }

        self.letters = list(self.questions_db.keys())
        random.shuffle(self.letters)
        # إصلاح: dict بدل set لتتبع الأسئلة لكل حرف
        self.used_per_letter = {letter: [] for letter in self.letters}
        self.current_letter = None

    def get_question(self):
        if self.current_question >= self.questions_count:
            return self.end_game()

        self.current_letter = self.letters[self.current_question % len(self.letters)]
        questions = self.questions_db[self.current_letter]
        used = self.used_per_letter[self.current_letter]

        available = [i for i in range(len(questions)) if i not in used]
        if not available:
            self.used_per_letter[self.current_letter] = []
            available = list(range(len(questions)))

        idx = random.choice(available)
        self.used_per_letter[self.current_letter].append(idx)

        q_data = questions[idx]
        self.current_answer = q_data["a"]

        return self.build_question_message(
            f"حرف: {self.current_letter}\n\n{q_data['q']}",
            f"الاجابة تبدا بحرف {self.current_letter}"
        )

    def check_answer(self, user_answer, user_id, display_name):
        if not self.game_active or user_id in self.answered_users:
            return None

        normalized = self.normalize_text(user_answer)

        if normalized == "ايقاف":
            return self.handle_withdrawal(user_id, display_name)

        if self.supports_hint and normalized == "لمح":
            ans = self.current_answer[0]
            return {"response": self.build_text_message(
                f"يبدا بحرف: {ans[0]}\nعدد الحروف: {len(ans)}"
            ), "points": 0}

        if self.supports_reveal and normalized == "جاوب":
            return self.handle_reveal()

        for correct in self.current_answer:
            if normalized == self.normalize_text(correct):
                return self.handle_correct_answer(user_id, display_name)

        return None
