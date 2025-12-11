import sqlite3
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, List
from contextlib import contextmanager

logger = logging.getLogger(__name__)

class Database:
    """مدير قاعدة البيانات"""
    
    def __init__(self, db_path='botmesh.db'):
        self.db_path = db_path
        self.conn = None
        self.init_db()
    
    @contextmanager
    def get_conn(self):
        """الحصول على اتصال قاعدة البيانات"""
        conn = sqlite3.connect(self.db_path, timeout=30)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=NORMAL")
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"خطأ في قاعدة البيانات: {e}")
            raise
        finally:
            conn.close()
    
    def init_db(self):
        """تهيئة قاعدة البيانات"""
        with self.get_conn() as conn:
            cursor = conn.cursor()
            
            # جدول المستخدمين
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    points INTEGER DEFAULT 0,
                    is_registered BOOLEAN DEFAULT 0,
                    theme TEXT DEFAULT 'أبيض',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                ) WITHOUT ROWID
            ''')
            
            # جدول الجلسات
            cursor.execute('''
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
            ''')
            
            # جدول إحصائيات الالعاب
            cursor.execute('''
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
            ''')
            
            # الفهارس
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_points ON users(points DESC)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_registered ON users(is_registered) WHERE is_registered=1')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_sessions_user ON sessions(user_id, started_at DESC)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_stats_game ON game_stats(game_name, plays DESC)')
            
            logger.info("تم تهيئة قاعدة البيانات")
    
    def get_user(self, user_id: str) -> Optional[Dict]:
        """الحصول على بيانات المستخدم"""
        with self.get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT * FROM users WHERE user_id = ?',
                (user_id,)
            )
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def create_user(self, user_id: str, name: str) -> bool:
        """إنشاء مستخدم جديد"""
        with self.get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''INSERT OR IGNORE INTO users 
                   (user_id, name, points, is_registered, last_activity) 
                   VALUES (?, ?, 0, 0, ?)''',
                (user_id, name[:50], datetime.now())
            )
            return cursor.rowcount > 0
    
    def update_user(self, user_id: str, **kwargs) -> bool:
        """تحديث بيانات المستخدم"""
        if not kwargs:
            return False
        
        fields = []
        values = []
        
        for key, value in kwargs.items():
            if key in ['name', 'points', 'is_registered', 'theme']:
                fields.append(f"{key} = ?")
                values.append(value)
        
        if not fields:
            return False
        
        fields.append("last_activity = ?")
        values.extend([datetime.now(), user_id])
        
        with self.get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(
                f"UPDATE users SET {', '.join(fields)} WHERE user_id = ?",
                values
            )
            return cursor.rowcount > 0
    
    def update_user_name(self, user_id: str, name: str) -> bool:
        """تحديث اسم المستخدم"""
        return self.update_user(user_id, name=name[:50])
    
    def add_points(self, user_id: str, points: int) -> bool:
        """إضافة نقاط للمستخدم"""
        with self.get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE users SET points = points + ?, last_activity = ? WHERE user_id = ?',
                (points, datetime.now(), user_id)
            )
            return cursor.rowcount > 0
    
    def set_user_theme(self, user_id: str, theme: str) -> bool:
        """تعيين ثيم المستخدم"""
        return self.update_user(user_id, theme=theme)
    
    def get_leaderboard(self, limit: int = 20) -> List:
        """الحصول على لوحة الصدارة"""
        with self.get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''SELECT name, points, is_registered 
                   FROM users 
                   WHERE points > 0 
                   ORDER BY points DESC, last_activity DESC 
                   LIMIT ?''',
                (limit,)
            )
            return [
                (row['name'], row['points'], bool(row['is_registered']))
                for row in cursor.fetchall()
            ]
    
    def create_session(self, user_id: str, game_name: str, team_mode: bool = False) -> int:
        """إنشاء جلسة لعبة"""
        with self.get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''INSERT INTO sessions (user_id, game_name, team_mode, started_at) 
                   VALUES (?, ?, ?, ?)''',
                (user_id, game_name, int(team_mode), datetime.now())
            )
            return cursor.lastrowid
    
    def complete_session(self, session_id: int, score: int) -> bool:
        """إنهاء جلسة اللعبة"""
        with self.get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''UPDATE sessions 
                   SET completed = 1, score = ?, completed_at = ? 
                   WHERE session_id = ?''',
                (score, datetime.now(), session_id)
            )
            return cursor.rowcount > 0
    
    def record_game_stat(self, user_id: str, game_name: str, score: int, won: bool = False) -> bool:
        """تسجيل إحصائية اللعبة"""
        with self.get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''INSERT INTO game_stats 
                   (user_id, game_name, plays, wins, total_score, last_played) 
                   VALUES (?, ?, 1, ?, ?, ?)
                   ON CONFLICT(user_id, game_name) DO UPDATE SET
                   plays = plays + 1,
                   wins = wins + ?,
                   total_score = total_score + ?,
                   last_played = ?''',
                (user_id, game_name, int(won), score, datetime.now(),
                 int(won), score, datetime.now())
            )
            return cursor.rowcount > 0
    
    def get_user_stats(self, user_id: str) -> Dict:
        """الحصول على إحصائيات المستخدم"""
        with self.get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''SELECT game_name, plays, wins, total_score 
                   FROM game_stats 
                   WHERE user_id = ? 
                   ORDER BY plays DESC''',
                (user_id,)
            )
            return {
                row['game_name']: {
                    'plays': row['plays'],
                    'wins': row['wins'],
                    'score': row['total_score']
                }
                for row in cursor.fetchall()
            }
    
    def get_popular_games(self, limit: int = 13) -> List[str]:
        """الحصول على الالعاب الأكثر شعبية"""
        with self.get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''SELECT game_name, SUM(plays) as total 
                   FROM game_stats 
                   GROUP BY game_name 
                   ORDER BY total DESC 
                   LIMIT ?''',
                (limit,)
            )
            return [row['game_name'] for row in cursor.fetchall()]
    
    def get_stats(self) -> Dict:
        """الحصول على الإحصائيات العامة"""
        with self.get_conn() as conn:
            cursor = conn.cursor()
            
            cursor.execute('SELECT COUNT(*) as count FROM users')
            total_users = cursor.fetchone()['count']
            
            cursor.execute('SELECT COUNT(*) as count FROM users WHERE is_registered = 1')
            registered_users = cursor.fetchone()['count']
            
            cursor.execute('SELECT COUNT(*) as count FROM sessions')
            total_sessions = cursor.fetchone()['count']
            
            cursor.execute('SELECT COUNT(*) as count FROM sessions WHERE completed = 1')
            completed_sessions = cursor.fetchone()['count']
            
            return {
                'total_users': total_users,
                'registered_users': registered_users,
                'total_sessions': total_sessions,
                'completed_sessions': completed_sessions
            }
    
    def cleanup_old_data(self, days: int = 90):
        """تنظيف البيانات القديمة"""
        with self.get_conn() as conn:
            cursor = conn.cursor()
            cutoff = datetime.now() - timedelta(days=days)
            
            cursor.execute(
                '''DELETE FROM users 
                   WHERE last_activity < ? 
                   AND points = 0 
                   AND is_registered = 0''',
                (cutoff,)
            )
            deleted = cursor.rowcount
            
            if deleted > 0:
                logger.info(f"تم حذف {deleted} مستخدم غير نشط")
