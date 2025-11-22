"""
Bot Mesh - Configuration File
Created by: Abeer Aldosari © 2025
"""
import os
from enum import Enum
from dataclasses import dataclass
from typing import List, Dict


class Theme(Enum):
    WHITE = "white"
    BLACK = "black"
    GRAY = "gray"
    PURPLE = "purple"
    BLUE = "blue"
    PINK = "pink"
    MINT = "mint"


@dataclass
class ThemeColors:
    name: str
    name_ar: str
    emoji: str
    background: str
    surface: str
    card: str
    text_primary: str
    text_secondary: str
    accent: str
    button_primary: str
    button_secondary: str
    border: str
    success: str = "#48BB78"
    error: str = "#FC8181"
    warning: str = "#F6AD55"


THEMES: Dict[Theme, ThemeColors] = {
    Theme.WHITE: ThemeColors(
        "white", "أبيض", "⚪", "#E0E5EC", "#E0E5EC", "#D1D9E6",
        "#2C3E50", "#7F8C8D", "#667EEA", "#667EEA", "#A0AEC0", "#C8D0E7"
    ),
    Theme.BLACK: ThemeColors(
        "black", "أسود", "⚫", "#0F0F1A", "#1A1A2E", "#16213E",
        "#FFFFFF", "#A0AEC0", "#00D9FF", "#00D9FF", "#4A5568", "#2D3748"
    ),
    Theme.GRAY: ThemeColors(
        "gray", "رمادي", "🔘", "#1A202C", "#2D3748", "#4A5568",
        "#F7FAFC", "#CBD5E0", "#68D391", "#48BB78", "#718096", "#4A5568"
    ),
    Theme.PURPLE: ThemeColors(
        "purple", "بنفسجي", "💜", "#1E1B4B", "#312E81", "#3730A3",
        "#F5F3FF", "#C4B5FD", "#A855F7", "#9333EA", "#6B21A8", "#4C1D95"
    ),
    Theme.BLUE: ThemeColors(
        "blue", "أزرق", "💙", "#0C1929", "#1E3A5F", "#0F2744",
        "#E0F2FE", "#7DD3FC", "#00D9FF", "#0EA5E9", "#0369A1", "#0369A1"
    ),
    Theme.PINK: ThemeColors(
        "pink", "وردي", "🌸", "#FFF1F2", "#FFE4E6", "#FFFFFF",
        "#881337", "#BE123C", "#F43F5E", "#E11D48", "#F43F5E", "#FFC9D0"
    ),
    Theme.MINT: ThemeColors(
        "mint", "نعناعي", "🍃", "#ECFDF5", "#D1FAE5", "#FFFFFF",
        "#065F46", "#059669", "#10B981", "#059669", "#10B981", "#9EF3CA"
    ),
}


class Config:
    # LINE Bot
    LINE_CHANNEL_ACCESS_TOKEN: str = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', '')
    LINE_CHANNEL_SECRET: str = os.getenv('LINE_CHANNEL_SECRET', '')
    
    # Gemini AI
    GEMINI_API_KEYS: List[str] = [
        k for k in [
            os.getenv('GEMINI_API_KEY_1', ''),
            os.getenv('GEMINI_API_KEY_2', ''),
            os.getenv('GEMINI_API_KEY_3', '')
        ] if k
    ]
    
    # Redis
    REDIS_URL: str = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    REDIS_ENABLED: bool = os.getenv('REDIS_ENABLED', 'false').lower() == 'true'
    
    # Database
    DB_PATH: str = os.getenv('DB_PATH', 'data')
    DB_NAME: str = os.getenv('DB_NAME', 'game_scores.db')
    
    # Bot
    BOT_NAME: str = 'Bot Mesh'
    BOT_VERSION: str = '2.0.0'
    DEBUG: bool = os.getenv('DEBUG', 'false').lower() == 'true'
    
    # Game
    POINTS_PER_WIN: int = 10
    DEFAULT_QUESTIONS: int = 10
    
    # Theme
    DEFAULT_THEME: Theme = Theme.WHITE
    
    # خريطة الألعاب (11 لعبة)
    GAME_MAP = {
        'ذكاء': {'class': 'IqGame', 'emoji': '🧠', 'name': 'اختبار الذكاء', 'color': '#667EEA'},
        'لون': {'class': 'WordColorGame', 'emoji': '🎨', 'name': 'لعبة الألوان', 'color': '#9F7AEA'},
        'سلسلة': {'class': 'ChainWordsGame', 'emoji': '⛓️', 'name': 'سلسلة الكلمات', 'color': '#4FD1C5'},
        'ترتيب': {'class': 'ScrambleWordGame', 'emoji': '🔤', 'name': 'ترتيب الحروف', 'color': '#68D391'},
        'تكوين': {'class': 'LettersWordsGame', 'emoji': '✏️', 'name': 'تكوين الكلمات', 'color': '#FC8181'},
        'أسرع': {'class': 'FastTypingGame', 'emoji': '⚡', 'name': 'الكتابة السريعة', 'color': '#F687B3'},
        'لعبة': {'class': 'HumanAnimalPlantGame', 'emoji': '🎯', 'name': 'إنسان حيوان نبات', 'color': '#63B3ED'},
        'خمن': {'class': 'GuessGame', 'emoji': '🤔', 'name': 'خمن الكلمة', 'color': '#B794F4'},
        'توافق': {'class': 'CompatibilityGame', 'emoji': '💖', 'name': 'نسبة التوافق', 'color': '#FEB2B2'},
        'ضد': {'class': 'OppositeGame', 'emoji': '↔️', 'name': 'الأضداد', 'color': '#9AE6B4'},
        'أغنية': {'class': 'SongGame', 'emoji': '🎵', 'name': 'خمن الأغنية', 'color': '#E9D8FD'},
    }
    
    @classmethod
    def get_theme(cls, theme_name: str = None) -> ThemeColors:
        if theme_name:
            for theme_enum, theme_data in THEMES.items():
                if theme_data.name == theme_name or theme_data.name_ar == theme_name:
                    return theme_data
        return THEMES[cls.DEFAULT_THEME]
    
    @classmethod
    def get_db_path(cls) -> str:
        return os.path.join(cls.DB_PATH, cls.DB_NAME)
    
    @classmethod
    def validate(cls) -> bool:
        errors = []
        if not cls.LINE_CHANNEL_ACCESS_TOKEN:
            errors.append("LINE_CHANNEL_ACCESS_TOKEN missing")
        if not cls.LINE_CHANNEL_SECRET:
            errors.append("LINE_CHANNEL_SECRET missing")
        if errors:
            raise ValueError(f"Config errors: {', '.join(errors)}")
        return True
