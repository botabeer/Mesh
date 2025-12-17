import logging
from threading import Lock
from config import Config
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class GameManager:
    """مدير الألعاب - نسخة محسنة لكل الألعاب مع 5 جولات وأول إجابة صحيحة"""

    MAX_ROUNDS = 5

    def __init__(self, db):
        self.db = db
        self._lock = Lock()
        self._active = {}  # user_id -> game_state
        self._games = self._load_games()
        logger.info(f"GameManager loaded {len(self._games)} games")

    # ================= Load Games =================
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
                instance = game_class(self.db, "light")
                if not hasattr(instance, "start"):
                    raise AttributeError("Missing start()")
                games[name] = game_class
                logger.info(f"Loaded game: {name}")
            except Exception as e:
                logger.error(f"Failed loading {name}: {e}")

        return games

    # ================= Handle Commands =================
    def handle(self, user_id: str, cmd: str, theme: str, raw_text: str):
        user = self.db.get_user(user_id)
        normalized_cmd = Config.normalize(cmd)

        # التحقق إذا المستخدم في وضع انسحب
        if self.db.is_ignored(user_id):
            if normalized_cmd in ["انسحب","تسجيل","بداية","العاب","نقاطي","الصدارة","ثيم","مساعدة"]:
                pass  # يمكن التفاعل مع هذه الأوامر فقط
            else:
                return None

        # بدء اللعبة
        if normalized_cmd in self._games:
            return self._start_game(user_id, normalized_cmd, theme)

        # التحقق إذا اللعبة فعّالة
        with self._lock:
            game_state = self._active.get(user_id)

        if game_state:
            return self._handle_answer(user_id, raw_text)

        return None

    # ================= Start / Stop =================
    def _start_game(self, user_id: str, game_name: str, theme: str):
        try:
            GameClass = self._games[game_name]
            game = GameClass(self.db, theme)
            game.game_name = game_name

            # استعادة التقدم إذا موجود
            progress = self.db.get_game_progress(user_id)
            if progress and progress.get("game") == game_name:
                if hasattr(game, "restore"):
                    game.restore(progress)

            with self._lock:
                self._active[user_id] = {
                    "game": game,
                    "round": 1,
                    "answered": False,
                    "score": 0,
                    "start_time": datetime.now()
                }

            response = game.start(user_id)
            return self._safe_response(response)

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

    # ================= Answer Handling =================
    def _handle_answer(self, user_id: str, answer: str):
        with self._lock:
            state = self._active.get(user_id)
        if not state:
            return None

        game = state["game"]

        # فقط أول إجابة صحيحة
        if state["answered"]:
            return None

        try:
            result = game.check(answer, user_id)
            response = self._safe_response(result.get("response")) if isinstance(result, dict) else None

            if isinstance(result, dict) and result.get("correct"):
                state["answered"] = True
                state["score"] += result.get("points", 1)
                # الانتقال للسؤال التالي
                if state["round"] < self.MAX_ROUNDS:
                    state["round"] += 1
                    state["answered"] = False
                    next_q = game.next_question(user_id)
                    return self._safe_response(next_q)
                else:
                    # انتهاء اللعبة
                    self.db.finish_game(user_id, True)
                    self.db.add_points(user_id, state["score"])
                    self.db.clear_game_progress(user_id)
                    with self._lock:
                        self._active.pop(user_id, None)
                    return response or f"انتهت اللعبة! نقاطك: {state['score']}"

            return response

        except Exception as e:
            logger.exception(f"Answer error: {e}")
            with self._lock:
                self._active.pop(user_id, None)
            return None

    # ================= Safety =================
    def _safe_response(self, response):
        if not response:
            return None
        if isinstance(response, list):
            return [r for r in response if r]
        return response

    # ================= Count Active =================
    def count_active(self):
        """عدد الألعاب النشطة"""
        with self._lock:
            return len(self._active)
