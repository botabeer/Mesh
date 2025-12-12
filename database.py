import sqlite3
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Tuple
from contextlib import contextmanager
from threading import Lock

logger = logging.getLogger(__name__)


class Database:
    """مدير قاعدة البيانات الآمن والمحسّن"""

    def __init__(self, db_path: str = "botmesh.db"):
        self.db_path = db_path
        self.lock = Lock()
        self.init_db()
        logger.info(f"تم تهيئة قاعدة البيانات: {db_path}")

    @contextmanager
    def get_conn(self):
        """الحصول على اتصال آمن بقاعدة البيانات"""
        conn = sqlite3.connect(self.db_path, timeout=30, check_same_thread=False)
        conn.row_factory = sqlite3.Row

        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=NORMAL")
        conn.execute("PRAGMA cache_size=10000")
        conn.execute("PRAGMA temp_store=MEMORY")

        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"خطأ في قاعدة البيانات: {e}", exc_info=True)
            raise
        finally:
            conn.close()

    def init_db(self):
        """إنشاء الجداول والفهارس"""
        with self.lock:
            with self.get_conn() as conn:
                c = conn.cursor()

                c.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        user_id TEXT PRIMARY KEY,
                        name TEXT NOT NULL,
                        points INTEGER DEFAULT 0,
                        is_registered BOOLEAN DEFAULT 0,
                        theme TEXT DEFAULT 'ابيض',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    ) WITHOUT ROWID
                """)

                c.execute("""
                    CREATE TABLE IF NOT EXISTS sessions (
                        session_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id TEXT NOT NULL,
                        game_name TEXT NOT NULL,
                        score INTEGER DEFAULT 0,
                        team_mode BOOLEAN DEFAULT 0,
                        completed BOOLEAN DEFAULT 0,
                        started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        completed_at TIMESTAMP,
                        FOREIGN KEY(user_id) REFERENCES users(user_id)
                    )
                """)

                c.execute("""
                    CREATE TABLE IF NOT EXISTS game_stats (
                        user_id TEXT NOT NULL,
                        game_name TEXT NOT NULL,
                        plays INTEGER DEFAULT 0,
                        wins INTEGER DEFAULT 0,
                        total_score INTEGER DEFAULT 0,
                        last_played TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        PRIMARY KEY(user_id, game_name),
                        FOREIGN KEY(user_id) REFERENCES users(user_id)
                    ) WITHOUT ROWID
                """)

                c.execute("CREATE INDEX IF NOT EXISTS idx_users_points ON users(points DESC)")
                c.execute("CREATE INDEX IF NOT EXISTS idx_users_registered ON users(is_registered) WHERE is_registered=1")
                c.execute("CREATE INDEX IF NOT EXISTS idx_users_activity ON users(last_activity DESC)")
                c.execute("CREATE INDEX IF NOT EXISTS idx_sessions_user ON sessions(user_id, started_at DESC)")
                c.execute("CREATE INDEX IF NOT EXISTS idx_sessions_game ON sessions(game_name, started_at DESC)")
                c.execute("CREATE INDEX IF NOT EXISTS idx_stats_game ON game_stats(game_name, plays DESC)")
                c.execute("CREATE INDEX IF NOT EXISTS idx_stats_user ON game_stats(user_id, last_played DESC)")

                logger.info("تم إنشاء الجداول والفهارس بنجاح")

    # المستخدمون

    def get_user(self, user_id: str) -> Optional[Dict]:
        with self.get_conn() as conn:
            row = conn.execute(
                "SELECT * FROM users WHERE user_id = ?",
                (user_id,)
            ).fetchone()
            return dict(row) if row else None

    def create_user(self, user_id: str, name: str) -> bool:
        try:
            with self.lock:
                with self.get_conn() as conn:
                    conn.execute(
                        "INSERT OR IGNORE INTO users (user_id, name, last_activity) VALUES (?, ?, ?)",
                        (user_id, name[:100], datetime.now())
                    )
                    return True
        except Exception as e:
            logger.error(f"خطأ في إنشاء المستخدم: {e}")
            return False

    def update_user(self, user_id: str, **kwargs) -> bool:
        if not kwargs:
            return False

        allowed = {"name", "points", "is_registered", "theme"}
        fields = []
        values = []

        for key, value in kwargs.items():
            if key in allowed:
                fields.append(f"{key} = ?")
                values.append(value)

        if not fields:
            return False

        fields.append("last_activity = ?")
        values.append(datetime.now())
        values.append(user_id)

        try:
            with self.lock:
                with self.get_conn() as conn:
                    conn.execute(
                        f"UPDATE users SET {', '.join(fields)} WHERE user_id = ?",
                        values
                    )
            return True
        except Exception as e:
            logger.error(f"خطأ في التحديث: {e}")
            return False

    def update_user_name(self, user_id: str, name: str) -> bool:
        return self.update_user(user_id, name=name[:100])

    def add_points(self, user_id: str, points: int) -> bool:
        try:
            with self.lock:
                with self.get_conn() as conn:
                    conn.execute(
                        "UPDATE users SET points = points + ?, last_activity = ? WHERE user_id = ?",
                        (points, datetime.now(), user_id)
                    )
            return True
        except Exception as e:
            logger.error(f"خطأ في إضافة النقاط: {e}")
            return False

    def set_user_theme(self, user_id: str, theme: str) -> bool:
        return self.update_user(user_id, theme=theme)

    def get_leaderboard(self, limit: int = 20) -> List[Tuple[str, int, bool]]:
        with self.get_conn() as conn:
            rows = conn.execute(
                "SELECT name, points, is_registered FROM users WHERE points > 0 ORDER BY points DESC, last_activity DESC LIMIT ?",
                (limit,)
            ).fetchall()
            return [(r["name"], r["points"], bool(r["is_registered"])) for r in rows]

    # الجلسات

    def create_session(self, user_id: str, game_name: str, team_mode: bool = False) -> int:
        with self.lock:
            with self.get_conn() as conn:
                cursor = conn.execute(
                    "INSERT INTO sessions (user_id, game_name, team_mode, started_at) VALUES (?, ?, ?, ?)",
                    (user_id, game_name, int(team_mode), datetime.now())
                )
                return cursor.lastrowid

    def complete_session(self, session_id: int, score: int) -> bool:
        try:
            with self.lock:
                with self.get_conn() as conn:
                    conn.execute(
                        "UPDATE sessions SET completed = 1, score = ?, completed_at = ? WHERE session_id = ?",
                        (score, datetime.now(), session_id)
                    )
            return True
        except Exception as e:
            logger.error(f"خطأ في إكمال الجلسة: {e}")
            return False

    def get_user_sessions(self, user_id: str, limit: int = 10) -> List[Dict]:
        with self.get_conn() as conn:
            rows = conn.execute(
                "SELECT * FROM sessions WHERE user_id = ? ORDER BY started_at DESC LIMIT ?",
                (user_id, limit)
            ).fetchall()
            return [dict(r) for r in rows]

    # الإحصائيات

    def record_game_stat(self, user_id: str, game_name: str, score: int, won: bool = False) -> bool:
        try:
            with self.lock:
                with self.get_conn() as conn:
                    conn.execute(
                        """
                        INSERT INTO game_stats (user_id, game_name, plays, wins, total_score, last_played)
                        VALUES (?, ?, 1, ?, ?, ?)
                        ON CONFLICT(user_id, game_name) DO UPDATE SET
                            plays = plays + 1,
                            wins = wins + ?,
                            total_score = total_score + ?,
                            last_played = ?
                        """,
                        (user_id, game_name, int(won), score, datetime.now(),
                         int(won), score, datetime.now())
                    )
            return True
        except Exception as e:
            logger.error(f"خطأ في تسجيل الإحصائية: {e}")
            return False

    def get_user_stats(self, user_id: str) -> Dict:
        with self.get_conn() as conn:
            rows = conn.execute(
                "SELECT game_name, plays, wins, total_score FROM game_stats WHERE user_id = ? ORDER BY plays DESC",
                (user_id,)
            ).fetchall()

            return {
                r["game_name"]: {
                    "plays": r["plays"],
                    "wins": r["wins"],
                    "score": r["total_score"]
                }
                for r in rows
            }

    def get_popular_games(self, limit: int = 13) -> List[str]:
        with self.get_conn() as conn:
            rows = conn.execute(
                "SELECT game_name, SUM(plays) AS total_plays FROM game_stats GROUP BY game_name ORDER BY total_plays DESC LIMIT ?",
                (limit,)
            ).fetchall()
            return [r["game_name"] for r in rows]

    def get_game_leaderboard(self, game_name: str, limit: int = 10) -> List[Tuple[str, int, int]]:
        with self.get_conn() as conn:
            rows = conn.execute(
                """
                SELECT u.name, gs.total_score, gs.plays
                FROM game_stats gs
                JOIN users u ON gs.user_id = u.user_id
                WHERE gs.game_name = ?
                ORDER BY gs.total_score DESC, gs.plays ASC
                LIMIT ?
                """,
                (game_name, limit)
            ).fetchall()

            return [(r["name"], r["total_score"], r["plays"]) for r in rows]

    # الإحصائيات العامة

    def get_stats(self) -> Dict:
        with self.get_conn() as conn:
            return {
                "total_users": conn.execute("SELECT COUNT(*) AS c FROM users").fetchone()["c"],
                "registered_users": conn.execute("SELECT COUNT(*) AS c FROM users WHERE is_registered = 1").fetchone()["c"],
                "total_sessions": conn.execute("SELECT COUNT(*) AS c FROM sessions").fetchone()["c"],
                "completed_sessions": conn.execute("SELECT COUNT(*) AS c FROM sessions WHERE completed = 1").fetchone()["c"],
                "total_points": conn.execute("SELECT COALESCE(SUM(points), 0) AS s FROM users").fetchone()["s"],
                "active_today": conn.execute(
                    "SELECT COUNT(*) AS c FROM users WHERE DATE(last_activity) = DATE(?)",
                    (datetime.now(),)
                ).fetchone()["c"]
            }

    # الصيانة

    def cleanup_old_data(self, days: int = 90):
        cutoff = datetime.now() - timedelta(days=days)

        try:
            with self.lock:
                with self.get_conn() as conn:
                    deleted_users = conn.execute(
                        "DELETE FROM users WHERE last_activity < ? AND points = 0 AND is_registered = 0",
                        (cutoff,)
                    ).rowcount

                    deleted_sessions = conn.execute(
                        "DELETE FROM sessions WHERE completed = 1 AND completed_at < ?",
                        (cutoff,)
                    ).rowcount

                    conn.execute("VACUUM")

                return deleted_users, deleted_sessions

        except Exception as e:
            logger.error(f"خطأ في التنظيف: {e}")
            return 0, 0

    def backup_database(self, backup_path: str) -> bool:
        try:
            import shutil
            shutil.copy2(self.db_path, backup_path)
            logger.info(f"تم النسخ الاحتياطي: {backup_path}")
            return True
        except Exception as e:
            logger.error(f"خطأ في النسخ الاحتياطي: {e}")
            return False

    def get_database_size(self) -> int:
        import os
        try:
            return os.path.getsize(self.db_path)
        except:
            return 0
