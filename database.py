"""
Bot Mesh - Database Manager (Enhanced with Async Support)
Created by: Abeer Aldosari © 2025
"""
import sqlite3
import asyncio
import logging
import os
from datetime import datetime
from typing import Optional, List, Dict, Any
from contextlib import asynccontextmanager
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)


@dataclass
class User:
    """نموذج المستخدم"""
    user_id: str
    display_name: str
    total_points: int = 0
    games_played: int = 0
    wins: int = 0
    theme: str = "light"
    last_played: Optional[str] = None
    created_at: Optional[str] = None
    
    @property
    def win_rate(self) -> float:
        if self.games_played == 0:
            return 0
        return (self.wins / self.games_played) * 100
    
    @property
    def level(self) -> str:
        if self.total_points < 100:
            return "🌱 مبتدئ"
        elif self.total_points < 500:
            return "⭐ متوسط"
        elif self.total_points < 1000:
            return "🔥 محترف"
        elif self.total_points < 5000:
            return "👑 أسطوري"
        return "💎 خارق"


class ConnectionPool:
    """مجمع اتصالات قاعدة البيانات"""
    
    def __init__(self, db_path: str, max_connections: int = 10):
        self.db_path = db_path
        self.max_connections = max_connections
        self._pool: List[sqlite3.Connection] = []
        self._lock = asyncio.Lock()
        self._executor = ThreadPoolExecutor(max_workers=max_connections)
    
    def _create_connection(self) -> sqlite3.Connection:
        """إنشاء اتصال جديد"""
        conn = sqlite3.connect(self.db_path, check_same_thread=False, timeout=30)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=NORMAL")
        return conn
    
    async def get_connection(self) -> sqlite3.Connection:
        """الحصول على اتصال"""
        async with self._lock:
            if self._pool:
                return self._pool.pop()
            return self._create_connection()
    
    async def release_connection(self, conn: sqlite3.Connection):
        """إرجاع الاتصال للمجمع"""
        async with self._lock:
            if len(self._pool) < self.max_connections:
                self._pool.append(conn)
            else:
                conn.close()
    
    async def close_all(self):
        """إغلاق جميع الاتصالات"""
        async with self._lock:
            for conn in self._pool:
                conn.close()
            self._pool.clear()
        self._executor.shutdown(wait=True)


