from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from linebot.v3.messaging import FlexMessage, FlexContainer
import re


class BaseGame(ABC):
    def __init__(self, line_bot_api, questions_count=5):
        self.line_bot_api = line_bot_api
        self.questions_count = questions_count
        self.current_question = 0
        self.game_active = False
        self.previous_question = None
        self.previous_answer = None
        self.answered_users = set()
        self.team_mode = False
        self.joined_users = set()
        self.scores = {}
        self.current_answer = None
        self.supports_hint = False
        self.supports_reveal = False
        self.db = None
        self.theme = "ابيض"

    @abstractmethod
    def start_game(self):
        pass

    @abstractmethod
    def get_question(self):
        pass

    @abstractmethod
    def check_answer(self, user_answer: str, user_id: str, display_name: str) -> Optional[Dict[str, Any]]:
        pass

    def normalize_text(self, text: str) -> str:
        text = text.strip().lower()
        text = re.sub(r'[^\w\s]', '', text)
        return text

    def can_use_hint(self):
        return self.supports_hint

    def can_reveal_answer(self):
        return self.supports_reveal

    def add_score(self, user_id: str, display_name: str, points: int):
        if user_id not in self.scores:
            self.scores[user_id] = {"name": display_name, "points": 0}
        self.scores[user_id]["points"] += points

    def add_team_score(self, team: str, points: int):
        if team not in self.scores:
            self.scores[team] = {"points": 0}
        self.scores[team]["points"] += points

    def get_user_team(self, user_id: str) -> Optional[str]:
        return None

    def assign_to_team(self, user_id: str) -> str:
        return "default"

    def set_database(self, db):
        """تعيين قاعدة البيانات"""
        self.db = db

    def set_theme(self, theme: str):
        """تعيين الثيم"""
        self.theme = theme

    def end_game(self) -> Dict[str, Any]:
        self.game_active = False
        return {
            "game_over": True,
            "points": 0,
            "message": "انتهت اللعبة"
        }

    def _create_text_message(self, text: str) -> Dict[str, Any]:
        from linebot.v3.messaging import TextMessage
        return TextMessage(text=text)

    def build_question_flex(self, question_text: str, additional_info: Optional[str] = None):
        """واجهة FlexMessage محسنة مع ازرار لمح/جاوب"""
        c = self.get_theme_colors()

        progress_percent = int(((self.current_question + 1) / self.questions_count) * 100)
        progress_text = f"السؤال {self.current_question + 1}/{self.questions_count}"

        contents = [
            {
                "type": "text",
                "text": self.game_name,
                "size": "xxl",
                "weight": "bold",
                "color": c["primary"],
                "align": "center"
            },
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

        if self.can_use_hint() and self.can_reveal_answer():
            contents.extend([
                {"type": "separator", "margin": "xl", "color": c["border"]},
                {"type": "box", "layout": "horizontal", "spacing": "sm", "margin": "lg", "contents": [
                    {"type": "button", "action": {"type": "message", "label": "لمح", "text": "لمح"}, "style": "secondary", "height": "sm", "color": c["secondary"]},
                    {"type": "button", "action": {"type": "message", "label": "جاوب", "text": "جاوب"}, "style": "secondary", "height": "sm", "color": c["secondary"]}
                ]}
            ])

        flex_dict = {
            "type": "bubble",
            "size": "mega",
            "body": {"type": "box", "layout": "vertical", "contents": contents, "paddingAll": "24px", "backgroundColor": c["bg"]}
        }

        return FlexMessage(
            alt_text=f"{self.game_name}: {question_text[:50]}",
            contents=FlexContainer.from_dict(flex_dict)
        )

    def get_theme_colors(self) -> Dict[str, str]:
        """الحصول على الوان الثيم"""
        from config import Config
        theme_colors = Config.get_theme(self.theme)
        
        if not theme_colors.get("info"):
            theme_colors["info"] = theme_colors.get("secondary", "#17a2b8")
        
        if not theme_colors.get("info_bg"):
            theme_colors["info_bg"] = "#e9f7fd"
        
        return theme_colors

    def _create_flex_with_buttons(self, title: str, flex_content: Dict[str, Any]):
        return FlexMessage(
            alt_text=title,
            contents=FlexContainer.from_dict(flex_content)
        )
