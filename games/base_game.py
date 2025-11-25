"""
Bot Mesh - Base Game Class
Created by: Abeer Aldosari © 2025

All games inherit from this base class
"""

from linebot.v3.messaging import FlexMessage, FlexContainer
from constants import (
    THEMES, DEFAULT_THEME, BOT_RIGHTS, ROUNDS_PER_GAME,
    POINTS_PER_CORRECT_ANSWER, normalize_arabic
)


class BaseGame:
    """Base class for all games"""
    
    def __init__(self, line_bot_api):
        self.line_bot_api = line_bot_api
        self.theme = DEFAULT_THEME
        self.current_round = 0
        self.total_rounds = ROUNDS_PER_GAME
        self.score = 0
        self.current_question = None
        self.current_answer = None
        self.game_name = "لعبة"
        self.game_icon = "🎮"
        
    def set_theme(self, theme):
        """Set game theme"""
        self.theme = theme if theme in THEMES else DEFAULT_THEME
    
    def get_colors(self):
        """Get current theme colors"""
        return THEMES.get(self.theme, THEMES[DEFAULT_THEME])
    
    def start_game(self):
        """Start the game - override in child classes"""
        self.current_round = 1
        self.score = 0
        return self.next_question()
    
    def next_question(self):
        """Generate next question - override in child classes"""
        raise NotImplementedError("Must implement next_question()")
    
    def check_answer(self, user_answer, user_id, username):
        """Check user answer - override in child classes"""
        raise NotImplementedError("Must implement check_answer()")
    
    def normalize_answer(self, text):
        """Normalize answer for comparison"""
        return normalize_arabic(text)
    
    def build_question_card(self, question_text, hint_text=None, additional_contents=None):
        """Build question card with neumorphic design"""
        colors = self.get_colors()
        
        contents = [
            # Game Header
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": f"{self.game_icon} {self.game_name}",
                        "weight": "bold",
                        "size": "lg",
                        "color": colors["primary"],
                        "flex": 3
                    },
                    {
                        "type": "text",
                        "text": f"سؤال {self.current_round} من {self.total_rounds}",
                        "size": "sm",
                        "color": colors["text2"],
                        "align": "end",
                        "flex": 2
                    }
                ]
            },
            {"type": "separator", "color": colors["shadow1"]},
            
            # Question Card
            {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": [
                    {
                        "type": "text",
                        "text": question_text,
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
        
        # Add hint if provided
        if hint_text:
            contents.append({
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": f"💡 {hint_text}",
                        "size": "sm",
                        "color": colors["text2"],
                        "wrap": True,
                        "align": "center"
                    }
                ],
                "backgroundColor": colors["card"],
                "cornerRadius": "15px",
                "paddingAll": "15px"
            })
        
        # Add additional contents
        if additional_contents:
            contents.extend(additional_contents)
        
        # Score indicator
        contents.append({
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "text",
                    "text": f"⭐ النقاط: {self.score}",
                    "size": "sm",
                    "color": colors["primary"],
                    "weight": "bold"
                }
            ]
        })
        
        # Footer with action buttons
        footer = [
            {
                "type": "box",
                "layout": "horizontal",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "button",
                        "action": {"type": "message", "label": "💡 لمح", "text": "لمح"},
                        "style": "secondary",
                        "height": "sm",
                        "color": colors["shadow1"]
                    },
                    {
                        "type": "button",
                        "action": {"type": "message", "label": "🔍 جاوب", "text": "جاوب"},
                        "style": "secondary",
                        "height": "sm",
                        "color": colors["shadow1"]
                    }
                ]
            },
            {
                "type": "box",
                "layout": "horizontal",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "button",
                        "action": {"type": "message", "label": "⛔ إيقاف", "text": "إيقاف"},
                        "style": "primary",
                        "height": "sm",
                        "color": "#FF5555"
                    }
                ]
            },
            {"type": "separator", "color": colors["shadow1"]},
            {
                "type": "text",
                "text": BOT_RIGHTS,
                "size": "xxs",
                "color": colors["text2"],
                "align": "center"
            }
        ]
        
        card = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "lg",
                "contents": contents,
                "backgroundColor": colors["bg"],
                "paddingAll": "20px"
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": footer,
                "backgroundColor": colors["bg"],
                "paddingAll": "15px"
            },
            "styles": {
                "body": {"backgroundColor": colors["bg"]},
                "footer": {"backgroundColor": colors["bg"]}
            }
        }
        
        return FlexMessage(
            alt_text=f"{self.game_name} - {self.current_round}/{self.total_rounds}",
            contents=FlexContainer.from_dict(card)
        )
    
    def build_result_card(self, is_correct, correct_answer, message):
        """Build result card (correct/wrong answer)"""
        colors = self.get_colors()
        
        result_emoji = "✅" if is_correct else "❌"
        result_text = "إجابة صحيحة!" if is_correct else "إجابة خاطئة"
        result_color = "#48BB78" if is_correct else "#FF5555"
        
        contents = [
            {
                "type": "text",
                "text": f"{result_emoji} {result_text}",
                "weight": "bold",
                "size": "xl",
                "color": result_color,
                "align": "center"
            },
            {"type": "separator", "color": colors["shadow1"]},
            {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "text",
                        "text": message,
                        "size": "md",
                        "color": colors["text"],
                        "wrap": True,
                        "align": "center"
                    },
                    {
                        "type": "text",
                        "text": f"الإجابة الصحيحة: {correct_answer}",
                        "size": "sm",
                        "color": colors["text2"],
                        "wrap": True,
                        "align": "center"
                    } if not is_correct else None
                ],
                "backgroundColor": colors["card"],
                "cornerRadius": "20px",
                "paddingAll": "20px"
            },
            {
                "type": "text",
                "text": f"⭐ النقاط الحالية: {self.score}",
                "size": "md",
                "color": colors["primary"],
                "weight": "bold",
                "align": "center"
            }
        ]
        
        # Remove None values
        contents = [c for c in contents if c is not None]
        
        card = {
            "type": "bubble",
            "size": "kilo",
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "lg",
                "contents": contents,
                "backgroundColor": colors["bg"],
                "paddingAll": "20px"
            },
            "styles": {
                "body": {"backgroundColor": colors["bg"]}
            }
        }
        
        return FlexMessage(
            alt_text=result_text,
            contents=FlexContainer.from_dict(card)
        )
    
    def build_game_over_card(self, username, final_score):
        """Build game over card with replay option"""
        colors = self.get_colors()
        
        # Determine performance message
        if final_score == self.total_rounds * POINTS_PER_CORRECT_ANSWER:
            performance = "🏆 ممتاز! إجابات كاملة!"
            perf_color = "#D53F8C"
        elif final_score >= (self.total_rounds * POINTS_PER_CORRECT_ANSWER) * 0.6:
            performance = "⭐ أداء جيد جداً!"
            perf_color = "#667EEA"
        elif final_score >= (self.total_rounds * POINTS_PER_CORRECT_ANSWER) * 0.4:
            performance = "👍 أداء جيد"
            perf_color = "#48BB78"
        else:
            performance = "💪 حاول مرة أخرى"
            perf_color = "#DD6B20"
        
        contents = [
            {
                "type": "text",
                "text": f"🎉 انتهت اللعبة",
                "weight": "bold",
                "size": "xxl",
                "color": colors["primary"],
                "align": "center"
            },
            {"type": "separator", "color": colors["shadow1"]},
            {
                "type": "box",
                "layout": "vertical",
                "spacing": "lg",
                "contents": [
                    {
                        "type": "text",
                        "text": f"👤 {username}",
                        "size": "lg",
                        "color": colors["text"],
                        "weight": "bold",
                        "align": "center"
                    },
                    {
                        "type": "text",
                        "text": f"{final_score}",
                        "size": "xxl",
                        "weight": "bold",
                        "color": colors["primary"],
                        "align": "center"
                    },
                    {
                        "type": "text",
                        "text": "نقطة",
                        "size": "md",
                        "color": colors["text2"],
                        "align": "center"
                    }
                ],
                "backgroundColor": colors["card"],
                "cornerRadius": "20px",
                "paddingAll": "30px"
            },
            {
                "type": "text",
                "text": performance,
                "size": "lg",
                "color": perf_color,
                "weight": "bold",
                "align": "center"
            }
        ]
        
        footer = [
            {
                "type": "box",
                "layout": "horizontal",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "button",
                        "action": {
                            "type": "message",
                            "label": "🔄 إعادة اللعبة",
                            "text": f"لعبة {self.game_name}"
                        },
                        "style": "primary",
                        "height": "sm",
                        "color": colors["button"]
                    }
                ]
            },
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
                        "style": "secondary",
                        "height": "sm"
                    }
                ]
            },
            {"type": "separator", "color": colors["shadow1"]},
            {
                "type": "text",
                "text": BOT_RIGHTS,
                "size": "xxs",
                "color": colors["text2"],
                "align": "center"
            }
        ]
        
        card = {
            "type": "bubble",
            "size": "kilo",
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "xl",
                "contents": contents,
                "backgroundColor": colors["bg"],
                "paddingAll": "20px"
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": footer,
                "backgroundColor": colors["bg"],
                "paddingAll": "15px"
            },
            "styles": {
                "body": {"backgroundColor": colors["bg"]},
                "footer": {"backgroundColor": colors["bg"]}
            }
        }
        
        return FlexMessage(
            alt_text=f"انتهت اللعبة - {final_score} نقطة",
            contents=FlexContainer.from_dict(card)
        )
    
    def get_hint(self):
        """Get hint for current question - override if needed"""
        if not self.current_answer:
            return "لا يوجد تلميح متاح"
        
        answer = str(self.current_answer)
        hint_length = max(1, len(answer) // 2)
        return answer[:hint_length] + "..." 
    
    def reveal_answer(self):
        """Reveal the correct answer"""
        return f"الإجابة الصحيحة: {self.current_answer}"
