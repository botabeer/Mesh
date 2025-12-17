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
        self._changing_names = {}
        self._game_progress = {}
        self._ignored = set()
        self._theme_cache = {}
        self._cache_timeout = 300
        self._init_db()
        logger.info("Database initialized")

    # ================= Core =================

    @contextmanager
    def _get_conn(self):
        conn = sqlite3.connect(
            Config.DB_PATH,
            timeout=10,
            check_same_thread=False
        )
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=NORMAL")
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"DB error: {e}")
            raise
        finally:
            conn.close()

    def _init_db(self):
        with self._get_conn() as conn:
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
            conn.execute("CREATE INDEX IF NOT EXISTS idx_points ON users(points DESC, wins DESC)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_active ON users(last_active DESC)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_user_active ON users(user_id, last_active DESC)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_user_games ON users(games DESC) WHERE games > 0")

    # ================= Users =================

    def get_user(self, user_id):
        try:
            with self._get_conn() as conn:
                row = conn.execute(
                    "SELECT * FROM users WHERE user_id=?", (user_id,)
                ).fetchone()
                return dict(row) if row else None
        except Exception as e:
            logger.error(f"Get user error: {e}")
            return None

    def register_user(self, user_id, name):
        name = name.strip()
        if not Config.validate_name(name):
            return False

        try:
            with self._get_conn() as conn:
                exists = conn.execute(
                    "SELECT 1 FROM users WHERE user_id=?", (user_id,)
                ).fetchone()

                if exists:
                    conn.execute(
                        "UPDATE users SET name=?, last_active=CURRENT_TIMESTAMP WHERE user_id=?",
                        (name, user_id)
                    )
                else:
                    conn.execute(
                        "INSERT INTO users (user_id, name) VALUES (?, ?)",
                        (user_id, name)
                    )

            with self._lock:
                self._ignored.discard(user_id)
                self._theme_cache.pop(user_id, None)

            return True
        except Exception as e:
            logger.error(f"Register error: {e}")
            return False

    def change_name(self, user_id, new_name):
        new_name = new_name.strip()
        if not Config.validate_name(new_name):
            return False

        try:
            with self._get_conn() as conn:
                cur = conn.execute(
                    "UPDATE users SET name=?, last_active=CURRENT_TIMESTAMP WHERE user_id=?",
                    (new_name, user_id)
                )
                return cur.rowcount > 0
        except Exception as e:
            logger.error(f"Change name error: {e}")
            return False

    def update_activity(self, user_id):
        try:
            with self._get_conn() as conn:
                conn.execute(
                    "UPDATE users SET last_active=CURRENT_TIMESTAMP WHERE user_id=?",
                    (user_id,)
                )
        except Exception as e:
            logger.error(f"Update activity error: {e}")

    # ================= Stats =================

    def add_points(self, user_id, points):
        if points <= 0:
            return False
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

    def finish_game(self, user_id, won):
        try:
            with self._get_conn() as conn:
                cur = conn.execute(
                    "UPDATE users SET games=games+1, wins=wins+?, last_active=CURRENT_TIMESTAMP WHERE user_id=?",
                    (1 if won else 0, user_id)
                )
                return cur.rowcount > 0
        except Exception as e:
            logger.error(f"Finish game error: {e}")
            return False

    def get_leaderboard(self, limit=10):
        try:
            with self._get_conn() as conn:
                rows = conn.execute(
                    """SELECT name, points, wins, games
                       FROM users
                       WHERE games > 0
                       ORDER BY points DESC, wins DESC
                       LIMIT ?""",
                    (limit,)
                ).fetchall()
                return [dict(r) for r in rows]
        except Exception as e:
            logger.error(f"Leaderboard error: {e}")
            return []

    # ================= Theme =================

    def get_theme(self, user_id):
        now = time.time()
        cached = self._theme_cache.get(user_id)

        if cached and now - cached[1] < self._cache_timeout:
            return cached[0]

        try:
            with self._get_conn() as conn:
                row = conn.execute(
                    "SELECT theme FROM users WHERE user_id=?",
                    (user_id,)
                ).fetchone()
                theme = row["theme"] if row else "light"

            self._theme_cache[user_id] = (theme, now)
            return theme
        except Exception as e:
            logger.error(f"Get theme error: {e}")
            return "light"

    def toggle_theme(self, user_id):
        new_theme = "dark" if self.get_theme(user_id) == "light" else "light"
        try:
            with self._get_conn() as conn:
                conn.execute(
                    "UPDATE users SET theme=? WHERE user_id=?",
                    (new_theme, user_id)
                )
            self._theme_cache[user_id] = (new_theme, time.time())
            return new_theme
        except Exception as e:
            logger.error(f"Toggle theme error: {e}")
            return new_theme

    # ================= States =================

    def is_waiting_name(self, user_id):
        return user_id in self._waiting_names

    def set_waiting_name(self, user_id, state):
        with self._lock:
            if state:
                self._waiting_names[user_id] = time.time()
            else:
                self._waiting_names.pop(user_id, None)

    def is_changing_name(self, user_id):
        return user_id in self._changing_names

    def set_changing_name(self, user_id, state):
        with self._lock:
            if state:
                self._changing_names[user_id] = time.time()
            else:
                self._changing_names.pop(user_id, None)

    def is_ignored(self, user_id):
        return user_id in self._ignored

    def set_ignored(self, user_id, state):
        with self._lock:
            if state:
                self._ignored.add(user_id)
            else:
                self._ignored.discard(user_id)

    # ================= Games =================

    def save_game_progress(self, user_id, progress):
        with self._lock:
            self._game_progress[user_id] = {
                **progress,
                "saved_at": time.time()
            }

    def get_game_progress(self, user_id):
        return self._game_progress.get(user_id)

    def clear_game_progress(self, user_id):
        with self._lock:
            self._game_progress.pop(user_id, None)

    # ================= Cleanup =================

    def cleanup_memory(self, timeout=1800):
        now = time.time()
        with self._lock:
            self._waiting_names = {
                k: v for k, v in self._waiting_names.items()
                if now - v < timeout
            }
            self._changing_names = {
                k: v for k, v in self._changing_names.items()
                if now - v < timeout
            }
            self._game_progress = {
                k: v for k, v in self._game_progress.items()
                if now - v.get("saved_at", now) < timeout
            }
            self._theme_cache = {
                k: v for k, v in self._theme_cache.items()
                if now - v[1] < self._cache_timeout
            }
        logger.info("Memory cleanup completed")
