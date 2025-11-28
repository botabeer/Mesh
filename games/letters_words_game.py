"""
لعبة تكوين الكلمات - Bot Mesh v9.0 FINAL
Created by: Abeer Aldosari © 2025
✅ فردي: لمح (أول حرف + عدد) + جاوب + مؤقت
✅ فريقين: مؤقت فقط
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
            {"letters": ["ب","ي","ت","ك","م","ن"], "words": ["بيت","كتب","نبت","بنت","نكت"]}
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

        # ✅ النص الإضافي حسب الوضع
        if self.team_mode:
            additional_info = f"⏱️ {self.round_time} ثانية\nمطلوب {self.required_words} كلمات"
        else:
            additional_info = f"⏱️ {self.round_time} ثانية\nمطلوب {self.required_words} كلمات\n💡 اكتب 'لمح' أو 'جاوب'"

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

        # ✅ لمح وجاوب للفردي فقط
        if not self.team_mode:
            if normalized == "لمح":
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

            if normalized == "جاوب":
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
