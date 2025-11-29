"""
Bot Mesh - Database v12.1 OPTIMIZED
Created by: Abeer Aldosari © 2025
✅ Connection pooling محترف
✅ Prepared statements صحيحة
✅ Retry logic ذكي
✅ Auto-vacuum
✅ مقاومة race conditions
"""

import sqlite3
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Tuple, Any
from contextlib import contextmanager
import logging
import time
import threading
import queue
from functools import wraps

logger = logging.getLogger(__name__)


def retry_on_locked(max_retries=3, delay=0.1):
    """Decorator للإعادة التلقائية عند قفل قاعدة البيانات"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except sqlite3.OperationalError as e:
                    if "locked" in str(e).lower() and attempt < max_retries - 1:
                        time.sleep(delay * (attempt + 1))
                        continue
                    raise
            return func(*args, **kwargs)
        return wrapper
    return decorator


class ConnectionPool:
    """Connection pool احترافي"""
    
    def __init__(self, db_path: str, pool_size: int = 10, timeout: float = 30.0):
        self.db_path = db_path
        self.pool_size = pool_size
        self.timeout = timeout
        self._pool = queue.Queue(maxsize=pool_size)
        self._lock = threading.Lock()
        self._initialize_pool()
    
    def _create_connection(self) -> sqlite3.Connection:
        """إنشاء اتصال مُحسّن"""
        conn = sqlite3.connect(
            self.db_path,
            timeout=self.timeout,
            isolation_level=None,
            check_same_thread=False
        )
        conn.row_factory = sqlite3.Row
        
        # تحسينات الأداء
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=NORMAL")
        conn.execute("PRAGMA cache_size=-64000")  # 64MB
        conn.execute("PRAGMA temp_store=MEMORY")
        conn.execute("PRAGMA mmap_size=268435456")  # 256MB
        conn.execute("PRAGMA foreign_keys=ON")
        conn.execute("PRAGMA auto_vacuum=INCREMENTAL")
        conn.execute("PRAGMA page_size=4096")
        
        return conn
    
    def _initialize_pool(self):
        """ملء البركة بالاتصالات"""
        for _ in range(self.pool_size):
            try:
                conn = self._create_connection()
                self._pool.put(conn, block=False)
            except Exception as e:
                logger.error(f"فشل إنشاء اتصال: {e}")
    
    @contextmanager
    def get_connection(self):
        """الحصول على اتصال من البركة"""
        conn = None
        try:
            # محاولة الحصول على اتصال موجود
            try:
                conn = self._pool.get(block=True, timeout=5.0)
            except queue.Empty:
                # إنشاء اتصال جديد إذا لزم الأمر
                conn = self._create_connection()
            
            yield conn
            
        except Exception as e:
            logger.error(f"خطأ في الاتصال: {e}")
            if conn:
                try:
                    conn.rollback()
                except:
                    pass
            raise
        finally:
            # إرجاع الاتصال للبركة
            if conn:
                try:
                    if self._pool.qsize() < self.pool_size:
                        self._pool.put(conn, block=False)
                    else:
                        conn.close()
                except:
                    try:
                        conn.close()
                    except:
                        pass
    
    def close_all(self):
        """إغلاق جميع الاتصالات"""
        while not self._pool.empty():
            try:
                conn = self._pool.get(block=False)
                conn.close()
            except:
                pass


class Database:
    """Database management محترف"""
    
    def __init__(self, db_path='botmesh.db'):
        self.db_path = db_path
        self._ensure_clean_db()
        self.pool = ConnectionPool(db_path, pool_size=10)
        self.init_database()
        self._start_maintenance_thread()
        logger.info(f"✅ Database initialized: {db_path}")
    
    def _ensure_clean_db(self):
        """التأكد من نظافة قاعدة البيانات"""
        if os.path.exists(self.db_path):
            try:
                conn = sqlite3.connect(self.db_path, timeout=5)
                conn.execute("SELECT 1")
                conn.close()
            except sqlite3.OperationalError:
                try:
                    os.remove(self.db_path)
                    logger.warning("⚠️ تم حذف قاعدة بيانات مقفلة")
                except Exception as e:
                    logger.error(f"❌ فشل حذف قاعدة البيانات: {e}")
    
    @retry_on_locked()
    def init_database(self):
        """تهيئة الجداول مع indexes محسّنة"""
        with self.pool.get_connection() as conn:
            cursor = conn.cursor()
            
            # Users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    points INTEGER DEFAULT 0,
                    is_registered BOOLEAN DEFAULT 0,
                    is_online BOOLEAN DEFAULT 0,
                    last_online TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                ) WITHOUT ROWID
            ''')
            
            # User preferences
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_preferences (
                    user_id TEXT PRIMARY KEY,
                    theme TEXT DEFAULT 'أبيض',
                    language TEXT DEFAULT 'ar',
                    notifications BOOLEAN DEFAULT 1,
                    last_theme_change TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
                ) WITHOUT ROWID
            ''')
            
            # Game sessions
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS game_sessions (
                    session_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    owner_id TEXT NOT NULL,
                    game_name TEXT NOT NULL,
                    mode TEXT DEFAULT 'solo',
                    team_mode BOOLEAN DEFAULT 0,
                    score INTEGER DEFAULT 0,
                    completed BOOLEAN DEFAULT 0,
                    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    completed_at TIMESTAMP,
                    FOREIGN KEY (owner_id) REFERENCES users(user_id)
                )
            ''')
            
            # Team members
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS team_members (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id INTEGER NOT NULL,
                    user_id TEXT NOT NULL,
                    team_name TEXT NOT NULL,
                    score INTEGER DEFAULT 0,
                    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (session_id) REFERENCES game_sessions(session_id) ON DELETE CASCADE,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            ''')
            
            # Team scores
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS team_scores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id INTEGER NOT NULL,
                    team_name TEXT NOT NULL,
                    score INTEGER DEFAULT 0,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (session_id) REFERENCES game_sessions(session_id) ON DELETE CASCADE,
                    UNIQUE(session_id, team_name)
                )
            ''')
            
            # Game statistics
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS game_stats (
                    user_id TEXT NOT NULL,
                    game_name TEXT NOT NULL,
                    plays INTEGER DEFAULT 0,
                    wins INTEGER DEFAULT 0,
                    total_score INTEGER DEFAULT 0,
                    best_score INTEGER DEFAULT 0,
                    avg_score REAL DEFAULT 0.0,
                    last_played TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (user_id, game_name),
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
                ) WITHOUT ROWID
            ''')
            
            # Indexes محسّنة
            indexes = [
                'CREATE INDEX IF NOT EXISTS idx_users_points ON users(points DESC, last_activity DESC)',
                'CREATE INDEX IF NOT EXISTS idx_users_registered ON users(is_registered, points DESC) WHERE is_registered=1',
                'CREATE INDEX IF NOT EXISTS idx_users_online ON users(is_online, last_online DESC) WHERE is_online=1',
                'CREATE INDEX IF NOT EXISTS idx_sessions_owner ON game_sessions(owner_id, started_at DESC)',
                'CREATE INDEX IF NOT EXISTS idx_sessions_active ON game_sessions(completed, started_at DESC) WHERE completed=0',
                'CREATE INDEX IF NOT EXISTS idx_team_members_session ON team_members(session_id, team_name)',
                'CREATE INDEX IF NOT EXISTS idx_game_stats_user ON game_stats(user_id, plays DESC)',
            ]
            
            for idx in indexes:
                cursor.execute(idx)
            
            cursor.execute("ANALYZE")
            logger.info("✅ تم تهيئة الجداول والـ indexes")
    
    @retry_on_locked()
    def get_user(self, user_id: str) -> Optional[Dict]:
        """الحصول على المستخدم - prepared statement"""
        with self.pool.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT u.*, p.theme, p.language, p.notifications
                FROM users u
                LEFT JOIN user_preferences p ON u.user_id = p.user_id
                WHERE u.user_id = ?
            ''', (user_id,))
            row = cursor.fetchone()
            if row:
                user_dict = dict(row)
                if not user_dict.get('theme'):
                    user_dict['theme'] = 'أبيض'
                return user_dict
            return None
    
    @retry_on_locked()
    def create_user(self, user_id: str, name: str) -> bool:
        """إنشاء مستخدم - prepared statement"""
        with self.pool.get_connection() as conn:
            cursor = conn.cursor()
            now = datetime.now()
            name = name[:50] if name else "مستخدم"
            
            cursor.execute('''
                INSERT OR IGNORE INTO users 
                (user_id, name, points, is_registered, is_online, last_online, last_activity)
                VALUES (?, ?, 0, 0, 1, ?, ?)
            ''', (user_id, name, now, now))
            
            cursor.execute('''
                INSERT OR IGNORE INTO user_preferences (user_id, theme)
                VALUES (?, 'أبيض')
            ''', (user_id,))
            
            return True
    
    @retry_on_locked()
    def update_user(self, user_id: str, **kwargs) -> bool:
        """تحديث المستخدم - آمن من SQL injection"""
        if not kwargs:
            return False
        
        allowed_fields = {'name', 'points', 'is_registered', 'is_online'}
        fields = []
        values = []
        
        for key, value in kwargs.items():
            if key in allowed_fields:
                fields.append(f"{key} = ?")
                values.append(value)
        
        if not fields:
            return False
        
        with self.pool.get_connection() as conn:
            cursor = conn.cursor()
            fields.append("last_activity = ?")
            values.extend([datetime.now(), user_id])
            
            query = f"UPDATE users SET {', '.join(fields)} WHERE user_id = ?"
            cursor.execute(query, values)
            return True
    
    @retry_on_locked()
    def add_points(self, user_id: str, points: int) -> bool:
        """إضافة نقاط - atomic operation"""
        with self.pool.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE users 
                SET points = points + ?, last_activity = ?
                WHERE user_id = ?
            ''', (points, datetime.now(), user_id))
            return True
    
    @retry_on_locked()
    def get_leaderboard(self, limit: int = 20) -> List[Tuple[str, int, bool]]:
        """لوحة الصدارة - محسّنة"""
        with self.pool.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT name, points, is_online 
                FROM users 
                WHERE is_registered = 1 AND points > 0
                ORDER BY points DESC, last_activity DESC 
                LIMIT ?
            ''', (limit,))
            return [(row['name'], row['points'], bool(row['is_online'])) 
                    for row in cursor.fetchall()]
    
    def _start_maintenance_thread(self):
        """بدء thread للصيانة الدورية"""
        def maintenance_worker():
            while True:
                try:
                    time.sleep(3600)  # كل ساعة
                    self._perform_maintenance()
                except Exception as e:
                    logger.error(f"خطأ في الصيانة: {e}")
        
        thread = threading.Thread(target=maintenance_worker, daemon=True)
        thread.start()
    
    @retry_on_locked()
    def _perform_maintenance(self):
        """صيانة دورية"""
        with self.pool.get_connection() as conn:
            cursor = conn.cursor()
            
            # Incremental vacuum
            cursor.execute("PRAGMA incremental_vacuum(100)")
            
            # تحديث الإحصائيات
            cursor.execute("ANALYZE")
            
            # حذف الجلسات القديمة
            old_date = datetime.now() - timedelta(days=7)
            cursor.execute('''
                DELETE FROM game_sessions 
                WHERE completed = 1 AND completed_at < ?
            ''', (old_date,))
            
            logger.info("✅ صيانة دورية مكتملة")
    
    @retry_on_locked()
    def cleanup_inactive_users(self, days: int = 30) -> int:
        """تنظيف المستخدمين غير النشطين"""
        with self.pool.get_connection() as conn:
            cursor = conn.cursor()
            cutoff = datetime.now() - timedelta(days=days)
            
            cursor.execute('''
                DELETE FROM users 
                WHERE last_activity < ? AND (is_registered = 0 OR points = 0)
            ''', (cutoff,))
            deleted = cursor.rowcount
            
            if deleted > 0:
                logger.info(f"✅ تم حذف {deleted} مستخدم غير نشط")
            
            return deleted
    
    def close(self):
        """إغلاق قاعدة البيانات"""
        self.pool.close_all()
        logger.info("✅ تم إغلاق قاعدة البيانات")


# Singleton
_db_instance = None
_db_lock = threading.Lock()

def get_database() -> Database:
    """الحصول على singleton instance"""
    global _db_instance
    if _db_instance is None:
        with _db_lock:
            if _db_instance is None:
                _db_instance = Database()
    return _db_instance


__all__ = ['Database', 'get_database']
