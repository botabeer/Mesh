from typing import Dict, Any, Optional, List
from datetime import datetime
from linebot.v3.messaging import FlexMessage, FlexContainer, TextMessage


class BaseGame:
    """
    القاعدة الأساسية لجميع الألعاب
    تم إنشاؤه خصيصًا لمشروع Bot Mesh
    """

    # إعدادات عامة
    game_name = "لعبة"
    supports_hint = True
    supports_answer = True
    supports_timer = False  # للأسرع فقط

    def __init__(self, questions_count: int = 5):
        self.questions_count = questions_count
        self.current_question_index = 0
        self.current_question_data = None
        self.previous_answer = None

        self.players_scores: Dict[str, Dict[str, Any]] = {}
        self.answered_users = set()

        self.game_active = False
        self.game_start_time: Optional[datetime] = None

    # =================================================
    # دورة حياة اللعبة
    # =================================================

    def start(self):
        self.current_question_index = 0
        self.players_scores.clear()
        self.answered_users.clear()
        self.previous_answer = None
        self.game_active = True
        self.game_start_time = datetime.now()
        return self.get_question()

    def get_question(self) -> Dict[str, Any]:
        raise NotImplementedError("يجب تنفيذ get_question في اللعبة الفرعية")

    def check_answer(self, user_answer: str, user_id: str, display_name: str) -> Dict[str, Any]:
        raise NotImplementedError("يجب تنفيذ check_answer في اللعبة الفرعية")

    def next_question(self) -> Dict[str, Any]:
        self.current_question_index += 1
        self.answered_users.clear()

        if self.current_question_index >= self.questions_count:
            return self.end_game()

        return self.get_question()

    def stop_game(self) -> Dict[str, Any]:
        self.game_active = False
        return {
            "game_over": True,
            "response": TextMessage(text="تم إيقاف اللعبة")
        }

    # =================================================
    # النقاط
    # =================================================

    def add_score(self, user_id: str, display_name: str, points: int = 1):
        if user_id not in self.players_scores:
            self.players_scores[user_id] = {
                "name": display_name,
                "score": 0
            }

        self.players_scores[user_id]["score"] += points
        self.answered_users.add(user_id)

    # =================================================
    # التلميح وكشف الإجابة
    # =================================================

    def get_hint(self) -> str:
        if not self.supports_hint or not self.current_question_data:
            return "لا يوجد تلميح"

        answer = str(self.current_question_data["answer"])
        first_letter = answer[0]
        length = len(answer)

        return f"أول حرف: {first_letter} | عدد الحروف: {length}"

    def reveal_answer(self) -> str:
        if not self.supports_answer or not self.current_question_data:
            return "لا توجد إجابة"

        return f"الإجابة الصحيحة: {self.current_question_data['answer']}"

    # =================================================
    # إنهاء اللعبة + إعلان الفائز
    # =================================================

    def end_game(self) -> Dict[str, Any]:
        self.game_active = False

        if not self.players_scores:
            return {
                "game_over": True,
                "response": TextMessage(text="انتهت اللعبة ولم يحقق أحد نقاطًا")
            }

        winner = max(
            self.players_scores.items(),
            key=lambda item: item[1]["score"]
        )

        winner_name = winner[1]["name"]
        winner_score = winner[1]["score"]

        flex = self.build_game_over_flex(winner_name, winner_score)

        return {
            "game_over": True,
            "winner": winner_name,
            "points": winner_score,
            "response": flex
        }

    # =================================================
    # بناء نافذة السؤال (مع عرض جواب السابق)
    # =================================================

    def build_question_flex(
        self,
        question_text: str,
        theme: Dict[str, str],
    ) -> FlexMessage:

        contents = []

        # عنوان اللعبة + الجولة
        contents.append({
            "type": "text",
            "text": f"{self.game_name} - {self.current_question_index + 1}/{self.questions_count}",
            "size": "md",
            "weight": "bold",
            "align": "center",
            "color": theme["text"]
        })

        contents.append({"type": "separator"})

        # عرض إجابة السؤال السابق إذا وجدت
        if self.previous_answer:
            contents.append({
                "type": "text",
                "text": f"إجابة السؤال السابق: {self.previous_answer}",
                "size": "sm",
                "wrap": True,
                "color": theme["text"]
            })
            contents.append({"type": "separator"})

        # السؤال الحالي
        contents.append({
            "type": "box",
            "layout": "vertical",
            "backgroundColor": theme["card"],
            "paddingAll": "12px",
            "cornerRadius": "lg",
            "contents": [
                {
                    "type": "text",
                    "text": question_text,
                    "wrap": True,
                    "size": "lg",
                    "align": "center",
                    "color": theme["text"]
                }
            ]
        })

        # أزرار التحكم
        buttons = []

        if self.supports_hint:
            buttons.append(self._control_button("تلميح", "لمح", theme))

        if self.supports_answer:
            buttons.append(self._control_button("إجابة", "جاوب", theme))

        buttons.append(self._control_button("إيقاف", "إيقاف", theme, danger=True))

        contents.append({
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": buttons
        })

        bubble = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "backgroundColor": theme["bg"],
                "contents": contents
            }
        }

        return FlexMessage(
            alt_text=f"{self.game_name} - سؤال",
            contents=FlexContainer.from_dict(bubble)
        )

    # =================================================
    # نافذة فوز + إعادة
    # =================================================

    def build_game_over_flex(self, winner_name: str, score: int) -> FlexMessage:
        bubble = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "lg",
                "contents": [
                    {
                        "type": "text",
                        "text": "انتهت اللعبة",
                        "weight": "bold",
                        "size": "xl",
                        "align": "center"
                    },
                    {
                        "type": "text",
                        "text": f"الفائز: {winner_name}",
                        "align": "center"
                    },
                    {
                        "type": "text",
                        "text": f"النقاط: {score}",
                        "align": "center"
                    },
                    {
                        "type": "button",
                        "action": {
                            "type": "message",
                            "label": "إعادة",
                            "text": f"لعبة {self.game_name}"
                        },
                        "style": "primary"
                    }
                ]
            }
        }

        return FlexMessage(
            alt_text="انتهت اللعبة",
            contents=FlexContainer.from_dict(bubble)
        )

    # =================================================
    # أزرار التحكم
    # =================================================

    def _control_button(self, label, text, theme, danger=False):
        color = "#dc2626" if danger else theme["btn"]

        return {
            "type": "button",
            "style": "primary",
            "color": color,
            "action": {
                "type": "message",
                "label": label,
                "text": text
            }
        }
