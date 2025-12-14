from games.base_game import BaseGame
import random
from typing import Dict, Any, Optional
from linebot.v3.messaging import FlexMessage, FlexContainer, TextMessage

class ChainWordsGame(BaseGame):
    """لعبة سلسلة محسّنة: 5 جولات، دعم الثيم، أمر لمّح وجاوب"""

    def __init__(self, line_bot_api=None):
        super().__init__(line_bot_api, questions_count=5)
        self.game_name = "سلسلة"
        self.starting_words = [
            "سيارة","تفاح","قلم","نجم","كتاب","باب","رمل","لعبة",
            "حديقة","ورد","دفتر","معلم","منزل","شمس","سفر"
        ]
        self.used_words = set()
        self.last_word = None
        self.current_question = 0

    def start_game(self):
        self.current_question = 0
        self.game_active = True
        self.answered_users.clear()
        self.last_word = random.choice(self.starting_words)
        self.used_words = {self.last_word}
        return self.get_question()

    def get_question(self):
        """سؤال جديد مع دعم الثيم"""
        c = self.get_theme_colors()
        required_letter = self.last_word[0]  # لمّح يعطي أول حرف
        total_letters = len(self.last_word)
        return self.build_question_flex(
            question_text=f"ابدأ كلمة جديدة تبدأ بحرف '{required_letter}'",
            additional_info=f"الكلمة المطلوبة مكونة من {total_letters} حرفًا"
        )

    def check_answer(self, user_answer: str, user_id: str, display_name: str) -> Optional[Dict[str, Any]]:
        if not self.game_active or user_id in self.answered_users:
            return None

        normalized = self.normalize_text(user_answer)
        required_letter = self.last_word[-1]

        if normalized[0] == required_letter and normalized not in self.used_words:
            # تسجيل الإجابة الصحيحة
            self.add_score(user_id, display_name, 1)
            self.last_word = normalized
            self.used_words.add(normalized)
            self.answered_users.clear()
            self.current_question += 1

            if self.current_question >= self.questions_count:
                # إعلان الفائز بعد الجولة الخامسة
                winner_id, points = self.get_top_scorer()
                self.game_active = False
                return {"response": TextMessage(text=f"انتهت اللعبة! الفائز: {winner_id} ({points} نقطة)"), "points": 1, "game_over": True}

            # الانتقال للجولة التالية
            return {"response": self.get_question(), "points": 1}

        return None

    def build_question_flex(self, question_text: str, additional_info: str = None):
        """واجهة FlexMessage محسّنة لدعم الثيم والأزرار"""
        c = self.get_theme_colors()

        contents = [
            {"type": "text", "text": self.game_name, "size": "xxl", "weight": "bold", "color": c["primary"], "align": "center"},
            {"type": "text", "text": f"السؤال {self.current_question+1}/{self.questions_count}", "size": "sm", "color": c["text2"], "align": "center", "margin": "md"},
            {"type": "text", "text": question_text, "size": "lg", "color": c["text"], "align": "center", "wrap": True, "margin": "md"}
        ]

        if additional_info:
            contents.append({"type": "text", "text": additional_info, "size": "sm", "color": c["info"], "align": "center", "margin": "md"})

        # أزرار لمّح وجاوب
        contents.append({"type": "box", "layout": "horizontal", "spacing": "sm", "margin": "lg", "contents": [
            {"type": "button", "action": {"type": "message", "label": "لمح", "text": "لمح"}, "style": "secondary", "height": "sm", "color": c["secondary"]},
            {"type": "button", "action": {"type": "message", "label": "جاوب", "text": "جاوب"}, "style": "secondary", "height": "sm", "color": c["secondary"]}
        ]})

        return FlexMessage(
            alt_text="سلسلة - جولة جديدة",
            contents=FlexContainer.from_dict({
                "type": "bubble",
                "body": {"type": "box", "layout": "vertical", "contents": contents, "paddingAll": "20px", "backgroundColor": c["bg"]}
            })
        )
