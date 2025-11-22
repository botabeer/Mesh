"""
Bot Mesh - Redis Cache Manager
Created by: Abeer Aldosari © 2025
"""
import json
import logging
from typing import Any, Optional, Dict
from datetime import timedelta
from functools import wraps
import asyncio

logger = logging.getLogger(__name__)

try:
    import redis.asyncio as aioredis
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    logger.warning("Redis not installed. Using in-memory cache.")


class InMemoryCache:
    """كاش في الذاكرة كبديل لـ Redis"""
    
    def __init__(self):
        self._cache: Dict[str, Any] = {}
        self._expiry: Dict[str, float] = {}
    
    async def get(self, key: str) -> Optional[str]:
        import time
        if key in self._expiry and time.time() > self._expiry[key]:
            del self._cache[key]
            del self._expiry[key]
            return None
        return self._cache.get(key)
    
    async def set(self, key: str, value: str, ex: int = None) -> bool:
        import time
        self._cache[key] = value
        if ex:
            self._expiry[key] = time.time() + ex
        return True
    
    async def delete(self, key: str) -> bool:
        self._cache.pop(key, None)
        self._expiry.pop(key, None)
        return True
    
    async def exists(self, key: str) -> bool:
        return key in self._cache
    
    async def incr(self, key: str) -> int:
        val = int(self._cache.get(key, 0)) + 1
        self._cache[key] = str(val)
        return val
    
    async def expire(self, key: str, seconds: int) -> bool:
        import time
        if key in self._cache:
            self._expiry[key] = time.time() + seconds
            return True
        return False
    
    async def keys(self, pattern: str = "*") -> list:
        import fnmatch
        return [k for k in self._cache.keys() if fnmatch.fnmatch(k, pattern)]
    
    async def flushdb(self) -> bool:
        self._cache.clear()
        self._expiry.clear()
        return True


class CacheManager:
    """مدير الكاش الموحد"""
    
    def __init__(self, redis_url: str = None, enabled: bool = True, ttl: int = 3600):
        self.ttl = ttl
        self.enabled = enabled
        self._client = None
        self._redis_url = redis_url
        self._connected = False
    
    async def connect(self) -> bool:
        """الاتصال بـ Redis"""
        if not self.enabled:
            self._client = InMemoryCache()
            self._connected = True
            return True
        
        if REDIS_AVAILABLE and self._redis_url:
            try:
                self._client = aioredis.from_url(
                    self._redis_url,
                    encoding="utf-8",
                    decode_responses=True
                )
                await self._client.ping()
                self._connected = True
                logger.info("✅ Connected to Redis")
                return True
            except Exception as e:
                logger.warning(f"⚠️ Redis connection failed: {e}")
        
        # Fallback to in-memory cache
        self._client = InMemoryCache()
        self._connected = True
        logger.info("📦 Using in-memory cache")
        return True
    
    async def disconnect(self):
        """قطع الاتصال"""
        if self._client and REDIS_AVAILABLE and not isinstance(self._client, InMemoryCache):
            await self._client.close()
        self._connected = False
    
    async def get(self, key: str) -> Optional[Any]:
        """جلب قيمة"""
        if not self._connected:
            await self.connect()
        
        try:
            value = await self._client.get(key)
            if value:
                try:
                    return json.loads(value)
                except json.JSONDecodeError:
                    return value
        except Exception as e:
            logger.error(f"Cache get error: {e}")
        return None
    
    async def set(self, key: str, value: Any, ttl: int = None) -> bool:
        """تخزين قيمة"""
        if not self._connected:
            await self.connect()
        
        try:
            if isinstance(value, (dict, list)):
                value = json.dumps(value, ensure_ascii=False)
            return await self._client.set(key, value, ex=ttl or self.ttl)
        except Exception as e:
            logger.error(f"Cache set error: {e}")
            return False
    
    async def delete(self, key: str) -> bool:
        """حذف قيمة"""
        if not self._connected:
            return False
        
        try:
            return await self._client.delete(key)
        except Exception as e:
            logger.error(f"Cache delete error: {e}")
            return False
    
    async def get_user_theme(self, user_id: str) -> str:
        """جلب ثيم المستخدم"""
        return await self.get(f"theme:{user_id}") or "light"
    
    async def set_user_theme(self, user_id: str, theme: str) -> bool:
        """تخزين ثيم المستخدم"""
        return await self.set(f"theme:{user_id}", theme, ttl=86400 * 30)
    
    async def get_leaderboard(self) -> Optional[list]:
        """جلب لوحة الصدارة من الكاش"""
        return await self.get("leaderboard:top10")
    
    async def set_leaderboard(self, data: list) -> bool:
        """تخزين لوحة الصدارة"""
        return await self.set("leaderboard:top10", data, ttl=300)
    
    async def increment_counter(self, key: str) -> int:
        """زيادة عداد"""
        if not self._connected:
            await self.connect()
        
        try:
            return await self._client.incr(key)
        except Exception as e:
            logger.error(f"Cache incr error: {e}")
            return 0
    
    async def rate_limit_check(self, user_id: str, limit: int = 100, window: int = 60) -> bool:
        """فحص Rate Limiting"""
        key = f"rate:{user_id}"
        count = await self.increment_counter(key)
        
        if count == 1:
            await self._client.expire(key, window)
        
        return count <= limit


def cached(ttl: int = 3600, key_prefix: str = ""):
    """Decorator للكاش"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache = kwargs.get('cache')
            if not cache:
                return await func(*args, **kwargs)
            
            cache_key = f"{key_prefix}:{func.__name__}:{hash(str(args) + str(kwargs))}"
            
            # Try to get from cache
            result = await cache.get(cache_key)
            if result is not None:
                return result
            
            # Execute function and cache result
            result = await func(*args, **kwargs)
            await cache.set(cache_key, result, ttl=ttl)
            
            return result
        return wrapper
    return decorator


# Singleton instance
cache_manager = CacheManager()
