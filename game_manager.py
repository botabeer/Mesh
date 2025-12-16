import logging
from threading import Lock

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
            "ترتيب": ("games.scramble", "ScrambleGame"),
            "ضد": ("games.opposite", "OppositeGame"),
            "اسرع": ("games.fast_typing", "FastTypingGame"),
            "سلسله": ("games.chain_words", "ChainWordsGame"),
            "انسان_حيوان": ("games.human_animal", "HumanAnimalGame"),
            "كون_كلمات": ("games.letters_words", "LettersWordsGame"),
            "اغاني": ("games.song", "SongGame"),
            "الوان": ("games.word_color", "WordColorGame"),
            "مافيا": ("games.mafia", "MafiaGame"),
            "توافق": ("games.compatibility", "CompatibilityGame")
        }
        
        for name, (mod_path, class_name) in mappings.items():
            try:
                mod = __import__(mod_path, fromlist=[class_name])
                games[name] = getattr(mod, class_name)
                logger.info(f"Loaded game: {name}")
            except Exception as e:
                logger.error(f"Failed to load {name}: {e}")
        
        return games

    def handle(self, user_id: str, cmd: str, theme: str, text: str):
        with self._lock:
            game = self._active.get(user_id)

        if game:
            return self._handle_answer(user_id, text)

        if cmd in self._games:
            return self._start_game(user_id, cmd, theme)

        return None

    def stop_game(self, user_id: str) -> bool:
        with self._lock:
            game = self._active.pop(user_id, None)
            if game:
                self.db.save_game_progress(user_id, {
                    "score": getattr(game, 'score', 0),
                    "current_q": getattr(game, 'current_q', 0)
                })
            return game is not None

    def count_active(self) -> int:
        with self._lock:
            return len(self._active)

    def _start_game(self, user_id: str, game_name: str, theme: str):
        try:
            GameClass = self._games[game_name]
            game = GameClass(self.db, theme)
            
            with self._lock:
                self._active[user_id] = game
            
            logger.info(f"Started {game_name} for user {user_id}")
            return game.start(user_id)
            
        except Exception as e:
            logger.exception(f"Error starting game {game_name}: {e}")
            with self._lock:
                self._active.pop(user_id, None)
            return None

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
                logger.info(f"Game ended for user {user_id}")
            
            return result.get("response")
            
        except Exception as e:
            logger.exception(f"Error handling answer: {e}")
            with self._lock:
                self._active.pop(user_id, None)
            return None

    def get_active_games(self):
        with self._lock:
            return {
                user_id: type(game).__name__ 
                for user_id, game in self._active.items()
            }
