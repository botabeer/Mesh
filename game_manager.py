import logging
from threading import Lock
from linebot.v3.messaging import TextMessage

logger = logging.getLogger(__name__)


class GameManager:
    """مدير الالعاب - Thread-safe"""

    def __init__(self, db):
        self.db = db
        self._lock = Lock()
        self._active = {}
        self._games = self._load_games()
        logger.info(f"Loaded {len(self._games)} games")

    def _load_games(self):
        games = {}
        mappings = {
            "ذكاء": ("games.iq", "IqGame"),
            "خمن": ("games.guess", "GuessGame"),
            "رياضيات": ("games.math", "MathGame"),
        }

        for name, (module, cls) in mappings.items():
            try:
                mod = __import__(module, fromlist=[cls])
                games[name] = getattr(mod, cls)
            except Exception as e:
                logger.error(f"Failed to load {name}: {e}")

        return games

    def handle(self, user_id: str, cmd: str, theme: str):
        # 1️⃣ تحقق سريع داخل القفل
        with self._lock:
            game = self._active.get(user_id)

        # 2️⃣ معالجة خارج القفل
        if game:
            return self._handle_answer(user_id, cmd)

        if cmd in self._games:
            return self._start_game(user_id, cmd, theme)

        return None

    def _start_game(self, user_id: str, game_name: str, theme: str):
        try:
            GameClass = self._games[game_name]
            game = GameClass(self.db, theme)

            with self._lock:
                self._active[user_id] = game

            result = game.start()
            logger.info(f"Started {game_name} for {user_id}")
            return result

        except Exception as e:
            logger.error(f"Start game error: {e}")
            return TextMessage(text="فشل بدء اللعبة")

    def _handle_answer(self, user_id: str, answer: str):
        with self._lock:
            game = self._active.get(user_id)

        if not game:
            return None

        try:
            result = game.check(answer, user_id)

            if result and result.get("game_over"):
                with self._lock:
                    self._active.pop(user_id, None)

            return result.get("response") if result else None

        except Exception as e:
            logger.error(f"Handle answer error: {e}")
            with self._lock:
                self._active.pop(user_id, None)
            return TextMessage(text="حدث خطأ في اللعبة")

    def stop_game(self, user_id: str) -> bool:
        with self._lock:
            return self._active.pop(user_id, None) is not None

    def count_active(self) -> int:
        with self._lock:
            return len(self._active)
