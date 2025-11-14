import sqlite3
from datetime import datetime
import threading

# قفل لضمان أمان العمليات
db_lock = threading.Lock()
DB_NAME = 'game_scores.db'

def get_connection():
    """إنشاء اتصال بقاعدة البيانات"""
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """تهيئة قاعدة البيانات"""
    with db_lock:
        conn = get_connection()
        cursor = conn.cursor()
        
        # جدول المستخدمين
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                display_name TEXT NOT NULL,
                total_points INTEGER DEFAULT 0,
                games_played INTEGER DEFAULT 0,
                wins INTEGER DEFAULT 0,
                last_played TIMESTAMP,
                registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # جدول تاريخ الألعاب
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS game_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                game_type TEXT NOT NULL,
                points INTEGER NOT NULL,
                won BOOLEAN NOT NULL,
                played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')
        
        # فهارس للأداء
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_user_points 
            ON users(total_points DESC)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_game_history_user 
            ON game_history(user_id, played_at DESC)
        ''')
        
        conn.commit()
        conn.close()

def update_user_points(user_id, display_name, points, won, game_type):
    """تحديث نقاط المستخدم"""
    with db_lock:
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            # التحقق من وجود المستخدم
            cursor.execute('SELECT user_id FROM users WHERE user_id = ?', (user_id,))
            exists = cursor.fetchone()
            
            if exists:
                # تحديث المستخدم الموجود
                cursor.execute('''
                    UPDATE users 
                    SET total_points = total_points + ?,
                        games_played = games_played + 1,
                        wins = wins + ?,
                        last_played = ?,
                        display_name = ?
                    WHERE user_id = ?
                ''', (points, 1 if won else 0, datetime.now(), display_name, user_id))
            else:
                # إضافة مستخدم جديد
                cursor.execute('''
                    INSERT INTO users (user_id, display_name, total_points, games_played, wins, last_played)
                    VALUES (?, ?, ?, 1, ?, ?)
                ''', (user_id, display_name, points, 1 if won else 0, datetime.now()))
            
            # إضافة سجل اللعبة
            cursor.execute('''
                INSERT INTO game_history (user_id, game_type, points, won)
                VALUES (?, ?, ?, ?)
            ''', (user_id, game_type, points, won))
            
            conn.commit()
        
        except Exception as e:
            print(f"❌ خطأ في تحديث النقاط: {e}")
            conn.rollback()
        
        finally:
            conn.close()

def get_user_stats(user_id):
    """الحصول على إحصائيات المستخدم"""
    with db_lock:
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT total_points, games_played, wins, last_played, registered_at
                FROM users
                WHERE user_id = ?
            ''', (user_id,))
            
            row = cursor.fetchone()
            
            if row:
                return {
                    'total_points': row['total_points'],
                    'games_played': row['games_played'],
                    'wins': row['wins'],
                    'last_played': row['last_played'],
                    'registered_at': row['registered_at']
                }
            
            return None
        
        except Exception as e:
            print(f"❌ خطأ في جلب الإحصائيات: {e}")
            return None
        
        finally:
            conn.close()

def get_leaderboard(limit=10):
    """الحصول على لوحة الصدارة"""
    with db_lock:
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT user_id, display_name, total_points, games_played, wins
                FROM users
                ORDER BY total_points DESC, games_played ASC
                LIMIT ?
            ''', (limit,))
            
            rows = cursor.fetchall()
            
            return [dict(row) for row in rows]
        
        except Exception as e:
            print(f"❌ خطأ في جلب الصدارة: {e}")
            return []
        
        finally:
            conn.close()
