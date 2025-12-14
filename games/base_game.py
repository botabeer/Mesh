from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
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
        self.team_scores = {"team_a": 0, "team_b": 0}
        self.user_teams = {}
        self.current_answer = None
        self.supports_hint = False
        self.supports_reveal = False
        self.db = None
        self.theme = Config.DEFAULT_THEME
        self.game_name = "Game"

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
        if not text:
            return ""
        text = text.strip().lower()
        replacements = {
            "أ": "ا", "إ": "ا", "آ": "ا", 
            "ى": "ي", "ة": "ه", "ؤ": "و", "ئ": "ي"
        }
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

    def get_top_scorer(self):
        if not self.scores:
            return "لا يوجد فائز", 0
        
        if self.team_mode:
            if self.team_scores["team_a"] > self.team_scores["team_b"]:
                return "الفريق الاول", self.team_scores["team_a"]
            elif self.team_scores["team_b"] > self.team_scores["team_a"]:
                return "الفريق الثاني", self.team_scores["team_b"]
            else:
                return "تعادل", self.team_scores["team_a"]
        
        top = max(self.scores.items(), key=lambda x: x[1]["points"])
        return top[1]["name"], top[1]["points"]

    def get_user_team(self, user_id: str) -> Optional[str]:
        return self.user_teams.get(user_id)

    def assign_to_team(self, user_id: str) -> str:
        if user_id in self.user_teams:
            return self.user_teams[user_id]
        
        team_a_count = sum(1 for t in self.user_teams.values() if t == "team_a")
        team_b_count = sum(1 for t in self.user_teams.values() if t == "team_b")
        
        team = "team_a" if team_a_count <= team_b_count else "team_b"
        self.user_teams[user_id] = team
        return team

    def add_team_score(self, team: str, points: int):
        if team in self.team_scores:
            self.team_scores[team] += points

    def set_database(self, db):
        self.db = db

    def set_theme(self, theme: str):
        if Config.is_valid_theme(theme):
            self.theme = theme

    def end_game(self) -> Dict[str, Any]:
        self.game_active = False
        winner_name, points = self.get_top_scorer()
        return {
            "game_over": True,
            "points": 0,
            "message": f"انتهت اللعبة\nالفائز: {winner_name}\nالنقاط: {points}"
        }

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
        colors = Config.get_theme(self.theme)
        colors.setdefault("info", colors.get("secondary", "#17a2b8"))
        return colors

    def build_question_flex(self, question_text: str, additional_info: Optional[str] = None) -> FlexMessage:
        c = self.get_theme_colors()
        progress = int(((self.current_question + 1) / self.questions_count) * 100)
        progress_text = f"السؤال {self.current_question + 1} من {self.questions_count}"

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
                "margin": "md",
                "contents": [
                    {
                        "type": "text",
                        "text": progress_text,
                        "size": "xs",
                        "color": c["text2"]
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "backgroundColor": c["border"],
                        "height": "6px",
                        "cornerRadius": "3px",
                        "margin": "sm",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "vertical",
                                "backgroundColor": c["primary"],
                                "width": f"{progress}%",
                                "height": "6px",
                                "cornerRadius": "3px"
                            }
                        ]
                    }
                ]
            },
            {
                "type": "separator",
                "margin": "lg",
                "color": c["border"]
            }
        ]

        if self.previous_question and self.previous_answer:
            prev_ans = self.previous_answer
            if isinstance(prev_ans, list) and prev_ans:
                prev_ans = prev_ans[0]
            prev_ans = str(prev_ans)[:50]
            prev_q = str(self.previous_question)
            if len(prev_q) > 60:
                prev_q = prev_q[:57] + "..."
            
            contents.append({
                "type": "box",
                "layout": "vertical",
                "backgroundColor": c["card"],
                "cornerRadius": "12px",
                "paddingAll": "12px",
                "borderWidth": "1px",
                "borderColor": c["border"],
                "margin": "md",
                "contents": [
                    {
                        "type": "text",
                        "text": "السؤال السابق",
                        "size": "xs",
                        "color": c["text3"],
                        "weight": "bold"
                    },
                    {
                        "type": "text",
                        "text": prev_q,
                        "size": "xs",
                        "color": c["text2"],
                        "wrap": True,
                        "margin": "xs"
                    },
                    {
                        "type": "text",
                        "text": f"الاجابة: {prev_ans}",
                        "size": "xs",
                        "color": c["success"],
                        "wrap": True,
                        "weight": "bold",
                        "margin": "xs"
                    }
                ]
            })
            contents.append({
                "type": "separator",
                "margin": "lg",
                "color": c["border"]
            })

        contents.append({
            "type": "box",
            "layout": "vertical",
            "backgroundColor": c["card"],
            "cornerRadius": "15px",
            "paddingAll": "20px",
            "borderWidth": "2px",
            "borderColor": c["primary"],
            "margin": "lg",
            "contents": [
                {
                    "type": "text",
                    "text": question_text,
                    "size": "xl",
                    "color": c["text"],
                    "align": "center",
                    "wrap": True,
                    "weight": "bold"
                }
            ]
        })

        if additional_info:
            contents.append({
                "type": "text",
                "text": additional_info,
                "size": "sm",
                "color": c["info"],
                "align": "center",
                "wrap": True,
                "margin": "md"
            })

        if self.can_use_hint() and self.can_reveal_answer():
            contents.append({
                "type": "separator",
                "margin": "xl",
                "color": c["border"]
            })
            contents.append({
                "type": "box",
                "layout": "horizontal",
                "spacing": "sm",
                "margin": "lg",
                "contents": [
                    {
                        "type": "button",
                        "action": {
                            "type": "message",
                            "label": "لمح",
                            "text": "لمح"
                        },
                        "style": "secondary",
                        "height": "sm",
                        "color": c["secondary"]
                    },
                    {
                        "type": "button",
                        "action": {
                            "type": "message",
                            "label": "جاوب",
                            "text": "جاوب"
                        },
                        "style": "secondary",
                        "height": "sm",
                        "color": c["secondary"]
                    }
                ]
            })

        flex_dict = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": contents,
                "paddingAll": "24px",
                "backgroundColor": c["bg"]
            }
        }
        
        return FlexMessage(
            alt_text=f"{self.game_name}: {question_text[:50]}",
            contents=FlexContainer.from_dict(flex_dict)
        )
