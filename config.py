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
        text = re.sub(r"[\u064B-\u065F\u0670]", "", text)
        replacements = {"أ": "ا", "إ": "ا", "آ": "ا", "ى": "ي", "ة": "ه", "ؤ": "و", "ئ": "ي"}
        for old, new in replacements.items():
            text = text.replace(old, new)
        text = re.sub(r"[^\w\sء-ي]", "", text)
        return text.strip().lower()
    
    @staticmethod
    def get_theme(theme):
        """الثيمات حسب التصميم"""
        if theme == "dark":
            return {
                "bg": "#8FAFD9",
                "card": "#000000",
                "card_secondary": "#2C2C2E",
                "text": "#FFFFFF",
                "text_secondary": "#E5E5EA",
                "text_tertiary": "#A1A1AA",
                "border": "#2C2C2E",
                "primary": "#FFFFFF",
                "button_primary": "#E5E5EA",
                "button_text": "#000000"
            }
        else:
            return {
                "bg": "#8FAFD9",
                "card": "#FFFFFF",
                "card_secondary": "#E5E7EB",
                "text": "#111827",
                "text_secondary": "#1F2937",
                "text_tertiary": "#6B7280",
                "border": "#E5E7EB",
                "primary": "#111827",
                "button_primary": "#DEE1E7",
                "button_text": "#111827"
            }
