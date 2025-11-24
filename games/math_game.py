"""
Bot Mesh - Math & IQ Game
Created by: Abeer Aldosari © 2025
"""
import random
from games.base_game import BaseGame

class MathGame(BaseGame):
    """لعبة الرياضيات - حل مسائل رياضية بسيطة"""
    
    def __init__(self, line_api):
        super().__init__(line_api)
        self.max_rounds = 5
        self.operations = ['+', '-', '×', '÷']
        self.difficulty = 'easy'  # easy, medium, hard
        self.current_round = 0
        self.correct_answer = None
    
    def start_game(self):
        self.current_round = 0
        question_data = self.generate_question()
        return self.build_flex_question(
            title="🔢 لعبة الرياضيات",
            question=f"احسب: {question_data['question']}",
            options=question_data.get('options')
        )
    
    def generate_question(self):
        """توليد سؤال رياضي عشوائي"""
        # تحديد مستوى الصعوبة حسب الجولة
        if self.current_round < 2:
            self.difficulty = 'easy'
        elif self.current_round < 4:
            self.difficulty = 'medium'
        else:
            self.difficulty = 'hard'
        
        if self.difficulty == 'easy':
            num1 = random.randint(1, 20)
            num2 = random.randint(1, 20)
            operations = ['+', '-']
        elif self.difficulty == 'medium':
            num1 = random.randint(10, 50)
            num2 = random.randint(10, 50)
            operations = ['+', '-', '×']
        else:
            num1 = random.randint(20, 100)
            num2 = random.randint(2, 20)
            operations = ['+', '-', '×', '÷']
        
        operation = random.choice(operations)
        if operation == '+':
            answer = num1 + num2
        elif operation == '-':
            if num1 < num2:
                num1, num2 = num2, num1
            answer = num1 - num2
        elif operation == '×':
            answer = num1 * num2
        else:
            num1 = num2 * random.randint(2, 10)
            answer = num1 // num2
        
        # توليد خيارات عشوائية للإجابة
        options = [str(answer)]
        while len(options) < 4:
            wrong = answer + random.randint(-10, 10)
            if str(wrong) not in options:
                options.append(str(wrong))
        random.shuffle(options)
        
        self.current_question = {
            'question': f"{num1} {operation} {num2} = ؟",
            'answer': str(answer),
            'options': options,
            'difficulty': self.difficulty
        }
        self.correct_answer = str(answer)
        return self.current_question
    
    def check_answer(self, answer, uid, name):
        """التحقق من الإجابة وتحديث النقاط"""
        if not self.game_active:
            return None
        
        self.add_player(uid, name)
        answer = answer.strip()
        is_correct = answer == self.correct_answer
        difficulty_bonus = {'easy': 0, 'medium': 5, 'hard': 10}
        points = self.calculate_points(is_correct, difficulty_bonus.get(self.difficulty, 0))
        self.update_score(uid, points, is_correct)
        
        result_flex = self.build_flex_result(
            correct=is_correct,
            answer=f"الإجابة الصحيحة: {self.correct_answer}",
            player_name=name,
            points=points
        )
        
        game_continues = self.next_round()
        
        response = {
            'response': result_flex,
            'points': points,
            'won': is_correct,
            'game_over': not game_continues
        }
        
        if game_continues:
            next_question = self.generate_question()
            response['next_question'] = self.build_flex_question(
                title="🔢 لعبة الرياضيات",
                question=f"احسب: {next_question['question']}",
                options=next_question.get('options')
            )
        else:
            response['leaderboard'] = self.build_flex_leaderboard()
        
        return response
    
    def get_game_info(self):
        """معلومات اللعبة"""
        return {
            'name': 'لعبة الرياضيات',
            'description': 'حل مسائل رياضية بسيطة',
            'icon': '🔢',
            'difficulty': self.difficulty,
            'rounds': self.max_rounds,
            'players': len(self.players)
        }

# Alias للـ IqGame إذا أردت استخدام نفس الكود
class IqGame(MathGame):
    pass
