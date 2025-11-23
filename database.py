"""
Bot Mesh - Database (SQLite)
"""
import sqlite3
import time

class DB:
    def __init__(self, path):
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self.create_tables()

    def create_tables(self):
        c = self.conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS users(
            uid TEXT PRIMARY KEY,
            name TEXT,
            points INTEGER DEFAULT 0,
            games INTEGER DEFAULT 0,
            wins INTEGER DEFAULT 0,
            theme TEXT DEFAULT 'white',
            joined_at REAL DEFAULT ?)
        """, (time.time(),))
        self.conn.commit()

    def get_user(self, uid):
        c = self.conn.cursor()
        c.execute("SELECT * FROM users WHERE uid=?", (uid,))
        row = c.fetchone()
        if row:
            keys = ["uid","name","points","games","wins","theme","joined_at"]
            return dict(zip(keys,row))
        return None

    def update(self, uid, name, points, won, game_type, theme="white"):
        user = self.get_user(uid)
        if not user:
            c = self.conn.cursor()
            c.execute("INSERT INTO users(uid,name,points,games,wins,theme,joined_at) VALUES(?,?,?,?,?,?,?)",
                      (uid,name,points,1,1 if won else 0,theme,time.time()))
        else:
            c = self.conn.cursor()
            c.execute("""UPDATE users SET name=?, points=points+?, games=games+1,
                         wins=wins+? WHERE uid=?""",(name,points,1 if won else 0,uid))
        self.conn.commit()

    def set_theme(self, uid, theme):
        c = self.conn.cursor()
        c.execute("UPDATE users SET theme=? WHERE uid=?", (theme, uid))
        self.conn.commit()

    def rank(self, uid):
        c = self.conn.cursor()
        c.execute("SELECT COUNT(*)+1 FROM users WHERE points>=(SELECT points FROM users WHERE uid=?)", (uid,))
        return c.fetchone()[0]

    def cleanup_old_users(self):
        """حذف المستخدمين بعد أسبوع"""
        week_ago = time.time() - 7*24*3600
        c = self.conn.cursor()
        c.execute("DELETE FROM users WHERE joined_at<?", (week_ago,))
        self.conn.commit()
