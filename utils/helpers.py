"""
Helper Functions
الوظائف المساعدة العامة
"""

import re
import logging
import time
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

def get_user_profile_safe(user_id, line_bot_api):
    """
    الحصول على معلومات المستخدم بشكل آمن
    
    Args:
        user_id: معرف المستخدم
        line_bot_api: كائن LINE Bot API
        
    Returns:
        str: اسم المستخدم أو اسم افتراضي
    """
    try:
        profile = line_bot_api.get_profile(user_id)
        display_name = profile.display_name if profile.display_name else "مستخدم"
        return display_name
    except Exception as e:
        logger.error(f"❌ خطأ في الحصول على الملف الشخصي: {e}")
        return f"مستخدم_{user_id[:8]}"

def normalize_text(text):
    """
    تطبيع النص العربي للمقارنة
    
    Args:
        text: النص المراد تطبيعه
        
    Returns:
        str: النص المطبّع
    """
    if not text:
        return ""
    
    # تحويل إلى حروف صغيرة وإزالة المسافات الزائدة
    text = text.strip().lower()
    
    # إزالة "ال" التعريف من البداية
    text = re.sub(r'^ال', '', text)
    
    # توحيد الهمزات
    text = text.replace('أ', 'ا').replace('إ', 'ا').replace('آ', 'ا')
    
    # توحيد التاء المربوطة والهاء
    text = text.replace('ة', 'ه')
    
    # توحيد الألف المقصورة والياء
    text = text.replace('ى', 'ي')
    
    # إزالة التشكيل
    text = re.sub(r'[\u064B-\u065F]', '', text)
    
    return text

def check_rate_limit(user_id, user_message_count, max_messages=20, time_window=60):
    """
    فحص حد المعدل للرسائل (Rate Limiting)
    
    Args:
        user_id: معرف المستخدم
        user_message_count: قاموس تتبع الرسائل
        max_messages: الحد الأقصى للرسائل
        time_window: النافذة الزمنية بالثواني
        
    Returns:
        bool: True إذا كان المستخدم ضمن الحد المسموح
    """
    now = datetime.now()
    user_data = user_message_count[user_id]
    
    # إعادة تعيين العداد إذا انتهت النافذة الزمنية
    if now - user_data['reset_time'] > timedelta(seconds=time_window):
        user_data['count'] = 0
        user_data['reset_time'] = now
    
    # فحص إذا تجاوز الحد
    if user_data['count'] >= max_messages:
        logger.warning(f"⚠️ تجاوز حد الرسائل: {user_id}")
        return False
    
    # زيادة العداد
    user_data['count'] += 1
    return True

def cleanup_old_games(active_games, games_lock, interval=300, max_age_minutes=10):
    """
    تنظيف الألعاب القديمة (يعمل في خيط منفصل)
    
    Args:
        active_games: قاموس الألعاب النشطة
        games_lock: قفل thread-safe
        interval: مدة الانتظار بين عمليات التنظيف (ثواني)
        max_age_minutes: عمر اللعبة الأقصى قبل الحذف (دقائق)
    """
    logger.info(f"🧹 بدأ خيط تنظيف الألعاب القديمة (كل {interval} ثانية)")
    
    while True:
        try:
            time.sleep(interval)
            now = datetime.now()
            to_delete = []
            
            with games_lock:
                for game_id, game_data in active_games.items():
                    created_at = game_data.get('created_at', now)
                    age = now - created_at
                    
                    if age > timedelta(minutes=max_age_minutes):
                        to_delete.append(game_id)
                
                # حذف الألعاب القديمة
                for game_id in to_delete:
                    del active_games[game_id]
                    logger.info(f"🗑️ تم حذف لعبة قديمة: {game_id}")
                
                if to_delete:
                    logger.info(f"✅ تم تنظيف {len(to_delete)} لعبة قديمة")
                    
        except Exception as e:
            logger.error(f"❌ خطأ في خيط التنظيف: {e}")

def format_time_ago(dt):
    """
    تحويل وقت إلى صيغة 'منذ كذا'
    
    Args:
        dt: datetime object أو ISO string
        
    Returns:
        str: وصف زمني بالعربية
    """
    if isinstance(dt, str):
        dt = datetime.fromisoformat(dt)
    
    now = datetime.now()
    diff = now - dt
    
    if diff.days > 365:
        years = diff.days // 365
        return f"منذ {years} سنة" if years == 1 else f"منذ {years} سنوات"
    elif diff.days > 30:
        months = diff.days // 30
        return f"منذ {months} شهر" if months == 1 else f"منذ {months} أشهر"
    elif diff.days > 0:
        return f"منذ {diff.days} يوم" if diff.days == 1 else f"منذ {diff.days} أيام"
    elif diff.seconds > 3600:
        hours = diff.seconds // 3600
        return f"منذ {hours} ساعة" if hours == 1 else f"منذ {hours} ساعات"
    elif diff.seconds > 60:
        minutes = diff.seconds // 60
        return f"منذ {minutes} دقيقة" if minutes == 1 else f"منذ {minutes} دقائق"
    else:
        return "الآن"
