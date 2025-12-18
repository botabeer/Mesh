import os
import re
from dotenv import load_dotenv

load_dotenv()

class Config:
    BOT_NAME = "Bot Mesh"
    VERSION = "17.0"
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

    RESERVED_COMMANDS = {
        "بدايه", "بداية", "العاب", "نقاطي", "الصداره", "الصدارة",
        "ثيم", "مساعده", "مساعدة", "تسجيل", "ايقاف", "انسحب",
        "تغيير الاسم", "تغيير اسمي", "ذكاء", "خمن", "رياضيات", 
        "ترتيب", "ضد", "اسرع", "سلسله", "سلسلة", "توافق", 
        "لعبه", "لعبة", "تكوين", "اغاني", "الوان", "مافيا",
        "تحدي", "سؤال", "سوال", "اعتراف", "منشن", "موقف",
        "حكمه", "حكمة", "شخصيه", "شخصية"
    }

    THEMES = {
        "light": {
            "primary": "#FFFFFF",
            "secondary": "#CCCCCC",
            "accent": "#999999",
            
            "bg": "#000000",
            "bg_secondary": "#0A0A0A",
            "bg_tertiary": "#1A1A1A",
            
            "card": "#000000",
            "card_secondary": "#0D0D0D",
            "glass": "#141414",
            
            "text": "#FFFFFF",
            "text_secondary": "#CCCCCC",
            "text_tertiary": "#999999",
            
            "border": "#333333",
            "border_light": "#1A1A1A",
        },
        
        "dark": {
            "primary": "#FFFFFF",
            "secondary": "#CCCCCC",
            "accent": "#999999",
            
            "bg": "#000000",
            "bg_secondary": "#0A0A0A",
            "bg_tertiary": "#1A1A1A",
            
            "card": "#000000",
            "card_secondary": "#0D0D0D",
            "glass": "#141414",
            
            "text": "#FFFFFF",
            "text_secondary": "#CCCCCC",
            "text_tertiary": "#999999",
            
            "border": "#333333",
            "border_light": "#1A1A1A",
        },
    }

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
