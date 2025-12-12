import os
import re
from dotenv import load_dotenv
from constants import THEMES, DEFAULT_THEME

load_dotenv()


class Config:
    """الإعدادات المركزية لبوت Mesh"""

    # معلومات عامة
    BOT_NAME = "Bot Mesh"
    VERSION = "24.0"
    RIGHTS = "عبير الدوسري 2025"

    # إعدادات LINE
    LINE_SECRET = os.getenv("LINE_CHANNEL_SECRET")
    LINE_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

    # الثيمات
    THEMES = THEMES
    DEFAULT_THEME = DEFAULT_THEME

    # إعدادات الألعاب
    GAMES = {
        "ذكاء": {
            "hint": True,
            "reveal": True,
            "timer": None,
            "no_registration": False,
            "group_only": False,
            "description": "ألغاز وأحاجي عربية"
        },
        "روليت": {
            "hint": True,
            "reveal": True,
            "timer": None,
            "no_registration": False,
            "group_only": False,
            "description": "لعبة الروليت الشهيرة"
        },
        "خمن": {
            "hint": True,
            "reveal": True,
            "timer": None,
            "no_registration": False,
            "group_only": False,
            "description": "خمن الكلمة من الفئة"
        },
        "اغنيه": {
            "hint": True,
            "reveal": True,
            "timer": None,
            "no_registration": False,
            "group_only": False,
            "description": "خمن الفنان من كلمات الأغنية"
        },
        "ترتيب": {
            "hint": True,
            "reveal": True,
            "timer": None,
            "no_registration": False,
            "group_only": False,
            "description": "رتب الحروف لتكوين كلمة"
        },
        "تكوين": {
            "hint": True,
            "reveal": True,
            "timer": None,
            "no_registration": False,
            "group_only": False,
            "description": "كون كلمات من الحروف"
        },
        "ضد": {
            "hint": True,
            "reveal": True,
            "timer": None,
            "no_registration": False,
            "group_only": False,
            "description": "اعرف عكس الكلمة"
        },
        "لعبة": {
            "hint": True,
            "reveal": True,
            "timer": None,
            "no_registration": False,
            "group_only": False,
            "description": "إنسان حيوان نبات جماد بلاد"
        },
        "اسرع": {
            "hint": False,
            "reveal": False,
            "timer": 20,
            "no_registration": False,
            "group_only": False,
            "description": "اكتب النص بأسرع وقت"
        },
        "سلسلة": {
            "hint": False,
            "reveal": False,
            "timer": None,
            "no_registration": False,
            "group_only": False,
            "description": "بناء سلسلة كلمات"
        },
        "لون": {
            "hint": True,
            "reveal": True,
            "timer": None,
            "no_registration": False,
            "group_only": False,
            "description": "اختبار الألوان Stroop"
        },
        "رياضيات": {
            "hint": True,
            "reveal": True,
            "timer": None,
            "no_registration": False,
            "group_only": False,
            "description": "مسائل حسابية"
        },
        "توافق": {
            "hint": False,
            "reveal": False,
            "timer": None,
            "no_registration": True,
            "group_only": False,
            "description": "نسبة التوافق بين اسمين"
        },
        "مافيا": {
            "hint": False,
            "reveal": False,
            "timer": None,
            "no_registration": False,
            "group_only": True,
            "description": "لعبة مافيا جماعية"
        }
    }

    # معدل الاستخدام
    RATE_LIMIT_MESSAGES = 30
    RATE_LIMIT_WINDOW = 60

    # قاعدة البيانات
    DATABASE_PATH = "botmesh.db"
    DATABASE_CLEANUP_DAYS = 90

    # الخادم
    DEFAULT_PORT = 10000

    # --------------------------------------------------------

    @classmethod
    def validate(cls):
        """التحقق من وجود المتغيرات الضرورية"""
        if not cls.LINE_SECRET:
            raise ValueError("LINE_CHANNEL_SECRET مفقود في متغيرات البيئة")
        if not cls.LINE_ACCESS_TOKEN:
            raise ValueError("LINE_CHANNEL_ACCESS_TOKEN مفقود في متغيرات البيئة")
        return True

    @classmethod
    def normalize(cls, text: str) -> str:
        """تطبيع النص العربي للمقارنة والبحث"""
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
        """إرجاع ثيم معين أو الافتراضي"""
        if name and name in cls.THEMES:
            return cls.THEMES[name]
        return cls.THEMES[cls.DEFAULT_THEME]

    @classmethod
    def is_valid_theme(cls, name: str) -> bool:
        """التحقق من صحة اسم الثيم"""
        return name in cls.THEMES

    @classmethod
    def get_game_config(cls, name: str):
        """إرجاع إعدادات لعبة محددة"""
        return cls.GAMES.get(name, {})

    @classmethod
    def get_all_games(cls):
        """إرجاع قائمة جميع الألعاب"""
        return list(cls.GAMES.keys())

    @classmethod
    def get_games_by_type(cls, game_type: str):
        """البحث عن الألعاب حسب نوع خاص"""
        if game_type == "registration_required":
            return [
                name for name, cfg in cls.GAMES.items()
                if not cfg.get("no_registration", False)
            ]
        if game_type == "group_only":
            return [
                name for name, cfg in cls.GAMES.items()
                if cfg.get("group_only", False)
            ]
        if game_type == "timed":
            return [
                name for name, cfg in cls.GAMES.items()
                if cfg.get("timer")
            ]
        return []
