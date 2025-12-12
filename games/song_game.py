from games.base_game import BaseGame
import random
from typing import Dict, Any, Optional


class SongGame(BaseGame):
    """لعبة أغنيه"""

    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, questions_count=5)
        self.game_name = "اغنيه"
        self.supports_hint = True
        self.supports_reveal = True

        self.songs = [
            {"lyrics": "رجعت لي أيام الماضي معاك", "artist": "أم كلثوم"},
            {"lyrics": "قولي أحبك كي تزيد وسامتي", "artist": "كاظم الساهر"},
            {"lyrics": "بردان أنا تكفى أبي احترق بدفا لعيونك", "artist": "محمد عبده"},
            {"lyrics": "جلست والخوف بعينيها تتأمل فنجاني", "artist": "عبد الحليم حافظ"},
            {"lyrics": "أحبك موت كلمة مالها تفسير", "artist": "ماجد المهندس"},
            {"lyrics": "تملي معاك ولو حتى بعيد عني", "artist": "عمرو دياب"},
            {"lyrics": "رحت عني ما قويت جيت لك لاتردني", "artist": "عبدالمجيد عبدالله"},
            {"lyrics": "أنا لحبيبي وحبيبي إلي", "artist": "فيروز"},
            {"lyrics": "كيف أبيّن لك شعوري دون ما أحكي", "artist": "عايض"},
            {"lyrics": "خذني من ليلي لليلك", "artist": "عبادي الجوهر"},
            {"lyrics": "تدري كثر ماني من البعد مخنوق", "artist": "راشد الماجد"},
            {"lyrics": "اسخر لك غلا وتشوفني مقصر", "artist": "عايض"},
            {"lyrics": "أشوفك كل يوم وأروح وأقول نظرة ترد الروح", "artist": "محمد عبده"},
            {"lyrics": "منوتي ليتك معي", "artist": "محمد عبده"},
            {"lyrics": "جننت قلبي بحب يلوي ذراعي", "artist": "ماجد المهندس"},
            {"lyrics": "أحبك ليه أنا مدري", "artist": "عبدالمجيد عبدالله"},
            {"lyrics": "في زحمة الناس صعبة حالتي", "artist": "محمد عبده"},
            {"lyrics": "الحب يتعب من يدله والله في حبه بلاني", "artist": "راشد الماجد"},
            {"lyrics": "محد غيرك شغل عقلي شغل بالي", "artist": "وليد الشامي"},
            {"lyrics": "بديت أطيب بديت احس بك عادي", "artist": "ماجد المهندس"},
            {"lyrics": "احس اني لقيتك بس عشان تضيع مني", "artist": "عبدالمجيد عبدالله"},
            {"lyrics": "اختلفنا مين يحب الثاني أكثر", "artist": "محمد عبده"},
            {"lyrics": "من أول نظرة شفتك قلت هذا اللي تمنيته", "artist": "ماجد المهندس"},
            {"lyrics": "لبيه يا بو عيون وساع", "artist": "محمد عبده"},
            {"lyrics": "سألوني الناس عنك يا حبيبي", "artist": "فيروز"},
            {"lyrics": "أنا بلياك إذا أرمش تنزل ألف دمعة", "artist": "ماجد المهندس"},
            {"lyrics": "عطشان يا برق السما", "artist": "ماجد المهندس"},
            {"lyrics": "يراودني شعور إني أحبك أكثر من أول", "artist": "راشد الماجد"},
            {"lyrics": "أنا أكثر شخص بالدنيا يحبك", "artist": "راشد الماجد"},
            {"lyrics": "ليت العمر لو كان مليون مرة", "artist": "راشد الماجد"},
            {"lyrics": "تلمست لك عذر", "artist": "راشد الماجد"},
            {"lyrics": "عظيم إحساسي والشوق فيني", "artist": "راشد الماجد"},
            {"lyrics": "قال الوداع ومقصده يجرح القلب", "artist": "راشد الماجد"},
            {"lyrics": "حبيته بيني وبين نفسي", "artist": "شيرين"},
            {"lyrics": "اللي لقى احبابه نسى اصحابه", "artist": "راشد الماجد"},
            {"lyrics": "مقادير يا قلبي العنا مقادير", "artist": "طلال مداح"},
            {"lyrics": "ظلمتني والله قوي يجازيك", "artist": "طلال مداح"},
            {"lyrics": "كلمة ولو جبر خاطر", "artist": "عبادي الجوهر"},
            {"lyrics": "أنا لولا الغلا والمحبة", "artist": "فؤاد عبدالواحد"},
            {"lyrics": "أحبك لو تكون حاضر", "artist": "عبادي الجوهر"},
            {"lyrics": "ماعاد يمديني ولا عاد يمديك", "artist": "عبدالمجيد عبدالله"},
            {"lyrics": "يا بعدهم كلهم يا سراجي بينهم", "artist": "عبدالمجيد عبدالله"},
            {"lyrics": "حتى الكره احساس", "artist": "عبدالمجيد عبدالله"},
            {"lyrics": "استكثرك وقتي علي", "artist": "عبدالمجيد عبدالله"},
            {"lyrics": "ياما حاولت الفراق وما قويت", "artist": "عبدالمجيد عبدالله"}
        ]

        random.shuffle(self.songs)
        self.used_songs = []

    def start_game(self):
        """بدء اللعبة"""
        self.current_question = 0
        self.game_active = True
        self.previous_question = None
        self.previous_answer = None
        self.answered_users.clear()
        self.used_songs.clear()
        return self.get_question()

    def get_question(self):
        """الحصول على سؤال"""
        available = [s for s in self.songs if s not in self.used_songs]
        if not available:
            self.used_songs.clear()
            available = self.songs.copy()

        q_data = random.choice(available)
        self.used_songs.append(q_data)
        self.current_answer = [q_data["artist"]]

        return self.build_question_flex(
            question_text=q_data['lyrics'],
            additional_info="من المغني"
        )

    def check_answer(self, user_answer: str, user_id: str, display_name: str) -> Optional[Dict[str, Any]]:
        """التحقق من الإجابة"""
        if not self.game_active or user_id in self.answered_users:
            return None

        normalized = self.normalize_text(user_answer)

        if self.can_use_hint() and normalized == "لمح":
            artist = self.current_answer[0]
            hint = f"يبدأ بـ {artist[0]}\nعدد الحروف: {len(artist)}"
            return {"message": hint, "points": 0}

        if self.can_reveal_answer() and normalized == "جاوب":
            reveal = f"المغني: {self.current_answer[0]}"
            self.previous_question = self.used_songs[-1]["lyrics"] if self.used_songs else None
            self.previous_answer = self.current_answer[0]
            self.current_question += 1
            self.answered_users.clear()

            if self.current_question >= self.questions_count:
                result = self.end_game()
                result["message"] = f"{reveal}\n\nانتهت اللعبة"
                return result

            return {"message": reveal, "response": self.get_question(), "points": 0}

        correct_normalized = self.normalize_text(self.current_answer[0])
        
        if normalized == correct_normalized:
            total_points = 1
            
            self.add_score(user_id, display_name, total_points)

            self.previous_question = self.used_songs[-1]["lyrics"] if self.used_songs else None
            self.previous_answer = self.current_answer[0]
            self.answered_users.add(user_id)
            self.current_question += 1
            self.answered_users.clear()

            if self.current_question >= self.questions_count:
                result = self.end_game()
                result["points"] = total_points
                return result

            return {"message": f"صحيح +{total_points}", "response": self.get_question(), "points": total_points}

        return None
