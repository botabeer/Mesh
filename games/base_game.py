"""
Bot Mesh - Base Game with AI Support & Dynamic Themes (Fixed for SDK v3)
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
        from config import THEMES
        return THEMES.get(self.theme, THEMES["white"])
    
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
    
    def get_hint(self) -> str:
        """Get hint for current answer"""
        if not self.current_answer:
            return "💡 لا يوجد تلميح"
        a = str(self.current_answer).strip()
        first_char = a[0]
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
        
        # Try to generate next question
        try:
            return self.get_question()
        except:
            return self.generate_question()
    
    def end_game(self) -> Dict[str, Any]:
        """End the game and show results"""
        self.game_active = False
        
        sorted_players = sorted(self.scores.values(), key=lambda x: x.points, reverse=True)
        
        msg = "🏁 انتهت اللعبة!\n" + "═" * 20 + "\n\n"
        
        if sorted_players:
            msg += "🏆 النتائج:\n\n"
            medals = ["🥇", "🥈", "🥉"]
            for i, p in enumerate(sorted_players[:10]):
                medal = medals[i] if i < 3 else f"{i+1}."
                msg += f"{medal} {p.display_name}: {p.points} نقطة\n"
            msg += f"\n🎉 مبروك {sorted_players[0].display_name}!"
        else:
            msg += "لم يشارك أحد"
        
        return {
            'game_over': True,
            'message': msg,
            'response': self._create_text_message(msg),
            'points': 0,
            'won': bool(sorted_players)
        }
    
    def _create_text_message(self, text: str):
        """Create LINE text message (SDK v3)"""
        return TextMessage(text=text)
    
    def _create_flex_message(self, alt_text: str, contents: dict):
        """Create LINE Flex message (SDK v3)"""
        return FlexMessage(
            altText=alt_text,
            contents=FlexContainer.from_dict(contents)
        )
    
    def _create_flex_with_buttons(self, alt_text: str, flex_content: dict):
        """Create Flex Message with hint/reveal buttons"""
        colors = self.get_theme_colors()
        
        if self.supports_hint or self.supports_reveal:
            buttons = []
            if self.supports_hint:
                buttons.append({
                    "type": "button",
                    "action": {"type": "message", "label": "💡 لمح", "text": "لمح"},
                    "style": "secondary",
                    "color": colors.get("card", "#F1F5F9"),
                    "height": "sm"
                })
            if self.supports_reveal:
                buttons.append({
                    "type": "button",
                    "action": {"type": "message", "label": "📝 جاوب", "text": "جاوب"},
                    "style": "primary",
                    "color": colors.get("primary", "#667EEA"),
                    "height": "sm"
                })
            
            if "body" in flex_content and "contents" in flex_content["body"]:
                flex_content["body"]["contents"].append({
                    "type": "box",
                    "layout": "horizontal",
                    "contents": buttons,
                    "spacing": "md",
                    "margin": "xl"
                })
        
        return self._create_flex_message(alt_text, flex_content)
    
    def build_question_flex(self, title: str, question: str, extra_info: str = ""):
        """Build question Flex message (compatibility method)"""
        colors = self.get_theme_colors()
        
        contents = [
            {
                "type": "text",
                "text": title,
                "weight": "bold",
                "size": "xl",
                "color": colors["primary"],
                "align": "center"
            },
            {
                "type": "separator",
                "margin": "md"
            },
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
                "paddingAll": "20px",
                "margin": "md"
            }
        ]
        
        if extra_info:
            contents.append({
                "type": "text",
                "text": extra_info,
                "size": "sm",
                "color": colors["text2"],
                "align": "center",
                "margin": "md",
                "wrap": True
            })
        
        # Add round info
        contents.append({
            "type": "text",
            "text": f"🎯 الجولة {self.current_round + 1}/{self.rounds}",
            "size": "sm",
            "color": colors["text2"],
            "align": "center",
            "margin": "md"
        })
        
        flex_content = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": contents,
                "paddingAll": "20px",
                "backgroundColor": colors["bg"]
            },
            "styles": {
                "body": {
                    "backgroundColor": colors["bg"]
                }
            }
        }
        
        return self._create_flex_with_buttons(title, flex_content)
    
    def build_result_flex(self, player_name: str, result_text: str, points: int, is_final: bool = False):
        """Build result Flex message (compatibility method)"""
        colors = self.get_theme_colors()
        
        status = "🎉 ممتاز!" if points > 0 else "❌ انتهت اللعبة"
        
        contents = [
            {
                "type": "text",
                "text": status,
                "weight": "bold",
                "size": "xl",
                "color": colors["primary"],
                "align": "center"
            },
            {
                "type": "separator",
                "margin": "md"
            },
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": f"👤 {player_name}",
                        "size": "md",
                        "color": colors["text"],
                        "margin": "md"
                    },
                    {
                        "type": "text",
                        "text": result_text,
                        "size": "md",
                        "color": colors["text2"],
                        "wrap": True,
                        "margin": "sm"
                    },
                    {
                        "type": "text",
                        "text": f"⭐ النقاط: +{points}",
                        "size": "md",
                        "color": colors["primary"],
                        "margin": "sm"
                    }
                ],
                "backgroundColor": colors["card"],
                "cornerRadius": "20px",
                "paddingAll": "20px",
                "margin": "md"
            }
        ]
        
        if is_final:
            # Show leaderboard
            sorted_players = sorted(self.scores.values(), key=lambda x: x.points, reverse=True)
            if sorted_players:
                contents.append({
                    "type": "separator",
                    "margin": "lg"
                })
                contents.append({
                    "type": "text",
                    "text": "🏆 النتائج النهائية",
                    "size": "lg",
                    "weight": "bold",
                    "color": colors["primary"],
                    "align": "center",
                    "margin": "md"
                })
                
                medals = ["🥇", "🥈", "🥉"]
                for i, p in enumerate(sorted_players[:3]):
                    medal = medals[i]
                    contents.append({
                        "type": "text",
                        "text": f"{medal} {p.display_name}: {p.points} نقطة",
                        "size": "sm",
                        "color": colors["text"],
                        "margin": "sm"
                    })
        
        flex_content = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": contents,
                "paddingAll": "20px",
                "backgroundColor": colors["bg"]
            },
            "styles": {
                "body": {
                    "backgroundColor": colors["bg"]
                }
            }
        }
        
        return self._create_flex_message("النتيجة", flex_content)
    
    def __str__(self):
        return f"{self.__class__.__name__}(round={self.current_round}/{self.rounds}, players={len(self.scores)})"
