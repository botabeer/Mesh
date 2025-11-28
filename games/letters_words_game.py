"""
لعبة تكوين الكلمات - النسخة النهائية المتكاملة
Created by: Abeer Aldosari © 2025
"""

from games.base_game import BaseGame
import random


class LettersWordsGame(BaseGame):
    """لعبة تكوين الكلمات"""

    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, questions_count=5)
        self.game_name = "تكوين"
        self.game_icon = ""

        # ✅ مجموعات الحروف الكاملة (مدمجة بدون حذف)
        self.letter_sets = [
            {"letters": ["ق","ل","م","ع","ر","ب"], "words": ["قلم","عمل","علم","قلب","رقم","عقل","قبل","بقر","قرب"]},
            {"letters": ["س","ا","ر","ة","ي","م"], "words": ["سيارة","سير","مسار","سارية","رأس","أسر","يسار","مارس"]},
            {"letters": ["ك","ت","ا","ب","م","ل"], "words": ["كتاب","كتب","مكتب","ملك","بكم","كلم","تلك","بلك"]},
            {"letters": ["د","ر","س","ة","م","ا"], "words": ["مدرسة","درس","مدرس","سدر","رسم","سرد","مسد"]},
            {"letters": ["ح","د","ي","ق","ة","ر"], "words": ["حديقة","حديد","قرد","دقيق","حرق","قدر","رحيق"]},
            {"letters": ["ب","ح","ر","ي","ة","س"], "words": ["بحيرة","بحر","سير","حرب","سحر","بحري"]},
            {"letters": ["ش","ج","ر","ة","م","ن"], "words": ["شجرة","شجر","نجم","رجم","شرج","نمر"]},
            {"letters": ["غ","ا","ب","ة","ر","ي"], "words": ["غابة","غراب","غرب","بغي","بير","ريب"]},
            {"letters": ["ن","خ","ل","ة","ي","م"], "words": ["نخلة","نخل","خلي","نمل","خيل","ملخ"]},
            {"letters": ["أ","س","د","ر","ن","ي"], "words": ["أسد","سرد","درس","سند","نرد","أسر"]},
            {"letters": ["ف","ي","ل","ط","ر","ن"], "words": ["فيل","طير","طفل","نفط","رفل","طرف"]},
            {"letters": ["ق","ط","ة","ر","ب","ي"], "words": ["قطة","قطر","بقر","طرب","رقبة","قرب"]},
            {"letters": ["ح","م","ا","م","ة","ل"], "words": ["حمامة","حمام","محل","حمل","ملح","حلم"]},
            {"letters": ["غ","ز","ا","ل","ر","ي"], "words": ["غزال","غزل","زرع","زال","لغز","رزق"]},
            {"letters": ["ت","م","ر","ي","ن","س"], "words": ["تمر","تمرين","ترس","سمر","نمر","رتم"]},
            {"letters": ["ل","ب","ن","ح","ة","ي"], "words": ["لبن","حلب","نبل","نحل","لحن"]},
            {"letters": ["خ","ب","ز","ر","ن","م"], "words": ["خبز","خزن","برز","زمن","نزر"]},
            {"letters": ["ع","س","ل","ج","ر","ن"], "words": ["عسل","جرس","عجل","رجل","سجل"]},
            {"letters": ["م","ا","ء","ي","ر","ن"], "words": ["ماء","مرء","نار","راء","أمر"]},
            {"letters": ["ب","ي","ت","ك","م","ن"], "words": ["بيت","كتب","نبت","بنت","نكت"]},
        ]

        random.shuffle(self.letter_sets)

        self.current_set = None
        self.found_words = set()
        self.required_words = 3

        # ✅ وضع الفرق
        self.team_mode = False
        self.team_players = set()

    # ==============================
    # بدء اللعبة
    # ==============================
    def start_game(self):
        self.current_question = 0
        self.game_active = True
        self.found_words.clear()
        self.previous_question = None
        self.previous_answer = None
        self.answered_users.clear()
        return self.get_question()

    # ==============================
    # إنشاء السؤال
    # ==============================
    def get_question(self):
        q_data = self.letter_sets[self.current_question % len(self.letter_sets)]
        self.current_set = q_data
        self.current_answer = q_data["words"]
        self.found_words.clear()

        colors = self.get_theme_colors()
        letters_display = " ▫️ ".join(q_data["letters"])

        flex_content = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": self.game_name, "align": "center", "weight": "bold"},
                    {"type": "separator"},
                    {"type": "text", "text": "كوّن كلمات من الحروف التالية:", "align": "center"},
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents":[{"type":"text","text":letters_display,"align":"center","weight":"bold"}],
                        "backgroundColor": colors["card"]
                    },
                    {"type": "text", "text": f"مطلوب {self.required_words} كلمات", "align": "center"},
                ]
            }
        }

        return self._create_flex_with_buttons(self.game_name, flex_content)

    # ==============================
    # فحص الإجابة
    # ==============================
    def check_answer(self, user_answer: str, user_id: str, display_name: str):

        if not self.game_active:
            return None

        normalized = self.normalize_text(user_answer)

        # ✅ تجاهل غير المنضمين في وضع الفريقين
        if self.team_mode and user_id not in self.team_players:
            return None

        # ✅ وضع الفريقين: لا يوجد لمح أو جاوب
        if self.team_mode and normalized in ["لمح","جاوب"]:
            return None

        # ==============================
        # الوضع الفردي فقط
        # ==============================
        if not self.team_mode:

            if normalized == "لمح":
                remaining = [w for w in self.current_answer if self.normalize_text(w) not in self.found_words]
                if remaining:
                    word = remaining[0]
                    hint = f"أول حرف: {word[0]}"
                else:
                    hint = "لا توجد تلميحات"
                return {"message": hint, "response": self._create_text_message(hint), "points": 0}

            if normalized == "جاوب":
                words = " ▪️ ".join(self.current_answer)
                msg = f"الكلمات الممكنة:\n{words}"
                self.current_question += 1
                self.answered_users.clear()
                self.found_words.clear()

                if self.current_question >= self.questions_count:
                    result = self.end_game()
                    result["message"] = f"{msg}\n\n{result.get('message','')}"
                    return result

                return {"message": msg, "response": self.get_question(), "points": 0}

        # ==============================
        # التحقق من صحة الإجابة
        # ==============================
        valid_words = [self.normalize_text(w) for w in self.current_answer]

        if normalized not in valid_words or normalized in self.found_words:
            return {"message":"إجابة غير صحيحة", "response": self._create_text_message("إجابة غير صحيحة"), "points":0}

        self.found_words.add(normalized)

        # ✅ احتساب النقاط فردي أو فريق
        points = self.add_score(user_id, display_name, 10)

        # ==============================
        # الانتقال للسؤال التالي
        # ==============================
        if len(self.found_words) >= self.required_words:

            self.current_question += 1
            self.answered_users.clear()
            self.found_words.clear()

            if self.current_question >= self.questions_count:
                result = self.end_game()
                result["points"] = points
                result["message"] = f"تم إنهاء الجولة\n{result.get('message','')}"
                return result

            return {"message": "تم الانتقال للجولة التالية", "response": self.get_question(), "points": points}

        remaining = self.required_words - len(self.found_words)
        return {"message": f"صحيح - تبقى {remaining} كلمات", "response": self._create_text_message("تم تسجيل الإجابة"), "points": points}
