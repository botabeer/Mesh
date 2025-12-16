import logging
from threading import Lock
from config import Config

logger = logging.getLogger(__name__)


class GameManager:
    """مدير الألعاب - نسخة مستقرة"""

    def __init__(self, db):
        self.db = db
        self._lock = Lock()
        self._active = {}
        self._games = self._load_games()
        logger.info(f"GameManager loaded {len(self._games)} games")

    # ================= Load =================

    def _load_games(self):
        games = {}

        game_mappings = {
            "ذكاء": ("games.iq", "IqGame"),
            "خمن": ("games.guess", "GuessGame"),
            "رياضيات": ("games.math", "MathGame"),
            "ترتيب": ("games.scramble", "ScrambleGame"),
            "ضد": ("games.opposite", "OppositeGame"),
            "اسرع": ("games.fast_typing", "FastTypingGame"),
            "سلسله": ("games.chain_words", "ChainWordsGame"),
            "انسان حيوان": ("games.human_animal", "HumanAnimalGame"),
            "كون كلمات": ("games.letters_words", "LettersWordsGame"),
            "اغاني": ("games.song", "SongGame"),
            "الوان": ("games.word_color", "WordColorGame"),
            "توافق": ("games.compatibility", "CompatibilityGame"),
            "مافيا": ("games.mafia", "MafiaGame"),
        }

        for name, (path, cls) in game_mappings.items():
            try:
                module = __import__(path, fromlist=[cls])
                game_class = getattr(module, cls)

                instance = game_class(self.db, "light")
                if not hasattr(instance, "start"):
                    raise AttributeError("Missing start()")

                games[name] = game_class
                logger.info(f"✓ Loaded game: {name}")

            except Exception as e:
                logger.error(f"✗ Failed loading {name}: {e}")

        return games

    # ================= Public =================

    def handle(self, user_id: str, cmd: str, theme: str, raw_text: str):
        user = self.db.get_user(user_id)

        normalized_cmd = Config.normalize(cmd)

        # بدء لعبة بدون تسجيل (توافق / مافيا)
        if not user and normalized_cmd in self._games:
            return self._start_game(user_id, normalized_cmd, theme)

        with self._lock:
            game = self._active.get(user_id)

        if game:
            return self._handle_answer(user_id, raw_text)

        if normalized_cmd in self._games:
            return self._start_game(user_id, normalized_cmd, theme)

        return None

    def stop_game(self, user_id: str) -> bool:
        with self._lock:
            game = self._active.pop(user_id, None)

        if not game:
            return False

        try:
            self.db.save_game_progress(user_id, {
                "game": getattr(game, "game_name", ""),
                "score": getattr(game, "score", 0),
                "current_q": getattr(game, "current_q", 0),
            })

            if hasattr(game, "on_stop"):
                game.on_stop(user_id)

        except Exception as e:
            logger.error(f"Stop error: {e}")

        logger.info(f"Game stopped for {user_id}")
        return True

    # ================= Internal =================

    def _start_game(self, user_id: str, game_name: str, theme: str):
        try:
            GameClass = self._games[game_name]
            game = GameClass(self.db, theme)
            game.game_name = game_name

            progress = self.db.get_game_progress(user_id)
            if progress and progress.get("game") == game_name:
                if hasattr(game, "restore"):
                    game.restore(progress)

            with self._lock:
                self._active[user_id] = game

            response = game.start(user_id)
            return self._safe_response(response)

        except Exception as e:
            logger.exception(f"Start game error [{game_name}]: {e}")
            with self._lock:
                self._active.pop(user_id, None)
            return None

    def _handle_answer(self, user_id: str, raw_answer: str):
        with self._lock:
            game = self._active.get(user_id)

        if not game:
            return None

        try:
            result = game.check(raw_answer, user_id)

            if not isinstance(result, dict):
                return None

            if result.get("game_over"):
                with self._lock:
                    self._active.pop(user_id, None)

                won = result.get("won", False)
                self.db.finish_game(user_id, won)
                self.db.clear_game_progress(user_id)

            return self._safe_response(result.get("response"))

        except Exception as e:
            logger.exception(f"Answer error: {e}")
            with self._lock:
                self._active.pop(user_id, None)
            return None

    # ================= Safety =================

    def _safe_response(self, response):
        if not response:
            return None

        if isinstance(response, list):
            return [r for r in response if r]

        return response
