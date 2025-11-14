import sqlite3
import logging
from datetime import datetime
from contextlib import contextmanager

logger = logging.getLogger(__name__)

DATABASE_NAME = 'game_scores.db'

@contextmanager
def get_db_connection():
    """الحصول على اتصال قاعدة البيانات بشكل آمن"""
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_NAME, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        yield conn
    except Exception as e:
        logger.error(f"❌ خطأ في الاتصال بقاعدة البيانات: {e}", exc_info=True)
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            conn.close()

def init_db():
    """تهيئة قاعدة البيانات"""
    try:
        with get_db_connection() as conn:
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
            
            # جدول سجل الألعاب
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
            
            # إنشاء الفهارس
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_user_points 
                ON users(total_points DESC)
            ''')
            
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_game_history_user 
                ON game_history(user_id, played_at DESC)
            ''')
            
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_game_history_type 
                ON game_history(game_type, played_at DESC)
            ''')
            
            conn.commit()
            logger.info("✅ تم تهيئة قاعدة البيانات بنجاح")
            
    except Exception as e:
        logger.error(f"❌ خطأ في تهيئة قاعدة البيانات: {e}", exc_info=True)

def update_user_points(user_id, display_name, points, won, game_type):
    """تحديث نقاط المستخدم"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # التحقق من وجود المستخدم
            cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
            user = cursor.fetchone()
            
            if user:
                # تحديث المستخدم الموجود
                cursor.execute('''
                    UPDATE users 
                    SET display_name = ?,
                        total_points = total_points + ?,
                        games_played = games_played + 1,
                        wins = wins + ?,
                        last_played = ?
                    WHERE user_id = ?
                ''', (display_name, points, 1 if won else 0, datetime.now(), user_id))
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
            logger.info(f"✅ تم تحديث نقاط {display_name}: +{points} ({game_type})")
            
    except Exception as e:
        logger.error(f"❌ خطأ في تحديث النقاط: {e}", exc_info=True)

def get_user_stats(user_id):
    """الحصول على إحصائيات المستخدم"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT total_points, games_played, wins, last_played, registered_at
                FROM users 
                WHERE user_id = ?
            ''', (user_id,))
            
            result = cursor.fetchone()
            
            if result:
                return {
                    'total_points': result['total_points'],
                    'games_played': result['games_played'],
                    'wins': result['wins'],
                    'last_played': result['last_played'],
                    'registered_at': result['registered_at']
                }
            
            return None
            
    except Exception as e:
        logger.error(f"❌ خطأ في جلب الإحصائيات: {e}", exc_info=True)
        return None

def get_leaderboard(limit=10):
    """الحصول على لوحة الصدارة"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT user_id, display_name, total_points, games_played, wins
                FROM users 
                ORDER BY total_points DESC, wins DESC
                LIMIT ?
            ''', (limit,))
            
            results = cursor.fetchall()
            
            return [dict(row) for row in results]
            
    except Exception as e:
        logger.error(f"❌ خطأ في جلب لوحة الصدارة: {e}", exc_info=True)
        return []

def get_game_history(user_id, limit=10):
    """الحصول على سجل ألعاب المستخدم"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT game_type, points, won, played_at
                FROM game_history 
                WHERE user_id = ?
                ORDER BY played_at DESC
                LIMIT ?
            ''', (user_id, limit))
            
            results = cursor.fetchall()
            
            return [dict(row) for row in results]
            
    except Exception as e:
        logger.error(f"❌ خطأ في جلب سجل الألعاب: {e}", exc_info=True)
        return []

def get_game_stats(game_type):
    """الحصول على إحصائيات لعبة معينة"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT 
                    COUNT(*) as total_games,
                    SUM(points) as total_points,
                    AVG(points) as avg_points,
                    COUNT(CASE WHEN won = 1 THEN 1 END) as total_wins
                FROM game_history 
                WHERE game_type = ?
            ''', (game_type,))
            
            result = cursor.fetchone()
            
            if result:
                return dict(result)
            
            return None
            
    except Exception as e:
        logger.error(f"❌ خطأ في جلب إحصائيات اللعبة: {e}", exc_info=True)
        return None

def get_user_rank(user_id):
    """الحصول على ترتيب المستخدم"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT COUNT(*) + 1 as rank
                FROM users 
                WHERE total_points > (
                    SELECT total_points 
                    FROM users 
                    WHERE user_id = ?
                )
            ''', (user_id,))
            
            result = cursor.fetchone()
            
            if result:
                return result['rank']
            
            return None
            
    except Exception as e:
        logger.error(f"❌ خطأ في جلب ترتيب المستخدم: {e}", exc_info=True)
        return None

def get_total_users():
    """الحصول على إجمالي عدد المستخدمين"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('SELECT COUNT(*) as total FROM users')
            result = cursor.fetchone()
            
            return result['total'] if result else 0
            
    except Exception as e:
        logger.error(f"❌ خطأ في جلب عدد المستخدمين: {e}", exc_info=True)
        return 0

def get_total_games_played():
    """الحصول على إجمالي عدد الألعاب"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('SELECT COUNT(*) as total FROM game_history')
            result = cursor.fetchone()
            
            return result['total'] if result else 0
            
    except Exception as e:
        logger.error(f"❌ خطأ في جلب عدد الألعاب: {e}", exc_info=True)
        return 0

def delete_user_data(user_id):
    """حذف بيانات المستخدم (للخصوصية)"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # حذف سجل الألعاب
            cursor.execute('DELETE FROM game_history WHERE user_id = ?', (user_id,))
            
            # حذف المستخدم
            cursor.execute('DELETE FROM users WHERE user_id = ?', (user_id,))
            
            conn.commit()
            logger.info(f"🗑️ تم حذف بيانات المستخدم: {user_id}")
            return True
            
    except Exception as e:
        logger.error(f"❌ خطأ في حذف بيانات المستخدم: {e}", exc_info=True)
        return False

def reset_user_stats(user_id):
    """إعادة تعيين إحصائيات المستخدم"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE users 
                SET total_points = 0,
                    games_played = 0,
                    wins = 0
                WHERE user_id = ?
            ''', (user_id,))
            
            conn.commit()
            logger.info(f"🔄 تم إعادة تعيين إحصائيات المستخدم: {user_id}")
            return True
            
    except Exception as e:
        logger.error(f"❌ خطأ في إعادة تعيين الإحصائيات: {e}", exc_info=True)
        return False

def backup_database(backup_path='game_scores_backup.db'):
    """نسخ احتياطي لقاعدة البيانات"""
    try:
        import shutil
        shutil.copy2(DATABASE_NAME, backup_path)
        logger.info(f"💾 تم إنشاء نسخة احتياطية: {backup_path}")
        return True
    except Exception as e:
        logger.error(f"❌ خطأ في النسخ الاحتياطي: {e}", exc_info=True)
        return False
