‏import random
‏from linebot.models import TextSendMessage

‏class GuessGame:
‏    def __init__(self, line_bot_api):
‏        self.line_bot_api = line_bot_api
‏        self.number = None
    
‏    def start_game(self):
‏        self.number = random.randint(1, 50)
‏        text = f"🎲 خمن الرقم\n\n━━━━━━━━━━━━━━\nخمن رقم بين 1 و 50"
‏        return TextSendMessage(text=text)
    
‏    def check_answer(self, answer, user_id, display_name):
‏        if not self.number:
‏            return None
        
‏        try:
‏            guess = int(answer.strip())
‏        except:
‏            return None
        
‏        if guess == self.number:
‏            new_q = self.start_game()
‏            msg = f"✓ صحيح يا {display_name}!\n\nالرقم: {self.number}\n+10 نقطة\n\n{new_q.text}"
‏            return {'points': 10, 'won': True, 'message': msg, 'response': TextSendMessage(text=msg), 'game_over': False}
‏        elif guess < self.number:
‏            return {'points': 0, 'won': False, 'message': "⬆️ أكبر", 'response': TextSendMessage(text="⬆️ أكبر"), 'game_over': False}
‏        else:
‏            return {'points': 0, 'won': False, 'message': "⬇️ أصغر", 'response': TextSendMessage(text="⬇️ أصغر"), 'game_over': False}
    
‏    def get_hint(self):
‏        if self.number <= 25:
‏            return "💡 الرقم بين 1 و 25"
‏        else:
‏            return "💡 الرقم بين 26 و 50"
    
‏    def reveal_answer(self):
‏        ans = self.number
‏        self.number = None
‏        return f"الرقم: {ans}"
