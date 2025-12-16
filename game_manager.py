import logging
from threading import Lock
from config import Config

logger = logging.getLogger(__name__)


class GameManager:
    def __init__(self, db):
        self.db = db
        self._lock = Lock()
        self._active = {}     # user_id -> game instance
        self._games = self._load_games()
        logger.info(f"GameManager initialized with {len(self._games)} games")

    # ===============================
    # Load Games
    # ===============================
    def _load_games(self):
        games = {}

        # تعريف الألعاب مع جميع الأسماء المحتملة
        mappings = {
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
            "مافيا": ("games.mafia", "MafiaGame"),
            "توافق": ("games.compatibility", "CompatibilityGame"),
        }

        for name, (module_path, class_name) in mappings.items():
            try:
                mod = __import__(module_path, fromlist=[class_name])
                games[name] = getattr(mod, class_name)
                logger.info(f"✓ Loaded game: {name}")
            except Exception as e:
                logger.error(f"✗ Failed to load {name}: {e}")

        return games

    # ===============================
    # Public API
    # ===============================
    def handle(self, user_id: str, cmd: str, theme: str, raw_text: str):
        user = self.db.get_user(user_id)
        if not user:
            return None

        with self._lock:
            game = self._active.get(user_id)

        # اللاعب داخل لعبة
        if game:
            return self._handle_answer(user_id, raw_text)

        # بدء لعبة جديدة - تحقق من الأوامر المطابقة
        logger.info(f"Checking game command: '{cmd}'")
        logger.info(f"Available games: {list(self._games.keys())}")
        
        if cmd in self._games:
            logger.info(f"Starting game: {cmd}")
            return self._start_game(user_id, cmd, theme)
        else:
            logger.warning(f"Game '{cmd}' not found in available games")

        return None

    def stop_game(self, user_id: str) -> bool:
        with self._lock:
            game = self._active.pop(user_id, None)

        if not game:
            return False

        # حفظ التقدم
        self.db.save_game_progress(user_id, {
            "game": getattr(game, 'game_name', 'unknown'),
            "score": getattr(game, "score", 0),
            "current_q": getattr(game, "current_q", 0),
        })

        # إبلاغ اللعبة أنها أُوقفت
        if hasattr(game, "on_stop"):
            try:
                game.on_stop(user_id)
            except Exception as e:
                logger.error(f"Error in game on_stop: {e}")

        logger.info(f"Game stopped for user {user_id}")
        return True

    def count_active(self) -> int:
        with self._lock:
            return len(self._active)

    def get_active_games(self):
        with self._lock:
            return {
                uid: type(game).__name__
                for uid, game in self._active.items()
            }

    # ===============================
    # Internal
    # ===============================
    def _start_game(self, user_id: str, game_name: str, theme: str):
        try:
            GameClass = self._games[game_name]
            game = GameClass(self.db, theme)
            
            # إضافة اسم اللعبة
            game.game_name = game_name

            # استكمال التقدم إن وجد
            progress = self.db.get_game_progress(user_id)
            if progress and progress.get("game") == game_name:
                if hasattr(game, "restore"):
                    game.restore(progress)

            with self._lock:
                self._active[user_id] = game

            logger.info(f"✓ Started game '{game_name}' for {user_id}")
            return game.start(user_id)

        except Exception as e:
            logger.exception(f"✗ Error starting game {game_name}: {e}")
            with self._lock:
                self._active.pop(user_id, None)
            return None

    def _handle_answer(self, user_id: str, raw_answer: str):
        with self._lock:
            game = self._active.get(user_id)

        if not game:
            return None

        try:
            answer = Config.normalize(raw_answer)
            result = game.check(answer, user_id)

            if not result:
                return None

            # نهاية اللعبة
            if result.get("game_over"):
                with self._lock:
                    self._active.pop(user_id, None)

                won = result.get("won", False)
                self.db.finish_game(user_id, won)
                self.db.clear_game_progress(user_id)

                logger.info(f"Game finished for {user_id}, won={won}")

            return result.get("response")

        except Exception as e:
            logger.exception(f"Error handling answer for {user_id}: {e}")
            with self._lock:
                self._active.pop(user_id, None)
            return None
