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
            "primary": "#000000",
            "secondary": "#333333",
            "accent": "#666666",
            "success": "#2D2D2D",
            "warning": "#595959",
            "danger": "#1A1A1A",
            "info": "#404040",
            
            "bg": "#FFFFFF",
            "bg_secondary": "#F8F8F8",
            "bg_tertiary": "#F0F0F0",
            
            "card": "#FFFFFF",
            "card_secondary": "#FAFAFA",
            "glass": "#F5F5F5",
            "glass_strong": "#FFFFFF",
            
            "text": "#000000",
            "text_secondary": "#4D4D4D",
            "text_tertiary": "#737373",
            "text_muted": "#999999",
            
            "border": "#E0E0E0",
            "border_light": "#EBEBEB",
            
            "overlay": "#000000",
            
            "shadow_sm": "0 1px 2px rgba(0, 0, 0, 0.05)",
            "shadow": "0 2px 4px rgba(0, 0, 0, 0.08)",
            "shadow_md": "0 4px 6px rgba(0, 0, 0, 0.1)",
            "shadow_lg": "0 8px 16px rgba(0, 0, 0, 0.12)",
            "shadow_xl": "0 12px 24px rgba(0, 0, 0, 0.15)",
            
            "gradient_primary": "linear-gradient(135deg, #333333 0%, #000000 100%)",
            "gradient_secondary": "linear-gradient(135deg, #666666 0%, #333333 100%)",
            "gradient_success": "linear-gradient(135deg, #4D4D4D 0%, #2D2D2D 100%)",
        },
        
        "dark": {
            "primary": "#FFFFFF",
            "secondary": "#CCCCCC",
            "accent": "#999999",
            "success": "#D2D2D2",
            "warning": "#A6A6A6",
            "danger": "#E5E5E5",
            "info": "#BFBFBF",
            
            "bg": "#000000",
            "bg_secondary": "#0A0A0A",
            "bg_tertiary": "#1A1A1A",
            
            "card": "#0D0D0D",
            "card_secondary": "#1A1A1A",
            "glass": "#141414",
            "glass_strong": "#1F1F1F",
            
            "text": "#FFFFFF",
            "text_secondary": "#B3B3B3",
            "text_tertiary": "#8C8C8C",
            "text_muted": "#666666",
            
            "border": "#2D2D2D",
            "border_light": "#1A1A1A",
            
            "overlay": "#000000",
            
            "shadow_sm": "0 1px 2px rgba(0, 0, 0, 0.3)",
            "shadow": "0 2px 4px rgba(0, 0, 0, 0.4)",
            "shadow_md": "0 4px 6px rgba(0, 0, 0, 0.5)",
            "shadow_lg": "0 8px 16px rgba(0, 0, 0, 0.6)",
            "shadow_xl": "0 12px 24px rgba(0, 0, 0, 0.7)",
            
            "gradient_primary": "linear-gradient(135deg, #FFFFFF 0%, #CCCCCC 100%)",
            "gradient_secondary": "linear-gradient(135deg, #999999 0%, #CCCCCC 100%)",
            "gradient_success": "linear-gradient(135deg, #B3B3B3 0%, #D2D2D2 100%)",
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
