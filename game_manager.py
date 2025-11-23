"""
Bot Mesh - Game Manager
"""
class GameManager:
    def __init__(self):
        self.active_games = {}  # gid: {"game": game_obj, "type": name}
        self.registered_users = set()
        self.answered_users = {}

    def register(self, uid):
        self.registered_users.add(uid)

    def unregister(self, uid):
        self.registered_users.discard(uid)
        for gid in self.answered_users:
            self.answered_users[gid].discard(uid)

    def is_registered(self, uid):
        return uid in self.registered_users

    def start_game(self, gid, game, game_type):
        self.active_games[gid] = {"game": game, "type": game_type}
        self.answered_users[gid] = set()

    def get_game(self, gid):
        return self.active_games.get(gid)

    def end_game(self, gid):
        self.active_games.pop(gid, None)
        self.answered_users.pop(gid, None)

    def has_answered(self, gid, uid):
        return uid in self.answered_users.get(gid, set())

    def mark_answered(self, gid, uid):
        if gid in self.answered_users:
            self.answered_users[gid].add(uid)

    def get_users_count(self):
        return len(self.registered_users)

    def get_active_games_count(self):
        return len(self.active_games)
