"""
Bot Mesh - Configuration File (Fixed)
Created by: Abeer Aldosari © 2025
"""
import os
from enum import Enum
from dataclasses import dataclass
from typing import List, Dict


class Theme(Enum):
    """الثيمات المتاحة - متطابقة مع flex_builder.py"""
    WHITE = "white"    # أبيض
    BLACK = "black"    # أسود
    GRAY = "gray"      # رمادي
    PURPLE = "purple"  # بنفسجي
    BLUE = "blue"      # أزرق


@dataclass
class ThemeColors:
    """ألوان الثيم"""
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
    shadow_dark: str = ""
    shadow_light: str = ""
    success: str = "#48BB78"
    error: str = "#FC8181"
    warning: str = "#F6AD55"


# =============================================
# 🎨 الثيمات الخمسة (متطابقة مع flex_builder.py)
# =============================================
THEMES: Dict[Theme, ThemeColors] = {
    # ⚪ أبيض - Neumorphism Light
    Theme.WHITE: ThemeColors(
        name="white", name_ar="أبيض", emoji="⚪",
        background="#E0E5EC",
        surface="#E0E5EC", 
        card="#D1D9E6",
        text_primary="#2C3E50",
        text_secondary="#7F8C8D",
        accent="#667EEA",
        button_primary="#667EEA",
        button_secondary="#A0AEC0",
        border="#C8D0E7",
        shadow_dark="#A3B1C6",
        shadow_light="#FFFFFF"
    ),
    
    # ⚫ أسود - Dark Neon
    Theme.BLACK: ThemeColors(
        name="black", name_ar="أسود", emoji="⚫",
        background="#0F0F1A",
        surface="#1A1A2E",
        card="#16213E",
        text_primary="#FFFFFF",
        text_secondary="#A0AEC0",
        accent="#00D9FF",
        button_primary="#00D9FF",
        button_secondary="#4A5568",
        border="#2D3748",
        shadow_dark="#0D0D1A",
        shadow_light="#2A2A4A"
    ),
    
    # 🔘 رمادي - Slate Gray
    Theme.GRAY: ThemeColors(
        name="gray", name_ar="رمادي", emoji="🔘",
        background="#1A202C",
        surface="#2D3748",
        card="#4A5568",
        text_primary="#F7FAFC",
        text_secondary="#CBD5E0",
        accent="#68D391",
        button_primary="#48BB78",
        button_secondary="#718096",
        border="#4A5568",
        shadow_dark="#1A202C",
        shadow_light="#4A5568"
    ),
    
    # 💜 بنفسجي - Purple Night
    Theme.PURPLE: ThemeColors(
        name="purple", name_ar="بنفسجي", emoji="💜",
        background="#1E1B4B",
        surface="#312E81",
        card="#3730A3",
        text_primary="#F5F3FF",
        text_secondary="#C4B5FD",
        accent="#A855F7",
        button_primary="#9333EA",
        button_secondary="#6B21A8",
        border="#4C1D95",
        shadow_dark="#0F0A2E",
        shadow_light="#4338CA"
    ),
    
    # 💙 أزرق - Ocean Blue
    Theme.BLUE: ThemeColors(
        name="blue", name_ar="أزرق", emoji="💙",
        background="#0C1929",
        surface="#1E3A5F",
        card="#0F2744",
        text_primary="#E0F2FE",
        text_secondary="#7DD3FC",
        accent="#00D9FF",
        button_primary="#0EA5E9",
        button_secondary="#0369A1",
        border="#0369A1",
        shadow_dark="#061224",
        shadow_light="#1E4976"
    )
}


