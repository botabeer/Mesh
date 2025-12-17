import logging
from threading import Lock
from datetime import datetime
from config import Config
from ui import UI

logger = logging.getLogger(__name__)

class GameManager:
    """مدير الألعاب المحسّن - مدمج مع UI و BaseGame، 5 جولات"""

    MAX_ROUNDS = 5

    def __init__(self, db, theme="light"):
        self.db = db
        self.theme = theme
        self.ui = UI(theme)
        self._lock = Lock()
        self._active = {}  # user_id -> {"game": game_instance, "round": int, ...}
        self._games = self._load_games()
        logger.info(f"GameManager loaded {len(self._games)} games")

    def _load_games(self):
        """تحميل الألعاب ديناميكيًا"""
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
            "تكوين": ("games.letters_words", "LettersWordsGame"),
            "اغاني": ("games.song", "SongGame"),
            "الوان": ("games.word_color", "WordColorGame"),
            "توافق": ("games.compatibility", "CompatibilityGame"),
            "مافيا": ("games.mafia", "MafiaGame"),
        }

        for name, (path, cls) in game_mappings.items():
            try:
                module = __import__(path, fromlist=[cls])
                game_class = getattr(module, cls)
                instance = game_class(self.db, self.theme)
                if not hasattr(instance, "start"):
                    raise AttributeError("Missing start() method")
                games[name] = game_class
                logger.info(f"Loaded game: {name}")
            except Exception as e:
                logger.error(f"Failed loading {name}: {e}")
        return games

    def handle(self, user_id: str, cmd: str, raw_text: str):
        """التعامل مع الأوامر أو الإجابات"""
        user = self.db.get_user(user_id)
        normalized_cmd = Config.normalize(cmd)

        if self.db.is_ignored(user_id):
            if normalized_cmd in ["انسحب","تسجيل","بداية","العاب","نقاطي","الصدارة","ثيم","مساعدة"]:
                pass
            else:
                return None

        # بدء اللعبة
        if normalized_cmd in self._games:
            return self._start_game(user_id, normalized_cmd)

        # التحقق إذا اللعبة فعّالة
        with self._lock:
            state = self._active.get(user_id)

        if state:
            return self._handle_answer(user_id, raw_text)

        return None

    def _start_game(self, user_id: str, game_name: str):
        try:
            GameClass = self._games[game_name]
            game = GameClass(self.db, self.theme)
            game.game_name = game_name
            game.total_q = self.MAX_ROUNDS

            progress = self.db.get_game_progress(user_id)
            if progress and progress.get("game") == game_name:
                if hasattr(game, "restore"):
                    game.restore(progress)

            with self._lock:
                self._active[user_id] = {
                    "game": game,
                    "round": 0,
                    "score": 0,
                    "start_time": datetime.now()
                }

            response = game.start(user_id)
            return response

        except Exception as e:
            logger.exception(f"Start game error [{game_name}]: {e}")
            with self._lock:
                self._active.pop(user_id, None)
            return None

    def stop_game(self, user_id: str):
        with self._lock:
            state = self._active.pop(user_id, None)

        if not state:
            return False

        try:
            game = state["game"]
            self.db.save_game_progress(user_id, {
                "game": getattr(game, "game_name", ""),
                "score": state["score"],
                "round": state["round"],
            })
            if hasattr(game, "on_stop"):
                game.on_stop(user_id)
        except Exception as e:
            logger.error(f"Stop error: {e}")

        logger.info(f"Game stopped for {user_id}")
        return True

    def _handle_answer(self, user_id: str, answer: str):
        with self._lock:
            state = self._active.get(user_id)

        if not state:
            return None

        game = state["game"]

        try:
            result = game.check(answer, user_id)
            if not result:
                return None

            # انتهت اللعبة
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

    def count_active(self):
        with self._lock:
            return len(self._active)
