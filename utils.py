"""
utils.py - Utility functions for Bot Mesh
"""
import re
import time
from collections import defaultdict
from typing import Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class RateLimiter:
    """معدل محدد للطلبات لمنع الإساءة"""
    
    def __init__(self, max_requests: int = 5, window: int = 60):
        self.max_requests = max_requests
        self.window = window
        self.requests = defaultdict(list)
    
    def is_allowed(self, user_id: str) -> bool:
        """التحقق من السماح للمستخدم بإرسال طلب"""
        now = time.time()
        
        # تنظيف الطلبات القديمة
        self.requests[user_id] = [
            timestamp for timestamp in self.requests[user_id]
            if now - timestamp < self.window
        ]
        
        # التحقق من الحد الأقصى
        if len(self.requests[user_id]) >= self.max_requests:
            return False
        
        # إضافة الطلب الحالي
        self.requests[user_id].append(now)
        return True
    
    def get_remaining_time(self, user_id: str) -> int:
        """الحصول على الوقت المتبقي حتى يمكن إرسال طلب جديد"""
        if not self.requests[user_id]:
            return 0
        
        oldest_request = min(self.requests[user_id])
        time_passed = time.time() - oldest_request
        return max(0, int(self.window - time_passed))


class InputValidator:
    """التحقق من صحة المدخلات"""
    
    @staticmethod
    def validate_username(name: str) -> Tuple[bool, str]:
        """
        التحقق من صحة اسم المستخدم
        Returns: (is_valid, error_message)
        """
        if not name:
            return False, "الاسم فارغ"
        
        # إزالة المسافات الزائدة
        name = ' '.join(name.split())
        
        if len(name) < 2:
            return False, "الاسم قصير جداً (حد أدنى حرفين)"
        
        if len(name) > 50:
            return False, "الاسم طويل جداً (حد أقصى 50 حرف)"
        
        # السماح بالعربية والإنجليزية والأرقام والمسافات فقط
        if not re.match(r'^[ء-يa-zA-Z0-9\s]+$', name):
            return False, "الاسم يحتوي على رموز غير مسموحة"
        
        # منع الأسماء التي تحتوي على أرقام فقط
        if re.match(r'^\d+$', name):
            return False, "الاسم لا يمكن أن يكون أرقام فقط"
        
        return True, ""
    
    @staticmethod
    def sanitize_text(text: str, max_length: int = 1000) -> str:
        """تنظيف النص من المحتوى الخطير"""
        if not text:
            return ""
        
        # تحديد الطول
        text = text[:max_length]
        
        # إزالة المسافات الزائدة
        text = ' '.join(text.split())
        
        # إزالة الأحرف الخاصة الخطيرة
        dangerous_chars = ['<', '>', '{', '}', '\\', '|']
        for char in dangerous_chars:
            text = text.replace(char, '')
        
        return text.strip()
    
    @staticmethod
    def is_spam(text: str) -> bool:
        """التحقق من الرسائل المزعجة"""
        if not text:
            return False
        
        # رسائل قصيرة جداً متكررة
        if len(text) == 1 and text in ['ا', 'أ', 'ي', 'و']:
            return True
        
        # رسائل طويلة جداً
        if len(text) > 2000:
            return True
        
        # تكرار الحرف نفسه
        if len(set(text)) < 3 and len(text) > 10:
            return True
        
        # روابط مشبوهة
        spam_patterns = [
            r'https?://bit\.ly',
            r'https?://.*\.tk',
            r'CLICK HERE',
            r'اضغط هنا للحصول',
            r'ربح مضمون',
        ]
        
        for pattern in spam_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        
        return False


