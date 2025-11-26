"""
Bot Mesh v7.0 - Enhanced Math Game
لعبة رياضيات ذكية مع مستويات صعوبة متدرجة
Created by: Enhanced System © 2025
"""

import random
from typing import Dict, Any
from core.game_engine import BaseGame, Question, GameMode


class EnhancedMathGame(BaseGame):
    """لعبة رياضيات محسنة مع ذكاء في توليد الأسئلة"""

    def __init__(self, mode: GameMode = GameMode.SINGLE, **kwargs):
        super().__init__(
            game_id=kwargs.get('game_id', 'math'),
            game_name="رياضيات",
            game_icon="🔢",
            mode=mode,
            max_rounds=kwargs.get('max_rounds', 5)
        )

        # مستويات الصعوبة المتدرجة
        self.difficulty_levels = {
            1: {
                "min": 1, "max": 20,
                "ops": ['+', '-'],
                "label": "سهل 🌱",
                "time_limit": 30
            },
            2: {
                "min": 10, "max": 50,
                "ops": ['+', '-', '×'],
                "label": "متوسط ⭐",
                "time_limit": 45
            },
            3: {
                "min": 20, "max": 100,
                "ops": ['+', '-', '×'],
                "label": "صعب 🔥",
                "time_limit": 60
            },
            4: {
                "min": 50, "max": 200,
                "ops": ['+', '-', '×'],
                "label": "صعب جداً 💪",
                "time_limit": 75
            },
            5: {
                "min": 100, "max": 500,
                "ops": ['+', '-', '×', '÷'],
                "label": "خبير 👑",
                "time_limit": 90
            }
        }

    def generate_question(self) -> Question:
        """توليد سؤال رياضي ذكي"""
        # تحديد المستوى بناءً على الجولة الحالية
        level_num = min(self.current_round, 5)
        level = self.difficulty_levels[level_num]

        # اختيار عملية عشوائية
        operation = random.choice(level["ops"])

        if operation == '+':
            return self._generate_addition(level)
        elif operation == '-':
            return self._generate_subtraction(level)
        elif operation == '×':
            return self._generate_multiplication(level)
        elif operation == '÷':
            return self._generate_division(level)
        else:
            return self._generate_addition(level)

    def _generate_addition(self, level: Dict) -> Question:
        """توليد سؤال جمع"""
        a = random.randint(level["min"], level["max"])
        b = random.randint(level["min"], level["max"])
        answer = a + b

        return Question(
            question=f"{a} + {b} = ؟",
            answer=str(answer),
            hint=f"💡 الناتج أكبر من {max(a, b)}",
            category="جمع",
            difficulty=self._get_difficulty_from_numbers(a, b),
            metadata={"a": a, "b": b, "operation": "+"}
        )

    def _generate_subtraction(self, level: Dict) -> Question:
        """توليد سؤال طرح (التأكد من أن النتيجة موجبة)"""
        a = random.randint(level["min"] + 10, level["max"])
        b = random.randint(level["min"], a - 1)
        answer = a - b

        return Question(
            question=f"{a} - {b} = ؟",
            answer=str(answer),
            hint=f"💡 الناتج أقل من {a}",
            category="طرح",
            difficulty=self._get_difficulty_from_numbers(a, b),
            metadata={"a": a, "b": b, "operation": "-"}
        )

    def _generate_multiplication(self, level: Dict) -> Question:
        """توليد سؤال ضرب (أرقام معقولة)"""
        # تحديد نطاق أصغر للضرب لتجنب الأرقام الكبيرة جداً
        max_factor = min(20, level["max"] // 10)
        a = random.randint(2, max_factor)
        b = random.randint(2, max_factor)
        answer = a * b

        # تلميح ذكي
        hint = f"💡 العدد "
        if answer % 2 == 0:
            hint += "زوجي"
        else:
            hint += "فردي"
        
        if answer % 5 == 0:
            hint += " ومن مضاعفات 5"

        return Question(
            question=f"{a} × {b} = ؟",
            answer=str(answer),
            hint=hint,
            category="ضرب",
            difficulty=self._get_difficulty_from_numbers(a, b),
            metadata={"a": a, "b": b, "operation": "×"}
        )

    def _generate_division(self, level: Dict) -> Question:
        """توليد سؤال قسمة (مع ناتج صحيح)"""
        # توليد ناتج القسمة أولاً
        result = random.randint(2, 20)
        divisor = random.randint(2, 15)
        dividend = result * divisor
        
        return Question(
            question=f"{dividend} ÷ {divisor} = ؟",
            answer=str(result),
            hint=f"💡 الناتج أقل من {dividend // 2}",
            category="قسمة",
            difficulty=self._get_difficulty_from_numbers(dividend, divisor),
            metadata={"a": dividend, "b": divisor, "operation": "÷"}
        )

    def _get_difficulty_from_numbers(self, a: int, b: int) -> int:
        """حساب صعوبة السؤال بناءً على الأرقام"""
        total = abs(a) + abs(b)
        
        if total < 50:
            return 1
        elif total < 100:
            return 2
        elif total < 200:
            return 3
        elif total < 500:
            return 4
        else:
            return 5

    def submit_answer(self, user_id: str, username: str, answer: str) -> Dict[str, Any]:
        """فحص الإجابة مع دعم الأرقام"""
        # تطبيع الإجابة (إزالة الفواصل والمسافات)
        normalized_answer = answer.strip().replace(',', '').replace('،', '').replace(' ', '')
        
        # التحقق من أنها رقم
        try:
            int(normalized_answer)
        except ValueError:
            return self._error_response("❌ الرجاء إدخال رقم صحيح")

        return super().submit_answer(user_id, username, normalized_answer)


# تسجيل اللعبة في المدير
def register():
    from core.game_manager import game_manager
    game_manager.register_game("رياضيات", EnhancedMathGame)
