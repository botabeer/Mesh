"""
⚙️ Bot Mesh v7.0 - Configuration
إعدادات التطبيق والمتغيرات البيئية
Created by: Abeer Aldosari © 2025
"""

import os
import sys
import logging
from dotenv import load_dotenv

# تحميل متغيرات البيئة
load_dotenv()

logger = logging.getLogger(__name__)

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
    # Database Configuration
    # ============================================================================
    DATABASE_PATH = os.getenv('DATABASE_PATH', 'data/botmesh.db')
    
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
            errors.append("❌ LINE_CHANNEL_ACCESS_TOKEN غير موجود")
        
        if not cls.LINE_CHANNEL_SECRET:
            errors.append("❌ LINE_CHANNEL_SECRET غير موجود")
        
        # إنشاء مجلد البيانات
        data_dir = os.path.dirname(cls.DATABASE_PATH)
        if data_dir and not os.path.exists(data_dir):
            try:
                os.makedirs(data_dir)
                logger.info(f"✅ تم إنشاء مجلد البيانات: {data_dir}")
            except Exception as e:
                errors.append(f"❌ فشل إنشاء مجلد البيانات: {e}")
        
        is_valid = len(errors) == 0
        return is_valid, errors
    
    @classmethod
    def is_valid(cls) -> bool:
        """التحقق السريع من الصحة"""
        valid, _ = cls.validate()
        return valid
    
    @classmethod
    def print_config(cls):
        """طباعة الإعدادات (للتطوير)"""
        if cls.DEBUG:
            logger.info("=" * 50)
            logger.info("⚙️ إعدادات Bot Mesh v7.0")
            logger.info("=" * 50)
            logger.info(f"PORT: {cls.PORT}")
            logger.info(f"DEBUG: {cls.DEBUG}")
            logger.info(f"DATABASE: {cls.DATABASE_PATH}")
            logger.info(f"QUESTIONS_PER_GAME: {cls.QUESTIONS_PER_GAME}")
            logger.info(f"GAME_TIMEOUT: {cls.GAME_TIMEOUT_MINUTES} دقيقة")
            logger.info(f"RATE_LIMIT: {cls.MAX_MESSAGES_PER_MINUTE} رسالة/دقيقة")
            logger.info("=" * 50)

# ============================================================================
# التحقق عند الاستيراد
# ============================================================================
if __name__ != "__main__":
    config_valid, config_errors = Config.validate()
    if not config_valid:
        logger.error("❌ إعدادات غير صحيحة:")
        for error in config_errors:
            logger.error(f"   {error}")
        logger.error("💡 تأكد من ضبط المتغيرات البيئية")
    else:
        logger.info("✅ تم التحقق من الإعدادات بنجاح")
        Config.print_config()
