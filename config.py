import os
import re
from dotenv import load_dotenv

load_dotenv()

class Config:
    # معلومات البوت
    BOT_NAME = "Bot Mesh"
    VERSION = "2.0"
    RIGHTS = "Created by Abeer Aldossari 2025"

    # إعدادات LINE
    LINE_SECRET = os.getenv("LINE_CHANNEL_SECRET")
    LINE_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

    # قاعدة البيانات
    DATABASE_PATH = "botmesh.db"
    DEFAULT_PORT = 10000

    # حدود المعدل
    RATE_LIMIT_MESSAGES = 30
    RATE_LIMIT_WINDOW = 60

    # الثيمات المحسّنة بأسلوب iOS زجاجي
    THEMES = {
        "light": {
            # الألوان الأساسية
            "primary": "#000000",
            "secondary": "#666666",
            "accent": "#333333",
            
            # ألوان الحالة
            "success": "#2C2C2E",
            "warning": "#48484A",
            "danger": "#1C1C1E",
            "info": "#3A3A3C",
            
            # ألوان الخلفية
            "bg": "#FFFFFF",
            "bg_secondary": "#F9F9F9",
            "card": "rgba(255, 255, 255, 0.85)",
            "overlay": "rgba(255, 255, 255, 0.95)",
            
            # ألوان النص (مع text2 و text3)
            "text": "#000000",
            "text2": "#666666",  # إضافة text2
            "text3": "#999999",  # إضافة text3
            "text_secondary": "#666666",
            "text_tertiary": "#999999",
            "text_disabled": "#CCCCCC",
            
            # الحدود والفواصل
            "border": "rgba(0, 0, 0, 0.1)",
            "separator": "rgba(0, 0, 0, 0.08)",
            "shadow": "rgba(0, 0, 0, 0.05)",
        },
        
        "dark": {
            # الألوان الأساسية
            "primary": "#FFFFFF",
            "secondary": "#A0A0A0",
            "accent": "#CCCCCC",
            
            # ألوان الحالة
            "success": "#E5E5E7",
            "warning": "#C7C7CC",
            "danger": "#F2F2F7",
            "info": "#D1D1D6",
            
            # ألوان الخلفية
            "bg": "#000000",
            "bg_secondary": "#0A0A0A",
            "card": "rgba(28, 28, 30, 0.85)",
            "overlay": "rgba(28, 28, 30, 0.95)",
            
            # ألوان النص (مع text2 و text3)
            "text": "#FFFFFF",
            "text2": "#A0A0A0",  # إضافة text2
            "text3": "#666666",  # إضافة text3
            "text_secondary": "#A0A0A0",
            "text_tertiary": "#666666",
            "text_disabled": "#3A3A3C",
            
            # الحدود والفواصل
            "border": "rgba(255, 255, 255, 0.1)",
            "separator": "rgba(255, 255, 255, 0.08)",
            "shadow": "rgba(0, 0, 0, 0.3)",
        }
    }

    DEFAULT_THEME = "light"

    # الألعاب المتاحة
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

    @classmethod
    def validate(cls):
        """التحقق من صحة الإعدادات"""
        if not cls.LINE_SECRET or not cls.LINE_ACCESS_TOKEN:
            raise ValueError("LINE credentials missing")
        return True

    @classmethod
    def get_port(cls) -> int:
        """الحصول على المنفذ"""
        try:
            return int(os.getenv("PORT", cls.DEFAULT_PORT))
        except:
            return cls.DEFAULT_PORT

    @classmethod
    def normalize(cls, text: str) -> str:
        """تطبيع النص العربي"""
        if not text:
            return ""
        text = text[:1000].strip().lower()
        
        # استبدال الأحرف المتشابهة
        replacements = {
            "أ": "ا", "إ": "ا", "آ": "ا", "ى": "ي",
            "ة": "ه", "ؤ": "و", "ئ": "ي"
        }
        for old, new in replacements.items():
            text = text.replace(old, new)
        
        # إزالة التشكيل
        text = re.sub(r"[\u064B-\u065F\u0670]", "", text)
        
        # إزالة الرموز
        text = re.sub(r"[^\w\sء-ي]", "", text)
        
        return text

    @classmethod
    def get_theme(cls, name: str = None):
        """الحصول على الثيم"""
        return cls.THEMES.get(name, cls.THEMES[cls.DEFAULT_THEME])

    @classmethod
    def is_valid_theme(cls, name: str) -> bool:
        """التحقق من صحة الثيم"""
        return name in cls.THEMES
