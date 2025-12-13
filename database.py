import sqlite3
import logging
from datetime import datetime
from typing import Dict, List, Optional
from contextlib import contextmanager

logger = logging.getLogger(__name__)

class Database:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.init_db()

    @contextmanager
    def _get_connection(self):
        conn = sqlite3.connect(self.db_path, timeout=10, detect_types=sqlite3.PARSE_DECLTYPES)
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

    def init_db(self):
        try:
            with self._get_connection() as conn:
                c = conn.cursor()
                c.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        user_id TEXT PRIMARY KEY,
                        name TEXT NOT NULL,
                        points INTEGER DEFAULT 0,
                        temp_points INTEGER DEFAULT 0,
                        is_registered INTEGER DEFAULT 0,
                        theme TEXT DEFAULT 'light',
                        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                        last_active TEXT DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                c.execute("CREATE INDEX IF NOT EXISTS idx_users_points ON users(points DESC)")
                c.execute("CREATE INDEX IF NOT EXISTS idx_users_registered ON users(is_registered)")
                logger.info("Database initialized")
        except Exception as e:
            logger.error(f"Init error: {e}")

    def get_user(self, user_id: str) -> Optional[Dict]:
        try:
            with self._get_connection() as conn:
                c = conn.cursor()
                c.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
                row = c.fetchone()
                return dict(row) if row else None
        except Exception as e:
            logger.error(f"Get user error: {e}")
            return None

    def create_user(self, user_id: str, name: str, is_registered: int = 0):
        try:
            with self._get_connection() as conn:
                c = conn.cursor()
                c.execute("INSERT OR IGNORE INTO users (user_id, name, is_registered) VALUES (?, ?, ?)",
                         (user_id, name, is_registered))
                logger.info(f"User created: {name}")
        except Exception as e:
            logger.error(f"Create user error: {e}")

    def update_user(self, user_id: str, **kwargs):
        try:
            with self._get_connection() as conn:
                c = conn.cursor()
                updates, values = [], []
                for key, value in kwargs.items():
                    if key in ['name', 'points', 'temp_points', 'is_registered', 'theme']:
                        updates.append(f"{key} = ?")
                        values.append(value)
                if updates:
                    updates.append("last_active = ?")
                    values.append(datetime.utcnow().isoformat())
                    query = f"UPDATE users SET {', '.join(updates)} WHERE user_id = ?"
                    values.append(user_id)
                    c.execute(query, values)
        except Exception as e:
            logger.error(f"Update user error: {e}")

    def add_points(self, user_id: str, points: int, name: str = "Unknown", temp: bool = False):
        try:
            user = self.get_user(user_id)
            if not user:
                self.create_user(user_id, name, is_registered=1)
            elif name != "Unknown" and user.get("name") != name:
                self.update_user(user_id, name=name)

            field = "temp_points" if temp else "points"
            with self._get_connection() as conn:
                c = conn.cursor()
                c.execute(f"UPDATE users SET {field} = {field} + ?, last_active = ? WHERE user_id = ?",
                         (points, datetime.utcnow().isoformat(), user_id))
        except Exception as e:
            logger.error(f"Add points error: {e}")

    def reset_temp_points(self):
        try:
            with self._get_connection() as conn:
                c = conn.cursor()
                c.execute("UPDATE users SET temp_points = 0")
        except Exception as e:
            logger.error(f"Reset temp points error: {e}")

    def get_leaderboard(self, limit: int = 20, include_temp: bool = False) -> List[tuple]:
        try:
            with self._get_connection() as conn:
                c = conn.cursor()
                if include_temp:
                    c.execute("""SELECT name, points + temp_points AS total 
                                FROM users WHERE is_registered = 1 
                                ORDER BY total DESC LIMIT ?""", (limit,))
                    return [(r['name'], r['total']) for r in c.fetchall()]
                else:
                    c.execute("""SELECT name, points FROM users 
                                WHERE is_registered = 1 
                                ORDER BY points DESC LIMIT ?""", (limit,))
                    return [(r['name'], r['points']) for r in c.fetchall()]
        except Exception as e:
            logger.error(f"Leaderboard error: {e}")
            return []
