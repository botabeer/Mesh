"""
Bot Mesh - Database Manager
Created by: Abeer Aldosari © 2025
"""
import os
import sqlite3
from datetime import datetime


class DB:
    """مدير قاعدة البيانات"""
    
    def __init__(self, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.path = path
        self._init()
    
    def _init(self):
        """إنشاء الجداول"""
        conn = sqlite3.connect(self.path)
        
        # جدول المستخدمين
        conn.execute('''CREATE TABLE IF NOT EXISTS users (
            uid TEXT PRIMARY KEY,
            name TEXT,
            points INT DEFAULT 0,
            games INT DEFAULT 0,
            wins INT DEFAULT 0,
            theme TEXT DEFAULT 'white'
        )''')
        
        # جدول التاريخ
        conn.execute('''CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uid TEXT,
            game TEXT,
            points INT,
            won INT,
            time TEXT
        )''')
        
        conn.commit()
        conn.close()
    
    def get_user(self, uid):
        """الحصول على بيانات المستخدم"""
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        result = conn.execute('SELECT * FROM users WHERE uid=?', (uid,)).fetchone()
        conn.close()
        return dict(result) if result else None
    
    def update(self, uid, name, points, won, game):
        """تحديث بيانات المستخدم"""
        conn = sqlite3.connect(self.path)
        existing = conn.execute('SELECT 1 FROM users WHERE uid=?', (uid,)).fetchone()
        
        if existing:
            conn.execute(
                'UPDATE users SET points=points+?, games=games+1, wins=wins+?, name=? WHERE uid=?',
                (points, 1 if won else 0, name, uid)
            )
        else:
            conn.execute(
                'INSERT INTO users VALUES (?,?,?,1,?,?)',
                (uid, name, points, 1 if won else 0, 'white')
            )
        
        # حفظ في التاريخ
        conn.execute(
            'INSERT INTO history VALUES (NULL,?,?,?,?,?)',
            (uid, game, points, 1 if won else 0, datetime.now().isoformat())
        )
        
        conn.commit()
        conn.close()
    
    def leaderboard(self, limit=10):
        """لوحة الصدارة"""
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        results = conn.execute(
            'SELECT * FROM users ORDER BY points DESC LIMIT ?',
            (limit,)
        ).fetchall()
        conn.close()
        return [dict(r) for r in results]
    
    def rank(self, uid):
        """ترتيب المستخدم"""
        conn = sqlite3.connect(self.path)
        result = conn.execute('''
            SELECT COUNT(*)+1 FROM users 
            WHERE points > (SELECT COALESCE(points,0) FROM users WHERE uid=?)
        ''', (uid,)).fetchone()
        conn.close()
        return result[0] if result else 0
    
    def set_theme(self, uid, theme):
        """تغيير الثيم"""
        conn = sqlite3.connect(self.path)
        conn.execute('UPDATE users SET theme=? WHERE uid=?', (theme, uid))
        conn.commit()
        conn.close()
