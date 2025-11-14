‏import random
‏from linebot.models import TextSendMessage

‏class MemoryGame:
‏    def __init__(self, line_bot_api):
‏        self.line_bot_api = line_bot_api
‏        self.sequence = None
    
‏    def start_game(self):
‏        length = random.randint(4, 7)
‏        self.sequence = [random.randint(1, 9) for _ in range(length)]
‏        seq_str = ' '.join(map(str, self.sequence))
        
‏        text = f"🧠 تذكر الأرقام\n\n{seq_str}\n\n━━━━━━━━━━━━━━\nأعد كتابة الأرقام بنفس الترتيب (بمسافات)"
‏        return TextSendMessage(text=text)
    
‏    def check_answer(self, answer, user_id, display_name):
‏        if not self.sequence:
‏            return None
        
‏        try:
‏            user_seq = [int(x) for x in answer.strip().split()]
‏        except:
‏            return None
        
‏        if user_seq == self.sequence:
‏            new_q = self.start_game()
‏            msg = f"✓ ذاكرة قوية يا {display_name}!\n\n+10 نقطة\n\n{new_q.text}"
‏            return {'points': 10, 'won': True, 'message': msg, 'response': TextSendMessage(text=msg), 'game_over': False}
‏        return None
    
‏    def get_hint(self):
‏        return f"💡 عدد الأرقام: {len(self.sequence)}"
    
‏    def reveal_answer(self):
‏        ans = ' '.join(map(str, self.sequence))
‏        self.sequence = None
‏        return f"الأرقام: {ans}"
