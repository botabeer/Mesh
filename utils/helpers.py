import logging
import unicodedata
from datetime import datetime, timedelta
import time

logger = logging.getLogger(__name__)

def normalize_text(text):
    """
    تطبيع النص العربي لقبول جميع أشكال الحروف
    """
    if not text:
        return ""
    
    text = text.strip()
    
    # إزالة التشكيل
    text = ''.join(c for c in text if not unicodedata.category(c).startswith('M'))
    
    # توحيد الحروف العربية
    replacements = {
        'أ': 'ا', 'إ': 'ا', 'آ': 'ا', 'ٱ': 'ا',
        'ؤ': 'و',
        'ئ': 'ي', 'ى': 'ي',
        'ة': 'ه',
        'ء': ''
    }
    
    for old, new in replacements.items():
        text = text.replace(old, new)
    
    # إزالة المسافات الزائدة
    text = ' '.join(text.split())
    
    # تحويل إلى أحرف صغيرة
    text = text.lower()
    
    return text

def get_user_profile_safe(user_id, line_bot_api):
    """
    الحصول على اسم المستخدم بشكل آمن
    """
    try:
        profile = line_bot_api.get_profile(user_id)
        return profile.display_name
    except Exception as e:
        logger.warning(f"⚠️ فشل الحصول على ملف المستخدم: {e}")
        return f"User_{user_id[:8]}"

def check_rate_limit(user_id, user_message_count, max_messages=30, time_window=60):
    """
    فحص حد المعدل (Rate Limiting)
    
    Args:
        user_id: معرف المستخدم
        user_message_count: قاموس عداد الرسائل
        max_messages: الحد الأقصى للرسائل (افتراضي: 30)
        time_window: نافذة الوقت بالثواني (افتراضي: 60)
    
    Returns:
        bool: True إذا كان المستخدم ضمن الحد المسموح
    """
    try:
        current_time = datetime.now()
        user_data = user_message_count[user_id]
        
        # إعادة تعيين العداد إذا مر وقت كافٍ
        if current_time - user_data['reset_time'] > timedelta(seconds=time_window):
            user_data['count'] = 0
            user_data['reset_time'] = current_time
        
        # زيادة العداد
        user_data['count'] += 1
        
        # فحص الحد
        if user_data['count'] > max_messages:
            logger.warning(f"⚠️ تجاوز حد المعدل للمستخدم: {user_id}")
            return False
        
        return True
        
    except Exception as e:
        logger.error(f"❌ خطأ في فحص حد المعدل: {e}")
        return True  # السماح في حالة الخطأ

def cleanup_old_games(active_games, games_lock, cleanup_interval=300, max_age=900):
    """
    تنظيف الألعاب القديمة تلقائياً
    
    Args:
        active_games: قاموس الألعاب النشطة
        games_lock: قفل الألعاب
        cleanup_interval: فترة التنظيف بالثواني (افتراضي: 5 دقائق)
        max_age: العمر الأقصى للعبة بالثواني (افتراضي: 15 دقيقة)
    """
    while True:
        try:
            time.sleep(cleanup_interval)
            
            current_time = datetime.now()
            games_to_remove = []
            
            with games_lock:
                for game_id, game_data in active_games.items():
                    if 'created_at' in game_data:
                        age = (current_time - game_data['created_at']).total_seconds()
                        if age > max_age:
                            games_to_remove.append(game_id)
                
                for game_id in games_to_remove:
                    game_type = active_games[game_id].get('type', 'unknown')
                    del active_games[game_id]
                    logger.info(f"🗑️ تم حذف لعبة {game_type} قديمة ({game_id})")
            
            if games_to_remove:
                logger.info(f"✅ تم تنظيف {len(games_to_remove)} لعبة قديمة")
                
        except Exception as e:
            logger.error(f"❌ خطأ في تنظيف الألعاب: {e}", exc_info=True)

