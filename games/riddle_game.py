import random
from games.base_game import BaseGame


class RiddleGame(BaseGame):
    def __init__(self, line_bot_api, difficulty=3, theme='light'):
        super().__init__(line_bot_api, difficulty=difficulty, theme=theme)
        self.game_name = "لغز"
        self.supports_hint = True
        self.supports_reveal = True

        self.riddles = [
            {"q": "ما الشيء الذي يمشي بلا ارجل ويبكي بلا عيون", "a": ["السحاب", "الغيم"]},
            {"q": "له راس ولكن لا عين له", "a": ["الدبوس", "المسمار"]},
            {"q": "شيء كلما زاد نقص", "a": ["العمر"]},
            {"q": "يكتب ولا يقرا ابدا", "a": ["القلم"]},
            {"q": "له اسنان كثيرة ولكنه لا يعض", "a": ["المشط"]},
            {"q": "يوجد في الماء ولكن الماء يميته", "a": ["الملح"]},
            {"q": "يتكلم بجميع اللغات دون ان يتعلمها", "a": ["الصدى"]},
            {"q": "شيء كلما اخذت منه كبر", "a": ["الحفرة"]},
            {"q": "يخترق الزجاج ولا يكسره", "a": ["الضوء"]},
            {"q": "يسمع بلا اذن ويتكلم بلا لسان", "a": ["الهاتف"]},
            {"q": "له عين ولا يرى", "a": ["الابرة"]},
            {"q": "يجري ولا يمشي", "a": ["الماء", "النهر"]},
            {"q": "ما الذي يحدث مرة في الدقيقة ومرتين في اللحظة", "a": ["القاف"]},
            {"q": "ترى كل شيء وليس لها عيون", "a": ["المراة"]},
            {"q": "له اربع ارجل ولا يستطيع المشي", "a": ["الطاولة", "الكرسي"]},
            {"q": "اذا اكلته كله تستفيد واذا اكلت نصفه تموت", "a": ["السمسم"]},
            {"q": "من هو الخال الوحيد لاولاد عمتك", "a": ["ابي", "والدي"]},
            {"q": "يسير بلا رجلين ولا يدخل الا بالاذنين", "a": ["الصوت"]},
            {"q": "شيء اذا غليته جمد", "a": ["البيض"]},
            {"q": "شيء له رقبة وليس له راس", "a": ["الزجاجة"]},
            {"q": "ما هو الذي يكون اخضر في الارض واسود في السوق واحمر في البيت", "a": ["الشاي"]},
            {"q": "شيء تملكه ولكن غيرك يستخدمه اكثر منك", "a": ["الاسم"]},
            {"q": "انا ابن الماء فإن تركوني في الماء مت", "a": ["الثلج"]},
            {"q": "يمشي ويقف وليس له ارجل", "a": ["الساعة"]},
            {"q": "كلي ثقوب ومع ذلك احفظ الماء", "a": ["الاسفنج"]},
            {"q": "ابن امك وابن ابيك وليس باختك ولا باخيك", "a": ["انت"]},
            {"q": "ما هو اطول نهر في العالم", "a": ["النيل"]},
            {"q": "ما هو الحيوان الملقب بسفينة الصحراء", "a": ["الجمل"]},
            {"q": "كم عدد الوان قوس قزح", "a": ["7", "سبعة"]},
            {"q": "ما هو اكبر كوكب في المجموعة الشمسية", "a": ["المشتري"]},
            {"q": "ما هي اصغر دولة في العالم", "a": ["الفاتيكان"]},
            {"q": "ما هو اسرع حيوان بري", "a": ["الفهد"]},
            {"q": "ما هي عاصمة فرنسا", "a": ["باريس"]},
            {"q": "ما هي اصغر قارة في العالم", "a": ["استراليا"]},
            {"q": "من اول من صعد الى القمر", "a": ["نيل ارمسترونج", "ارمسترونج"]},
            {"q": "كم عدد اجنحة النحلة", "a": ["4", "اربعة"]},
            {"q": "ما هو لون دم الاخطبوط", "a": ["ازرق"]},
            {"q": "كم عدد حروف اللغة العربية", "a": ["28", "ثمانية وعشرون"]},
            {"q": "ما هي عاصمة مصر", "a": ["القاهرة"]},
            {"q": "ما هي عاصمة السعودية", "a": ["الرياض"]}
        ]

        random.shuffle(self.riddles)
        self.used_riddles = []

    def get_question(self):
        available = [r for r in self.riddles if r not in self.used_riddles]
        if not available:
            self.used_riddles = []
            available = self.riddles.copy()
            random.shuffle(available)

        riddle = random.choice(available)
        self.used_riddles.append(riddle)
        self.current_answer = riddle["a"]
        self.previous_question = riddle["q"]

        return self.build_question_message(riddle["q"])

    def check_answer(self, user_answer, user_id, display_name):
        if not self.game_active or user_id in self.answered_users:
            return None

        normalized = self.normalize_text(user_answer)

        if normalized == "ايقاف":
            return self.handle_withdrawal(user_id, display_name)

        if self.supports_hint and normalized == "لمح":
            answer = self.current_answer[0]
            return {"response": self.build_text_message(
                f"يبدأ بحرف: {answer[0]}\nعدد الحروف: {len(answer)}"
            ), "points": 0}

        if self.supports_reveal and normalized == "جاوب":
            return self.handle_reveal()

        for correct in self.current_answer:
            if self.normalize_text(correct) == normalized:
                return self.handle_correct_answer(user_id, display_name)

        return None
