import sqlite3
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Tuple
from contextlib import contextmanager
from threading import Lock

logger = logging.getLogger(__name__)


class Database:
    """مدير قاعدة البيانات"""

    def __init__(self, db_path: str = "botmesh.db"):
        self.db_path = db_path
        self.lock = Lock()
        self.init_db()
        logger.info(f"تم تهيئة قاعدة البيانات: {db_path}")

    @contextmanager
    def get_conn(self):
        """الحصول على اتصال آمن"""
        conn = sqlite3.connect(self.db_path, timeout=30, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=NORMAL")
        
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
        """إنشاء الجداول"""
        with self.lock:
            with self.get_conn() as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        user_id TEXT PRIMARY KEY,
                        name TEXT NOT NULL,
                        points INTEGER DEFAULT 0,
                        is_registered BOOLEAN DEFAULT 0,
                        theme TEXT DEFAULT 'ابيض',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS sessions (
                        session_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id TEXT NOT NULL,
                        game_name TEXT NOT NULL,
                        score INTEGER DEFAULT 0,
                        completed BOOLEAN DEFAULT 0,
                        started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        completed_at TIMESTAMP,
                        FOREIGN KEY(user_id) REFERENCES users(user_id)
                    )
                """)
                
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS game_stats (
                        user_id TEXT NOT NULL,
                        game_name TEXT NOT NULL,
                        plays INTEGER DEFAULT 0,
                        wins INTEGER DEFAULT 0,
                        total_score INTEGER DEFAULT 0,
                        last_played TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        PRIMARY KEY(user_id, game_name),
                        FOREIGN KEY(user_id) REFERENCES users(user_id)
                    )
                """)
                
                conn.execute("CREATE INDEX IF NOT EXISTS idx_users_points ON users(points DESC)")
                conn.execute("CREATE INDEX IF NOT EXISTS idx_sessions_user ON sessions(user_id, started_at DESC)")
                
                logger.info("تم إنشاء الجداول بنجاح")

    def get_user(self, user_id: str) -> Optional[Dict]:
        """الحصول على بيانات المستخدم"""
        with self.get_conn() as conn:
            row = conn.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()
            return dict(row) if row else None

    def create_user(self, user_id: str, name: str) -> bool:
        """إنشاء مستخدم جديد"""
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

    def record_game_stat(self, user_id: str, game_name: str, score: int, won: bool = False) -> bool:
        """تسجيل إحصائيات اللعبة"""
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
        """الحصول على إحصائيات المستخدم"""
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
        """الحصول على الألعاب الأكثر شعبية"""
        with self.get_conn() as conn:
            rows = conn.execute(
                "SELECT game_name, SUM(plays) AS total FROM game_stats GROUP BY game_name ORDER BY total DESC LIMIT ?",
                (limit,)
            ).fetchall()
            return [r["game_name"] for r in rows]

    def get_stats(self) -> Dict:
        """الحصول على الإحصائيات العامة"""
        with self.get_conn() as conn:
            return {
                "total_users": conn.execute("SELECT COUNT(*) AS c FROM users").fetchone()["c"],
                "registered_users": conn.execute("SELECT COUNT(*) AS c FROM users WHERE is_registered = 1").fetchone()["c"],
                "total_sessions": conn.execute("SELECT COUNT(*) AS c FROM sessions").fetchone()["c"],
                "active_today": conn.execute(
                    "SELECT COUNT(*) AS c FROM users WHERE DATE(last_activity) = DATE(?)",
                    (datetime.now(),)
                ).fetchone()["c"]
            }

    def get_database_size(self) -> int:
        """الحصول على حجم قاعدة البيانات"""
        import os
        try:
            return os.path.getsize(self.db_path)
        except:
            return 0

    def update_user(self, user_id: str, **kwargs) -> bool:
        """تحديث بيانات المستخدم"""
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
                    conn.execute(f"UPDATE users SET {', '.join(fields)} WHERE user_id = ?", values)
            return True
        except Exception as e:
            logger.error(f"خطأ في التحديث: {e}")
            return False

    def update_user_name(self, user_id: str, name: str) -> bool:
        """تحديث اسم المستخدم"""
        return self.update_user(user_id, name=name[:100])

    def add_points(self, user_id: str, points: int) -> bool:
        """إضافة نقاط للمستخدم"""
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
        """تعيين ثيم المستخدم"""
        return self.update_user(user_id, theme=theme)

    def get_leaderboard(self, limit: int = 20) -> List[Tuple[str, int, bool]]:
        """الحصول على لوحة الصدارة"""
        with self.get_conn() as conn:
            rows = conn.execute(
                "SELECT name, points, is_registered FROM users WHERE points > 0 ORDER BY points DESC LIMIT ?",
                (limit,)
            ).fetchall()
            return [(r["name"], r["points"], bool(r["is_registered"])) for r in rows]

    def create_session(self, user_id: str, game_name: str) -> int:
        """إنشاء جلسة لعب"""
        with self.lock:
            with self.get_conn() as conn:
                cursor = conn.execute(
                    "INSERT INTO sessions (user_id, game_name, started_at) VALUES (?, ?, ?)",
                    (user_id, game_name, datetime.now())
                )
                return cursor.lastrowid

    def complete_session(self, session_id: int, score: int) -> bool:
        """إكمال جلسة اللعب"""
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
