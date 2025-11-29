"""
Bot Mesh - Base Game v13.0
Created by: Abeer Aldosari © 2025
✅ استيراد الثيمات من constants_v13_optimized
✅ دعم كامل للفرق
✅ can_use_hint() و can_reveal_answer()
"""

from typing import Dict, Any, Optional
from datetime import datetime
from linebot.v3.messaging import FlexMessage, FlexContainer, TextMessage
import re
from constants_v13_optimized import THEMES, DEFAULT_THEME

class BaseGame:
    """BaseGame - نظام اللعبة الأساسي"""
    
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
        
        # دعم الفرق
        self.team_mode = False
        self.joined_users = set()
        self.user_teams: Dict[str, str] = {}
        self.team_scores: Dict[str, int] = {"team1": 0, "team2": 0}
        
        # دعم الجلسات
        self.session_id = None
        self.session_type = "solo"
        self.db = None

    def can_use_hint(self) -> bool:
        """هل يمكن استخدام 'لمح'؟"""
        return (not self.team_mode) and self.supports_hint

    def can_reveal_answer(self) -> bool:
        """هل يمكن استخدام 'جاوب'؟"""
        return (not self.team_mode) and self.supports_reveal

    def normalize_text(self, text: str) -> str:
        """تطبيع النص العربي"""
        if not text:
            return ""
        text = text.strip().lower()
        replacements = {'أ':'ا','إ':'ا','آ':'ا','ى':'ي','ة':'ه','ؤ':'و','ئ':'ي'}
        for old, new in replacements.items():
            text = text.replace(old, new)
        return re.sub(r'[\u064B-\u065F\u0670]', '', text)

    def add_score(self, user_id: str, display_name: str, points: int = 1) -> int:
        """إضافة نقاط"""
        if user_id in self.answered_users:
            return 0
        if user_id not in self.scores:
            self.scores[user_id] = {"name": display_name, "score": 0}
        self.scores[user_id]["score"] += points
        self.answered_users.add(user_id)
        return points

    def add_team_score(self, team_name: str, points: int):
        """إضافة نقاط للفريق"""
        if team_name in self.team_scores:
            self.team_scores[team_name] += points
        return points

    def assign_to_team(self, user_id: str) -> str:
        """تعيين المستخدم لفريق"""
        if user_id in self.user_teams:
            return self.user_teams[user_id]
        team1_count = sum(1 for t in self.user_teams.values() if t == "team1")
        team2_count = sum(1 for t in self.user_teams.values() if t == "team2")
        team = "team1" if team1_count <= team2_count else "team2"
        self.user_teams[user_id] = team
        self.joined_users.add(user_id)
        return team

    def get_user_team(self, user_id: str) -> Optional[str]:
        """الحصول على فريق المستخدم"""
        return self.user_teams.get(user_id)

    def is_user_joined(self, user_id: str) -> bool:
        """التحقق من انضمام المستخدم"""
        return user_id in self.joined_users

    def join_user(self, user_id: str):
        """انضمام مستخدم"""
        self.joined_users.add(user_id)
        if self.team_mode:
            return self.assign_to_team(user_id)
        return None

    def get_theme_colors(self) -> Dict[str, str]:
        """الحصول على ألوان الثيم من constants"""
        return THEMES.get(self.current_theme, THEMES[DEFAULT_THEME])

    def set_theme(self, theme_name: str):
        """تعيين الثيم"""
        if theme_name in THEMES:
            self.current_theme = theme_name

    def set_database(self, db):
        """تعيين قاعدة البيانات"""
        self.db = db

    def start_game(self):
        """بدء اللعبة"""
        self.current_question = 0
        self.scores.clear()
        self.answered_users.clear()
        self.previous_question = None
        self.previous_answer = None
        self.game_active = True
        self.game_start_time = datetime.now()
        return self.get_question()

    def get_question(self):
        """الحصول على السؤال - يجب تطبيقه"""
        raise NotImplementedError("يجب تطبيق get_question في اللعبة")

    def check_answer(self, user_answer: str, user_id: str, display_name: str) -> Optional[Dict[str, Any]]:
        """التحقق من الإجابة - يجب تطبيقه"""
        raise NotImplementedError("يجب تطبيق check_answer في اللعبة")

    def end_game(self) -> Dict[str, Any]:
        """إنهاء اللعبة وإعلان الفائز"""
        self.game_active = False
        
        if self.team_mode:
            team1_score = self.team_scores.get("team1", 0)
            team2_score = self.team_scores.get("team2", 0)
            if team1_score > team2_score:
                winner = "الفريق الأول 🥇"
            elif team2_score > team1_score:
                winner = "الفريق الثاني 🥈"
            else:
                winner = "تعادل ⚖️"
            
            message = (
                f"🏆 انتهت اللعبة!\n\n"
                f"النتيجة النهائية:\n"
                f"▫️ الفريق الأول: {team1_score}\n"
                f"▫️ الفريق الثاني: {team2_score}\n\n"
                f"الفائز: {winner}"
            )
            
            return {
                "game_over": True,
                "points": max(team1_score, team2_score),
                "message": message
            }
        
        if not self.scores:
            return {"game_over": True, "points": 0, "message": "🏁 انتهت اللعبة"}
        
        leaderboard = sorted(self.scores.items(), key=lambda x: x[1]["score"], reverse=True)
        winner = leaderboard[0]
        winner_text = f"🏆 الفائز: {winner[1]['name']}\n▫️ النقاط: {winner[1]['score']}\n\n"
        
        if len(leaderboard) > 1:
            winner_text += "📊 الترتيب:\n"
            for i, (uid, data) in enumerate(leaderboard[:5], 1):
                medal = ["🥇", "🥈", "🥉"][i-1] if i <= 3 else f"{i}."
                winner_text += f"{medal} {data['name']}: {data['score']}\n"
        
        return {"game_over": True, "points": winner[1]["score"], "message": winner_text}

    def _create_text_message(self, text: str):
        """إنشاء رسالة نصية"""
        return TextMessage(text=text)

    def _create_flex_with_buttons(self, alt_text: str, flex_content: dict):
        """إنشاء Flex Message"""
        return FlexMessage(alt_text=alt_text, contents=FlexContainer.from_dict(flex_content))

    def build_question_flex(self, question_text: str, additional_info: str = None):
        """بناء Flex للسؤال"""
        colors = self.get_theme_colors()
        
        contents = [
            {"type": "text", "text": f"{self.game_icon} {self.game_name}", "size": "xl", "weight": "bold", "color": colors["primary"], "align": "center"},
            {"type": "text", "text": f"سؤال {self.current_question + 1} من {self.questions_count}", "size": "sm", "color": colors["text2"], "align": "center", "margin": "xs"},
            {"type": "separator", "margin": "lg", "color": colors["border"]},
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": question_text, "size": "lg", "color": colors["text"], "align": "center", "wrap": True}
                ],
                "cornerRadius": "15px",
                "paddingAll": "20px",
                "margin": "lg",
                "borderWidth": "1px",
                "borderColor": colors["border"]
            }
        ]
        
        if additional_info:
            contents.append({
                "type": "text",
                "text": additional_info,
                "size": "xs",
                "color": colors["text2"],
                "align": "center",
                "wrap": True,
                "margin": "md"
            })
        
        flex_content = {
            "type": "bubble",
            "size": "kilo",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": contents,
                "paddingAll": "20px"
            }
        }
        
        return self._create_flex_with_buttons(self.game_name, flex_content)

    def get_game_info(self) -> Dict[str, Any]:
        """معلومات اللعبة"""
        return {
            "name": self.game_name,
            "questions_count": self.questions_count,
            "supports_hint": self.supports_hint,
            "supports_reveal": self.supports_reveal,
            "active": self.game_active,
            "current_question": self.current_question,
            "players_count": len(self.scores),
            "team_mode": self.team_mode,
            "session_type": self.session_type
        }
