import os
import re
from dotenv import load_dotenv

load_dotenv()

class Config:
    BOT_NAME = "Bot Mesh"
    VERSION = "1.0"
    RIGHTS = "Created by Abeer Aldossari 2025"

    LINE_SECRET = os.getenv("LINE_CHANNEL_SECRET")
    LINE_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

    DATABASE_PATH = "botmesh.db"
    DEFAULT_PORT = 10000

    RATE_LIMIT_MESSAGES = 30
    RATE_LIMIT_WINDOW = 60

    THEMES = {
        "light": {
            "bg": "#F2F2F7", "card": "#FFFFFF", "primary": "#007AFF",
            "secondary": "#5AC8FA", "success": "#34C759", "warning": "#FF9500",
            "danger": "#FF3B30", "text": "#000000", "text2": "#3C3C43",
            "text3": "#8E8E93", "border": "#E5E5EA"
        },
        "dark": {
            "bg": "#000000", "card": "#1C1C1E", "primary": "#0A84FF",
            "secondary": "#64D2FF", "success": "#30D158", "warning": "#FF9F0A",
            "danger": "#FF453A", "text": "#FFFFFF", "text2": "#EBEBF5",
            "text3": "#8E8E93", "border": "#3A3A3C"
        }
    }

    DEFAULT_THEME = "light"

    POINT_GAMES = ["iq", "guess", "opposite", "scramble", "math",
                   "song", "color", "letters", "game", "chain", "fast"]

    FUN_GAMES = {
        "question": {"group_only": False},
        "mention": {"group_only": False},
        "challenge": {"group_only": False},
        "confession": {"group_only": False},
        "situation": {"group_only": False},
        "quote": {"group_only": False},
        "compatibility": {"group_only": False},
        "mafia": {"group_only": True}
    }

    @classmethod
    def validate(cls):
        if not cls.LINE_SECRET or not cls.LINE_ACCESS_TOKEN:
            raise ValueError("LINE credentials missing")
        return True

    @classmethod
    def get_port(cls) -> int:
        try:
            return int(os.getenv("PORT", cls.DEFAULT_PORT))
        except:
            return cls.DEFAULT_PORT

    @classmethod
    def normalize(cls, text: str) -> str:
        if not text:
            return ""
        text = text[:1000].strip().lower()
        replacements = {"أ": "ا", "إ": "ا", "آ": "ا", "ى": "ي",
                       "ة": "ه", "ؤ": "و", "ئ": "ي"}
        for old, new in replacements.items():
            text = text.replace(old, new)
        text = re.sub(r"[\u064B-\u065F\u0670]", "", text)
        text = re.sub(r"[^\w\sء-ي]", "", text)
        return text

    @classmethod
    def get_theme(cls, name: str = None):
        return cls.THEMES.get(name, cls.THEMES[cls.DEFAULT_THEME])

    @classmethod
    def is_valid_theme(cls, name: str) -> bool:
        return name in cls.THEMES
