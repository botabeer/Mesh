import os
import re
from dotenv import load_dotenv

load_dotenv()


class Config:
    """إعدادات التطبيق الرئيسية"""
    
    # معلومات التطبيق
    BOT_NAME = "Bot Mesh"
    VERSION = "11.0"
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
        "انسان حيوان", "كون كلمات", "اغاني", "الوان", "مافيا",
        "تحدي", "سؤال", "سوال", "اعتراف", "منشن", "موقف", 
        "حكمه", "حكمة", "شخصيه", "شخصية"
    }

    # الأوامر الرئيسية
    MAIN_COMMANDS = {
        "بدايه", "بداية", "العاب", "نقاطي", "الصداره", "الصدارة",
        "ثيم", "مساعده", "مساعدة", "تسجيل", "تغيير الاسم", "تغيير اسمي"
    }

    # السمات (Themes)
    THEMES = {
        "light": {
            "primary": "#2196F3",
            "secondary": "#5C6BC0",
            "success": "#4CAF50",
            "warning": "#FF9800",
            "danger": "#F44336",
            "error": "#F44336",
            "info": "#00BCD4",
            "bg": "#FAFAFA",
            "bg_secondary": "#FFFFFF",
            "card": "#FFFFFF",
            "text": "#212121",
            "text_secondary": "#616161",
            "text_tertiary": "#9E9E9E",
            "border": "#E0E0E0",
            "glass": "#F5F5F5"
        },
        "dark": {
            "primary": "#42A5F5",
            "secondary": "#7E57C2",
            "success": "#66BB6A",
            "warning": "#FFA726",
            "danger": "#EF5350",
            "error": "#EF5350",
            "info": "#26C6DA",
            "bg": "#121212",
            "bg_secondary": "#1E1E1E",
            "card": "#1E1E1E",
            "text": "#FFFFFF",
            "text_secondary": "#E0E0E0",
            "text_tertiary": "#9E9E9E",
            "border": "#2C2C2C",
            "glass": "#242424"
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
        
        # السماح بالعربية والإنجليزية والمسافات فقط
        return bool(re.match(r'^[\u0600-\u06FFa-zA-Z\s]{2,50}$', name.strip()))


# التحقق من وجود بيانات الاعتماد
if not Config.LINE_SECRET or not Config.LINE_TOKEN:
    raise RuntimeError("LINE credentials missing. Please set LINE_CHANNEL_SECRET and LINE_CHANNEL_ACCESS_TOKEN")
