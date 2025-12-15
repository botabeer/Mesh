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
        """تحميل جميع الألعاب المتاحة"""
        games = {}
        
        # خريطة الألعاب: الأمر -> (المسار، اسم الكلاس)
        mappings = {
            # ألعاب فردية
            "ذكاء": ("games.iq", "IqGame"),
            "خمن": ("games.guess", "GuessGame"),
            "رياضيات": ("games.math", "MathGame"),
            "ترتيب": ("games.scramble", "ScrambleGame"),
            "ضد": ("games.opposite", "OppositeGame"),
            "اسرع": ("games.fast_typing", "FastTypingGame"),
            
            # ألعاب جديدة
            "سلسله": ("games.ChainWordsGame", "ChainWordsGame"),
            "انسان_حيوان": ("games.HumanAnimalPlantGame", "HumanAnimalPlantGame"),
            "كون_كلمات": ("games.LettersWordsGame", "LettersWordsGame"),
            "اغاني": ("games.SongGame", "SongGame"),
            "الوان": ("games.WordColorGame", "WordColorGame"),
            
            # ألعاب جماعية
            "مافيا": ("games.mafia", "MafiaGame"),
            "توافق": ("games.compatibility", "CompatibilityGame")
        }
        
        for name, (mod_path, class_name) in mappings.items():
            try:
                mod = __import__(mod_path, fromlist=[class_name])
                games[name] = getattr(mod, class_name)
                logger.info(f"✓ Loaded game: {name}")
            except Exception as e:
                logger.error(f"✗ Failed to load {name}: {e}")
        
        return games

    def handle(self, user_id: str, cmd: str, theme: str, text: str):
        """معالجة الأوامر المتعلقة بالألعاب"""
        with self._lock:
            game = self._active.get(user_id)

        # إذا كان اللاعب في لعبة نشطة
        if game:
            return self._handle_answer(user_id, text)

        # بدء لعبة جديدة
        if cmd in self._games:
            return self._start_game(user_id, cmd, theme)

        return None

    def stop_game(self, user_id: str) -> bool:
        """إيقاف اللعبة الحالية للاعب"""
        with self._lock:
            return self._active.pop(user_id, None) is not None

    def count_active(self) -> int:
        """عدد الألعاب النشطة حالياً"""
        with self._lock:
            return len(self._active)

    def _start_game(self, user_id: str, game_name: str, theme: str):
        """بدء لعبة جديدة"""
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
        """معالجة إجابة اللاعب"""
        with self._lock:
            game = self._active.get(user_id)
        
        if not game:
            return None
        
        try:
            result = game.check(answer, user_id)
            
            if not result:
                return None
            
            # إذا انتهت اللعبة، إزالتها من القائمة النشطة
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
        """الحصول على قائمة الألعاب النشطة"""
        with self._lock:
            return {
                user_id: type(game).__name__ 
                for user_id, game in self._active.items()
            }
