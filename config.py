import os
import re
from dotenv import load_dotenv

load_dotenv()


class Config:
    # App Info
    BOT_NAME = "Bot Mesh"
    VERSION = "10.1"
    COPYRIGHT = "Created by Abeer Aldosari 2025"

    # LINE Credentials
    LINE_SECRET = os.getenv("LINE_CHANNEL_SECRET")
    LINE_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

    # Server / DB
    DB_PATH = os.getenv("DB_PATH", "botmesh.db")
    PORT = int(os.getenv("PORT", 5000))
    WORKERS = int(os.getenv("WORKERS", 4))
    ENV = os.getenv("ENV", "production")

    # Game Settings
    QUESTIONS_PER_GAME = 5
    MAX_NAME_LENGTH = 50
    MIN_NAME_LENGTH = 2

    # الأوامر المحجوزة (لا تقبل كأسماء)
    RESERVED_COMMANDS = {
        "بدايه", "بداية",
        "العاب",
        "نقاطي",
        "الصداره", "الصدارة",
        "ثيم",
        "مساعده", "مساعدة",
        "تسجيل",
        "انسحب",
        "ايقاف",
        "تغيير الاسم", "تغيير اسمي",
        # أسماء الألعاب
        "ذكاء",
        "خمن",
        "رياضيات",
        "ترتيب",
        "ضد",
        "اسرع",
        "سلسله", "سلسلة",
        "انسان حيوان",
        "كون كلمات",
        "اغاني",
        "الوان",
        "مافيا",
        "توافق",
        "صواب خطا",
        # محتوى تفاعلي
        "تحدي",
        "سؤال", "سوال",
        "اعتراف",
        "منشن",
        "موقف",
        "حكمه", "حكمة",
        "شخصيه", "شخصية"
    }

    # أوامر رئيسية (تجاهلها داخل اللعبة)
    MAIN_COMMANDS = {
        "بدايه", "بداية",
        "العاب",
        "نقاطي",
        "الصداره", "الصدارة",
        "ثيم",
        "مساعده", "مساعدة",
        "تسجيل",
        "تغيير الاسم", "تغيير اسمي"
    }

    # Themes
    THEMES = {
        "light": {
            "primary": "#007AFF",
            "secondary": "#5856D6",
            "success": "#34C759",
            "warning": "#FF9500",
            "danger": "#FF3B30",
            "info": "#5AC8FA",
            "bg": "#F2F2F7",
            "bg_secondary": "#FFFFFF",
            "card": "#FFFFFF",
            "text": "#000000",
            "text_secondary": "#3C3C43",
            "text_tertiary": "#8E8E93",
            "border": "#E5E5EA",
            "glass": "#F8F8F8"
        },
        "dark": {
            "primary": "#0A84FF",
            "secondary": "#5E5CE6",
            "success": "#30D158",
            "warning": "#FF9F0A",
            "danger": "#FF453A",
            "info": "#64D2FF",
            "bg": "#000000",
            "bg_secondary": "#1C1C1E",
            "card": "#1C1C1E",
            "text": "#FFFFFF",
            "text_secondary": "#EBEBF5",
            "text_tertiary": "#98989D",
            "border": "#3A3A3C",
            "glass": "#2C2C2E"
        }
    }

    @classmethod
    def get_theme(cls, name: str = "light"):
        return cls.THEMES.get(name, cls.THEMES["light"])

    @classmethod
    def normalize(cls, text: str) -> str:
        """تطبيع موحّد للنصوص العربية"""
        if not text:
            return ""

        text = text.strip().lower()
        text = text[:1000]

        # إزالة التشكيل
        text = re.sub(r"[\u064B-\u065F\u0670]", "", text)

        # توحيد الحروف
        replacements = {
            "أ": "ا", "إ": "ا", "آ": "ا",
            "ى": "ي", "ة": "ه",
            "ؤ": "و", "ئ": "ي"
        }
        for old, new in replacements.items():
            text = text.replace(old, new)

        # تنظيف الرموز
        text = re.sub(r"[^\w\sء-ي]", "", text)

        # تنظيف المسافات
        text = re.sub(r"\s+", " ", text).strip()

        return text


# Startup Validation
if not Config.LINE_SECRET or not Config.LINE_TOKEN:
    raise RuntimeError("LINE credentials missing")
