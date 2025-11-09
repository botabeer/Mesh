import random
from linebot.models import TextSendMessage

class MathGame:
    def __init__(self, line_bot_api):
        self.line_bot_api = line_bot_api
        self.current_question = None
        self.current_answer = None
        self.operation = None
        self.numbers = []

    def _generate_question(self):
        """توليد سؤال رياضيات عشوائي"""
        operations = [
            'addition', 
            'subtraction', 
            'multiplication', 
            'division', 
            'mixed', 
            'exponent', 
            'square_root', 
            'fraction'
        ]
        
        operation_type = random.choice(operations)
        
        if operation_type == 'addition':
            a = random.randint(10, 500)
            b = random.randint(10, 500)
            self.current_answer = a + b
            self.current_question = f"{a} + {b} = ?"
            self.numbers = [a, b]
            self.operation = '+'
            
        elif operation_type == 'subtraction':
            a = random.randint(50, 500)
            b = random.randint(10, a-1)
            self.current_answer = a - b
            self.current_question = f"{a} - {b} = ?"
            self.numbers = [a, b]
            self.operation = '-'
            
        elif operation_type == 'multiplication':
            a = random.randint(2, 25)
            b = random.randint(2, 25)
            self.current_answer = a * b
            self.current_question = f"{a} × {b} = ?"
            self.numbers = [a, b]
            self.operation = '×'
            
        elif operation_type == 'division':
            b = random.randint(2, 20)
            answer = random.randint(2, 20)
            a = b * answer
            self.current_answer = answer
            self.current_question = f"{a} ÷ {b} = ?"
            self.numbers = [a, b]
            self.operation = '÷'
            
        elif operation_type == 'mixed':
            a = random.randint(2, 20)
            b = random.randint(2, 20)
            c = random.randint(2, 20)
            if random.choice([True, False]):
                self.current_answer = (a + b) * c
                self.current_question = f"({a} + {b}) × {c} = ?"
            else:
                self.current_answer = a * b + c
                self.current_question = f"{a} × {b} + {c} = ?"
            self.numbers = [a, b, c]
            self.operation = 'mixed'
            
        elif operation_type == 'exponent':
            a = random.randint(2, 10)
            b = random.randint(2, 4)
            self.current_answer = a ** b
            self.current_question = f"{a}^{b} = ?"
            self.numbers = [a, b]
            self.operation = 'exponent'
            
        elif operation_type == 'square_root':
            a = random.randint(2, 20)
            self.current_answer = a
            self.current_question = f"√{a**2} = ?"
            self.numbers = [a]
            self.operation = 'square_root'
            
        elif operation_type == 'fraction':
            numerator = random.randint(1, 10)
            denominator = random.randint(2, 10)
            self.current_answer = round(numerator / denominator, 2)
            self.current_question = f"{numerator}/{denominator} = ? (أقرب رقم عشري)"
            self.numbers = [numerator, denominator]
            self.operation = 'fraction'

    def start_game(self):
        """بدء اللعبة"""
        self._generate_question()
        return TextSendMessage(
            text=f"لعبة الرياضيات\n\n{self.current_question}\n\n💡 لمح: تلميح\n✅ جاوب: الإجابة"
        )

    def get_hint(self):
        """إعطاء تلميح"""
        if not self.current_question:
            return "لا يوجد سؤال حالي"
        
        if self.operation == '+':
            return f"الناتج أكبر من {self.numbers[0]} وأصغر من {self.numbers[0] + self.numbers[1] + 10}"
        elif self.operation == '-':
            return f"الناتج بين {max(0, self.current_answer - 10)} و {self.current_answer + 10}"
        elif self.operation == '×':
            return f"جرب ضرب {self.numbers[0]} في {self.numbers[1]}"
        elif self.operation == '÷':
            return f"كم مرة يدخل {self.numbers[1]} في {self.numbers[0]}؟"
        elif self.operation == 'mixed':
            return "احسب ما بين الأقواس أولاً، ثم أكمل العملية"
        elif self.operation == 'exponent':
            return f"جرب ضرب {self.numbers[0]} في نفسه {self.numbers[1]-1} مرات"
        elif self.operation == 'square_root':
            return f"فكر في أي عدد إذا تم تربيعه يعطي {self.numbers[0]**2}"
        elif self.operation == 'fraction':
            return "اقسم البسط على المقام وأقرب الناتج عشريًا"

    def get_answer(self):
        """إعطاء الإجابة الكاملة"""
        if self.current_answer is None:
            return "لا يوجد سؤال حالي"
        return str(self.current_answer)

    def check_answer(self, answer, user_id, display_name):
        """التحقق من الإجابة"""
        if self.current_answer is None:
            return None
        
        try:
            user_answer = float(answer.strip())
            if abs(user_answer - self.current_answer) < 0.01:
                points = 7
                self._generate_question()
                return {
                    'points': points,
                    'won': True,
                    'response': TextSendMessage(
                        text=f"✅ صحيح يا {display_name}! +{points}\n\nسؤال جديد:\n{self.current_question}\n\n💡 لمح: تلميح\n✅ جاوب: الإجابة"
                    )
                }
        except ValueError:
            pass
        
        return {
            'points': 0,
            'won': False,
            'response': TextSendMessage(
                text=f"❌ خطأ! حاول مرة أخرى\nالسؤال: {self.current_question}"
            )
        }
