
import os, time, json
from functools import lru_cache
try:
    import redis
except Exception:
    redis = None
import shelve

class StorageFallback:
    def __init__(self, path='points.db'):
        self.path = path
    def _open(self):
        return shelve.open(self.path)
    def get(self, key, default=None):
        with self._open() as db:
            return db.get(key, default)
    def set(self, key, val):
        with self._open() as db:
            db[key]=val
    def delete(self, key):
        with self._open() as db:
            if key in db: del db[key]

class PointsEngine:
    def __init__(self, redis_url=None):
        self.redis_url = redis_url or os.getenv('REDIS_URL')
        self.r = None
        if redis and self.redis_url:
            try:
                self.r = redis.from_url(self.redis_url)
            except Exception:
                self.r = None
        self.fallback = StorageFallback()

    def _key(self, user_id):
        return f"points:{user_id}"

    def get(self, user_id):
        key=self._key(user_id)
        if self.r:
            val=self.r.get(key)
            return json.loads(val) if val else {'points':0,'combo':0,'xp':0,'level':1}
        else:
            return self.fallback.get(key, {'points':0,'combo':0,'xp':0,'level':1})

    def set(self, user_id, data):
        key=self._key(user_id)
        if self.r:
            self.r.set(key, json.dumps(data))
        else:
            self.fallback.set(key, data)

    def add(self, user_id, amount, reason=None):
        data=self.get(user_id)
        data['points'] = data.get('points',0) + amount
        data['xp'] = data.get('xp',0) + max(1, int(amount/2))
        # level up every 100 xp
        while data['xp'] >= 100:
            data['xp'] -= 100
            data['level'] = data.get('level',1) + 1
        self.set(user_id, data)
        return data

    def deduct(self, user_id, amount, reason=None):
        data=self.get(user_id)
        data['points'] = max(0, data.get('points',0) - amount)
        self.set(user_id, data)
        return data

    def combo(self, user_id):
        data=self.get(user_id)
        data['combo'] = data.get('combo',0) + 1
        bonus = min(5, data['combo']) * 2
        data['points'] += bonus
        self.set(user_id, data)
        return data

    def reset_combo(self, user_id):
        data=self.get(user_id)
        data['combo'] = 0
        self.set(user_id, data)
        return data
