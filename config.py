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
            # ثيم فاتح - أبيض ورمادي
            "primary": "#000000",           # أسود للعناصر المهمة
            "secondary": "#6B7280",         # رمادي متوسط
            "success": "#111827",           # أسود داكن للنجاح
            "warning": "#374151",           # رمادي داكن للتحذير
            "danger": "#1F2937",            # رمادي داكن جداً للخطر
            "info": "#4B5563",              # رمادي للمعلومات
            
            # خلفيات
            "bg": "#FFFFFF",                # أبيض نقي
            "bg_secondary": "#F9FAFB",      # رمادي فاتح جداً
            "card": "#FFFFFF",              # أبيض للكروت
            "glass": "#F3F4F6",             # رمادي فاتح شفاف
            
            # نصوص
            "text": "#000000",              # أسود للنصوص الرئيسية
            "text_secondary": "#374151",    # رمادي داكن للثانوي
            "text_tertiary": "#9CA3AF",     # رمادي فاتح للتفاصيل
            
            # حدود
            "border": "#E5E7EB",            # حدود رمادية فاتحة
        },
        "dark": {
            # ثيم داكن - أسود ورمادي
            "primary": "#FFFFFF",           # أبيض للعناصر المهمة
            "secondary": "#9CA3AF",         # رمادي فاتح
            "success": "#F3F4F6",           # رمادي فاتح جداً للنجاح
            "warning": "#D1D5DB",           # رمادي فاتح للتحذير
            "danger": "#E5E7EB",            # رمادي فاتح جداً للخطر
            "info": "#B0B5BA",              # رمادي للمعلومات
            
            # خلفيات
            "bg": "#000000",                # أسود نقي
            "bg_secondary": "#111827",      # رمادي داكن جداً
            "card": "#1F2937",              # رمادي داكن للكروت
            "glass": "#374151",             # رمادي متوسط شفاف
            
            # نصوص
            "text": "#FFFFFF",              # أبيض للنصوص الرئيسية
            "text_secondary": "#D1D5DB",    # رمادي فاتح للثانوي
            "text_tertiary": "#9CA3AF",     # رمادي متوسط للتفاصيل
            
            # حدود
            "border": "#374151",            # حدود رمادية داكنة
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