class GameStatsCalculator:
    """حساب الإحصائيات المتقدمة"""
    
    @staticmethod
    def calculate_win_rate(wins: int, total_games: int) -> float:
        """حساب معدل الفوز"""
        if total_games == 0:
            return 0.0
        return round((wins / total_games) * 100, 2)
    
    @staticmethod
    def calculate_average_score(total_points: int, total_games: int) -> float:
        """حساب متوسط النقاط لكل لعبة"""
        if total_games == 0:
            return 0.0
        return round(total_points / total_games, 2)
    
    @staticmethod
    def get_rank_title(total_points: int) -> str:
        """الحصول على لقب بناءً على النقاط"""
        if total_points < 10:
            return "مبتدئ"
        elif total_points < 50:
            return "لاعب"
        elif total_points < 100:
            return "محترف"
        elif total_points < 250:
            return "خبير"
        elif total_points < 500:
            return "نجم"
        elif total_points < 1000:
            return "أسطورة"
        else:
            return "بطل"
    
    @staticmethod
    def calculate_streak(game_history: list) -> int:
        """حساب سلسلة الانتصارات الحالية"""
        streak = 0
        for game in reversed(game_history):
            if game.get('won', 0) == 1:
                streak += 1
            else:
                break
        return streak


class MessageFormatter:
    """تنسيق الرسائل بشكل أفضل"""
    
    @staticmethod
    def format_error_message(error: str) -> str:
        """تنسيق رسالة خطأ"""
        return f"❌ خطأ: {error}\n\nحاول مرة أخرى أو اكتب 'مساعدة'"
    
    @staticmethod
    def format_success_message(message: str) -> str:
        """تنسيق رسالة نجاح"""
        return f"✅ {message}"
    
    @staticmethod
    def format_info_message(message: str) -> str:
        """تنسيق رسالة معلومات"""
        return f"ℹ️ {message}"
    
    @staticmethod
    def format_points(points: int) -> str:
        """تنسيق النقاط مع الوحدة المناسبة"""
        if points == 0:
            return "لا توجد نقاط"
        elif points == 1:
            return "نقطة واحدة"
        elif points == 2:
            return "نقطتان"
        elif points <= 10:
            return f"{points} نقاط"
        else:
            return f"{points} نقطة"
    
    @staticmethod
    def format_time_ago(timestamp) -> str:
        """تنسيق الوقت منذ حدث معين"""
        from datetime import datetime
        
        if isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp)
        
        now = datetime.utcnow()
        diff = now - timestamp
        
        seconds = diff.total_seconds()
        
        if seconds < 60:
            return "الآن"
        elif seconds < 3600:
            minutes = int(seconds / 60)
            return f"منذ {minutes} دقيقة" if minutes == 1 else f"منذ {minutes} دقائق"
        elif seconds < 86400:
            hours = int(seconds / 3600)
            return f"منذ {hours} ساعة" if hours == 1 else f"منذ {hours} ساعات"
        else:
            days = int(seconds / 86400)
            return f"منذ {days} يوم" if days == 1 else f"منذ {days} أيام"


class CacheManager:
    """إدارة الذاكرة المؤقتة"""
    
    def __init__(self, ttl: int = 300):
        self.cache = {}
        self.ttl = ttl  # Time to live in seconds
    
    def get(self, key: str) -> Optional[any]:
        """الحصول على قيمة من الذاكرة المؤقتة"""
        if key not in self.cache:
            return None
        
        value, timestamp = self.cache[key]
        
        # التحقق من انتهاء الصلاحية
        if time.time() - timestamp > self.ttl:
            del self.cache[key]
            return None
        
        return value
    
    def set(self, key: str, value: any):
        """حفظ قيمة في الذاكرة المؤقتة"""
        self.cache[key] = (value, time.time())
    
    def clear(self):
        """مسح الذاكرة المؤقتة"""
        self.cache.clear()
    
    def cleanup(self):
        """تنظيف القيم المنتهية"""
        now = time.time()
        expired_keys = [
            key for key, (_, timestamp) in self.cache.items()
            if now - timestamp > self.ttl
        ]
        for key in expired_keys:
            del self.cache[key]
        
        logger.info(f"Cleaned up {len(expired_keys)} expired cache entries")


# مثيلات عامة يمكن استخدامها في التطبيق
rate_limiter = RateLimiter(max_requests=10, window=60)
game_rate_limiter = RateLimiter(max_requests=5, window=30)
validator = InputValidator()
stats_calculator = GameStatsCalculator()
message_formatter = MessageFormatter()
cache_manager = CacheManager(ttl=300)
