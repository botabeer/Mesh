# games/base_game.py - FIXED VERSION
"""
Bot Mesh - Base Game System FIXED
تم إصلاح التعارضات
"""

from typing import Dict, Any, Optional
from datetime import datetime
from linebot.v3.messaging import FlexMessage, FlexContainer, TextMessage
import re

class BaseGame:
    """BaseGame - نظام اللعبة الأساسي"""
    
    game_name = "لعبة"
    game_icon = "🎮"
    supports_hint = True
    supports_reveal = True

    # ثيمات زجاجية
    THEMES = {
        "أبيض": {
            "bg": "linear-gradient(135deg, #F8FAFC 0%, #E2E8F0 100%)",
            "card": "#FFFFFF",
            "glass": "rgba(255,255,255,0.85)",
            "primary": "#3B82F6",
            "text": "#1E293B",
            "text2": "#64748B",
            "shadow1": "rgba(59,130,246,0.1)",
            "border": "rgba(59,130,246,0.1)",
            "success": "#10B981",
            "error": "#EF4444"
        },
        "أسود": {
            "bg": "linear-gradient(135deg,#0F172A 0%,#1E293B 100%)",
            "card": "#1E293B",
            "glass": "rgba(30,41,59,0.85)",
            "primary": "#60A5FA",
            "text": "#F1F5F9",
            "text2": "#CBD5E1",
            "shadow1": "rgba(96,165,250,0.1)",
            "border": "rgba(96,165,250,0.1)",
            "success": "#10B981",
            "error": "#EF4444"
        }
    }

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
        self.current_theme = "أبيض"

    def normalize_text(self, text: str) -> str:
        """تطبيع النص العربي"""
        if not text:
            return ""
        text = text.strip().lower()
        replacements = {
            'أ': 'ا', 'إ': 'ا', 'آ': 'ا', 
            'ى': 'ي', 'ة': 'ه', 
            'ؤ': 'و', 'ئ': 'ي'
        }
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

    def get_theme_colors(self) -> Dict[str, str]:
        """الحصول على ألوان الثيم"""
        return self.THEMES.get(self.current_theme, self.THEMES["أبيض"])

    def set_theme(self, theme_name: str):
        """تعيين الثيم"""
        if theme_name in self.THEMES:
            self.current_theme = theme_name

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
        """إنهاء اللعبة"""
        self.game_active = False
        if not self.scores:
            return {
                "game_over": True,
                "points": 0,
                "message": "🏁 انتهت اللعبة"
            }
        
        leaderboard = sorted(
            self.scores.items(),
            key=lambda x: x[1]["score"],
            reverse=True
        )
        
        winner = leaderboard[0]
        winner_text = (
            f"🏆 الفائز: {winner[1]['name']}\n"
            f"▫️ النقاط: {winner[1]['score']}\n\n"
            f"📊 الترتيب:\n"
        )
        
        for i, (uid, data) in enumerate(leaderboard[:5], 1):
            medal = ["🥇", "🥈", "🥉"][i-1] if i <= 3 else f"{i}."
            winner_text += f"{medal} {data['name']}: {data['score']}\n"
        
        return {
            "game_over": True,
            "points": winner[1]["score"],
            "message": winner_text
        }

    def get_leaderboard(self) -> str:
        """الحصول على الترتيب"""
        if not self.scores:
            return "لا يوجد لاعبون بعد"
        
        leaderboard = sorted(
            self.scores.items(),
            key=lambda x: x[1]["score"],
            reverse=True
        )
        
        text = "📊 الترتيب:\n"
        for i, (uid, data) in enumerate(leaderboard, 1):
            medal = ["🥇", "🥈", "🥉"][i-1] if i <= 3 else f"{i}."
            text += f"{medal} {data['name']}: {data['score']}\n"
        
        return text

    def _create_text_message(self, text: str):
        """إنشاء رسالة نصية"""
        return TextMessage(text=text)

    def _create_flex_with_buttons(self, alt_text: str, flex_content: dict):
        """إنشاء Flex Message"""
        return FlexMessage(
            alt_text=alt_text,
            contents=FlexContainer.from_dict(flex_content)
        )

    def build_question_flex(self, question_text: str, additional_info: str = None):
        """بناء Flex للسؤال"""
        colors = self.get_theme_colors()
        
        contents = [
            {
                "type": "text",
                "text": f"{self.game_icon} {self.game_name}",
                "size": "xl",
                "weight": "bold",
                "color": colors["primary"],
                "align": "center"
            },
            {
                "type": "text",
                "text": f"سؤال {self.current_question + 1} من {self.questions_count}",
                "size": "sm",
                "color": colors["text2"],
                "align": "center",
                "margin": "xs"
            },
            {
                "type": "separator",
                "color": colors["border"],
                "margin": "lg"
            },
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": question_text,
                        "size": "lg",
                        "color": colors["text"],
                        "align": "center",
                        "wrap": True
                    }
                ],
                "backgroundColor": colors["glass"],
                "cornerRadius": "15px",
                "paddingAll": "20px",
                "margin": "lg"
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
                "paddingAll": "20px",
                "backgroundColor": colors["bg"]
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
            "players_count": len(self.scores)
        }
