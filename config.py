import os
import re
from dotenv import load_dotenv

load_dotenv()

class Config:
    """إعدادات البوت"""
    
    BOT_NAME = "Bot Mesh"
    VERSION = "24.0"
    RIGHTS = "عبير الدوسري 2025"
    
    LINE_SECRET = os.getenv("LINE_CHANNEL_SECRET")
    LINE_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
    
    # الثيمات
    THEMES = {
        "أبيض": {
            "bg": "#F2F2F7", "card": "#FFFFFF", "primary": "#007AFF",
            "secondary": "#5AC8FA", "success": "#34C759", "text": "#000000",
            "text2": "#1C1C1E", "text3": "#8E8E93", "border": "#D1D1D6"
        },
        "أسود": {
            "bg": "#000000", "card": "#1C1C1E", "primary": "#0A84FF",
            "secondary": "#64D2FF", "success": "#30D158", "text": "#FFFFFF",
            "text2": "#E5E5EA", "text3": "#8E8E93", "border": "#38383A"
        },
        "أزرق": {
            "bg": "#EBF4FF", "card": "#FFFFFF", "primary": "#0066CC",
            "secondary": "#3399FF", "success": "#28A745", "text": "#001F3F",
            "text2": "#003366", "text3": "#6699CC", "border": "#B3D9FF"
        },
        "بنفسجي": {
            "bg": "#F5F0FF", "card": "#FFFFFF", "primary": "#8B5CF6",
            "secondary": "#A78BFA", "success": "#10B981", "text": "#3B0764",
            "text2": "#5B21B6", "text3": "#A78BFA", "border": "#DDD6FE"
        },
        "وردي": {
            "bg": "#FFF1F2", "card": "#FFFFFF", "primary": "#EC4899",
            "secondary": "#F472B6", "success": "#10B981", "text": "#831843",
            "text2": "#9F1239", "text3": "#F472B6", "border": "#FBCFE8"
        },
        "أخضر": {
            "bg": "#ECFDF5", "card": "#FFFFFF", "primary": "#059669",
            "secondary": "#10B981", "success": "#10B981", "text": "#064E3B",
            "text2": "#065F46", "text3": "#10B981", "border": "#A7F3D0"
        },
        "رمادي": {
            "bg": "#F5F5F5", "card": "#FFFFFF", "primary": "#607D8B",
            "secondary": "#78909C", "success": "#66BB6A", "text": "#263238",
            "text2": "#37474F", "text3": "#90A4AE", "border": "#CFD8DC"
        },
        "أحمر": {
            "bg": "#FEF2F2", "card": "#FFFFFF", "primary": "#DC2626",
            "secondary": "#EF4444", "success": "#10B981", "text": "#7F1D1D",
            "text2": "#991B1B", "text3": "#EF4444", "border": "#FECACA"
        },
        "بني": {
            "bg": "#F5F1ED", "card": "#FFFFFF", "primary": "#8B6F47",
            "secondary": "#A68A64", "success": "#66BB6A", "text": "#3E2723",
            "text2": "#5D4037", "text3": "#A1887F", "border": "#D7CCC8"
        }
    }
    
    # الالعاب
    GAMES = {
        "ذكاء": {"hint": True, "reveal": True},
        "روليت": {"hint": True, "reveal": True},
        "خمن": {"hint": True, "reveal": True},
        "أغنيه": {"hint": True, "reveal": True},
        "ترتيب": {"hint": True, "reveal": True},
        "تكوين": {"hint": True, "reveal": True},
        "ضد": {"hint": True, "reveal": True},
        "لعبة": {"hint": True, "reveal": True},
        "أسرع": {"hint": False, "reveal": False, "timer": 20},
        "سلسلة": {"hint": False, "reveal": False},
        "لون": {"hint": True, "reveal": True},
        "رياضيات": {"hint": True, "reveal": True},
        "توافق": {"hint": False, "reveal": False, "no_registration": True},
        "مافيا": {"hint": False, "reveal": False, "group_only": True}
    }
    
    @classmethod
    def validate(cls):
        """التحقق من الإعدادات"""
        if not cls.LINE_SECRET:
            raise ValueError("LINE_CHANNEL_SECRET مفقود")
        if not cls.LINE_ACCESS_TOKEN:
            raise ValueError("LINE_CHANNEL_ACCESS_TOKEN مفقود")
    
    @classmethod
    def normalize(cls, text: str) -> str:
        """تطبيع النص"""
        if not text:
            return ""
        
        text = text[:1000].strip().lower()
        
        replacements = {
            'أ': 'ا', 'إ': 'ا', 'آ': 'ا',
            'ى': 'ي', 'ة': 'ه', 'ؤ': 'و', 'ئ': 'ي'
        }
        
        for old, new in replacements.items():
            text = text.replace(old, new)
        
        text = re.sub(r'[\u064B-\u065F\u0670]', '', text)
        
        return text
    
    @classmethod
    def get_theme(cls, name: str = None):
        """الحصول على الثيم"""
        return cls.THEMES.get(name, cls.THEMES["أبيض"])
    
    @classmethod
    def is_valid_theme(cls, name: str) -> bool:
        """التحقق من صحة الثيم"""
        return name in cls.THEMES
    
    @classmethod
    def get_game_config(cls, name: str):
        """الحصول على إعدادات اللعبة"""
        return cls.GAMES.get(name, {})
