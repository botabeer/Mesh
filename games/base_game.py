"""
Bot Mesh Base Game Module
الكلاس الأساسي لجميع الألعاب
Created by: Abeer Aldosari - 2025
"""

from typing import Dict, Any, Optional
from datetime import datetime
from linebot.v3.messaging import FlexMessage, FlexContainer, TextMessage
import re
from constants import THEMES, DEFAULT_THEME

class BaseGame:
    """الكلاس الأساسي لجميع الألعاب"""
    
    game_name = "لعبة"
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
    
    def can_use_hint(self) -> bool:
        """التحقق من إمكانية استخدام التلميح"""
        return (not self.team_mode) and self.supports_hint
    
    def can_reveal_answer(self) -> bool:
        """التحقق من إمكانية كشف الإجابة"""
        return (not self.team_mode) and self.supports_reveal
    
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
        
        text = re.sub(r'[\u064B-\u065F\u0670]', '', text)
        
        return text
    
    def add_score(self, user_id: str, display_name: str, points: int = 1) -> int:
        """إضافة نقاط للاعب"""
        if user_id in self.answered_users:
            return 0
        
        if user_id not in self.scores:
            self.scores[user_id] = {"name": display_name, "score": 0}
        
        self.scores[user_id]["score"] += points
        self.answered_users.add(user_id)
        
        return points
    
    def add_team_score(self, team_name: str, points: int) -> int:
        """إضافة نقاط للفريق"""
        if team_name in self.team_scores:
            self.team_scores[team_name] += points
        return points
    
    def assign_to_team(self, user_id: str) -> str:
        """تعيين المستخدم لفريق"""
        if user_id in self.user_teams:
            return self.user_teams[user_id]
        
        t1_count = sum(1 for t in self.user_teams.values() if t == "team1")
        t2_count = sum(1 for t in self.user_teams.values() if t == "team2")
        
        team = "team1" if t1_count <= t2_count else "team2"
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
        """إضافة مستخدم للعبة"""
        self.joined_users.add(user_id)
        if self.team_mode:
            return self.assign_to_team(user_id)
        return None
    
    def get_theme_colors(self) -> Dict[str, str]:
        """الحصول على ألوان الثيم"""
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
        """الحصول على السؤال التالي - يجب تطبيقها في كل لعبة"""
        raise NotImplementedError("يجب تطبيق get_question في الكلاس الفرعي")
    
    def check_answer(self, user_answer: str, user_id: str, display_name: str) -> Optional[Dict[str, Any]]:
        """التحقق من الإجابة - يجب تطبيقها في كل لعبة"""
        raise NotImplementedError("يجب تطبيق check_answer في الكلاس الفرعي")
    
    def end_game(self) -> Dict[str, Any]:
        """إنهاء اللعبة وحساب النتائج"""
        self.game_active = False
        
        if self.team_mode:
            t1 = self.team_scores.get("team1", 0)
            t2 = self.team_scores.get("team2", 0)
            
            if t1 > t2:
                winner = "الفريق الاول"
            elif t2 > t1:
                winner = "الفريق الثاني"
            else:
                winner = "تعادل"
            
            return {
                "game_over": True,
                "points": max(t1, t2),
                "message": f"انتهت اللعبة\n\nالنتيجة\nالفريق الاول: {t1}\nالفريق الثاني: {t2}\n\nالفائز: {winner}"
            }
        
        if not self.scores:
            return {
                "game_over": True,
                "points": 0,
                "message": "انتهت اللعبة\nلم يشارك احد"
            }
        
        leaderboard = sorted(
            self.scores.items(),
            key=lambda x: x[1]["score"],
            reverse=True
        )
        
        winner = leaderboard[0]
        winner_name = winner[1]['name']
        winner_score = winner[1]['score']
        
        message = f"الفائز: {winner_name}\nالنقاط: {winner_score}\n\n"
        
        if len(leaderboard) > 1:
            message += "الترتيب\n"
            for i, (uid, data) in enumerate(leaderboard[:5], 1):
                message += f"{i}. {data['name']}: {data['score']}\n"
        
        return {
            "game_over": True,
            "points": winner_score,
            "message": message
        }
    
    def _create_text_message(self, text: str) -> TextMessage:
        """إنشاء رسالة نصية"""
        return TextMessage(text=text)
    
    def _create_flex_with_buttons(self, alt_text: str, flex_content: dict) -> FlexMessage:
        """إنشاء رسالة Flex"""
        return FlexMessage(
            alt_text=alt_text,
            contents=FlexContainer.from_dict(flex_content)
        )
    
    def build_question_flex(self, question_text: str, additional_info: str = None) -> FlexMessage:
        """بناء واجهة السؤال الموحدة"""
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
                            {
                                "type": "text",
                                "text": progress_text,
                                "size": "xs",
                                "color": c["text2"],
                                "flex": 1
                            },
                            {
                                "type": "text",
                                "text": f"{progress_percent}%",
                                "size": "xs",
                                "color": c["primary"],
                                "weight": "bold",
                                "align": "end",
                                "flex": 0
                            }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [],
                                "width": f"{progress_percent}%",
                                "backgroundColor": c["primary"],
                                "height": "6px",
                                "cornerRadius": "3px"
                            }
                        ],
                        "backgroundColor": c["border"],
                        "height": "6px",
                        "cornerRadius": "3px",
                        "margin": "sm"
                    }
                ],
                "margin": "md"
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
            elif not isinstance(prev_ans, str):
                prev_ans = str(prev_ans)
            
            prev_q = str(self.previous_question)
            if len(prev_q) > 60:
                prev_q = prev_q[:57] + "..."
            
            contents.append({
                "type": "box",
                "layout": "vertical",
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
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": "الاجابة:",
                                "size": "xs",
                                "color": c["text3"],
                                "flex": 0
                            },
                            {
                                "type": "text",
                                "text": prev_ans[:50],
                                "size": "xs",
                                "color": c["success"],
                                "wrap": True,
                                "weight": "bold",
                                "flex": 1,
                                "margin": "xs"
                            }
                        ],
                        "margin": "xs"
                    }
                ],
                "backgroundColor": c["card"],
                "cornerRadius": "12px",
                "paddingAll": "12px",
                "borderWidth": "1px",
                "borderColor": c["border"],
                "margin": "md"
            })
            
            contents.append({
                "type": "separator",
                "margin": "lg",
                "color": c["border"]
            })
        
        contents.append({
            "type": "box",
            "layout": "vertical",
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
            ],
            "backgroundColor": c["card"],
            "cornerRadius": "15px",
            "paddingAll": "20px",
            "borderWidth": "2px",
            "borderColor": c["primary"],
            "margin": "lg"
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
            contents.extend([
                {
                    "type": "separator",
                    "margin": "xl",
                    "color": c["border"]
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "sm",
                    "margin": "lg",
                    "contents": [
                        {
                            "type": "button",
                            "action": {"type": "message", "label": "لمح", "text": "لمح"},
                            "style": "secondary",
                            "height": "sm",
                            "color": c["secondary"]
                        },
                        {
                            "type": "button",
                            "action": {"type": "message", "label": "جاوب", "text": "جاوب"},
                            "style": "secondary",
                            "height": "sm",
                            "color": c["secondary"]
                        }
                    ]
                }
            ])
        
        return self._create_flex_with_buttons(
            self.game_name,
            {
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
        )
    
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
