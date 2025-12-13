import sqlite3
import logging
from threading import Lock
from datetime import datetime, timedelta
from contextlib import contextmanager

logger = logging.getLogger(__name__)

class Database:
    _lock = Lock()
    _conn = None
    _initialized = False
    _leaderboard_cache = None
    _leaderboard_cache_time = 0
    CACHE_TTL = 300
    INACTIVITY_DAYS = 30
    
    @staticmethod
    @contextmanager
    def get_connection():
        if Database._conn is None:
            Database._conn = sqlite3.connect(
                'game_scores.db',
                check_same_thread=False,
                timeout=10.0
            )
            Database._conn.row_factory = sqlite3.Row
            
            if not Database._initialized:
                Database._create_tables()
                Database._initialized = True
        
        conn = Database._conn
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
    
    @staticmethod
    def _create_tables():
        try:
            conn = Database._conn
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id TEXT PRIMARY KEY,
                    display_name TEXT NOT NULL,
                    total_points INTEGER DEFAULT 0,
                    games_played INTEGER DEFAULT 0,
                    wins INTEGER DEFAULT 0,
                    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS game_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    game_type TEXT NOT NULL,
                    points INTEGER DEFAULT 0,
                    won BOOLEAN DEFAULT 0,
                    played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
                )
            ''')
            
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_users_points 
                ON users(total_points DESC, games_played DESC)
            ''')
            
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_game_history 
                ON game_history(user_id, played_at DESC)
            ''')
            
            cursor.execute('PRAGMA foreign_keys = ON')
            cursor.execute('PRAGMA journal_mode = WAL')
            cursor.execute('PRAGMA synchronous = NORMAL')
            
            conn.commit()
            logger.info("Database tables created successfully")
        
        except Exception as e:
            logger.error(f"Database table creation error: {e}")
            raise
    
    @staticmethod
    def init():
        try:
            with Database.get_connection() as conn:
                pass
            logger.info("Database initialized successfully")
        except Exception as e:
            logger.error(f"Database init error: {e}")
            raise
    
    @staticmethod
    def register_or_update_user(user_id, display_name):
        with Database._lock:
            try:
                with Database.get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute('''
                        INSERT INTO users (user_id, display_name, last_activity)
                        VALUES (?, ?, CURRENT_TIMESTAMP)
                        ON CONFLICT(user_id) DO UPDATE SET
                            display_name = excluded.display_name,
                            last_activity = CURRENT_TIMESTAMP
                    ''', (user_id, display_name))
                    
                    logger.info(f"User registered: {user_id}")
                    return True
            except Exception as e:
                logger.error(f"Register error: {e}")
                return False
    
    @staticmethod
    def update_last_activity(user_id):
        try:
            with Database.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE users SET last_activity = CURRENT_TIMESTAMP
                    WHERE user_id = ?
                ''', (user_id,))
                return cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Update activity error: {e}")
            return False
    
    @staticmethod
    def update_user_points(user_id, points, won, game_type):
        with Database._lock:
            try:
                with Database.get_connection() as conn:
                    cursor = conn.cursor()
                    
                    cursor.execute('''
                        UPDATE users
                        SET total_points = total_points + ?,
                            games_played = games_played + 1,
                            wins = wins + ?,
                            last_activity = CURRENT_TIMESTAMP
                        WHERE user_id = ?
                    ''', (points, 1 if won else 0, user_id))
                    
                    cursor.execute('''
                        INSERT INTO game_history (user_id, game_type, points, won)
                        VALUES (?, ?, ?, ?)
                    ''', (user_id, game_type, points, won))
                    
                    Database._leaderboard_cache = None
                    
                    logger.info(f"Points updated for {user_id}: +{points}")
                    return True
            except Exception as e:
                logger.error(f"Update points error: {e}")
                return False
    
    @staticmethod
    def get_user_stats(user_id):
        try:
            with Database.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT total_points, games_played, wins, display_name
                    FROM users WHERE user_id = ?
                ''', (user_id,))
                
                row = cursor.fetchone()
                if row:
                    return {
                        'total_points': row[0],
                        'games_played': row[1],
                        'wins': row[2],
                        'display_name': row[3]
                    }
                return None
        except Exception as e:
            logger.error(f"Get stats error: {e}")
            return None
    
    @staticmethod
    def get_leaderboard(limit=20, force_refresh=False):
        from time import time
        now = time()
        
        if (not force_refresh and 
            Database._leaderboard_cache and 
            now - Database._leaderboard_cache_time < Database.CACHE_TTL):
            return Database._leaderboard_cache[:limit]
        
        try:
            with Database.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT display_name, total_points, games_played, wins
                    FROM users
                    WHERE games_played > 0
                    ORDER BY total_points DESC, wins DESC
                    LIMIT ?
                ''', (limit,))
                
                results = cursor.fetchall()
                leaders = [
                    (row[0], row[1])
                    for row in results
                ]
                
                Database._leaderboard_cache = leaders
                Database._leaderboard_cache_time = now
                
                return leaders
        except Exception as e:
            logger.error(f"Get leaderboard error: {e}")
            return []
    
    @staticmethod
    def cleanup_inactive_users():
        with Database._lock:
            try:
                with Database.get_connection() as conn:
                    cursor = conn.cursor()
                    cutoff = datetime.now() - timedelta(days=Database.INACTIVITY_DAYS)
                    
                    cursor.execute('''
                        DELETE FROM users
                        WHERE last_activity < ?
                    ''', (cutoff.strftime('%Y-%m-%d %H:%M:%S'),))
                    
                    deleted = cursor.rowcount
                    if deleted > 0:
                        logger.info(f"Cleaned up {deleted} inactive users")
                        Database._leaderboard_cache = None
                    
                    return deleted
            except Exception as e:
                logger.error(f"Cleanup error: {e}")
                return 0
