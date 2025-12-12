import os
import re
from dotenv import load_dotenv

load_dotenv()


class Config:
    # معلومات البوت
    BOT_NAME = "Bot Mesh"
    VERSION = "1.0"
    RIGHTS = "تم إنشاء هذا البوت بواسطة عبير الدوسري © 2025"

    # بيانات LINE
    LINE_SECRET = os.getenv("LINE_CHANNEL_SECRET")
    LINE_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

    # قاعدة البيانات
    DATABASE_PATH = "botmesh.db"
    DEFAULT_PORT = 10000

    # الحد من الرسائل
    RATE_LIMIT_MESSAGES = 30
    RATE_LIMIT_WINDOW = 60

    # ثيمين فقط: فاتح وداكن (تصميم iOS زجاجي)
    THEMES = {
        "فاتح": {
            "bg": "#F2F2F7",
            "glass": "rgba(255, 255, 255, 0.8)",
            "card": "rgba(255, 255, 255, 0.95)",
            "primary": "#007AFF",
            "secondary": "#5AC8FA",
            "success": "#34C759",
            "warning": "#FF9500",
            "danger": "#FF3B30",
            "text": "#000000",
            "text2": "#3C3C43",
            "text3": "#8E8E93",
            "border": "rgba(60, 60, 67, 0.18)",
            "shadow": "rgba(0, 0, 0, 0.1)"
        },
        "داكن": {
            "bg": "#000000",
            "glass": "rgba(28, 28, 30, 0.8)",
            "card": "rgba(44, 44, 46, 0.95)",
            "primary": "#0A84FF",
            "secondary": "#64D2FF",
            "success": "#30D158",
            "warning": "#FF9F0A",
            "danger": "#FF453A",
            "text": "#FFFFFF",
            "text2": "#EBEBF5",
            "text3": "#8E8E93",
            "border": "rgba(142, 142, 147, 0.18)",
            "shadow": "rgba(255, 255, 255, 0.1)"
        }
    }

    DEFAULT_THEME = "فاتح"

    # ألعاب النقاط (تتطلب تسجيل)
    POINT_GAMES = [
        "ذكاء", "خمن", "ضد", "ترتيب", "رياضيات",
        "اغنيه", "لون", "تكوين", "لعبة", "سلسلة", "اسرع"
    ]

    # ألعاب ترفيهية (بدون نقاط)
    FUN_GAMES = [
        "سؤال", "منشن", "تحدي", "اعتراف", "موقف", "اقتباس", "توافق"
    ]

    @classmethod
    def validate(cls):
        """التحقق من الإعدادات الأساسية"""
        if not cls.LINE_SECRET:
            raise ValueError("LINE_CHANNEL_SECRET مفقود")
        if not cls.LINE_ACCESS_TOKEN:
            raise ValueError("LINE_CHANNEL_ACCESS_TOKEN مفقود")
        return True

    @classmethod
    def normalize(cls, text: str) -> str:
        """توحيد النص العربي"""
        if not text:
            return ""
        
        text = text[:1000].strip().lower()
        
        # توحيد الأحرف العربية
        replacements = {
            "أ": "ا", "إ": "ا", "آ": "ا",
            "ى": "ي", "ة": "ه",
            "ؤ": "و", "ئ": "ي"
        }
        
        for old, new in replacements.items():
            text = text.replace(old, new)
        
        # إزالة التشكيل
        text = re.sub(r"[\u064B-\u065F\u0670]", "", text)
        
        return text

    @classmethod
    def get_theme(cls, name: str = None):
        """الحصول على الثيم"""
        if name and name in cls.THEMES:
            return cls.THEMES[name]
        return cls.THEMES[cls.DEFAULT_THEME]

    @classmethod
    def is_valid_theme(cls, name: str) -> bool:
        """التحقق من صحة الثيم"""
        return name in cls.THEMES

    @classmethod
    def get_all_games(cls):
        """جميع الألعاب"""
        return cls.POINT_GAMES + cls.FUN_GAMES

    @classmethod
    def is_point_game(cls, game_name: str) -> bool:
        """هل اللعبة تتطلب نقاط"""
        return game_name in cls.POINT_GAMES

    @classmethod
    def is_fun_game(cls, game_name: str) -> bool:
        """هل اللعبة ترفيهية"""
        return game_name in cls.FUN_GAMES
