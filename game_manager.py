import time

class GameManager:
    def __init__(self):
        self.active_games = {}  # gid: {'game': obj, 'type': str, 'answered_users': []}
        self.registered_users = {}  # uid: {'name': str, 'joined_at': timestamp}
        self.ignored_users = set()

    # -------- تسجيل المستخدم --------
    def register(self, uid, name):
        self.registered_users[uid] = {'name': name, 'joined_at': time.time()}
        if uid in self.ignored_users:
            self.ignored_users.remove(uid)

    def unregister(self, uid):
        """انسحب المستخدم"""
        if uid in self.registered_users:
            del self.registered_users[uid]
        self.ignored_users.add(uid)

    def is_registered(self, uid):
        return uid in self.registered_users

    def should_ignore(self, uid):
        return uid in self.ignored_users

    # -------- إدارة الألعاب --------
    def start_game(self, gid, game, game_type):
        self.active_games[gid] = {'game': game, 'type': game_type, 'answered_users': set()}

    def get_game(self, gid):
        return self.active_games.get(gid)

    def end_game(self, gid):
        if gid in self.active_games:
            del self.active_games[gid]

    def has_answered(self, gid, uid):
        game_data = self.get_game(gid)
        return uid in game_data['answered_users'] if game_data else False

    def mark_answered(self, gid, uid):
        game_data = self.get_game(gid)
        if game_data:
            game_data['answered_users'].add(uid)

    # -------- تنظيف البيانات --------
    def cleanup_users(self):
        now = time.time()
        expired = [uid for uid, u in self.registered_users.items() if now - u['joined_at'] > 7*24*3600]
        for uid in expired:
            del self.registered_users[uid]
