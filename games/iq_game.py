"""
Bot Mesh - IQ Game with AI Support
Created by: Abeer Aldosari © 2025

Features:
- Gemini AI question generation
- Fallback to static questions
- Smart answer validation
"""

import random
from games.base_game import BaseGame
from constants import POINTS_PER_CORRECT_ANSWER


class IqGame(BaseGame):
    """IQ/Logic puzzles game"""
    
    def __init__(self, line_bot_api):
        super().__init__(line_bot_api)
        self.game_name = "IQ"
        self.game_icon = "🧠"
        
        # AI functions (will be set by app.py)
        self.ai_generate_question = None
        self.ai_check_answer = None
        
        # Fallback questions
        self.fallback_questions = [
            {"q": "ما هو الشيء الذي يمشي بلا أرجل ويبكي بلا عيون؟", "a": "السحاب"},
            {"q": "له رأس ولا عين له؟", "a": "الدبوس"},
            {"q": "ما هو الشيء الذي إذا أكلته كله تستفيد وإذا أكلت نصفه تموت؟", "a": "السمسم"},
            {"q": "شيء موجود في السماء إذا أضفت إليه حرفا أصبح في الأرض؟", "a": "نجم"},
            {"q": "ما هو الشيء الذي كلما زاد نقص؟", "a": "العمر"},
            {"q": "ما هو الشيء الذي يكتب ولا يقرأ؟", "a": "القلم"},
            {"q": "ما هو الشيء الذي له أسنان ولا يعض؟", "a": "المشط"},
            {"q": "أنا في الماء ولكن إذا لمسني الماء أموت، من أنا؟", "a": "الملح"},
            {"q": "ما هو الشيء الذي يتحدث جميع لغات العالم؟", "a": "صدى الصوت"},
            {"q": "شيء يؤخذ منك قبل أن تعطيه؟", "a": "الصورة"},
            {"q": "ما هو الشيء الذي إذا دخل الماء لم يبتل؟", "a": "الضوء"},
            {"q": "رجل معه ست بنات لكل بنت أخ واحد، كم عدد أولاد الرجل؟", "a": "7"},
            {"q": "ما هو الشيء الذي يقرصك ولا تراه؟", "a": "الجوع"},
            {"q": "ما الذي يحترق دون أن يحترق؟", "a": "الشمعة"},
            {"q": "ما هو الشيء الذي كلما أخذت منه كبر؟", "a": "الحفرة"}
        ]
        
        self.used_questions = []
    
    def next_question(self):
        """Generate next question using AI or fallback"""
        if self.current_round > self.total_rounds:
            return None
        
        # Try AI generation first
        question_data = None
        if self.ai_generate_question:
            try:
                question_data = self.ai_generate_question()
            except Exception as e:
                print(f"AI generation failed: {e}")
        
        # Fallback to static questions
        if not question_data:
            available = [q for q in self.fallback_questions if q not in self.used_questions]
            if not available:
                self.used_questions = []
                available = self.fallback_questions.copy()
            
            question_data = random.choice(available)
            self.used_questions.append(question_data)
        
        # Handle different response formats
        if "q" in question_data and "a" in question_data:
            self.current_question = question_data["q"]
            self.current_answer = question_data["a"]
        elif "question" in question_data and "answer" in question_data:
            self.current_question = question_data["question"]
            self.current_answer = question_data["answer"]
        else:
            # Fallback
            q = random.choice(self.fallback_questions)
            self.current_question = q["q"]
            self.current_answer = q["a"]
        
        return self.build_question_card(
            self.current_question,
            hint_text="فكر جيداً قبل الإجابة"
        )
    
    def check_answer(self, user_answer, user_id, username):
        """Check user answer with AI or string matching"""
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
            is_correct = normalized_user in normalized_answer or normalized_answer in normalized_user
        
        # Update score
        if is_correct:
            self.score += POINTS_PER_CORRECT_ANSWER
        
        # Prepare response
        result_msg = "أحسنت! إجابة صحيحة" if is_correct else "حاول مرة أخرى"
        
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
        """Get intelligent hint"""
        if not self.current_answer:
            return "لا يوجد تلميح"
        
        answer = str(self.current_answer)
        
        # For short answers, show first letter
        if len(answer) <= 3:
            return f"يبدأ بـ: {answer[0]}"
        
        # For medium answers, show first half
        hint_length = len(answer) // 2
        return f"{answer[:hint_length]}..."
