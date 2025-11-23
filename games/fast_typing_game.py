"""
لعبة الكتابة السريعة - Fast Typing (جمل مختلطة قصيرة)
"""
from linebot.models import TextSendMessage
from .base_game import BaseGame
import random
from datetime import datetime

class FastTypingGame(BaseGame):
    """لعبة الكتابة السريعة - جمل قصيرة مختلطة"""
    
    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, questions_count=5)
        
        # جمل مختلطة: أذكار/دعاء + حكم + اقتباسات
        self.sentences = [
            "سبحان الله",
            "الحمد لله",
            "الله أكبر",
            "لا حول ولا قوة",
            "أستغفر الله",
            "العلم نور",
            "الصبر مفتاح",
            "الوقت كالسيف",
            "التعاون أساس النجاح",
            "الإرادة تصنع",
            "المعرفة قوة",
            "التواضع زينة",
            "لا تؤجل",
            "الصدق منجاة",
            "احترم تُحترم",
            "الحكمة ضالة",
            "التفاؤل حياة",
            "العقل السليم",
            "السعادة اختيار",
            "الابتسامة صدقة",
            "اللهم اجعلنا شاكرين",
            "اللهم اغفر لنا",
            "الله ولي التوفيق",
            "اللهم ارحمنا",
            "التحدي يصنع",
            "المحبة تنير",
            "النجاح صبر",
            "العمل عبادة",
            "العقل نور",
            "الأمل حياة",
            "الإيمان قوة",
            "الشكر يزيد",
            "الهدوء راحة",
            "التغيير بداية",
            "المثابرة نجاح",
            "الأخلاق تاج",
            "التعلم مستمر",
            "اللهم بارك لنا",
            "اللهم احفظنا",
            "الأمانة أساس",
            "الحب أساس",
            "الثقة مفتاح"
        ]
        
        random.shuffle(self.sentences)
        self.start_time = None
        self.first_answer = True
    
    def start_game(self):
        """بدء اللعبة"""
        self.current_question = 0
        return self.get_question()
    
    def get_question(self):
        """الحصول على الجملة الحالية"""
        sentence = self.sentences[self.current_question % len(self.sentences)]
        self.current_answer = sentence
        self.start_time = datetime.now()
        self.first_answer = True
        
        message = f"⚡ اكتب بسرعة ({self.current_question + 1}/{self.questions_count})\n\n"
        message += f"📝 اكتب هذه الجملة:\n« {sentence} »\n\n"
        message += "⏱️ أسرع إجابة صحيحة تفوز!"
        
        return TextSendMessage(text=message)
    
    def check_answer(self, user_answer, user_id, display_name):
        """فحص الإجابة"""
        if not self.game_active:
            return None
        
        if user_id in self.answered_users:
            return None
        
        if user_answer.strip() == self.current_answer:
            time_taken = (datetime.now() - self.start_time).total_seconds() if self.start_time else 0
            points = 15 if self.first_answer else 10
            self.first_answer = False
            points = self.add_score(user_id, display_name, points)
            
            next_q = self.next_question()
            
            if isinstance(next_q, dict) and next_q.get('game_over'):
                next_q['points'] = points
                return next_q
            
            message = f"⚡ سريع جداً يا {display_name}!\n"
            message += f"⏱️ الوقت: {time_taken:.1f} ثانية\n"
            message += f"+{points} نقطة\n\n"
            
            if hasattr(next_q, 'text'):
                message += next_q.text
            
            return {
                'message': message,
                'response': TextSendMessage(text=message),
                'points': points
            }
        
        return None
