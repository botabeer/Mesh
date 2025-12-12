from games.base_game import BaseGame
import random
from typing import Dict, Any, Optional


class ChainWordsGame(BaseGame):
    """لعبة سلسلة محسّنة نهائية"""

    def __init__(self, line_bot_api=None):
        super().__init__(line_bot_api, questions_count=5)
        self.game_name = "سلسلة"
        self.supports_hint = True  # لتفعيل أزرار اللمح والجاوب
        self.supports_reveal = True

        self.starting_words = [
            "سيارة","تفاح","قلم","نجم","كتاب","باب","رمل","لعبة","حديقة","ورد",
            "دفتر","معلم","منزل","شمس","سفر","رياضة","علم","مدرسة","طائرة","عصير",
            "بحر","سماء","طريق","جبل","مدينة","شجرة","حاسب","هاتف","ساعة","مطر",
            "زهرة","سرير","مطبخ","نافذة","مفتاح","مصباح","وسادة","بطارية","لوحة",
            "حقيبة","مزرعة","قطار","مكتبة","مستشفى","ملعب","مسبح","مقهى","مكتب","مطار"
        ]

        self.last_word = None
        self.used_words = set()

    def start_game(self):
        """بدء اللعبة"""
        self.current_question = 0
        self.game_active = True
        self.previous_question = None
        self.previous_answer = None
        self.last_word = random.choice(self.starting_words)
        self.used_words = {self.normalize_text(self.last_word)}
        self.answered_users.clear()
        return self.get_question()

    def get_question(self):
        """سؤال جديد"""
        required_letter = self.last_word[-1]
        return self.build_question_flex(
            question_text=f"الكلمة السابقة\n{self.last_word}",
            additional_info=f"ابدأ بحرف {required_letter}"
        )

    def check_answer(self, user_answer: str, user_id: str, display_name: str) -> Optional[Dict[str, Any]]:
        """التحقق من الإجابة"""
        if not self.game_active:
            return None

        if user_id in self.answered_users:
            return None

        if self.team_mode and user_id not in self.joined_users:
            return None

        normalized_answer = self.normalize_text(user_answer)

        if normalized_answer in self.used_words or len(normalized_answer) < 2:
            return None

        required_letter = self.normalize_text(self.last_word[-1])

        if normalized_answer[0] == required_letter:
            # تسجيل الكلمة
            self.used_words.add(normalized_answer)
            self.previous_question = f"كلمة تبدأ بـ {self.last_word[-1]}"
            self.previous_answer = user_answer.strip()
            self.last_word = user_answer.strip()

            total_points = 1

            # إضافة النقاط حسب الوضع (فردي أو جماعي)
            if self.team_mode:
                team = self.get_user_team(user_id) or self.assign_to_team(user_id)
                self.add_team_score(team, total_points)
                points_to_db = self.team_scores[team]
            else:
                self.add_score(user_id, display_name, total_points)
                points_to_db = self.scores[user_id]["points"]

            # تحديث قاعدة البيانات مباشرة
            if self.db:
                self.db.add_points(user_id, total_points)

            self.current_question += 1
            self.answered_users.clear()

            if self.current_question >= self.questions_count:
                result = self.end_game()
                result["points"] = points_to_db
                return result

            return {
                "message": f" صحيح +{total_points}",
                "response": self.get_question(),
                "points": total_points
            }

        return None

    def build_question_flex(self, question_text: str, additional_info: str = None):
        """واجهة FlexMessage محسّنة مع أزرار لمّح/جاوب"""
        c = self.get_theme_colors()

        progress_percent = int(((self.current_question + 1) / self.questions_count) * 100)
        progress_text = f"السؤال {self.current_question + 1}/{self.questions_count}"

        contents = [
            # عنوان اللعبة
            {
                "type": "text",
                "text": self.game_name,
                "size": "xxl",
                "weight": "bold",
                "color": c["primary"],
                "align": "center"
            },
            # شريط التقدم
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {"type": "text", "text": progress_text, "size": "xs", "color": c["text2"], "flex": 1},
                            {"type": "text", "text": f"{progress_percent}%", "size": "xs", "color": c["primary"], "weight": "bold", "align": "end", "flex": 0}
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [{"type": "box", "layout": "vertical", "contents": [], "width": f"{progress_percent}%", "backgroundColor": c["primary"], "height": "6px", "cornerRadius": "3px"}],
                        "backgroundColor": c["border"],
                        "height": "6px",
                        "cornerRadius": "3px",
                        "margin": "sm"
                    }
                ],
                "margin": "md"
            },
            {"type": "separator", "margin": "lg", "color": c["border"]}
        ]

        # السؤال السابق
        if self.previous_question and self.previous_answer:
            prev_ans = self.previous_answer
            if isinstance(prev_ans, list) and prev_ans:
                prev_ans = prev_ans[0]
            elif not isinstance(prev_ans, str):
                prev_ans = str(prev_ans)

            prev_q = str(self.previous_question)
            if len(prev_q) > 60:
                prev_q = prev_q[:57] + "..."

            contents.append({
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "السؤال السابق", "size": "xs", "color": c["text3"], "weight": "bold"},
                    {"type": "text", "text": prev_q, "size": "xs", "color": c["text2"], "wrap": True, "margin": "xs"},
                    {"type": "box", "layout": "horizontal", "contents": [
                        {"type": "text", "text": "الاجابة:", "size": "xs", "color": c["text3"], "flex": 0},
                        {"type": "text", "text": prev_ans[:50], "size": "xs", "color": c["success"], "wrap": True, "weight": "bold", "flex": 1, "margin": "xs"}
                    ], "margin": "xs"}
                ],
                "backgroundColor": c["card"],
                "cornerRadius": "12px",
                "paddingAll": "12px",
                "borderWidth": "1px",
                "borderColor": c["border"],
                "margin": "md"
            })
            contents.append({"type": "separator", "margin": "lg", "color": c["border"]})

        # السؤال الحالي
        contents.append({
            "type": "box",
            "layout": "vertical",
            "contents": [{"type": "text", "text": question_text, "size": "xl", "color": c["text"], "align": "center", "wrap": True, "weight": "bold"}],
            "backgroundColor": c["card"],
            "cornerRadius": "15px",
            "paddingAll": "20px",
            "borderWidth": "2px",
            "borderColor": c["primary"],
            "margin": "lg"
        })

        if additional_info:
            contents.append({"type": "text", "text": additional_info, "size": "sm", "color": c["info"], "align": "center", "wrap": True, "margin": "md"})

        # أزرار لمّح / جاوب
        if self.can_use_hint() and self.can_reveal_answer():
            contents.extend([
                {"type": "separator", "margin": "xl", "color": c["border"]},
                {"type": "box", "layout": "horizontal", "spacing": "sm", "margin": "lg", "contents": [
                    {"type": "button", "action": {"type": "message", "label": "لمح", "text": "لمح"}, "style": "secondary", "height": "sm", "color": c["secondary"]},
                    {"type": "button", "action": {"type": "message", "label": "جاوب", "text": "جاوب"}, "style": "secondary", "height": "sm", "color": c["secondary"]}
                ]}
            ])

        return self._create_flex_with_buttons(
            self.game_name,
            {
                "type": "bubble",
                "size": "mega",
                "body": {"type": "box", "layout": "vertical", "contents": contents, "paddingAll": "24px", "backgroundColor": c["bg"]}
            }
        )
