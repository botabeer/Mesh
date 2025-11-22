"""
Bot Mesh - Cache Manager (Real Implementation)
Created by: Abeer Aldosari © 2025
"""
import os
import json
import time
import logging
from typing import Any, Optional
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class CacheManager:
    """مدير الكاش البسيط (In-Memory)"""
    
    def __init__(self, default_ttl: int = 3600):
        """
        Args:
            default_ttl: مدة صلاحية الكاش بالثواني (افتراضي: ساعة واحدة)
        """
        self._cache = {}
        self.default_ttl = default_ttl
        self.hits = 0
        self.misses = 0
        logger.info(f"✅ Cache initialized (TTL: {default_ttl}s)")
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """
        حفظ قيمة في الكاش
        
        Args:
            key: المفتاح
            value: القيمة
            ttl: مدة الصلاحية (ثواني) أو None للاستخدام الافتراضي
        
        Returns:
            True إذا نجحت العملية
        """
        try:
            expiry = time.time() + (ttl or self.default_ttl)
            self._cache[key] = {
                'value': value,
                'expiry': expiry,
                'created': datetime.now().isoformat()
            }
            logger.debug(f"📝 Cache SET: {key} (TTL: {ttl or self.default_ttl}s)")
            return True
        except Exception as e:
            logger.error(f"❌ Cache SET error: {e}")
            return False
    
    def get(self, key: str) -> Optional[Any]:
        """
        استرجاع قيمة من الكاش
        
        Args:
            key: المفتاح
        
        Returns:
            القيمة إذا وُجدت ولم تنتهي صلاحيتها، وإلا None
        """
        if key not in self._cache:
            self.misses += 1
            logger.debug(f"❌ Cache MISS: {key}")
            return None
        
        item = self._cache[key]
        
        # التحقق من انتهاء الصلاحية
        if time.time() > item['expiry']:
            self.delete(key)
            self.misses += 1
            logger.debug(f"⏰ Cache EXPIRED: {key}")
            return None
        
        self.hits += 1
        logger.debug(f"✅ Cache HIT: {key}")
        return item['value']
    
    def delete(self, key: str) -> bool:
        """
        حذف قيمة من الكاش
        
        Args:
            key: المفتاح
        
        Returns:
            True إذا تم الحذف بنجاح
        """
        if key in self._cache:
            del self._cache[key]
            logger.debug(f"🗑️ Cache DELETE: {key}")
            return True
        return False
    
    def clear(self) -> int:
        """
        مسح كل الكاش
        
        Returns:
            عدد العناصر التي تم حذفها
        """
        count = len(self._cache)
        self._cache.clear()
        logger.info(f"🧹 Cache CLEARED: {count} items")
        return count
    
    def cleanup(self) -> int:
        """
        تنظيف العناصر منتهية الصلاحية
        
        Returns:
            عدد العناصر التي تم حذفها
        """
        now = time.time()
        expired = [k for k, v in self._cache.items() if now > v['expiry']]
        
        for key in expired:
            del self._cache[key]
        
        if expired:
            logger.info(f"🧹 Cache CLEANUP: {len(expired)} expired items removed")
        
        return len(expired)
    
    def get_stats(self) -> dict:
        """
        إحصائيات الكاش
        
        Returns:
            قاموس بالإحصائيات
        """
        total_requests = self.hits + self.misses
        hit_rate = (self.hits / total_requests * 100) if total_requests > 0 else 0
        
        return {
            'total_items': len(self._cache),
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': f"{hit_rate:.2f}%",
            'total_requests': total_requests
        }
    
    def exists(self, key: str) -> bool:
        """
        التحقق من وجود مفتاح
        
        Args:
            key: المفتاح
        
        Returns:
            True إذا كان موجوداً وصالحاً
        """
        return self.get(key) is not None


class RedisCache:
    """
    واجهة Redis الكاش (اختياري)
    يُستخدم فقط إذا كان Redis متاحاً
    """
    
    def __init__(self, redis_url: str, default_ttl: int = 3600):
        """
        Args:
            redis_url: عنوان Redis
            default_ttl: مدة الصلاحية الافتراضية
        """
        self.redis_url = redis_url
        self.default_ttl = default_ttl
        self._redis = None
        self._connect()
    
    def _connect(self):
        """الاتصال بـ Redis"""
        try:
            import redis
            self._redis = redis.from_url(self.redis_url, decode_responses=True)
            self._redis.ping()
            logger.info(f"✅ Redis connected: {self.redis_url}")
        except ImportError:
            logger.warning("⚠️ redis package not installed. Use: pip install redis")
        except Exception as e:
            logger.error(f"❌ Redis connection failed: {e}")
            self._redis = None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """حفظ في Redis"""
        if not self._redis:
            return False
        
        try:
            serialized = json.dumps(value)
            return self._redis.setex(
                key,
                ttl or self.default_ttl,
                serialized
            )
        except Exception as e:
            logger.error(f"❌ Redis SET error: {e}")
            return False
    
    def get(self, key: str) -> Optional[Any]:
        """استرجاع من Redis"""
        if not self._redis:
            return None
        
        try:
            value = self._redis.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.error(f"❌ Redis GET error: {e}")
            return None
    
    def delete(self, key: str) -> bool:
        """حذف من Redis"""
        if not self._redis:
            return False
        
        try:
            return bool(self._redis.delete(key))
        except Exception as e:
            logger.error(f"❌ Redis DELETE error: {e}")
            return False
    
    def clear(self) -> bool:
        """مسح كل قاعدة البيانات (خطير!)"""
        if not self._redis:
            return False
        
        try:
            self._redis.flushdb()
            return True
        except Exception as e:
            logger.error(f"❌ Redis CLEAR error: {e}")
            return False


# =============================================
# 🏭 Factory Function
# =============================================
def create_cache(use_redis: bool = False, redis_url: str = None, ttl: int = 3600):
    """
    إنشاء نظام الكاش المناسب
    
    Args:
        use_redis: استخدام Redis أو In-Memory
        redis_url: عنوان Redis
        ttl: مدة الصلاحية الافتراضية
    
    Returns:
        CacheManager أو RedisCache
    """
    if use_redis and redis_url:
        cache = RedisCache(redis_url, ttl)
        if cache._redis:
            return cache
        logger.warning("⚠️ Redis failed, falling back to in-memory cache")
    
    return CacheManager(ttl)


# =============================================
# 🌐 Singleton Instance
# =============================================
# يتم إنشاء instance واحد فقط في التطبيق
_cache_instance = None

def get_cache():
    """الحصول على instance الكاش"""
    global _cache_instance
    if _cache_instance is None:
        redis_enabled = os.getenv('REDIS_ENABLED', 'false').lower() == 'true'
        redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
        ttl = int(os.getenv('CACHE_TTL', '3600'))
        
        _cache_instance = create_cache(redis_enabled, redis_url, ttl)
    
    return _cache_instance


# =============================================
# 📝 مثال على الاستخدام
# =============================================
if __name__ == "__main__":
    # إنشاء كاش
    cache = CacheManager(ttl=10)  # 10 ثواني للاختبار
    
    # حفظ
    cache.set("user:123", {"name": "أحمد", "points": 100})
    
    # استرجاع
    user = cache.get("user:123")
    print(f"User: {user}")
    
    # إحصائيات
    print(f"Stats: {cache.get_stats()}")
    
    # انتظار انتهاء الصلاحية
    import time
    time.sleep(11)
    
    # محاولة الاسترجاع بعد انتهاء الصلاحية
    user = cache.get("user:123")  # None
    print(f"After expiry: {user}")
