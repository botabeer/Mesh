import random
from linebot.models import TextSendMessage
from utils.helpers import normalize_text

class WordColorGame:
    def __init__(self, line_bot_api, use_ai=False, get_api_key=None, switch_key=None):
        self.line_bot_api = line_bot_api
        self.current_color = None
        self.current_word_color = None
        
        self.colors = ["أحمر", "أزرق", "أخضر", "أصفر", "برتقالي", "بنفسجي", "أسود", "أبيض"]
    
    def start_game(self):
        self.current_color = random.choice(self.colors)
        self.current_word_color = random.choice(self.colors)
        
        text = (
            "🎨 ما هو لون الكلمة؟\n\n"
            f"{self.current_word_color}\n\n"
            "━━━━━━━━━━━━━━\n"
            "ما لون الكلمة المكتوبة (وليس معنى الكلمة)؟"
        )
        return TextSendMessage(text=text)
    
    def check_answer(self, answer, user_id, display_name):
        if not self.current_color:
            return None
        
        if normalize_text(answer) == normalize_text(self.current_color):
            new_q = self.start_game()
            msg = f"✓ صحيح يا {display_name}\n\n+10 نقطة\n\n{new_q.text}"
            return {
                'points': 10,
                'won': True,
                'message': msg,
                'response': TextSendMessage(text=msg),
                'game_over': False
            }
        return None
    
    def get_hint(self):
        return "💡 ركز على لون الكلمة نفسها"
    
    def reveal_answer(self):
        ans = self.current_color
        self.current_color = None
        return f"اللون الصحيح: {ans}"
