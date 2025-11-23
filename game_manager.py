"""
Bot Mesh - Game Manager
Created by: Abeer Aldosari © 2025
"""
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class GameManager:
    def __init__(self):
        self.active_games = {}  # gid: {"game": game_obj, "type": name, "started_at": timestamp}
        self.registered_users = set()
        self.answered_users = {}  # gid: {uid: answer_count}
        logger.info("✅ GameManager initialized")

    def register(self, uid):
        """تسجيل لاعب جديد"""
        self.registered_users.add(uid)
        logger.info(f"✅ User registered: {uid}")
        return True

    def unregister(self, uid):
        """إلغاء تسجيل لاعب"""
        self.registered_users.discard(uid)
        # حذف إجاباته من جميع الألعاب
        for gid in list(self.answered_users.keys()):
            if uid in self.answered_users[gid]:
                del self.answered_users[gid][uid]
        logger.info(f"✅ User unregistered: {uid}")
        return True

    def is_registered(self, uid):
        """التحقق من تسجيل اللاعب"""
        return uid in self.registered_users

    def start_game(self, gid, game, game_type):
        """بدء لعبة جديدة"""
        self.active_games[gid] = {
            "game": game,
            "type": game_type,
            "started_at": datetime.now()
        }
        self.answered_users[gid] = {}
        logger.info(f"✅ Game started: {game_type} in {gid}")
        return True

    def get_game(self, gid):
        """الحصول على اللعبة النشطة"""
        game_data = self.active_games.get(gid)
        if game_data:
            # التحقق من انتهاء وقت اللعبة (5 دقائق)
            time_limit = timedelta(minutes=5)
            if datetime.now() - game_data['started_at'] > time_limit:
                logger.warning(f"⚠️ Game timeout in {gid}")
                self.end_game(gid)
                return None
        return game_data

    def end_game(self, gid):
        """إنهاء اللعبة"""
        game_data = self.active_games.pop(gid, None)
        self.answered_users.pop(gid, None)
        if game_data:
            logger.info(f"✅ Game ended: {game_data['type']} in {gid}")
            return True
        return False

    def has_answered(self, gid, uid):
        """التحقق من إجابة اللاعب"""
        if gid not in self.answered_users:
            return False
        return uid in self.answered_users[gid]

    def mark_answered(self, gid, uid):
        """تسجيل إجابة اللاعب"""
        if gid not in self.answered_users:
            self.answered_users[gid] = {}
        
        if uid not in self.answered_users[gid]:
            self.answered_users[gid][uid] = 0
        
        self.answered_users[gid][uid] += 1
        logger.debug(f"✅ Answer marked for {uid} in {gid}")
        return True

    def get_answer_count(self, gid, uid):
        """الحصول على عدد إجابات اللاعب"""
        if gid not in self.answered_users:
            return 0
        return self.answered_users[gid].get(uid, 0)

    def get_users_count(self):
        """عدد اللاعبين المسجلين"""
        return len(self.registered_users)

    def get_active_games_count(self):
        """عدد الألعاب النشطة"""
        return len(self.active_games)

    def get_game_players(self, gid):
        """الحصول على لاعبي اللعبة"""
        if gid not in self.answered_users:
            return []
        return list(self.answered_users[gid].keys())

    def reset_game_answers(self, gid):
        """إعادة تعيين إجابات اللعبة"""
        if gid in self.answered_users:
            self.answered_users[gid] = {}
            logger.info(f"✅ Answers reset for game in {gid}")
            return True
        return False

    def get_stats(self):
        """إحصائيات المدير"""
        return {
            'registered_users': len(self.registered_users),
            'active_games': len(self.active_games),
            'total_answers': sum(len(answers) for answers in self.answered_users.values())
        }

    def cleanup_old_games(self):
        """تنظيف الألعاب القديمة"""
        time_limit = timedelta(minutes=5)
        now = datetime.now()
        cleaned = 0
        
        for gid in list(self.active_games.keys()):
            game_data = self.active_games[gid]
            if now - game_data['started_at'] > time_limit:
                self.end_game(gid)
                cleaned += 1
        
        if cleaned > 0:
            logger.info(f"✅ Cleaned up {cleaned} old games")
        
        return cleaned
