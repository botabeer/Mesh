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
    MIN_NAME_LENGTH = 1
    DAILY_REWARD_POINTS = 10
    DAILY_REWARD_HOURS = 24
    
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
        if theme == "dark":
            return {
                "bg": "#000000",
                "card": "#1A1A1A",
                "text": "#FFFFFF",
                "text_secondary": "#B3B3B3",
                "text_tertiary": "#808080",
                "border": "#333333",
                "primary": "#FFFFFF",
                "success": "#22C55E",
                "warning": "#F59E0B",
                "danger": "#EF4444",
                "info": "#3B82F6",
                "accent": "#8B5CF6",
                "glass": "#1A1A1A",
                "card_secondary": "#262626"
            }
        else:
            return {
                "bg": "#FFFFFF",
                "card": "#F9FAFB",
                "text": "#111827",
                "text_secondary": "#6B7280",
                "text_tertiary": "#9CA3AF",
                "border": "#E5E7EB",
                "primary": "#3B82F6",
                "success": "#10B981",
                "warning": "#F59E0B",
                "danger": "#EF4444",
                "info": "#3B82F6",
                "accent": "#8B5CF6",
                "glass": "#F3F4F6",
                "card_secondary": "#F3F4F6"
            }
