"""
لعبة إنسان حيوان نبات - Bot Mesh v9.0 FINAL
Created by: Abeer Aldosari © 2025
✅ فردي: لمح (أول حرف + عدد) + جاوب + مؤقت
✅ فريقين: مؤقت فقط
"""

from games.base_game import BaseGame
import random
import time
from typing import Dict, Any, Optional


class HumanAnimalPlantGame(BaseGame):
    """لعبة إنسان حيوان نبات"""

    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, questions_count=5)
        self.game_name = "إنسان حيوان نبات"
        self.game_icon = "🌿"
        self.supports_hint = True
        self.supports_reveal = True

        self.round_time = 25  # ⏱️ 25 ثانية
        self.round_start_time = None

        self.letters = list("ابتجحدرزسشصطعفقكلمنهوي")
        random.shuffle(self.letters)
        self.categories = ["إنسان", "حيوان", "نبات", "جماد", "بلاد"]

        self.database = {
            "إنسان": {
                "م": ["محمد", "مريم", "مصطفى", "منى"],
                "أ": ["أحمد", "أمل", "أمير", "أميرة"],
                "ع": ["علي", "عمر", "عائشة", "عبير"],
                "ف": ["فاطمة", "فهد", "فيصل"],
                "س": ["سارة", "سعيد", "سلمان"],
                "ر": ["رامي", "رنا", "رشيد"],
                "ن": ["نورة", "نايف", "نادر"],
                "ه": ["هند", "هاني", "هيثم"],
                "ي": ["يوسف", "ياسمين", "يزيد"]
            },
            "حيوان": {
                "أ": ["أسد", "أرنب", "أفعى"],
                "ج": ["جمل", "جاموس"],
                "ح": ["حصان", "حمار"],
                "خ": ["خروف"],
                "د": ["دجاجة", "ديك"],
                "ذ": ["ذئب"],
                "ز": ["زرافة"],
                "س": ["سمكة", "سلحفاة"],
                "ص": ["صقر"],
                "ط": ["طاووس"],
                "ع": ["عصفور"],
                "غ": ["غزال", "غراب"],
                "ف": ["فيل", "فهد"],
                "ق": ["قرد", "قطة"],
                "ك": ["كلب"],
                "ن": ["نمر", "نعامة"],
                "و": ["وزة"]
            },
            "نبات": {
                "ت": ["تفاح", "تمر", "توت"],
                "ب": ["بطيخ", "برتقال", "بطاطس"],
                "ر": ["رمان", "ريحان"],
                "ز": ["زيتون", "زعتر"],
                "ع": ["عنب"],
                "ف": ["فراولة", "فجل"],
                "ك": ["كرز", "كمثرى"],
                "م": ["موز", "مشمش"],
                "ن": ["نعناع"],
                "و": ["ورد"]
            },
            "جماد": {
                "ب": ["باب", "بيت"],
                "ت": ["تلفاز", "تلفون"],
                "ج": ["جدار"],
                "ح": ["حائط"],
                "س": ["سيارة", "ساعة"],
                "ش": ["شباك"],
                "ط": ["طاولة"],
                "ق": ["قلم"],
                "ك": ["كرسي", "كتاب"],
                "م": ["مفتاح", "مكتب"],
                "ن": ["نافذة"]
            },
            "بلاد": {
                "أ": ["أمريكا", "ألمانيا"],
                "ب": ["بريطانيا"],
                "ت": ["تركيا", "تونس"],
                "ج": ["الجزائر"],
                "س": ["السعودية", "سوريا"],
                "ع": ["عمان"],
                "ف": ["فرنسا"],
                "ق": ["قطر"],
                "ك": ["الكويت"],
                "ل": ["لبنان", "ليبيا"],
                "م": ["مصر", "المغرب"],
                "ي": ["اليمن", "اليابان"]
            }
        }

        self.current_category = None
        self.current_letter = None

    def start_game(self):
        self.current_question = 0
        self.game_active = True
        self.previous_question = None
        self.previous_answer = None
        self.answered_users.clear()
        return self.get_question()

    def get_question(self):
        self.current_letter = self.letters[self.current_question % len(self.letters)]
        self.current_category = random.choice(self.categories)
        self.round_start_time = time.time()

        # ✅ النص الإضافي حسب الوضع
        if self.team_mode:
            additional_info = f"⏱️ {self.round_time} ثانية"
        else:
            additional_info = f"⏱️ {self.round_time} ثانية\n💡 اكتب 'لمح' أو 'جاوب'"

        return self.build_question_flex(
            question_text=f"الفئة: {self.current_category}\nالحرف: {self.current_letter}",
            additional_info=additional_info
        )

    def _time_expired(self) -> bool:
        if not self.round_start_time:
            return False
        return (time.time() - self.round_start_time) > self.round_time

    def get_suggested_answer(self) -> Optional[str]:
        """الحصول على إجابة مقترحة من القاعدة"""
        if self.current_category in self.database:
            if self.current_letter in self.database[self.current_category]:
                answers = self.database[self.current_category][self.current_letter]
                if answers:
                    return random.choice(answers)
        return None

    def validate_answer(self, normalized_answer: str) -> bool:
        """التحقق من صحة الإجابة"""
        if not normalized_answer or len(normalized_answer) < 2:
            return False

        required_letter = self.normalize_text(self.current_letter)
        if normalized_answer[0] != required_letter:
            return False

        return True

    def check_answer(self, user_answer: str, user_id: str, display_name: str) -> Optional[Dict[str, Any]]:
        if not self.game_active:
            return None

        # التحقق من الوقت
        if self._time_expired():
            suggested = self.get_suggested_answer()
            msg = f"⏱️ انتهى الوقت!\nمثال: {suggested}" if suggested else "⏱️ انتهى الوقت!"
            
            self.current_question += 1
            self.answered_users.clear()

            if self.current_question >= self.questions_count:
                result = self.end_game()
                result["message"] = f"{msg}\n\n{result.get('message', '')}"
                return result

            return {
                "message": msg,
                "response": self.get_question(),
                "points": 0
            }

        if user_id in self.answered_users:
            return None

        if self.team_mode and user_id not in self.joined_users:
            return None

        normalized_answer = self.normalize_text(user_answer)

        # ✅ لمح وجاوب للفردي فقط
        if not self.team_mode:
            if normalized_answer == "لمح":
                suggested = self.get_suggested_answer()
                if suggested:
                    hint = f"💡 تبدأ بـ: {suggested[0]}\nعدد الحروف: {len(suggested)}"
                else:
                    hint = "💡 فكر جيداً"
                return {
                    "message": hint,
                    "response": self._create_text_message(hint),
                    "points": 0
                }

            if normalized_answer == "جاوب":
                suggested = self.get_suggested_answer()
                reveal = f"مثال: {suggested}" if suggested else "لا توجد إجابة ثابتة"
                self.current_question += 1
                self.answered_users.clear()

                if self.current_question >= self.questions_count:
                    result = self.end_game()
                    result["message"] = f"{reveal}\n\n{result.get('message', '')}"
                    return result

                return {
                    "message": reveal,
                    "response": self.get_question(),
                    "points": 0
                }

        # التحقق من صحة الإجابة
        is_valid = self.validate_answer(normalized_answer)

        if not is_valid:
            return {
                "message": f"❌ يجب أن تبدأ بحرف {self.current_letter}",
                "response": self._create_text_message(f"❌ يجب أن تبدأ بحرف {self.current_letter}"),
                "points": 0
            }

        self.answered_users.add(user_id)

        base_points = 10
        elapsed = int(time.time() - self.round_start_time)
        remaining = max(0, self.round_time - elapsed)
        time_bonus = max(0, remaining // 2)
        total_points = base_points + time_bonus

        if self.team_mode:
            team = self.get_user_team(user_id)
            if not team:
                team = self.assign_to_team(user_id)
            self.add_team_score(team, total_points)
        else:
            self.add_score(user_id, display_name, total_points)

        self.current_question += 1
        self.answered_users.clear()

        if self.current_question >= self.questions_count:
            result = self.end_game()
            result["points"] = total_points
            return result

        return {
            "message": f"✅ صحيح!\n+{total_points} نقطة",
            "response": self.get_question(),
            "points": total_points
        }
