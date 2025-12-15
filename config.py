import os
import re
from dotenv import load_dotenv

# تحميل .env فقط في التطوير المحلي
if os.getenv("ENV") != "production":
    load_dotenv()


class Config:
    BOT_NAME = "Bot Mesh"
    VERSION = "2.0"
    RIGHTS = "Created by Abeer Aldossari 2025"

    LINE_SECRET = os.getenv("LINE_CHANNEL_SECRET")
    LINE_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

    DATABASE_PATH = "botmesh.db"
    DEFAULT_PORT = 5000

    RATE_LIMIT_MESSAGES = 30
    RATE_LIMIT_WINDOW = 60

    THEMES = {
        "light": {
            "primary": "#000000",
            "secondary": "#666666",
            "accent": "#333333",
            "success": "#2C2C2E",
            "warning": "#48484A",
            "danger": "#1C1C1E",
            "info": "#3A3A3C",
            "bg": "#FFFFFF",
            "bg_secondary": "#F9F9F9",
            "card": "rgba(255, 255, 255, 0.85)",
            "overlay": "rgba(255, 255, 255, 0.95)",
            "text": "#000000",
            "text2": "#666666",
            "text3": "#999999",
            "text_secondary": "#666666",
            "text_tertiary": "#999999",
            "text_disabled": "#CCCCCC",
            "border": "rgba(0, 0, 0, 0.1)",
            "separator": "rgba(0, 0, 0, 0.08)",
            "shadow": "rgba(0, 0, 0, 0.05)",
        },
        "dark": {
            "primary": "#FFFFFF",
            "secondary": "#A0A0A0",
            "accent": "#CCCCCC",
            "success": "#E5E5E7",
            "warning": "#C7C7CC",
            "danger": "#F2F2F7",
            "info": "#D1D1D6",
            "bg": "#000000",
            "bg_secondary": "#0A0A0A",
            "card": "rgba(28, 28, 30, 0.85)",
            "overlay": "rgba(28, 28, 30, 0.95)",
            "text": "#FFFFFF",
            "text2": "#A0A0A0",
            "text3": "#666666",
            "text_secondary": "#A0A0A0",
            "text_tertiary": "#666666",
            "text_disabled": "#3A3A3C",
            "border": "rgba(255, 255, 255, 0.1)",
            "separator": "rgba(255, 255, 255, 0.08)",
            "shadow": "rgba(0, 0, 0, 0.3)",
        }
    }

    DEFAULT_THEME = "light"

    COMMAND_ALIASES = {
        "بداية": ["start", "بدايه", "القائمة", "القائمه"],
        "العاب": ["ألعاب", "الالعاب", "الألعاب", "games"],
        "مساعدة": ["help", "مساعده", "ساعدني"],
        "نقاطي": ["احصائياتي", "احصائيات", "نقاط"],
        "الصدارة": ["المتصدرين", "الصداره", "leaderboard"],
        "ايقاف": ["stop", "إيقاف", "توقف"],
        "تسجيل": ["register", "انشاء حساب"],
        "تغيير": ["تعديل", "تحديث"],
    }

    POINT_GAMES = [
        "ذكاء", "خمن", "ضد", "ترتيب", "رياضيات",
        "اغنيه", "لون", "تكوين", "لعبة", "سلسلة", "اسرع"
    ]

    FUN_GAMES = {
        "سؤال": {"group_only": False},
        "منشن": {"group_only": False},
        "تحدي": {"group_only": False},
        "اعتراف": {"group_only": False},
        "موقف": {"group_only": False},
        "اقتباس": {"group_only": False},
        "توافق": {"group_only": False},
        "مافيا": {"group_only": True}
    }

    # --------------------------------------------------
    # Validation
    # --------------------------------------------------
    @classmethod
    def validate(cls):
        if not cls.LINE_SECRET or not cls.LINE_ACCESS_TOKEN:
            raise RuntimeError("LINE credentials missing")
        return True

    # --------------------------------------------------
    # Utils
    # --------------------------------------------------
    @classmethod
    def get_port(cls) -> int:
        try:
            return int(os.getenv("PORT", cls.DEFAULT_PORT))
        except (TypeError, ValueError):
            return cls.DEFAULT_PORT

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
        text = re.sub(r"[^\w\sء-ي]", "", text)
        return text

    # --------------------------------------------------
    # Theme helpers
    # --------------------------------------------------
    @classmethod
    def get_theme(cls, name: str = None) -> dict:
        return cls.THEMES.get(name, cls.THEMES[cls.DEFAULT_THEME])

    @classmethod
    def is_valid_theme(cls, name: str) -> bool:
        return name in cls.THEMES

    # --------------------------------------------------
    # Command resolver (FIXED)
    # --------------------------------------------------
    @classmethod
    def resolve_command(cls, text: str) -> str:
        normalized = cls.normalize(text)
        for main_cmd, aliases in cls.COMMAND_ALIASES.items():
            if normalized == cls.normalize(main_cmd):
                return main_cmd
            for alias in aliases:
                if normalized == cls.normalize(alias):
                    return main_cmd
        return normalized
