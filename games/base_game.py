"""Bot Mesh - Base Game v19.0 COMPACT | © 2025 Abeer Aldosari"""
from typing import Dict, Any, Optional
from datetime import datetime
from linebot.v3.messaging import FlexMessage, FlexContainer, TextMessage
import re
from constants import THEMES, DEFAULT_THEME

class BaseGame:
    game_name = "لعبة"
    game_icon = "🎮"
    supports_hint = True
    supports_reveal = True

    def __init__(self, line_bot_api=None, questions_count: int = 5):
        self.line_bot_api = line_bot_api
        self.questions_count = questions_count
        self.current_question = 0
        self.current_answer = None
        self.previous_question = None
        self.previous_answer = None
        self.scores: Dict[str, Dict[str, Any]] = {}
        self.answered_users = set()
        self.game_active = False
        self.game_start_time: Optional[datetime] = None
        self.current_theme = DEFAULT_THEME
        self.team_mode = False
        self.joined_users = set()
        self.user_teams: Dict[str, str] = {}
        self.team_scores: Dict[str, int] = {"team1": 0, "team2": 0}
        self.session_id = None
        self.session_type = "solo"
        self.db = None

    def can_use_hint(self) -> bool: return (not self.team_mode) and self.supports_hint
    def can_reveal_answer(self) -> bool: return (not self.team_mode) and self.supports_reveal
    def normalize_text(self, text: str) -> str:
        if not text: return ""
        text = text.strip().lower()
        for old, new in {'أ':'ا','إ':'ا','آ':'ا','ى':'ي','ة':'ه','ؤ':'و','ئ':'ي'}.items(): text = text.replace(old, new)
        return re.sub(r'[\u064B-\u065F\u0670]', '', text)

    def add_score(self, user_id: str, display_name: str, points: int = 1) -> int:
        if user_id in self.answered_users: return 0
        if user_id not in self.scores: self.scores[user_id] = {"name": display_name, "score": 0}
        self.scores[user_id]["score"] += 1
        self.answered_users.add(user_id)
        return 1

    def add_team_score(self, team_name: str, points: int):
        if team_name in self.team_scores: self.team_scores[team_name] += 1
        return 1

    def assign_to_team(self, user_id: str) -> str:
        if user_id in self.user_teams: return self.user_teams[user_id]
        t1_count = sum(1 for t in self.user_teams.values() if t == "team1")
        t2_count = sum(1 for t in self.user_teams.values() if t == "team2")
        team = "team1" if t1_count <= t2_count else "team2"
        self.user_teams[user_id] = team
        self.joined_users.add(user_id)
        return team

    def get_user_team(self, user_id: str) -> Optional[str]: return self.user_teams.get(user_id)
    def is_user_joined(self, user_id: str) -> bool: return user_id in self.joined_users
    def join_user(self, user_id: str):
        self.joined_users.add(user_id)
        if self.team_mode: return self.assign_to_team(user_id)
        return None

    def get_theme_colors(self) -> Dict[str, str]: return THEMES.get(self.current_theme, THEMES[DEFAULT_THEME])
    def set_theme(self, theme_name: str):
        if theme_name in THEMES: self.current_theme = theme_name
    def set_database(self, db): self.db = db

    def start_game(self):
        self.current_question = 0
        self.scores.clear()
        self.answered_users.clear()
        self.previous_question = None
        self.previous_answer = None
        self.game_active = True
        self.game_start_time = datetime.now()
        return self.get_question()

    def get_question(self): raise NotImplementedError("يجب تطبيق get_question")
    def check_answer(self, user_answer: str, user_id: str, display_name: str) -> Optional[Dict[str, Any]]: raise NotImplementedError("يجب تطبيق check_answer")

    def end_game(self) -> Dict[str, Any]:
        self.game_active = False
        if self.team_mode:
            t1, t2 = self.team_scores.get("team1",0), self.team_scores.get("team2",0)
            winner = "الفريق الأول 🥇" if t1>t2 else "الفريق الثاني 🥈" if t2>t1 else "تعادل"
            return {"game_over":True,"points":max(t1,t2),"message":f"🏆 انتهت اللعبة!\n\nالنتيجة:\nالفريق الأول: {t1}\nالفريق الثاني: {t2}\n\nالفائز: {winner}"}
        if not self.scores: return {"game_over":True,"points":0,"message":"انتهت اللعبة"}
        lb = sorted(self.scores.items(), key=lambda x: x[1]["score"], reverse=True)
        winner = lb[0]
        msg = f"🏆 الفائز: {winner[1]['name']}\nالنقاط: {winner[1]['score']}\n\n"
        if len(lb) > 1:
            msg += "الترتيب:\n"
            for i, (uid, data) in enumerate(lb[:5], 1):
                medal = ["🥇","🥈","🥉"][i-1] if i<=3 else f"{i}."
                msg += f"{medal} {data['name']}: {data['score']}\n"
        return {"game_over":True,"points":winner[1]["score"],"message":msg}

    def _create_text_message(self, text: str): return TextMessage(text=text)
    def _create_flex_with_buttons(self, alt_text: str, flex_content: dict): return FlexMessage(alt_text=alt_text, contents=FlexContainer.from_dict(flex_content))
    def _glass_box_enhanced(self, contents, radius="15px", padding="15px"):
        c = self.get_theme_colors()
        return {"type":"box","layout":"vertical","contents":contents,"cornerRadius":radius,"paddingAll":padding,"borderWidth":"1px","borderColor":c["border"]}

    def build_question_flex(self, question_text: str, additional_info: str = None):
        c = self.get_theme_colors()
        contents = [
            {"type":"text","text":f"{self.game_icon} {self.game_name}","size":"xl","weight":"bold","color":c["primary"],"align":"center"},
            {"type":"text","text":f"سؤال {self.current_question + 1} من {self.questions_count}","size":"sm","color":c["text2"],"align":"center","margin":"xs"},
            {"type":"separator","margin":"lg","color":c["border"]}
        ]
        if self.previous_question and self.previous_answer:
            prev_ans = self.previous_answer if isinstance(self.previous_answer, str) else (self.previous_answer[0] if isinstance(self.previous_answer, list) and self.previous_answer else "")
            prev_q = str(self.previous_question)
            if len(prev_q) > 50: prev_q = prev_q[:47] + "..."
            contents.append(self._glass_box_enhanced([
                {"type":"text","text":"السؤال السابق","size":"xs","color":c["text3"],"weight":"bold"},
                {"type":"text","text":prev_q,"size":"xs","color":c["text2"],"wrap":True,"margin":"xs"},
                {"type":"text","text":f"الإجابة: {prev_ans}","size":"xs","color":c["success"],"wrap":True,"margin":"xs","weight":"bold"}
            ],"10px","10px"))
            contents.append({"type":"separator","margin":"md","color":c["border"]})
        contents.append(self._glass_box_enhanced([{"type":"text","text":question_text,"size":"lg","color":c["text"],"align":"center","wrap":True,"weight":"bold"}],"15px","20px"))
        if additional_info: contents.append({"type":"text","text":additional_info,"size":"xs","color":c["text2"],"align":"center","wrap":True,"margin":"md"})
        return self._create_flex_with_buttons(self.game_name,{"type":"bubble","size":"mega","body":{"type":"box","layout":"vertical","contents":contents,"paddingAll":"20px","backgroundColor":c["bg"]}})

    def get_game_info(self) -> Dict[str, Any]:
        return {"name":self.game_name,"questions_count":self.questions_count,"supports_hint":self.supports_hint,"supports_reveal":self.supports_reveal,"active":self.game_active,"current_question":self.current_question,"players_count":len(self.scores),"team_mode":self.team_mode,"session_type":self.session_type}
