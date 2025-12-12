from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
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
        # يمكن تنفيذ فرق لاحقًا
        return None

    def assign_to_team(self, user_id: str) -> str:
        # افتراضي: لا فرق
        return "default"

    def end_game(self) -> Dict[str, Any]:
        self.game_active = False
        return {
            "game_over": True,
            "points": 0,
            "message": "انتهت اللعبة"
        }

    def _create_text_message(self, text: str) -> Dict[str, Any]:
        return {"type": "text", "text": text}

    def build_question_flex(self, question_text: str, additional_info: Optional[str] = None) -> Dict[str, Any]:
        contents = [{"type": "text", "text": question_text, "wrap": True}]
        if additional_info:
            contents.append({"type": "text", "text": additional_info, "wrap": True, "size": "sm", "color": "#888888"})
        return {
            "type": "flex",
            "altText": question_text,
            "contents": {"type": "bubble", "body": {"type": "box", "layout": "vertical", "contents": contents}}
        }

    def get_theme_colors(self) -> Dict[str, str]:
        return {
            "primary": "#1E90FF",
            "text": "#000000",
            "text2": "#555555",
            "text3": "#888888",
            "info": "#17a2b8",
            "success": "#28a745",
            "error": "#dc3545",
            "warning": "#ffc107",
            "border": "#cccccc",
            "card": "#f8f9fa",
            "bg": "#ffffff",
            "info_bg": "#e9f7fd"
        }

    def _create_flex_with_buttons(self, title: str, flex_content: Dict[str, Any]) -> Dict[str, Any]:
        return {"type": "flex", "altText": title, "contents": flex_content}
