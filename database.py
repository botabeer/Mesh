import sqlite3
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class Database:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # جدول المستخدمين
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    points INTEGER DEFAULT 0,
                    is_registered INTEGER DEFAULT 0,
                    theme TEXT DEFAULT 'فاتح',
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    last_active TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # جدول الجلسات
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    session_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    game_name TEXT NOT NULL,
                    points_earned INTEGER DEFAULT 0,
                    completed INTEGER DEFAULT 0,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            """)

            # جدول الإحصائيات
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS game_stats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    game_name TEXT NOT NULL,
                    plays INTEGER DEFAULT 0,
                    total_points INTEGER DEFAULT 0,
                    last_played TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            """)

            # إنشاء الفهارس
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_points ON users(points DESC)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_registered ON users(is_registered)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_sessions_user ON sessions(user_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_stats_user_game ON game_stats(user_id, game_name)")

            conn.commit()
            conn.close()
            logger.info("Database initialized successfully")
        except Exception as e:
            logger.error(f"Database initialization error: {e}")

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def get_user(self, user_id: str) -> Optional[Dict]:
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return dict(row)
            return None
        except Exception as e:
            logger.error(f"Get user error: {e}")
            return None

    def create_user(self, user_id: str, name: str):
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT OR IGNORE INTO users (user_id, name) VALUES (?, ?)",
                (user_id, name)
            )
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Create user error: {e}")

    def update_user(self, user_id: str, **kwargs):
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            updates = []
            values = []
            
            for key, value in kwargs.items():
                if key in ['name', 'points', 'is_registered', 'theme']:
                    updates.append(f"{key} = ?")
                    values.append(value)
            
            if updates:
                updates.append("last_active = ?")
                values.append(datetime.utcnow().isoformat())
                values.append(user_id)
                
                query = f"UPDATE users SET {', '.join(updates)} WHERE user_id = ?"
                cursor.execute(query, values)
                conn.commit()
            
            conn.close()
        except Exception as e:
            logger.error(f"Update user error: {e}")

    def add_points(self, user_id: str, points: int):
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET points = points + ?, last_active = ? WHERE user_id = ?",
                (points, datetime.utcnow().isoformat(), user_id)
            )
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Add points error: {e}")

    def set_user_theme(self, user_id: str, theme: str):
        self.update_user(user_id, theme=theme)

    def get_leaderboard(self, limit: int = 20) -> List[tuple]:
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT name, points, is_registered 
                FROM users 
                WHERE is_registered = 1
                ORDER BY points DESC 
                LIMIT ?
            """, (limit,))
            rows = cursor.fetchall()
            conn.close()
            return [(row['name'], row['points'], row['is_registered']) for row in rows]
        except Exception as e:
            logger.error(f"Get leaderboard error: {e}")
            return []

    def create_session(self, user_id: str, game_name: str) -> int:
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO sessions (user_id, game_name) VALUES (?, ?)",
                (user_id, game_name)
            )
            session_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return session_id
        except Exception as e:
            logger.error(f"Create session error: {e}")
            return 0

    def complete_session(self, session_id: int, points: int):
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE sessions SET points_earned = ?, completed = 1 WHERE session_id = ?",
                (points, session_id)
            )
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Complete session error: {e}")

    def record_game_stat(self, user_id: str, game_name: str, points: int, won: bool):
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO game_stats (user_id, game_name, plays, total_points, last_played)
                VALUES (?, ?, 1, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    plays = plays + 1,
                    total_points = total_points + ?,
                    last_played = ?
            """, (user_id, game_name, points, datetime.utcnow().isoformat(), points, datetime.utcnow().isoformat()))
            
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Record game stat error: {e}")

    def get_user_stats(self, user_id: str) -> Optional[Dict]:
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT game_name, plays, total_points
                FROM game_stats
                WHERE user_id = ?
                ORDER BY plays DESC
                LIMIT 5
            """, (user_id,))
            rows = cursor.fetchall()
            conn.close()
            
            if rows:
                return {
                    row['game_name']: {
                        'plays': row['plays'],
                        'total_points': row['total_points']
                    }
                    for row in rows
                }
            return None
        except Exception as e:
            logger.error(f"Get user stats error: {e}")
            return None

    def get_stats(self) -> Dict:
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) as total FROM users")
            total_users = cursor.fetchone()['total']
            
            cursor.execute("SELECT COUNT(*) as total FROM users WHERE is_registered = 1")
            registered_users = cursor.fetchone()['total']
            
            today = datetime.utcnow().date().isoformat()
            cursor.execute(
                "SELECT COUNT(*) as total FROM users WHERE DATE(last_active) = ?",
                (today,)
            )
            active_today = cursor.fetchone()['total']
            
            conn.close()
            
            return {
                'total_users': total_users,
                'registered_users': registered_users,
                'active_today': active_today
            }
        except Exception as e:
            logger.error(f"Get stats error: {e}")
            return {'total_users': 0, 'registered_users': 0, 'active_today': 0}

    def get_database_size(self) -> int:
        try:
            import os
            return os.path.getsize(self.db_path)
        except:
            return 0
