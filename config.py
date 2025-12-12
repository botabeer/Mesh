import os
import re
from dotenv import load_dotenv

load_dotenv()


class Config:
    """إعدادات النظام المركزية"""

    # معلومات البوت
    BOT_NAME = "Bot Mesh"
    VERSION = "24.0"
    RIGHTS = "عبير الدوسري 2025"

    # LINE API
    LINE_SECRET = os.getenv("LINE_CHANNEL_SECRET")
    LINE_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

    # قاعدة البيانات
    DATABASE_PATH = "botmesh.db"
    DATABASE_CLEANUP_DAYS = 90

    # الخادم
    DEFAULT_PORT = 10000

    # معدل الاستخدام
    RATE_LIMIT_MESSAGES = 30
    RATE_LIMIT_WINDOW = 60

    # الثيمات
    THEMES = {
        "ابيض": {
            "bg": "#F2F2F7",
            "card": "#FFFFFF",
            "primary": "#007AFF",
            "secondary": "#5AC8FA",
            "success": "#34C759",
            "text": "#000000",
            "text2": "#1C1C1E",
            "text3": "#8E8E93",
            "border": "#D1D1D6",
            "error": "#FF3B30",
            "warning": "#FF9500"
        },
        "اسود": {
            "bg": "#000000",
            "card": "#1C1C1E",
            "primary": "#0A84FF",
            "secondary": "#64D2FF",
            "success": "#30D158",
            "text": "#FFFFFF",
            "text2": "#E5E5EA",
            "text3": "#8E8E93",
            "border": "#38383A",
            "error": "#FF453A",
            "warning": "#FFD60A"
        },
        "ازرق": {
            "bg": "#EBF4FF",
            "card": "#FFFFFF",
            "primary": "#0066CC",
            "secondary": "#3399FF",
            "success": "#28A745",
            "text": "#001F3F",
            "text2": "#003366",
            "text3": "#6699CC",
            "border": "#B3D9FF",
            "error": "#DC3545",
            "warning": "#FFC107"
        }
    }

    DEFAULT_THEME = "ابيض"

    # الألعاب
    GAMES = {
        "ذكاء": {"requires_registration": True, "group_only": False},
        "روليت": {"requires_registration": True, "group_only": False},
        "خمن": {"requires_registration": True, "group_only": False},
        "اغنيه": {"requires_registration": True, "group_only": False},
        "ترتيب": {"requires_registration": True, "group_only": False},
        "تكوين": {"requires_registration": True, "group_only": False},
        "ضد": {"requires_registration": True, "group_only": False},
        "لعبة": {"requires_registration": True, "group_only": False},
        "اسرع": {"requires_registration": True, "group_only": False},
        "سلسلة": {"requires_registration": True, "group_only": False},
        "لون": {"requires_registration": True, "group_only": False},
        "رياضيات": {"requires_registration": True, "group_only": False},
        "توافق": {"requires_registration": False, "group_only": False}
    }

    @classmethod
    def validate(cls):
        """التحقق من المتغيرات الضرورية"""
        if not cls.LINE_SECRET:
            raise ValueError("LINE_CHANNEL_SECRET مفقود")
        if not cls.LINE_ACCESS_TOKEN:
            raise ValueError("LINE_CHANNEL_ACCESS_TOKEN مفقود")
        return True

    @classmethod
    def normalize(cls, text: str) -> str:
        """تطبيع النص العربي"""
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
        """الحصول على الثيم"""
        if name and name in cls.THEMES:
            return cls.THEMES[name]
        return cls.THEMES[cls.DEFAULT_THEME]

    @classmethod
    def is_valid_theme(cls, name: str) -> bool:
        """التحقق من صحة الثيم"""
        return name in cls.THEMES

    @classmethod
    def get_game_config(cls, name: str):
        """الحصول على إعدادات اللعبة"""
        return cls.GAMES.get(name, {})

    @classmethod
    def get_all_games(cls):
        """الحصول على جميع الألعاب"""
        return list(cls.GAMES.keys())
