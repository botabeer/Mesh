"""
Bot Mesh - Cache Manager
"""
import time
import logging

logger = logging.getLogger(__name__)

class CacheManager:
    """In-Memory Cache"""
    def __init__(self, ttl=3600):
        self._cache = {}
        self.ttl = ttl
        self.hits = 0
        self.misses = 0
        logger.info(f"Cache initialized with TTL={ttl}s")

    def set(self, key, value, ttl=None):
        expiry = time.time() + (ttl or self.ttl)
        self._cache[key] = {'value': value, 'expiry': expiry}
        return True

    def get(self, key):
        item = self._cache.get(key)
        if not item:
            self.misses += 1
            return None
        if time.time() > item['expiry']:
            self._cache.pop(key, None)
            self.misses += 1
            return None
        self.hits += 1
        return item['value']

    def delete(self, key):
        return self._cache.pop(key, None) is not None

    def clear(self):
        count = len(self._cache)
        self._cache.clear()
        return count

    def stats(self):
        total = self.hits + self.misses
        hit_rate = (self.hits/total*100) if total else 0
        return {'hits': self.hits, 'misses': self.misses, 'hit_rate': f"{hit_rate:.2f}%"}
