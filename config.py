"""
⚙️ Bot Mesh v7.0 - Configuration
إعدادات التطبيق والمتغيرات البيئية
"""

import os
from dotenv import load_dotenv

# تحميل متغيرات البيئة
load_dotenv()

class Config:
    """إعدادات التطبيق"""
    
    # ============================================================================
    # LINE Credentials
    # ============================================================================
    LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', '')
    LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET', '')
    
    # ============================================================================
    # Server Configuration
    # ============================================================================
    PORT = int(os.getenv('PORT', 10000))
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # ============================================================================
    # Game Settings
    # ============================================================================
    QUESTIONS_PER_GAME = int(os.getenv('QUESTIONS_PER_GAME', 5))
    POINTS_PER_CORRECT_ANSWER = int(os.getenv('POINTS_PER_CORRECT_ANSWER', 10))
    GAME_TIMEOUT_MINUTES = int(os.getenv('GAME_TIMEOUT_MINUTES', 30))
    
    # ============================================================================
    # Rate Limiting
    # ============================================================================
    MAX_MESSAGES_PER_MINUTE = int(os.getenv('MAX_MESSAGES_PER_MINUTE', 20))
    
    # ============================================================================
    # Validation
    # ============================================================================
    @classmethod
    def validate(cls) -> tuple:
        """
        التحقق من صحة الإعدادات
        Returns: (is_valid, errors_list)
        """
        errors = []
        
        if not cls.LINE_CHANNEL_ACCESS_TOKEN:
            errors.append("LINE_CHANNEL_ACCESS_TOKEN غير موجود")
        
        if not cls.LINE_CHANNEL_SECRET:
            errors.append("LINE_CHANNEL_SECRET غير موجود")
        
        is_valid = len(errors) == 0
        
        return is_valid, errors
    
    @classmethod
    def is_valid(cls) -> bool:
        """التحقق السريع من الصحة"""
        valid, _ = cls.validate()
        return valid
