import os
import re
from dotenv import load_dotenv

load_dotenv()


class Config:
    BOT_NAME = "Bot Mesh"
    VERSION = "16.0"
    AUTHOR = "عبير الدوسري"
    COPYRIGHT = "تم إنشاء هذا البوت بواسطة عبير الدوسري @ 2025"

    LINE_SECRET = os.getenv("LINE_CHANNEL_SECRET")
    LINE_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

    if not LINE_SECRET or not LINE_TOKEN:
        raise RuntimeError("LINE credentials missing")

    DB_PATH = os.getenv("DB_PATH", "botmesh.db")
    PORT = int(os.getenv("PORT", 5000))
    WORKERS = int(os.getenv("WORKERS", 4))
    ENV = os.getenv("ENV", "production")

    QUESTIONS_PER_GAME = 5
    MAX_MESSAGE_LENGTH = 5000

    MAX_NAME_LENGTH = 50
    MIN_NAME_LENGTH = 1

    RATE_LIMIT_REQUESTS = 20
    RATE_LIMIT_WINDOW = 60

    # أوامر محجوزة (تمنع استخدامها كاسم)
    RESERVED_COMMANDS = {
        "بدايه", "بداية", "العاب", "نقاطي", "الصداره", "الصدارة",
        "ثيم", "مساعده", "مساعدة", "تسجيل", "ايقاف", "انسحب",
        "تغيير الاسم", "تغيير اسمي",

        # الألعاب
        "ذكاء", "خمن", "رياضيات", "ترتيب", "ضد", "اسرع",
        "سلسله", "سلسلة", "توافق", "انسان حيوان", "تكوين",
        "اغاني", "الوان", "مافيا",

        # النصوص
        "تحدي", "سؤال", "سوال", "اعتراف", "منشن", "موقف",
        "حكمه", "حكمة", "شخصيه", "شخصية"
    }

    THEMES = {
        "light": {
            "primary": "#2C3E50",
            "secondary": "#4A5A6A",
            "success": "#16A34A",
            "warning": "#CA8A04",
            "danger": "#DC2626",
            "info": "#2563EB",
            "bg": "#F5F6F7",
            "bg_secondary": "#ECEFF1",
            "card": "#FFFFFF",
            "glass": "#F1F3F5",
            "text": "#2C3E50",
            "text_secondary": "#5A6C7D",
            "text_tertiary": "#7F8C8D",
            "border": "#DDE1E5",
            "shadow": "0 2px 6px rgba(0,0,0,0.1)",
        },
        "dark": {
            "primary": "#60A5FA",
            "secondary": "#94A3B8",
            "success": "#4ADE80",
            "warning": "#FBBF24",
            "danger": "#F87171",
            "info": "#60A5FA",
            "bg": "#0F172A",
            "bg_secondary": "#1E293B",
            "card": "#1E293B",
            "glass": "#334155",
            "text": "#F1F5F9",
            "text_secondary": "#CBD5E1",
            "text_tertiary": "#94A3B8",
            "border": "#334155",
            "shadow": "0 2px 8px rgba(0,0,0,0.4)",
        },
    }

    # ================= Utils =================

    @classmethod
    def get_theme(cls, name="light"):
        return cls.THEMES.get(name, cls.THEMES["light"])

    @classmethod
    def normalize(cls, text):
        if not text:
            return ""
        text = str(text).strip()[:1000].lower()
        text = re.sub(r"[\u064B-\u065F\u0670]", "", text)

        replace_map = {
            "أ": "ا", "إ": "ا", "آ": "ا", "ٱ": "ا",
            "ى": "ي", "ة": "ه", "ؤ": "و", "ئ": "ي"
        }
        for a, b in replace_map.items():
            text = text.replace(a, b)

        text = re.sub(r"[^\w\sء-ي]", "", text, flags=re.UNICODE)
        return re.sub(r"\s+", " ", text).strip()

    @classmethod
    def validate_name(cls, name):
        if not isinstance(name, str):
            return False

        name = name.strip()
        if not (cls.MIN_NAME_LENGTH <= len(name) <= cls.MAX_NAME_LENGTH):
            return False

        if not re.fullmatch(r"[\u0600-\u06FFa-zA-Z\s]+", name):
            return False

        if name.lower() in {"admin", "bot", "system", "root"}:
            return False

        return True

    @classmethod
    def sanitize_text(cls, text, max_length=1000):
        if not text:
            return ""
        text = str(text)[:max_length]
        return re.sub(r"[\x00-\x1f\x7f-\x9f]", "", text).strip()
