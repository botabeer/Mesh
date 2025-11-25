"""
Bot Mesh - Base Game Class (Neumorphism Soft Edition)
Created by: Abeer Aldosari © 2025
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Set
from dataclasses import dataclass
from datetime import datetime
import re
import logging

from linebot.v3.messaging import TextMessage, FlexMessage, FlexContainer

logger = logging.getLogger(__name__)

@dataclass
class PlayerScore:
    """بيانات اللاعب"""
    user_id: str
    display_name: str
    points: int = 0
    correct: int = 0

class BaseGame(ABC):
    """الكلاس الأساسي لجميع الألعاب - Neumorphism Edition"""
    
    def __init__(self, line_bot_api, questions_count: int = 5, rounds: int = None):
        self.line_bot_api = line_bot_api
        self.questions_count = questions_count
        self.rounds = rounds if rounds is not None else questions_count
        self.current_question = 0
        self.current_round = 0
        self.current_answer = None
        self.game_active = True
        self.scores: Dict[str, PlayerScore] = {}
        self.answered_users: Set[str] = set()
        self.created_at = datetime.now()
        self.theme = "💜"
        self.supports_hint = True
        self.supports_reveal = True
    
    @abstractmethod
    def start_game(self) -> Any:
        """بدء اللعبة وإرجاع أول سؤال"""
        pass
    
    @abstractmethod
    def check_answer(self, answer: str, uid: str, name: str) -> Optional[Dict[str, Any]]:
        """التحقق من إجابة اللاعب"""
        pass
    
    def generate_question(self) -> Any:
        """توليد سؤال جديد"""
        pass
    
    def get_question(self) -> Any:
        """الحصول على السؤال الحالي"""
        pass
    
    def set_theme(self, theme_emoji: str):
        """تعيين ثيم اللعبة"""
        self.theme = theme_emoji
    
    def get_theme_colors(self) -> Dict[str, str]:
        """الحصول على ألوان الثيم الحالي - Neumorphism Soft"""
        themes = {
            "💜": {
                "bg": "#E0E5EC",
                "card": "#E0E5EC",
                "primary": "#9F7AEA",
                "secondary": "#B794F4",
                "text": "#44337A",
                "text2": "#6B46C1",
                "shadow1": "#A3B1C6",
                "shadow2": "#FFFFFF"
            },
            "💚": {
                "bg": "#E0E5EC",
                "card": "#E0E5EC",
                "primary": "#48BB78",
                "secondary": "#68D391",
                "text": "#234E52",
                "text2": "#2C7A7B",
                "shadow1": "#A3B1C6",
                "shadow2": "#FFFFFF"
            },
            "🤍": {
                "bg": "#E0E5EC",
                "card": "#E0E5EC",
                "primary": "#667EEA",
                "secondary": "#7F9CF5",
                "text": "#2D3748",
                "text2": "#718096",
                "shadow1": "#A3B1C6",
                "shadow2": "#FFFFFF"
            },
            "🖤": {
                "bg": "#2D3748",
                "card": "#3A4556",
                "primary": "#667EEA",
                "secondary": "#7F9CF5",
                "text": "#E2E8F0",
                "text2": "#CBD5E0",
                "shadow1": "#1A202C",
                "shadow2": "#414D5F"
            },
            "💙": {
                "bg": "#E0E5EC",
                "card": "#E0E5EC",
                "primary": "#3182CE",
                "secondary": "#4299E1",
                "text": "#2C5282",
                "text2": "#2B6CB0",
                "shadow1": "#A3B1C6",
                "shadow2": "#FFFFFF"
            },
            "🩶": {
                "bg": "#E0E5EC",
                "card": "#E0E5EC",
                "primary": "#718096",
                "secondary": "#A0AEC0",
                "text": "#2D3748",
                "text2": "#4A5568",
                "shadow1": "#A3B1C6",
                "shadow2": "#FFFFFF"
            },
            "🩷": {
                "bg": "#E0E5EC",
                "card": "#E0E5EC",
                "primary": "#D53F8C",
                "secondary": "#ED64A6",
                "text": "#702459",
                "text2": "#97266D",
                "shadow1": "#A3B1C6",
                "shadow2": "#FFFFFF"
            },
            "🧡": {
                "bg": "#E0E5EC",
                "card": "#E0E5EC",
                "primary": "#DD6B20",
                "secondary": "#ED8936",
                "text": "#7C2D12",
                "text2": "#C05621",
                "shadow1": "#A3B1C6",
                "shadow2": "#FFFFFF"
            },
            "🤎": {
                "bg": "#E0E5EC",
                "card": "#E0E5EC",
                "primary": "#8B4513",
                "secondary": "#A0522D",
                "text": "#5C2E00",
                "text2": "#7A4F1D",
                "shadow1": "#A3B1C6",
                "shadow2": "#FFFFFF"
            }
        }
        return themes.get(self.theme, themes["💜"])
    
    def normalize_text(self, text: str) -> str:
        """تطبيع النص العربي"""
        if not text:
            return ""
        t = re.sub(r'[\u0617-\u061A\u064B-\u0652]', '', text)
        t = re.sub(r'[أإآ]', 'ا', t)
        t = re.sub(r'[ة]', 'ه', t)
        t = re.sub(r'[ىئ]', 'ي', t)
        return ' '.join(t.split()).strip()
    
    def add_score(self, uid: str, name: str, pts: int) -> int:
        """إضافة نقاط للاعب"""
        if uid not in self.scores:
            self.scores[uid] = PlayerScore(uid, name)
        self.scores[uid].points += pts
        self.scores[uid].correct += 1
        self.answered_users.add(uid)
        return pts
    
    def get_hint(self) -> str:
        """الحصول على تلميح"""
        if not self.current_answer:
            return "لا يوجد تلميح"
        answer_str = str(self.current_answer).strip()
        first_char = answer_str[0] if answer_str else "؟"
        length = len(answer_str)
        return f"تلميح: أول حرف '{first_char}' وعدد الحروف {length}"
    
    def reveal_answer(self) -> str:
        """كشف الإجابة الصحيحة"""
        return f"الإجابة الصحيحة: {self.current_answer}"
    
    def next_question(self) -> Any:
        """الانتقال للسؤال التالي"""
        self.current_question += 1
        self.current_round += 1
        self.answered_users.clear()
        
        if self.current_question >= self.questions_count:
            return self.end_game()
        
        try:
            return self.get_question()
        except:
            return self.end_game()
    
    def end_game(self) -> Dict[str, Any]:
        """إنهاء اللعبة وعرض النتائج - Neumorphism"""
        self.game_active = False
        sorted_players = sorted(self.scores.values(), key=lambda x: x.points, reverse=True)
        colors = self.get_theme_colors()
        
        if sorted_players:
            winner = sorted_players[0]
            
            # بناء قائمة اللاعبين
            players_list = []
            medals = ["🥇", "🥈", "🥉"]
            for i, player in enumerate(sorted_players[:5]):
                medal = medals[i] if i < 3 else f"{i+1}."
                players_list.append({
                    "type": "text",
                    "text": f"{medal} {player.display_name}: {player.points} نقطة",
                    "size": "sm",
                    "color": colors["text"]
                })
            
            flex_content = {
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
                            "color": colors["primary"],
                            "align": "center"
                        },
                        {"type": "separator", "color": colors["shadow1"]},
                        {
                            "type": "box",
                            "layout": "vertical",
                            "spacing": "md",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": f"الفائز: {winner.display_name}",
                                    "size": "lg",
                                    "weight": "bold",
                                    "color": colors["text"],
                                    "align": "center"
                                },
                                {
                                    "type": "text",
                                    "text": f"{winner.points} نقطة",
                                    "size": "xl",
                                    "weight": "bold",
                                    "color": colors["primary"],
                                    "align": "center"
                                }
                            ],
                            "backgroundColor": colors["card"],
                            "cornerRadius": "20px",
                            "paddingAll": "20px"
                        },
                        {"type": "separator", "color": colors["shadow1"]},
                        {
                            "type": "box",
                            "layout": "vertical",
                            "spacing": "sm",
                            "contents": players_list,
                            "backgroundColor": colors["card"],
                            "cornerRadius": "20px",
                            "paddingAll": "15px"
                        }
                    ],
                    "backgroundColor": colors["bg"],
                    "paddingAll": "20px"
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "button",
                            "action": {"type": "message", "label": "مساعدة", "text": "مساعدة"},
                            "style": "secondary",
                            "height": "sm"
                        },
                        {"type": "separator", "color": colors["shadow1"]},
                        {
                            "type": "text",
                            "text": "تم إنشاؤه بواسطة عبير الدوسري © 2025",
                            "size": "xxs",
                            "color": colors["text2"],
                            "align": "center"
                        }
                    ],
                    "backgroundColor": colors["bg"],
                    "paddingAll": "15px"
                },
                "styles": {
                    "body": {"backgroundColor": colors["bg"]},
                    "footer": {"backgroundColor": colors["bg"]}
                }
            }
            
            msg = f"الفائز: {winner.display_name} بـ {winner.points} نقطة"
        else:
            flex_content = {
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
                            "color": colors["primary"],
                            "align": "center"
                        },
                        {"type": "separator", "color": colors["shadow1"]},
                        {
                            "type": "text",
                            "text": "لم يشارك أحد في اللعبة",
                            "size": "md",
                            "color": colors["text2"],
                            "align": "center"
                        }
                    ],
                    "backgroundColor": colors["bg"],
                    "paddingAll": "20px"
                }
            }
            msg = "لم يشارك أحد"
        
        return {
            'game_over': True,
            'message': msg,
            'response': FlexMessage(alt_text="نتيجة اللعبة", contents=FlexContainer.from_dict(flex_content)),
            'points': 0,
            'won': bool(sorted_players)
        }
    
    def _create_flex_message(self, alt_text: str, contents: dict):
        """إنشاء Flex Message LINE"""
        if not alt_text:
            alt_text = "رسالة"
        return FlexMessage(alt_text=alt_text, contents=FlexContainer.from_dict(contents))
    
    def _create_text_message(self, text: str):
        """إنشاء رسالة نصية LINE"""
        if not text or not text.strip():
            text = "رسالة فارغة"
        return TextMessage(text=text)
    
    def _create_flex_with_buttons(self, alt_text: str, flex_content: dict):
        """إنشاء Flex Message مع أزرار اللعب - Neumorphism"""
        colors = self.get_theme_colors()
        
        # إضافة footer إذا لم يكن موجوداً
        if "footer" not in flex_content:
            flex_content["footer"] = {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "text",
                        "text": "الأوامر المتاحة:",
                        "size": "xs",
                        "weight": "bold",
                        "color": colors["text"]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "spacing": "sm",
                        "contents": [
                            {
                                "type": "button",
                                "action": {"type": "message", "label": "لمح", "text": "لمح"},
                                "style": "secondary",
                                "height": "sm",
                                "color": colors["shadow1"]
                            },
                            {
                                "type": "button",
                                "action": {"type": "message", "label": "جاوب", "text": "جاوب"},
                                "style": "secondary",
                                "height": "sm",
                                "color": colors["shadow1"]
                            }
                        ]
                    },
                    {
                        "type": "button",
                        "action": {"type": "message", "label": "إيقاف", "text": "إيقاف"},
                        "style": "primary",
                        "color": "#FF5555",
                        "height": "sm"
                    },
                    {"type": "separator", "color": colors["shadow1"]},
                    {
                        "type": "text",
                        "text": "تم إنشاؤه بواسطة عبير الدوسري © 2025",
                        "size": "xxs",
                        "color": colors["text2"],
                        "align": "center"
                    }
                ],
                "backgroundColor": colors["bg"],
                "paddingAll": "15px"
            }
        
        # تأكد من وجود styles
        if "styles" not in flex_content:
            flex_content["styles"] = {}
        flex_content["styles"]["footer"] = {"backgroundColor": colors["bg"]}
        
        return self._create_flex_message(alt_text, flex_content)
    
    def build_question_flex(self, title: str, question: str, extra_info: str = "", progress: str = ""):
        """بناء Flex Message للسؤال - Neumorphism Enhanced"""
        colors = self.get_theme_colors()
        
        header_contents = [
            {
                "type": "text",
                "text": title,
                "weight": "bold",
                "size": "xl",
                "color": colors["text"],
                "align": "center"
            }
        ]
        
        if progress:
            header_contents.append({
                "type": "text",
                "text": progress,
                "size": "sm",
                "color": colors["text2"],
                "align": "center"
            })
        
        body_contents = [
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": question,
                        "size": "lg",
                        "color": colors["text"],
                        "wrap": True,
                        "weight": "bold",
                        "align": "center"
                    }
                ],
                "backgroundColor": colors["card"],
                "cornerRadius": "20px",
                "paddingAll": "25px"
            }
        ]
        
        if extra_info:
            body_contents.append({
                "type": "text",
                "text": extra_info,
                "size": "sm",
                "color": colors["text2"],
                "align": "center",
                "wrap": True
            })
        
        flex_content = {
            "type": "bubble",
            "size": "kilo",
            "header": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": header_contents,
                "backgroundColor": colors["bg"],
                "paddingAll": "20px"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "lg",
                "contents": body_contents,
                "backgroundColor": colors["bg"],
                "paddingAll": "20px"
            },
            "styles": {
                "body": {"backgroundColor": colors["bg"]},
                "header": {"backgroundColor": colors["bg"]}
            }
        }
        
        return self._create_flex_with_buttons(title, flex_content)
