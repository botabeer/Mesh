"""
Bot Mesh - Opposite Words Game with AI
Created by: Abeer Aldosari © 2025

Find the opposite of the given word!
"""

import random
from games.base_game import BaseGame
from constants import POINTS_PER_CORRECT_ANSWER


class OppositeGame(BaseGame):
    """Opposite words game"""
    
    def __init__(self, line_bot_api):
        super().__init__(line_bot_api)
        self.game_name = "عكس"
        self.game_icon = "↔️"
        
        # AI functions
        self.ai_generate_question = None
        self.ai_check_answer = None
        
        # Fallback opposite pairs
        self.opposites = [
            {"word": "كبير", "opposite": "صغير"},
            {"word": "طويل", "opposite": "قصير"},
            {"word": "سريع", "opposite": "بطيء"},
            {"word": "قوي", "opposite": "ضعيف"},
            {"word": "حار", "opposite": "بارد"},
            {"word": "نظيف", "opposite": "قذر"},
            {"word": "سهل", "opposite": "صعب"},
            {"word": "جميل", "opposite": "قبيح"},
            {"word": "غني", "opposite": "فقير"},
            {"word": "ثقيل", "opposite": "خفيف"},
            {"word": "عميق", "opposite": "ضحل"},
            {"word": "واسع", "opposite": "ضيق"},
            {"word": "مظلم", "opposite": "مضيء"},
            {"word": "رطب", "opposite": "جاف"},
            {"word": "قديم", "opposite": "جديد"},
            {"word": "بعيد", "opposite": "قريب"},
            {"word": "مرتفع", "opposite": "منخفض"},
            {"word": "مبكر", "opposite": "متأخر"},
            {"word": "فوق", "opposite": "تحت"},
            {"word": "داخل", "opposite": "خارج"}
        ]
        
        self.used_words = []
    
    def next_question(self):
        """Generate next opposite word question"""
        if self.current_round > self.total_rounds:
            return None
        
        # Try AI generation first
        question_data = None
        if self.ai_generate_question:
            try:
                question_data = self.ai_generate_question()
            except:
                pass
        
        # Fallback to static pairs
        if not question_data:
            available = [w for w in self.opposites if w not in self.used_words]
            if not available:
                self.used_words = []
                available = self.opposites.copy()
            
            question_data = random.choice(available)
            self.used_words.append(question_data)
        
        # Extract word and opposite
        if "word" in question_data and "opposite" in question_data:
            word = question_data["word"]
            opposite = question_data["opposite"]
        else:
            # Fallback
            q = random.choice(self.opposites)
            word = q["word"]
            opposite = q["opposite"]
        
        self.current_question = word
        self.current_answer = opposite
        
        colors = self.get_colors()
        
        # Build card with the word
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
                "text": "↔️ ما هو عكس هذه الكلمة؟",
                "size": "md",
                "color": colors["text"],
                "weight": "bold",
                "align": "center",
                "wrap": True
            },
            
            # The word
            {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": [
                    {
                        "type": "text",
                        "text": word,
                        "size": "xxl",
                        "color": colors["primary"],
                        "weight": "bold",
                        "align": "center"
                    }
                ],
                "backgroundColor": colors["card"],
                "cornerRadius": "20px",
                "paddingAll": "30px"
            },
            
            # Hint
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "💡 فكر في المعنى المعاكس تماماً",
                        "size": "sm",
                        "color": colors["text2"],
                        "align": "center",
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
        """Check opposite word with AI or string matching"""
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
        is_correct = False
        
        # Try AI validation first
        if self.ai_check_answer:
            try:
                is_correct = self.ai_check_answer(self.current_answer, text)
            except:
                pass
        
        # Fallback to string matching
        if not is_correct:
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
        """Get hint for opposite"""
        if not self.current_answer or len(self.current_answer) < 2:
            return "فكر في الضد"
        
        # Show first letter
        return f"يبدأ بحرف: {self.current_answer[0]}"
