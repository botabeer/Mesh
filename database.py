"""
Bot Mesh - Database Handler
Created by: Abeer Aldosari © 2025
"""
import sqlite3
from datetime import datetime, timedelta
import os

class DB:
    def __init__(self, path):
        # تأكد أن مجلد الملف موجود
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            uid TEXT PRIMARY KEY,
            name TEXT,
            points INTEGER DEFAULT 0,
            games INTEGER DEFAULT 0,
            wins INTEGER DEFAULT 0,
            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        self.conn.commit()

    def get_user(self, uid):
        self.cursor.execute("SELECT * FROM users WHERE uid=?", (uid,))
        row = self.cursor.fetchone()
        if row:
            return {
                'uid': row[0],
                'name': row[1],
                'points': row[2],
                'games': row[3],
                'wins': row[4],
                'joined_at': row[5],
                'last_active': row[6]
            }
        return None

    def add_or_update_user(self, uid, name):
        self.cursor.execute("""
        INSERT INTO users(uid, name) VALUES(?, ?)
        ON CONFLICT(uid) DO UPDATE SET name=excluded.name, last_active=CURRENT_TIMESTAMP
        """, (uid, name))
        self.conn.commit()

    def update_points(self, uid, points=0, won=False):
        user = self.get_user(uid)
        if user:
            new_points = user['points'] + points
            new_games = user['games'] + 1
            new_wins = user['wins'] + (1 if won else 0)
            self.cursor.execute("""
            UPDATE users
            SET points=?, games=?, wins=?, last_active=CURRENT_TIMESTAMP
            WHERE uid=?
            """, (new_points, new_games, new_wins, uid))
            self.conn.commit()

    def cleanup_names(self):
        """حذف المستخدمين الذين مضى على آخر نشاطهم أكثر من أسبوع"""
        one_week_ago = datetime.now() - timedelta(days=7)
        self.cursor.execute("DELETE FROM users WHERE last_active < ?", (one_week_ago,))
        self.conn.commit()
