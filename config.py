import os
import re
from dotenv import load_dotenv

load_dotenv()


class Config:
    """إعدادات التطبيق المحسّنة"""
    
    # معلومات التطبيق
    BOT_NAME = "Bot Mesh"
    VERSION = "12.0"
    COPYRIGHT = "Created by Abeer Aldosari 2025"

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
    MIN_NAME_LENGTH = 2

    # الأوامر المحجوزة
    RESERVED_COMMANDS = {
        "بدايه", "بداية", "العاب", "نقاطي", "الصداره", "الصدارة",
        "ثيم", "مساعده", "مساعدة", "تسجيل", "انسحب", "ايقاف",
        "تغيير الاسم", "تغيير اسمي", "ذكاء", "خمن", "رياضيات",
        "ترتيب", "ضد", "اسرع", "سلسله", "سلسلة", "توافق",
        "انسان حيوان", "كون كلمات", "اغاني", "الوان",
        "تحدي", "سؤال", "سوال", "اعتراف", "منشن", "موقف", 
        "حكمه", "حكمة", "شخصيه", "شخصية"
    }

    # السمات المحسّنة (أبيض، أسود، رمادي)
    THEMES = {
        "light": {
            "primary": "#374151",      # رمادي داكن
            "secondary": "#6B7280",    # رمادي متوسط
            "success": "#4B5563",      # رمادي للنجاح
            "warning": "#9CA3AF",      # رمادي فاتح
            "danger": "#1F2937",       # رمادي داكن جداً
            "error": "#1F2937",
            "info": "#6B7280",
            "bg": "#FFFFFF",           # أبيض
            "bg_secondary": "#F9FAFB",
            "card": "#FFFFFF",
            "text": "#111827",         # أسود تقريباً
            "text_secondary": "#374151",
            "text_tertiary": "#9CA3AF",
            "border": "#E5E7EB",
            "glass": "#F9FAFB"
        },
        "dark": {
            "primary": "#D1D5DB",      # رمادي فاتح
            "secondary": "#9CA3AF",    # رمادي متوسط
            "success": "#D1D5DB",
            "warning": "#6B7280",
            "danger": "#E5E7EB",
            "error": "#E5E7EB",
            "info": "#9CA3AF",
            "bg": "#111827",           # أسود تقريباً
            "bg_secondary": "#1F2937",
            "card": "#1F2937",
            "text": "#F9FAFB",         # أبيض تقريباً
            "text_secondary": "#D1D5DB",
            "text_tertiary": "#6B7280",
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
        
        return bool(re.match(r'^[\u0600-\u06FFa-zA-Z\s]{2,50}$', name.strip()))


# التحقق من وجود بيانات الاعتماد
if not Config.LINE_SECRET or not Config.LINE_TOKEN:
    raise RuntimeError("LINE credentials missing")
