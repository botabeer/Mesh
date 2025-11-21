"""
config.py - إعدادات التطبيق
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """إعدادات التطبيق"""
    
    # LINE Bot
    LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', 'YOUR_TOKEN')
    LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET', 'YOUR_SECRET')
    
    # Server
    PORT = int(os.getenv('PORT', 5000))
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Database
    DB_NAME = os.getenv('DB_NAME', 'data/game_scores.db')
    
    # Game Settings
    DEFAULT_ROUNDS = 5
    POINTS_CORRECT = 10
    POINTS_FAST_BONUS = 5
    HINT_PENALTY = 2
    
    # Colors (Neumorphism)
    BG_COLOR = '#E0E5EC'
    TEXT_PRIMARY = '#4A5568'
    TEXT_SECONDARY = '#A3B1C6'
    ACCENT_COLOR = '#667eea'
    GRADIENT_START = '#667eea'
    GRADIENT_END = '#764ba2'
