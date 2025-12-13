import sqlite3
import logging
from datetime import datetime
from typing import Dict, List, Optional
from contextlib import contextmanager

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Database:
    """Fully integrated SQLite database handler with bot-friendly interface."""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.init_db()

    @contextmanager
    def _get_connection(self):
        """Context manager for SQLite connection with commit/rollback."""
        conn = sqlite3.connect(
            self.db_path,
            timeout=10,
            detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
        )
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

    # ------------------- Initialization -------------------

    def init_db(self):
        """Initialize tables and indexes."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
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
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_points ON users(points DESC)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_registered ON users(is_registered)")
                logger.info("Database initialized successfully.")
        except Exception as e:
            logger.error(f"Database initialization error: {e}")

    # ------------------- Core User Operations -------------------

    def get_user(self, user_id: str) -> Optional[Dict]:
        """Retrieve a user by ID."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
                row = cursor.fetchone()
                return dict(row) if row else None
        except Exception as e:
            logger.error(f"Get user error: {e}")
            return None

    def create_user(self, user_id: str, name: str, is_registered: int = 0):
        """Create a new user, ignoring if already exists."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR IGNORE INTO users (user_id, name, is_registered)
                    VALUES (?, ?, ?)
                """, (user_id, name, is_registered))
                logger.info(f"User created: {name} ({user_id})")
        except Exception as e:
            logger.error(f"Create user error: {e}")

    def update_user(self, user_id: str, **kwargs):
        """Update user dynamically, including last_active timestamp."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                updates = []
                values = []

                for key, value in kwargs.items():
                    if key in ['name', 'points', 'temp_points', 'is_registered', 'theme']:
                        updates.append(f"{key} = ?")
                        values.append(value)

                if updates:
                    updates.append("last_active = ?")
                    values.append(datetime.utcnow().isoformat())
                    query = f"UPDATE users SET {', '.join(updates)} WHERE user_id = ?"
                    values.append(user_id)
                    cursor.execute(query, values)
                    logger.info(f"User {user_id} updated with {kwargs}")
        except Exception as e:
            logger.error(f"Update user error: {e}")

    def delete_user(self, user_id: str):
        """Delete a user by ID."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
                logger.info(f"User {user_id} deleted.")
        except Exception as e:
            logger.error(f"Delete user error: {e}")

    # ------------------- Points Management -------------------

    def add_points(self, user_id: str, points: int, name: str = "Unknown", temp: bool = False):
        """
        Add points to a user.
        Automatically creates the user if not exists.
        Can add temporary points if temp=True.
        """
        try:
            user = self.get_user(user_id)
            if not user:
                # Create user if missing
                self.create_user(user_id, name, is_registered=1)
            else:
                # Update name if different
                if name != "Unknown" and user.get("name") != name:
                    self.update_user(user_id, name=name)

            field = "temp_points" if temp else "points"

            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(f"""
                    UPDATE users
                    SET {field} = {field} + ?, last_active = ?
                    WHERE user_id = ?
                """, (points, datetime.utcnow().isoformat(), user_id))
                point_type = "temporary" if temp else "regular"
                logger.info(f"Added {points} {point_type} points to user {user_id}")
        except Exception as e:
            logger.error(f"Add points error: {e}")

    def reset_temp_points(self):
        """Reset temporary points for all users."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE users SET temp_points = 0")
                logger.info("Temporary points reset for all users.")
        except Exception as e:
            logger.error(f"Reset temp points error: {e}")

    # ------------------- Leaderboard -------------------

    def get_leaderboard(self, limit: int = 20, include_temp: bool = False) -> List[tuple]:
        """
        Return top registered users ordered by points.
        include_temp=True includes temporary points in the total score.
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                if include_temp:
                    cursor.execute(f"""
                        SELECT name, points + temp_points AS total_points
                        FROM users
                        WHERE is_registered = 1
                        ORDER BY total_points DESC
                        LIMIT ?
                    """, (limit,))
                    return [(row['name'], row['total_points']) for row in cursor.fetchall()]
                else:
                    cursor.execute("""
                        SELECT name, points
                        FROM users
                        WHERE is_registered = 1
                        ORDER BY points DESC
                        LIMIT ?
                    """, (limit,))
                    return [(row['name'], row['points']) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Get leaderboard error: {e}")
            return []

    # ------------------- Bot-Friendly Wrappers -------------------

    def add_points_for_user(self, user_id: str, points: int, name: str = "Unknown"):
        """Wrapper for bots: add regular points."""
        self.add_points(user_id, points, name=name, temp=False)

    def add_temp_points_for_user(self, user_id: str, points: int, name: str = "Unknown"):
        """Wrapper for bots: add temporary points."""
        self.add_points(user_id, points, name=name, temp=True)

    def get_leaderboard_for_bot(self, limit: int = 20, include_temp: bool = False) -> str:
        """Return leaderboard formatted as a string ready for sending in chat."""
        board = self.get_leaderboard(limit=limit, include_temp=include_temp)
        if not board:
            return "Leaderboard is empty."
        lines = [f"{i+1}. {name} - {pts} points" for i, (name, pts) in enumerate(board)]
        return "\n".join(lines)
