‏import random
‏from linebot.models import TextSendMessage
‏from utils.helpers import normalize_text

‏class ScrambleWordGame:
‏    def __init__(self, line_bot_api):
‏        self.line_bot_api = line_bot_api
‏        self.current_word = None
‏        self.scrambled = None
        
‏        self.words = ["كتاب", "مدرسة", "حاسوب", "هاتف", "طائرة", "سيارة", "مستشفى", "جامعة", "مكتبة", "حديقة"]
    
‏    def start_game(self):
‏        self.current_word = random.choice(self.words)
‏        letters = list(self.current_word)
‏        random.shuffle(letters)
‏        self.scrambled = ''.join(letters)
        
‏        text = f"🔀 رتب الحروف\n\n{' '.join(self.scrambled)}\n\n━━━━━━━━━━━━━━\nما هي الكلمة؟"
‏        return TextSendMessage(text=text)
    
‏    def check_answer(self, answer, user_id, display_name):
‏        if not self.current_word:
‏            return None
        
‏        if normalize_text(answer) == normalize_text(self.current_word):
‏            new_q = self.start_game()
‏            msg = f"✓ صحيح يا {display_name}\n\nالكلمة: {self.current_word}\n+10 نقطة\n\n{new_q.text}"
‏            return {'points': 10, 'won': True, 'message': msg, 'response': TextSendMessage(text=msg), 'game_over': False}
‏        return None
    
‏    def get_hint(self):
‏        return f"💡 عدد الحروف: {len(self.current_word)}\nأول حرف: {self.current_word[0]}"
    
‏    def reveal_answer(self):
‏        ans = self.current_word
‏        self.current_word = None
‏        return f"الكلمة: {ans}"
