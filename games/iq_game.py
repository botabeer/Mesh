from games.base_game import BaseGame
import random
from typing import Dict, Any, Optional
from linebot.v3.messaging import FlexMessage, FlexContainer, TextMessage

class IqGame(BaseGame):
    """لعبة ذكاء محسّنة: 5 جولات، دعم الثيم، لمّح وجاوب"""

    def __init__(self, line_bot_api=None):
        super().__init__(line_bot_api, questions_count=5)
        self.game_name = "ذكاء"
        self.supports_hint = True
        self.supports_reveal = True
        
        self.riddles = [
            {"q": "ما الشيء الذي يمشي بلا أرجل ويبكي بلا عيون", "a": ["السحاب", "الغيم"]},
            {"q": "له رأس ولكن لا عين له", "a": ["الدبوس", "المسمار"]},
            {"q": "شيء كلما زاد نقص", "a": ["العمر", "الوقت"]},
            {"q": "يكتب ولا يقرأ أبداً", "a": ["القلم"]},
            {"q": "له أسنان كثيرة ولكنه لا يعض", "a": ["المشط"]},
            {"q": "يوجد في الماء ولكن الماء يميته", "a": ["الملح"]},
            {"q": "يتكلم بجميع اللغات دون أن يتعلمها", "a": ["الصدى"]},
            {"q": "شيء كلما أخذت منه كبر", "a": ["الحفرة"]},
            {"q": "يخترق الزجاج ولا يكسره", "a": ["الضوء", "النور"]},
            {"q": "يسمع بلا أذن ويتكلم بلا لسان", "a": ["الهاتف", "الجوال"]}
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
        self.scores.clear()
        return self.get_question()

    def get_question(self):
        available = [r for r in self.riddles if r not in self.used_riddles]
        if not available:
            self.used_riddles = []
            available = self.riddles.copy()

        riddle = random.choice(available)
        self.used_riddles.append(riddle)
        self.current_answer = riddle["a"]

        return self.build_question_flex(riddle['q'], f"السؤال {self.current_question+1}/{self.questions_count}")

    def check_answer(self, user_answer: str, user_id: str, display_name: str) -> Optional[Dict[str, Any]]:
        if not self.game_active or user_id in self.answered_users:
            return None
        
        normalized = self.normalize_text(user_answer)

        # أمر لمّح
        if self.can_use_hint() and normalized == "لمح":
            if not self.current_answer:
                return None
            answer = self.current_answer[0]
            hint = f"تبدأ بـ {answer[0]} | عدد الحروف: {len(answer)}"
            return {"message": hint, "points": 0}

        # أمر جاوب
        if self.can_reveal_answer() and normalized == "جاوب":
            answers_text = " او ".join(self.current_answer)
            self.previous_question = self.used_riddles[-1]["q"] if self.used_riddles else None
            self.previous_answer = answers_text
            self.current_question += 1
            self.answered_users.clear()

            if self.current_question >= self.questions_count:
                winner_id, points = self.get_top_scorer()
                self.game_active = False
                return {
                    "response": TextMessage(text=f"انتهت اللعبة! الفائز: {winner_id} ({points} نقطة)\nالإجابة: {answers_text}"),
                    "points": 0,
                    "game_over": True
                }

            return {"message": f"الإجابة: {answers_text}", "response": self.get_question(), "points": 0}

        # التحقق من الإجابة الصحيحة
        for correct in self.current_answer:
            if self.normalize_text(correct) == normalized:
                self.answered_users.add(user_id)
                total_points = 1

                if self.team_mode:
                    team = self.get_user_team(user_id) or self.assign_to_team(user_id)
                    self.add_team_score(team, total_points)
                else:
                    self.add_score(user_id, display_name, total_points)

                self.previous_question = self.used_riddles[-1]["q"] if self.used_riddles else None
                self.previous_answer = user_answer.strip()
                self.current_question += 1
                self.answered_users.clear()

                if self.current_question >= self.questions_count:
                    winner_id, points = self.get_top_scorer()
                    self.game_active = False
                    return {
                        "response": TextMessage(text=f"انتهت اللعبة! الفائز: {winner_id} ({points} نقطة)"),
                        "points": total_points,
                        "game_over": True
                    }

                return {"message": f"صحيح +{total_points}", "response": self.get_question(), "points": total_points}

        return None

    def build_question_flex(self, question_text: str, additional_info: str = None):
        """واجهة FlexMessage محسّنة مع دعم الثيم وأزرار لمّح / جاوب"""
        c = self.get_theme_colors()
        contents = [
            {"type": "text", "text": self.game_name, "size": "xxl", "weight": "bold", "color": c["primary"], "align": "center"},
            {"type": "text", "text": question_text, "size": "lg", "color": c["text"], "align": "center", "wrap": True, "margin": "md"}
        ]
        if additional_info:
            contents.append({"type": "text", "text": additional_info, "size": "sm", "color": c["info"], "align": "center", "margin": "md"})

        # أزرار لمّح / جاوب
        contents.append({"type": "box", "layout": "horizontal", "spacing": "sm", "margin": "lg", "contents": [
            {"type": "button", "action": {"type": "message", "label": "لمح", "text": "لمح"}, "style": "secondary", "height": "sm", "color": c["secondary"]},
            {"type": "button", "action": {"type": "message", "label": "جاوب", "text": "جاوب"}, "style": "secondary", "height": "sm", "color": c["secondary"]}
        ]})

        return FlexMessage(
            alt_text=f"{self.game_name} - جولة جديدة",
            contents=FlexContainer.from_dict({
                "type": "bubble",
                "body": {"type": "box", "layout": "vertical", "contents": contents, "paddingAll": "20px", "backgroundColor": c["bg"]}
            })
        )
