from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from linebot.v3.messaging import FlexMessage, FlexContainer, TextMessage
import re
from config import Config


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
        self.theme = Config.DEFAULT_THEME
        self.game_name = "Game"

    @abstractmethod
    def start_game(self):
        """ابدأ اللعبة"""
        pass

    @abstractmethod
    def get_question(self) -> str:
        """ارجاع نص السؤال الحالي"""
        pass

    @abstractmethod
    def check_answer(self, user_answer: str, user_id: str, display_name: str) -> Optional[Dict[str, Any]]:
        """تحقق من الاجابة"""
        pass

    def normalize_text(self, text: str) -> str:
        if not text:
            return ""
        text = text.strip().lower()
        replacements = {"أ": "ا", "إ": "ا", "آ": "ا", "ى": "ي", "ة": "ه", "ؤ": "و", "ئ": "ي"}
        for old, new in replacements.items():
            text = text.replace(old, new)
        text = re.sub(r"[\u064B-\u065F\u0670]", "", text)
        text = re.sub(r"[^\w\sء-ي]", "", text)
        return text

    def can_use_hint(self) -> bool:
        return self.supports_hint

    def can_reveal_answer(self) -> bool:
        return self.supports_reveal

    def add_score(self, user_id: str, display_name: str, points: int):
        if user_id not in self.scores:
            self.scores[user_id] = {"name": display_name, "points": 0}
        self.scores[user_id]["points"] += points

    def set_database(self, db):
        self.db = db

    def set_theme(self, theme: str):
        if Config.is_valid_theme(theme):
            self.theme = theme

    def end_game(self) -> Dict[str, Any]:
        self.game_active = False
        return {"game_over": True, "points": 0, "message": "انتهت اللعبة"}

    def normalize_result(self, result: Any) -> Dict[str, Any]:
        if result is None:
            return None
        if isinstance(result, TextMessage):
            return {"response": result, "points": 0, "game_over": False}
        if isinstance(result, dict):
            result.setdefault("points", 0)
            result.setdefault("game_over", False)
            return result
        return {"response": result, "points": 0, "game_over": False}

    def get_theme_colors(self) -> Dict[str, str]:
        c = Config.get_theme(self.theme)
        c.setdefault("info", c.get("secondary", "#17a2b8"))
        c.setdefault("info_bg", "#e9f7fd")
        return c

    def build_question_flex(self, question_text: str, additional_info: Optional[str] = None) -> FlexMessage:
        c = self.get_theme_colors()
        progress_percent = int(((self.current_question + 1) / self.questions_count) * 100)
        progress_text = f"السؤال {self.current_question + 1}/{self.questions_count}"

        contents = [
            {"type": "text", "text": self.game_name, "size": "xxl", "weight": "bold", "color": c["primary"], "align": "center"},
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": progress_text, "size": "xs", "color": c["text2"]},
                    {"type": "box", "layout": "vertical", "backgroundColor": c["border"], "contents": [
                        {"type": "box", "layout": "vertical", "backgroundColor": c["primary"], "width": f"{progress_percent}%", "height": "6px", "cornerRadius": "3px"}
                    ], "height": "6px", "cornerRadius": "3px", "margin": "sm"}
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
                    {"type": "text", "text": f"الاجابة: {prev_ans[:50]}", "size": "xs", "color": c["success"], "wrap": True, "weight": "bold", "margin": "xs"}
                ],
                "backgroundColor": c["card"], "cornerRadius": "12px", "paddingAll": "12px", "borderWidth": "1px", "borderColor": c["border"], "margin": "md"
            })
            contents.append({"type": "separator", "margin": "lg", "color": c["border"]})

        contents.append({
            "type": "box",
            "layout": "vertical",
            "contents": [{"type": "text", "text": question_text, "size": "xl", "color": c["text"], "align": "center", "wrap": True, "weight": "bold"}],
            "backgroundColor": c["card"], "cornerRadius": "15px", "paddingAll": "20px", "borderWidth": "2px", "borderColor": c["primary"], "margin": "lg"
        })

        if additional_info:
            contents.append({"type": "text", "text": additional_info, "size": "sm", "color": c["info"], "align": "center", "wrap": True, "margin": "md"})

        # أزرار "لمح" و "جاوب"
        if self.can_use_hint() and self.can_reveal_answer():
            contents.append({"type": "separator", "margin": "xl", "color": c["border"]})
            contents.append({"type": "box", "layout": "horizontal", "spacing": "sm", "margin": "lg", "contents": [
                {"type": "button", "action": {"type": "message", "label": "لمح", "text": "لمح"}, "style": "secondary", "height": "sm", "color": c["secondary"]},
                {"type": "button", "action": {"type": "message", "label": "جاوب", "text": "جاوب"}, "style": "secondary", "height": "sm", "color": c["secondary"]}
            ]})

        flex_dict = {"type": "bubble", "size": "mega", "body": {"type": "box", "layout": "vertical", "contents": contents, "paddingAll": "24px", "backgroundColor": c["bg"]}}
        return FlexMessage(alt_text=f"{self.game_name}: {question_text[:50]}", contents=FlexContainer.from_dict(flex_dict))
