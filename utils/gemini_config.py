import os
import logging

logger = logging.getLogger(__name__)

# تفعيل/تعطيل الذكاء الاصطناعي
USE_AI = os.getenv('USE_AI', 'true').lower() == 'true'

# مفاتيح Gemini API (دعم 3 مفاتيح)
GEMINI_API_KEYS = [
    os.getenv('GEMINI_API_KEY_1', ''),
    os.getenv('GEMINI_API_KEY_2', ''),
    os.getenv('GEMINI_API_KEY_3', '')
]

# تصفية المفاتيح الفارغة
GEMINI_API_KEYS = [key for key in GEMINI_API_KEYS if key]

# المفتاح الحالي
current_key_index = 0

def get_gemini_api_key():
    """الحصول على مفتاح Gemini API الحالي"""
    global current_key_index
    
    if not GEMINI_API_KEYS:
        logger.warning("⚠️ لا توجد مفاتيح Gemini API متاحة")
        return None
    
    if current_key_index >= len(GEMINI_API_KEYS):
        current_key_index = 0
    
    key = GEMINI_API_KEYS[current_key_index]
    logger.info(f"🔑 استخدام مفتاح Gemini API #{current_key_index + 1}")
    return key

def switch_gemini_key():
    """التبديل إلى مفتاح Gemini API التالي"""
    global current_key_index
    
    if not GEMINI_API_KEYS:
        logger.warning("⚠️ لا توجد مفاتيح للتبديل")
        return None
    
    current_key_index = (current_key_index + 1) % len(GEMINI_API_KEYS)
    logger.info(f"🔄 تم التبديل إلى مفتاح Gemini API #{current_key_index + 1}")
    return get_gemini_api_key()

def reset_gemini_key():
    """إعادة تعيين إلى المفتاح الأول"""
    global current_key_index
    current_key_index = 0
    logger.info("🔄 تم إعادة تعيين مفتاح Gemini API إلى الأول")

def get_total_keys():
    """الحصول على إجمالي عدد المفاتيح المتاحة"""
    return len(GEMINI_API_KEYS)

def is_ai_enabled():
    """التحقق من تفعيل الذكاء الاصطناعي"""
    return USE_AI and len(GEMINI_API_KEYS) > 0

# معلومات التكوين عند البدء
if __name__ != "__main__":
    if is_ai_enabled():
        logger.info(f"✅ الذكاء الاصطناعي مفعل ({get_total_keys()} مفاتيح متاحة)")
    else:
        if not USE_AI:
            logger.info("ℹ️ الذكاء الاصطناعي معطل")
        else:
            logger.warning("⚠️ الذكاء الاصطناعي معطل (لا توجد مفاتيح API)")
