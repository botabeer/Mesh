"""
Bot Mesh - Cache Manager
"""
import time
import logging

logger = logging.getLogger(__name__)

class CacheManager:
    def __init__(self, ttl=3600):
        self._cache = {}
        self.ttl = ttl
        self.hits = 0
        self.misses = 0

    def set(self, key, value):
        expiry = time.time() + self.ttl
        self._cache[key] = {"value": value, "expiry": expiry}

    def get(self, key):
        item = self._cache.get(key)
        if not item or time.time() > item["expiry"]:
            self.misses += 1
            self._cache.pop(key, None)
            return None
        self.hits += 1
        return item["value"]

    def delete(self, key):
        return self._cache.pop(key, None) is not None

    def clear(self):
        count = len(self._cache)
        self._cache.clear()
        return count
