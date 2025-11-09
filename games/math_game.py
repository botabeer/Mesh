import random
from linebot.models import TextSendMessage

class MathGame:
    def __init__(self, line_bot_api):
        self.line_bot_api = line_bot_api
        self.current_question_text = None
        self.correct_answer = None
        self.current_question = 1
        self.max_questions = 10
        self.players_scores = {}
        self.hint_used = False
    
    def generate_question(self):
        """إنشاء سؤال رياضي عشوائي"""
        operation = random.choice(['+', '-', '×', '÷'])
        
        if operation == '+':
            a = random.randint(10, 100)
            b = random.randint(10, 100)
            answer = a + b
            question = f"{a} + {b}"
        
        elif operation == '-':
            a = random.randint(20, 100)
            b = random.randint(10, a)
            answer = a - b
            question = f"{a} - {b}"
        
        elif operation == '×':
            a = random.randint(2, 15)
            b = random.randint(2, 15)
            answer = a * b
            question = f"{a} × {b}"
        
        else:  # ÷
            b = random.randint(2, 12)
            answer = random.randint(2, 20)
            a = b * answer
            question = f"{a} ÷ {b}"
        
        return question, answer
    
    def start_game(self):
        self.current_question = 1
        self.players_scores = {}
        return self.next_question()
    
    def next_question(self):
        """الانتقال للسؤال التالي"""
        if self.current_question > self.max_questions:
            return self.end_game()
        
        self.current_question_text, self.correct_answer = self.generate_question()
        self.hint_used = False
        
        return TextSendMessage(
            text=f"السؤال {self.current_question}/{self.max_questions}\n\n{self.current_question_text} = ?"
        )
    
    def get_hint(self):
        """الحصول على تلميح"""
        if self.hint_used:
            return TextSendMessage(text="تم استخدام التلميح مسبقاً")
        
        self.hint_used = True
        
        # تلميح بناءً على الرقم
        if self.correct_answer < 20:
            hint = f"الناتج أقل من 20"
        elif self.correct_answer < 50:
            hint = f"الناتج بين 20 و 50"
        elif self.correct_answer < 100:
            hint = f"الناتج بين 50 و 100"
        else:
            hint = f"الناتج أكبر من 100"
        
        return TextSendMessage(text=f"تلميح:\n{hint}")
    
    def show_answer(self):
        """عرض الإجابة الصحيحة"""
        msg = f"الإجابة الصحيحة: {self.correct_answer}"
        
        self.current_question += 1
        
        if self.current_question <= self.max_questions:
            next_q = self.next_question()
            return TextSendMessage(text=f"{msg}\n\n{next_q.text}")
        else:
            end_msg = self.end_game()
            return TextSendMessage(text=f"{msg}\n\n{end_msg.text}")
    
    def end_game(self):
        """إنهاء اللعبة وعرض النتائج"""
        if not self.players_scores:
            return TextSendMessage(text="انتهت اللعبة\nلم يشارك أحد")
        
        sorted_players = sorted(self.players_scores.items(), key=lambda x: x[1]['score'], reverse=True)
        
        msg = "النتائج النهائية\n\n"
        for i, (name, data) in enumerate(sorted_players[:5], 1):
            emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"  {i}."
            msg += f"{emoji} {name}: {data['score']} نقطة\n"
        
        winner = sorted_players[0]
        msg += f"\nالفائز: {winner[0]}"
        
        return TextSendMessage(text=msg)
    
    def check_answer(self, answer, user_id, display_name):
        if not self.current_question_text:
            return None
        
        # التحقق من أوامر التلميح والإجابة
        if answer == 'لمح':
            return {
                'message': '',
                'points': 0,
                'game_over': False,
                'response': self.get_hint()
            }
        
        if answer == 'جاوب':
            return {
                'message': '',
                'points': 0,
                'game_over': self.current_question > self.max_questions,
                'response': self.show_answer()
            }
        
        try:
            user_answer = int(answer.strip())
        except ValueError:
            return {
                'message': "أدخل رقم صحيح فقط",
                'points': 0,
                'game_over': False,
                'response': TextSendMessage(text="أدخل رقم صحيح فقط")
            }
        
        if user_answer == self.correct_answer:
            points = 10 if not self.hint_used else 5
            
            if display_name not in self.players_scores:
                self.players_scores[display_name] = {'score': 0}
            self.players_scores[display_name]['score'] += points
            
            msg = f"صحيح يا {display_name}"
            
            self.current_question += 1
            
            if self.current_question <= self.max_questions:
                next_q = self.next_question()
                return {
                    'message': msg,
                    'points': points,
                    'won': True,
                    'game_over': False,
                    'response': TextSendMessage(text=f"{msg}\n\n{next_q.text}")
                }
            else:
                end_msg = self.end_game()
                return {
                    'message': msg,
                    'points': points,
                    'won': True,
                    'game_over': True,
                    'response': TextSendMessage(text=f"{msg}\n\n{end_msg.text}")
                }
        
        return None
