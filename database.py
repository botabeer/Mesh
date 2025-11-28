"""
Bot Mesh - Database Management System
Created by: Abeer Aldosari © 2025

Features:
- SQLite database for persistent storage
- User management with points and themes
- Game sessions tracking
- Statistics and leaderboard
- Auto cleanup for inactive users
- FIXED: Database locking issues with multiple workers
"""

import sqlite3
import json
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Tuple
import logging
import threading

logger = logging.getLogger(__name__)


class Database:
    """نظام إدارة قاعدة البيانات"""
    
    def __init__(self, db_path='botmesh.db'):
        self.db_path = db_path
        self.local = threading.local()
        self.init_database()
    
    def get_connection(self):
        """إنشاء اتصال بقاعدة البيانات مع timeout وتحسينات"""
        if not hasattr(self.local, 'conn') or self.local.conn is None:
            self.local.conn = sqlite3.connect(
                self.db_path,
                timeout=30.0,  # انتظار 30 ثانية قبل الفشل
                check_same_thread=False
            )
            self.local.conn.row_factory = sqlite3.Row
            # تفعيل WAL mode لتحسين الأداء
            self.local.conn.execute('PRAGMA journal_mode=WAL')
            self.local.conn.execute('PRAGMA busy_timeout=30000')
        return self.local.conn
    
    def init_database(self):
        """إنشاء جداول قاعدة البيانات"""
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
                played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
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
                PRIMARY KEY (user_id, achievement_id),
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                FOREIGN KEY (achievement_id) REFERENCES achievements(achievement_id) ON DELETE CASCADE
            )
        ''')
        
        # إنشاء indexes للأداء
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_points ON users(points DESC)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_activity ON users(last_activity)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_sessions_user ON game_sessions(user_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_sessions_game ON game_sessions(game_name)')
        
        conn.commit()
        
        logger.info("✅ Database initialized successfully")
    
    # ==================== User Management ====================
    
    def get_user(self, user_id: str) -> Optional[Dict]:
        """الحصول على بيانات مستخدم"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        row = cursor.fetchone()
        
        if row:
            return dict(row)
        return None
    
    def create_user(self, user_id: str, name: str) -> bool:
        """إنشاء مستخدم جديد"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO users (user_id, name, points, is_registered, theme, last_activity)
                VALUES (?, ?, 0, 0, 'أبيض', ?)
            ''', (user_id, name, datetime.now()))
            
            conn.commit()
            
            logger.info(f"✅ User created: {name} ({user_id})")
            return True
        except sqlite3.IntegrityError:
            logger.warning(f"⚠️ User already exists: {user_id}")
            return False
    
    def update_user(self, user_id: str, **kwargs) -> bool:
        """تحديث بيانات مستخدم"""
        if not kwargs:
            return False
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # بناء استعلام التحديث ديناميكياً
        fields = []
        values = []
        for key, value in kwargs.items():
            if key in ['name', 'points', 'is_registered', 'theme']:
                fields.append(f"{key} = ?")
                values.append(value)
        
        if not fields:
            return False
        
        # إضافة تحديث last_activity
        fields.append("last_activity = ?")
        values.append(datetime.now())
        values.append(user_id)
        
        query = f"UPDATE users SET {', '.join(fields)} WHERE user_id = ?"
        cursor.execute(query, values)
        
        conn.commit()
        return True
    
    def add_points(self, user_id: str, points: int) -> bool:
        """إضافة نقاط لمستخدم"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE users 
            SET points = points + ?, last_activity = ?
            WHERE user_id = ?
        ''', (points, datetime.now(), user_id))
        
        conn.commit()
        return True
    
    def update_activity(self, user_id: str) -> bool:
        """تحديث آخر نشاط"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE users 
            SET last_activity = ?
            WHERE user_id = ?
        ''', (datetime.now(), user_id))
        
        conn.commit()
        return True
    
    def get_leaderboard(self, limit: int = 10) -> List[Tuple[str, int]]:
        """الحصول على لوحة الصدارة"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT name, points 
            FROM users 
            WHERE is_registered = 1 
            ORDER BY points DESC 
            LIMIT ?
        ''', (limit,))
        
        leaderboard = cursor.fetchall()
        
        return [(row['name'], row['points']) for row in leaderboard]
    
    def get_user_rank(self, user_id: str) -> Optional[int]:
        """الحصول على ترتيب المستخدم"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT COUNT(*) + 1 as rank
            FROM users 
            WHERE is_registered = 1 
            AND points > (SELECT points FROM users WHERE user_id = ?)
        ''', (user_id,))
        
        row = cursor.fetchone()
        
        return row['rank'] if row else None
    
    # ==================== Game Sessions ====================
    
    def create_game_session(self, user_id: str, game_name: str) -> int:
        """إنشاء جلسة لعبة جديدة"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO game_sessions (user_id, game_name, score, completed)
            VALUES (?, ?, 0, 0)
        ''', (user_id, game_name))
        
        session_id = cursor.lastrowid
        conn.commit()
        
        return session_id
    
    def complete_game_session(self, session_id: int, score: int) -> bool:
        """إكمال جلسة لعبة"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE game_sessions 
            SET score = ?, completed = 1
            WHERE session_id = ?
        ''', (score, session_id))
        
        conn.commit()
        return True
    
    def get_user_game_stats(self, user_id: str) -> Dict[str, int]:
        """إحصائيات ألعاب المستخدم"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT game_name, COUNT(*) as plays
            FROM game_sessions
            WHERE user_id = ?
            GROUP BY game_name
        ''', (user_id,))
        
        stats = {row['game_name']: row['plays'] for row in cursor.fetchall()}
        
        return stats
    
    # ==================== Game Statistics ====================
    
    def update_game_stats(self, game_name: str, completed: bool = False, points: int = 0):
        """تحديث إحصائيات لعبة"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # التحقق من وجود اللعبة
        cursor.execute('SELECT * FROM game_stats WHERE game_name = ?', (game_name,))
        exists = cursor.fetchone()
        
        if exists:
            # تحديث
            cursor.execute('''
                UPDATE game_stats 
                SET plays = plays + 1,
                    completions = completions + ?,
                    total_points = total_points + ?,
                    last_played = ?
                WHERE game_name = ?
            ''', (1 if completed else 0, points, datetime.now(), game_name))
            
            # حساب المتوسط
            if completed:
                cursor.execute('''
                    UPDATE game_stats 
                    SET avg_score = CAST(total_points AS REAL) / NULLIF(completions, 0)
                    WHERE game_name = ?
                ''', (game_name,))
        else:
            # إنشاء
            cursor.execute('''
                INSERT INTO game_stats (game_name, plays, completions, total_points, avg_score, last_played)
                VALUES (?, 1, ?, ?, ?, ?)
            ''', (game_name, 1 if completed else 0, points, 
                  float(points) if completed else 0.0, datetime.now()))
        
        conn.commit()
    
    def get_game_stats(self, game_name: str) -> Optional[Dict]:
        """الحصول على إحصائيات لعبة"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM game_stats WHERE game_name = ?', (game_name,))
        row = cursor.fetchone()
        
        return dict(row) if row else None
    
    def get_all_game_stats(self) -> Dict[str, Dict]:
        """الحصول على إحصائيات جميع الألعاب"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM game_stats')
        rows = cursor.fetchall()
        
        return {row['game_name']: dict(row) for row in rows}
    
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
            
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def unlock_achievement(self, user_id: str, achievement_id: str) -> bool:
        """فتح إنجاز للمستخدم"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # التحقق من عدم فتحه مسبقاً
            cursor.execute('''
                SELECT 1 FROM user_achievements 
                WHERE user_id = ? AND achievement_id = ?
            ''', (user_id, achievement_id))
            
            if cursor.fetchone():
                return False
            
            # فتح الإنجاز
            cursor.execute('''
                INSERT INTO user_achievements (user_id, achievement_id)
                VALUES (?, ?)
            ''', (user_id, achievement_id))
            
            # إضافة نقاط المكافأة
            cursor.execute('''
                UPDATE users 
                SET points = points + (
                    SELECT points_reward FROM achievements WHERE achievement_id = ?
                )
                WHERE user_id = ?
            ''', (achievement_id, user_id))
            
            conn.commit()
            return True
        except:
            return False
    
    def get_user_achievements(self, user_id: str) -> List[Dict]:
        """الحصول على إنجازات المستخدم"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT a.*, ua.unlocked_at
            FROM achievements a
            JOIN user_achievements ua ON a.achievement_id = ua.achievement_id
            WHERE ua.user_id = ?
            ORDER BY ua.unlocked_at DESC
        ''', (user_id,))
        
        achievements = [dict(row) for row in cursor.fetchall()]
        
        return achievements
    
    # ==================== Cleanup ====================
    
    def cleanup_inactive_users(self, days: int = 7) -> int:
        """حذف المستخدمين غير النشطين"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cutoff = datetime.now() - timedelta(days=days)
        
        cursor.execute('''
            DELETE FROM users 
            WHERE last_activity < ?
        ''', (cutoff,))
        
        deleted = cursor.rowcount
        conn.commit()
        
        logger.info(f"🧹 Cleaned up {deleted} inactive users")
        return deleted
    
    def cleanup_old_sessions(self, days: int = 30) -> int:
        """حذف جلسات الألعاب القديمة"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cutoff = datetime.now() - timedelta(days=days)
        
        cursor.execute('''
            DELETE FROM game_sessions 
            WHERE played_at < ?
        ''', (cutoff,))
        
        deleted = cursor.rowcount
        conn.commit()
        
        logger.info(f"🧹 Cleaned up {deleted} old game sessions")
        return deleted
    
    # ==================== Backup & Restore ====================
    
    def backup_database(self, backup_path: str) -> bool:
        """نسخ احتياطي لقاعدة البيانات"""
        try:
            import shutil
            shutil.copy2(self.db_path, backup_path)
            logger.info(f"✅ Database backed up to {backup_path}")
            return True
        except Exception as e:
            logger.error(f"❌ Backup failed: {e}")
            return False
    
    def get_stats_summary(self) -> Dict:
        """ملخص إحصائيات قاعدة البيانات"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) as total FROM users')
        total_users = cursor.fetchone()['total']
        
        cursor.execute('SELECT COUNT(*) as registered FROM users WHERE is_registered = 1')
        registered_users = cursor.fetchone()['registered']
        
        cursor.execute('SELECT COUNT(*) as total FROM game_sessions')
        total_sessions = cursor.fetchone()['total']
        
        cursor.execute('SELECT COUNT(*) as completed FROM game_sessions WHERE completed = 1')
        completed_sessions = cursor.fetchone()['completed']
        
        cursor.execute('SELECT SUM(points) as total_points FROM users')
        total_points = cursor.fetchone()['total_points'] or 0
        
        return {
            'total_users': total_users,
            'registered_users': registered_users,
            'total_sessions': total_sessions,
            'completed_sessions': completed_sessions,
            'total_points': total_points
        }


# ==================== Singleton Instance ====================

_db_instance = None

def get_database() -> Database:
    """الحصول على instance واحد من قاعدة البيانات"""
    global _db_instance
    if _db_instance is None:
        _db_instance = Database()
    return _db_instance
