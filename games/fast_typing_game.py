import random
import time
from linebot.models import TextSendMessage
from utils.helpers import normalize_text

class FastTypingGame:
    def __init__(self, line_bot_api):
        self.line_bot_api = line_bot_api
        self.current_text = None
        self.start_time = None
        
        # جمل للكتابة السريعة
        self.texts = [
            "الحياة جميلة",
            "النجاح يحتاج إلى صبر",
            "العلم نور",
            "الوقت كالذهب",
            "الصديق وقت الضيق",
            "الصحة تاج على رؤوس الأصحاء",
            "من جد وجد ومن زرع حصد",
            "العقل السليم في الجسم السليم",
            "اطلبوا العلم من المهد إلى اللحد",
            "الصبر مفتاح الفرج"
        ]
    
    def start_game(self):
        """بدء لعبة جديدة"""
        self.current_text = random.choice(self.texts)
        self.start_time = time.time()
        
        text = f"⚡ اكتب الجملة التالية بسرعة\n\n{self.current_text}\n\n━━━━━━━━━━━━━━\nابدأ الكتابة الآن!"
        return TextSendMessage(text=text)
    
    def check_answer(self, answer, user_id, display_name):
        """فحص الإجابة"""
        if not self.current_text or not self.start_time:
            return None
        
        normalized_answer = normalize_text(answer)
        normalized_text = normalize_text(self.current_text)
        
        # التحقق من التطابق
        if normalized_answer == normalized_text:
            elapsed_time = time.time() - self.start_time
            
            # حساب النقاط بناءً على السرعة
            if elapsed_time < 3:
                points = 15
                speed_msg = "سريع جداً!"
            elif elapsed_time < 5:
                points = 12
                speed_msg = "سريع"
            elif elapsed_time < 8:
                points = 10
                speed_msg = "جيد"
            elif elapsed_time < 12:
                points = 7
                speed_msg = "متوسط"
            else:
                points = 5
                speed_msg = "بطيء"
            
            new_question = self.start_game()
            message = f"✓ إجابة صحيحة يا {display_name}\n\n⏱️ الوقت: {elapsed_time:.2f} ثانية\n🏃 {speed_msg}\n+{points} نقطة\n\n{new_question.text}"
            
            return {
                'points': points,
                'won': True,
                'message': message,
                'response': TextSendMessage(text=message),
                'game_over': False
            }
        
        return None
    
    def get_hint(self):
        """تلميح"""
        if not self.current_text:
            return "لا يوجد سؤال حالي"
        
        # عرض أول 3 أحرف
        hint_text = self.current_text[:3] + "..."
        return f"💡 التلميح\n\n{hint_text}"
    
    def reveal_answer(self):
        """كشف الإجابة"""
        if not self.current_text:
            return "لا يوجد سؤال حالي"
        
        answer = self.current_text
        self.current_text = None
        self.start_time = None
        
        return f"الإجابة الصحيحة:\n{answer}"