def format_time(seconds):
    """
    تنسيق الوقت بشكل قابل للقراءة
    
    Args:
        seconds: الوقت بالثواني
    
    Returns:
        str: الوقت المنسق
    """
    if seconds < 60:
        return f"{seconds:.1f} ثانية"
    elif seconds < 3600:
        minutes = seconds // 60
        secs = seconds % 60
        return f"{int(minutes)} دقيقة و {int(secs)} ثانية"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{int(hours)} ساعة و {int(minutes)} دقيقة"

def validate_arabic_text(text, min_length=2, max_length=50):
    """
    التحقق من صحة النص العربي
    
    Args:
        text: النص المراد فحصه
        min_length: الحد الأدنى للطول
        max_length: الحد الأقصى للطول
    
    Returns:
        bool: True إذا كان النص صحيحاً
    """
    if not text or len(text) < min_length or len(text) > max_length:
        return False
    
    # التحقق من وجود أحرف عربية
    arabic_pattern = any('\u0600' <= char <= '\u06FF' for char in text)
    
    return arabic_pattern

def calculate_points(base_points, time_taken=None, hint_count=0, time_thresholds=None):
    """
    حساب النقاط بناءً على عدة عوامل
    
    Args:
        base_points: النقاط الأساسية
        time_taken: الوقت المستغرق (اختياري)
        hint_count: عدد التلميحات
        time_thresholds: عتبات الوقت للنقاط الإضافية
    
    Returns:
        int: النقاط النهائية
    """
    points = base_points
    
    # خصم نقاط التلميحات
    points -= (hint_count * 3)
    
    # إضافة/خصم نقاط الوقت
    if time_taken and time_thresholds:
        for threshold, bonus in sorted(time_thresholds.items()):
            if time_taken <= threshold:
                points += bonus
                break
    
    # الحد الأدنى نقطة واحدة
    return max(points, 1)

def get_emoji_for_rank(rank):
    """
    الحصول على إيموجي مناسب للترتيب
    
    Args:
        rank: الترتيب (1، 2، 3، إلخ)
    
    Returns:
        str: الإيموجي المناسب
    """
    emojis = {
        1: '🥇',
        2: '🥈',
        3: '🥉'
    }
    return emojis.get(rank, '▪️')

def truncate_text(text, max_length=100, suffix='...'):
    """
    اختصار النص الطويل
    
    Args:
        text: النص المراد اختصاره
        max_length: الحد الأقصى للطول
        suffix: اللاحقة (افتراضي: ...)
    
    Returns:
        str: النص المختصر
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix

def format_number(number):
    """
    تنسيق الأرقام بالفواصل
    
    Args:
        number: الرقم المراد تنسيقه
    
    Returns:
        str: الرقم المنسق
    """
    return f"{number:,}"

def get_time_greeting():
    """
    الحصول على تحية مناسبة حسب الوقت
    
    Returns:
        str: التحية
    """
    current_hour = datetime.now().hour
    
    if 5 <= current_hour < 12:
        return "صباح الخير"
    elif 12 <= current_hour < 17:
        return "مساء الخير"
    elif 17 <= current_hour < 21:
        return "مساء الخير"
    else:
        return "مساء الخير"

def safe_divide(numerator, denominator, default=0):
    """
    القسمة الآمنة (تجنب القسمة على صفر)
    
    Args:
        numerator: البسط
        denominator: المقام
        default: القيمة الافتراضية عند القسمة على صفر
    
    Returns:
        float: النتيجة
    """
    try:
        if denominator == 0:
            return default
        return numerator / denominator
    except:
        return default

def get_win_rate(games_played, wins):
    """
    حساب معدل الفوز
    
    Args:
        games_played: عدد الألعاب
        wins: عدد الانتصارات
    
    Returns:
        str: معدل الفوز بالنسبة المئوية
    """
    if games_played == 0:
        return "0%"
    
    rate = (wins / games_played) * 100
    return f"{rate:.1f}%"
