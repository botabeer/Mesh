import sqlite3
import os

class DB:
    def __init__(self, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users (
            uid TEXT PRIMARY KEY,
            name TEXT,
            points INTEGER DEFAULT 0,
            games INTEGER DEFAULT 0,
            wins INTEGER DEFAULT 0,
            last_updated REAL
        )""")
        self.conn.commit()

    def update(self, uid, name, points=0, won=False, game_type=None):
        self.cursor.execute("SELECT * FROM users WHERE uid=?", (uid,))
        if self.cursor.fetchone():
            self.cursor.execute(
                "UPDATE users SET name=?, points=points+?, games=games+1, wins=wins+? WHERE uid=?",
                (name, points, int(won), uid)
            )
        else:
            self.cursor.execute(
                "INSERT INTO users (uid, name, points, games, wins, last_updated) VALUES (?,?,?,?,?,?)",
                (uid, name, points, 1, int(won), time.time())
            )
        self.conn.commit()

    def get_user(self, uid):
        self.cursor.execute("SELECT * FROM users WHERE uid=?", (uid,))
        row = self.cursor.fetchone()
        if row:
            return {'uid': row[0], 'name': row[1], 'points': row[2], 'games': row[3], 'wins': row[4]}
        return None

    def rank(self, uid):
        self.cursor.execute("SELECT uid FROM users ORDER BY points DESC")
        rows = self.cursor.fetchall()
        for idx, r in enumerate(rows):
            if r[0] == uid:
                return idx+1
        return None
