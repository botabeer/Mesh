"""
Bot Mesh - Database Manager
"""
import sqlite3
import time
from datetime import datetime, timedelta

class DB:
    def __init__(self, path='data/game.db'):
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self._create_tables()

    def _create_tables(self):
        c = self.conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS users(
                uid TEXT PRIMARY KEY,
                name TEXT,
                theme TEXT,
                points INTEGER,
                games INTEGER,
                wins INTEGER,
                last_active REAL
            )
        """)
        self.conn.commit()

    def register_or_update_user(self, uid, name):
        now = time.time()
        user = self.get_user(uid)
        c = self.conn.cursor()
        if user:
            c.execute("UPDATE users SET name=?, last_active=? WHERE uid=?", (name, now, uid))
        else:
            c.execute("INSERT INTO users(uid,name,theme,points,games,wins,last_active) VALUES(?,?,?,?,?,?,?)",
                      (uid, name, 'white', 0,0,0, now))
        self.conn.commit()

    def remove_user(self, uid):
        c = self.conn.cursor()
        c.execute("DELETE FROM users WHERE uid=?", (uid,))
        self.conn.commit()

    def get_user(self, uid):
        c = self.conn.cursor()
        c.execute("SELECT * FROM users WHERE uid=?", (uid,))
        row = c.fetchone()
        if row:
            return {'uid': row[0], 'name': row[1], 'theme': row[2],
                    'points': row[3], 'games': row[4], 'wins': row[5], 'last_active': row[6]}
        return None

    def set_theme(self, uid, theme):
        c = self.conn.cursor()
        c.execute("UPDATE users SET theme=? WHERE uid=?", (theme, uid))
        self.conn.commit()

    def update(self, uid, name, points, won, game_type):
        c = self.conn.cursor()
        user = self.get_user(uid)
        if not user:
            return
        games = user['games'] + 1
        wins = user['wins'] + (1 if won else 0)
        total_points = user['points'] + points
        c.execute("UPDATE users SET points=?, games=?, wins=?, name=?, last_active=? WHERE uid=?",
                  (total_points, games, wins, name, time.time(), uid))
        self.conn.commit()

    def rank(self, uid):
        c = self.conn.cursor()
        c.execute("SELECT uid, points FROM users ORDER BY points DESC")
        users = c.fetchall()
        for idx, u in enumerate(users,1):
            if u[0]==uid:
                return idx
        return None

    def cleanup_old_users(self, days=7):
        cutoff = time.time() - days*86400
        c = self.conn.cursor()
        c.execute("DELETE FROM users WHERE last_active<?", (cutoff,))
        self.conn.commit()
