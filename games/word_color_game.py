"""
لعبة الكلمة واللون - Stroop Effect مع دعم AI للتحقق من الإجابات
"""
from linebot.models import TextSendMessage
from .base_game import BaseGame
import random
import difflib


class WordColorGame(BaseGame):
    """لعبة الكلمة واللون مع مقارنة ذكية للإجابات"""
    
    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, questions_count=10)
        
        # قائمة الألوان
        self.colors = {
            "أحمر": "🔴",
            "أزرق": "🔵",
            "أخضر": "🟢",
            "أصفر": "🟡",
            "برتقالي": "🟠",
            "أرجواني": "🟣",
            "بني": "🟤",
            "أسود": "⚫",
            "أبيض": "⚪"
        }
        self.color_names = list(self.colors.keys())
    
    def start_game(self):
        """بدء اللعبة"""
        self.current_question = 0
        self.game_active = True
        return self.get_question()
    
    def generate_question(self):
        """توليد سؤال جديد"""
        word_color = random.choice(self.color_names)
        display_color = random.choice(self.color_names)
        
        if random.random() < 0.3:
            display_color = word_color
        
        self.current_answer = display_color
        return word_color, display_color
    
    def get_question(self):
        """إنشاء رسالة السؤال"""
        word_color, display_color = self.generate_question()
        color_emoji = self.colors[display_color]
        
        message = f"🎨 كلمة ولون ({self.current_question + 1}/{self.questions_count})\n\n"
        message += f"❓ ما لون الدائرة؟\n\n"
        message += f"الكلمة: {word_color}\n"
        message += f"الدائرة: {color_emoji}\n\n"
        message += "💡 اكتب لون الدائرة وليس الكلمة!"
        
        return TextSendMessage(text=message)
    
    def get_hint(self):
        """تلميح AI: أول حرف وعدد الحروف"""
        answer = self.current_answer.strip()
        first_char = answer[0]
        length = len(answer)
        return f"💡 تلميح: أول حرف '{first_char}' وعدد الحروف {length}"
    
    def check_answer(self, user_answer, user_id, display_name):
        """التحقق من الإجابة مع دعم AI-like fuzzy match"""
        if not self.game_active:
            return None
        if user_id in self.answered_users:
            return None
        
        answer = user_answer.strip()
        
        if answer == 'لمح':
            hint = self.get_hint()
            return {'message': hint, 'response': TextSendMessage(text=hint), 'points': 0}
        
        if answer == 'جاوب':
            reveal = f"🎨 الإجابة الصحيحة: {self.current_answer}"
            next_q = self.next_question()
            if isinstance(next_q, dict) and next_q.get('game_over'):
                next_q['message'] = f"{reveal}\n\n{next_q.get('message','')}"
                return next_q
            return {'message': reveal, 'response': next_q, 'points': 0}
        
        normalized = self.normalize_text(answer)
        correct = self.normalize_text(self.current_answer)
        
        # مقارنة ذكية باستخدام difflib
        ratio = difflib.SequenceMatcher(None, normalized, correct).ratio()
        if normalized == correct or ratio > 0.8:
            points = self.add_score(user_id, display_name, 10)
            next_q = self.next_question()
            if isinstance(next_q, dict) and next_q.get('game_over'):
                next_q['points'] = points
                return next_q
            msg = f"✅ ممتاز يا {display_name}!\n🎨 اللون: {self.current_answer}\n+{points} نقطة"
            return {'message': msg, 'response': next_q, 'points': points}
        
        return {'message': "▫️ إجابة غير صحيحة ▪️", 'response': TextSendMessage(text="▫️ إجابة غير صحيحة ▪️"), 'points': 0}
