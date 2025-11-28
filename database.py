"""
Bot Mesh - Database Management System
Created by: Abeer Aldosari © 2025

Features:
- SQLite database for persistent storage
- Lock-free initialization
- Thread-safe operations
"""

import sqlite3
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Tuple
import logging
import time

logger = logging.getLogger(__name__)


class Database:
    """نظام إدارة قاعدة البيانات"""
    
    def __init__(self, db_path='botmesh.db'):
        self.db_path = db_path
        # حذف قاعدة البيانات القديمة إذا كانت مقفلة
        self._ensure_clean_db()
        self.init_database()
    
    def _ensure_clean_db(self):
        """التأكد من قاعدة بيانات نظيفة"""
        if os.path.exists(self.db_path):
            try:
                # محاولة الاتصال
                conn = sqlite3.connect(self.db_path, timeout=5)
                conn.close()
            except:
                # إذا فشل، احذف الملف
                try:
                    os.remove(self.db_path)
                    logger.warning("⚠️ Removed locked database file")
                except:
                    pass
    
    def get_connection(self):
        """إنشاء اتصال بقاعدة البيانات"""
        conn = sqlite3.connect(
            self.db_path,
            timeout=60.0,
            isolation_level=None,  # autocommit mode
            check_same_thread=False
        )
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """إنشاء جداول قاعدة البيانات"""
        for attempt in range(3):
            try:
                conn = self.get_connection()
                cursor = conn.cursor()
                
                # جدول المستخدمين
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        user_id TEXT PRIMARY KEY,
                        name TEXT NOT NULL,
                        points INTEGER DEFAULT 0,
                        is_registered BOOLEAN DEFAULT 0,
                        theme TEXT DEFAULT 'أبيض',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # جدول جلسات الألعاب
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS game_sessions (
                        session_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id TEXT NOT NULL,
                        game_name TEXT NOT NULL,
                        score INTEGER DEFAULT 0,
                        completed BOOLEAN DEFAULT 0,
                        played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # جدول إحصائيات الألعاب
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS game_stats (
                        game_name TEXT PRIMARY KEY,
                        plays INTEGER DEFAULT 0,
                        completions INTEGER DEFAULT 0,
                        total_points INTEGER DEFAULT 0,
                        avg_score REAL DEFAULT 0.0,
                        last_played TIMESTAMP
                    )
                ''')
                
                # جدول الإنجازات
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS achievements (
                        achievement_id TEXT PRIMARY KEY,
                        name TEXT NOT NULL,
                        description TEXT,
                        points_reward INTEGER DEFAULT 0,
                        icon TEXT
                    )
                ''')
                
                # جدول إنجازات المستخدمين
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS user_achievements (
                        user_id TEXT NOT NULL,
                        achievement_id TEXT NOT NULL,
                        unlocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        PRIMARY KEY (user_id, achievement_id)
                    )
                ''')
                
                # إنشاء indexes
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_points ON users(points DESC)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_activity ON users(last_activity)')
                
                conn.close()
                logger.info("✅ Database initialized successfully")
                return
                
            except sqlite3.OperationalError as e:
                if attempt < 2:
                    logger.warning(f"⚠️ DB init attempt {attempt + 1} failed, retrying...")
                    time.sleep(1)
                else:
                    logger.error(f"❌ DB init failed: {e}")
                    raise
    
    # ==================== User Management ====================
    
    def get_user(self, user_id: str) -> Optional[Dict]:
        """الحصول على بيانات مستخدم"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
            row = cursor.fetchone()
            conn.close()
            return dict(row) if row else None
        except:
            return None
    
    def create_user(self, user_id: str, name: str) -> bool:
        """إنشاء مستخدم جديد"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR IGNORE INTO users (user_id, name, points, is_registered, theme, last_activity)
                VALUES (?, ?, 0, 0, 'أبيض', ?)
            ''', (user_id, name, datetime.now()))
            conn.close()
            return True
        except:
            return False
    
    def update_user(self, user_id: str, **kwargs) -> bool:
        """تحديث بيانات مستخدم"""
        if not kwargs:
            return False
        
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            fields = []
            values = []
            for key, value in kwargs.items():
                if key in ['name', 'points', 'is_registered', 'theme']:
                    fields.append(f"{key} = ?")
                    values.append(value)
            
            if not fields:
                return False
            
            fields.append("last_activity = ?")
            values.append(datetime.now())
            values.append(user_id)
            
            query = f"UPDATE users SET {', '.join(fields)} WHERE user_id = ?"
            cursor.execute(query, values)
            conn.close()
            return True
        except:
            return False
    
    def add_points(self, user_id: str, points: int) -> bool:
        """إضافة نقاط لمستخدم"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE users 
                SET points = points + ?, last_activity = ?
                WHERE user_id = ?
            ''', (points, datetime.now(), user_id))
            conn.close()
            return True
        except:
            return False
    
    def update_activity(self, user_id: str) -> bool:
        """تحديث آخر نشاط"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE users SET last_activity = ? WHERE user_id = ?
            ''', (datetime.now(), user_id))
            conn.close()
            return True
        except:
            return False
    
    def get_leaderboard(self, limit: int = 10) -> List[Tuple[str, int]]:
        """الحصول على لوحة الصدارة"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT name, points FROM users 
                WHERE is_registered = 1 
                ORDER BY points DESC LIMIT ?
            ''', (limit,))
            leaderboard = cursor.fetchall()
            conn.close()
            return [(row['name'], row['points']) for row in leaderboard]
        except:
            return []
    
    def get_user_rank(self, user_id: str) -> Optional[int]:
        """الحصول على ترتيب المستخدم"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT COUNT(*) + 1 as rank FROM users 
                WHERE is_registered = 1 AND points > (SELECT points FROM users WHERE user_id = ?)
            ''', (user_id,))
            row = cursor.fetchone()
            conn.close()
            return row['rank'] if row else None
        except:
            return None
    
    # ==================== Game Sessions ====================
    
    def create_game_session(self, user_id: str, game_name: str) -> int:
        """إنشاء جلسة لعبة جديدة"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO game_sessions (user_id, game_name, score, completed)
                VALUES (?, ?, 0, 0)
            ''', (user_id, game_name))
            session_id = cursor.lastrowid
            conn.close()
            return session_id
        except:
            return 0
    
    def complete_game_session(self, session_id: int, score: int) -> bool:
        """إكمال جلسة لعبة"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE game_sessions SET score = ?, completed = 1 WHERE session_id = ?
            ''', (score, session_id))
            conn.close()
            return True
        except:
            return False
    
    def get_user_game_stats(self, user_id: str) -> Dict[str, int]:
        """إحصائيات ألعاب المستخدم"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT game_name, COUNT(*) as plays
                FROM game_sessions WHERE user_id = ? GROUP BY game_name
            ''', (user_id,))
            stats = {row['game_name']: row['plays'] for row in cursor.fetchall()}
            conn.close()
            return stats
        except:
            return {}
    
    # ==================== Game Statistics ====================
    
    def update_game_stats(self, game_name: str, completed: bool = False, points: int = 0):
        """تحديث إحصائيات لعبة"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM game_stats WHERE game_name = ?', (game_name,))
            exists = cursor.fetchone()
            
            if exists:
                cursor.execute('''
                    UPDATE game_stats 
                    SET plays = plays + 1, completions = completions + ?,
                        total_points = total_points + ?, last_played = ?
                    WHERE game_name = ?
                ''', (1 if completed else 0, points, datetime.now(), game_name))
            else:
                cursor.execute('''
                    INSERT INTO game_stats (game_name, plays, completions, total_points, last_played)
                    VALUES (?, 1, ?, ?, ?)
                ''', (game_name, 1 if completed else 0, points, datetime.now()))
            
            conn.close()
        except:
            pass
    
    def get_all_game_stats(self) -> Dict[str, Dict]:
        """الحصول على إحصائيات جميع الألعاب"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM game_stats')
            rows = cursor.fetchall()
            conn.close()
            return {row['game_name']: dict(row) for row in rows}
        except:
            return {}
    
    # ==================== Achievements ====================
    
    def create_achievement(self, achievement_id: str, name: str, 
                          description: str, points_reward: int, icon: str) -> bool:
        """إنشاء إنجاز"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR IGNORE INTO achievements (achievement_id, name, description, points_reward, icon)
                VALUES (?, ?, ?, ?, ?)
            ''', (achievement_id, name, description, points_reward, icon))
            conn.close()
            return True
        except:
            return False
    
    def unlock_achievement(self, user_id: str, achievement_id: str) -> bool:
        """فتح إنجاز للمستخدم"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT 1 FROM user_achievements 
                WHERE user_id = ? AND achievement_id = ?
            ''', (user_id, achievement_id))
            
            if cursor.fetchone():
                conn.close()
                return False
            
            cursor.execute('''
                INSERT INTO user_achievements (user_id, achievement_id) VALUES (?, ?)
            ''', (user_id, achievement_id))
            
            cursor.execute('''
                UPDATE users SET points = points + (
                    SELECT points_reward FROM achievements WHERE achievement_id = ?
                ) WHERE user_id = ?
            ''', (achievement_id, user_id))
            
            conn.close()
            return True
        except:
            return False
    
    def get_user_achievements(self, user_id: str) -> List[Dict]:
        """الحصول على إنجازات المستخدم"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT a.*, ua.unlocked_at
                FROM achievements a
                JOIN user_achievements ua ON a.achievement_id = ua.achievement_id
                WHERE ua.user_id = ? ORDER BY ua.unlocked_at DESC
            ''', (user_id,))
            achievements = [dict(row) for row in cursor.fetchall()]
            conn.close()
            return achievements
        except:
            return []
    
    # ==================== Cleanup ====================
    
    def cleanup_inactive_users(self, days: int = 7) -> int:
        """حذف المستخدمين غير النشطين"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cutoff = datetime.now() - timedelta(days=days)
            cursor.execute('DELETE FROM users WHERE last_activity < ?', (cutoff,))
            deleted = cursor.rowcount
            conn.close()
            return deleted
        except:
            return 0
    
    def cleanup_old_sessions(self, days: int = 30) -> int:
        """حذف جلسات الألعاب القديمة"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cutoff = datetime.now() - timedelta(days=days)
            cursor.execute('DELETE FROM game_sessions WHERE played_at < ?', (cutoff,))
            deleted = cursor.rowcount
            conn.close()
            return deleted
        except:
            return 0
    
    def backup_database(self, backup_path: str) -> bool:
        """نسخ احتياطي"""
        try:
            import shutil
            shutil.copy2(self.db_path, backup_path)
            return True
        except:
            return False
    
    def get_stats_summary(self) -> Dict:
        """ملخص الإحصائيات"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT COUNT(*) as total FROM users')
            total_users = cursor.fetchone()['total']
            
            cursor.execute('SELECT COUNT(*) as registered FROM users WHERE is_registered = 1')
            registered_users = cursor.fetchone()['registered']
            
            cursor.execute('SELECT SUM(points) as total_points FROM users')
            total_points = cursor.fetchone()['total_points'] or 0
            
            conn.close()
            
            return {
                'total_users': total_users,
                'registered_users': registered_users,
                'total_points': total_points
            }
        except:
            return {
                'total_users': 0,
                'registered_users': 0,
                'total_points': 0
            }


# ==================== Singleton Instance ====================

_db_instance = None

def get_database() -> Database:
    """الحصول على instance واحد من قاعدة البيانات"""
    global _db_instance
    if _db_instance is None:
        _db_instance = Database()
    return _db_instance
