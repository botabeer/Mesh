import os
import re
from dotenv import load_dotenv

# تحميل متغيرات البيئة من ملف .env
load_dotenv()


class Config:
    """إعدادات التطبيق الاحترافية والموحدة"""

    # ==============================
    # معلومات البوت
    # ==============================
    BOT_NAME = "Bot Mesh"
    VERSION = "15.0"
    AUTHOR = "عبير الدوسري"
    COPYRIGHT = "تم إنشاء هذا البوت بواسطة عبير الدوسري @ 2025"

    # ==============================
    # مفاتيح LINE
    # ==============================
    LINE_SECRET = os.getenv("LINE_CHANNEL_SECRET")
    LINE_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

    if not LINE_SECRET or not LINE_TOKEN:
        raise RuntimeError(
            "LINE credentials are missing. Please set LINE_CHANNEL_SECRET and LINE_CHANNEL_ACCESS_TOKEN"
        )

    # ==============================
    # إعدادات قاعدة البيانات والبورت
    # ==============================
    DB_PATH = os.getenv("DB_PATH", "botmesh.db")
    PORT = int(os.getenv("PORT", 5000))
    WORKERS = int(os.getenv("WORKERS", 4))
    ENV = os.getenv("ENV", "production")  # "development" أو "production"

    # ==============================
    # إعدادات الألعاب
    # ==============================
    QUESTIONS_PER_GAME = 5
    MAX_NAME_LENGTH = 50
    MIN_NAME_LENGTH = 1

    # ==============================
    # الأوامر المحجوزة
    # ==============================
    RESERVED_COMMANDS = {
        "بدايه", "بداية", "العاب", "نقاطي", "الصداره", "الصدارة",
        "ثيم", "مساعده", "مساعدة", "تسجيل", "ايقاف", "انسحب",
        "تغيير الاسم", "تغيير اسمي", "ذكاء", "خمن", "رياضيات",
        "ترتيب", "ضد", "اسرع", "سلسله", "سلسلة", "توافق",
        "انسان حيوان", "تكوين", "اغاني", "الوان",
        "تحدي", "سؤال", "سوال", "اعتراف", "منشن", "موقف",
        "حكمه", "حكمة", "شخصيه", "شخصية", "مافيا"
    }

    # ==============================
    # الثيمات (Themes) المحسنة مع ظل
    # ==============================
    THEMES = {
        "light": {
            "primary": "#2C3E50",
            "secondary": "#4A5A6A",
            "success": "#3D566E",
            "warning": "#7A8A99",
            "danger": "#5C6B7C",
            "info": "#6B7D8C",
            "bg": "#F5F6F7",
            "bg_secondary": "#ECEFF1",
            "card": "#FFFFFF",
            "glass": "#F1F3F5",
            "text": "#2C3E50",
            "text_secondary": "#5A6C7D",
            "text_tertiary": "#7F8C8D",
            "border": "#DDE1E5",
            "shadow": "0 2px 6px rgba(0,0,0,0.1)"  # ظل خفيف للكروت
        },
        "dark": {
            "primary": "#EAEAEA",
            "secondary": "#C0C4C8",
            "success": "#A8B5C3",
            "warning": "#B0BFC8",
            "danger": "#9AAAB3",
            "info": "#B0B5BA",
            "bg": "#121416",
            "bg_secondary": "#1E2328",
            "card": "#1F2429",
            "glass": "#2A2F36",
            "text": "#EAEAEA",
            "text_secondary": "#C0C4C8",
            "text_tertiary": "#9CA3AF",
            "border": "#2E343B",
            "shadow": "0 2px 8px rgba(0,0,0,0.3)"  # ظل أقوى للكروت الداكنة
        },
    }

    # ==============================
    # دوال مساعدة
    # ==============================
    @classmethod
    def get_theme(cls, name: str = "light") -> dict:
        """الحصول على ألوان الثيم، fallback إلى light إذا غير موجود"""
        return cls.THEMES.get(name, cls.THEMES["light"])

    @classmethod
    def normalize(cls, text: str) -> str:
        """تطبيع النص العربي لحذف الحركات وتهيئة الأحرف"""
        if not text:
            return ""
        text = text.strip().lower()[:1000]
        # إزالة الحركات العربية
        text = re.sub(r"[\u064B-\u065F\u0670]", "", text)
        # استبدال بعض الحروف لتوحيد النص
        replacements = {"أ": "ا", "إ": "ا", "آ": "ا", "ى": "ي", "ة": "ه", "ؤ": "و", "ئ": "ي"}
        for old, new in replacements.items():
            text = text.replace(old, new)
        # إزالة الرموز الخاصة باستثناء الأحرف العربية والأرقام والمسافات
        text = re.sub(r"[^\w\sء-ي]", "", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    @classmethod
    def validate_name(cls, name: str) -> bool:
        """التحقق من صحة الاسم حسب الطول والحروف المسموح بها"""
        if not name:
            return False
        name = name.strip()
        if not (cls.MIN_NAME_LENGTH <= len(name) <= cls.MAX_NAME_LENGTH):
            return False
        # يسمح بالأحرف العربية، الإنجليزية، والمسافات
        return bool(re.match(r"^[\u0600-\u06FFa-zA-Z\s]+$", name))
