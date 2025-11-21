"""
database.py - إدارة قاعدة البيانات
"""

import sqlite3
from datetime import datetime
from config import Config
import os

class Database:
    """إدارة قاعدة البيانات"""
    
    def __init__(self, db_name=None):
        self.db_name = db_name or Config.DB_NAME
        self._ensure_data_dir()
        self._init_db()
    
    def _ensure_data_dir(self):
        """التأكد من وجود مجلد البيانات"""
        os.makedirs(os.path.dirname(self.db_name), exist_ok=True)
    
    def _get_connection(self):
        """الحصول على اتصال"""
        return sqlite3.connect(self.db_name)
    
    def _init_db(self):
        """إنشاء الجداول"""
        conn = self._get_connection()
        c = conn.cursor()
        
        # جدول المستخدمين
        c.execute('''CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            display_name TEXT,
            total_points INTEGER DEFAULT 0,
            games_played INTEGER DEFAULT 0,
            wins INTEGER DEFAULT 0,
            last_played TEXT,
            created_at TEXT
        )''')
        
        # جدول سجل الألعاب
        c.execute('''CREATE TABLE IF NOT EXISTS game_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            game_type TEXT,
            points INTEGER,
            won INTEGER,
            played_at TEXT,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )''')
        
        # جدول الإنجازات
        c.execute('''CREATE TABLE IF NOT EXISTS achievements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            achievement_type TEXT,
            achieved_at TEXT,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )''')
        
        conn.commit()
        conn.close()
    
    def update_user_score(self, user_id, display_name, points, won=False, game_type=None):
        """تحديث نقاط المستخدم"""
        conn = self._get_connection()
        c = conn.cursor()
        now = datetime.now().isoformat()
        
        c.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        user = c.fetchone()
        
        if user:
            new_points = user[2] + points
            new_games = user[3] + 1
            new_wins = user[4] + (1 if won else 0)
            c.execute('''UPDATE users SET 
                total_points = ?, games_played = ?, wins = ?, 
                last_played = ?, display_name = ?
                WHERE user_id = ?''',
                (new_points, new_games, new_wins, now, display_name, user_id))
        else:
            c.execute('''INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?)''',
                (user_id, display_name, points, 1, 1 if won else 0, now, now))
        
        # تسجيل في السجل
        if game_type:
            c.execute('''INSERT INTO game_history (user_id, game_type, points, won, played_at)
                VALUES (?, ?, ?, ?, ?)''', (user_id, game_type, points, 1 if won else 0, now))
        
        conn.commit()
        conn.close()
    
    def get_user(self, user_id):
        """الحصول على بيانات مستخدم"""
        conn = self._get_connection()
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        user = c.fetchone()
        conn.close()
        
        if user:
            return {
                'user_id': user[0], 'display_name': user[1],
                'total_points': user[2], 'games_played': user[3],
                'wins': user[4], 'last_played': user[5]
            }
        return None
    
    def get_leaderboard(self, limit=5):
        """لوحة الصدارة"""
        conn = self._get_connection()
        c = conn.cursor()
        c.execute('''SELECT display_name, total_points FROM users 
            ORDER BY total_points DESC LIMIT ?''', (limit,))
        leaders = c.fetchall()
        conn.close()
        return leaders
    
    def get_user_rank(self, user_id):
        """ترتيب المستخدم"""
        conn = self._get_connection()
        c = conn.cursor()
        c.execute('''SELECT COUNT(*) + 1 FROM users WHERE total_points > 
            (SELECT total_points FROM users WHERE user_id = ?)''', (user_id,))
        rank = c.fetchone()[0]
        conn.close()
        return rank
    
    def add_achievement(self, user_id, achievement_type):
        """إضافة إنجاز"""
        conn = self._get_connection()
        c = conn.cursor()
        c.execute('''INSERT INTO achievements (user_id, achievement_type, achieved_at)
            VALUES (?, ?, ?)''', (user_id, achievement_type, datetime.now().isoformat()))
        conn.commit()
        conn.close()
    
    def get_user_achievements(self, user_id):
        """إنجازات المستخدم"""
        conn = self._get_connection()
        c = conn.cursor()
        c.execute('SELECT achievement_type, achieved_at FROM achievements WHERE user_id = ?', (user_id,))
        achievements = c.fetchall()
        conn.close()
        return achievements
