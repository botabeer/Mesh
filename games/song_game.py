"""
لعبة تخمين الأغنية - Bot Mesh v9.1 FIXED
Created by: Abeer Aldosari © 2025
✅ فردي: لمح (أول حرف + عدد) + جاوب + مؤقت
✅ فريقين: مؤقت فقط (بدون لمح/جاوب)
"""

from games.base_game import BaseGame
import random
import time
from typing import Dict, Any, Optional


class SongGame(BaseGame):
    """لعبة تخمين الأغنية"""

    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, questions_count=5)
        self.game_name = "أغنية"
        self.game_icon = "🎵"
        self.supports_hint = True
        self.supports_reveal = True

        self.round_time = 30  # ⏱️ 30 ثانية
        self.round_start_time = None

        self.songs = [
            {"lyrics":"رجعت لي أيام الماضي معاك","artist":"أم كلثوم"},
            {"lyrics":"جلست والخوف بعينيها تتأمل فنجاني","artist":"عبد الحليم حافظ"},
            {"lyrics":"تملي معاك ولو حتى بعيد عني","artist":"عمرو دياب"},
            {"lyrics":"يا بنات يا بنات","artist":"نانسي عجرم"},
            {"lyrics":"قولي أحبك كي تزيد وسامتي","artist":"كاظم الساهر"},
            {"lyrics":"أنا لحبيبي وحبيبي إلي","artist":"فيروز"},
            {"lyrics":"حبيبي يا كل الحياة اوعدني تبقى معايا","artist":"تامر حسني"},
            {"lyrics":"قلبي بيسألني عنك دخلك طمني وينك","artist":"وائل كفوري"},
            {"lyrics":"كيف أبيّن لك شعوري دون ما أحكي","artist":"عايض"},
            {"lyrics":"اسخر لك غلا وتشوفني مقصر","artist":"عايض"},
            {"lyrics":"رحت عني ما قويت جيت لك لاتردني","artist":"عبدالمجيد عبدالله"},
            {"lyrics":"خذني من ليلي لليلك","artist":"عبادي الجوهر"},
            {"lyrics":"تدري كثر ماني من البعد مخنوق","artist":"راشد الماجد"},
            {"lyrics":"انسى هالعالم ولو هم يزعلون","artist":"عباس ابراهيم"},
            {"lyrics":"أنا عندي قلب واحد","artist":"حسين الجسمي"},
            {"lyrics":"منوتي ليتك معي","artist":"محمد عبده"},
            {"lyrics":"خلنا مني طمني عليك","artist":"نوال الكويتية"},
            {"lyrics":"أحبك ليه أنا مدري","artist":"عبدالمجيد عبدالله"},
            {"lyrics":"أمر الله أقوى أحبك والعقل واعي","artist":"ماجد المهندس"},
            {"lyrics":"الحب يتعب من يدله والله في حبه بلاني","artist":"راشد الماجد"}
        ]

        random.shuffle(self.songs)
        self.used_songs = []

    def start_game(self):
        self.current_question = 0
        self.game_active = True
        self.previous_question = None
        self.previous_answer = None
        self.answered_users.clear()
        self.used_songs = []
        return self.get_question()

    def get_question(self):
        available = [s for s in self.songs if s not in self.used_songs]
        if not available:
            self.used_songs = []
            available = self.songs.copy()

        q_data = random.choice(available)
        self.used_songs.append(q_data)
        self.current_answer = [q_data["artist"]]
        self.round_start_time = time.time()

        # ✅ استخدام can_use_hint() و can_reveal_answer()
        if self.can_use_hint() and self.can_reveal_answer():
            additional_info = f"⏱️ {self.round_time} ثانية\nمن المغني؟\n💡 اكتب 'لمح' أو 'جاوب'"
        else:
            additional_info = f"⏱️ {self.round_time} ثانية\nمن المغني؟"

        return self.build_question_flex(
            question_text=f"🎵\n{q_data['lyrics']}",
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
            correct = self.current_answer[0]
            self.current_question += 1
            self.answered_users.clear()

            if self.current_question >= self.questions_count:
                result = self.end_game()
                result["message"] = f"⏱️ انتهى الوقت!\nالمغني: {correct}\n\n{result.get('message', '')}"
                return result

            return {
                "message": f"⏱️ انتهى الوقت!\nالمغني: {correct}",
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
            artist = self.current_answer[0]
            hint = f"💡 يبدأ بـ: {artist[0]}\nعدد الحروف: {len(artist)}"
            return {
                "message": hint,
                "response": self._create_text_message(hint),
                "points": 0
            }

        # ✅ كشف الإجابة (فردي فقط)
        if self.can_reveal_answer() and normalized == "جاوب":
            reveal = f"المغني: {self.current_answer[0]}"
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

        # ✅ تجاهل لمح/جاوب في وضع الفريقين بشكل صامت
        if self.team_mode and normalized in ["لمح", "جاوب"]:
            return None

        # التحقق من الإجابة
        correct_normalized = self.normalize_text(self.current_answer[0])
        
        if normalized == correct_normalized:
            base_points = 10
            elapsed = int(time.time() - self.round_start_time)
            remaining = max(0, self.round_time - elapsed)
            time_bonus = max(0, remaining // 3)
            total_points = base_points + time_bonus

            if self.team_mode:
                team = self.get_user_team(user_id)
                if not team:
                    team = self.assign_to_team(user_id)
                self.add_team_score(team, total_points)
            else:
                self.add_score(user_id, display_name, total_points)

            self.answered_users.add(user_id)
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
