import logging
from threading import Lock
from linebot.v3.messaging import TextMessage

logger = logging.getLogger(__name__)


class GameManager:
    def __init__(self, db):
        self.db = db
        self._lock = Lock()
        self._active = {}
        self._games = self._load_games()
        logger.info(f"GameManager initialized with {len(self._games)} games")

    def _load_games(self):
        games = {}

        mappings = {
            "ذكاء": ("games.iq", "IqGame"),
            "خمن": ("games.guess", "GuessGame"),
            "رياضيات": ("games.math", "MathGame"),
        }

        for name, (module_path, class_name) in mappings.items():
            try:
                mod = __import__(module_path, fromlist=[class_name])
                game_class = getattr(mod, class_name)
                games[name] = game_class
                logger.info(f"Loaded game: {name}")
            except Exception:
                logger.exception(f"Failed to load game: {name}")

        return games

    def handle(self, user_id: str, cmd: str, theme: str):
        with self._lock:
            game = self._active.get(user_id)

        if game:
            return self._handle_answer(user_id, cmd)

        if cmd in self._games:
            return self._start_game(user_id, cmd, theme)

        return None

    def stop_game(self, user_id: str) -> bool:
        with self._lock:
            return self._active.pop(user_id, None) is not None

    def count_active(self) -> int:
        with self._lock:
            return len(self._active)

    def _start_game(self, user_id: str, game_name: str, theme: str):
        try:
            GameClass = self._games[game_name]
            game = GameClass(self.db, theme)

            with self._lock:
                self._active[user_id] = game

            logger.info(f"Started game [{game_name}] for {user_id}")
            result = game.start(user_id)

            if isinstance(result, dict) and "response" in result:
                return result["response"]
            return result

        except Exception:
            logger.exception("Start game error")
            with self._lock:
                self._active.pop(user_id, None)

            return TextMessage(text="فشل بدء اللعبه")

    def _handle_answer(self, user_id: str, answer: str):
        with self._lock:
            game = self._active.get(user_id)

        if not game:
            return None

        try:
            result = game.check(answer, user_id)

            if not result:
                return None

            if result.get("game_over"):
                with self._lock:
                    self._active.pop(user_id, None)

            return result.get("response")

        except Exception:
            logger.exception("Handle answer error")
            with self._lock:
                self._active.pop(user_id, None)

            return TextMessage(text="حدث خطا اثناء اللعبه")
