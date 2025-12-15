import os
import re
from dotenv import load_dotenv

load_dotenv()


class Config:
    BOT_NAME = "Bot Mesh"
    VERSION = "3.0"

    LINE_SECRET = os.getenv("LINE_CHANNEL_SECRET")
    LINE_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

    DB_PATH = "botmesh.db"

    THEMES = {
        "light": {
            "primary": "#007AFF",
            "secondary": "#8E8E93",
            "success": "#34C759",
            "warning": "#FF9500",
            "danger": "#FF3B30",
            "bg": "#FFFFFF",
            "bg_secondary": "#F2F2F7",
            "card": "rgba(255, 255, 255, 0.8)",
            "glass": "rgba(242, 242, 247, 0.8)",
            "text": "#000000",
            "text_secondary": "#3C3C43",
            "text_tertiary": "#8E8E93",
            "border": "rgba(0, 0, 0, 0.1)",
            "shadow": "rgba(0, 0, 0, 0.08)"
        },
        "dark": {
            "primary": "#0A84FF",
            "secondary": "#98989D",
            "success": "#30D158",
            "warning": "#FF9F0A",
            "danger": "#FF453A",
            "bg": "#000000",
            "bg_secondary": "#1C1C1E",
            "card": "rgba(28, 28, 30, 0.8)",
            "glass": "rgba(44, 44, 46, 0.8)",
            "text": "#FFFFFF",
            "text_secondary": "#EBEBF5",
            "text_tertiary": "#98989D",
            "border": "rgba(255, 255, 255, 0.1)",
            "shadow": "rgba(0, 0, 0, 0.3)"
        }
    }

    GAMES = [
        "ذكاء", "خمن", "رياضيات", "ترتيب", "اغنيه",
        "لون", "ضد", "تكوين", "سلسلة", "اسرع"
    ]

    @classmethod
    def get_theme(cls, name: str = "light"):
        return cls.THEMES.get(name, cls.THEMES["light"])

    @classmethod
    def normalize(cls, text: str) -> str:
        if not text:
            return ""

        text = text.strip().lower()[:1000]
        text = re.sub(r"[\u064B-\u065F\u0670]", "", text)

        replacements = {
            "أ": "ا", "إ": "ا", "آ": "ا",
            "ى": "ي", "ة": "ه",
            "ؤ": "و", "ئ": "ي"
        }
        for old, new in replacements.items():
            text = text.replace(old, new)

        text = re.sub(r"[^\w\sء-ي]", "", text)
        text = re.sub(r"\s+", " ", text)

        return text.strip()


if not Config.LINE_SECRET or not Config.LINE_TOKEN:
    raise RuntimeError("LINE credentials are missing")
