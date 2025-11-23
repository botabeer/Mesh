"""
لعبة سلسلة الكلمات - Neumorphism Soft Version
Created by: Abeer Aldosari © 2025
"""
from linebot.models import FlexSendMessage, TextSendMessage
from .base_game import BaseGame
import random

class ChainWordsGame(BaseGame):
    """لعبة سلسلة الكلمات - نسخة محسّنة Neumorphism Soft"""
    
    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, questions_count=5)
        self.starting_words = [
            "سيارة", "تفاح", "قلم", "نجم", "كتاب", "باب", "رمل", 
            "لعبة", "حديقة", "ورد", "دفتر", "معلم", "منزل", "شمس",
            "سفر", "رياضة", "علم", "مدرسة", "طائرة", "عصير"
        ]
        self.last_word = None
        self.used_words = set()
        self.theme = "white"

    def set_theme(self, theme_name: str):
        self.theme = theme_name

    def _get_theme_colors(self):
        themes = {
            "white": {"bg": "#E0E5EC", "card": "#D1D9E6", "accent": "#667EEA", 
                     "text": "#2C3E50", "text2": "#7F8C8D"},
            "black": {"bg": "#0F0F1A", "card": "#1A1A2E", "accent": "#00D9FF",
                     "text": "#FFFFFF", "text2": "#A0AEC0"},
            "gray": {"bg": "#1A202C", "card": "#2D3748", "accent": "#68D391",
                    "text": "#F7FAFC", "text2": "#CBD5E0"},
            "purple": {"bg": "#1E1B4B", "card": "#312E81", "accent": "#A855F7",
                      "text": "#F5F3FF", "text2": "#C4B5FD"},
            "blue": {"bg": "#0C1929", "card": "#1E3A5F", "accent": "#00D9FF",
                    "text": "#E0F2FE", "text2": "#7DD3FC"}
        }
        return themes.get(self.theme, themes["white"])

    def start_game(self):
        self.current_question = 0
        self.last_word = random.choice(self.starting_words)
        self.used_words.add(self.normalize_text(self.last_word))
        return self.get_question()

    def get_question(self):
        colors = self._get_theme_colors()
        required_letter = self.last_word[-1]

        flex_content = {
            "type": "bubble",
            "size": "kilo",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "🔗 سلسلة الكلمات", "size": "lg",
                     "weight": "bold", "color": "#FFFFFF", "align": "center"},
                    {"type": "text", "text": "تأثير 3D - عمق ناعم", "size": "xs",
                     "color": "#E0E0E0", "align": "center"}
                ],
                "backgroundColor": colors["accent"],
                "paddingAll": "15px"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", 
                     "text": f"سؤال {self.current_question + 1} من {self.questions_count}",
                     "size": "sm", "color": colors["text2"], "align": "center", "margin": "sm"},
                    {"type": "text", 
                     "text": f"📝 الكلمة السابقة: {self.last_word}",
                     "size": "md", "color": colors["text"], "align": "center", "margin": "md"},
                    {"type": "text", 
                     "text": f"🔤 اكتب كلمة تبدأ بحرف: {required_letter}",
                     "size": "md", "color": colors["text"], "align": "center", "margin": "md"},
                    {"type": "text",
                     "text": "⚠️ لا تكرر الكلمات المستخدمة\n❌ لا تدعم: جاوب و لمّح",
                     "size": "xs", "color": colors["text2"], "align": "center", "margin": "md"}
                ],
                "backgroundColor": colors["card"],
                "cornerRadius": "20px",
                "paddingAll": "20px",
                "margin": "lg"
            }
        }

        return FlexSendMessage(alt_text="لعبة سلسلة الكلمات", contents=flex_content)

    def check_answer(self, user_answer, user_id, display_name):
        if not self.game_active:
            return None
        
        if user_id in self.answered_users:
            return None
        
        normalized_answer = self.normalize_text(user_answer)
        if normalized_answer in self.used_words:
            msg = f"❌ الكلمة '{user_answer}' مستخدمة من قبل!"
            return {'message': msg, 'response': TextSendMessage(text=msg), 'points': 0}
        
        required_letter = self.last_word[-1]
        if normalized_answer and normalized_answer[0] == self.normalize_text(required_letter) and len(normalized_answer) >= 2:
            self.used_words.add(normalized_answer)
            self.last_word = user_answer.strip()
            points = self.add_score(user_id, display_name, 10)
            
            self.current_question += 1
            self.answered_users.clear()
            
            if self.current_question >= self.questions_count:
                result = self.end_game()
                result['points'] = points
                return result
            
            next_q = self.get_question()
            message = f"✅ ممتاز يا {display_name}!\n+{points} نقطة\n\n"
            message += f"السؤال التالي..."
            
            return {'message': message, 'response': next_q, 'points': points}
        
        return None
