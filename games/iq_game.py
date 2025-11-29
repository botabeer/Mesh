from games.base_game import BaseGame
import random
import time
from typing import Dict, Any, Optional


class IqGame(BaseGame):
    """لعبة الذكاء - ألغاز ذكية"""

    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, questions_count=5)
        self.game_name = "ذكاء"
        self.game_icon = "▫️"
        self.supports_hint = True
        self.supports_reveal = True

        self.round_time = 30
        self.round_start_time = None
        
        self.riddles = [
            {"q": "ما الشيء الذي يمشي بلا أرجل ويبكي بلا عيون؟", "a": ["السحاب", "الغيم", "سحاب", "غيم"]},
            {"q": "له رأس ولكن لا عين له؟", "a": ["الدبوس", "المسمار", "الإبرة", "دبوس", "مسمار", "ابرة"]},
            {"q": "شيء كلما زاد نقص؟", "a": ["العمر", "الوقت", "عمر", "وقت"]},
            {"q": "يكتب ولا يقرأ أبداً؟", "a": ["القلم", "قلم"]},
            {"q": "له أسنان كثيرة ولكنه لا يعض؟", "a": ["المشط", "مشط"]},
            {"q": "يوجد في الماء ولكن الماء يميته؟", "a": ["الملح", "ملح"]},
            {"q": "يتكلم بجميع اللغات دون أن يتعلمها؟", "a": ["الصدى", "صدى"]},
            {"q": "شيء كلما أخذت منه كبر؟", "a": ["الحفرة", "حفرة"]},
            {"q": "يخترق الزجاج ولا يكسره؟", "a": ["الضوء", "النور", "ضوء", "نور"]},
            {"q": "يسمع بلا أذن ويتكلم بلا لسان؟", "a": ["الهاتف", "الجوال", "هاتف", "جوال"]},
            {"q": "ما هو الشيء الذي تراه ولا تستطيع لمسه؟", "a": ["الظل", "ظل"]},
            {"q": "ما هو الذي يمشي بلا قدمين؟", "a": ["الوقت", "وقت", "الزمن"]},
            {"q": "ما هو الشيء الذي إذا دخل الماء لا يبتل؟", "a": ["الضوء", "ضوء"]},
            {"q": "له عينان ولا يرى؟", "a": ["المقص", "مقص"]},
            {"q": "أخضر في الأرض وأسود في السوق وأحمر في البيت؟", "a": ["الشاي", "شاي"]},
            {"q": "ما هو الشيء الذي لا يمشي إلا بالضرب؟", "a": ["المسمار", "مسمار"]},
            {"q": "ما هو الشيء الذي إذا قطعته كبر؟", "a": ["الحبل", "حبل"]},
            {"q": "له أوراق وليس شجراً؟", "a": ["الكتاب", "كتاب"]},
            {"q": "ما هو الشيء الذي يقرصك ولا تراه؟", "a": ["الجوع", "جوع"]},
            {"q": "يمتلئ بالثقوب ويحفظ الماء؟", "a": ["الإسفنج", "اسفنج"]},
            {"q": "يسير بلا قدمين ويدخل الأذنين؟", "a": ["الصوت", "صوت"]},
            {"q": "يولد كبيراً ويموت صغيراً؟", "a": ["الشمعة", "شمعة"]},
            {"q": "له رقبة وليس له رأس؟", "a": ["الزجاجة", "زجاجة"]},
            {"q": "تستطيع كسره دون لمسه؟", "a": ["الوعد", "وعد"]},
            {"q": "ما هو الذي ينام ولا يستيقظ؟", "a": ["الموت", "موت"]},
            {"q": "أبيض في الليل وأسود في النهار؟", "a": ["الطريق", "طريق"]},
            {"q": "ما هو الشيء الذي لا يتكلم ولكن إذا ضربته صاح؟", "a": ["الجرس", "جرس"]},
            {"q": "ما هو الشيء الذي إذا سميته كسر؟", "a": ["الصمت", "صمت"]},
            {"q": "ما هو الشيء الذي تذبحه وتبكي عليه؟", "a": ["البصل", "بصل"]},
            {"q": "يطير بلا أجنحة؟", "a": ["الوقت", "وقت", "الزمن"]},
            {"q": "يسير بلا عيون؟", "a": ["الماء", "ماء"]},
            {"q": "يأكل ولا يشبع؟", "a": ["النار", "نار"]},
            {"q": "ما هو الشيء الذي تراه ولا تمسكه؟", "a": ["الهواء", "هواء"]},
            {"q": "له مفتاح ولا يفتح؟", "a": ["البيانو", "بيانو"]},
            {"q": "يتحرك دائماً حولك ولا تشعر به؟", "a": ["الهواء", "هواء"]},
            {"q": "يُرى ولا يُمس؟", "a": ["الظل", "ظل"]},
            {"q": "ما هو الشيء الذي كلما كبر صغر؟", "a": ["العمر", "عمر"]},
            {"q": "له يد واحدة ولا يستطيع التصفيق؟", "a": ["الساعة", "ساعة"]},
            {"q": "ما هو الشيء الذي له أربع أرجل ولا يمشي؟", "a": ["الكرسي", "كرسي", "الطاولة", "طاولة"]},
            {"q": "يصعد ولا ينزل؟", "a": ["العمر", "عمر", "السلم"]},
            {"q": "ما هو الشيء الذي ينبض بلا قلب؟", "a": ["الساعة", "ساعة"]},
            {"q": "له فم ولا يتكلم؟", "a": ["النهر", "نهر", "الوادي"]},
            {"q": "يجري ولا يمشي؟", "a": ["الماء", "ماء", "النهر"]},
            {"q": "يمكنك رميه ولكن لا يمكنك التقاطه؟", "a": ["الريش", "ريش"]},
            {"q": "ما هو الشيء الذي كلما أعطيته كلما أخذ منك؟", "a": ["السر", "سر"]},
            {"q": "له ذيل ولكن لا جسد له؟", "a": ["العملة", "عملة"]},
            {"q": "يملأ الغرفة ولا يشغل حيزاً؟", "a": ["الضوء", "ضوء", "الهواء"]},
            {"q": "ما هو الشيء الذي له قلب ولكن لا أعضاء أخرى؟", "a": ["الشجرة", "شجرة"]},
            {"q": "له جذور لا يراها أحد؟", "a": ["الشجرة", "شجرة"]},
            {"q": "يرتفع ولا يسقط أبداً؟", "a": ["الدخان", "دخان"]}
        ]

        random.shuffle(self.riddles)
        self.used_riddles = []

    def start_game(self):
        self.current_question = 0
        self.game_active = True
        self.used_riddles = []
        self.previous_question = None
        self.previous_answer = None
        self.answered_users.clear()
        return self.get_question()

    def get_question(self):
        available = [r for r in self.riddles if r not in self.used_riddles]
        if not available:
            self.used_riddles = []
            available = self.riddles.copy()

        riddle = random.choice(available)
        self.used_riddles.append(riddle)
        self.current_answer = riddle["a"]
        self.round_start_time = time.time()

        if self.can_use_hint() and self.can_reveal_answer():
            additional_info = f"الوقت {self.round_time} ثانية\n اكتب 'لمح' أو 'جاوب'"
        else:
            additional_info = f"الوقت {self.round_time} ثانية"

        return self.build_question_flex(
            question_text=f" {riddle['q']}",
            additional_info=additional_info
        )

    def _time_expired(self) -> bool:
        if not self.round_start_time:
            return False
        return (time.time() - self.round_start_time) > self.round_time

    def check_answer(self, user_answer: str, user_id: str, display_name: str) -> Optional[Dict[str, Any]]:
        if not self.game_active:
            return None

        if self._time_expired():
            answers_text = " أو ".join(self.current_answer)
            self.previous_question = self.used_riddles[-1]["q"] if self.used_riddles else None
            self.previous_answer = answers_text
            self.current_question += 1
            self.answered_users.clear()

            if self.current_question >= self.questions_count:
                result = self.end_game()
                result["message"] = f"انتهى الوقت\n الإجابة: {answers_text}\n\n{result.get('message', '')}"
                return result

            return {
                "message": f"انتهى الوقت\n الإجابة: {answers_text}",
                "response": self.get_question(),
                "points": 0
            }

        if user_id in self.answered_users:
            return None
        
        if self.team_mode and user_id not in self.joined_users:
            return None

        normalized = self.normalize_text(user_answer)

        if self.can_use_hint() and normalized == "لمح":
            if not self.current_answer:
                return {
                    "message": "لا توجد تلميحات",
                    "response": self._create_text_message("لا توجد تلميحات"),
                    "points": 0
                }
            
            answer = self.current_answer[0]
            if len(answer) <= 2:
                hint = f"الكلمة قصيرة: {answer[0]}_"
            else:
                hint = f"تلميح: {answer[0]}{answer[1]}{'_' * (len(answer) - 2)}"
            
            return {
                "message": hint,
                "response": self._create_text_message(hint),
                "points": 0
            }

        if self.can_reveal_answer() and normalized == "جاوب":
            answers_text = " أو ".join(self.current_answer)
            self.previous_question = self.used_riddles[-1]["q"] if self.used_riddles else None
            self.previous_answer = answers_text
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

        if self.team_mode and normalized in ["لمح", "جاوب"]:
            return None

        for correct in self.current_answer:
            if self.normalize_text(correct) == normalized:
                total_points = 1

                if self.team_mode:
                    team = self.get_user_team(user_id)
                    if not team:
                        team = self.assign_to_team(user_id)
                    self.add_team_score(team, total_points)
                else:
                    self.add_score(user_id, display_name, total_points)

                self.previous_question = self.used_riddles[-1]["q"] if self.used_riddles else None
                self.previous_answer = correct

                self.current_question += 1
                self.answered_users.clear()

                if self.current_question >= self.questions_count:
                    result = self.end_game()
                    result["points"] = total_points
                    return result

                return {
                    "message": f"صحيح\n+{total_points} نقطة",
                    "response": self.get_question(),
                    "points": total_points
                }

        return {
            "message": "إجابة غير صحيحة",
            "response": self._create_text_message("إجابة غير صحيحة"),
            "points": 0
        }
