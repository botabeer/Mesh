import os
import re
from dotenv import load_dotenv

load_dotenv()


class Config:
    """إعدادات التطبيق المحسّنة"""
    
    # معلومات التطبيق
    BOT_NAME = "Bot Mesh"
    VERSION = "13.0"
    COPYRIGHT = "تم إنشاء هذا البوت بواسطة عبير الدوسري @ 2025"
    AUTHOR = "عبير الدوسري"

    # بيانات LINE API
    LINE_SECRET = os.getenv("LINE_CHANNEL_SECRET")
    LINE_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

    # إعدادات الخادم
    DB_PATH = os.getenv("DB_PATH", "botmesh.db")
    PORT = int(os.getenv("PORT", 5000))
    WORKERS = int(os.getenv("WORKERS", 4))
    ENV = os.getenv("ENV", "production")

    # إعدادات الألعاب
    QUESTIONS_PER_GAME = 5
    MAX_NAME_LENGTH = 50
    MIN_NAME_LENGTH = 1

    # الأوامر المحجوزة
    RESERVED_COMMANDS = {
        "بدايه", "بداية", "العاب", "نقاطي", "الصداره", "الصدارة",
        "ثيم", "مساعده", "مساعدة", "تسجيل", "انسحب", "ايقاف",
        "تغيير الاسم", "تغيير اسمي", "ذكاء", "خمن", "رياضيات",
        "ترتيب", "ضد", "اسرع", "سلسله", "سلسلة", "توافق",
        "انسان حيوان", "كون كلمات", "اغاني", "الوان",
        "تحدي", "سؤال", "سوال", "اعتراف", "منشن", "موقف", 
        "حكمه", "حكمة", "شخصيه", "شخصية", "مافيا"
    }

    # السمات المحسّنة
    THEMES = {
        "light": {
            "primary": "#2C3E50",
            "secondary": "#5D6D7E",
            "success": "#27AE60",
            "warning": "#F39C12",
            "danger": "#E74C3C",
            "error": "#C0392B",
            "info": "#3498DB",
            "bg": "#FFFFFF",
            "bg_secondary": "#F8F9FA",
            "card": "#FFFFFF",
            "text": "#1A1A1A",
            "text_secondary": "#4A4A4A",
            "text_tertiary": "#7A7A7A",
            "border": "#E0E0E0",
            "glass": "#F5F7FA"
        },
        "dark": {
            "primary": "#ECF0F1",
            "secondary": "#BDC3C7",
            "success": "#2ECC71",
            "warning": "#F1C40F",
            "danger": "#E74C3C",
            "error": "#C0392B",
            "info": "#3498DB",
            "bg": "#1A1A1A",
            "bg_secondary": "#2C2C2C",
            "card": "#2C2C2C",
            "text": "#F5F5F5",
            "text_secondary": "#D5D5D5",
            "text_tertiary": "#A5A5A5",
            "border": "#3A3A3A",
            "glass": "#252525"
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
        
        # إزالة التشكيل
        text = re.sub(r"[\u064B-\u065F\u0670]", "", text)
        
        # توحيد الحروف المتشابهة
        replacements = {
            "أ": "ا", "إ": "ا", "آ": "ا",
            "ى": "ي", "ة": "ه",
            "ؤ": "و", "ئ": "ي"
        }
        for old, new in replacements.items():
            text = text.replace(old, new)
        
        # إزالة الرموز الخاصة
        text = re.sub(r"[^\w\sء-ي]", "", text)
        
        # إزالة المسافات الزائدة
        text = re.sub(r"\s+", " ", text).strip()
        
        return text

    @classmethod
    def validate_name(cls, name: str) -> bool:
        """التحقق من صحة الاسم"""
        if not name or len(name) < cls.MIN_NAME_LENGTH or len(name) > cls.MAX_NAME_LENGTH:
            return False
        
        return bool(re.match(r'^[\u0600-\u06FFa-zA-Z\s]{1,50}$', name.strip()))


# التحقق من وجود بيانات الاعتماد
if not Config.LINE_SECRET or not Config.LINE_TOKEN:
    raise RuntimeError("LINE credentials missing")
