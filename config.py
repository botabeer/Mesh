‏import os
‏from dotenv import load_dotenv

‏load_dotenv()

‏class Config:
    """إعدادات التطبيق"""
    
‏    # LINE Bot
‏    LINE_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', '')
‏    LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET', '')
    
    # قاعدة البيانات
‏    DB_NAME = 'game_scores.db'
    
    # إعدادات اللعبة
‏    ROUNDS_PER_GAME = 5
‏    POINTS_PER_CORRECT = 10
‏    POINTS_BONUS = 20
    
    # الألوان (Neumorphism)
‏    COLORS = {
‏        'background': '#E0E5EC',
‏        'shadow_dark': 'rgba(163, 177, 198, 0.6)',
‏        'shadow_light': 'rgba(255, 255, 255, 0.7)',
‏        'gradient_start': '#667eea',
‏        'gradient_end': '#764ba2',
‏        'text_primary': '#4A5568',
‏        'text_secondary': '#A3B1C6'
    }