class Database:
    """مدير قاعدة البيانات المحسن"""
    
    def __init__(self, db_path: str = "data", db_name: str = "game_scores.db", max_connections: int = 10):
        self.db_path = db_path
        self.db_name = db_name
        self.full_path = os.path.join(db_path, db_name)
        self._pool: Optional[ConnectionPool] = None
        self._initialized = False
    
    async def initialize(self):
        """تهيئة قاعدة البيانات"""
        if self._initialized:
            return
        
        # إنشاء المجلد إذا لم يكن موجوداً
        os.makedirs(self.db_path, exist_ok=True)
        
        self._pool = ConnectionPool(self.full_path)
        
        # إنشاء الجداول
        await self._create_tables()
        self._initialized = True
        logger.info(f"✅ Database initialized: {self.full_path}")
    
    async def _create_tables(self):
        """إنشاء الجداول"""
        conn = await self._pool.get_connection()
        try:
            cursor = conn.cursor()
            
            # جدول المستخدمين
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id TEXT PRIMARY KEY,
                    display_name TEXT NOT NULL,
                    total_points INTEGER DEFAULT 0,
                    games_played INTEGER DEFAULT 0,
                    wins INTEGER DEFAULT 0,
                    theme TEXT DEFAULT 'light',
                    last_played TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # جدول سجل الألعاب
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS game_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    game_type TEXT NOT NULL,
                    points INTEGER DEFAULT 0,
                    won INTEGER DEFAULT 0,
                    duration INTEGER,
                    played_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            ''')
            
            # جدول الإنجازات
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS achievements (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    achievement_type TEXT NOT NULL,
                    achieved_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(user_id, achievement_type),
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            ''')
            
            # الفهارس
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_points ON users(total_points DESC)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_history_user ON game_history(user_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_history_date ON game_history(played_at)')
            
            conn.commit()
        finally:
            await self._pool.release_connection(conn)
    
    async def get_user(self, user_id: str) -> Optional[User]:
        """جلب بيانات مستخدم"""
        conn = await self._pool.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
            row = cursor.fetchone()
            
            if row:
                return User(
                    user_id=row['user_id'],
                    display_name=row['display_name'],
                    total_points=row['total_points'],
                    games_played=row['games_played'],
                    wins=row['wins'],
                    theme=row['theme'] or 'light',
                    last_played=row['last_played'],
                    created_at=row['created_at']
                )
            return None
        finally:
            await self._pool.release_connection(conn)
    
    async def update_user_score(self, user_id: str, display_name: str, 
                                points: int, won: bool = False, 
                                game_type: str = None) -> User:
        """تحديث نقاط المستخدم"""
        conn = await self._pool.get_connection()
        try:
            cursor = conn.cursor()
            now = datetime.now().isoformat()
            
            # التحقق من وجود المستخدم
            cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
            existing = cursor.fetchone()
            
            if existing:
                cursor.execute('''
                    UPDATE users SET 
                        total_points = total_points + ?,
                        games_played = games_played + 1,
                        wins = wins + ?,
                        display_name = ?,
                        last_played = ?
                    WHERE user_id = ?
                ''', (points, 1 if won else 0, display_name, now, user_id))
            else:
                cursor.execute('''
                    INSERT INTO users (user_id, display_name, total_points, games_played, wins, last_played, created_at)
                    VALUES (?, ?, ?, 1, ?, ?, ?)
                ''', (user_id, display_name, points, 1 if won else 0, now, now))
            
            # تسجيل في السجل
            if game_type:
                cursor.execute('''
                    INSERT INTO game_history (user_id, game_type, points, won, played_at)
                    VALUES (?, ?, ?, ?, ?)
                ''', (user_id, game_type, points, 1 if won else 0, now))
            
            conn.commit()
            
            # جلب البيانات المحدثة
            return await self.get_user(user_id)
        finally:
            await self._pool.release_connection(conn)
    
    async def get_leaderboard(self, limit: int = 10) -> List[User]:
        """جلب لوحة الصدارة"""
        conn = await self._pool.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM users 
                ORDER BY total_points DESC 
                LIMIT ?
            ''', (limit,))
            
            return [
                User(
                    user_id=row['user_id'],
                    display_name=row['display_name'],
                    total_points=row['total_points'],
                    games_played=row['games_played'],
                    wins=row['wins'],
                    theme=row['theme'] or 'light'
                )
                for row in cursor.fetchall()
            ]
        finally:
            await self._pool.release_connection(conn)
    
    async def get_user_rank(self, user_id: str) -> int:
        """جلب ترتيب المستخدم"""
        conn = await self._pool.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT COUNT(*) + 1 as rank FROM users 
                WHERE total_points > (
                    SELECT COALESCE(total_points, 0) FROM users WHERE user_id = ?
                )
            ''', (user_id,))
            result = cursor.fetchone()
            return result['rank'] if result else 0
        finally:
            await self._pool.release_connection(conn)
    
    async def set_user_theme(self, user_id: str, theme: str) -> bool:
        """تحديث ثيم المستخدم"""
        conn = await self._pool.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET theme = ? WHERE user_id = ?', (theme, user_id))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            await self._pool.release_connection(conn)
    
    async def add_achievement(self, user_id: str, achievement_type: str) -> bool:
        """إضافة إنجاز"""
        conn = await self._pool.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR IGNORE INTO achievements (user_id, achievement_type, achieved_at)
                VALUES (?, ?, ?)
            ''', (user_id, achievement_type, datetime.now().isoformat()))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            await self._pool.release_connection(conn)
    
    async def get_user_achievements(self, user_id: str) -> List[Dict[str, Any]]:
        """جلب إنجازات المستخدم"""
        conn = await self._pool.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT achievement_type, achieved_at FROM achievements 
                WHERE user_id = ? ORDER BY achieved_at DESC
            ''', (user_id,))
            return [dict(row) for row in cursor.fetchall()]
        finally:
            await self._pool.release_connection(conn)
    
    async def get_stats(self) -> Dict[str, Any]:
        """إحصائيات عامة"""
        conn = await self._pool.get_connection()
        try:
            cursor = conn.cursor()
            
            cursor.execute('SELECT COUNT(*) as count FROM users')
            total_users = cursor.fetchone()['count']
            
            cursor.execute('SELECT COUNT(*) as count FROM game_history')
            total_games = cursor.fetchone()['count']
            
            cursor.execute('SELECT SUM(total_points) as sum FROM users')
            total_points = cursor.fetchone()['sum'] or 0
            
            return {
                'total_users': total_users,
                'total_games': total_games,
                'total_points': total_points
            }
        finally:
            await self._pool.release_connection(conn)
    
    async def close(self):
        """إغلاق قاعدة البيانات"""
        if self._pool:
            await self._pool.close_all()
            self._initialized = False


# Singleton instance
db = Database()