class Config:
    """إعدادات البوت"""
    
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
    CACHE_TTL: int = int(os.getenv('CACHE_TTL', '3600'))
    
    # Database
    DB_PATH: str = os.getenv('DB_PATH', 'data')
    DB_NAME: str = os.getenv('DB_NAME', 'game_scores.db')
    DB_MAX_CONNECTIONS: int = int(os.getenv('DB_MAX_CONNECTIONS', '10'))
    
    # Bot Settings
    BOT_NAME: str = 'Bot Mesh'
    BOT_VERSION: str = '2.0.0'
    DEBUG: bool = os.getenv('DEBUG', 'false').lower() == 'true'
    
    # Game Settings
    POINTS_PER_WIN: int = 10
    POINTS_PER_CORRECT: int = 5
    DEFAULT_QUESTIONS: int = 10
    
    # Rate Limiting
    MAX_REQUESTS_PER_MINUTE: int = 100
    RATE_LIMIT_WINDOW: int = 60
    
    # Theme Settings
    DEFAULT_THEME: Theme = Theme.WHITE
    
    # Monitoring
    ENABLE_METRICS: bool = os.getenv('ENABLE_METRICS', 'true').lower() == 'true'
    
    # =============================================
    # 🎮 خريطة الألعاب (GAME_MAP) - FIXED
    # =============================================
    GAME_MAP = {
        # الألعاب الأساسية
        'ذكاء': {
            'class': 'IqGame',
            'emoji': '🧠',
            'name': 'اختبار الذكاء',
            'color': '#667EEA'
        },
        'لون': {
            'class': 'WordColorGame',
            'emoji': '🎨',
            'name': 'لعبة الألوان',
            'color': '#9F7AEA'
        },
        'سلسلة': {
            'class': 'ChainWordsGame',
            'emoji': '⛓️',
            'name': 'سلسلة الكلمات',
            'color': '#4FD1C5'
        },
        'ترتيب': {
            'class': 'ScrambleWordGame',
            'emoji': '🔤',
            'name': 'ترتيب الحروف',
            'color': '#68D391'
        },
        'تكوين': {
            'class': 'LettersWordsGame',
            'emoji': '✏️',
            'name': 'تكوين الكلمات',
            'color': '#FC8181'
        },
        'أسرع': {
            'class': 'FastTypingGame',
            'emoji': '⚡',
            'name': 'الكتابة السريعة',
            'color': '#F687B3'
        },
        'لعبة': {
            'class': 'HumanAnimalPlantGame',
            'emoji': '🎯',
            'name': 'إنسان حيوان نبات',
            'color': '#63B3ED'
        },
        'خمن': {
            'class': 'GuessGame',
            'emoji': '🤔',
            'name': 'خمن الكلمة',
            'color': '#B794F4'
        },
        'توافق': {
            'class': 'CompatibilityGame',
            'emoji': '💖',
            'name': 'نسبة التوافق',
            'color': '#FEB2B2'
        },
        'رياضيات': {
            'class': 'MathGame',
            'emoji': '🔢',
            'name': 'الرياضيات',
            'color': '#667EEA'
        },
        'ذاكرة': {
            'class': 'MemoryGame',
            'emoji': '🧩',
            'name': 'اختبار الذاكرة',
            'color': '#90CDF4'
        },
        'لغز': {
            'class': 'RiddleGame',
            'emoji': '🎭',
            'name': 'حل الألغاز',
            'color': '#FBD38D'
        },
        'ضد': {
            'class': 'OppositeGame',
            'emoji': '↔️',
            'name': 'الأضداد',
            'color': '#9AE6B4'
        },
        'إيموجي': {
            'class': 'EmojiGame',
            'emoji': '😀',
            'name': 'خمن الإيموجي',
            'color': '#FEEBC8'
        },
        'أغنية': {
            'class': 'SongGame',
            'emoji': '🎵',
            'name': 'خمن الأغنية',
            'color': '#E9D8FD'
        }
    }
    
    @classmethod
    def get_theme(cls, theme_name: str = None) -> ThemeColors:
        """الحصول على ثيم"""
        if theme_name:
            for theme_enum, theme_data in THEMES.items():
                if theme_data.name == theme_name or theme_data.name_ar == theme_name:
                    return theme_data
        return THEMES[cls.DEFAULT_THEME]
    
    @classmethod
    def get_db_path(cls) -> str:
        """مسار قاعدة البيانات"""
        return os.path.join(cls.DB_PATH, cls.DB_NAME)
    
    @classmethod
    def validate(cls) -> bool:
        """التحقق من الإعدادات"""
        errors = []
        if not cls.LINE_CHANNEL_ACCESS_TOKEN:
            errors.append("LINE_CHANNEL_ACCESS_TOKEN missing")
        if not cls.LINE_CHANNEL_SECRET:
            errors.append("LINE_CHANNEL_SECRET missing")
        if errors:
            raise ValueError(f"Config errors: {', '.join(errors)}")
        return True
    
    @classmethod
    def to_dict(cls) -> dict:
        """تحويل الإعدادات لقاموس"""
        return {
            'bot_name': cls.BOT_NAME,
            'version': cls.BOT_VERSION,
            'debug': cls.DEBUG,
            'redis_enabled': cls.REDIS_ENABLED,
            'total_games': len(cls.GAME_MAP)
        }
