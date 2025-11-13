import re
import logging
import time
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

def get_user_profile_safe(user_id, line_bot_api):
    """الحصول على معلومات المستخدم بشكل آمن"""
    try:
        profile = line_bot_api.get_profile(user_id)
        display_name = profile.display_name if profile.display_name else "مستخدم"
        return display_name
    except Exception as e:
        logger.error(f"خطأ في الحصول على الملف الشخصي: {e}")
        return f"مستخدم_{user_id[:8]}"

def normalize_text(text):
    """تطبيع النص العربي للمقارنة"""
    if not text:
        return ""
    
    text = text.strip().lower()
    text = re.sub(r'^ال', '', text)
    text = text.replace('أ', 'ا').replace('إ', 'ا').replace('آ', 'ا')
    text = text.replace('ة', 'ه')
    text = text.replace('ى', 'ي')
    text = re.sub(r'[\u064B-\u065F]', '', text)
    return text

def check_rate_limit(user_id, user_message_count, max_messages=20, time_window=60):
    """فحص حد المعدل للرسائل"""
    now = datetime.now()
    user_data = user_message_count[user_id]
    
    if now - user_data['reset_time'] > timedelta(seconds=time_window):
        user_data['count'] = 0
        user_data['reset_time'] = now
    
    if user_data['count'] >= max_messages:
        logger.warning(f"تجاوز حد الرسائل: {user_id}")
        return False
    
    user_data['count'] += 1
    return True

def cleanup_old_games(active_games, games_lock):
    """تنظيف الألعاب القديمة (يعمل في خيط منفصل)"""
    while True:
        try:
            time.sleep(300)  # كل 5 دقائق
            now = datetime.now()
            to_delete = []
            
            with games_lock:
                for game_id, game_data in active_games.items():
                    if now - game_data.get('created_at', now) > timedelta(minutes=10):
                        to_delete.append(game_id)
                
                for game_id in to_delete:
                    del active_games[game_id]
                    logger.info(f"تم حذف لعبة قديمة: {game_id}")
        except Exception as e:
            logger.error(f"خطأ في التنظيف: {e}")
