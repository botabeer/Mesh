"""
Bot Mesh - Scrambled Word Game
Created by: Abeer Aldosari © 2025

Unscramble the letters to form the correct word!
"""

import random
from games.base_game import BaseGame
from constants import POINTS_PER_CORRECT_ANSWER


class ScrambleWordGame(BaseGame):
    """Scrambled word game"""
    
    def __init__(self, line_bot_api):
        super().__init__(line_bot_api)
        self.game_name = "كلمة مبعثرة"
        self.game_icon = "🔤"
        
        # Word bank
        self.words = [
            "مدرسة", "كتاب", "قلم", "باب", "نافذة", "طاولة", "كرسي",
            "سيارة", "طائرة", "قطار", "سفينة", "دراجة",
            "تفاحة", "موز", "برتقال", "عنب", "بطيخ", "فراولة",
            "شمس", "قمر", "نجمة", "سماء", "بحر", "جبل", "نهر",
            "أسد", "نمر", "فيل", "زرافة", "حصان", "غزال",
            "ورد", "شجرة", "زهرة", "عشب", "ورقة",
            "منزل", "مسجد", "حديقة", "ملعب", "مطعم", "مكتبة",
            "صديق", "عائلة", "أخ", "أخت", "والد", "والدة",
            "كمبيوتر", "هاتف", "تلفاز", "ساعة", "راديو"
        ]
        
        self.used_words = []
    
    def scramble_word(self, word):
        """Scramble a word's letters"""
        letters = list(word)
        
        # Ensure scrambled is different from original
        attempts = 0
        while attempts < 10:
            random.shuffle(letters)
            scrambled = ''.join(letters)
            if scrambled != word:
                return scrambled
            attempts += 1
        
        # If still same, just reverse it
        return word[::-1]
    
    def next_question(self):
        """Generate next scrambled word"""
        if self.current_round > self.total_rounds:
            return None
        
        # Pick a word
        available = [w for w in self.words if w not in self.used_words]
        if not available:
            self.used_words = []
            available = self.words.copy()
        
        word = random.choice(available)
        self.used_words.append(word)
        
        scrambled = self.scramble_word(word)
        
        self.current_question = scrambled
        self.current_answer = word
        
        colors = self.get_colors()
        
        # Build card with letter boxes
        letter_boxes = []
        for i in range(0, len(scrambled), 4):
            chunk = scrambled[i:i+4]
            row = {
                "type": "box",
                "layout": "horizontal",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": letter,
                                "size": "xl",
                                "weight": "bold",
                                "color": colors["primary"],
                                "align": "center"
                            }
                        ],
                        "backgroundColor": colors["card"],
                        "cornerRadius": "15px",
                        "paddingAll": "15px",
                        "flex": 1
                    }
                    for letter in chunk
                ]
            }
            letter_boxes.append(row)
        
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
                "text": "🔄 رتب الحروف لتكوين كلمة صحيحة",
                "size": "md",
                "color": colors["text"],
                "weight": "bold",
                "align": "center",
                "wrap": True
            }
        ] + letter_boxes + [
            # Hint
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": f"💡 الكلمة مكونة من {len(word)} حروف",
                        "size": "sm",
                        "color": colors["text2"],
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
                "type": "button",
                "action": {"type": "message", "label": "⛔ إيقاف", "text": "إيقاف"},
                "style": "primary",
                "height": "sm",
                "color": "#FF5555"
            }
        ]
        
        from linebot.v3.messaging import FlexMessage, FlexContainer
        
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
        """Check word answer"""
        text = user_answer.strip()
        
        # Handle special commands
        if text == "لمح":
            hint = self.get_hint()
            return {
                'response': self.build_question_card(
                    self.current_question,
                    hint_text=f"تلميح: {hint}"
                ),
                'points': 0,
                'game_over': False
            }
        
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
        """Get word hint"""
        if not self.current_answer or len(self.current_answer) < 2:
            return "فكر جيداً"
        
        # Show first and last letter
        return f"تبدأ بـ {self.current_answer[0]} وتنتهي بـ {self.current_answer[-1]}"
