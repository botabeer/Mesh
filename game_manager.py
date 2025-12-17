import logging
from threading import Lock
from datetime import datetime
from config import Config
from ui import UI

logger = logging.getLogger(__name__)

class GameManager:
    MAX_ROUNDS = 5

    def __init__(self, db, theme="light"):
        self.db = db
        self.theme = theme
        self.ui = UI(theme)
        self._lock = Lock()
        self._active = {}  # user_id -> state
        self._mafia_game = None  # Single mafia game instance
        self._games = self._load_games()
        logger.info(f"GameManager loaded {len(self._games)} games")

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
                
                # Special handling for mafia - it's a group game
                if name == "مافيا":
                    games[name] = game_class
                else:
                    instance = game_class(self.db, self.theme)
                    if not hasattr(instance, "start"):
                        raise AttributeError("Missing start() method")
                    games[name] = game_class
                
                logger.info(f"Loaded game: {name}")
            except Exception as e:
                logger.error(f"Failed loading {name}: {e}")
        return games

    def handle(self, user_id, cmd, raw_text, theme="light"):
        normalized_cmd = Config.normalize(cmd)

        if self.db.is_ignored(user_id):
            if normalized_cmd in ["انسحب", "تسجيل", "بداية", "العاب", "نقاطي", "الصدارة", "ثيم", "مساعدة"]:
                pass
            else:
                return None

        # Check for mafia game commands
        if normalized_cmd == "مافيا":
            return self._start_mafia_game(user_id, theme)
        
        # Check if mafia game is active and handle its commands
        if self._mafia_game and self._mafia_game.game_active:
            mafia_response = self._mafia_game.check(raw_text, user_id)
            if mafia_response:
                return mafia_response.get("response")

        # Regular single-player games
        if normalized_cmd in self._games and normalized_cmd != "مافيا":
            return self._start_game(user_id, normalized_cmd, theme)

        with self._lock:
            state = self._active.get(user_id)

        if state:
            return self._handle_answer(user_id, raw_text)

        return None

    def _start_mafia_game(self, user_id, theme="light"):
        """Start or join mafia game"""
        try:
            # Create new game if doesn't exist or previous ended
            if not self._mafia_game or not self._mafia_game.game_active:
                GameClass = self._games["مافيا"]
                self._mafia_game = GameClass(self.db, theme)
                responses = self._mafia_game.start(user_id)
                return responses if isinstance(responses, list) else [responses]
            else:
                # Game already active, return status
                return self._mafia_game.game_status_screen()
        except Exception as e:
            logger.exception(f"Start mafia game error: {e}")
            self._mafia_game = None
            return None

    def _start_game(self, user_id, game_name, theme="light"):
        try:
            GameClass = self._games[game_name]
            game = GameClass(self.db, theme)
            game.game_name = game_name
            game.total_q = self.MAX_ROUNDS

            progress = self.db.get_game_progress(user_id)
            if progress and progress.get("game") == game_name:
                if hasattr(game, "restore"):
                    game.restore(progress)

            with self._lock:
                self._active[user_id] = {
                    "game": game,
                    "round": getattr(progress, "round", 0) if progress else 0,
                    "score": getattr(progress, "score", 0) if progress else 0,
                    "start_time": datetime.now()
                }

            response = game.start(user_id)
            return response

        except Exception as e:
            logger.exception(f"Start game error [{game_name}]: {e}")
            with self._lock:
                self._active.pop(user_id, None)
            return None

    def stop_game(self, user_id):
        # Check if user is in mafia game
        if self._mafia_game and user_id in self._mafia_game.players:
            # Don't allow stopping mafia mid-game
            return False
        
        with self._lock:
            state = self._active.pop(user_id, None)

        if not state:
            return False

        try:
            game = state["game"]
            self.db.save_game_progress(user_id, {
                "game": getattr(game, "game_name", ""),
                "score": state.get("score", 0),
                "round": state.get("round", 0)
            })
            if hasattr(game, "on_stop"):
                game.on_stop(user_id)
        except Exception as e:
            logger.error(f"Stop error: {e}")

        logger.info(f"Game stopped for {user_id}")
        return True

    def _handle_answer(self, user_id, answer):
        with self._lock:
            state = self._active.get(user_id)
            if not state:
                return None
            
            game = state["game"]
            game_data = {
                'game': game,
                'round': state['round'],
                'score': state['score']
            }

        try:
            result = game.check(answer, user_id)
            if not result:
                return None

            if result.get("game_over"):
                with self._lock:
                    self._active.pop(user_id, None)
                self.db.clear_game_progress(user_id)
                return result.get("response")

            with self._lock:
                if user_id in self._active:
                    self._active[user_id]['round'] = game_data['round']
                    self._active[user_id]['score'] = game_data['score']

            return result.get("response")

        except Exception as e:
            logger.exception(f"Answer error: {e}")
            with self._lock:
                self._active.pop(user_id, None)
            return None

    def count_active(self):
        with self._lock:
            count = len(self._active)
        
        # Add mafia game if active
        if self._mafia_game and self._mafia_game.game_active:
            count += 1
        
        return count
