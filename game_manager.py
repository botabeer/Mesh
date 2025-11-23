"""
Bot Mesh - Game Manager
"""
class GameManager:
    def __init__(self):
        self.active_games = {}   # gid -> {'game': GameObject, 'type': 'ذكاء'}
        self.user_answers = {}   # gid -> set(uid)

    def register(self, uid):
        # placeholder: maybe track users for statistics
        pass

    def remove_user(self, uid):
        for gid in list(self.active_games.keys()):
            self.user_answers.get(gid,set()).discard(uid)

    def get_game(self, gid):
        return self.active_games.get(gid)

    def start_game(self, gid, game, game_type):
        self.active_games[gid] = {'game': game, 'type': game_type}
        self.user_answers[gid] = set()

    def end_game(self, gid):
        self.active_games.pop(gid, None)
        self.user_answers.pop(gid, None)

    def has_answered(self, gid, uid):
        return uid in self.user_answers.get(gid,set())

    def mark_answered(self, gid, uid):
        if gid not in self.user_answers:
            self.user_answers[gid] = set()
        self.user_answers[gid].add(uid)

    def is_registered(self, uid):
        # placeholder: we only allow registered users to play
        return True

    def get_users_count(self):
        return sum(len(u) for u in self.user_answers.values())

    def get_active_games_count(self):
        return len(self.active_games)
