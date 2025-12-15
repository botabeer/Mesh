import logging
from threading import Lock
from linebot.v3.messaging import TextMessage

logger = logging.getLogger(__name__)


class GameManager:
    """مدير الألعاب - Thread-safe + LINE SDK v3 safe"""

    def __init__(self, db):
        self.db = db
        self._lock = Lock()
        self._active = {}
        self._games = self._load_games()
        logger.info(f"GameManager initialized with {len(self._games)} games")

    # ---------------- Load Games ----------------

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

    # ---------------- Public API ----------------

    def handle(self, user_id: str, cmd: str, theme: str):
        """
        يعالج الأمر ويرجع:
        - TextMessage / FlexMessage
        - أو None
        """
        with self._lock:
            game = self._active.get(user_id)

        if game:
            return self._handle_answer(user_id, cmd)

        if cmd in self._games:
            return self._start_game(user_id, cmd, theme)

        return None

    def stop_game(self, user_id: str) -> bool:
        """إيقاف لعبة يدوية"""
        with self._lock:
            return self._active.pop(user_id, None) is not None

    def count_active(self) -> int:
        """عدد الألعاب النشطة"""
        with self._lock:
            return len(self._active)

    # ---------------- Internal ----------------

    def _start_game(self, user_id: str, game_name: str, theme: str):
        try:
            GameClass = self._games[game_name]
            game = GameClass(self.db, theme)

            with self._lock:
                self._active[user_id] = game

            logger.info(f"Started game [{game_name}] for {user_id}")
            response = game.start(user_id)

            return self._normalize_response(response)

        except Exception:
            logger.exception("Start game error")
            with self._lock:
                self._active.pop(user_id, None)

            return TextMessage(text="❌ فشل بدء اللعبة")

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

            return self._normalize_response(result.get("response"))

        except Exception:
            logger.exception("Handle answer error")
            with self._lock:
                self._active.pop(user_id, None)

            return TextMessage(text="⚠️ حدث خطأ أثناء اللعبة")

    # ---------------- Utils ----------------

    def _normalize_response(self, response):
        """
        يضمن أن الناتج صالح للإرسال عبر LINE
        """
        if response is None:
            return None

        if isinstance(response, TextMessage):
            return response

        # لو اللعبة رجعت نص فقط
        if isinstance(response, str):
            return TextMessage(text=response)

        logger.warning(f"Invalid game response type: {type(response)}")
        return TextMessage(text="⚠️ استجابة غير صالحة من اللعبة")
