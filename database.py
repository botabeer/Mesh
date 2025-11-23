"""
Bot Mesh - Database Handler
Created by: Abeer Aldosari © 2025
"""
import sqlite3
from datetime import datetime, timedelta
import os
import logging

logger = logging.getLogger(__name__)

class DB:
    def __init__(self, path):
        try:
            # تأكد أن مجلد الملف موجود
            dir_path = os.path.dirname(path)
            if dir_path:
                os.makedirs(dir_path, exist_ok=True)
            
            self.path = path
            self.conn = sqlite3.connect(path, check_same_thread=False, timeout=10)
            self.conn.row_factory = sqlite3.Row
            self.cursor = self.conn.cursor()
            self._create_tables()
            logger.info(f"✅ Database initialized at: {path}")
        except Exception as e:
            logger.error(f"❌ Database initialization failed: {e}")
            raise

    def _create_tables(self):
        try:
            # جدول المستخدمين
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                uid TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                theme TEXT DEFAULT 'white',
                points INTEGER DEFAULT 0,
                games INTEGER DEFAULT 0,
                wins INTEGER DEFAULT 0,
                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
            
            # جدول الإحصائيات
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                uid TEXT NOT NULL,
                game_type TEXT NOT NULL,
                points INTEGER DEFAULT 0,
                won INTEGER DEFAULT 0,
                played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (uid) REFERENCES users(uid) ON DELETE CASCADE
            )
            """)
            
            # إنشاء فهارس لتحسين الأداء
            self.cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_users_last_active 
            ON users(last_active)
            """)
            
            self.cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_stats_uid 
            ON stats(uid)
            """)
            
            self.conn.commit()
            logger.info("✅ Database tables created successfully")
        except Exception as e:
            logger.error(f"❌ Failed to create tables: {e}")
            raise

    def get_user(self, uid):
        try:
            self.cursor.execute("SELECT * FROM users WHERE uid=?", (uid,))
            row = self.cursor.fetchone()
            if row:
                return dict(row)
            return None
        except Exception as e:
            logger.error(f"❌ Error getting user {uid}: {e}")
            return None

    def add_or_update_user(self, uid, name):
        try:
            self.cursor.execute("""
            INSERT INTO users(uid, name, last_active) 
            VALUES(?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(uid) DO UPDATE SET 
                name=excluded.name, 
                last_active=CURRENT_TIMESTAMP
            """, (uid, name))
            self.conn.commit()
            logger.debug(f"✅ User updated: {uid} - {name}")
            return True
        except Exception as e:
            logger.error(f"❌ Error updating user {uid}: {e}")
            return False

    def update_points(self, uid, points=0, won=False):
        try:
            user = self.get_user(uid)
            if not user:
                logger.warning(f"⚠️ User {uid} not found for points update")
                return False
            
            new_points = user['points'] + points
            new_games = user['games'] + 1
            new_wins = user['wins'] + (1 if won else 0)
            
            self.cursor.execute("""
            UPDATE users
            SET points=?, games=?, wins=?, last_active=CURRENT_TIMESTAMP
            WHERE uid=?
            """, (new_points, new_games, new_wins, uid))
            self.conn.commit()
            logger.info(f"✅ Points updated for {uid}: +{points} pts, won={won}")
            return True
        except Exception as e:
            logger.error(f"❌ Error updating points for {uid}: {e}")
            return False

    def update_theme(self, uid, theme):
        try:
            self.cursor.execute("""
            UPDATE users 
            SET theme=?, last_active=CURRENT_TIMESTAMP 
            WHERE uid=?
            """, (theme, uid))
            self.conn.commit()
            logger.info(f"✅ Theme updated for {uid}: {theme}")
            return True
        except Exception as e:
            logger.error(f"❌ Error updating theme for {uid}: {e}")
            return False

    def add_game_stat(self, uid, game_type, points, won):
        try:
            self.cursor.execute("""
            INSERT INTO stats(uid, game_type, points, won)
            VALUES(?, ?, ?, ?)
            """, (uid, game_type, points, 1 if won else 0))
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(f"❌ Error adding game stat: {e}")
            return False

    def get_leaderboard(self, limit=10):
        try:
            self.cursor.execute("""
            SELECT uid, name, points, games, wins
            FROM users
            ORDER BY points DESC, wins DESC
            LIMIT ?
            """, (limit,))
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            logger.error(f"❌ Error getting leaderboard: {e}")
            return []

    def get_user_rank(self, uid):
        try:
            self.cursor.execute("""
            SELECT COUNT(*) + 1 as rank
            FROM users
            WHERE points > (SELECT points FROM users WHERE uid=?)
            """, (uid,))
            result = self.cursor.fetchone()
            return result['rank'] if result else None
        except Exception as e:
            logger.error(f"❌ Error getting user rank: {e}")
            return None

    def cleanup_inactive_users(self, days=7):
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            self.cursor.execute("""
            DELETE FROM users 
            WHERE last_active < ?
            """, (cutoff_date,))
            deleted = self.cursor.rowcount
            self.conn.commit()
            logger.info(f"✅ Cleaned up {deleted} inactive users (older than {days} days)")
            return deleted
        except Exception as e:
            logger.error(f"❌ Error during cleanup: {e}")
            return 0

    def get_stats(self):
        try:
            self.cursor.execute("""
            SELECT 
                COUNT(*) as total_users,
                SUM(games) as total_games,
                SUM(points) as total_points
            FROM users
            """)
            result = self.cursor.fetchone()
            return dict(result) if result else {}
        except Exception as e:
            logger.error(f"❌ Error getting stats: {e}")
            return {}

    def close(self):
        try:
            if self.conn:
                self.conn.close()
                logger.info("✅ Database connection closed")
        except Exception as e:
            logger.error(f"❌ Error closing database: {e}")

    def __del__(self):
        self.close()
