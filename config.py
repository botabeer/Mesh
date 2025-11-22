"""
Bot Mesh - Configuration
Created by: Abeer Aldosari © 2025
"""
import os
from typing import List


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
    
    # Database
    DB_PATH: str = os.getenv('DB_PATH', 'data')
    DB_NAME: str = os.getenv('DB_NAME', 'game_scores.db')
    
    # Bot
    BOT_NAME: str = 'Bot Mesh'
    BOT_VERSION: str = '2.0.0'
    DEBUG: bool = os.getenv('DEBUG', 'false').lower() == 'true'
    
    # 11 لعبة
    GAME_MAP = {
        'ذكاء': {'class': 'IqGame', 'emoji': '🧠', 'name': 'اختبار الذكاء'},
        'لون': {'class': 'WordColorGame', 'emoji': '🎨', 'name': 'الكلمة واللون'},
        'ترتيب': {'class': 'ScrambleWordGame', 'emoji': '🔤', 'name': 'ترتيب الحروف'},
        'تكوين': {'class': 'LettersWordsGame', 'emoji': '✏️', 'name': 'تكوين الكلمات'},
        'سلسلة': {'class': 'ChainWordsGame', 'emoji': '⛓️', 'name': 'سلسلة الكلمات'},
        'أسرع': {'class': 'FastTypingGame', 'emoji': '⚡', 'name': 'الكتابة السريعة'},
        'لعبة': {'class': 'HumanAnimalPlantGame', 'emoji': '🎯', 'name': 'إنسان حيوان نبات'},
        'خمن': {'class': 'GuessGame', 'emoji': '🤔', 'name': 'خمن الكلمة'},
        'ضد': {'class': 'OppositeGame', 'emoji': '↔️', 'name': 'الأضداد'},
        'توافق': {'class': 'CompatibilityGame', 'emoji': '💖', 'name': 'نسبة التوافق'},
        'أغنية': {'class': 'SongGame', 'emoji': '🎵', 'name': 'خمن الأغنية'},
    }
