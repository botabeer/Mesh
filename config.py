import os
import re
from dotenv import load_dotenv

load_dotenv()

class Config:
    LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
    LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
    DB_PATH = os.getenv("DB_PATH", "botmesh.db")
    PORT = int(os.getenv("PORT", 5000))
    WORKERS = int(os.getenv("WORKERS", 4))
    ENV = os.getenv("ENV", "production")
    
    QUESTIONS_PER_GAME = 5
    MAX_NAME_LENGTH = 50
    MIN_NAME_LENGTH = 2
    DAILY_REWARD_POINTS = 10
    DAILY_REWARD_HOURS = 24
    INACTIVE_DAYS = 30
    
    ACHIEVEMENTS = {
        "first_game": {"name": "اللعبة الاولى", "desc": "اكمل اول لعبة", "points": 5},
        "ten_games": {"name": "محترف", "desc": "اكمل 10 العاب", "points": 20},
        "fifty_games": {"name": "خبير", "desc": "اكمل 50 لعبة", "points": 50},
        "hundred_games": {"name": "اسطورة", "desc": "اكمل 100 لعبة", "points": 100},
        "first_win": {"name": "الفوز الاول", "desc": "احصل على فوز مثالي", "points": 10},
        "ten_wins": {"name": "فائز متميز", "desc": "احصل على 10 انتصارات", "points": 30},
        "hundred_points": {"name": "جامع النقاط", "desc": "اجمع 100 نقطة", "points": 25},
        "streak_3": {"name": "سلسلة قوية", "desc": "فز ب 3 العاب متتالية", "points": 15},
        "streak_5": {"name": "سلسلة ذهبية", "desc": "فز ب 5 العاب متتالية", "points": 35},
        "all_games": {"name": "المستكشف", "desc": "جرب جميع الالعاب", "points": 40}
    }
    
    @staticmethod
    def normalize(text):
        if not text:
            return ""
        # ازالة التشكيل
        text = re.sub(r"[\u064B-\u065F\u0670]", "", text)
        # توحيد الحروف
        replacements = {
            "أ": "ا", "إ": "ا", "آ": "ا", 
            "ى": "ي", "ة": "ه", 
            "ؤ": "و", "ئ": "ي"
        }
        for old, new in replacements.items():
            text = text.replace(old, new)
        # ازالة الاحرف غير العربية والانجليزية
        text = re.sub(r"[^\w\sء-ي]", "", text)
        return text.strip().lower()
    
    @staticmethod
    def get_theme(theme):
        if theme == "dark":
            return {
                "bg": "#1A1A1A",
                "card": "#2D2D2D",
                "card_secondary": "#3D3D3D",
                "text": "#FFFFFF",
                "text_secondary": "#CCCCCC",
                "text_tertiary": "#999999",
                "border": "#4D4D4D",
                "primary": "#FFFFFF",
                "button_primary": "#4D4D4D",
                "button_secondary": "#3D3D3D",
                "button_text": "#FFFFFF"
            }
        else:
            return {
                "bg": "#FFFFFF",
                "card": "#F5F5F5",
                "card_secondary": "#E8E8E8",
                "text": "#1A1A1A",
                "text_secondary": "#4D4D4D",
                "text_tertiary": "#808080",
                "border": "#CCCCCC",
                "primary": "#1A1A1A",
                "button_primary": "#E8E8E8",
                "button_secondary": "#D8D8D8",
                "button_text": "#1A1A1A"
            }
