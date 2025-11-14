import re
from datetime import datetime, timedelta
import time

def get_user_profile_safe(user_id, line_bot_api):
    """الحصول على اسم المستخدم بأمان"""
    try:
        profile = line_bot_api.get_profile(user_id)
        return profile.display_name
    except:
        return "لاعب"

def normalize_text(text):
    """تطبيع النص العربي"""
    if not text:
        return ""
    
    # إزالة التشكيل
    text = re.sub(r'[\u0617-\u061A\u064B-\u0652]', '', text)
    
    # توحيد الهمزات
    text = text.replace('أ', 'ا').replace('إ', 'ا').replace('آ', 'ا')
    text = text.replace('ؤ', 'و').replace('ئ', 'ي').replace('ء', '')
    
    # توحيد التاء المربوطة والألف المقصورة
    text = text.replace('ة', 'ه').replace('ى', 'ي')
    
    # إزالة المسافات الزائدة
    text = ' '.join(text.split())
    
    return text.strip().lower()

def check_rate_limit(user_id, user_message_count, max_messages=30, window_seconds=60):
    """فحص حد المعدل"""
    current_time = datetime.now()
    user_data = user_message_count[user_id]
    
    # إعادة تعيين العداد إذا مرت الفترة الزمنية
    if (current_time - user_data['reset_time']).total_seconds() > window_seconds:
        user_data['count'] = 0
        user_data['reset_time'] = current_time
    
    # زيادة العداد
    user_data['count'] += 1
    
    # التحقق من الحد
    if user_data['count'] > max_messages:
        return False
    
    return True

def cleanup_old_games(active_games, games_lock, max_age_minutes=15, sleep_seconds=300):
    """تنظيف الألعاب القديمة"""
    while True:
        try:
            time.sleep(sleep_seconds)
            current_time = datetime.now()
            to_remove = []
            
            with games_lock:
                for game_id, game_data in active_games.items():
                    age = current_time - game_data['created_at']
                    if age > timedelta(minutes=max_age_minutes):
                        to_remove.append(game_id)
                
                for game_id in to_remove:
                    del active_games[game_id]
                    print(f"🗑️ تم حذف لعبة قديمة: {game_id}")
        
        except Exception as e:
            print(f"❌ خطأ في التنظيف: {e}")
