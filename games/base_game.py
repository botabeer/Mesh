"""
Bot Mesh - Base Game Class (Enhanced & Fixed)
Created by: Abeer Aldosari © 2025
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Set
from dataclasses import dataclass
from datetime import datetime
import re
import logging

# LINE SDK v3 imports
from linebot.v3.messaging import TextMessage, FlexMessage, FlexContainer

logger = logging.getLogger(__name__)


@dataclass
class PlayerScore:
    user_id: str
    display_name: str
    points: int = 0
    correct: int = 0


class BaseGame(ABC):
    def __init__(self, line_bot_api, questions_count: int = 10, rounds: int = None):
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
        self.theme = "white"
        self.supports_hint = True
        self.supports_reveal = True
    
    @abstractmethod
    def start_game(self) -> Any:
        """Start the game and return first question"""
        pass
    
    @abstractmethod
    def check_answer(self, answer: str, uid: str, name: str) -> Optional[Dict[str, Any]]:
        """Check player answer"""
        pass
    
    def generate_question(self) -> Any:
        """Generate a new question - override in subclass if needed"""
        pass
    
    def get_question(self) -> Any:
        """Get current question - override in subclass if needed"""
        pass
    
    def set_theme(self, theme_name: str):
        """Set game theme"""
        self.theme = theme_name
    
    def get_theme_colors(self):
        """Get current theme colors"""
        themes_config = {
            "white": {
                "bg": "#F8F9FA",
                "card": "#FFFFFF",
                "primary": "#667EEA",
                "text": "#2D3748",
                "text2": "#718096"
            },
            "purple": {
                "bg": "#F3E8FF",
                "card": "#FAF5FF",
                "primary": "#9F7AEA",
                "text": "#44337A",
                "text2": "#6B46C1"
            },
            "green": {
                "bg": "#E6FFFA",
                "card": "#F0FFF4",
                "primary": "#38B2AC",
                "text": "#234E52",
                "text2": "#2C7A7B"
            },
            "black": {
                "bg": "#1A202C",
                "card": "#2D3748",
                "primary": "#667EEA",
                "text": "#E2E8F0",
                "text2": "#CBD5E0"
            },
            "blue": {
                "bg": "#EBF8FF",
                "card": "#BEE3F8",
                "primary": "#3182CE",
                "text": "#2C5282",
                "text2": "#2B6CB0"
            },
            "gray": {
                "bg": "#F7FAFC",
                "card": "#EDF2F7",
                "primary": "#718096",
                "text": "#2D3748",
                "text2": "#4A5568"
            },
            "pink": {
                "bg": "#FFF5F7",
                "card": "#FED7E2",
                "primary": "#D53F8C",
                "text": "#702459",
                "text2": "#97266D"
            },
            "orange": {
                "bg": "#FFFAF0",
                "card": "#FEEBC8",
                "primary": "#DD6B20",
                "text": "#7C2D12",
                "text2": "#C05621"
            },
            "brown": {
                "bg": "#F7F3EF",
                "card": "#EDE0D4",
                "primary": "#8B4513",
                "text": "#5C2E00",
                "text2": "#7A4F1D"
            }
        }
        
        # تحويل الثيم من emoji إلى اسم
        theme_map = {
            "💜": "purple",
            "💚": "green",
            "🤍": "white",
            "🖤": "black",
            "💙": "blue",
            "🩶": "gray",
            "🩷": "pink",
            "🧡": "orange",
            "🤎": "brown"
        }
        
        theme_name = theme_map.get(self.theme, "white")
        return themes_config.get(theme_name, themes_config["white"])
    
    def normalize_text(self, text: str) -> str:
        """Normalize Arabic text"""
        if not text:
            return ""
        t = re.sub(r'[\u0617-\u061A\u064B-\u0652]', '', text)
        t = re.sub(r'[إأآا]', 'ا', t)
        t = re.sub(r'[ة]', 'ه', t)
        t = re.sub(r'[ىئ]', 'ي', t)
        return ' '.join(t.split()).strip()
    
    def add_score(self, uid: str, name: str, pts: int) -> int:
        """Add score for a player"""
        if uid not in self.scores:
            self.scores[uid] = PlayerScore(uid, name)
        self.scores[uid].points += pts
        self.scores[uid].correct += 1
        self.answered_users.add(uid)
        return pts
    
    def add_player_score(self, uid: str, pts: int):
        """Add points to player (compatibility method)"""
        if uid in self.scores:
            self.scores[uid].points += pts
        else:
            self.scores[uid] = PlayerScore(uid, "Player", pts, 1)
    
    def get_hint(self) -> str:
        """Get hint for current answer"""
        if not self.current_answer:
            return "لا يوجد تلميح"
        a = str(self.current_answer).strip()
        first_char = a[0] if a else "؟"
        length = len(a)
        return f"💡 تلميح: أول حرف '{first_char}' وعدد الحروف {length}"
    
    def reveal_answer(self) -> str:
        """Reveal the correct answer"""
        return f"📝 الإجابة: {self.current_answer}"
    
    def next_question(self) -> Any:
        """Move to next question"""
        self.current_question += 1
        self.current_round += 1
        self.answered_users.clear()
        
        if self.current_question >= self.questions_count:
            return self.end_game()
        
        try:
            return self.get_question()
        except:
            try:
                return self.generate_question()
            except:
                return self.end_game()
    
    def end_game(self) -> Dict[str, Any]:
        """End the game and show results"""
        self.game_active = False
        
        sorted_players = sorted(self.scores.values(), key=lambda x: x.points, reverse=True)
        
        msg = "🏁 انتهت اللعبة\n" + "─" * 20 + "\n\n"
        
        if sorted_players:
            msg += "🏆 النتائج:\n\n"
            medals = ["🥇", "🥈", "🥉"]
            for i, p in enumerate(sorted_players[:10]):
                medal = medals[i] if i < 3 else f"{i+1}."
                msg += f"{medal} {p.display_name}: {p.points} نقطة\n"
            msg += f"\n🎉 مبروك {sorted_players[0].display_name}!"
        else:
            msg += "لم يشارك أحد في اللعبة"
        
        return {
            'game_over': True,
            'message': msg,
            'response': self._create_text_message(msg),
            'points': 0,
            'won': bool(sorted_players)
        }
    
    def _create_text_message(self, text: str):
        """Create LINE text message (SDK v3)"""
        if not text or not text.strip():
            text = "رسالة فارغة"
        return TextMessage(text=text)
    
    def _create_flex_message(self, alt_text: str, contents: dict):
        """Create LINE Flex message (SDK v3)"""
        if not alt_text:
            alt_text = "رسالة"
        return FlexMessage(
            altText=alt_text,
            contents=FlexContainer.from_dict(contents)
        )
    
    def _create_flex_with_buttons(self, alt_text: str, flex_content: dict):
        """Create Flex message with fixed buttons"""
        # إضافة أزرار ثابتة إذا لم تكن موجودة
        if "footer" not in flex_content:
            colors = self.get_theme_colors()
            flex_content["footer"] = {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "button",
                        "action": {
                            "type": "message",
                            "label": "إيقاف",
                            "text": "إيقاف"
                        },
                        "style": "secondary",
                        "height": "sm"
                    },
                    {
                        "type": "button",
                        "action": {
                            "type": "message",
                            "label": "Home",
                            "text": "Home"
                        },
                        "style": "primary",
                        "height": "sm"
                    }
                ],
                "spacing": "sm",
                "margin": "md"
            }
        
        return self._create_flex_message(alt_text, flex_content)
    
    def build_question_flex(self, title: str, question: str, extra_info: str = ""):
        """Build modern 3D question Flex message"""
        colors = self.get_theme_colors()
        
        flex_content = {
            "type": "bubble",
            "size": "kilo",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": title,
                        "weight": "bold",
                        "size": "xl",
                        "color": "#FFFFFF",
                        "align": "center"
                    },
                    {
                        "type": "text",
                        "text": f"الجولة {self.current_round + 1}/{self.rounds}",
                        "size": "sm",
                        "color": "#FFFFFF",
                        "align": "center",
                        "margin": "sm"
                    }
                ],
                "backgroundColor": colors["primary"],
                "paddingAll": "20px"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
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
                ] + ([{
                    "type": "text",
                    "text": extra_info,
                    "size": "sm",
                    "color": colors["text2"],
                    "align": "center",
                    "margin": "lg",
                    "wrap": True
                }] if extra_info else []),
                "backgroundColor": colors["bg"],
                "paddingAll": "20px"
            },
            "styles": {
                "body": {
                    "backgroundColor": colors["bg"]
                },
                "header": {
                    "backgroundColor": colors["primary"]
                }
            }
        }
        
        return self._create_flex_with_buttons(title, flex_content)
    
    def build_result_flex(self, player_name: str, result_text: str, points: int, is_final: bool = False):
        """Build modern 3D result Flex message"""
        colors = self.get_theme_colors()
        
        status_color = colors["primary"] if points > 0 else "#EF4444"
        status_text = "✅ صحيح" if points > 0 else "انتهت اللعبة"
        
        flex_content = {
            "type": "bubble",
            "size": "kilo",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": status_text,
                        "weight": "bold",
                        "size": "xxl",
                        "color": "#FFFFFF",
                        "align": "center"
                    }
                ],
                "backgroundColor": status_color,
                "paddingAll": "20px"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": player_name,
                                "size": "lg",
                                "weight": "bold",
                                "color": colors["text"],
                                "align": "center"
                            },
                            {
                                "type": "separator",
                                "margin": "md"
                            },
                            {
                                "type": "text",
                                "text": result_text,
                                "size": "md",
                                "color": colors["text2"],
                                "wrap": True,
                                "align": "center",
                                "margin": "md"
                            },
                            {
                                "type": "text",
                                "text": f"النقاط: +{points}",
                                "size": "lg",
                                "color": colors["primary"],
                                "weight": "bold",
                                "align": "center",
                                "margin": "md"
                            }
                        ],
                        "backgroundColor": colors["card"],
                        "cornerRadius": "20px",
                        "paddingAll": "20px"
                    }
                ],
                "backgroundColor": colors["bg"],
                "paddingAll": "20px"
            }
        }
        
        return self._create_flex_with_buttons("نتيجة", flex_content)
