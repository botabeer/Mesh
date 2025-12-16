import sqlite3
import logging
import time
from threading import Lock
from contextlib import contextmanager
from config import Config

logger = logging.getLogger(__name__)


class Database:
    def __init__(self):
        self._lock = Lock()
        self._waiting_names = {}
        self._game_progress = {}
        self._init_db()

    @contextmanager
    def _get_conn(self):
        conn = sqlite3.connect(
            Config.DB_PATH,
            timeout=10,
            check_same_thread=False
        )
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def _init_db(self):
        with self._lock, self._get_conn() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    points INTEGER DEFAULT 0,
                    games INTEGER DEFAULT 0,
                    wins INTEGER DEFAULT 0,
                    theme TEXT DEFAULT 'light',
                    last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_points ON users(points DESC, wins DESC)"
            )
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_active ON users(last_active DESC)"
            )

        logger.info("Database initialized")

    def get_user(self, user_id: str):
        try:
            with self._get_conn() as conn:
                row = conn.execute(
                    "SELECT * FROM users WHERE user_id=?",
                    (user_id,)
                ).fetchone()
                return dict(row) if row else None
        except Exception as e:
            logger.error(f"Get user error: {e}")
            return None

    def register_user(self, user_id: str, name: str) -> bool:
        name = name.strip()[:50]
        if len(name) < 2:
            return False

        with self._lock:
            try:
                with self._get_conn() as conn:
                    conn.execute("""
                        INSERT INTO users (user_id, name)
                        VALUES (?, ?)
                        ON CONFLICT(user_id) DO UPDATE SET
                            name=excluded.name,
                            last_active=CURRENT_TIMESTAMP
                    """, (user_id, name))
                return True
            except Exception as e:
                logger.error(f"Register error: {e}")
                return False

    def update_activity(self, user_id: str):
        try:
            with self._get_conn() as conn:
                conn.execute(
                    "UPDATE users SET last_active=CURRENT_TIMESTAMP WHERE user_id=?",
                    (user_id,)
                )
        except Exception:
            pass

    def add_points(self, user_id: str, points: int) -> bool:
        if points <= 0:
            return False

        with self._lock:
            try:
                with self._get_conn() as conn:
                    cur = conn.execute(
                        "UPDATE users SET points=points+?, last_active=CURRENT_TIMESTAMP WHERE user_id=?",
                        (points, user_id)
                    )
                return cur.rowcount > 0
            except Exception as e:
                logger.error(f"Add points error: {e}")
                return False

    def finish_game(self, user_id: str, won: bool) -> bool:
        with self._lock:
            try:
                with self._get_conn() as conn:
                    cur = conn.execute("""
                        UPDATE users
                        SET games = games + 1,
                            wins = wins + ?,
                            last_active = CURRENT_TIMESTAMP
                        WHERE user_id=?
                    """, (1 if won else 0, user_id))
                return cur.rowcount > 0
            except Exception as e:
                logger.error(f"Finish game error: {e}")
                return False

    def get_leaderboard(self, limit: int = 10):
        try:
            with self._get_conn() as conn:
                rows = conn.execute("""
                    SELECT name, points, wins, games
                    FROM users
                    WHERE games > 0
                    ORDER BY points DESC, wins DESC
                    LIMIT ?
                """, (limit,)).fetchall()

                return [
                    {
                        "name": r["name"],
                        "points": r["points"],
                        "wins": r["wins"],
                        "games": r["games"]
                    } for r in rows
                ]
        except Exception:
            return []

    def get_theme(self, user_id: str) -> str:
        try:
            with self._get_conn() as conn:
                row = conn.execute(
                    "SELECT theme FROM users WHERE user_id=?",
                    (user_id,)
                ).fetchone()
                return row["theme"] if row else "light"
        except Exception:
            return "light"

    def toggle_theme(self, user_id: str) -> str:
        current = self.get_theme(user_id)
        new = "dark" if current == "light" else "light"

        with self._lock:
            try:
                with self._get_conn() as conn:
                    conn.execute(
                        "UPDATE users SET theme=? WHERE user_id=?",
                        (new, user_id)
                    )
                return new
            except Exception:
                return current

    def is_waiting_name(self, user_id: str) -> bool:
        return user_id in self._waiting_names

    def set_waiting_name(self, user_id: str, waiting: bool):
        if waiting:
            self._waiting_names[user_id] = time.time()
        else:
            self._waiting_names.pop(user_id, None)

    def save_game_progress(self, user_id: str, progress: dict):
        with self._lock:
            self._game_progress[user_id] = {
                **progress,
                "saved_at": time.time()
            }

    def get_game_progress(self, user_id: str):
        return self._game_progress.get(user_id)

    def clear_game_progress(self, user_id: str):
        with self._lock:
            self._game_progress.pop(user_id, None)

    def cleanup_memory(self, timeout: int = 1800):
        now = time.time()

        with self._lock:
            self._waiting_names = {
                k: v for k, v in self._waiting_names.items()
                if now - v < timeout
            }

            self._game_progress = {
                k: v for k, v in self._game_progress.items()
                if now - v.get("saved_at", now) < timeout
            }
