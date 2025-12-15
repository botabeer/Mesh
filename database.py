import sqlite3
import logging
from threading import Lock
from datetime import datetime, timedelta
from contextlib import contextmanager
from typing import Optional, List, Dict
from config import Config

logger = logging.getLogger(__name__)

class Database:
    _lock = Lock()
    _cache_lock = Lock()
    _leaderboard_cache: Optional[List[tuple]] = None
    _leaderboard_cache_time: float = 0
    CACHE_TTL = 300
    INACTIVITY_DAYS = 30

    @staticmethod
    @contextmanager
    def get_connection():
        conn = sqlite3.connect(Config.DATABASE_PATH, timeout=10, detect_types=sqlite3.PARSE_DECLTYPES)
        conn.row_factory = sqlite3.Row
        try:
            cursor = conn.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")
            cursor.execute("PRAGMA journal_mode = WAL")
            cursor.execute("PRAGMA synchronous = NORMAL")
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    @staticmethod
    def init():
        with Database.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id TEXT PRIMARY KEY,
                    display_name TEXT NOT NULL,
                    total_points INTEGER DEFAULT 0,
                    games_played INTEGER DEFAULT 0,
                    wins INTEGER DEFAULT 0,
                    theme TEXT DEFAULT 'light',
                    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS game_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    game_type TEXT NOT NULL,
                    points INTEGER DEFAULT 0,
                    won INTEGER DEFAULT 0,
                    played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
                )
            """)
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_score ON users(total_points DESC, wins DESC)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_history_user ON game_history(user_id, played_at DESC)")
        logger.info("Database initialized")

    @staticmethod
    def register_or_update_user(user_id: str, display_name: str) -> bool:
        with Database._lock:
            try:
                with Database.get_connection() as conn:
                    conn.execute("""
                        INSERT INTO users (user_id, display_name, last_activity)
                        VALUES (?, ?, CURRENT_TIMESTAMP)
                        ON CONFLICT(user_id) DO UPDATE SET
                            display_name = excluded.display_name,
                            last_activity = CURRENT_TIMESTAMP
                    """, (user_id, display_name))
                Database.clear_cache()
                return True
            except Exception as e:
                logger.error(f"Register error: {e}")
                return False

    @staticmethod
    def update_last_activity(user_id: str) -> None:
        try:
            with Database.get_connection() as conn:
                conn.execute("UPDATE users SET last_activity = CURRENT_TIMESTAMP WHERE user_id = ?", (user_id,))
        except Exception as e:
            logger.error(f"Activity update error: {e}")

    @staticmethod
    def get_user_theme(user_id: str) -> str:
        try:
            with Database.get_connection() as conn:
                row = conn.execute("SELECT theme FROM users WHERE user_id = ?", (user_id,)).fetchone()
                return row["theme"] if row else Config.DEFAULT_THEME
        except Exception:
            return Config.DEFAULT_THEME

    @staticmethod
    def toggle_user_theme(user_id: str) -> str:
        current = Database.get_user_theme(user_id)
        new_theme = "dark" if current == "light" else "light"
        with Database._lock:
            try:
                with Database.get_connection() as conn:
                    conn.execute("UPDATE users SET theme = ? WHERE user_id = ?", (new_theme, user_id))
                return new_theme
            except Exception:
                return current

    @staticmethod
    def update_user_points(user_id: str, points: int, won: bool, game_type: str) -> bool:
        with Database._lock:
            try:
                with Database.get_connection() as conn:
                    conn.execute("""
                        UPDATE users
                        SET total_points = total_points + ?,
                            games_played = games_played + 1,
                            wins = wins + ?,
                            last_activity = CURRENT_TIMESTAMP
                        WHERE user_id = ?
                    """, (points, int(won), user_id))
                    conn.execute("""
                        INSERT INTO game_history (user_id, game_type, points, won)
                        VALUES (?, ?, ?, ?)
                    """, (user_id, game_type, points, int(won)))
                Database.clear_cache()
                return True
            except Exception as e:
                logger.error(f"Points update error: {e}")
                return False

    @staticmethod
    def get_user_stats(user_id: str) -> Optional[Dict]:
        try:
            with Database.get_connection() as conn:
                row = conn.execute("""
                    SELECT display_name, total_points, games_played, wins, theme
                    FROM users WHERE user_id = ?
                """, (user_id,)).fetchone()
                return dict(row) if row else None
        except Exception:
            return None

    @staticmethod
    def get_leaderboard(limit: int = 20) -> List[tuple]:
        import time
        now = time.time()
        with Database._cache_lock:
            if Database._leaderboard_cache and now - Database._leaderboard_cache_time < Database.CACHE_TTL:
                return Database._leaderboard_cache[:limit]

        try:
            with Database.get_connection() as conn:
                rows = conn.execute("""
                    SELECT display_name, total_points
                    FROM users
                    WHERE games_played > 0
                    ORDER BY total_points DESC, wins DESC
                    LIMIT ?
                """, (limit,)).fetchall()
                result = [(r["display_name"], r["total_points"]) for r in rows]

            with Database._cache_lock:
                Database._leaderboard_cache = result
                Database._leaderboard_cache_time = now

            return result
        except Exception:
            return []

    @staticmethod
    def cleanup_inactive_users() -> int:
        cutoff = datetime.utcnow() - timedelta(days=Database.INACTIVITY_DAYS)
        with Database._lock:
            try:
                with Database.get_connection() as conn:
                    cur = conn.execute("DELETE FROM users WHERE last_activity < ?", (cutoff,))
                deleted = cur.rowcount or 0
                if deleted:
                    Database.clear_cache()
                    logger.info(f"Cleaned {deleted} inactive users")
                return deleted
            except Exception:
                return 0

    @staticmethod
    def clear_cache():
        with Database._cache_lock:
            Database._leaderboard_cache = None
            Database._leaderboard_cache_time = 0
