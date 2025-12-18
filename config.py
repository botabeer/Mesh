import os
import re
from dotenv import load_dotenv

load_dotenv()

class Config:
    # إعدادات LINE
    LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
    LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
    
    # إعدادات قاعدة البيانات
    DB_PATH = os.getenv("DB_PATH", "botmesh.db")
    
    # إعدادات الخادم
    PORT = int(os.getenv("PORT", 5000))
    WORKERS = int(os.getenv("WORKERS", 4))  # زيادة Workers
    ENV = os.getenv("ENV", "production")
    
    # إعدادات الألعاب
    QUESTIONS_PER_GAME = 5
    MAX_NAME_LENGTH = 50
    MIN_NAME_LENGTH = 1
    
    # إعدادات المكافآت
    DAILY_REWARD_POINTS = 10
    DAILY_REWARD_HOURS = 24
    
    # الإنجازات
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
        """تطبيع النص العربي"""
        if not text:
            return ""
        
        # إزالة التشكيل
        text = re.sub(r"[\u064B-\u065F\u0670]", "", text)
        
        # توحيد الحروف
        replacements = {
            "أ": "ا", "إ": "ا", "آ": "ا", "ى": "ي",
            "ة": "ه", "ؤ": "و", "ئ": "ي"
        }
        for old, new in replacements.items():
            text = text.replace(old, new)
        
        # إزالة الرموز
        text = re.sub(r"[^\w\sء-ي]", "", text)
        
        return text.strip().lower()
    
    @staticmethod
    def get_theme(theme):
        """الحصول على ألوان الثيم (موحد - أسود/أبيض)"""
        return {
            "bg": "#000000",
            "text": "#FFFFFF",
            "secondary": "#CCCCCC",
            "border": "#333333",
            "primary": "#FFFFFF",
            "success": "#FFFFFF",
            "warning": "#CCCCCC",
            "danger": "#FFFFFF",
            "info": "#CCCCCC"
        }
