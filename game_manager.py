"""
Bot Mesh - Game Manager
Created by: Abeer Aldosari © 2025
"""


class GameManager:
    """مدير الألعاب والمستخدمين"""
    
    def __init__(self):
        self.users = set()  # المستخدمين المسجلين
        self.games = {}     # الألعاب النشطة {group_id: {game, type}}
    
    def register(self, uid):
        """تسجيل مستخدم"""
        self.users.add(uid)
    
    def unregister(self, uid):
        """إلغاء تسجيل مستخدم"""
        self.users.discard(uid)
    
    def is_registered(self, uid):
        """التحقق من تسجيل المستخدم"""
        return uid in self.users
    
    def start_game(self, gid, game, gtype):
        """بدء لعبة جديدة"""
        self.games[gid] = {
            'game': game,
            'type': gtype
        }
    
    def get_game(self, gid):
        """الحصول على اللعبة النشطة"""
        return self.games.get(gid)
    
    def end_game(self, gid):
        """إنهاء اللعبة"""
        return self.games.pop(gid, None)
    
    def get_active_games_count(self):
        """عدد الألعاب النشطة"""
        return len(self.games)
    
    def get_users_count(self):
        """عدد المستخدمين المسجلين"""
        return len(self.users)
