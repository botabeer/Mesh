"""
Bot Mesh v7.0 - Game Manager
مدير الألعاب المركزي مع Caching ذكي
Created by: Enhanced System © 2025
"""

import logging
from typing import Dict, Optional, Type, List
from datetime import datetime, timedelta
from threading import Lock
from core.game_engine import BaseGame, GameMode, GameStatus

logger = logging.getLogger(__name__)


class GameCache:
    """نظام Cache ذكي للأسئلة"""
    
    def __init__(self, max_size: int = 1000, ttl_minutes: int = 60):
        self.cache: Dict[str, tuple] = {}  # {key: (data, timestamp)}
        self.max_size = max_size
        self.ttl = timedelta(minutes=ttl_minutes)
        self.lock = Lock()
        
        self.hits = 0
        self.misses = 0

    def get(self, key: str) -> Optional[any]:
        """الحصول على بيانات من Cache"""
        with self.lock:
            if key in self.cache:
                data, timestamp = self.cache[key]
                
                # التحقق من الصلاحية
                if datetime.now() - timestamp < self.ttl:
                    self.hits += 1
                    return data
                else:
                    # حذف البيانات منتهية الصلاحية
                    del self.cache[key]
            
            self.misses += 1
            return None

    def set(self, key: str, data: any):
        """حفظ بيانات في Cache"""
        with self.lock:
            # إذا وصل Cache للحد الأقصى، احذف أقدم العناصر
            if len(self.cache) >= self.max_size:
                # حذف 20% من أقدم العناصر
                items = sorted(self.cache.items(), key=lambda x: x[1][1])
                to_remove = int(self.max_size * 0.2)
                for key, _ in items[:to_remove]:
                    del self.cache[key]
            
            self.cache[key] = (data, datetime.now())

    def clear(self):
        """مسح كل Cache"""
        with self.lock:
            self.cache.clear()
            self.hits = 0
            self.misses = 0

    def get_stats(self) -> Dict:
        """إحصائيات Cache"""
        total = self.hits + self.misses
        hit_rate = (self.hits / total * 100) if total > 0 else 0
        
        return {
            "size": len(self.cache),
            "max_size": self.max_size,
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": f"{hit_rate:.2f}%"
        }


class GameManager:
    """
    مدير الألعاب المركزي
    يتعامل مع إنشاء وإدارة جميع الألعاب
    """

    def __init__(self):
        self.games: Dict[str, BaseGame] = {}  # {room_id: game}
        self.game_types: Dict[str, Type[BaseGame]] = {}  # {game_name: GameClass}
        self.cache = GameCache()
        self.lock = Lock()

        # إحصائيات
        self.stats = {
            "total_games_created": 0,
            "total_games_finished": 0,
            "total_players": set(),
            "games_by_type": {},
            "start_time": datetime.now()
        }

    def register_game(self, game_name: str, game_class: Type[BaseGame]):
        """تسجيل نوع لعبة جديد"""
        self.game_types[game_name] = game_class
        self.stats["games_by_type"][game_name] = 0
        logger.info(f"✅ تم تسجيل لعبة: {game_name}")

    def create_game(
        self,
        room_id: str,
        game_name: str,
        mode: GameMode = GameMode.SINGLE,
        **kwargs
    ) -> Optional[BaseGame]:
        """إنشاء لعبة جديدة"""
        
        # التحقق من وجود نوع اللعبة
        if game_name not in self.game_types:
            logger.error(f"❌ لعبة غير موجودة: {game_name}")
            return None

        with self.lock:
            # إنهاء اللعبة السابقة إن وجدت
            if room_id in self.games:
                old_game = self.games[room_id]
                if old_game.status == GameStatus.ACTIVE:
                    logger.warning(f"⚠️ إيقاف لعبة نشطة في {room_id}")

            try:
                # إنشاء اللعبة الجديدة
                game_class = self.game_types[game_name]
                game = game_class(
                    game_id=f"{room_id}_{datetime.now().timestamp()}",
                    mode=mode,
                    **kwargs
                )
                
                self.games[room_id] = game
                self.stats["total_games_created"] += 1
                self.stats["games_by_type"][game_name] += 1
                
                logger.info(f"🎮 تم إنشاء لعبة {game_name} في {room_id}")
                return game

            except Exception as e:
                logger.error(f"❌ فشل إنشاء اللعبة: {e}", exc_info=True)
                return None

    def get_game(self, room_id: str) -> Optional[BaseGame]:
        """الحصول على لعبة نشطة"""
        return self.games.get(room_id)

    def remove_game(self, room_id: str) -> bool:
        """حذف لعبة"""
        with self.lock:
            if room_id in self.games:
                game = self.games[room_id]
                
                # تحديث الإحصائيات
                if game.status == GameStatus.FINISHED:
                    self.stats["total_games_finished"] += 1
                
                for player_id in game.players:
                    self.stats["total_players"].add(player_id)
                
                del self.games[room_id]
                logger.info(f"🗑️ تم حذف لعبة من {room_id}")
                return True
            
            return False

    def cleanup_expired_games(self, max_minutes: int = 30) -> int:
        """تنظيف الألعاب المنتهية"""
        expired = []
        
        with self.lock:
            for room_id, game in self.games.items():
                if game.is_expired(max_minutes):
                    expired.append(room_id)
        
        for room_id in expired:
            self.remove_game(room_id)
        
        if expired:
            logger.info(f"🧹 تم حذف {len(expired)} ألعاب منتهية")
        
        return len(expired)

    def get_active_games_count(self) -> int:
        """عدد الألعاب النشطة"""
        return len([g for g in self.games.values() if g.status == GameStatus.ACTIVE])

    def get_statistics(self) -> Dict:
        """الحصول على الإحصائيات الكاملة"""
        uptime = (datetime.now() - self.stats["start_time"]).total_seconds()
        
        return {
            "active_games": self.get_active_games_count(),
            "total_games": len(self.games),
            "total_games_created": self.stats["total_games_created"],
            "total_games_finished": self.stats["total_games_finished"],
            "unique_players": len(self.stats["total_players"]),
            "games_by_type": self.stats["games_by_type"],
            "cache_stats": self.cache.get_stats(),
            "uptime_hours": round(uptime / 3600, 2),
            "available_games": list(self.game_types.keys())
        }

    def get_leaderboard(self, limit: int = 10) -> List[Dict]:
        """لوحة الصدارة من جميع الألعاب النشطة"""
        all_players = {}
        
        for game in self.games.values():
            for player in game.players.values():
                if player.user_id not in all_players:
                    all_players[player.user_id] = {
                        "username": player.username,
                        "total_points": 0,
                        "games_played": 0,
                        "correct_answers": 0
                    }
                
                all_players[player.user_id]["total_points"] += player.points
                all_players[player.user_id]["games_played"] += 1
                all_players[player.user_id]["correct_answers"] += player.correct_answers
        
        # ترتيب حسب النقاط
        sorted_players = sorted(
            all_players.values(),
            key=lambda x: x["total_points"],
            reverse=True
        )
        
        return sorted_players[:limit]


# Instance مركزية واحدة
game_manager = GameManager()
