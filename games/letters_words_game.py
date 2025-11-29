"""
لعبة تكوين الكلمات - Bot Mesh v9.1 FIXED
Created by: Abeer Aldosari © 2025
✅ فردي: لمح (أول حرف + عدد) + جاوب + مؤقت
✅ فريقين: مؤقت فقط (بدون لمح/جاوب)
✅ 3 كلمات لكل جولة
"""

from games.base_game import BaseGame
import random
import time
from typing import Dict, Any, Optional


class LettersWordsGame(BaseGame):
    """لعبة تكوين الكلمات"""

    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, questions_count=5)
        self.game_name = "تكوين"
        self.game_icon = "📝"
        self.supports_hint = True
        self.supports_reveal = True

        self.round_time = 40  # ⏱️ 40 ثانية للعثور على 3 كلمات
        self.round_start_time = None

        self.letter_sets = [
            {"letters": ["ق","ل","م","ع","ر","ب"], "words": ["قلم","عمل","علم","قلب","رقم","عقل","قبل","بقر","قرب","عرب","بعر"]},
            {"letters": ["س","ا","ر","ة","ي","م"], "words": ["سيارة","سير","مسار","سارية","رأس","أسر","يسار","مارس","سام","رمي"]},
            {"letters": ["ك","ت","ا","ب","م","ل"], "words": ["كتاب","كتب","مكتب","ملك","بكم","كلم","تلك","بلك","كمل","تمك"]},
            {"letters": ["د","ر","س","ة","م","ا"], "words": ["مدرسة","درس","مدرس","سدر","رسم","سرد","مسد","رمد","سمر"]},
            {"letters": ["ح","د","ي","ق","ة","ر"], "words": ["حديقة","حديد","قرد","دقيق","حرق","قدر","رحيق","حقد","دحر"]},
            {"letters": ["ب","ح","ر","ي","ة","س"], "words": ["بحيرة","بحر","سير","حرب","سحر","بحري","سبر","حبر"]},
            {"letters": ["ش","ج","ر","ة","م","ن"], "words": ["شجرة","شجر","نجم","رجم","شرج","نمر","جمر","نشر"]},
            {"letters": ["غ","ا","ب","ة","ر","ي"], "words": ["غابة","غراب","غرب","بغي","بير","ريب","غرا","بري"]},
            {"letters": ["ن","خ","ل","ة","ي","م"], "words": ["نخلة","نخل","خلي","نمل","خيل","ملخ","نيل","خمل"]},
            {"letters": ["أ","س","د","ر","ن","ي"], "words": ["أسد","سرد","درس","سند","نرد","أسر","دنس","سير"]},
            {"letters": ["ف","ي","ل","ط","ر","ن"], "words": ["فيل","طير","طفل","نفط","رفل","طرف","فرن","طين"]},
            {"letters": ["ق","ط","ة","ر","ب","ي"], "words": ["قطة","قطر","بقر","طرب","رقبة","قرب","طيب","قبر"]},
            {"letters": ["ح","م","ا","م","ة","ل"], "words": ["حمامة","حمام","محل","حمل","ملح","حلم","محم","أمل"]},
            {"letters": ["غ","ز","ا","ل","ر","ي"], "words": ["غزال","غزل","زرع","زال","لغز","رزق","زير","غلا"]},
            {"letters": ["ت","م","ر","ي","ن","س"], "words": ["تمر","تمرين","ترس","سمر","نمر","رتم","سنر","نير"]},
            {"letters": ["ل","ب","ن","ح","ة","ي"], "words": ["لبن","حلب","نبل","نحل","لحن","بني","حين"]},
            {"letters": ["خ","ب","ز","ر","ن","م"], "words": ["خبز","خزن","برز","زمن","نزر","زرن","خمر"]},
            {"letters": ["ع","س","ل","ج","ر","ن"], "words": ["عسل","جرس","عجل","رجل","سجل","عجن","سرج"]},
            {"letters": ["م","ا","ء","ي","ر","ن"], "words": ["ماء","مرء","نار","راء","أمر","مير","رين"]},
            {"letters": ["ب","ي","ت","ك","م","ن"], "words": ["بيت","كتب","نبت","بنت","نكت","كمن","بكم"]},
            {"letters": ["ص","ب","ا","ح","ر","ي"], "words": ["صباح","صحر","بحر","صبر","حار","حصر","بصر"]},
            {"letters": ["و","ر","د","ة","ج","ن"], "words": ["وردة","ورد","جنة","جرد","ندر","رجن","جند"]},
            {"letters": ["ط","ب","ي","ب","ح","ك"], "words": ["طبيب","طبخ","حبك","بيك","طيب","حكي"]},
            {"letters": ["م","ع","ل","م","ر","ا"], "words": ["معلم","علم","عمل","مرا","عمر","لمع"]},
            {"letters": ["ك","ر","ة","س","ل","ي"], "words": ["كرة","كرسي","سلة","كيس","سير","ركل"]},
            {"letters": ["ش","م","س","ع","ن","و"], "words": ["شمس","شمع","سمع","عنو","نعم","سنو"]},
            {"letters": ["ق","م","ر","ج","و","ل"], "words": ["قمر","جمر","رجل","جول","قول","مرج"]},
            {"letters": ["ب","ح","ر","ا","ط","ي"], "words": ["بحار","بحر","طير","حار","بري","حبر"]},
            {"letters": ["ج","ب","ل","س","ن","م"], "words": ["جبل","سجل","نجم","بسم","لبس","جمل"]},
            {"letters": ["ن","ه","ر","د","ي","ا"], "words": ["نهر","نهار","نار","دار","هدر","رند"]},
            {"letters": ["ص","خ","ر","ة","ب","ت"], "words": ["صخرة","صخر","خبر","رخت","بخت","تبر"]},
            {"letters": ["ر","م","ل","ي","ع","ا"], "words": ["رمل","رمي","عمل","ريع","لعي","مير"]},
            {"letters": ["و","ا","د","ي","ب","ح"], "words": ["وادي","واد","بحر","بدي","حدي","دوي"]},
            {"letters": ["س","م","ا","ء","ر","ز"], "words": ["سماء","سما","رزق","مزر","زرا","سرا"]},
            {"letters": ["أ","ر","ض","ي","ع","ن"], "words": ["أرض","عرض","رين","عين","رضي","نير"]},
            {"letters": ["ت","ل","ف","ز","ا","ي"], "words": ["تلفاز","تلف","فلت","زال","لفت","فيل"]},
            {"letters": ["ه","ا","ت","ف","ر","ن"], "words": ["هاتف","هتف","تفه","رفت","نفر","فتن"]},
            {"letters": ["ح","ا","س","و","ب","ر"], "words": ["حاسوب","حسب","سوب","سحر","حرب","سبر"]},
            {"letters": ["م","ف","ت","ا","ح","ق"], "words": ["مفتاح","مفت","حفت","قفت","متح","حقف"]},
            {"letters": ["س","ا","ع","ة","ر","ي"], "words": ["ساعة","سعر","عرا","رعي","سير","عسر"]},
            {"letters": ["ص","و","ر","ة","ج","م"], "words": ["صورة","صور","رجم","جمر","وجر","مرج"]},
            {"letters": ["م","ر","آ","ة","ن","ك"], "words": ["مرآة","مرا","نمر","كرم","نكر","أمر"]},
            {"letters": ["ف","ر","ش","ا","ة","ت"], "words": ["فرشاة","فرش","رشا","شرف","فتر","شتر"]},
            {"letters": ["ص","ا","ب","و","ن","ح"], "words": ["صابون","صاب","بحن","نصب","حصن","بصن"]},
            {"letters": ["م","ن","د","ي","ل","ش"], "words": ["منديل","مند","دين","نيل","شمل","ليد"]},
            {"letters": ["ق","ل","ا","د","ة","ج"], "words": ["قلادة","قلد","جدل","دقة","لجة","جلد"]},
            {"letters": ["خ","ا","ت","م","ر","ن"], "words": ["خاتم","خمر","تمر","نتر","رخم","متن"]},
            {"letters": ["س","و","ا","ر","ح","ك"], "words": ["سوار","سور","حرك","سحر","كرا","رسو"]},
            {"letters": ["ح","ق","ي","ب","ة","ج"], "words": ["حقيبة","حقب","جبة","بيج","حبق","قبح"]},
            {"letters": ["م","ح","ف","ظ","ة","ر"], "words": ["محفظة","محف","فظر","حفر","ظفر","رمح"]}
        ]

        random.shuffle(self.letter_sets)
        self.current_set = None
        self.found_words = set()
        self.required_words = 3

    def start_game(self):
        self.current_question = 0
        self.game_active = True
        self.previous_question = None
        self.previous_answer = None
        self.answered_users.clear()
        self.found_words.clear()
        return self.get_question()

    def get_question(self):
        q_data = self.letter_sets[self.current_question % len(self.letter_sets)]
        self.current_set = q_data
        self.current_answer = q_data["words"]
        self.found_words.clear()
        self.round_start_time = time.time()

        letters_display = " • ".join(q_data["letters"])

        # ✅ استخدام can_use_hint() و can_reveal_answer()
        if self.can_use_hint() and self.can_reveal_answer():
            additional_info = f"⏱️ {self.round_time} ثانية\nمطلوب {self.required_words} كلمات\n💡 اكتب 'لمح' أو 'جاوب'"
        else:
            additional_info = f"⏱️ {self.round_time} ثانية\nمطلوب {self.required_words} كلمات"

        return self.build_question_flex(
            question_text=f"كوّن كلمات من:\n{letters_display}",
            additional_info=additional_info
        )

    def _time_expired(self) -> bool:
        if not self.round_start_time:
            return False
        return (time.time() - self.round_start_time) > self.round_time

    def check_answer(self, user_answer: str, user_id: str, display_name: str) -> Optional[Dict[str, Any]]:
        if not self.game_active:
            return None

        # التحقق من الوقت
        if self._time_expired():
            words = " • ".join(self.current_answer[:5])
            self.current_question += 1
            self.answered_users.clear()
            self.found_words.clear()

            if self.current_question >= self.questions_count:
                result = self.end_game()
                result["message"] = f"⏱️ انتهى الوقت!\nكلمات ممكنة: {words}\n\n{result.get('message', '')}"
                return result

            return {
                "message": f"⏱️ انتهى الوقت!\nكلمات ممكنة: {words}",
                "response": self.get_question(),
                "points": 0
            }

        if self.team_mode and user_id not in self.joined_users:
            return None

        normalized = self.normalize_text(user_answer)

        # ✅ التلميح (فردي فقط)
        if self.can_use_hint() and normalized == "لمح":
            remaining = [w for w in self.current_answer if self.normalize_text(w) not in self.found_words]
            if remaining:
                word = remaining[0]
                hint = f"💡 تبدأ بـ: {word[0]}\nعدد الحروف: {len(word)}"
            else:
                hint = "لا توجد تلميحات"
            return {
                "message": hint,
                "response": self._create_text_message(hint),
                "points": 0
            }

        # ✅ كشف الإجابة (فردي فقط)
        if self.can_reveal_answer() and normalized == "جاوب":
            words = " • ".join(self.current_answer[:5])
            msg = f"كلمات ممكنة:\n{words}"
            self.current_question += 1
            self.answered_users.clear()
            self.found_words.clear()

            if self.current_question >= self.questions_count:
                result = self.end_game()
                result["message"] = f"{msg}\n\n{result.get('message', '')}"
                return result

            return {
                "message": msg,
                "response": self.get_question(),
                "points": 0
            }

        # ✅ تجاهل لمح/جاوب في وضع الفريقين بشكل صامت
        if self.team_mode and normalized in ["لمح", "جاوب"]:
            return None

        # التحقق من صحة الإجابة
        valid_words = [self.normalize_text(w) for w in self.current_answer]

        if normalized not in valid_words or normalized in self.found_words:
            return {
                "message": "❌ خطأ أو مكررة",
                "response": self._create_text_message("❌ خطأ أو مكررة"),
                "points": 0
            }

        self.found_words.add(normalized)
        points = 10

        if self.team_mode:
            team = self.get_user_team(user_id)
            if not team:
                team = self.assign_to_team(user_id)
            self.add_team_score(team, points)
        else:
            self.add_score(user_id, display_name, points)

        # الانتقال للسؤال التالي
        if len(self.found_words) >= self.required_words:
            self.current_question += 1
            self.answered_users.clear()
            self.found_words.clear()

            if self.current_question >= self.questions_count:
                result = self.end_game()
                result["points"] = points
                return result

            return {
                "message": f"✅ تم! انتقال للجولة التالية",
                "response": self.get_question(),
                "points": points
            }

        remaining = self.required_words - len(self.found_words)
        return {
            "message": f"✅ صحيح! تبقى {remaining} كلمة",
            "response": self._create_text_message(f"✅ صحيح! تبقى {remaining} كلمة"),
            "points": points
        }
