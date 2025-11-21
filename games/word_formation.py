import random
from .base_game import BaseGame
from linebot.models import TextSendMessage

class WordFormationGame(BaseGame):
    """لعبة تكوين الكلمات"""
    
    def __init__(self, line_bot_api):
        super().__init__(line_bot_api)
        self.letters = []
        self.valid_words = []
        self.found_words = set()
        self.word_list = [
            'قلم', 'كتاب', 'باب', 'نور', 'قمر', 'شمس', 'ورد', 'بحر',
            'جبل', 'نهر', 'سحاب', 'مطر', 'ريح', 'شجر', 'حجر', 'رمل'
        ]
    
    def get_game_name(self):
        return "تكوين الكلمات"
    
    def generate_question(self):
        # اختيار 5 حروف عشوائية
        arabic_letters = 'ابتثجحخدذرزسشصضطظعغفقكلمنهويء'
        self.letters = random.sample(arabic_letters, 5)
        
        # إيجاد الكلمات الممكنة
        self.valid_words = [word for word in self.word_list 
                           if all(letter in self.letters for letter in word)]
        
        self.current_question = f"كوّن 3 كلمات من هذه الحروف:\n\n{' - '.join(self.letters)}\n\nاكتب كلمة واحدة في كل رسالة"
        self.correct_answer = self.valid_words
    
    def check_answer(self, answer, user_id, display_name):
        answer = answer.strip()
        
        if answer in self.found_words:
            return {
                'message': "⚠️ كلمة مكررة! جرب كلمة أخرى",
                'response': TextSendMessage(text="⚠️ كلمة مكررة! جرب كلمة أخرى"),
                'points': 0,
                'won': False,
                'game_over': False
            }
        
        if answer in self.valid_words:
            self.found_words.add(answer)
            remaining = 3 - len(self.found_words)
            
            if len(self.found_words) >= 3:
                return {
                    'message': f"🎉 ممتاز {display_name}!\n\nأكملت اللعبة بنجاح!\n+{self.calculate_points(True)} نقطة",
                    'response': TextSendMessage(text=f"🎉 ممتاز {display_name}!\n\nأكملت اللعبة بنجاح!\n+{self.calculate_points(True)} نقطة"),
                    'points': self.calculate_points(True),
                    'won': True,
                    'game_over': True
                }
            
            return {
                'message': f"✅ صحيح!\nباقي {remaining} كلمات",
                'response': TextSendMessage(text=f"✅ صحيح!\nباقي {remaining} كلمات"),
                'points': 5,
                'won': False,
                'game_over': False
            }
        
        self.attempts += 1
        if self.attempts >= self.max_attempts:
            return {
                'message': f"❌ انتهت المحاولات\n\nالكلمات الصحيحة:\n{', '.join(self.valid_words[:3])}",
                'response': TextSendMessage(text=f"❌ انتهت المحاولات\n\nالكلمات الصحيحة:\n{', '.join(self.valid_words[:3])}"),
                'points': 0,
                'won': False,
                'game_over': True
            }
        
        return {
            'message': f"❌ خطأ! المحاولات المتبقية: {self.max_attempts - self.attempts}",
            'response': TextSendMessage(text=f"❌ خطأ! المحاولات المتبقية: {self.max_attempts - self.attempts}"),
            'points': 0,
            'won': False,
            'game_over': False
        }
