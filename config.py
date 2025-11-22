"""
Bot Mesh - Configuration File
Created by: Abeer Aldosari © 2025
"""
import os

class Config:
    """إعدادات البوت"""
    
    # LINE Bot Settings
    LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', '')
    LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET', '')
    
    # Gemini AI Settings (Optional)
    GEMINI_API_KEY_1 = os.getenv('GEMINI_API_KEY_1', '')
    GEMINI_API_KEY_2 = os.getenv('GEMINI_API_KEY_2', '')
    GEMINI_API_KEY_3 = os.getenv('GEMINI_API_KEY_3', '')
    
    # Database Settings
    DB_NAME = 'game_scores.db'
    DB_MAX_CONNECTIONS = 10
    
    # Bot Settings
    BOT_NAME = 'Bot Mesh'
    
    # Game Settings
    POINTS_PER_WIN = 10
    POINTS_PER_CORRECT = 5
    
    # Rate Limiting
    MAX_REQUESTS_PER_MINUTE = 100
    
    # Neumorphic Design Colors
    NEUMORPHIC_COLORS = {
        'background': '#E0E5EC',
        'text_primary': '#A3B1C6',
        'text_secondary': '#FFFFFF',
        'shadow_dark': '#A3B1C6',
        'shadow_light': '#FFFFFF',
        'accent': '#DADE2C',
        'button_primary': '#C3AED6',
        'button_secondary': '#A3B1C6'
    }
    
    # Game Colors (Neumorphic Palette)
    GAME_COLORS = {
        'iq': '#A3B1C6',
        'color': '#C3AED6',
        'chain': '#8FC7D6',
        'scramble': '#A8D5BA',
        'letters': '#D4A5A5',
        'typing': '#FFB6C1',
        'human': '#B0C4DE',
        'guess': '#D8BFD8',
        'compatibility': '#FFB3BA',
        'math': '#A3B1C6',
        'memory': '#BAE1FF',
        'riddle': '#FFDFBA',
        'opposite': '#BAFFC9',
        'emoji': '#FFE5B4',
        'song': '#E0BBE4'
    }
    
    @classmethod
    def get_gemini_keys(cls):
        """الحصول على مفاتيح Gemini المتاحة"""
        keys = []
        for i in range(1, 4):
            key = getattr(cls, f'GEMINI_API_KEY_{i}', '')
            if key:
                keys.append(key)
        return keys
    
    @classmethod
    def validate(cls):
        """التحقق من الإعدادات المطلوبة"""
        errors = []
        
        if not cls.LINE_CHANNEL_ACCESS_TOKEN:
            errors.append("LINE_CHANNEL_ACCESS_TOKEN is missing")
        
        if not cls.LINE_CHANNEL_SECRET:
            errors.append("LINE_CHANNEL_SECRET is missing")
        
        if errors:
            raise ValueError(f"Configuration errors: {', '.join(errors)}")
        
        return True
