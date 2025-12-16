import os
import re
from dotenv import load_dotenv

load_dotenv()


class Config:
    """إعدادات التطبيق المحسّنة"""
    
    BOT_NAME = "Bot Mesh"
    VERSION = "15.0"
    COPYRIGHT = "تم إنشاء هذا البوت بواسطة عبير الدوسري @ 2025"
    AUTHOR = "عبير الدوسري"

    LINE_SECRET = os.getenv("LINE_CHANNEL_SECRET")
    LINE_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

    DB_PATH = os.getenv("DB_PATH", "botmesh.db")
    PORT = int(os.getenv("PORT", 5000))
    WORKERS = int(os.getenv("WORKERS", 4))
    ENV = os.getenv("ENV", "production")

    QUESTIONS_PER_GAME = 5
    MAX_NAME_LENGTH = 50
    MIN_NAME_LENGTH = 1

    RESERVED_COMMANDS = {
        "بدايه", "بداية", "العاب", "نقاطي", "الصداره", "الصدارة",
        "ثيم", "مساعده", "مساعدة", "تسجيل", "ايقاف", "انسحب",
        "تغيير الاسم", "تغيير اسمي", "ذكاء", "خمن", "رياضيات",
        "ترتيب", "ضد", "اسرع", "سلسله", "سلسلة", "توافق",
        "انسان حيوان", "تكوين", "اغاني", "الوان",
        "تحدي", "سؤال", "سوال", "اعتراف", "منشن", "موقف", 
        "حكمه", "حكمة", "شخصيه", "شخصية", "مافيا"
    }

    THEMES = {
        "light": {
            "primary": "#000000",
            "secondary": "#6B7280",
            "success": "#4B5563",
            "warning": "#6B7280",
            "danger": "#374151",
            "info": "#6B7280",
            "bg": "#FFFFFF",
            "bg_secondary": "#F9FAFB",
            "card": "#FFFFFF",
            "text": "#111827",
            "text_secondary": "#4B5563",
            "text_tertiary": "#9CA3AF",
            "border": "#E5E7EB",
            "glass": "#F3F4F6"
        },
        "dark": {
            "primary": "#FFFFFF",
            "secondary": "#9CA3AF",
            "success": "#D1D5DB",
            "warning": "#9CA3AF",
            "danger": "#6B7280",
            "info": "#9CA3AF",
            "bg": "#000000",
            "bg_secondary": "#1F2937",
            "card": "#1F2937",
            "text": "#F9FAFB",
            "text_secondary": "#D1D5DB",
            "text_tertiary": "#9CA3AF",
            "border": "#374151",
            "glass": "#1F2937"
        }
    }

    @classmethod
    def get_theme(cls, name: str = "light") -> dict:
        """الحصول على ألوان السمة"""
        return cls.THEMES.get(name, cls.THEMES["light"])

    @classmethod
    def normalize(cls, text: str) -> str:
        """تطبيع النص العربي"""
        if not text:
            return ""
        
        text = text.strip().lower()[:1000]
        text = re.sub(r"[\u064B-\u065F\u0670]", "", text)
        
        replacements = {
            "أ": "ا", "إ": "ا", "آ": "ا",
            "ى": "ي", "ة": "ه",
            "ؤ": "و", "ئ": "ي"
        }
        for old, new in replacements.items():
            text = text.replace(old, new)
        
        text = re.sub(r"[^\w\sء-ي]", "", text)
        text = re.sub(r"\s+", " ", text).strip()
        
        return text

    @classmethod
    def validate_name(cls, name: str) -> bool:
        """التحقق من صحة الاسم"""
        if not name or len(name) < cls.MIN_NAME_LENGTH or len(name) > cls.MAX_NAME_LENGTH:
            return False
        return bool(re.match(r'^[\u0600-\u06FFa-zA-Z\s]{1,50}$', name.strip()))


if not Config.LINE_SECRET or not Config.LINE_TOKEN:
    raise RuntimeError("LINE credentials missing")
