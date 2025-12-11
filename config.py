import os
import re
from dotenv import load_dotenv
from constants import THEMES

load_dotenv()

class Config:
    BOT_NAME = "Bot Mesh"
    VERSION = "24.0"
    RIGHTS = "عبير الدوسري 2025"
    
    LINE_SECRET = os.getenv("LINE_CHANNEL_SECRET")
    LINE_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
    
    THEMES = THEMES
    
    GAMES = {
        "ذكاء": {"hint": True, "reveal": True},
        "روليت": {"hint": True, "reveal": True},
        "خمن": {"hint": True, "reveal": True},
        "اغنيه": {"hint": True, "reveal": True},
        "ترتيب": {"hint": True, "reveal": True},
        "تكوين": {"hint": True, "reveal": True},
        "ضد": {"hint": True, "reveal": True},
        "لعبة": {"hint": True, "reveal": True},
        "اسرع": {"hint": False, "reveal": False, "timer": 20},
        "سلسلة": {"hint": False, "reveal": False},
        "لون": {"hint": True, "reveal": True},
        "رياضيات": {"hint": True, "reveal": True},
        "توافق": {"hint": False, "reveal": False, "no_registration": True},
        "مافيا": {"hint": False, "reveal": False, "group_only": True}
    }
    
    @classmethod
    def validate(cls):
        if not cls.LINE_SECRET:
            raise ValueError("LINE_CHANNEL_SECRET missing")
        if not cls.LINE_ACCESS_TOKEN:
            raise ValueError("LINE_CHANNEL_ACCESS_TOKEN missing")
    
    @classmethod
    def normalize(cls, text: str) -> str:
        if not text:
            return ""
        text = text[:1000].strip().lower()
        for old, new in {'أ':'ا','إ':'ا','آ':'ا','ى':'ي','ة':'ه','ؤ':'و','ئ':'ي'}.items():
            text = text.replace(old, new)
        return re.sub(r'[\u064B-\u065F\u0670]', '', text)
    
    @classmethod
    def get_theme(cls, name: str = None):
        return cls.THEMES.get(name, cls.THEMES["ابيض"])
    
    @classmethod
    def is_valid_theme(cls, name: str) -> bool:
        return name in cls.THEMES
    
    @classmethod
    def get_game_config(cls, name: str):
        return cls.GAMES.get(name, {})
