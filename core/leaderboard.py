
import os, json, time
try:
    import redis
except Exception:
    redis = None
from .points import PointsEngine

class Leaderboard:
    def __init__(self, redis_url=None):
        self.redis_url = redis_url or os.getenv('REDIS_URL')
        self.r = None
        if redis and self.redis_url:
            try:
                self.r = redis.from_url(self.redis_url)
            except Exception:
                self.r = None
        self.points = PointsEngine(redis_url=self.redis_url)

    def update_user(self, user_id):
        data = self.points.get(user_id)
        score = data.get('points',0)
        if self.r:
            self.r.zadd('leaderboard:global', {str(user_id): score})
        # if no redis, nothing to update in central store

    def top(self, n=10):
        if self.r:
            pairs = self.r.zrevrange('leaderboard:global',0,n-1,withscores=True)
            return [(int(uid), int(score)) for uid,score in pairs]
        else:
            # fallback: scan all known keys in shelve (not efficient but works)
            import shelve, os
            dbpath = 'points.db'
            if not os.path.exists(dbpath):
                return []
            with shelve.open(dbpath) as db:
                items = []
                for k in db:
                    try:
                        if k.startswith('points:'):
                            uid = int(k.split(':',1)[1])
                            items.append((uid, db[k].get('points',0)))
                    except Exception:
                        continue
            items.sort(key=lambda x: x[1], reverse=True)
            return items[:n]

    def rank_of(self, user_id):
        if self.r:
            rank = self.r.zrevrank('leaderboard:global', str(user_id))
            if rank is None:
                return None
            return rank+1
        else:
            # fallback compute
            tops = self.top(10000)
            for idx,(uid,score) in enumerate(tops, start=1):
                if int(uid)==int(user_id):
                    return idx
            return None
