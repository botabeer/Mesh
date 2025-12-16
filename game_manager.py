import logging
from threading import Lock
from config import Config

logger = logging.getLogger(__name__)


class GameManager:
    def __init__(self, db):
        self.db = db
        self._lock = Lock()
        self._active = {}
        self._games = self._load_games()
        logger.info(f"✅ GameManager initialized with {len(self._games)} games")
        logger.info(f"✅ Loaded games: {list(self._games.keys())}")

    def _load_games(self):
        """تحميل جميع الألعاب بشكل صحيح"""
        games = {}

        # ✅ قائمة الألعاب الكاملة مع التطبيع الصحيح
        game_mappings = {
            # الاسم المُطبَّع: (المسار، اسم الكلاس)
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

        for game_name, (module_path, class_name) in game_mappings.items():
            try:
                # ✅ استيراد ديناميكي آمن
                module = __import__(module_path, fromlist=[class_name])
                game_class = getattr(module, class_name)
                
                # ✅ التحقق من أن الكلاس يعمل
                test_instance = game_class(self.db, "light")
                if not hasattr(test_instance, 'start'):
                    raise AttributeError(f"{class_name} missing start() method")
                
                games[game_name] = game_class
                logger.info(f"✅ Loaded: {game_name} → {class_name}")
                
            except ImportError as e:
                logger.error(f"❌ Import failed [{game_name}]: {e}")
            except AttributeError as e:
                logger.error(f"❌ Class error [{game_name}]: {e}")
            except Exception as e:
                logger.error(f"❌ Unknown error [{game_name}]: {e}")

        return games

    def handle(self, user_id: str, cmd: str, theme: str, raw_text: str):
        """معالجة الأوامر"""
        user = self.db.get_user(user_id)
        if not user:
            return None

        with self._lock:
            game = self._active.get(user_id)

        # ✅ لاعب داخل لعبة
        if game:
            return self._handle_answer(user_id, raw_text)

        # ✅ بدء لعبة جديدة
        # تطبيع الأمر للمقارنة
        normalized_cmd = Config.normalize(cmd)
        
        logger.info(f"🔍 Searching for game: '{normalized_cmd}'")
        logger.info(f"📋 Available games: {list(self._games.keys())}")
        
        if normalized_cmd in self._games:
            logger.info(f"✅ Starting game: {normalized_cmd}")
            return self._start_game(user_id, normalized_cmd, theme)
        else:
            logger.warning(f"❌ Game '{normalized_cmd}' not found")
            return None

    def stop_game(self, user_id: str) -> bool:
        """إيقاف اللعبة"""
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

        if hasattr(game, "on_stop"):
            try:
                game.on_stop(user_id)
            except Exception as e:
                logger.error(f"Error in game on_stop: {e}")

        logger.info(f"✅ Game stopped for {user_id}")
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
            
            # ✅ إضافة اسم اللعبة
            game.game_name = game_name

            # استكمال التقدم
            progress = self.db.get_game_progress(user_id)
            if progress and progress.get("game") == game_name:
                if hasattr(game, "restore"):
                    game.restore(progress)

            with self._lock:
                self._active[user_id] = game

            logger.info(f"✅ Started '{game_name}' for {user_id}")
            
            # ✅ استدعاء start() والحصول على الرسالة
            response = game.start(user_id)
            return response

        except Exception as e:
            logger.exception(f"❌ Error starting {game_name}: {e}")
            with self._lock:
                self._active.pop(user_id, None)
            return None

    def _handle_answer(self, user_id: str, raw_answer: str):
        """معالجة إجابة اللاعب"""
        with self._lock:
            game = self._active.get(user_id)

        if not game:
            return None

        try:
            answer = Config.normalize(raw_answer)
            result = game.check(answer, user_id)

            if not result:
                return None

            # ✅ نهاية اللعبة
            if result.get("game_over"):
                with self._lock:
                    self._active.pop(user_id, None)

                won = result.get("won", False)
                self.db.finish_game(user_id, won)
                self.db.clear_game_progress(user_id)

                logger.info(f"✅ Game finished for {user_id}, won={won}")

            return result.get("response")

        except Exception as e:
            logger.exception(f"❌ Error handling answer for {user_id}: {e}")
            with self._lock:
                self._active.pop(user_id, None)
            return None
