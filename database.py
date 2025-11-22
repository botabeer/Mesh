"""
Bot Mesh - Database
Created by: Abeer Aldosari © 2025
"""
import sqlite3
import os
import logging
from datetime import datetime
from typing import Optional, List
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class User:
    user_id: str
    display_name: str
    total_points: int = 0
    games_played: int = 0
    wins: int = 0
    theme: str = "white"


class Database:
    def __init__(self, db_path: str = "data", db_name: str = "game_scores.db"):
        self.path = os.path.join(db_path, db_name)
        self._init = False
    
    async def initialize(self):
        if self._init:
            return
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        
        conn = sqlite3.connect(self.path)
        c = conn.cursor()
        
        c.execute('''CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            display_name TEXT NOT NULL,
            total_points INTEGER DEFAULT 0,
            games_played INTEGER DEFAULT 0,
            wins INTEGER DEFAULT 0,
            theme TEXT DEFAULT 'white',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT, game_type TEXT, points INTEGER,
            won INTEGER, played_at TEXT DEFAULT CURRENT_TIMESTAMP
        )''')
        
        conn.commit()
        conn.close()
        self._init = True
        logger.info(f"✅ DB: {self.path}")
    
    def _conn(self):
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        return conn
    
    async def get_user(self, uid: str) -> Optional[User]:
        conn = self._conn()
        r = conn.execute('SELECT * FROM users WHERE user_id=?', (uid,)).fetchone()
        conn.close()
        if r:
            return User(r['user_id'], r['display_name'], r['total_points'],
                       r['games_played'], r['wins'], r['theme'] or 'white')
        return None
    
    async def update_user_score(self, uid: str, name: str, pts: int,
                                won: bool = False, gtype: str = None):
        conn = self._conn()
        c = conn.cursor()
        now = datetime.now().isoformat()
        
        exists = c.execute('SELECT 1 FROM users WHERE user_id=?', (uid,)).fetchone()
        
        if exists:
            c.execute('''UPDATE users SET total_points=total_points+?,
                games_played=games_played+1, wins=wins+?, display_name=?
                WHERE user_id=?''', (pts, 1 if won else 0, name, uid))
        else:
            c.execute('''INSERT INTO users (user_id,display_name,total_points,
                games_played,wins,created_at) VALUES (?,?,?,1,?,?)''',
                (uid, name, pts, 1 if won else 0, now))
        
        if gtype:
            c.execute('INSERT INTO history (user_id,game_type,points,won) VALUES (?,?,?,?)',
                (uid, gtype, pts, 1 if won else 0))
        
        conn.commit()
        conn.close()
    
    async def get_leaderboard(self, limit: int = 10) -> List[User]:
        conn = self._conn()
        rows = conn.execute('SELECT * FROM users ORDER BY total_points DESC LIMIT ?',
            (limit,)).fetchall()
        conn.close()
        return [User(r['user_id'], r['display_name'], r['total_points'],
                    r['games_played'], r['wins'], r['theme'] or 'white') for r in rows]
    
    async def get_user_rank(self, uid: str) -> int:
        conn = self._conn()
        r = conn.execute('''SELECT COUNT(*)+1 as rank FROM users WHERE total_points >
            (SELECT COALESCE(total_points,0) FROM users WHERE user_id=?)''', (uid,)).fetchone()
        conn.close()
        return r['rank'] if r else 0
