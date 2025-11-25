"""
Bot Mesh - Fast Typing Game
Created by: Abeer Aldosari © 2025

Type the text exactly as shown!
"""

import random
from datetime import datetime
from games.base_game import BaseGame
from constants import POINTS_PER_CORRECT_ANSWER


class FastTypingGame(BaseGame):
    """Fast typing speed game"""
    
    def __init__(self, line_bot_api):
        super().__init__(line_bot_api)
        self.game_name = "كتابة سريعة"
        self.game_icon = "⚡"
        
        # Typing phrases
        self.phrases = [
            "السرعة والدقة مهمتان",
            "التركيز هو مفتاح النجاح",
            "الممارسة تصنع الإتقان",
            "الوقت من ذهب",
            "اكتب بسرعة ودقة",
            "التحدي يبدأ الآن",
            "هيا اثبت مهارتك",
            "السرعة مع الدقة",
            "لا تستسلم أبداً",
            "النجاح يحتاج صبر",
            "الإبداع لا حدود له",
            "كن الأفضل دائماً",
            "التميز هو هدفنا",
            "احلم واسعى وحقق",
            "المثابرة طريق النجاح"
        ]
        
        self.question_start_time = None
        self.used_phrases = []
    
    def next_question(self):
        """Generate next typing challenge"""
        if self.current_round > self.total_rounds:
            return None
        
        # Pick a phrase
        available = [p for p in self.phrases if p not in self.used_phrases]
        if not available:
            self.used_phrases = []
            available = self.phrases.copy()
        
        phrase = random.choice(available)
        self.used_phrases.append(phrase)
        
        self.current_question = phrase
        self.current_answer = phrase
        self.question_start_time = datetime.now()
        
        colors = self.get_colors()
        
        # Build card with phrase to type
        from linebot.v3.messaging import FlexMessage, FlexContainer
        from constants import BOT_RIGHTS
        
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
                "text": "⚡ اكتب النص التالي بالضبط:",
                "size": "md",
                "color": colors["text"],
                "weight": "bold",
                "align": "center",
                "wrap": True
            },
            
            # Phrase to type
            {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": [
                    {
                        "type": "text",
                        "text": phrase,
                        "size": "xl",
                        "color": colors["primary"],
                        "weight": "bold",
                        "align": "center",
                        "wrap": True
                    }
                ],
                "backgroundColor": colors["card"],
                "cornerRadius": "20px",
                "paddingAll": "25px"
            },
            
            # Tips
            {
                "type": "box",
                "layout": "vertical",
                "spacing": "xs",
                "contents": [
                    {
                        "type": "text",
                        "text": "💡 نصائح:",
                        "size": "sm",
                        "color": colors["text"],
                        "weight": "bold"
                    },
                    {
                        "type": "text",
                        "text": "• اكتب بدقة وسرعة\n• احذر من الأخطاء الإملائية\n• السرعة مهمة!",
                        "size": "xs",
                        "color": colors["text2"],
                        "wrap": True
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
    
    def check_answer(self, user_answer, user_id, username):
        """Check typing accuracy and speed"""
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
        
        # Calculate time taken
        time_taken = (datetime.now() - self.question_start_time).total_seconds() if self.question_start_time else 0
        
        # Check exact match
        is_correct = text == self.current_answer
        
        # Bonus for speed (under 5 seconds)
        speed_bonus = 5 if time_taken < 5 and is_correct else 0
        
        # Update score
        points_earned = 0
        if is_correct:
            points_earned = POINTS_PER_CORRECT_ANSWER + speed_bonus
            self.score += points_earned
        
        # Move to next round
        self.current_round += 1
        
        # Prepare message
        if is_correct and speed_bonus > 0:
            message = f"🎉 ممتاز! أنجزتها في {time_taken:.1f} ثانية!\n+{speed_bonus} نقاط إضافية للسرعة!"
        elif is_correct:
            message = f"✅ صحيح! الوقت: {time_taken:.1f} ثانية"
        else:
            message = f"❌ خطأ! راجع الكتابة بدقة"
        
        # Check if game over
        if self.current_round > self.total_rounds:
            return {
                'response': self.build_game_over_card(username, self.score),
                'points': points_earned,
                'game_over': True
            }
        
        # Continue game
        next_q = self.next_question()
        
        return {
            'response': next_q,
            'points': points_earned,
            'game_over': False
        }
    
    def get_hint(self):
        """No hints for this game"""
        return "اكتب النص بالضبط كما هو!"
