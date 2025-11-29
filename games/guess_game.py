"""
لعبة التخمين - Bot Mesh v9.1 FIXED
Created by: Abeer Aldosari © 2025
✅ فردي: لمح (أول حرف + عدد) + جاوب + مؤقت
✅ فريقين: مؤقت فقط (بدون لمح/جاوب)
"""

from games.base_game import BaseGame
import random
import time
from typing import Dict, Any, Optional, List


class GuessGame(BaseGame):
    """لعبة التخمين"""

    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, questions_count=5)
        self.game_name = "تخمين"
        self.game_icon = "🔮"
        self.supports_hint = True
        self.supports_reveal = True

        self.round_time = 25  # ⏱️ 25 ثانية
        self.round_start_time = None

        # قاعدة البيانات - 50+ سؤال منطقي مع جميع الإجابات الممكنة
        self.items = {
            "المطبخ": {
                "ق": ["قدر", "قلاية", "قارورة"],
                "م": ["ملعقة", "مغرفة", "مقلاة", "مبشرة"],
                "س": ["سكين", "صحن", "سلة"],
                "ط": ["طنجرة", "طبق"],
                "ف": ["فرن", "فنجان", "فلتر"],
                "ك": ["كأس", "كوب"],
                "ش": ["شوكة", "شاي"],
                "ت": ["تنور", "ترمس"],
                "ص": ["صينية", "صحن"]
            },
            "غرفة النوم": {
                "س": ["سرير", "ستارة"],
                "و": ["وسادة", "ورد"],
                "م": ["مرآة", "مخدة", "مصباح"],
                "خ": ["خزانة"],
                "ل": ["لحاف", "لمبة"],
                "د": ["دولاب"],
                "ش": ["شرشف"]
            },
            "المدرسة": {
                "ق": ["قلم", "قرطاسية"],
                "د": ["دفتر", "دولاب"],
                "ك": ["كتاب", "كراسة"],
                "م": ["مسطرة", "ممحاة", "معلم", "مدير"],
                "س": ["سبورة", "سلم"],
                "ح": ["حقيبة", "حصة"],
                "ط": ["طالب", "طاولة"],
                "ش": ["شنطة"]
            },
            "الفواكه": {
                "ت": ["تفاح", "تمر", "توت", "تين"],
                "م": ["موز", "مشمش", "منجا"],
                "ع": ["عنب"],
                "ب": ["برتقال", "بطيخ", "برقوق"],
                "ر": ["رمان"],
                "ك": ["كمثرى", "كرز", "كيوي"],
                "ف": ["فراولة"],
                "ن": ["نكتارين"]
            },
            "الحيوانات": {
                "ق": ["قطة", "قرد"],
                "س": ["سنجاب"],
                "ف": ["فيل", "فهد", "فأر"],
                "أ": ["أسد", "أرنب"],
                "ج": ["جمل", "جاموس"],
                "ن": ["نمر", "نعامة"],
                "ح": ["حصان", "حمار"],
                "خ": ["خروف"],
                "ز": ["زرافة"],
                "د": ["ديك", "دجاج"]
            },
            "الخضروات": {
                "ب": ["بطاطس", "بصل", "بقدونس"],
                "ط": ["طماطم"],
                "خ": ["خيار", "خس"],
                "ج": ["جزر"],
                "ف": ["فلفل", "فجل"],
                "ك": ["كوسا"],
                "ب": ["باذنجان"],
                "ث": ["ثوم"]
            },
            "المهن": {
                "ط": ["طبيب", "طيار"],
                "م": ["معلم", "مهندس", "محامي"],
                "ك": ["كاتب"],
                "ص": ["صيدلي"],
                "خ": ["خباز"],
                "ن": ["نجار"],
                "ح": ["حداد"],
                "س": ["سائق"]
            },
            "الرياضة": {
                "ك": ["كرة", "كاراتيه"],
                "س": ["سباحة"],
                "ج": ["جري"],
                "ق": ["قفز"],
                "ر": ["رماية"],
                "م": ["مصارعة"],
                "ت": ["تنس"],
                "ج": ["جمباز"]
            },
            "الألوان": {
                "أ": ["أحمر", "أزرق", "أخضر"],
                "أ": ["أصفر"],
                "ب": ["بني", "برتقالي", "بنفسجي"],
                "و": ["وردي"],
                "ر": ["رمادي"]
            },
            "الطقس": {
                "م": ["مطر", "مشمس"],
                "ر": ["رعد", "ريح"],
                "ب": ["برق", "برد"],
                "غ": ["غيم", "غبار"],
                "ث": ["ثلج"],
                "ص": ["صحو"]
            }
        }

        # إنشاء الأسئلة
        self.questions_list: List[Dict[str, Any]] = []
        for category, letters in self.items.items():
            for letter, words in letters.items():
                self.questions_list.append({
                    "category": category,
                    "letter": letter,
                    "answers": words
                })

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
        q_data = self.questions_list[self.current_question % len(self.questions_list)]
        self.current_answer = q_data["answers"]
        self.round_start_time = time.time()

        # ✅ استخدام can_use_hint() و can_reveal_answer()
        if self.can_use_hint() and self.can_reveal_answer():
            additional_info = f"⏱️ {self.round_time} ثانية\n💡 اكتب 'لمح' أو 'جاوب'"
        else:
            additional_info = f"⏱️ {self.round_time} ثانية"

        return self.build_question_flex(
            question_text=f"الفئة: {q_data['category']}\nيبدأ بحرف: {q_data['letter']}",
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
            answers_text = " أو ".join(self.current_answer)
            self.current_question += 1
            self.answered_users.clear()

            if self.current_question >= self.questions_count:
                result = self.end_game()
                result["message"] = f"⏱️ انتهى الوقت!\nالإجابة: {answers_text}\n\n{result.get('message', '')}"
                return result

            return {
                "message": f"⏱️ انتهى الوقت!\nالإجابة: {answers_text}",
                "response": self.get_question(),
                "points": 0
            }

        if user_id in self.answered_users:
            return None
        
        if self.team_mode and user_id not in self.joined_users:
            return None

        normalized = self.normalize_text(user_answer)

        # ✅ التلميح (فردي فقط)
        if self.can_use_hint() and normalized == "لمح":
            if not self.current_answer:
                return {
                    "message": "لا توجد تلميحات",
                    "response": self._create_text_message("لا توجد تلميحات"),
                    "points": 0
                }
            
            answer = self.current_answer[0]
            hint = f"💡 تبدأ بـ: {answer[0]}\nعدد الحروف: {len(answer)}"
            return {
                "message": hint,
                "response": self._create_text_message(hint),
                "points": 0
            }

        # ✅ كشف الإجابة (فردي فقط)
        if self.can_reveal_answer() and normalized == "جاوب":
            answers_text = " أو ".join(self.current_answer)
            self.current_question += 1
            self.answered_users.clear()

            if self.current_question >= self.questions_count:
                result = self.end_game()
                result["message"] = f"الإجابة: {answers_text}\n\n{result.get('message', '')}"
                return result

            return {
                "message": f"الإجابة: {answers_text}",
                "response": self.get_question(),
                "points": 0
            }

        # ✅ تجاهل لمح/جاوب في وضع الفريقين بشكل صامت
        if self.team_mode and normalized in ["لمح", "جاوب"]:
            return None

        # التحقق من الإجابة
        for correct_answer in self.current_answer:
            if self.normalize_text(correct_answer) == normalized:
                
                base_points = 10
                elapsed = int(time.time() - self.round_start_time)
                remaining = max(0, self.round_time - elapsed)
                time_bonus = max(0, remaining // 2)
                total_points = base_points + time_bonus

                # توزيع النقاط
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

        return {
            "message": "❌ خطأ",
            "response": self._create_text_message("❌ خطأ"),
            "points": 0
        }
