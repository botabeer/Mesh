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
        "انسان حيوان", "تكوين", "اغاني", "الوان", "مافيا",
        "تحدي", "سؤال", "سوال", "اعتراف", "منشن", "موقف",
        "حكمه", "حكمة", "شخصيه", "شخصية"
    }

    THEMES = {
        "light": {
            "primary": "#2D3748",
            "secondary": "#4A5568",
            "accent": "#718096",
            "success": "#48BB78",
            "warning": "#ECC94B",
            "danger": "#F56565",
            "info": "#4299E1",
            
            "bg": "#F7FAFC",
            "bg_secondary": "#EDF2F7",
            "bg_tertiary": "#E2E8F0",
            
            "card": "rgba(255, 255, 255, 0.95)",
            "card_secondary": "rgba(255, 255, 255, 0.85)",
            "glass": "rgba(255, 255, 255, 0.75)",
            "glass_strong": "rgba(255, 255, 255, 0.9)",
            
            "text": "#1A202C",
            "text_secondary": "#4A5568",
            "text_tertiary": "#718096",
            "text_muted": "#A0AEC0",
            
            "border": "rgba(226, 232, 240, 0.8)",
            "border_light": "rgba(237, 242, 247, 0.6)",
            
            "overlay": "rgba(0, 0, 0, 0.5)",
            
            "shadow_sm": "0 2px 4px rgba(0, 0, 0, 0.06)",
            "shadow": "0 4px 12px rgba(0, 0, 0, 0.08)",
            "shadow_md": "0 6px 16px rgba(0, 0, 0, 0.1)",
            "shadow_lg": "0 10px 24px rgba(0, 0, 0, 0.12), 0 2px 8px rgba(0, 0, 0, 0.08)",
            "shadow_xl": "0 20px 40px rgba(0, 0, 0, 0.15), 0 4px 12px rgba(0, 0, 0, 0.1)",
            
            "gradient_primary": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
            "gradient_secondary": "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)",
            "gradient_success": "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)",
            "gradient_warm": "linear-gradient(135deg, #fa709a 0%, #fee140 100%)",
            "gradient_cool": "linear-gradient(135deg, #30cfd0 0%, #330867 100%)",
        },
        
        "dark": {
            "primary": "#E2E8F0",
            "secondary": "#CBD5E0",
            "accent": "#A0AEC0",
            "success": "#68D391",
            "warning": "#F6E05E",
            "danger": "#FC8181",
            "info": "#63B3ED",
            
            "bg": "#0F1419",
            "bg_secondary": "#1A202C",
            "bg_tertiary": "#2D3748",
            
            "card": "rgba(26, 32, 44, 0.95)",
            "card_secondary": "rgba(45, 55, 72, 0.85)",
            "glass": "rgba(26, 32, 44, 0.75)",
            "glass_strong": "rgba(26, 32, 44, 0.9)",
            
            "text": "#F7FAFC",
            "text_secondary": "#E2E8F0",
            "text_tertiary": "#CBD5E0",
            "text_muted": "#718096",
            
            "border": "rgba(74, 85, 104, 0.6)",
            "border_light": "rgba(45, 55, 72, 0.4)",
            
            "overlay": "rgba(0, 0, 0, 0.7)",
            
            "shadow_sm": "0 2px 4px rgba(0, 0, 0, 0.3)",
            "shadow": "0 4px 12px rgba(0, 0, 0, 0.4)",
            "shadow_md": "0 6px 16px rgba(0, 0, 0, 0.5)",
            "shadow_lg": "0 10px 24px rgba(0, 0, 0, 0.6), 0 2px 8px rgba(0, 0, 0, 0.4)",
            "shadow_xl": "0 20px 40px rgba(0, 0, 0, 0.7), 0 4px 12px rgba(0, 0, 0, 0.5)",
            
            "gradient_primary": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
            "gradient_secondary": "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)",
            "gradient_success": "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)",
            "gradient_warm": "linear-gradient(135deg, #fa709a 0%, #fee140 100%)",
            "gradient_cool": "linear-gradient(135deg, #30cfd0 0%, #330867 100%)",
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
