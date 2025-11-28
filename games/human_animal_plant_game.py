“””
لعبة إنسان حيوان نبات - نسخة الفرق + المؤقت + الصدارة
Created by: Abeer Aldosari © 2025
“””

from games.base_game import BaseGame
import random
import time
from typing import Dict, Any, Optional

class HumanAnimalPlantGame(BaseGame):

```
def __init__(self, line_bot_api):
    super().__init__(line_bot_api, questions_count=5)
    self.game_name = "إنسان حيوان نبات"
    self.game_icon = "▪️"

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
            "ض": ["ضبع"],
            "ط": ["طاووس"],
            "ظ": ["ظبي"],
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

    self.team_mode = False
    self.teams = {"A": [], "B": []}
    self.team_scores = {"A": 0, "B": 0}
    self.joined_users = set()

    self.round_start_time = None
    self.round_duration = 25  # ⏱️ مدة الجولة بالثواني

def detect_mode(self, source_type: str):
    self.team_mode = (source_type == "group")

def start_game(self, source_type="user"):
    self.detect_mode(source_type)

    self.current_question = 0
    self.game_active = True
    self.previous_question = None
    self.previous_answer = None
    self.answered_users.clear()

    self.joined_users.clear()
    self.teams = {"A": [], "B": []}
    self.team_scores = {"A": 0, "B": 0}

    if self.team_mode:
        return self._create_text_message(
            "وضع الفريقين مفعل\nاكتب: انضم للمشاركة"
        )

    return self.get_question()

def join_player(self, user_id: str):
    if user_id in self.joined_users:
        return None

    self.joined_users.add(user_id)

    team = "A" if len(self.teams["A"]) <= len(self.teams["B"]) else "B"
    self.teams[team].append(user_id)

    return self._create_text_message(f"تم انضمامك للفريق {team}")

def get_question(self):
    self.current_letter = self.letters[self.current_question % len(self.letters)]
    self.current_category = random.choice(self.categories)
    self.round_start_time = time.time()

    info = f"الفئة: {self.current_category}\nالحرف: {self.current_letter}\n⏱️ 25 ثانية"

    return self._create_text_message(info)

def time_expired(self):
    return (time.time() - self.round_start_time) > self.round_duration

def validate_answer(self, normalized_answer: str) -> bool:
    if not normalized_answer or len(normalized_answer) < 2:
        return False

    required_letter = self.normalize_text(self.current_letter)
    if normalized_answer[0] != required_letter:
        return False

    return True

def get_suggested_answer(self) -> Optional[str]:
    if self.current_category in self.database:
        if self.current_letter in self.database[self.current_category]:
            answers = self.database[self.current_category][self.current_letter]
            if answers:
                return random.choice(answers)
    return None

def check_answer(self, user_answer: str, user_id: str, display_name: str):

    if not self.game_active:
        return None

    if self.time_expired():
        self.current_question += 1
        self.answered_users.clear()

        if self.current_question >= self.questions_count:
            return self.end_game()

        return self.get_question()

    if self.team_mode and user_id not in self.joined_users:
        return None

    if user_id in self.answered_users:
        return None

    normalized_answer = self.normalize_text(user_answer)

    if not self.team_mode:
        if normalized_answer == "لمح":
            suggested = self.get_suggested_answer()
            hint = f"{suggested[0]}{'_' * (len(suggested)-1)}" if suggested else "فكر جيدا"
            return {'message': hint, 'response': self._create_text_message(hint), 'points': 0}

        if normalized_answer == "جاوب":
            suggested = self.get_suggested_answer()
            reveal = f"الإجابة: {suggested}" if suggested else "لا توجد إجابة ثابتة"
            self.current_question += 1
            self.answered_users.clear()

            if self.current_question >= self.questions_count:
                result = self.end_game()
                result['message'] = reveal
                return result

            return {'message': reveal, 'response': self.get_question(), 'points': 0}

    is_valid = self.validate_answer(normalized_answer)

    if not is_valid:
        return {'message': f"يجب أن تبدأ بحرف {self.current_letter}", 'response': None, 'points': 0}

    self.answered_users.add(user_id)

    if self.team_mode:
        team = "A" if user_id in self.teams["A"] else "B"
        self.team_scores[team] += 10
        scored_text = f"نقطة للفريق {team}"
    else:
        points = self.add_score(user_id, display_name, 10)
        scored_text = f"+{points} نقطة"

    self.current_question += 1
    self.answered_users.clear()

    if self.current_question >= self.questions_count:
        return self.end_game()

    return {
        'message': f"صحيح ▫️ {scored_text}",
        'response': self.get_question(),
        'points': 10
    }

def end_game(self):
    self.game_active = False

    if self.team_mode:
        winner = "A" if self.team_scores["A"] > self.team_scores["B"] else "B"
        result_text = (
            f"🏆 النتيجة النهائية\n"
            f"الفريق A: {self.team_scores['A']}\n"
            f"الفريق B: {self.team_scores['B']}\n"
            f"🥇 الفائز: الفريق {winner}"
        )
    else:
        result_text = self.get_leaderboard()

    return {
        'message': result_text,
        'response': self._create_text_message(result_text),
        'points': 0
    }
