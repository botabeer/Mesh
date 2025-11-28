"""
Bot Mesh - Database v7.2 with Themes & Auto Name Update
Created by: Abeer Aldosari © 2025
"""

import sqlite3
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Tuple
from contextlib import contextmanager
import logging
import time
import threading

logger = logging.getLogger(__name__)


class Database:
    """Database management with themes support"""
    
    def __init__(self, db_path='botmesh.db'):
        self.db_path = db_path
        self._local = threading.local()
        self._ensure_clean_db()
        self.init_database()
    
    def _ensure_clean_db(self):
        """Ensure clean database"""
        if os.path.exists(self.db_path):
            try:
                conn = sqlite3.connect(self.db_path, timeout=5)
                conn.execute("SELECT 1")
                conn.close()
            except:
                try:
                    os.remove(self.db_path)
                    logger.warning("Removed locked database")
                except:
                    pass
    
    @contextmanager
    def get_connection(self):
        """Connection context manager"""
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
            yield conn
        except Exception as e:
            logger.error(f"Database error: {e}")
            if conn:
                conn.rollback()
            raise
        finally:
            if conn:
                conn.close()
    
    def init_database(self):
        """Initialize database with themes support"""
        for attempt in range(3):
            try:
                with self.get_connection() as conn:
                    cursor = conn.cursor()
                    
                    # Users table
                    cursor.execute('''
                        CREATE TABLE IF NOT EXISTS users (
                            user_id TEXT PRIMARY KEY,
                            name TEXT NOT NULL,
                            points INTEGER DEFAULT 0,
                            is_registered BOOLEAN DEFAULT 0,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )
                    ''')
                    
                    # User preferences (themes)
                    cursor.execute('''
                        CREATE TABLE IF NOT EXISTS user_preferences (
                            user_id TEXT PRIMARY KEY,
                            theme TEXT DEFAULT 'أبيض',
                            last_theme_change TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY (user_id) REFERENCES users(user_id)
                        )
                    ''')
                    
                    # Game sessions
                    cursor.execute('''
                        CREATE TABLE IF NOT EXISTS game_sessions (
                            session_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id TEXT NOT NULL,
                            game_name TEXT NOT NULL,
                            score INTEGER DEFAULT 0,
                            completed BOOLEAN DEFAULT 0,
                            played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY (user_id) REFERENCES users(user_id)
                        )
                    ''')
                    
                    # Game stats
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
                    
                    # Indexes
                    cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_points ON users(points DESC)')
                    cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_registered ON users(is_registered)')
                    cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_activity ON users(last_activity)')
                    cursor.execute('CREATE INDEX IF NOT EXISTS idx_prefs_theme ON user_preferences(theme)')
                    cursor.execute('CREATE INDEX IF NOT EXISTS idx_sessions_user ON game_sessions(user_id)')
                    
                    logger.info("Database initialized successfully")
                return
                
            except sqlite3.OperationalError as e:
                if attempt < 2:
                    logger.warning(f"DB init attempt {attempt + 1} failed, retrying...")
                    time.sleep(1)
                else:
                    logger.error(f"DB init failed: {e}")
                    raise
    
    # ==================== User Management ====================
    
    def get_user(self, user_id: str) -> Optional[Dict]:
        """Get user data"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
                row = cursor.fetchone()
                return dict(row) if row else None
        except Exception as e:
            logger.error(f"Error getting user: {e}")
            return None
    
    def create_user(self, user_id: str, name: str) -> bool:
        """Create new user"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR IGNORE INTO users (user_id, name, points, is_registered, last_activity)
                    VALUES (?, ?, 0, 0, ?)
                ''', (user_id, name, datetime.now()))
                
                # Create default theme preference
                cursor.execute('''
                    INSERT OR IGNORE INTO user_preferences (user_id, theme)
                    VALUES (?, 'أبيض')
                ''', (user_id,))
                return True
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            return False
    
    def update_user(self, user_id: str, **kwargs) -> bool:
        """Update user data"""
        if not kwargs:
            return False
        
        allowed_fields = {'name', 'points', 'is_registered'}
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
            logger.error(f"Error updating user: {e}")
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
                return True
        except Exception as e:
            logger.error(f"Error updating name: {e}")
            return False
    
    def add_points(self, user_id: str, points: int) -> bool:
        """Add points"""
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
            logger.error(f"Error adding points: {e}")
            return False
    
    def update_activity(self, user_id: str) -> bool:
        """Update last activity"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'UPDATE users SET last_activity = ? WHERE user_id = ?',
                    (datetime.now(), user_id)
                )
                return True
        except Exception as e:
            logger.error(f"Error updating activity: {e}")
            return False
    
    def get_leaderboard(self, limit: int = 10) -> List[Tuple[str, int]]:
        """Get leaderboard"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT name, points FROM users 
                    WHERE is_registered = 1 AND points > 0
                    ORDER BY points DESC, last_activity DESC 
                    LIMIT ?
                ''', (limit,))
                return [(row['name'], row['points']) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Error getting leaderboard: {e}")
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
            logger.error(f"Error getting theme: {e}")
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
                return True
        except Exception as e:
            logger.error(f"Error setting theme: {e}")
            return False
    
    # ==================== Game Sessions ====================
    
    def create_game_session(self, user_id: str, game_name: str) -> int:
        """Create game session"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO game_sessions (user_id, game_name, score, completed)
                    VALUES (?, ?, 0, 0)
                ''', (user_id, game_name))
                return cursor.lastrowid
        except Exception as e:
            logger.error(f"Error creating session: {e}")
            return 0
    
    def complete_game_session(self, session_id: int, score: int) -> bool:
        """Complete game session"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'UPDATE game_sessions SET score = ?, completed = 1 WHERE session_id = ?',
                    (score, session_id)
                )
                return True
        except Exception as e:
            logger.error(f"Error completing session: {e}")
            return False
    
    def get_user_game_stats(self, user_id: str) -> Dict[str, int]:
        """Get user game stats"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT game_name, COUNT(*) as plays
                    FROM game_sessions 
                    WHERE user_id = ? AND completed = 1
                    GROUP BY game_name
                    ORDER BY plays DESC
                ''', (user_id,))
                return {row['game_name']: row['plays'] for row in cursor.fetchall()}
        except Exception as e:
            logger.error(f"Error getting user stats: {e}")
            return {}
    
    # ==================== Game Statistics ====================
    
    def update_game_stats(self, game_name: str, completed: bool = False, points: int = 0):
        """Update game stats"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute('SELECT 1 FROM game_stats WHERE game_name = ?', (game_name,))
                exists = cursor.fetchone()
                
                if exists:
                    cursor.execute('''
                        UPDATE game_stats 
                        SET plays = plays + 1, 
                            completions = completions + ?,
                            total_points = total_points + ?, 
                            last_played = ?
                        WHERE game_name = ?
                    ''', (1 if completed else 0, points, datetime.now(), game_name))
                else:
                    cursor.execute('''
                        INSERT INTO game_stats (game_name, plays, completions, total_points, last_played)
                        VALUES (?, 1, ?, ?, ?)
                    ''', (game_name, 1 if completed else 0, points, datetime.now()))
        except Exception as e:
            logger.error(f"Error updating game stats: {e}")
    
    # ==================== Maintenance ====================
    
    def cleanup_inactive_users(self, days: int = 30) -> int:
        """Cleanup inactive users"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cutoff = datetime.now() - timedelta(days=days)
                cursor.execute(
                    'DELETE FROM users WHERE last_activity < ? AND is_registered = 0',
                    (cutoff,)
                )
                return cursor.rowcount
        except Exception as e:
            logger.error(f"Error cleaning users: {e}")
            return 0
    
    def get_stats_summary(self) -> Dict:
        """Get stats summary"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute('SELECT COUNT(*) as total FROM users')
                total_users = cursor.fetchone()['total']
                
                cursor.execute('SELECT COUNT(*) as registered FROM users WHERE is_registered = 1')
                registered_users = cursor.fetchone()['registered']
                
                cursor.execute('SELECT SUM(points) as total_points FROM users')
                total_points = cursor.fetchone()['total_points'] or 0
                
                return {
                    'total_users': total_users,
                    'registered_users': registered_users,
                    'total_points': total_points
                }
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            return {'total_users': 0, 'registered_users': 0, 'total_points': 0}


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
    return _db_instance
