"""
Bot Mesh v7.0 - Database System (FIXED)
نظام قاعدة بيانات محسّن مع حل مشكلة Database Locked
Created by: Abeer Aldosari © 2025
"""

import sqlite3
import json
import logging
from datetime import datetime
from threading import Lock
from contextlib import contextmanager
from typing import Optional, Dict, Any, List
import time

logger = logging.getLogger(__name__)

class Database:
    """نظام قاعدة بيانات محسّن مع حل مشكلة القفل"""
    
    def __init__(self, db_path: str = "data/botmesh.db"):
        self.db_path = db_path
        self.lock = Lock()
        self._init_database()
        logger.info("✅ تم تهيئة قاعدة البيانات")
    
    @contextmanager
    def get_connection(self, retries=5, retry_delay=0.1):
        """
        Context manager للاتصال الآمن بقاعدة البيانات
        مع إعادة المحاولة في حالة القفل
        """
        conn = None
        for attempt in range(retries):
            try:
                # تفعيل WAL mode لتحسين التزامن
                conn = sqlite3.connect(
                    self.db_path,
                    timeout=30.0,  # انتظار 30 ثانية قبل رفع خطأ القفل
                    check_same_thread=False,
                    isolation_level=None  # autocommit mode
                )
                conn.row_factory = sqlite3.Row
                
                # تفعيل WAL mode
                conn.execute("PRAGMA journal_mode=WAL")
                conn.execute("PRAGMA busy_timeout=30000")  # 30 ثانية
                
                yield conn
                return
                
            except sqlite3.OperationalError as e:
                if "locked" in str(e).lower() and attempt < retries - 1:
                    logger.warning(f"⚠️ Database locked, retry {attempt + 1}/{retries}")
                    if conn:
                        conn.close()
                    time.sleep(retry_delay * (attempt + 1))
                    continue
                else:
                    logger.error(f"Database error: {e}")
                    if conn:
                        conn.close()
                    raise
            except Exception as e:
                logger.error(f"Database error: {e}")
                if conn:
                    conn.close()
                raise
            finally:
                if conn:
                    try:
                        conn.close()
                    except:
                        pass
    
    def _init_database(self):
        """إنشاء جداول قاعدة البيانات"""
        with self.lock:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # جدول المستخدمين
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        user_id TEXT PRIMARY KEY,
                        display_name TEXT NOT NULL,
                        points INTEGER DEFAULT 0,
                        games_played INTEGER DEFAULT 0,
                        wins INTEGER DEFAULT 0,
                        theme TEXT DEFAULT 'أزرق',
                        joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        status TEXT DEFAULT 'active'
                    )
                """)
                
                # جدول الألعاب النشطة
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS active_games (
                        user_id TEXT PRIMARY KEY,
                        game_name TEXT NOT NULL,
                        game_data TEXT,
                        started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users(user_id)
                    )
                """)
                
                # جدول سجل الألعاب
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS game_history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id TEXT NOT NULL,
                        game_name TEXT NOT NULL,
                        points_earned INTEGER DEFAULT 0,
                        completed BOOLEAN DEFAULT 0,
                        played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users(user_id)
                    )
                """)
                
                # جدول الإحصائيات
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS statistics (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        stat_key TEXT UNIQUE NOT NULL,
                        stat_value TEXT,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # إنشاء الفهارس
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_points ON users(points DESC)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_last_active ON users(last_active DESC)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_game_history_user ON game_history(user_id)")
                
                conn.commit()
                logger.info("✅ تم إنشاء جداول قاعدة البيانات")
    
    # ==================== إدارة المستخدمين ====================
    
    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """جلب بيانات مستخدم"""
        with self.lock:
            try:
                with self.get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
                    row = cursor.fetchone()
                    
                    if row:
                        return dict(row)
                    return None
            except Exception as e:
                logger.error(f"Error getting user {user_id}: {e}")
                return None
    
    def create_user(self, user_id: str, display_name: str) -> Dict[str, Any]:
        """إنشاء مستخدم جديد"""
        with self.lock:
            try:
                with self.get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT OR IGNORE INTO users (user_id, display_name)
                        VALUES (?, ?)
                    """, (user_id, display_name))
                    conn.commit()
                    
                    logger.info(f"✅ تم إنشاء مستخدم جديد: {display_name} ({user_id})")
                    return self.get_user(user_id)
            except Exception as e:
                logger.error(f"Error creating user {user_id}: {e}")
                # إرجاع مستخدم افتراضي في حالة الفشل
                return {
                    'user_id': user_id,
                    'display_name': display_name,
                    'points': 0,
                    'games_played': 0,
                    'wins': 0,
                    'theme': 'أزرق',
                    'status': 'active'
                }
    
    def update_user_name(self, user_id: str, display_name: str) -> bool:
        """تحديث اسم المستخدم"""
        with self.lock:
            try:
                with self.get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE users 
                        SET display_name = ?, last_active = CURRENT_TIMESTAMP
                        WHERE user_id = ?
                    """, (display_name, user_id))
                    conn.commit()
                    
                    if cursor.rowcount > 0:
                        logger.info(f"✅ تم تحديث الاسم: {display_name} ({user_id})")
                        return True
                    return False
            except Exception as e:
                logger.error(f"Error updating user name: {e}")
                return False
    
    def update_last_active(self, user_id: str):
        """تحديث آخر نشاط"""
        with self.lock:
            try:
                with self.get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE users 
                        SET last_active = CURRENT_TIMESTAMP
                        WHERE user_id = ?
                    """, (user_id,))
                    conn.commit()
            except Exception as e:
                logger.error(f"Error updating last active: {e}")
    
    def add_points(self, user_id: str, points: int):
        """إضافة نقاط للمستخدم"""
        with self.lock:
            try:
                with self.get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE users 
                        SET points = points + ?,
                            last_active = CURRENT_TIMESTAMP
                        WHERE user_id = ?
                    """, (points, user_id))
                    conn.commit()
            except Exception as e:
                logger.error(f"Error adding points: {e}")
    
    def increment_games(self, user_id: str, won: bool = False):
        """زيادة عدد الألعاب"""
        with self.lock:
            try:
                with self.get_connection() as conn:
                    cursor = conn.cursor()
                    if won:
                        cursor.execute("""
                            UPDATE users 
                            SET games_played = games_played + 1,
                                wins = wins + 1
                            WHERE user_id = ?
                        """, (user_id,))
                    else:
                        cursor.execute("""
                            UPDATE users 
                            SET games_played = games_played + 1
                            WHERE user_id = ?
                        """, (user_id,))
                    conn.commit()
            except Exception as e:
                logger.error(f"Error incrementing games: {e}")
    
    def update_theme(self, user_id: str, theme: str) -> bool:
        """تحديث ثيم المستخدم"""
        with self.lock:
            try:
                with self.get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE users 
                        SET theme = ?
                        WHERE user_id = ?
                    """, (theme, user_id))
                    conn.commit()
                    return cursor.rowcount > 0
            except Exception as e:
                logger.error(f"Error updating theme: {e}")
                return False
    
    # ==================== لوحة الصدارة ====================
    
    def get_leaderboard(self, limit: int = 10) -> List[Dict[str, Any]]:
        """جلب لوحة الصدارة"""
        with self.lock:
            try:
                with self.get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        SELECT display_name, points, games_played, wins
                        FROM users
                        WHERE status = 'active'
                        ORDER BY points DESC, wins DESC
                        LIMIT ?
                    """, (limit,))
                    
                    return [dict(row) for row in cursor.fetchall()]
            except Exception as e:
                logger.error(f"Error getting leaderboard: {e}")
                return []
    
    def get_user_rank(self, user_id: str) -> int:
        """جلب ترتيب المستخدم"""
        with self.lock:
            try:
                with self.get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        SELECT COUNT(*) + 1 as rank
                        FROM users
                        WHERE points > (
                            SELECT points FROM users WHERE user_id = ?
                        ) AND status = 'active'
                    """, (user_id,))
                    
                    result = cursor.fetchone()
                    return result['rank'] if result else 0
            except Exception as e:
                logger.error(f"Error getting user rank: {e}")
                return 0
    
    # ==================== إدارة الألعاب ====================
    
    def save_active_game(self, user_id: str, game_name: str, game_data: Dict[str, Any]):
        """حفظ لعبة نشطة"""
        with self.lock:
            try:
                with self.get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT OR REPLACE INTO active_games 
                        (user_id, game_name, game_data, started_at)
                        VALUES (?, ?, ?, CURRENT_TIMESTAMP)
                    """, (user_id, game_name, json.dumps(game_data, ensure_ascii=False)))
                    conn.commit()
            except Exception as e:
                logger.error(f"Error saving active game: {e}")
    
    def get_active_game(self, user_id: str) -> Optional[Dict[str, Any]]:
        """جلب لعبة نشطة"""
        with self.lock:
            try:
                with self.get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM active_games WHERE user_id = ?", (user_id,))
                    
                    row = cursor.fetchone()
                    if row:
                        data = dict(row)
                        data['game_data'] = json.loads(data['game_data'])
                        return data
                    return None
            except Exception as e:
                logger.error(f"Error getting active game: {e}")
                return None
    
    def delete_active_game(self, user_id: str):
        """حذف لعبة نشطة"""
        with self.lock:
            try:
                with self.get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM active_games WHERE user_id = ?", (user_id,))
                    conn.commit()
            except Exception as e:
                logger.error(f"Error deleting active game: {e}")
    
    def log_game_history(self, user_id: str, game_name: str, points: int, completed: bool):
        """تسجيل سجل اللعبة"""
        with self.lock:
            try:
                with self.get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT INTO game_history 
                        (user_id, game_name, points_earned, completed)
                        VALUES (?, ?, ?, ?)
                    """, (user_id, game_name, points, completed))
                    conn.commit()
            except Exception as e:
                logger.error(f"Error logging game history: {e}")
    
    # ==================== الإحصائيات ====================
    
    def get_total_users(self) -> int:
        """عدد المستخدمين الإجمالي"""
        with self.lock:
            try:
                with self.get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT COUNT(*) as count FROM users WHERE status = 'active'")
                    return cursor.fetchone()['count']
            except Exception as e:
                logger.error(f"Error getting total users: {e}")
                return 0
    
    def get_total_games_played(self) -> int:
        """عدد الألعاب الإجمالي"""
        with self.lock:
            try:
                with self.get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT SUM(games_played) as total FROM users")
                    result = cursor.fetchone()
                    return result['total'] or 0
            except Exception as e:
                logger.error(f"Error getting total games: {e}")
                return 0
    
    # ==================== الصيانة ====================
    
    def cleanup_old_games(self, hours: int = 24):
        """حذف الألعاب القديمة"""
        with self.lock:
            try:
                with self.get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        DELETE FROM active_games
                        WHERE datetime(started_at) < datetime('now', '-' || ? || ' hours')
                    """, (hours,))
                    conn.commit()
                    
                    deleted = cursor.rowcount
                    if deleted > 0:
                        logger.info(f"🧹 تم حذف {deleted} لعبة قديمة")
            except Exception as e:
                logger.error(f"Error cleaning old games: {e}")
    
    def optimize_database(self):
        """تحسين قاعدة البيانات"""
        with self.lock:
            try:
                with self.get_connection() as conn:
                    conn.execute("VACUUM")
                    conn.execute("ANALYZE")
                    logger.info("✅ تم تحسين قاعدة البيانات")
            except Exception as e:
                logger.error(f"Error optimizing database: {e}")
