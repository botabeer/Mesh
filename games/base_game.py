"""
Bot Mesh - Enhanced Base Game Class
Created by: Abeer Aldosari © 2025

Features:
- Neumorphism Soft Design with 9 themes
- Smart progress tracking with visual indicators
- Flexible hint/reveal system
- Smooth animations support
- RTL text normalization
- Performance optimized
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Set, List
from dataclasses import dataclass
from datetime import datetime
import re
import logging

from linebot.v3.messaging import TextMessage, FlexMessage, FlexContainer

logger = logging.getLogger(__name__)

@dataclass
class PlayerScore:
    """Player score data structure"""
    user_id: str
    display_name: str
    points: int = 0
    correct: int = 0
    start_time: datetime = None
    
    def __post_init__(self):
        if self.start_time is None:
            self.start_time = datetime.now()


class BaseGame(ABC):
    """
    Enhanced base class for all games
    
    Features:
    - Theme support with 9 Neumorphism themes
    - Progress bar visualization
    - Smart answer normalization
    - Hint and reveal system
    - Score tracking per player
    - Game state management
    """
    
    def __init__(self, line_bot_api, questions_count: int = 5, rounds: int = None):
        """
        Initialize game
        
        Args:
            line_bot_api: LINE Bot API instance
            questions_count: Number of questions/rounds
            rounds: Deprecated, use questions_count
        """
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
        
        logger.info(f"🎮 Game initialized: {self.__class__.__name__}")
    
    @abstractmethod
    def start_game(self) -> Any:
        """Start game and return first question"""
        pass
    
    @abstractmethod
    def check_answer(self, answer: str, uid: str, name: str) -> Optional[Dict[str, Any]]:
        """Check player's answer"""
        pass
    
    def generate_question(self) -> Any:
        """Generate new question (optional override)"""
        pass
    
    def get_question(self) -> Any:
        """Get current question (optional override)"""
        pass
    
    def set_theme(self, theme_emoji: str):
        """Set game theme"""
        if theme_emoji in self.get_available_themes():
            self.theme = theme_emoji
            logger.debug(f"🎨 Theme set to {theme_emoji}")
    
    def get_available_themes(self) -> List[str]:
        """Get list of available themes"""
        return ["💜", "💚", "🤍", "🖤", "💙", "🩶", "🩷", "🧡", "🤎"]
    
    def get_theme_colors(self) -> Dict[str, str]:
        """Get current theme colors - Neumorphism Soft Design"""
        themes = {
            "💜": {
                "name": "Purple Dream",
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
                "name": "Green Nature",
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
                "name": "Clean White",
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
                "name": "Dark Mode",
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
                "name": "Ocean Blue",
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
                "name": "Silver Gray",
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
                "name": "Pink Blossom",
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
                "name": "Sunset Orange",
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
                "name": "Earth Brown",
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
    
    def get_progress_bar(self) -> Dict:
        """
        Generate professional progress bar
        
        Returns:
            Flex box containing progress visualization
        """
        colors = self.get_theme_colors()
        progress_boxes = []
        
        for i in range(self.questions_count):
            if i < self.current_question:
                # Completed - Green
                bg_color = "#10B981"
            elif i == self.current_question:
                # Current - Theme primary
                bg_color = colors["primary"]
            else:
                # Upcoming - Light gray
                bg_color = "#E5E7EB"
            
            progress_boxes.append({
                "type": "box",
                "layout": "vertical",
                "contents": [],
                "width": f"{100//self.questions_count}%",
                "height": "6px",
                "backgroundColor": bg_color,
                "cornerRadius": "3px"
            })
        
        return {
            "type": "box",
            "layout": "horizontal",
            "contents": progress_boxes,
            "spacing": "xs"
        }
    
    def normalize_text(self, text: str) -> str:
        """
        Normalize Arabic text for comparison
        
        Handles:
        - Diacritics removal
        - Hamza normalization (أ، إ، آ → ا)
        - Ta marbuta normalization (ة → ه)
        - Alef maksura normalization (ى → ي)
        - Whitespace normalization
        
        Args:
            text: Input text
            
        Returns:
            Normalized text
        """
        if not text:
            return ""
        
        # Remove diacritics
        text = re.sub(r'[\u0617-\u061A\u064B-\u0652]', '', text)
        
        # Normalize hamza variations
        text = re.sub(r'[أإآ]', 'ا', text)
        
        # Normalize ta marbuta
        text = re.sub(r'[ة]', 'ه', text)
        
        # Normalize alef maksura and hamza on ya
        text = re.sub(r'[ىئ]', 'ي', text)
        
        # Normalize whitespace
        text = ' '.join(text.split()).strip()
        
        return text.lower()
    
    def add_score(self, uid: str, name: str, pts: int) -> int:
        """
        Add points to player
        
        Args:
            uid: User ID
            name: Display name
            pts: Points to add
            
        Returns:
            Points added
        """
        if uid not in self.scores:
            self.scores[uid] = PlayerScore(uid, name)
        
        self.scores[uid].points += pts
        self.scores[uid].correct += 1
        self.answered_users.add(uid)
        
        logger.debug(f"⭐ {name} earned {pts} points (total: {self.scores[uid].points})")
        return pts
    
    def get_hint(self) -> str:
        """
        Get hint for current question
        
        Returns:
            Hint text
        """
        if not self.supports_hint:
            return "❌ هذه اللعبة لا تدعم التلميحات"
        
        if not self.current_answer:
            return "💡 لا يوجد تلميح متاح"
        
        answer_str = str(self.current_answer).strip()
        
        # Handle list answers (multiple correct answers)
        if isinstance(self.current_answer, list):
            answer_str = str(self.current_answer[0]).strip()
        
        first_char = answer_str[0] if answer_str else "؟"
        length = len(answer_str)
        
        return f"💡 تلميح: يبدأ بـ '{first_char}' وطوله {length} أحرف"
    
    def reveal_answer(self) -> str:
        """
        Reveal correct answer
        
        Returns:
            Answer text
        """
        if not self.supports_reveal:
            return "❌ هذه اللعبة لا تدعم كشف الإجابة"
        
        if isinstance(self.current_answer, list):
            answers = " أو ".join(str(a) for a in self.current_answer)
            return f"📝 الإجابة الصحيحة: {answers}"
        
        return f"📝 الإجابة الصحيحة: {self.current_answer}"
    
    def next_question(self) -> Any:
        """
        Move to next question
        
        Returns:
            Next question or end game dict
        """
        self.current_question += 1
        self.current_round += 1
        self.answered_users.clear()
        
        if self.current_question >= self.questions_count:
            return self.end_game()
        
        try:
            return self.get_question()
        except Exception as e:
            logger.error(f"❌ Error getting next question: {e}")
            return self.end_game()
    
    def end_game(self) -> Dict[str, Any]:
        """
        End game and show results
        
        Returns:
            Game over dict with results
        """
        self.game_active = False
        sorted_players = sorted(
            self.scores.values(),
            key=lambda x: x.points,
            reverse=True
        )
        
        colors = self.get_theme_colors()
        
        if sorted_players:
            winner = sorted_players[0]
            
            # Build player list
            players_list = []
            medals = ["🥇", "🥈", "🥉"]
            
            for i, player in enumerate(sorted_players[:5]):
                medal = medals[i] if i < 3 else f"{i+1}."
                medal_color = colors["primary"] if i < 3 else colors["text"]
                
                players_list.append({
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "text",
                            "text": medal,
                            "size": "lg",
                            "flex": 0,
                            "color": medal_color
                        },
                        {
                            "type": "text",
                            "text": player.display_name,
                            "size": "sm",
                            "color": colors["text"],
                            "flex": 3
                        },
                        {
                            "type": "text",
                            "text": f"{player.points}",
                            "size": "sm",
                            "color": colors["primary"],
                            "align": "end",
                            "flex": 1
                        }
                    ],
                    "spacing": "md"
                })
            
            flex_content = {
                "type": "bubble",
                "size": "kilo",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "xl",
                    "contents": [
                        {
                            "type": "text",
                            "text": "🎉 انتهت اللعبة",
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
                                    "text": "🏆 الفائز",
                                    "size": "sm",
                                    "color": colors["text2"],
                                    "align": "center"
                                },
                                {
                                    "type": "text",
                                    "text": winner.display_name,
                                    "size": "xl",
                                    "weight": "bold",
                                    "color": colors["text"],
                                    "align": "center"
                                },
                                {
                                    "type": "text",
                                    "text": f"⭐ {winner.points} نقطة",
                                    "size": "lg",
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
                            "cornerRadius": "15px",
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
                            "type": "box",
                            "layout": "horizontal",
                            "spacing": "sm",
                            "contents": [
                                {
                                    "type": "button",
                                    "action": {"type": "message", "label": "🏠 بداية", "text": "بداية"},
                                    "style": "secondary",
                                    "height": "sm"
                                },
                                {
                                    "type": "button",
                                    "action": {"type": "message", "label": "🎮 ألعاب", "text": "مساعدة"},
                                    "style": "primary",
                                    "height": "sm",
                                    "color": colors["primary"]
                                }
                            ]
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
            
            msg = f"🏆 الفائز: {winner.display_name} بـ {winner.points} نقطة"
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
        
        logger.info(f"🏁 Game ended: {msg}")
        
        return {
            'game_over': True,
            'message': msg,
            'response': FlexMessage(
                alt_text="نتيجة اللعبة",
                contents=FlexContainer.from_dict(flex_content)
            ),
            'points': 0,
            'won': bool(sorted_players)
        }
    
    def _create_flex_message(self, alt_text: str, contents: dict):
        """Create LINE Flex Message"""
        if not alt_text or not alt_text.strip():
            alt_text = "رسالة"
        return FlexMessage(alt_text=alt_text, contents=FlexContainer.from_dict(contents))
    
    def _create_text_message(self, text: str):
        """Create LINE Text Message"""
        if not text or not text.strip():
            text = "رسالة فارغة"
        return TextMessage(text=text)
    
    def _create_flex_with_buttons(self, alt_text: str, flex_content: dict):
        """
        Create Flex Message with game control buttons
        
        Args:
            alt_text: Alternative text for notification
            flex_content: Flex message content
            
        Returns:
            FlexMessage with footer buttons
        """
        colors = self.get_theme_colors()
        
        # Add footer if not exists
        if "footer" not in flex_content:
            button_contents = []
            
            # Add hint/reveal buttons if supported
            if self.supports_hint or self.supports_reveal:
                hint_reveal_row = {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "sm",
                    "contents": []
                }
                
                if self.supports_hint:
                    hint_reveal_row["contents"].append({
                        "type": "button",
                        "action": {"type": "message", "label": "💡 لمح", "text": "لمح"},
                        "style": "secondary",
                        "height": "sm",
                        "color": colors["shadow1"]
                    })
                
                if self.supports_reveal:
                    hint_reveal_row["contents"].append({
                        "type": "button",
                        "action": {"type": "message", "label": "📝 جاوب", "text": "جاوب"},
                        "style": "secondary",
                        "height": "sm",
                        "color": colors["shadow1"]
                    })
                
                button_contents.append(hint_reveal_row)
            
            # Stop button
            button_contents.append({
                "type": "button",
                "action": {"type": "message", "label": "⛔ إيقاف", "text": "إيقاف"},
                "style": "primary",
                "color": "#FF5555",
                "height": "sm"
            })
            
            flex_content["footer"] = {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": button_contents + [
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
        
        # Ensure styles exist
        if "styles" not in flex_content:
            flex_content["styles"] = {}
        
        flex_content["styles"]["footer"] = {"backgroundColor": colors["bg"]}
        
        return self._create_flex_message(alt_text, flex_content)
    
    def build_question_flex(
        self,
        title: str,
        question: str,
        extra_info: str = "",
        progress: str = "",
        include_progress_bar: bool = True
    ):
        """
        Build enhanced Flex Message for question
        
        Args:
            title: Question title/header
            question: Main question text
            extra_info: Additional information
            progress: Progress text (e.g., "1/5")
            include_progress_bar: Whether to show visual progress bar
            
        Returns:
            FlexMessage with question
        """
        colors = self.get_theme_colors()
        
        header_contents = []
        
        # Title row with progress
        if progress:
            header_contents.append({
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": title,
                        "weight": "bold",
                        "size": "lg",
                        "color": "#FFFFFF",
                        "flex": 0
                    },
                    {
                        "type": "text",
                        "text": progress,
                        "size": "sm",
                        "color": "#FFFFFF",
                        "align": "end"
                    }
                ]
            })
        else:
            header_contents.append({
                "type": "text",
                "text": title,
                "weight": "bold",
                "size": "xl",
                "color": "#FFFFFF",
                "align": "center"
            })
        
        # Progress bar
        if include_progress_bar:
            header_contents.append(self.get_progress_bar())
        
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
                "spacing": "md",
                "contents": header_contents,
                "backgroundColor": colors["primary"],
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
                "header": {"backgroundColor": colors["primary"]}
            }
        }
        
        return self._create_flex_with_buttons(title, flex_content)
    
    def get_game_info(self) -> Dict[str, Any]:
        """
        Get game information
        
        Returns:
            Game metadata dict
        """
        return {
            "class": self.__class__.__name__,
            "questions_count": self.questions_count,
            "current_question": self.current_question,
            "active": self.game_active,
            "players_count": len(self.scores),
            "theme": self.theme,
            "supports_hint": self.supports_hint,
            "supports_reveal": self.supports_reveal,
            "created_at": self.created_at.isoformat()
        }
