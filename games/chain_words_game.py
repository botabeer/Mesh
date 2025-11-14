import random
from linebot.models import TextSendMessage
from utils.helpers import normalize_text

class ChainWordsGame:
    def __init__(self, line_bot_api):
        self.line_bot_api = line_bot_api
        self.current_word = None
        self.used_words = set()
        self.hint_used = False
        
        self.start_words = [
            "محمد", "أحمد", "علي", "حسن", "سارة",
            "كتاب", "قلم", "مدرسة", "بيت", "سيارة",
            "شمس", "قمر", "نجم", "بحر", "جبل"
        ]
    
    def start_game(self):
        self.current_word = random.choice(self.start_words)
        self.used_words = {normalize_text(self.current_word)}
        self.hint_used = False
        
        last_letter = self.current_word[-1]
        text = (
            f"🔗 سلسلة الكلمات\n\n"
            f"{self.current_word}\n\n"
            f"━━━━━━━━━━━━━━\n"
            f"اكتب كلمة تبدأ بحرف: {last_letter}"
        )
        return TextSendMessage(text=text)
    
    def check_answer(self, answer, user_id, display_name):
        if not self.current_word:
            return None
        
        normalized_answer = normalize_text(answer)
        last_letter = normalize_text(self.current_word[-1])
        
        if not normalized_answer.startswith(last_letter):
            return None
        
        if normalized_answer in self.used_words:
            msg = "✗ هذه الكلمة مستخدمة من قبل"
            return {
                'points': 0,
                'won': False,
                'message': msg,
                'response': TextSendMessage(text=msg),
                'game_over': False
            }
        
        self.used_words.add(normalized_answer)
        self.current_word = answer
        
        points = 5 if self.hint_used else 10
        new_last_letter = answer[-1]
        
        msg = (
            f"✓ إجابة صحيحة يا {display_name}\n\n"
            f"{answer}\n+{points} نقطة\n\n"
            f"━━━━━━━━━━━━━━\n"
            f"اكتب كلمة تبدأ بحرف: {new_last_letter}"
        )
        
        return {
            'points': points,
            'won': True,
            'message': msg,
            'response': TextSendMessage(text=msg),
            'game_over': False
        }
    
    def get_hint(self):
        if not self.current_word:
            return "لا يوجد سؤال حالي"
        
        self.hint_used = True
        last_letter = self.current_word[-1]
        
        return (
            f"💡 التلميح\n\n"
            f"ابحث عن أي كلمة تبدأ بحرف {last_letter}\n\n"
            f"⚠️ سيتم خصم 5 نقاط"
        )
    
    def reveal_answer(self):
        if not self.current_word:
            return "لا يوجد سؤال حالي"
        
        last_letter = self.current_word[-1]
        
        examples = {
            'د': 'دار', 'ر': 'رمل', 'ل': 'ليمون', 'ن': 'نور',
            'م': 'محمد', 'ه': 'هدى', 'ة': 'رحمة', 'ت': 'تفاح'
        }
        
        example = examples.get(last_letter, f"كلمة تبدأ بـ {last_letter}")
        return f"مثال على كلمة:\n{example}"
