"""
Bot Mesh - Database v11.2 FINAL
Created by: Abeer Aldosari © 2025
✅ تتبع الاتصال في الوقت الفعلي
✅ حذف تلقائي بعد شهر من عدم النشاط
✅ تحديث تلقائي للأسماء من LINE
✅ نظام خصوصية محسّن
"""

import sqlite3
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Tuple, Any
from contextlib import contextmanager
import logging
import time
import threading

logger = logging.getLogger(__name__)


class Database:
    """Database management with enhanced privacy features"""
    
    def __init__(self, db_path='botmesh.db'):
        self.db_path = db_path
        self._local = threading.local()
        self._ensure_clean_db()
        self.init_database()
        logger.info(f"✅ Database initialized: {db_path}")
    
    def _ensure_clean_db(self):
        """Ensure database is accessible and clean"""
        if os.path.exists(self.db_path):
            try:
                conn = sqlite3.connect(self.db_path, timeout=5)
                conn.execute("SELECT 1")
                conn.close()
            except sqlite3.OperationalError:
                try:
                    os.remove(self.db_path)
                    logger.warning("⚠️ Removed locked database")
                except Exception as e:
                    logger.error(f"❌ Failed to remove locked database: {e}")
    
    @contextmanager
    def get_connection(self):
        """Thread-safe connection context manager"""
        conn = None
        try:
            conn = sqlite3.connect(
                self.db_path,
                timeout=60.0,
                isolation_level=None,
                check_same_thread=False
            )
            conn.row_factory = sqlite3.Row
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("PRAGMA synchronous=NORMAL")
            conn.execute("PRAGMA foreign_keys=ON")
            yield conn
        except Exception as e:
            logger.error(f"❌ Database error: {e}")
            if conn:
                try:
                    conn.rollback()
                except:
                    pass
            raise
        finally:
            if conn:
                try:
                    conn.close()
                except:
                    pass
    
    def init_database(self):
        """Initialize all database tables"""
        for attempt in range(3):
            try:
                with self.get_connection() as conn:
                    cursor = conn.cursor()
                    
                    # Users table - مع تتبع الاتصال
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
                        )
                    ''')
                    
                    # User preferences (themes)
                    cursor.execute('''
                        CREATE TABLE IF NOT EXISTS user_preferences (
                            user_id TEXT PRIMARY KEY,
                            theme TEXT DEFAULT 'أبيض',
                            language TEXT DEFAULT 'ar',
                            notifications BOOLEAN DEFAULT 1,
                            last_theme_change TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
                        )
                    ''')
                    
                    # Game sessions (enhanced)
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
                            FOREIGN KEY (session_id) REFERENCES game_sessions(session_id) ON DELETE CASCADE
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
                        )
                    ''')
                    
                    # Activity logs
                    cursor.execute('''
                        CREATE TABLE IF NOT EXISTS activity_logs (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id TEXT NOT NULL,
                            action TEXT NOT NULL,
                            details TEXT,
                            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY (user_id) REFERENCES users(user_id)
                        )
                    ''')
                    
                    # Indexes for performance
                    cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_points ON users(points DESC)')
                    cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_registered ON users(is_registered)')
                    cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_activity ON users(last_activity)')
                    cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_online ON users(is_online)')
                    cursor.execute('CREATE INDEX IF NOT EXISTS idx_prefs_theme ON user_preferences(theme)')
                    cursor.execute('CREATE INDEX IF NOT EXISTS idx_sessions_owner ON game_sessions(owner_id)')
                    cursor.execute('CREATE INDEX IF NOT EXISTS idx_sessions_game ON game_sessions(game_name)')
                    cursor.execute('CREATE INDEX IF NOT EXISTS idx_team_members_session ON team_members(session_id)')
                    cursor.execute('CREATE INDEX IF NOT EXISTS idx_game_stats_user ON game_stats(user_id)')
                    cursor.execute('CREATE INDEX IF NOT EXISTS idx_logs_user ON activity_logs(user_id)')
                    
                    logger.info("✅ Database tables initialized successfully")
                return
                
            except sqlite3.OperationalError as e:
                if attempt < 2:
                    logger.warning(f"⚠️ DB init attempt {attempt + 1} failed, retrying...")
                    time.sleep(1)
                else:
                    logger.error(f"❌ DB init failed after 3 attempts: {e}")
                    raise
    
    # ==================== User Management ====================
    
    def get_user(self, user_id: str) -> Optional[Dict]:
        """Get user with preferences"""
        try:
            with self.get_connection() as conn:
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
        except Exception as e:
            logger.error(f"❌ Error getting user: {e}")
            return None
    
    def create_user(self, user_id: str, name: str) -> bool:
        """Create new user with default preferences"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                now = datetime.now()
                
                # Insert user
                cursor.execute('''
                    INSERT OR IGNORE INTO users (user_id, name, points, is_registered, is_online, last_online, last_activity)
                    VALUES (?, ?, 0, 0, 1, ?, ?)
                ''', (user_id, name, now, now))
                
                # Insert default preferences
                cursor.execute('''
                    INSERT OR IGNORE INTO user_preferences (user_id, theme)
                    VALUES (?, 'أبيض')
                ''', (user_id,))
                
                logger.info(f"✅ Created user: {user_id} ({name})")
                return True
        except Exception as e:
            logger.error(f"❌ Error creating user: {e}")
            return False
    
    def update_user(self, user_id: str, **kwargs) -> bool:
        """Update user data"""
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
        
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                fields.append("last_activity = ?")
                values.extend([datetime.now(), user_id])
                
                query = f"UPDATE users SET {', '.join(fields)} WHERE user_id = ?"
                cursor.execute(query, values)
                return True
        except Exception as e:
            logger.error(f"❌ Error updating user: {e}")
            return False
    
    def update_user_name(self, user_id: str, new_name: str) -> bool:
        """Update username (auto-sync from LINE)"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'UPDATE users SET name = ?, last_activity = ? WHERE user_id = ?',
                    (new_name, datetime.now(), user_id)
                )
                logger.info(f"✅ Updated name for {user_id}: {new_name}")
                return True
        except Exception as e:
            logger.error(f"❌ Error updating name: {e}")
            return False
    
    def set_user_online(self, user_id: str, is_online: bool = True) -> bool:
        """Set user online/offline status"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                now = datetime.now()
                cursor.execute(
                    'UPDATE users SET is_online = ?, last_online = ?, last_activity = ? WHERE user_id = ?',
                    (1 if is_online else 0, now, now, user_id)
                )
                return True
        except Exception as e:
            logger.error(f"❌ Error setting online status: {e}")
            return False
    
    def add_points(self, user_id: str, points: int) -> bool:
        """Add points to user"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE users 
                    SET points = points + ?, last_activity = ?
                    WHERE user_id = ?
                ''', (points, datetime.now(), user_id))
                return True
        except Exception as e:
            logger.error(f"❌ Error adding points: {e}")
            return False
    
    def update_activity(self, user_id: str) -> bool:
        """Update last activity timestamp and set online"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                now = datetime.now()
                cursor.execute(
                    'UPDATE users SET last_activity = ?, is_online = 1, last_online = ? WHERE user_id = ?',
                    (now, now, user_id)
                )
                return True
        except Exception as e:
            logger.error(f"❌ Error updating activity: {e}")
            return False
    
    def get_leaderboard(self, limit: int = 10) -> List[Tuple[str, int, bool]]:
        """Get leaderboard with online status"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT name, points, is_online FROM users 
                    WHERE is_registered = 1 AND points > 0
                    ORDER BY points DESC, last_activity DESC 
                    LIMIT ?
                ''', (limit,))
                return [(row['name'], row['points'], bool(row['is_online'])) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"❌ Error getting leaderboard: {e}")
            return []
    
    # ==================== Theme Management ====================
    
    def get_user_theme(self, user_id: str) -> str:
        """Get user's theme"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'SELECT theme FROM user_preferences WHERE user_id = ?',
                    (user_id,)
                )
                row = cursor.fetchone()
                return row['theme'] if row else 'أبيض'
        except Exception as e:
            logger.error(f"❌ Error getting theme: {e}")
            return 'أبيض'
    
    def set_user_theme(self, user_id: str, theme: str) -> bool:
        """Set user's theme"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO user_preferences (user_id, theme, last_theme_change)
                    VALUES (?, ?, ?)
                    ON CONFLICT(user_id) DO UPDATE SET
                        theme = excluded.theme,
                        last_theme_change = excluded.last_theme_change
                ''', (user_id, theme, datetime.now()))
                logger.info(f"✅ Theme updated: {user_id} -> {theme}")
                return True
        except Exception as e:
            logger.error(f"❌ Error setting theme: {e}")
            return False
    
    # ==================== Game Sessions ====================
    
    def create_game_session(self, owner_id: str, game_name: str, mode: str = 'solo', team_mode: int = 0) -> int:
        """Create game session"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO game_sessions (owner_id, game_name, mode, team_mode, started_at)
                    VALUES (?, ?, ?, ?, ?)
                ''', (owner_id, game_name, mode, team_mode, datetime.now()))
                session_id = cursor.lastrowid
                logger.info(f"✅ Session created: {session_id} ({game_name}, mode={mode})")
                return session_id
        except Exception as e:
            logger.error(f"❌ Error creating session: {e}")
            return 0
    
    def finish_session(self, session_id: int, score: int = 0) -> bool:
        """Mark session as completed"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'UPDATE game_sessions SET score = ?, completed = 1, completed_at = ? WHERE session_id = ?',
                    (score, datetime.now(), session_id)
                )
                logger.info(f"✅ Session finished: {session_id} (score={score})")
                return True
        except Exception as e:
            logger.error(f"❌ Error finishing session: {e}")
            return False
    
    # ==================== Team Management ====================
    
    def add_team_member(self, session_id: int, user_id: str, team_name: str) -> bool:
        """Add member to team"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO team_members (session_id, user_id, team_name)
                    VALUES (?, ?, ?)
                ''', (session_id, user_id, team_name))
                logger.info(f"✅ Team member added: {user_id} -> {team_name}")
                return True
        except Exception as e:
            logger.error(f"❌ Error adding team member: {e}")
            return False
    
    def add_team_points(self, session_id: int, team_name: str, points: int) -> bool:
        """Add points to team"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                # Check if team exists
                cursor.execute(
                    'SELECT id FROM team_scores WHERE session_id = ? AND team_name = ?',
                    (session_id, team_name)
                )
                
                if cursor.fetchone():
                    cursor.execute('''
                        UPDATE team_scores 
                        SET score = score + ?, updated_at = ?
                        WHERE session_id = ? AND team_name = ?
                    ''', (points, datetime.now(), session_id, team_name))
                else:
                    cursor.execute('''
                        INSERT INTO team_scores (session_id, team_name, score)
                        VALUES (?, ?, ?)
                    ''', (session_id, team_name, points))
                
                return True
        except Exception as e:
            logger.error(f"❌ Error adding team points: {e}")
            return False
    
    def get_team_points(self, session_id: int) -> Dict[str, int]:
        """Get team scores for session"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'SELECT team_name, score FROM team_scores WHERE session_id = ?',
                    (session_id,)
                )
                return {row['team_name']: row['score'] for row in cursor.fetchall()}
        except Exception as e:
            logger.error(f"❌ Error getting team points: {e}")
            return {}
    
    # ==================== Game Statistics ====================
    
    def record_game_stat(self, user_id: str, game_name: str, score: int, won: bool = False) -> bool:
        """Record game statistics"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Check if stat exists
                cursor.execute(
                    'SELECT plays, total_score, best_score FROM game_stats WHERE user_id = ? AND game_name = ?',
                    (user_id, game_name)
                )
                row = cursor.fetchone()
                
                if row:
                    plays = row['plays'] + 1
                    total_score = row['total_score'] + score
                    best_score = max(row['best_score'], score)
                    avg_score = total_score / plays
                    
                    cursor.execute('''
                        UPDATE game_stats 
                        SET plays = ?, wins = wins + ?, total_score = ?, best_score = ?, avg_score = ?, last_played = ?
                        WHERE user_id = ? AND game_name = ?
                    ''', (plays, 1 if won else 0, total_score, best_score, avg_score, datetime.now(), user_id, game_name))
                else:
                    cursor.execute('''
                        INSERT INTO game_stats (user_id, game_name, plays, wins, total_score, best_score, avg_score)
                        VALUES (?, ?, 1, ?, ?, ?, ?)
                    ''', (user_id, game_name, 1 if won else 0, score, score, float(score)))
                
                return True
        except Exception as e:
            logger.error(f"❌ Error recording game stat: {e}")
            return False
    
    def get_user_game_stats(self, user_id: str) -> Dict[str, Dict]:
        """Get user's game statistics"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT game_name, plays, wins, total_score, best_score, avg_score
                    FROM game_stats 
                    WHERE user_id = ?
                    ORDER BY plays DESC
                ''', (user_id,))
                
                stats = {}
                for row in cursor.fetchall():
                    stats[row['game_name']] = {
                        'plays': row['plays'],
                        'wins': row['wins'],
                        'total_score': row['total_score'],
                        'best_score': row['best_score'],
                        'avg_score': round(row['avg_score'], 1)
                    }
                return stats
        except Exception as e:
            logger.error(f"❌ Error getting user game stats: {e}")
            return {}
    
    # ==================== Activity Logs ====================
    
    def log_activity(self, user_id: str, action: str, details: Optional[str] = None) -> bool:
        """Log user activity"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'INSERT INTO activity_logs (user_id, action, details) VALUES (?, ?, ?)',
                    (user_id, action, details)
                )
                return True
        except Exception as e:
            logger.error(f"❌ Error logging activity: {e}")
            return False
    
    # ==================== Privacy & Maintenance ====================
    
    def cleanup_inactive_users(self, days: int = 30) -> int:
        """Cleanup inactive users (privacy feature)"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cutoff = datetime.now() - timedelta(days=days)
                
                # حذف المستخدمين غير النشطين (غير مسجلين أو لم يسجلوا دخول منذ شهر)
                cursor.execute('''
                    DELETE FROM users 
                    WHERE last_activity < ? AND (is_registered = 0 OR points = 0)
                ''', (cutoff,))
                deleted = cursor.rowcount
                
                if deleted > 0:
                    logger.info(f"✅ Cleaned {deleted} inactive users (privacy cleanup)")
                
                return deleted
        except Exception as e:
            logger.error(f"❌ Error cleaning users: {e}")
            return 0
    
    def set_all_offline(self) -> int:
        """Set all users offline (call on bot restart)"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('UPDATE users SET is_online = 0')
                count = cursor.rowcount
                logger.info(f"✅ Set {count} users offline")
                return count
        except Exception as e:
            logger.error(f"❌ Error setting offline: {e}")
            return 0
    
    def get_stats_summary(self) -> Dict:
        """Get database statistics summary"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute('SELECT COUNT(*) as total FROM users')
                total_users = cursor.fetchone()['total']
                
                cursor.execute('SELECT COUNT(*) as registered FROM users WHERE is_registered = 1')
                registered_users = cursor.fetchone()['registered']
                
                cursor.execute('SELECT COUNT(*) as online FROM users WHERE is_online = 1')
                online_users = cursor.fetchone()['online']
                
                cursor.execute('SELECT SUM(points) as total_points FROM users')
                total_points = cursor.fetchone()['total_points'] or 0
                
                cursor.execute('SELECT COUNT(*) as sessions FROM game_sessions')
                total_sessions = cursor.fetchone()['sessions']
                
                cursor.execute('SELECT COUNT(*) as completed FROM game_sessions WHERE completed = 1')
                completed_sessions = cursor.fetchone()['completed']
                
                return {
                    'total_users': total_users,
                    'registered_users': registered_users,
                    'online_users': online_users,
                    'total_points': total_points,
                    'total_sessions': total_sessions,
                    'completed_sessions': completed_sessions
                }
        except Exception as e:
            logger.error(f"❌ Error getting stats: {e}")
            return {
                'total_users': 0,
                'registered_users': 0,
                'online_users': 0,
                'total_points': 0,
                'total_sessions': 0,
                'completed_sessions': 0
            }


# ==================== Singleton ====================

_db_instance = None
_db_lock = threading.Lock()

def get_database() -> Database:
    """Get singleton database instance"""
    global _db_instance
    if _db_instance is None:
        with _db_lock:
            if _db_instance is None:
                _db_instance = Database()
                # Set all users offline on startup
                _db_instance.set_all_offline()
    return _db_instance


# ==================== Export ====================

__all__ = ['Database', 'get_database']
