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
            # iOS Light Theme - ألوان نظيفة ومريحة
            "primary": "#007AFF",           # أزرق iOS
            "secondary": "#8E8E93",         # رمادي ثانوي
            "success": "#34C759",           # أخضر iOS
            "warning": "#FF9500",           # برتقالي iOS
            "danger": "#FF3B30",            # أحمر iOS
            "info": "#5AC8FA",              # أزرق فاتح
            
            # خلفيات
            "bg": "#FFFFFF",                # أبيض نقي
            "bg_secondary": "#F2F2F7",      # رمادي فاتح جداً
            "card": "#FFFFFF",              # أبيض للكروت
            "glass": "#F9F9F9",             # زجاجي فاتح
            
            # نصوص
            "text": "#000000",              # أسود للنصوص الرئيسية
            "text_secondary": "#3C3C43",    # رمادي داكن للثانوي
            "text_tertiary": "#8E8E93",     # رمادي فاتح للتفاصيل
            
            # حدود
            "border": "#E5E5EA",            # حدود رمادية فاتحة
        },
        "dark": {
            # iOS Dark Theme - ألوان داكنة أنيقة
            "primary": "#0A84FF",           # أزرق iOS الداكن
            "secondary": "#98989D",         # رمادي ثانوي
            "success": "#32D74B",           # أخضر iOS الداكن
            "warning": "#FF9F0A",           # برتقالي iOS الداكن
            "danger": "#FF453A",            # أحمر iOS الداكن
            "info": "#64D2FF",              # أزرق فاتح
            
            # خلفيات
            "bg": "#000000",                # أسود نقي
            "bg_secondary": "#1C1C1E",      # رمادي داكن جداً
            "card": "#1C1C1E",              # رمادي داكن للكروت
            "glass": "#2C2C2E",             # زجاجي داكن
            
            # نصوص
            "text": "#FFFFFF",              # أبيض للنصوص الرئيسية
            "text_secondary": "#EBEBF5",    # رمادي فاتح للثانوي
            "text_tertiary": "#98989D",     # رمادي للتفاصيل
            
            # حدود
            "border": "#38383A",            # حدود رمادية داكنة
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
