import logging
from threading import Lock
from datetime import datetime

from config import Config
from ui import UI

logger = logging.getLogger(__name__)


class GameManager:
    MAX_ROUNDS = 5

    def __init__(self, db, theme="light"):
        self.db = db
        self.theme = theme
        self.ui = UI(theme)

        self._lock = Lock()
        self._active = {}
        self._games = self._load_games()

        logger.info(f"GameManager loaded {len(self._games)} games")

    # ================= Load =================

    def _load_games(self):
        games = {}

        game_map = {
            "ذكاء": ("games.iq", "IqGame"),
            "خمن": ("games.guess", "GuessGame"),
            "رياضيات": ("games.math", "MathGame"),
            "ترتيب": ("games.scramble", "ScrambleGame"),
            "ضد": ("games.opposite", "OppositeGame"),
            "اسرع": ("games.fast_typing", "FastTypingGame"),
            "سلسله": ("games.chain_words", "ChainWordsGame"),
            "انسان حيوان": ("games.human_animal", "HumanAnimalGame"),
            "تكوين": ("games.letters_words", "LettersWordsGame"),
            "اغاني": ("games.song", "SongGame"),
            "الوان": ("games.word_color", "WordColorGame"),
            "توافق": ("games.compatibility", "CompatibilityGame"),
            "مافيا": ("games.mafia", "MafiaGame"),
        }

        for name, (path, cls_name) in game_map.items():
            try:
                module = __import__(path, fromlist=[cls_name])
                game_cls = getattr(module, cls_name)

                instance = game_cls(self.db, self.theme)
                if not hasattr(instance, "start"):
                    raise AttributeError("Missing start()")

                games[name] = game_cls
                logger.info(f"Loaded game: {name}")

            except Exception as e:
                logger.error(f"Failed loading {name}: {e}")

        return games

    # ================= Public =================

    def handle(self, user_id, cmd, raw_text, theme="light"):
        cmd = Config.normalize(cmd)

        if self.db.is_ignored(user_id):
            if cmd not in Config.RESERVED_COMMANDS:
                return None

        if cmd in self._games:
            return self._start_game(user_id, cmd, theme)

        with self._lock:
            state = self._active.get(user_id)

        if state:
            return self._handle_answer(user_id, raw_text)

        return None

    def stop_game(self, user_id):
        with self._lock:
            state = self._active.pop(user_id, None)

        if not state:
            return False

        try:
            game = state["game"]
            self.db.save_game_progress(user_id, {
                "game": getattr(game, "game_name", ""),
                "score": state.get("score", 0),
                "round": state.get("round", 0)
            })

            if hasattr(game, "on_stop"):
                game.on_stop(user_id)

        except Exception as e:
            logger.error(f"Stop error: {e}")

        return True

    def count_active(self):
        with self._lock:
            return len(self._active)

    # ================= Internal =================

    def _start_game(self, user_id, game_name, theme):
        try:
            GameClass = self._games[game_name]
            game = GameClass(self.db, theme)

            game.game_name = game_name
            game.total_q = self.MAX_ROUNDS

            progress = self.db.get_game_progress(user_id)
            if progress and progress.get("game") == game_name:
                if hasattr(game, "restore"):
                    game.restore(progress)

            state = {
                "game": game,
                "start_time": datetime.now()
            }

            if not hasattr(game, "is_group_game"):
                state.update({"round": 0, "score": 0})

            with self._lock:
                self._active[user_id] = state

            return game.start(user_id)

        except Exception as e:
            logger.exception(f"Start game error [{game_name}]: {e}")
            with self._lock:
                self._active.pop(user_id, None)
            return None

    def _handle_answer(self, user_id, text):
        with self._lock:
            state = self._active.get(user_id)
            if not state:
                return None

            game = state["game"]

        try:
            result = game.check(text, user_id)
            if not result:
                return None

            if result.get("game_over"):
                with self._lock:
                    self._active.pop(user_id, None)
                self.db.clear_game_progress(user_id)
                return result.get("response")

            return result.get("response")

        except Exception as e:
            logger.exception(f"Answer error: {e}")
            with self._lock:
                self._active.pop(user_id, None)
            return None
