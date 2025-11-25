"""
Bot Mesh - Math Game with AI Support
Created by: Abeer Aldosari © 2025
"""

import random
from games.base_game import BaseGame
from constants import POINTS_PER_CORRECT_ANSWER


class MathGame(BaseGame):
    """Math puzzles game"""
    
    def __init__(self, line_bot_api):
        super().__init__(line_bot_api)
        self.game_name = "رياضيات"
        self.game_icon = "🔢"
        
        # AI functions
        self.ai_generate_question = None
        self.ai_check_answer = None
        
        # Difficulty levels by round
        self.difficulty = {
            1: (1, 20),    # Easy
            2: (10, 50),   # Medium
            3: (20, 100),  # Hard
            4: (50, 200),  # Very Hard
            5: (100, 500)  # Expert
        }
    
    def generate_math_question(self):
        """Generate math question"""
        min_num, max_num = self.difficulty.get(self.current_round, (1, 50))
        
        operations = ['+', '-', '*']
        weights = [0.4, 0.3, 0.3]  # More addition, less multiplication
        
        op = random.choices(operations, weights=weights)[0]
        
        if op == '+':
            a = random.randint(min_num, max_num)
            b = random.randint(min_num, max_num)
            question = f"{a} + {b} = ؟"
            answer = a + b
        
        elif op == '-':
            a = random.randint(min_num + 10, max_num)
            b = random.randint(min_num, a - 1)
            question = f"{a} - {b} = ؟"
            answer = a - b
        
        else:  # *
            a = random.randint(2, min(max_num // 10, 20))
            b = random.randint(2, min(max_num // 10, 20))
            question = f"{a} × {b} = ؟"
            answer = a * b
        
        return {"q": question, "a": str(answer)}
    
    def next_question(self):
        """Generate next math question"""
        if self.current_round > self.total_rounds:
            return None
        
        # Try AI generation
        question_data = None
        if self.ai_generate_question:
            try:
                question_data = self.ai_generate_question()
            except:
                pass
        
        # Fallback to generated questions
        if not question_data:
            question_data = self.generate_math_question()
        
        # Extract question and answer
        if "q" in question_data and "a" in question_data:
            self.current_question = question_data["q"]
            self.current_answer = str(question_data["a"])
        elif "question" in question_data and "answer" in question_data:
            self.current_question = question_data["question"]
            self.current_answer = str(question_data["answer"])
        else:
            q = self.generate_math_question()
            self.current_question = q["q"]
            self.current_answer = q["a"]
        
        # Build card with difficulty indicator
        difficulty_text = [
            "سهل",
            "متوسط", 
            "صعب",
            "صعب جداً",
            "خبير"
        ][self.current_round - 1]
        
        return self.build_question_card(
            self.current_question,
            hint_text=f"المستوى: {difficulty_text}"
        )
    
    def check_answer(self, user_answer, user_id, username):
        """Check math answer"""
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
        
        # Check if answer is numeric
        is_correct = False
        try:
            user_num = int(text.replace('،', '').replace(',', ''))
            correct_num = int(self.current_answer)
            is_correct = user_num == correct_num
        except:
            # Try AI validation
            if self.ai_check_answer:
                try:
                    is_correct = self.ai_check_answer(self.current_answer, text)
                except:
                    pass
        
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
        """Get math hint"""
        try:
            answer = int(self.current_answer)
            
            # Show if even/odd
            if answer % 2 == 0:
                return "العدد زوجي"
            else:
                return "العدد فردي"
        except:
            return "فكر جيداً"
