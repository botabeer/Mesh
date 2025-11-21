import sqlite3
from datetime import datetime
from contextlib import contextmanager
from config import DB_NAME
import logging

logger = logging.getLogger(__name__)

@contextmanager
def get_db():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def init_database():
    """تهيئة قاعدة البيانات"""
    try:
        with get_db() as conn:
            c = conn.cursor()
            
            # جدول المستخدمين
            c.execute('''CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                display_name TEXT NOT NULL,
                total_points INTEGER DEFAULT 0,
                games_played INTEGER DEFAULT 0,
                wins INTEGER DEFAULT 0,
                registered_at TEXT DEFAULT CURRENT_TIMESTAMP,
                last_played TEXT
            )''')
            
            # جدول تاريخ الألعاب
            c.execute('''CREATE TABLE IF NOT EXISTS game_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                game_type TEXT NOT NULL,
                points INTEGER DEFAULT 0,
                won INTEGER DEFAULT 0,
                played_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )''')
            
            # Indexes للأداء
            c.execute('CREATE INDEX IF NOT EXISTS idx_users_points ON users(total_points DESC)')
            c.execute('CREATE INDEX IF NOT EXISTS idx_history_user ON game_history(user_id, played_at DESC)')
            
            conn.commit()
            logger.info("✅ تم تهيئة قاعدة البيانات بنجاح")
    except Exception as e:
        logger.error(f"❌ خطأ في تهيئة قاعدة البيانات: {e}")

def update_user_points(user_id, display_name, points, won=False, game_type=""):
    """تحديث نقاط المستخدم"""
    try:
        with get_db() as conn:
            c = conn.cursor()
            c.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
            user = c.fetchone()
            
            now = datetime.now().isoformat()
            
            if user:
                c.execute('''UPDATE users SET 
                    total_points = total_points + ?,
                    games_played = games_played + 1,
                    wins = wins + ?,
                    last_played = ?,
                    display_name = ?
                    WHERE user_id = ?''',
                    (points, 1 if won else 0, now, display_name, user_id))
            else:
                c.execute('''INSERT INTO users 
                    (user_id, display_name, total_points, games_played, wins, last_played)
                    VALUES (?, ?, ?, 1, ?, ?)''',
                    (user_id, display_name, points, 1 if won else 0, now))
            
            if game_type:
                c.execute('''INSERT INTO game_history 
                    (user_id, game_type, points, won)
                    VALUES (?, ?, ?, ?)''',
                    (user_id, game_type, points, 1 if won else 0))
            
            conn.commit()
            return True
    except Exception as e:
        logger.error(f"❌ خطأ في تحديث النقاط: {e}")
        return False

def get_user_stats(user_id):
    """الحصول على إحصائيات المستخدم"""
    try:
        with get_db() as conn:
            c = conn.cursor()
            c.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
            return c.fetchone()
    except Exception as e:
        logger.error(f"❌ خطأ في جلب الإحصائيات: {e}")
        return None

def get_leaderboard(limit=10):
    """الحصول على لوحة الصدارة"""
    try:
        with get_db() as conn:
            c = conn.cursor()
            c.execute('''SELECT display_name, total_points, games_played, wins 
                FROM users ORDER BY total_points DESC LIMIT ?''', (limit,))
            return c.fetchall()
    except Exception as e:
        logger.error(f"❌ خطأ في جلب الصدارة: {e}")
        return []
