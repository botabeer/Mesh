import sqlite3
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, List
from contextlib import contextmanager

logger = logging.getLogger(__name__)

class Database:
    def __init__(self, db_path='botmesh.db'):
        self.db_path = db_path
        self.init_db()
    
    @contextmanager
    def get_conn(self):
        conn = sqlite3.connect(self.db_path, timeout=30)
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
    
    def init_db(self):
        with self.get_conn() as conn:
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY, name TEXT NOT NULL, points INTEGER DEFAULT 0,
                is_registered BOOLEAN DEFAULT 0, theme TEXT DEFAULT 'ابيض',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) WITHOUT ROWID''')
            
            c.execute('''CREATE TABLE IF NOT EXISTS sessions (
                session_id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT NOT NULL,
                game_name TEXT NOT NULL, score INTEGER DEFAULT 0, team_mode BOOLEAN DEFAULT 0,
                completed BOOLEAN DEFAULT 0, started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP, FOREIGN KEY(user_id) REFERENCES users(user_id)
            )''')
            
            c.execute('''CREATE TABLE IF NOT EXISTS game_stats (
                user_id TEXT NOT NULL, game_name TEXT NOT NULL, plays INTEGER DEFAULT 0,
                wins INTEGER DEFAULT 0, total_score INTEGER DEFAULT 0,
                last_played TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY(user_id, game_name), FOREIGN KEY(user_id) REFERENCES users(user_id)
            ) WITHOUT ROWID''')
            
            c.execute('CREATE INDEX IF NOT EXISTS idx_users_points ON users(points DESC)')
            c.execute('CREATE INDEX IF NOT EXISTS idx_users_registered ON users(is_registered) WHERE is_registered=1')
            c.execute('CREATE INDEX IF NOT EXISTS idx_sessions_user ON sessions(user_id, started_at DESC)')
            c.execute('CREATE INDEX IF NOT EXISTS idx_stats_game ON game_stats(game_name, plays DESC)')
            logger.info("DB initialized")
    
    def get_user(self, user_id: str) -> Optional[Dict]:
        with self.get_conn() as conn:
            row = conn.execute('SELECT * FROM users WHERE user_id = ?', (user_id,)).fetchone()
            return dict(row) if row else None
    
    def create_user(self, user_id: str, name: str) -> bool:
        with self.get_conn() as conn:
            c = conn.execute('INSERT OR IGNORE INTO users (user_id, name, last_activity) VALUES (?, ?, ?)',
                           (user_id, name[:50], datetime.now()))
            return c.rowcount > 0
    
    def update_user(self, user_id: str, **kwargs) -> bool:
        if not kwargs:
            return False
        fields, values = [], []
        for k, v in kwargs.items():
            if k in ['name', 'points', 'is_registered', 'theme']:
                fields.append(f"{k} = ?")
                values.append(v)
        if not fields:
            return False
        fields.append("last_activity = ?")
        values.extend([datetime.now(), user_id])
        with self.get_conn() as conn:
            c = conn.execute(f"UPDATE users SET {', '.join(fields)} WHERE user_id = ?", values)
            return c.rowcount > 0
    
    def update_user_name(self, user_id: str, name: str) -> bool:
        return self.update_user(user_id, name=name[:50])
    
    def add_points(self, user_id: str, points: int) -> bool:
        with self.get_conn() as conn:
            c = conn.execute('UPDATE users SET points = points + ?, last_activity = ? WHERE user_id = ?',
                           (points, datetime.now(), user_id))
            return c.rowcount > 0
    
    def set_user_theme(self, user_id: str, theme: str) -> bool:
        return self.update_user(user_id, theme=theme)
    
    def get_leaderboard(self, limit: int = 20) -> List:
        with self.get_conn() as conn:
            rows = conn.execute('''SELECT name, points, is_registered FROM users 
                WHERE points > 0 ORDER BY points DESC, last_activity DESC LIMIT ?''', (limit,)).fetchall()
            return [(r['name'], r['points'], bool(r['is_registered'])) for r in rows]
    
    def create_session(self, user_id: str, game_name: str, team_mode: bool = False) -> int:
        with self.get_conn() as conn:
            c = conn.execute('INSERT INTO sessions (user_id, game_name, team_mode, started_at) VALUES (?, ?, ?, ?)',
                           (user_id, game_name, int(team_mode), datetime.now()))
            return c.lastrowid
    
    def complete_session(self, session_id: int, score: int) -> bool:
        with self.get_conn() as conn:
            c = conn.execute('UPDATE sessions SET completed = 1, score = ?, completed_at = ? WHERE session_id = ?',
                           (score, datetime.now(), session_id))
            return c.rowcount > 0
    
    def record_game_stat(self, user_id: str, game_name: str, score: int, won: bool = False) -> bool:
        with self.get_conn() as conn:
            c = conn.execute('''INSERT INTO game_stats (user_id, game_name, plays, wins, total_score, last_played) 
                VALUES (?, ?, 1, ?, ?, ?) ON CONFLICT(user_id, game_name) DO UPDATE SET
                plays = plays + 1, wins = wins + ?, total_score = total_score + ?, last_played = ?''',
                (user_id, game_name, int(won), score, datetime.now(), int(won), score, datetime.now()))
            return c.rowcount > 0
    
    def get_user_stats(self, user_id: str) -> Dict:
        with self.get_conn() as conn:
            rows = conn.execute('''SELECT game_name, plays, wins, total_score FROM game_stats 
                WHERE user_id = ? ORDER BY plays DESC''', (user_id,)).fetchall()
            return {r['game_name']: {'plays': r['plays'], 'wins': r['wins'], 'score': r['total_score']} for r in rows}
    
    def get_popular_games(self, limit: int = 13) -> List[str]:
        with self.get_conn() as conn:
            rows = conn.execute('''SELECT game_name FROM game_stats 
                GROUP BY game_name ORDER BY SUM(plays) DESC LIMIT ?''', (limit,)).fetchall()
            return [r['game_name'] for r in rows]
    
    def get_stats(self) -> Dict:
        with self.get_conn() as conn:
            return {
                'total_users': conn.execute('SELECT COUNT(*) as c FROM users').fetchone()['c'],
                'registered_users': conn.execute('SELECT COUNT(*) as c FROM users WHERE is_registered = 1').fetchone()['c'],
                'total_sessions': conn.execute('SELECT COUNT(*) as c FROM sessions').fetchone()['c'],
                'completed_sessions': conn.execute('SELECT COUNT(*) as c FROM sessions WHERE completed = 1').fetchone()['c']
            }
    
    def cleanup_old_data(self, days: int = 90):
        with self.get_conn() as conn:
            c = conn.execute('''DELETE FROM users WHERE last_activity < ? 
                AND points = 0 AND is_registered = 0''', (datetime.now() - timedelta(days=days),))
            if c.rowcount > 0:
                logger.info(f"Deleted {c.rowcount} inactive users")
