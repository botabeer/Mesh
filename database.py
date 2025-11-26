"""
Bot Mesh v7.0 - Database System
نظام قاعدة بيانات متقدم مع SQLite
Created by: Abeer Aldosari © 2025
"""

import sqlite3
import json
import logging
from datetime import datetime
from threading import Lock
from contextlib import contextmanager
from typing import Optional, Dict, Any, List

logger = logging.getLogger(__name__)

class Database:
    """نظام قاعدة بيانات متقدم مع دعم كامل للمستخدمين"""
    
    def __init__(self, db_path: str = "data/botmesh.db"):
        self.db_path = db_path
        self.lock = Lock()
        self._init_database()
        logger.info("✅ تم تهيئة قاعدة البيانات")
    
    @contextmanager
    def get_connection(self):
        """Context manager للاتصال الآمن بقاعدة البيانات"""
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            conn.close()
    
    def _init_database(self):
        """إنشاء جداول قاعدة البيانات"""
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
            
            # إنشاء الفهارس لتحسين الأداء
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_points ON users(points DESC)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_last_active ON users(last_active DESC)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_game_history_user ON game_history(user_id)")
            
            logger.info("✅ تم إنشاء جداول قاعدة البيانات")
    
    # ==================== إدارة المستخدمين ====================
    
    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """جلب بيانات مستخدم"""
        with self.lock:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM users WHERE user_id = ?
                """, (user_id,))
                row = cursor.fetchone()
                
                if row:
                    return dict(row)
                return None
    
    def create_user(self, user_id: str, display_name: str) -> Dict[str, Any]:
        """إنشاء مستخدم جديد"""
        with self.lock:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO users (user_id, display_name)
                    VALUES (?, ?)
                """, (user_id, display_name))
                
                logger.info(f"✅ تم إنشاء مستخدم جديد: {display_name} ({user_id})")
                return self.get_user(user_id)
    
    def update_user_name(self, user_id: str, display_name: str) -> bool:
        """تحديث اسم المستخدم"""
        with self.lock:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE users 
                    SET display_name = ?, last_active = CURRENT_TIMESTAMP
                    WHERE user_id = ?
                """, (display_name, user_id))
                
                if cursor.rowcount > 0:
                    logger.info(f"✅ تم تحديث الاسم: {display_name} ({user_id})")
                    return True
                return False
    
    def update_last_active(self, user_id: str):
        """تحديث آخر نشاط"""
        with self.lock:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE users 
                    SET last_active = CURRENT_TIMESTAMP
                    WHERE user_id = ?
                """, (user_id,))
    
    def add_points(self, user_id: str, points: int):
        """إضافة نقاط للمستخدم"""
        with self.lock:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE users 
                    SET points = points + ?,
                        last_active = CURRENT_TIMESTAMP
                    WHERE user_id = ?
                """, (points, user_id))
    
    def increment_games(self, user_id: str, won: bool = False):
        """زيادة عدد الألعاب"""
        with self.lock:
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
    
    def update_theme(self, user_id: str, theme: str) -> bool:
        """تحديث ثيم المستخدم"""
        with self.lock:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE users 
                    SET theme = ?
                    WHERE user_id = ?
                """, (theme, user_id))
                return cursor.rowcount > 0
    
    # ==================== لوحة الصدارة ====================
    
    def get_leaderboard(self, limit: int = 10) -> List[Dict[str, Any]]:
        """جلب لوحة الصدارة"""
        with self.lock:
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
    
    def get_user_rank(self, user_id: str) -> int:
        """جلب ترتيب المستخدم"""
        with self.lock:
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
    
    # ==================== إدارة الألعاب ====================
    
    def save_active_game(self, user_id: str, game_name: str, game_data: Dict[str, Any]):
        """حفظ لعبة نشطة"""
        with self.lock:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO active_games 
                    (user_id, game_name, game_data, started_at)
                    VALUES (?, ?, ?, CURRENT_TIMESTAMP)
                """, (user_id, game_name, json.dumps(game_data, ensure_ascii=False)))
    
    def get_active_game(self, user_id: str) -> Optional[Dict[str, Any]]:
        """جلب لعبة نشطة"""
        with self.lock:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM active_games WHERE user_id = ?
                """, (user_id,))
                
                row = cursor.fetchone()
                if row:
                    data = dict(row)
                    data['game_data'] = json.loads(data['game_data'])
                    return data
                return None
    
    def delete_active_game(self, user_id: str):
        """حذف لعبة نشطة"""
        with self.lock:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    DELETE FROM active_games WHERE user_id = ?
                """, (user_id,))
    
    def log_game_history(self, user_id: str, game_name: str, points: int, completed: bool):
        """تسجيل سجل اللعبة"""
        with self.lock:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO game_history 
                    (user_id, game_name, points_earned, completed)
                    VALUES (?, ?, ?, ?)
                """, (user_id, game_name, points, completed))
    
    # ==================== الإحصائيات ====================
    
    def get_total_users(self) -> int:
        """عدد المستخدمين الإجمالي"""
        with self.lock:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) as count FROM users WHERE status = 'active'")
                return cursor.fetchone()['count']
    
    def get_total_games_played(self) -> int:
        """عدد الألعاب الإجمالي"""
        with self.lock:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT SUM(games_played) as total FROM users")
                result = cursor.fetchone()
                return result['total'] or 0
    
    # ==================== الصيانة ====================
    
    def cleanup_old_games(self, hours: int = 24):
        """حذف الألعاب القديمة"""
        with self.lock:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    DELETE FROM active_games
                    WHERE datetime(started_at) < datetime('now', '-' || ? || ' hours')
                """, (hours,))
                
                deleted = cursor.rowcount
                if deleted > 0:
                    logger.info(f"🧹 تم حذف {deleted} لعبة قديمة")
    
    def optimize_database(self):
        """تحسين قاعدة البيانات"""
        with self.lock:
            with self.get_connection() as conn:
                conn.execute("VACUUM")
                conn.execute("ANALYZE")
                logger.info("✅ تم تحسين قاعدة البيانات")
