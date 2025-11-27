"""
Bot Mesh v9.0 - Database Layer
Created by: Abeer Aldosari © 2025

التحسينات:
✅ SQLite مع persistence على disk
✅ Connection pooling
✅ Thread-safe operations
✅ Auto-backup
✅ Migration support
✅ Performance optimization
"""

import sqlite3
import logging
import os
import shutil
from threading import Lock, local
from contextlib import contextmanager
from datetime import datetime
from typing import Optional, Dict, List, Tuple

logger = logging.getLogger(__name__)

class DB:
    """قاعدة بيانات محسّنة مع persistence و thread safety"""
    
    # إصدار قاعدة البيانات (للـ migrations)
    DB_VERSION = 1
    
    def __init__(self, db_path: str = "data/botmesh.db"):
        """
        تهيئة قاعدة البيانات
        
        Args:
            db_path: مسار ملف قاعدة البيانات
        """
        self.db_path = db_path
        self.lock = Lock()
        self.local = local()  # Thread-local storage للاتصالات
        
        # إنشاء المجلد إذا لم يكن موجوداً
        db_dir = os.path.dirname(db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
        
        # تهيئة قاعدة البيانات
        self._init_database()
        
        logger.info(f"✅ Database initialized at {db_path}")
    
    def _get_connection(self) -> sqlite3.Connection:
        """الحصول على اتصال thread-local"""
        if not hasattr(self.local, 'conn') or self.local.conn is None:
            self.local.conn = sqlite3.connect(
                self.db_path,
                check_same_thread=False,
                timeout=10.0,
                isolation_level='IMMEDIATE'
            )
            self.local.conn.row_factory = sqlite3.Row
            
            # تحسينات الأداء
            self.local.conn.execute("PRAGMA journal_mode=WAL")
            self.local.conn.execute("PRAGMA synchronous=NORMAL")
            self.local.conn.execute("PRAGMA cache_size=-64000")  # 64MB cache
            self.local.conn.execute("PRAGMA temp_store=MEMORY")
        
        return self.local.conn
    
    @contextmanager
    def get_connection(self):
        """Context manager للاتصال الآمن"""
        conn = self._get_connection()
        try:
            yield conn
        except Exception as e:
            conn.rollback()
            raise e
    
    def _init_database(self):
        """إنشاء الجداول والفهارس"""
        with self.lock:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # جدول الإصدارات (للـ migrations)
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS schema_version (
                        version INTEGER PRIMARY KEY,
                        applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # جدول المستخدمين
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        user_id TEXT PRIMARY KEY,
                        name TEXT NOT NULL,
                        points INTEGER DEFAULT 0,
                        theme TEXT DEFAULT 'رمادي',
                        status TEXT DEFAULT 'active',
                        games_played INTEGER DEFAULT 0,
                        total_wins INTEGER DEFAULT 0,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # جدول إحصائيات الألعاب
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS game_stats (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id TEXT NOT NULL,
                        game_name TEXT NOT NULL,
                        points_earned INTEGER DEFAULT 0,
                        completed BOOLEAN DEFAULT 0,
                        played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users(user_id)
                    )
                """)
                
                # الفهارس
                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_users_points 
                    ON users(points DESC, name)
                """)
                
                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_users_status 
                    ON users(status)
                """)
                
                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_game_stats_user 
                    ON game_stats(user_id, played_at DESC)
                """)
                
                # Trigger لتحديث updated_at تلقائياً
                cursor.execute("""
                    CREATE TRIGGER IF NOT EXISTS update_users_timestamp 
                    AFTER UPDATE ON users
                    FOR EACH ROW
                    BEGIN
                        UPDATE users SET updated_at = CURRENT_TIMESTAMP
                        WHERE user_id = NEW.user_id;
                    END
                """)
                
                # التحقق من الإصدار
                cursor.execute("SELECT version FROM schema_version ORDER BY version DESC LIMIT 1")
                result = cursor.fetchone()
                
                if not result:
                    cursor.execute("INSERT INTO schema_version (version) VALUES (?)", (self.DB_VERSION,))
                
                conn.commit()
    
    def backup(self) -> bool:
        """إنشاء نسخة احتياطية"""
        try:
            backup_path = f"{self.db_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            with self.lock:
                # إغلاق كل الاتصالات
                if hasattr(self.local, 'conn') and self.local.conn:
                    self.local.conn.close()
                    self.local.conn = None
                
                # نسخ الملف
                shutil.copy2(self.db_path, backup_path)
            
            logger.info(f"✅ Database backup created: {backup_path}")
            return True
        
        except Exception as e:
            logger.error(f"❌ Backup failed: {e}")
            return False
    
    # ==================== إدارة المستخدمين ====================
    
    def get_user(self, user_id: str) -> Optional[Dict]:
        """
        جلب بيانات مستخدم
        
        Args:
            user_id: معرف المستخدم
        
        Returns:
            dict أو None
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT * FROM users WHERE user_id = ?",
                    (user_id,)
                )
                row = cursor.fetchone()
                
                if row:
                    return dict(row)
                return None
        
        except Exception as e:
            logger.error(f"Error getting user {user_id}: {e}")
            return None
    
    def create_user(self, user_id: str, name: str, theme: str = 'رمادي'):
        """
        إنشاء مستخدم جديد أو تحديث الموجود
        
        Args:
            user_id: معرف المستخدم
            name: اسم المستخدم
            theme: الثيم المفضل
        """
        try:
            with self.lock:
                with self.get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT INTO users (user_id, name, theme, status)
                        VALUES (?, ?, ?, 'active')
                        ON CONFLICT(user_id) DO UPDATE SET
                            name = excluded.name,
                            theme = excluded.theme,
                            status = 'active'
                    """, (user_id, name, theme))
                    
                    conn.commit()
                    logger.info(f"✅ User created/updated: {name} ({user_id})")
        
        except Exception as e:
            logger.error(f"Error creating user: {e}")
    
    def update_theme(self, user_id: str, theme: str):
        """تحديث ثيم المستخدم"""
        try:
            with self.lock:
                with self.get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE users SET theme = ? WHERE user_id = ?
                    """, (theme, user_id))
                    
                    conn.commit()
                    logger.info(f"🎨 Theme updated for {user_id}: {theme}")
        
        except Exception as e:
            logger.error(f"Error updating theme: {e}")
    
    def add_points(self, user_id: str, points: int):
        """إضافة نقاط للمستخدم"""
        try:
            with self.lock:
                with self.get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE users 
                        SET points = points + ?
                        WHERE user_id = ?
                    """, (points, user_id))
                    
                    conn.commit()
                    logger.info(f"⭐ Added {points} points to {user_id}")
        
        except Exception as e:
            logger.error(f"Error adding points: {e}")
    
    def deactivate_user(self, user_id: str):
        """إلغاء تفعيل المستخدم"""
        try:
            with self.lock:
                with self.get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE users SET status = 'inactive' WHERE user_id = ?
                    """, (user_id,))
                    
                    conn.commit()
                    logger.info(f"👋 User deactivated: {user_id}")
        
        except Exception as e:
            logger.error(f"Error deactivating user: {e}")
    
    # ==================== إحصائيات الألعاب ====================
    
    def record_game(self, user_id: str, game_name: str, points: int, completed: bool = True):
        """تسجيل لعبة مكتملة"""
        try:
            with self.lock:
                with self.get_connection() as conn:
                    cursor = conn.cursor()
                    
                    # تسجيل في game_stats
                    cursor.execute("""
                        INSERT INTO game_stats (user_id, game_name, points_earned, completed)
                        VALUES (?, ?, ?, ?)
                    """, (user_id, game_name, points, completed))
                    
                    # تحديث إحصائيات المستخدم
                    cursor.execute("""
                        UPDATE users 
                        SET games_played = games_played + 1,
                            total_wins = total_wins + ?
                        WHERE user_id = ?
                    """, (1 if completed else 0, user_id))
                    
                    conn.commit()
        
        except Exception as e:
            logger.error(f"Error recording game: {e}")
    
    # ==================== لوحة الصدارة ====================
    
    def get_leaderboard(self, limit: int = 10) -> List[Tuple[str, int]]:
        """
        جلب لوحة الصدارة
        
        Args:
            limit: عدد المستخدمين
        
        Returns:
            قائمة [(name, points), ...]
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT name, points
                    FROM users
                    WHERE status = 'active' AND points > 0
                    ORDER BY points DESC, name ASC
                    LIMIT ?
                """, (limit,))
                
                results = cursor.fetchall()
                return [(row['name'], row['points']) for row in results]
        
        except Exception as e:
            logger.error(f"Error getting leaderboard: {e}")
            return []
    
    def get_user_rank(self, user_id: str) -> int:
        """جلب ترتيب المستخدم"""
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
    
    # ==================== الإحصائيات ====================
    
    def get_total_users(self) -> int:
        """عدد المستخدمين النشطين"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT COUNT(*) as count
                    FROM users
                    WHERE status = 'active'
                """)
                
                result = cursor.fetchone()
                return result['count'] if result else 0
        
        except Exception as e:
            logger.error(f"Error getting total users: {e}")
            return 0
    
    def get_total_points(self) -> int:
        """إجمالي النقاط"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT SUM(points) as total
                    FROM users
                    WHERE status = 'active'
                """)
                
                result = cursor.fetchone()
                return result['total'] or 0
        
        except Exception as e:
            logger.error(f"Error getting total points: {e}")
            return 0
    
    def get_stats(self) -> Dict:
        """الحصول على إحصائيات شاملة"""
        try:
            return {
                'total_users': self.get_total_users(),
                'total_points': self.get_total_points(),
                'leaderboard_preview': self.get_leaderboard(3)
            }
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            return {
                'total_users': 0,
                'total_points': 0,
                'leaderboard_preview': []
            }
    
    def close(self):
        """إغلاق كل الاتصالات"""
        if hasattr(self.local, 'conn') and self.local.conn:
            self.local.conn.close()
            self.local.conn = None
