‏import random
from linebot.models import TextSendMessage
from utils.helpers import normalize_text

class EmojiGame:
    def __init__(self, line_bot_api):
        self.line_bot_api = line_bot_api
        self.current_answer = None
        
        self.emoji_words = [
            {"emoji": "🚗💨", "word": "سيارة سريعة"},
            {"emoji": "🌙✨", "word": "ليل جميل"},
            {"emoji": "☀️🏖️", "word": "شاطئ صيفي"},
            {"emoji": "📚✏️", "word": "دراسة"},
            {"emoji": "🍕🍔", "word": "طعام"},
            {"emoji": "⚽🏆", "word": "فوز رياضي"},
            {"emoji": "🎵🎤", "word": "غناء"},
            {"emoji": "💻📱", "word": "تقنية"},
        ]
    
    def start_game(self):
        item = random.choice(self.emoji_words)
        self.current_answer = item["word"]

        text = (
            "😀 خمن الكلمة\n\n"
            f"{item['emoji']}\n\n"
            "━━━━━━━━━━━━━━\n"
            "ماذا تعني هذه الإيموجي؟"
        )

        return TextSendMessage(text=text)
    
    def check_answer(self, answer, user_id, display_name):
        if not self.current_answer:
            return None
        
        normalized_answer = normalize_text(answer)
        normalized_correct = normalize_text(self.current_answer)

        if normalized_answer in normalized_correct or normalized_correct in normalized_answer:
            new_q = self.start_game()
            msg = (
                f"✓ صحيح يا {display_name}!\n\n"
                f"الكلمة: {self.current_answer}\n"
                "+10 نقطة\n\n"
                f"{new_q.text}"
            )

            return {
                "points": 10,
                "won": True,
                "message": msg,
                "response": TextSendMessage(text=msg),
                "game_over": False
            }

        return None
    
    def get_hint(self):
        return f"💡 عدد الكلمات: {len(self.current_answer.split())}"
    
    def reveal_answer(self):
        ans = self.current_answer
        self.current_answer = None
        return f"الكلمة: {ans}"
