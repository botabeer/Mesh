import sqlite3
import logging
import time
from threading import Lock
from contextlib import contextmanager
from typing import Optional, Dict, List
from config import Config

logger = logging.getLogger(__name__)


class Database:
    """إدارة قاعدة البيانات المحسّنة"""
    
    def __init__(self):
        self._lock = Lock()
        self._waiting_names = {}
        self._changing_names = {}
        self._game_progress = {}
        self._unregistered = set()  # المستخدمون الذين اختاروا عدم التسجيل
        self._init_db()
        logger.info("Database initialized")

    @contextmanager
    def _get_conn(self):
        """الحصول على اتصال بقاعدة البيانات"""
        conn = sqlite3.connect(
            Config.DB_PATH, 
            timeout=10, 
            check_same_thread=False,
            isolation_level=None
        )
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=NORMAL")
        
        try:
            yield conn
        except Exception as e:
            logger.error(f"Database error: {e}")
            raise
        finally:
            conn.close()

    def _init_db(self):
        """إنشاء الجداول"""
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
            
            conn.execute("CREATE INDEX IF NOT EXISTS idx_points ON users(points DESC, wins DESC)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_active ON users(last_active DESC)")

    def get_user(self, user_id: str) -> Optional[Dict]:
        """الحصول على بيانات المستخدم"""
        try:
            with self._get_conn() as conn:
                row = conn.execute("SELECT * FROM users WHERE user_id=?", (user_id,)).fetchone()
                return dict(row) if row else None
        except:
            return None

    def register_user(self, user_id: str, name: str) -> bool:
        """تسجيل مستخدم جديد"""
        name = name.strip()
        if not Config.validate_name(name):
            return False
        
        with self._lock:
            try:
                with self._get_conn() as conn:
                    existing = conn.execute("SELECT user_id FROM users WHERE user_id=?", (user_id,)).fetchone()
                    
                    if existing:
                        conn.execute(
                            "UPDATE users SET name=?, last_active=CURRENT_TIMESTAMP WHERE user_id=?",
                            (name, user_id)
                        )
                    else:
                        conn.execute("INSERT INTO users (user_id, name) VALUES (?, ?)", (user_id, name))
                    
                    # إزالة من قائمة غير المسجلين
                    self._unregistered.discard(user_id)
                    logger.info(f"User registered: {user_id} -> {name}")
                    return True
            except Exception as e:
                logger.error(f"Register error: {e}")
                return False

    def change_name(self, user_id: str, new_name: str) -> bool:
        """تغيير اسم المستخدم"""
        new_name = new_name.strip()
        if not Config.validate_name(new_name):
            return False
        
        with self._lock:
            try:
                with self._get_conn() as conn:
                    conn.execute(
                        "UPDATE users SET name=?, last_active=CURRENT_TIMESTAMP WHERE user_id=?",
                        (new_name, user_id)
                    )
                    logger.info(f"Name changed: {user_id} -> {new_name}")
                    return True
            except:
                return False

    def update_activity(self, user_id: str):
        """تحديث وقت النشاط"""
        try:
            with self._get_conn() as conn:
                conn.execute("UPDATE users SET last_active=CURRENT_TIMESTAMP WHERE user_id=?", (user_id,))
        except:
            pass

    def add_points(self, user_id: str, points: int) -> bool:
        """إضافة نقاط للمستخدم"""
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
            except:
                return False

    def finish_game(self, user_id: str, won: bool) -> bool:
        """تسجيل انتهاء اللعبة"""
        with self._lock:
            try:
                with self._get_conn() as conn:
                    cur = conn.execute(
                        "UPDATE users SET games=games+1, wins=wins+?, last_active=CURRENT_TIMESTAMP WHERE user_id=?",
                        (1 if won else 0, user_id)
                    )
                    return cur.rowcount > 0
            except:
                return False

    def get_leaderboard(self, limit: int = 10) -> List[Dict]:
        """الحصول على لوحة الصدارة"""
        try:
            with self._get_conn() as conn:
                rows = conn.execute(
                    "SELECT name, points, wins, games FROM users WHERE games>0 ORDER BY points DESC, wins DESC LIMIT ?",
                    (limit,)
                ).fetchall()
                return [dict(r) for r in rows]
        except:
            return []

    def get_theme(self, user_id: str) -> str:
        """الحصول على سمة المستخدم"""
        try:
            with self._get_conn() as conn:
                row = conn.execute("SELECT theme FROM users WHERE user_id=?", (user_id,)).fetchone()
                return row["theme"] if row else "light"
        except:
            return "light"

    def toggle_theme(self, user_id: str) -> str:
        """تبديل السمة"""
        current = self.get_theme(user_id)
        new_theme = "dark" if current == "light" else "light"
        
        with self._lock:
            try:
                with self._get_conn() as conn:
                    conn.execute("UPDATE users SET theme=? WHERE user_id=?", (new_theme, user_id))
                    return new_theme
            except:
                return current

    # إدارة حالات الانتظار
    def is_waiting_name(self, user_id: str) -> bool:
        return user_id in self._waiting_names

    def set_waiting_name(self, user_id: str, waiting: bool):
        if waiting:
            self._waiting_names[user_id] = time.time()
        else:
            self._waiting_names.pop(user_id, None)

    def is_changing_name(self, user_id: str) -> bool:
        return user_id in self._changing_names

    def set_changing_name(self, user_id: str, changing: bool):
        if changing:
            self._changing_names[user_id] = time.time()
        else:
            self._changing_names.pop(user_id, None)

    # إدارة المستخدمين المتجاهلين (انسحب)
    def is_ignored(self, user_id: str) -> bool:
        """التحقق إذا كان المستخدم في وضع التجاهل"""
        return user_id in self._unregistered

    def set_ignored(self, user_id: str, ignored: bool):
        """تعيين حالة التجاهل"""
        if ignored:
            self._unregistered.add(user_id)
            logger.info(f"User ignored: {user_id}")
        else:
            self._unregistered.discard(user_id)
            logger.info(f"User unignored: {user_id}")

    # إدارة تقدم اللعبة
    def save_game_progress(self, user_id: str, progress: dict):
        with self._lock:
            self._game_progress[user_id] = {**progress, "saved_at": time.time()}

    def get_game_progress(self, user_id: str) -> Optional[Dict]:
        return self._game_progress.get(user_id)

    def clear_game_progress(self, user_id: str):
        with self._lock:
            self._game_progress.pop(user_id, None)

    def cleanup_memory(self, timeout: int = 1800):
        """تنظيف الذاكرة من البيانات القديمة"""
        now = time.time()
        with self._lock:
            self._waiting_names = {k: v for k, v in self._waiting_names.items() if now - v < timeout}
            self._changing_names = {k: v for k, v in self._changing_names.items() if now - v < timeout}
            self._game_progress = {k: v for k, v in self._game_progress.items() if now - v.get("saved_at", now) < timeout}
        logger.info("Memory cleanup completed")
