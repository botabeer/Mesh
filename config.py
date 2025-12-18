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
        replacements = {
            "أ": "ا", "إ": "ا", "آ": "ا", "ى": "ي",
            "ة": "ه", "ؤ": "و", "ئ": "ي"
        }
        for old, new in replacements.items():
            text = text.replace(old, new)
        text = re.sub(r"[^\w\sء-ي]", "", text)
        return text.strip().lower()
    
    @staticmethod
    def get_theme(theme):
        themes = {
            "light": {
                "primary": "#2C3E50",
                "secondary": "#4A5A6A",
                "success": "#16A34A",
                "warning": "#CA8A04",
                "danger": "#DC2626",
                "info": "#2563EB",
                "bg": "#F5F6F7",
                "card": "#FFFFFF",
                "card_secondary": "#F8FAFC",
                "text": "#2C3E50",
                "text_secondary": "#64748B",
                "text_tertiary": "#94A3B8",
                "border": "#E2E8F0",
                "hover": "#F8FAFC",
                "glass": "#F1F5F9",
                "accent": "#8B5CF6"
            },
            "dark": {
                "primary": "#60A5FA",
                "secondary": "#94A3B8",
                "success": "#4ADE80",
                "warning": "#FBBF24",
                "danger": "#F87171",
                "info": "#60A5FA",
                "bg": "#0F172A",
                "card": "#1E293B",
                "card_secondary": "#1A202C",
                "text": "#F1F5F9",
                "text_secondary": "#94A3B8",
                "text_tertiary": "#64748B",
                "border": "#334155",
                "hover": "#334155",
                "glass": "#1E293B",
                "accent": "#A78BFA"
            }
        }
        return themes.get(theme, themes["light"])
