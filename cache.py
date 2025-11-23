import time

class CacheManager:
    def __init__(self):
        self._cache = {}

    def set(self, key, value, ttl=604800):  # أسبوع
        expiry = time.time() + ttl
        self._cache[key] = {'value': value, 'expiry': expiry}

    def get(self, key):
        item = self._cache.get(key)
        if not item or time.time() > item['expiry']:
            return None
        return item['value']

    def delete(self, key):
        if key in self._cache:
            del self._cache[key]
