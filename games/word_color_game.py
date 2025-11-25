"""
Bot Mesh - Word Color Game (Stroop Effect)
Created by: Abeer Aldosari © 2025

The classic Stroop test - say the color, not the word!
"""

import random
from games.base_game import BaseGame
from constants import POINTS_PER_CORRECT_ANSWER


class WordColorGame(BaseGame):
    """Word Color Game - Name the color, not the word"""
    
    def __init__(self, line_bot_api):
        super().__init__(line_bot_api)
        self.game_name = "لون الكلمة"
        self.game_icon = "🎨"
        
        # Color mappings
        self.colors = {
            "أحمر": "#E53E3E",
            "أزرق": "#3182CE",
            "أخضر": "#38A169",
            "أصفر": "#D69E2E",
            "برتقالي": "#DD6B20",
            "بنفسجي": "#805AD5",
            "وردي": "#D53F8C",
            "بني": "#8B4513"
        }
        
        self.color_names = list(self.colors.keys())
    
    def next_question(self):
        """Generate next color question"""
        if self.current_round > self.total_rounds:
            return None
        
        # Pick word and color (usually different)
        word = random.choice(self.color_names)
        
        # 70% chance of mismatch to make it challenging
        if random.random() < 0.7:
            color_name = random.choice([c for c in self.color_names if c != word])
        else:
            color_name = word
        
        self.current_question = word
        self.current_answer = color_name
        color_hex = self.colors[color_name]
        
        colors = self.get_colors()
        
        # Build special card with colored text
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
            
            # Instruction
            {
                "type": "text",
                "text": "📝 ما لون هذه الكلمة؟",
                "size": "md",
                "color": colors["text"],
                "weight": "bold",
                "align": "center"
            },
            
            # Colored Word (BIG!)
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": word,
                        "size": "xxl",
                        "weight": "bold",
                        "color": color_hex,
                        "align": "center"
                    }
                ],
                "backgroundColor": colors["card"],
                "cornerRadius": "20px",
                "paddingAll": "30px"
            },
            
            # Warning
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "⚠️ اكتب اسم اللون، وليس الكلمة!",
                        "size": "sm",
                        "color": "#FF5555",
                        "wrap": True,
                        "align": "center"
                    }
                ],
                "backgroundColor": colors["card"],
                "cornerRadius": "15px",
                "paddingAll": "15px"
            },
            
            # Score
            {
                "type": "text",
                "text": f"⭐ النقاط: {self.score}",
                "size": "sm",
                "color": colors["primary"],
                "weight": "bold",
                "align": "center"
            }
        ]
        
        # Footer
        footer = [
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
            }
        ]
        
        from linebot.v3.messaging import FlexMessage, FlexContainer
        from constants import BOT_RIGHTS
        
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
    
    def check_answer(self, user_answer, user_id, username):
        """Check color answer"""
        text = user_answer.strip()
        
        # Handle special commands
        if text == "جاوب":
            return {
                'response': self.build_result_card(
                    False,
                    self.current_answer,
                    "تم كشف الإجابة"
                ),
                'points': 0,
                'game_over': False
            }
        
        # Check answer
        normalized_answer = self.normalize_answer(self.current_answer)
        normalized_user = self.normalize_answer(text)
        
        is_correct = normalized_user == normalized_answer
        
        # Update score
        if is_correct:
            self.score += POINTS_PER_CORRECT_ANSWER
        
        # Move to next round
        self.current_round += 1
        
        # Check if game over
        if self.current_round > self.total_rounds:
            return {
                'response': self.build_game_over_card(username, self.score),
                'points': POINTS_PER_CORRECT_ANSWER if is_correct else 0,
                'game_over': True
            }
        
        # Continue game
        next_q = self.next_question()
        
        return {
            'response': next_q,
            'points': POINTS_PER_CORRECT_ANSWER if is_correct else 0,
            'game_over': False
        }
    
    def get_hint(self):
        """No hints for this game"""
        return "ركز على اللون، وليس الكلمة!"
