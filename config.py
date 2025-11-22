"""
Bot Mesh - Configuration File (Enhanced)
Created by: Abeer Aldosari © 2025
"""
import os
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Optional

class Theme(Enum):
    """ثيمات التطبيق"""
    LIGHT = "light"
    DARK = "dark"
    PURPLE = "purple"
    OCEAN = "ocean"
    SUNSET = "sunset"

@dataclass
class ThemeColors:
    """ألوان الثيم"""
    background: str
    surface: str
    text_primary: str
    text_secondary: str
    accent: str
    shadow_dark: str
    shadow_light: str
    button_primary: str
    button_secondary: str
    success: str = "#4CAF50"
    error: str = "#F44336"
    warning: str = "#FF9800"

# ثيمات محددة مسبقاً
THEMES: Dict[Theme, ThemeColors] = {
    Theme.LIGHT: ThemeColors(
        background="#E0E5EC",
        surface="#F0F5FA",
        text_primary="#2D3748",
        text_secondary="#718096",
        accent="#667EEA",
        shadow_dark="#A3B1C6",
        shadow_light="#FFFFFF",
        button_primary="#667EEA",
        button_secondary="#A3B1C6"
    ),
    Theme.DARK: ThemeColors(
        background="#1A202C",
        surface="#2D3748",
        text_primary="#F7FAFC",
        text_secondary="#A0AEC0",
        accent="#63B3ED",
        shadow_dark="#0D1117",
        shadow_light="#4A5568",
        button_primary="#4299E1",
        button_secondary="#4A5568"
    ),
    Theme.PURPLE: ThemeColors(
        background="#2D1B69",
        surface="#3D2B79",
        text_primary="#F0E6FF",
        text_secondary="#C4B5FD",
        accent="#A855F7",
        shadow_dark="#1A0F40",
        shadow_light="#5B4B8A",
        button_primary="#9333EA",
        button_secondary="#7C3AED"
    ),
    Theme.OCEAN: ThemeColors(
        background="#0F172A",
        surface="#1E293B",
        text_primary="#E2E8F0",
        text_secondary="#94A3B8",
        accent="#06B6D4",
        shadow_dark="#020617",
        shadow_light="#334155",
        button_primary="#0891B2",
        button_secondary="#0E7490"
    ),
    Theme.SUNSET: ThemeColors(
        background="#FFF7ED",
        surface="#FFEDD5",
        text_primary="#9A3412",
        text_secondary="#C2410C",
        accent="#F97316",
        shadow_dark="#FED7AA",
        shadow_light="#FFFFFF",
        button_primary="#EA580C",
        button_secondary="#FB923C"
    )
}

class Config:
    """إعدادات البوت المحسنة"""
    
    # LINE Bot Settings
    LINE_CHANNEL_ACCESS_TOKEN: str = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', '')
    LINE_CHANNEL_SECRET: str = os.getenv('LINE_CHANNEL_SECRET', '')
    
    # Gemini AI Settings
    GEMINI_API_KEYS: List[str] = [
        k for k in [
            os.getenv('GEMINI_API_KEY_1', ''),
            os.getenv('GEMINI_API_KEY_2', ''),
            os.getenv('GEMINI_API_KEY_3', '')
        ] if k
    ]
    
    # Redis Settings
    REDIS_URL: str = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    REDIS_ENABLED: bool = os.getenv('REDIS_ENABLED', 'false').lower() == 'true'
    CACHE_TTL: int = int(os.getenv('CACHE_TTL', '3600'))
    
    # Database Settings
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
    DEFAULT_THEME: Theme = Theme.LIGHT
    
    # Monitoring
    ENABLE_METRICS: bool = os.getenv('ENABLE_METRICS', 'true').lower() == 'true'
    METRICS_PORT: int = int(os.getenv('METRICS_PORT', '9090'))
    
    # WebSocket
    WS_ENABLED: bool = os.getenv('WS_ENABLED', 'false').lower() == 'true'
    WS_PORT: int = int(os.getenv('WS_PORT', '8765'))
    
    # Game Colors (Neumorphic Palette)
    GAME_COLORS: Dict[str, str] = {
        'iq': '#667EEA',
        'color': '#9F7AEA',
        'chain': '#4FD1C5',
        'scramble': '#68D391',
        'letters': '#FC8181',
        'typing': '#F687B3',
        'human': '#63B3ED',
        'guess': '#B794F4',
        'compatibility': '#FEB2B2',
        'math': '#667EEA',
        'memory': '#90CDF4',
        'riddle': '#FBD38D',
        'opposite': '#9AE6B4',
        'emoji': '#FEEBC8',
        'song': '#E9D8FD'
    }
    
    @classmethod
    def get_db_path(cls) -> str:
        """الحصول على مسار قاعدة البيانات الكامل"""
        return os.path.join(cls.DB_PATH, cls.DB_NAME)
    
    @classmethod
    def get_theme(cls, theme_name: str = None) -> ThemeColors:
        """الحصول على ألوان الثيم"""
        if theme_name:
            try:
                theme = Theme(theme_name)
                return THEMES[theme]
            except (ValueError, KeyError):
                pass
        return THEMES[cls.DEFAULT_THEME]
    
    @classmethod
    def validate(cls) -> bool:
        """التحقق من الإعدادات المطلوبة"""
        errors = []
        
        if not cls.LINE_CHANNEL_ACCESS_TOKEN:
            errors.append("LINE_CHANNEL_ACCESS_TOKEN is missing")
        
        if not cls.LINE_CHANNEL_SECRET:
            errors.append("LINE_CHANNEL_SECRET is missing")
        
        if errors:
            raise ValueError(f"Configuration errors: {', '.join(errors)}")
        
        return True
    
    @classmethod
    def to_dict(cls) -> dict:
        """تحويل الإعدادات لقاموس"""
        return {
            'bot_name': cls.BOT_NAME,
            'version': cls.BOT_VERSION,
            'debug': cls.DEBUG,
            'redis_enabled': cls.REDIS_ENABLED,
            'ws_enabled': cls.WS_ENABLED,
            'metrics_enabled': cls.ENABLE_METRICS
        }
