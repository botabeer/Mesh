import os
import re
from dotenv import load_dotenv

load_dotenv()


class Config:
    BOT_NAME = "Bot Mesh"
    VERSION = "1.0"
    RIGHTS = "تم إنشاء هذا البوت بواسطة عبير الدوسري © 2025"

    LINE_SECRET = os.getenv("LINE_CHANNEL_SECRET")
    LINE_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

    DATABASE_PATH = "botmesh.db"
    DEFAULT_PORT = 10000

    RATE_LIMIT_MESSAGES = 30
    RATE_LIMIT_WINDOW = 60

    # ثيمين فقط: فاتح وداكن بتصميم iOS زجاجي
    THEMES = {
        "فاتح": {
            "bg": "#F2F2F7",
            "glass": "rgba(255, 255, 255, 0.8)",
            "card": "rgba(255, 255, 255, 0.9)",
            "primary": "#007AFF",
            "secondary": "#5AC8FA",
            "success": "#34C759",
            "text": "#000000",
            "text2": "#3C3C43",
            "text3": "#8E8E93",
            "border": "rgba(60, 60, 67, 0.18)",
            "shadow": "rgba(0, 0, 0, 0.1)"
        },
        "داكن": {
            "bg": "#000000",
            "glass": "rgba(28, 28, 30, 0.8)",
            "card": "rgba(44, 44, 46, 0.9)",
            "primary": "#0A84FF",
            "secondary": "#64D2FF",
            "success": "#30D158",
            "text": "#FFFFFF",
            "text2": "#EBEBF5",
            "text3": "#8E8E93",
            "border": "rgba(142, 142, 147, 0.18)",
            "shadow": "rgba(255, 255, 255, 0.1)"
        }
    }

    DEFAULT_THEME = "فاتح"

    # ألعاب نقاط (تتطلب تسجيل)
    POINT_GAMES = [
        "ذكاء", "مافيا", "خمن", "اغنيه", "ترتيب", 
        "تكوين", "ضد", "لعبة", "اسرع", "سلسلة", 
        "لون", "رياضيات"
    ]

    # ألعاب ترفيهية (بدون تسجيل ولا نقاط)
    FUN_GAMES = [
        "سؤال", "منشن", "تحدي", "اعتراف", "توافق", "موقف", "اقتباس",
    ]

    @classmethod
    def validate(cls):
        if not cls.LINE_SECRET:
            raise ValueError("LINE_CHANNEL_SECRET مفقود")
        if not cls.LINE_ACCESS_TOKEN:
            raise ValueError("LINE_CHANNEL_ACCESS_TOKEN مفقود")
        return True

    @classmethod
    def normalize(cls, text: str) -> str:
        if not text:
            return ""
        
        text = text[:1000].strip().lower()
        
        replacements = {
            "أ": "ا", "إ": "ا", "آ": "ا",
            "ى": "ي", "ة": "ه",
            "ؤ": "و", "ئ": "ي"
        }
        
        for old, new in replacements.items():
            text = text.replace(old, new)
        
        text = re.sub(r"[\u064B-\u065F\u0670]", "", text)
        
        return text

    @classmethod
    def get_theme(cls, name: str = None):
        if name and name in cls.THEMES:
            return cls.THEMES[name]
        return cls.THEMES[cls.DEFAULT_THEME]

    @classmethod
    def is_valid_theme(cls, name: str) -> bool:
        return name in cls.THEMES

    @classmethod
    def get_all_games(cls):
        return cls.POINT_GAMES + cls.FUN_GAMES

    @classmethod
    def is_point_game(cls, game_name: str) -> bool:
        return game_name in cls.POINT_GAMES
