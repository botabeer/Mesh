import os
import re
from dotenv import load_dotenv

load_dotenv()


class Config:
    BOT_NAME = "Bot Mesh"
    VERSION = "24.1"
    RIGHTS = "عبير الدوسري 2025"

    LINE_SECRET = os.getenv("LINE_CHANNEL_SECRET")
    LINE_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

    DATABASE_PATH = "botmesh.db"
    DATABASE_CLEANUP_DAYS = 90

    DEFAULT_PORT = 10000

    RATE_LIMIT_MESSAGES = 30
    RATE_LIMIT_WINDOW = 60

    THEMES = {
        "ابيض": {"bg": "#FFFFFF", "card": "#F8F9FA", "primary": "#007AFF", 
                 "secondary": "#5AC8FA", "success": "#34C759", "text": "#000000", 
                 "text2": "#333333", "text3": "#666666", "border": "#DDDDDD", 
                 "error": "#FF3B30", "warning": "#FF9500"},
        "اسود": {"bg": "#000000", "card": "#1C1C1E", "primary": "#0A84FF", 
                 "secondary": "#64D2FF", "success": "#30D158", "text": "#FFFFFF", 
                 "text2": "#E5E5EA", "text3": "#8E8E93", "border": "#38383A", 
                 "error": "#FF453A", "warning": "#FFD60A"},
        "ازرق": {"bg": "#E3F2FD", "card": "#FFFFFF", "primary": "#2196F3", 
                 "secondary": "#03A9F4", "success": "#4CAF50", "text": "#000000", 
                 "text2": "#424242", "text3": "#757575", "border": "#90CAF9", 
                 "error": "#F44336", "warning": "#FF9800"},
        "بنفسجي": {"bg": "#F3E5F5", "card": "#FFFFFF", "primary": "#9C27B0", 
                   "secondary": "#BA68C8", "success": "#66BB6A", "text": "#000000", 
                   "text2": "#424242", "text3": "#757575", "border": "#CE93D8", 
                   "error": "#F44336", "warning": "#FF9800"},
        "وردي": {"bg": "#FCE4EC", "card": "#FFFFFF", "primary": "#E91E63", 
                 "secondary": "#F06292", "success": "#66BB6A", "text": "#000000", 
                 "text2": "#424242", "text3": "#757575", "border": "#F8BBD0", 
                 "error": "#F44336", "warning": "#FF9800"},
        "اخضر": {"bg": "#E8F5E9", "card": "#FFFFFF", "primary": "#4CAF50", 
                 "secondary": "#66BB6A", "success": "#8BC34A", "text": "#000000", 
                 "text2": "#424242", "text3": "#757575", "border": "#A5D6A7", 
                 "error": "#F44336", "warning": "#FF9800"},
        "رمادي": {"bg": "#F5F5F5", "card": "#FFFFFF", "primary": "#607D8B", 
                  "secondary": "#78909C", "success": "#4CAF50", "text": "#000000", 
                  "text2": "#424242", "text3": "#757575", "border": "#BDBDBD", 
                  "error": "#F44336", "warning": "#FF9800"},
        "احمر": {"bg": "#FFEBEE", "card": "#FFFFFF", "primary": "#F44336", 
                 "secondary": "#EF5350", "success": "#66BB6A", "text": "#000000", 
                 "text2": "#424242", "text3": "#757575", "border": "#FFCDD2", 
                 "error": "#D32F2F", "warning": "#FF9800"},
        "بني": {"bg": "#EFEBE9", "card": "#FFFFFF", "primary": "#795548", 
                "secondary": "#8D6E63", "success": "#66BB6A", "text": "#000000", 
                "text2": "#424242", "text3": "#757575", "border": "#BCAAA4", 
                "error": "#F44336", "warning": "#FF9800"}
    }

    DEFAULT_THEME = "ابيض"

    GAMES = {
        "ذكاء": {"requires_registration": True, "group_only": False},
        "روليت": {"requires_registration": True, "group_only": False},
        "خمن": {"requires_registration": True, "group_only": False},
        "اغنيه": {"requires_registration": True, "group_only": False},
        "ترتيب": {"requires_registration": True, "group_only": False},
        "تكوين": {"requires_registration": True, "group_only": False},
        "ضد": {"requires_registration": True, "group_only": False},
        "لعبة": {"requires_registration": True, "group_only": False},
        "اسرع": {"requires_registration": True, "group_only": False},
        "سلسلة": {"requires_registration": True, "group_only": False},
        "لون": {"requires_registration": True, "group_only": False},
        "رياضيات": {"requires_registration": True, "group_only": False},
        "توافق": {"requires_registration": False, "group_only": False},
        "مافيا": {"requires_registration": False, "group_only": True},
        "سؤال": {"requires_registration": False, "group_only": False},
        "منشن": {"requires_registration": False, "group_only": False},
        "تحدي": {"requires_registration": False, "group_only": False},
        "اعتراف": {"requires_registration": False, "group_only": False}
    }

    @classmethod
    def validate(cls):
        if not cls.LINE_SECRET:
            raise ValueError("LINE_CHANNEL_SECRET مفقود")
        if not cls.LINE_ACCESS_TOKEN:
            raise ValueError("LINE_CHANNEL_ACCESS_TOKEN مفقود")
        return True

    @classmethod
    def normalize(cls, text: str) -> str:
        if not text:
            return ""
        
        text = text[:1000].strip().lower()
        
        replacements = {
            "أ": "ا", "إ": "ا", "آ": "ا",
            "ى": "ي", "ة": "ه",
            "ؤ": "و", "ئ": "ي"
        }
        
        for old, new in replacements.items():
            text = text.replace(old, new)
        
        text = re.sub(r"[\u064B-\u065F\u0670]", "", text)
        
        return text

    @classmethod
    def get_theme(cls, name: str = None):
        if name and name in cls.THEMES:
            return cls.THEMES[name]
        return cls.THEMES[cls.DEFAULT_THEME]

    @classmethod
    def is_valid_theme(cls, name: str) -> bool:
        return name in cls.THEMES

    @classmethod
    def get_game_config(cls, name: str):
        return cls.GAMES.get(name, {})

    @classmethod
    def get_all_games(cls):
        return list(cls.GAMES.keys())
