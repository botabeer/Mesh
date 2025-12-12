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
    POINT_GAMES = {
        "ذكاء": {"name": "ذكاء", "group_only": False},
        "روليت": {"name": "روليت", "group_only": False},
        "خمن": {"name": "خمن", "group_only": False},
        "اغنيه": {"name": "أغنية", "group_only": False},
        "ترتيب": {"name": "ترتيب", "group_only": False},
        "تكوين": {"name": "تكوين", "group_only": False},
        "ضد": {"name": "ضد", "group_only": False},
        "لعبة": {"name": "لعبة", "group_only": False},
        "اسرع": {"name": "أسرع", "group_only": False},
        "سلسلة": {"name": "سلسلة", "group_only": False},
        "لون": {"name": "لون", "group_only": False},
        "رياضيات": {"name": "رياضيات", "group_only": False}
    }

    # ألعاب ترفيهية (بدون تسجيل ولا نقاط)
    FUN_GAMES = {
        "سؤال": {"name": "سؤال", "group_only": False},
        "منشن": {"name": "منشن", "group_only": True},
        "تحدي": {"name": "تحدي", "group_only": False},
        "اعتراف": {"name": "اعتراف", "group_only": False},
        "توافق": {"name": "توافق", "group_only": False}
    }

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
    def get_all_point_games(cls):
        return list(cls.POINT_GAMES.keys())

    @classmethod
    def get_all_fun_games(cls):
        return list(cls.FUN_GAMES.keys())

    @classmethod
    def get_all_games(cls):
        return cls.get_all_point_games() + cls.get_all_fun_games()
