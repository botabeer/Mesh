"""
💾 Bot Mesh v8.0 - Database
Created by: Abeer Aldosari © 2025

✅ SQLite in-memory
✅ حفظ الثيم لكل مستخدم
✅ إدارة النقاط
✅ لوحة الصدارة
"""

import sqlite3
import logging
from threading import Lock
from contextlib import contextmanager
from typing import Optional, Dict, List

logger = logging.getLogger(__name__)

class DB:
    """قاعدة بيانات SQLite في الذاكرة"""
    
    def __init__(self, db_path=":memory:"):
        """
        تهيئة قاعدة البيانات
        
        Args:
            db_path: مسار قاعدة البيانات (افتراضياً في الذاكرة)
        """
        self.db_path = db_path
        self.lock = Lock()
        self.conn = None
        self._init_database()
        logger.info("✅ Database initialized")
    
    @contextmanager
    def get_connection(self):
        """الحصول على اتصال آمن"""
        if self.conn is None:
            self.conn = sqlite3.connect(
                self.db_path,
                check_same_thread=False,
                isolation_level=None
            )
            self.conn.row_factory = sqlite3.Row
        
        yield self.conn
    
    def _init_database(self):
        """إنشاء الجداول"""
        with self.lock:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # جدول المستخدمين
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        user_id TEXT PRIMARY KEY,
                        name TEXT NOT NULL,
                        points INTEGER DEFAULT 0,
                        theme TEXT DEFAULT '💜',
                        status TEXT DEFAULT 'active',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # فهرس للنقاط (للصدارة)
                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_points 
                    ON users(points DESC, name)
                """)
                
                conn.commit()
    
    # ==================== إدارة المستخدمين ====================
    
    def get_user(self, user_id: str) -> Optional[Dict]:
        """
        جلب بيانات مستخدم
        
        Args:
            user_id: معرف المستخدم
        
        Returns:
            dict أو None
        """
        with self.lock:
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
    
    def create_user(self, user_id: str, name: str, theme: str = '💜'):
        """
        إنشاء مستخدم جديد
        
        Args:
            user_id: معرف المستخدم
            name: اسم المستخدم
            theme: الثيم المفضل
        """
        with self.lock:
            try:
                with self.get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT OR REPLACE INTO users (user_id, name, theme, status)
                        VALUES (?, ?, ?, 'active')
                    """, (user_id, name, theme))
                    conn.commit()
                    
                    logger.info(f"✅ Created user: {name} ({user_id})")
                    
            except Exception as e:
                logger.error(f"Error creating user: {e}")
    
    def update_theme(self, user_id: str, theme: str):
        """
        تحديث ثيم المستخدم
        
        Args:
            user_id: معرف المستخدم
            theme: الثيم الجديد
        """
        with self.lock:
            try:
                with self.get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE users 
                        SET theme = ?, updated_at = CURRENT_TIMESTAMP
                        WHERE user_id = ?
                    """, (theme, user_id))
                    conn.commit()
                    
                    logger.info(f"🎨 Updated theme for {user_id}: {theme}")
                    
            except Exception as e:
                logger.error(f"Error updating theme: {e}")
    
    def add_points(self, user_id: str, points: int):
        """
        إضافة نقاط للمستخدم
        
        Args:
            user_id: معرف المستخدم
            points: النقاط المراد إضافتها
        """
        with self.lock:
            try:
                with self.get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE users 
                        SET points = points + ?,
                            updated_at = CURRENT_TIMESTAMP
                        WHERE user_id = ?
                    """, (points, user_id))
                    conn.commit()
                    
                    logger.info(f"⭐ Added {points} points to {user_id}")
                    
            except Exception as e:
                logger.error(f"Error adding points: {e}")
    
    def deactivate_user(self, user_id: str):
        """
        إلغاء تفعيل المستخدم (الانسحاب)
        
        Args:
            user_id: معرف المستخدم
        """
        with self.lock:
            try:
                with self.get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE users 
                        SET status = 'inactive',
                            updated_at = CURRENT_TIMESTAMP
                        WHERE user_id = ?
                    """, (user_id,))
                    conn.commit()
                    
                    logger.info(f"👋 Deactivated user: {user_id}")
                    
            except Exception as e:
                logger.error(f"Error deactivating user: {e}")
    
    # ==================== لوحة الصدارة ====================
    
    def get_leaderboard(self, limit: int = 10) -> List[tuple]:
        """
        جلب لوحة الصدارة
        
        Args:
            limit: عدد المستخدمين
        
        Returns:
            قائمة [(name, points), ...]
        """
        with self.lock:
            try:
                with self.get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        SELECT name, points
                        FROM users
                        WHERE status = 'active'
                        ORDER BY points DESC, name ASC
                        LIMIT ?
                    """, (limit,))
                    
                    results = cursor.fetchall()
                    return [(row['name'], row['points']) for row in results]
                    
            except Exception as e:
                logger.error(f"Error getting leaderboard: {e}")
                return []
    
    def get_user_rank(self, user_id: str) -> int:
        """
        جلب ترتيب المستخدم
        
        Args:
            user_id: معرف المستخدم
        
        Returns:
            الترتيب (1-based)
        """
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
    
    # ==================== الإحصائيات ====================
    
    def get_total_users(self) -> int:
        """
        عدد المستخدمين النشطين
        
        Returns:
            عدد المستخدمين
        """
        with self.lock:
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
        """
        إجمالي النقاط لجميع المستخدمين
        
        Returns:
            إجمالي النقاط
        """
        with self.lock:
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
        """
        الحصول على إحصائيات كاملة
        
        Returns:
            dict مع الإحصائيات
        """
        return {
            'total_users': self.get_total_users(),
            'total_points': self.get_total_points(),
            'leaderboard_preview': self.get_leaderboard(3)
        }
