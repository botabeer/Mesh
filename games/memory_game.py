"""
لعبة اختبار الذاكرة - Enhanced Version
Created by: Abeer Aldosari © 2025
"""
from linebot.models import TextSendMessage
from .base_game import BaseGame
import random


class MemoryGame(BaseGame):
    """لعبة اختبار الذاكرة - أرقام وكلمات"""
    
    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, questions_count=10)
        self.sequence_type = "numbers"
    
    def generate_sequence(self, length):
        """توليد سلسلة عشوائية"""
        if self.sequence_type == "numbers":
            return [str(random.randint(0, 9)) for _ in range(length)]
        
        words = [
            "قلم", "كتاب", "شجرة", "بيت", "سيارة", 
            "قطة", "كلب", "زهرة", "نجم", "قمر",
            "شمس", "بحر", "جبل", "نهر", "طائر"
        ]
        return random.sample(words, min(length, len(words)))
    
    def start_game(self):
        """بدء اللعبة"""
        self.current_question = 0
        self.game_active = True
        return self.get_question()
    
    def get_question(self):
        """توليد السؤال"""
        # تدرج الصعوبة: يبدأ من 3 ويزيد تدريجياً (حد أقصى 6)
        length = 3 + (self.current_question // 3)
        length = min(length, 6)  # حد أقصى 6 عناصر
        
        # تبديل بين أرقام وكلمات
        self.sequence_type = "numbers" if self.current_question % 2 == 0 else "words"
        
        sequence = self.generate_sequence(length)
        self.current_answer = " ".join(sequence)
        
        # بناء الرسالة
        message = f"🧩 اختبار الذاكرة ({self.current_question + 1}/{self.questions_count})\n\n"
        message += f"👀 احفظ هذه السلسلة:\n\n"
        message += f"『 {' - '.join(sequence)} 』\n\n"
        
        if self.sequence_type == "numbers":
            message += "📝 اكتب الأرقام بنفس الترتيب\n"
        else:
            message += "📝 اكتب الكلمات بنفس الترتيب\n"
        
        message += "\n💡 يمكنك استخدام مسافة أو شرطة (-) للفصل"
        
        return TextSendMessage(text=message)
    
    def check_answer(self, user_answer, user_id, display_name):
        """فحص الإجابة"""
        if not self.game_active:
            return None
        
        if user_id in self.answered_users:
            return None
        
        # أمر جاوب
        if user_answer == 'جاوب':
            reveal = f"📝 الإجابة الصحيحة:\n{self.current_answer}"
            next_q = self.next_question()
            
            if isinstance(next_q, dict) and next_q.get('game_over'):
                next_q['message'] = f"{reveal}\n\n{next_q.get('message', '')}"
                return next_q
            
            message = f"{reveal}\n\n"
            if hasattr(next_q, 'text'):
                message += next_q.text
            
            return {
                'message': message,
                'response': TextSendMessage(text=message),
                'points': 0
            }
        
        # تنظيف إجابة المستخدم
        user_cleaned = user_answer.replace('-', ' ').strip()
        user_cleaned = ' '.join(user_cleaned.split())
        
        # مقارنة (غير حساسة لحالة الأحرف)
        if user_cleaned.lower() == self.current_answer.lower():
            points = self.add_score(user_id, display_name, 10)
            next_q = self.next_question()
            
            if isinstance(next_q, dict) and next_q.get('game_over'):
                next_q['points'] = points
                return next_q
            
            message = f"🎉 ذاكرة رائعة يا {display_name}!\n+{points} نقطة\n\n"
            if hasattr(next_q, 'text'):
                message += next_q.text
            
            return {
                'message': message,
                'response': TextSendMessage(text=message),
                'points': points
            }
        
        return None
