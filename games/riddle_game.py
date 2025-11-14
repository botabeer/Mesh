‏import random
‏from linebot.models import TextSendMessage
‏from utils.helpers import normalize_text

‏class RiddleGame:
‏    def __init__(self, line_bot_api):
‏        self.line_bot_api = line_bot_api
‏        self.current_answer = None
        
‏        self.riddles = [
‏            {"q": "له أوراق وما هو بنبات، له جلد وما هو بحيوان؟", "a": "الكتاب"},
‏            {"q": "ما هو الشيء الذي نرميه بعد العصر؟", "a": "البرتقال"},
‏            {"q": "إذا دخل الماء لم يبتل؟", "a": "الضوء"},
‏            {"q": "له رقبة ولا رأس له؟", "a": "الزجاجة"},
‏            {"q": "أخت خالك وليست خالتك؟", "a": "أمي"},
        ]
    
‏    def start_game(self):
‏        riddle = random.choice(self.riddles)
‏        self.current_answer = riddle['a']
‏        text = f"🤔 لغز\n\n{riddle['q']}\n\n━━━━━━━━━━━━━━\nما الحل؟"
‏        return TextSendMessage(text=text)
    
‏    def check_answer(self, answer, user_id, display_name):
‏        if not self.current_answer:
‏            return None
        
‏        if normalize_text(answer) in normalize_text(self.current_answer):
‏            new_q = self.start_game()
‏            msg = f"✓ صحيح يا {display_name}!\n\nالحل: {self.current_answer}\n+10 نقطة\n\n{new_q.text}"
‏            return {'points': 10, 'won': True, 'message': msg, 'response': TextSendMessage(text=msg), 'game_over': False}
‏        return None
    
‏    def get_hint(self):
‏        return f"💡 أول حرف: {self.current_answer[0]}"
    
‏    def reveal_answer(self):
‏        ans = self.current_answer
‏        self.current_answer = None
‏        return f"الحل: {ans}"
