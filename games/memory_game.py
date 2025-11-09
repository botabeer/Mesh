import random
from linebot.models import TextSendMessage

class MemoryGame:
    def __init__(self, line_bot_api):
        self.line_bot_api = line_bot_api
        
        # أنواع التسلسل
        self.sequences = ["أرقام", "ألوان", "حيوانات", "فواكه", "مدن"]
        
        # عناصر كل نوع
        self.items = {
            "أرقام": ["1","2","3","4","5","6","7","8","9","0"],
            "ألوان": ["أحمر","أزرق","أخضر","أصفر","أبيض","أسود","برتقالي","بنفسجي"],
            "حيوانات": ["أسد","نمر","فيل","قرد","زرافة","حمار وحشي","دب","ذئب"],
            "فواكه": ["تفاح","برتقال","موز","عنب","مانجو","فراولة","كيوي","أناناس"],
            "مدن": ["الرياض","جدة","مكة","المدينة","الدمام","الطائف","أبها","تبوك"]
        }
        
        self.current_sequence = []
        self.current_type = None
        self.sequence_length = 4
        self.waiting_for_answer = False
    
    def _generate_sequence(self):
        """توليد تسلسل عشوائي من النوع المختار"""
        self.current_type = random.choice(self.sequences)
        available_items = self.items[self.current_type]
        self.sequence_length = random.randint(4, 6)
        self.current_sequence = random.sample(available_items, min(self.sequence_length, len(available_items)))
        self.waiting_for_answer = True
    
    def start_game(self):
        """بدء اللعبة وعرض التسلسل للاعب"""
        self._generate_sequence()
        sequence_text = " - ".join(self.current_sequence)
        return TextSendMessage(
            text=f"لعبة الذاكرة\n\nاحفظ هذا التسلسل ({self.current_type}):\n{sequence_text}\n\nاكتب التسلسل بنفس الترتيب (افصل بينهم بمسافة)"
        )
    
    def get_hint(self):
        """إعطاء تلميح"""
        if not self.current_sequence:
            return "لا يوجد سؤال حالي"
        return f"التسلسل يبدأ بـ: {self.current_sequence[0]}\nوينتهي بـ: {self.current_sequence[-1]}\nعدد العناصر: {len(self.current_sequence)}"
    
    def get_answer(self):
        """إعطاء الإجابة الكاملة"""
        if not self.current_sequence:
            return "لا يوجد سؤال حالي"
        return " - ".join(self.current_sequence)
    
    def check_answer(self, answer, user_id, display_name):
        """التحقق من الإجابة"""
        if not self.current_sequence or not self.waiting_for_answer:
            return None
        
        user_sequence = [item.strip() for item in answer.replace("-", " ").split()]
        
        if len(user_sequence) == len(self.current_sequence):
            normalized_user = [item.lower() for item in user_sequence]
            normalized_correct = [item.lower() for item in self.current_sequence]
            
            if normalized_user == normalized_correct:
                points = 15
                # توليد تسلسل جديد
                self._generate_sequence()
                sequence_text = " - ".join(self.current_sequence)
                
                return {
                    'points': points,
                    'won': True,
                    'response': TextSendMessage(
                        text=f"رائع يا {display_name}! +{points}\n\nتسلسل جديد ({self.current_type}):\n{sequence_text}\nاكتبه بنفس الترتيب"
                    )
                }
        return None
