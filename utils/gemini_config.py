import os

# تفعيل/تعطيل الذكاء الاصطناعي
USE_AI = True

# مفاتيح Gemini API
GEMINI_KEYS = [
    os.getenv('GEMINI_API_KEY_1', ''),
    os.getenv('GEMINI_API_KEY_2', ''),
    os.getenv('GEMINI_API_KEY_3', '')
]

# فلترة المفاتيح الفارغة
GEMINI_KEYS = [key for key in GEMINI_KEYS if key]

# فهرس المفتاح الحالي
current_key_index = 0

def get_gemini_api_key():
    """الحصول على مفتاح API الحالي"""
    if not GEMINI_KEYS:
        return None
    return GEMINI_KEYS[current_key_index]

def switch_gemini_key():
    """التبديل إلى مفتاح API التالي"""
    global current_key_index
    
    if len(GEMINI_KEYS) <= 1:
        return
    
    current_key_index = (current_key_index + 1) % len(GEMINI_KEYS)
    print(f"🔄 تم التبديل إلى مفتاح API رقم {current_key_index + 1}")
