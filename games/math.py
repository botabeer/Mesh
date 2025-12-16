import random
from games.base import BaseGame


class MathGame(BaseGame):
    """لعبة رياضيات محسّنة"""
    
    def __init__(self, db, theme: str = "light"):
        super().__init__(db, theme)
        self.game_name = "رياضيات"
        
        self.levels = {
            1: {"min": 1, "max": 20, "ops": ["+", "-"]},
            2: {"min": 10, "max": 50, "ops": ["+", "-", "*"]},
            3: {"min": 20, "max": 100, "ops": ["+", "-", "*"]},
            4: {"min": 50, "max": 200, "ops": ["+", "-", "*", "/"]},
            5: {"min": 100, "max": 500, "ops": ["+", "-", "*", "/"]}
        }
    
    def get_question(self):
        """إنشاء سؤال رياضي"""
        level = min(self.current_q + 1, 5)
        cfg = self.levels[level]
        op = random.choice(cfg["ops"])
        
        if op == "+":
            a = random.randint(cfg["min"], cfg["max"])
            b = random.randint(cfg["min"], cfg["max"])
            self.current_answer = str(a + b)
            question = f"{a} + {b} = ؟"
        
        elif op == "-":
            a = random.randint(cfg["min"] + 10, cfg["max"])
            b = random.randint(cfg["min"], a - 1)
            self.current_answer = str(a - b)
            question = f"{a} - {b} = ؟"
        
        elif op == "*":
            max_factor = min(20, cfg["max"] // 10)
            a = random.randint(2, max_factor)
            b = random.randint(2, max_factor)
            self.current_answer = str(a * b)
            question = f"{a} × {b} = ؟"
        
        else:
            divisor = random.randint(2, 15)
            result = random.randint(2, 20)
            a = divisor * result
            self.current_answer = str(result)
            question = f"{a} ÷ {divisor} = ؟"
        
        hint = f"المستوى {level}"
        return self.build_question_flex(question, hint)
    
    def check_answer(self, answer: str) -> bool:
        """التحقق من الإجابة"""
        try:
            return str(int(answer.strip())) == self.current_answer
        except:
            return False
