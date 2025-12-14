# ========================================
# config.py
# ========================================

import os
import re
from dotenv import load_dotenv

# تحميل المتغيرات البيئية
load_dotenv()


class Config:
    # ------------------------------------
    # معلومات البوت
    # ------------------------------------
    BOT_NAME = "Bot Mesh"
    VERSION = "2.0"
    RIGHTS = "Created by Abeer Aldossari © 2025"

    # ------------------------------------
    # إعدادات LINE
    # ------------------------------------
    LINE_SECRET = os.getenv("LINE_CHANNEL_SECRET", "").strip()
    LINE_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", "").strip()

    # ------------------------------------
    # قاعدة البيانات
    # ------------------------------------
    DATABASE_PATH = os.getenv("DATABASE_PATH", "botmesh.db")

    # ------------------------------------
    # السيرفر
    # ------------------------------------
    DEFAULT_PORT = 10000

    # ------------------------------------
    # Rate Limiting
    # ------------------------------------
    RATE_LIMIT_MESSAGES = 30
    RATE_LIMIT_WINDOW = 60  # seconds

    # ------------------------------------
    # الثيمات (iOS Glass Style)
    # ------------------------------------
    THEMES = {
        "light": {
            "primary": "#000000",
            "secondary": "#666666",
            "accent": "#333333",

            "success": "#2C2C2E",
            "warning": "#48484A",
            "danger": "#1C1C1E",
            "info": "#3A3A3C",

            "bg": "#FFFFFF",
            "bg_secondary": "#F9F9F9",
            "card": "rgba(255, 255, 255, 0.85)",
            "overlay": "rgba(255, 255, 255, 0.95)",

            "text": "#000000",
            "text_secondary": "#666666",
            "text_tertiary": "#999999",
            "text_disabled": "#CCCCCC",

            "border": "rgba(0, 0, 0, 0.1)",
            "separator": "rgba(0, 0, 0, 0.08)",
            "shadow": "rgba(0, 0, 0, 0.05)",

            "blur_strong": "blur(20px)",
            "blur_medium": "blur(10px)",
            "blur_light": "blur(5px)",
        },

        "dark": {
            "primary": "#FFFFFF",
            "secondary": "#A0A0A0",
            "accent": "#CCCCCC",

            "success": "#E5E5E7",
            "warning": "#C7C7CC",
            "danger": "#F2F2F7",
            "info": "#D1D1D6",

            "bg": "#000000",
            "bg_secondary": "#0A0A0A",
            "card": "rgba(28, 28, 30, 0.85)",
            "overlay": "rgba(28, 28, 30, 0.95)",

            "text": "#FFFFFF",
            "text_secondary": "#A0A0A0",
            "text_tertiary": "#666666",
            "text_disabled": "#3A3A3C",

            "border": "rgba(255, 255, 255, 0.1)",
            "separator": "rgba(255, 255, 255, 0.08)",
            "shadow": "rgba(0, 0, 0, 0.3)",

            "blur_strong": "blur(20px)",
            "blur_medium": "blur(10px)",
            "blur_light": "blur(5px)",
        }
    }

    DEFAULT_THEME = "light"

    # ------------------------------------
    # الألعاب
    # ------------------------------------
    POINT_GAMES = [
        "ذكاء", "خمن", "ضد", "ترتيب",
        "رياضيات", "اغنيه", "لون",
        "تكوين", "سلسلة", "اسرع"
    ]

    FUN_GAMES = {
        "سؤال": {"group_only": False},
        "منشن": {"group_only": False},
        "تحدي": {"group_only": False},
        "اعتراف": {"group_only": False},
        "موقف": {"group_only": False},
        "اقتباس": {"group_only": False},
        "توافق": {"group_only": False},
        "مافيا": {"group_only": True},
    }

    # ------------------------------------
    # Validation
    # ------------------------------------
    @classmethod
    def validate(cls) -> bool:
        if not cls.LINE_SECRET:
            raise ValueError("LINE_CHANNEL_SECRET is missing")

        if not cls.LINE_ACCESS_TOKEN:
            raise ValueError("LINE_CHANNEL_ACCESS_TOKEN is missing")

        return True

    # ------------------------------------
    # Utilities
    # ------------------------------------
    @classmethod
    def get_port(cls) -> int:
        try:
            return int(os.getenv("PORT", cls.DEFAULT_PORT))
        except (TypeError, ValueError):
            return cls.DEFAULT_PORT

    @classmethod
    def normalize(cls, text: str) -> str:
        """
        تطبيع النص العربي (آمن وسريع)
        """
        if not text:
            return ""

        text = text.strip().lower()[:500]

        replacements = {
            "أ": "ا", "إ": "ا", "آ": "ا",
            "ى": "ي", "ة": "ه",
            "ؤ": "و", "ئ": "ي",
        }

        for old, new in replacements.items():
            text = text.replace(old, new)

        text = re.sub(r"[\u064B-\u065F\u0670]", "", text)
        text = re.sub(r"[^\w\sء-ي]", "", text)

        return text.strip()

    # ------------------------------------
    # Themes
    # ------------------------------------
    @classmethod
    def get_theme(cls, name: str = None) -> dict:
        return cls.THEMES.get(name, cls.THEMES[cls.DEFAULT_THEME])

    @classmethod
    def is_valid_theme(cls, name: str) -> bool:
        return name in cls.THEMES
