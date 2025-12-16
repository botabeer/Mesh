import logging
from threading import Lock
from config import Config

logger = logging.getLogger(__name__)


class GameManager:
    """مدير الألعاب المحسّن"""
    
    def __init__(self, db):
        self.db = db
        self._lock = Lock()
        self._active = {}
        self._games = self._load_games()
        logger.info(f"GameManager: {len(self._games)} games loaded")

    def _load_games(self):
        """تحميل جميع الألعاب"""
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

        for game_name, (module_path, class_name) in game_mappings.items():
            try:
                module = __import__(module_path, fromlist=[class_name])
                game_class = getattr(module, class_name)
                
                test_instance = game_class(self.db, "light")
                
                if not hasattr(test_instance, 'start'):
                    raise AttributeError(f"{class_name} missing start() method")
                
                games[game_name] = game_class
                logger.info(f"Loaded: {game_name}")
            except ImportError as e:
                logger.error(f"Import failed [{game_name}]: {e}")
            except AttributeError as e:
                logger.error(f"Class error [{game_name}]: {e}")
            except Exception as e:
                logger.error(f"Unknown error [{game_name}]: {e}")

        return games

    def handle(self, user_id: str, cmd: str, theme: str, raw_text: str):
        """معالجة أوامر اللعبة"""
        user = self.db.get_user(user_id)
        if not user:
            normalized_cmd = Config.normalize(cmd)
            if normalized_cmd in ["توافق", "مافيا"]:
                return self._start_game(user_id, normalized_cmd, theme)
            return None

        with self._lock:
            game = self._active.get(user_id)

        if game:
            return self._handle_answer(user_id, raw_text)

        normalized_cmd = Config.normalize(cmd)
        
        if normalized_cmd in self._games:
            return self._start_game(user_id, normalized_cmd, theme)
        
        return None

    def stop_game(self, user_id: str) -> bool:
        """إيقاف اللعبة الحالية"""
        with self._lock:
            game = self._active.pop(user_id, None)

        if not game:
            return False

        self.db.save_game_progress(user_id, {
            "game": getattr(game, 'game_name', 'unknown'),
            "score": getattr(game, "score", 0),
            "current_q": getattr(game, "current_q", 0),
        })

        if hasattr(game, "on_stop"):
            try:
                game.on_stop(user_id)
            except Exception as e:
                logger.error(f"Error in game on_stop: {e}")

        logger.info(f"Game stopped: {user_id}")
        return True

    def count_active(self) -> int:
        """عدد الألعاب النشطة"""
        with self._lock:
            return len(self._active)

    def get_active_games(self):
        """الألعاب النشطة"""
        with self._lock:
            return {
                uid: type(game).__name__
                for uid, game in self._active.items()
            }

    def _start_game(self, user_id: str, game_name: str, theme: str):
        """بدء لعبة جديدة"""
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
            
            logger.info(f"Started: {game_name} for {user_id}")
            response = game.start(user_id)
            
            if not response:
                with self._lock:
                    self._active.pop(user_id, None)
                return None
            
            return response
            
        except Exception as e:
            logger.exception(f"Error starting {game_name}: {e}")
            with self._lock:
                self._active.pop(user_id, None)
            return None

    def _handle_answer(self, user_id: str, raw_answer: str):
        """معالجة الإجابة"""
        with self._lock:
            game = self._active.get(user_id)
        
        if not game:
            return None
        
        try:
            answer = Config.normalize(raw_answer)
            result = game.check(answer, user_id)
            
            if not result:
                return None
            
            if result.get("game_over"):
                with self._lock:
                    self._active.pop(user_id, None)
                
                won = result.get("won", False)
                self.db.finish_game(user_id, won)
                self.db.clear_game_progress(user_id)
                logger.info(f"Game finished: {user_id}, won={won}")
            
            return result.get("response")
            
        except Exception as e:
            logger.exception(f"Error handling answer for {user_id}: {e}")
            with self._lock:
                self._active.pop(user_id, None)
            return None
