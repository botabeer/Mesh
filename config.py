import os
import re
from dotenv import load_dotenv

load_dotenv()


class Config:
    """اعدادات التطبيق المحسّنة"""
    
    BOT_NAME = "Bot Mesh"
    VERSION = "14.0"
    COPYRIGHT = "تم انشاء هذا البوت بواسطة عبير الدوسري @ 2025"
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
        "ثيم", "مساعده", "مساعدة", "تسجيل", "ايقاف",
        "تغيير الاسم", "تغيير اسمي", "ذكاء", "خمن", "رياضيات",
        "ترتيب", "ضد", "اسرع", "سلسله", "سلسلة", "توافق",
        "انسان حيوان", "كون كلمات", "اغاني", "الوان",
        "تحدي", "سؤال", "سوال", "اعتراف", "منشن", "موقف", 
        "حكمه", "حكمة", "شخصيه", "شخصية", "مافيا"
    }

    THEMES = {
        "light": {
            "primary": "#2563EB",
            "secondary": "#64748B",
            "success": "#10B981",
            "warning": "#F59E0B",
            "danger": "#EF4444",
            "error": "#DC2626",
            "info": "#3B82F6",
            "bg": "#FFFFFF",
            "bg_secondary": "#F8FAFC",
            "card": "#FFFFFF",
            "text": "#0F172A",
            "text_secondary": "#475569",
            "text_tertiary": "#94A3B8",
            "border": "#E2E8F0",
            "glass": "#F1F5F9"
        },
        "dark": {
            "primary": "#60A5FA",
            "secondary": "#94A3B8",
            "success": "#34D399",
            "warning": "#FBBF24",
            "danger": "#F87171",
            "error": "#EF4444",
            "info": "#60A5FA",
            "bg": "#0F172A",
            "bg_secondary": "#1E293B",
            "card": "#1E293B",
            "text": "#F1F5F9",
            "text_secondary": "#CBD5E1",
            "text_tertiary": "#94A3B8",
            "border": "#334155",
            "glass": "#1E293B"
        }
    }

    @classmethod
    def get_theme(cls, name: str = "light") -> dict:
        """الحصول على الوان السمة"""
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
