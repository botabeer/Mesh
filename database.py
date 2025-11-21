import sqlite3
from config import Config

DB_NAME = Config.DB_NAME

class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DB_NAME, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user TEXT NOT NULL,
                score INTEGER NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()

    def add_score(self, user, score):
        self.cursor.execute(
            "INSERT INTO scores (user, score) VALUES (?, ?)", (user, score)
        )
        self.conn.commit()

    def get_scores(self):
        self.cursor.execute("SELECT * FROM scores ORDER BY score DESC")
        return self.cursor.fetchall()
