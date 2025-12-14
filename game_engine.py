import logging
from typing import Dict
from linebot.v3.messaging import TextMessage

logger = logging.getLogger(__name__)


class GameEngine:
    STATE_IDLE = "idle"
    STATE_WAITING_NAME = "waiting_name"
    STATE_IN_GAME = "in_game"

    STOP_COMMANDS = {"ايقاف", "خروج", "stop", "إيقاف"}

    def __init__(self, messaging_api, database):
        self.messaging_api = messaging_api
        self.db = database
        self.active_games: Dict[str, object] = {}
        self.user_states: Dict[str, str] = {}
        self.games = self._load_all_games()

    # =========================
    # Game Loader
    # =========================
    def _load_all_games(self) -> Dict:
        games = {}
        game_mappings = {
            "ذكاء": ("iq_game", "IqGame"),
            "خمن": ("guess_game", "GuessGame"),
            "ضد": ("opposite_game", "OppositeGame"),
            "ترتيب": ("scramble_word_game", "ScrambleWordGame"),
            "رياضيات": ("math_game", "MathGame"),
            "اغنيه": ("song_game", "SongGame"),
            "لون": ("word_color_game", "WordColorGame"),
            "تكوين": ("letters_words_game", "LettersWordsGame"),
            "لعبة": ("human_animal_plant_game", "HumanAnimalPlantGame"),
            "سلسلة": ("chain_words_game", "ChainWordsGame"),
            "اسرع": ("fast_typing_game", "FastTypingGame"),
            "توافق": ("compatibility_game", "CompatibilityGame"),
            "مافيا": ("mafia_game", "MafiaGame"),
        }

        for name, (module, cls) in game_mappings.items():
            game_class = self._load_game(module, cls)
            if game_class:
                games[name] = game_class

        logger.info(f"Loaded games: {list(games.keys())}")
        return games

    def _load_game(self, module_name: str, class_name: str):
        try:
            module = __import__(f"games.{module_name}", fromlist=[class_name])
            return getattr(module, class_name)
        except Exception as e:
            logger.error(f"Failed to load {class_name}: {e}")
            return None

    # =========================
    # Main Entry
    # =========================
    def process_message(
        self,
        text: str,
        user_id: str,
        display_name: str,
        is_registered: bool,
        theme: str,
    ):
        text = text.strip()
        group_id = user_id  # ألعاب فردية

        # إيقاف اللعبة
        if text.lower() in self.STOP_COMMANDS:
            if self.stop_game(group_id):
                self.user_states[user_id] = self.STATE_IDLE
                return TextMessage(text="🛑 تم إيقاف اللعبة")
            return TextMessage(text="لا توجد لعبة نشطة")

        # لعبة نشطة
        if group_id in self.active_games:
            return self._handle_game_answer(
                text, user_id, group_id, display_name, theme
            )

        # بدء لعبة
        return self._handle_game_start(
            text, user_id, group_id, is_registered, theme
        )

    # =========================
    # Start Game
    # =========================
    def _handle_game_start(
        self,
        text: str,
        user_id: str,
        group_id: str,
        is_registered: bool,
        theme: str,
    ):
        if text in self.games:
            if not is_registered and text != "توافق":
                return TextMessage(text="يجب التسجيل أولاً ✍️\nاكتب: تسجيل")

            return self._start_game(text, user_id, group_id, theme)

        text_games = {"سؤال", "منشن", "تحدي", "اعتراف", "موقف", "اقتباس"}
        if text in text_games:
            return self._start_text_game(text)

        return TextMessage(text="❓ اكتب اسم لعبة للبدء")

    def _start_game(self, game_name: str, user_id: str, group_id: str, theme: str):
        GameClass = self.games.get(game_name)
        if not GameClass:
            return TextMessage(text="اللعبة غير متوفرة")

        try:
            game = GameClass(self.messaging_api)

            if hasattr(game, "set_database"):
                game.set_database(self.db)
            if hasattr(game, "set_theme"):
                game.set_theme(theme)

            self.active_games[group_id] = game
            self.user_states[user_id] = self.STATE_IN_GAME

            result = game.start_game()
            return result or TextMessage(text="🎮 بدأت اللعبة!")

        except Exception as e:
            logger.error(f"Start game error: {e}", exc_info=True)
            return TextMessage(text="فشل بدء اللعبة")

    # =========================
    # Game Answer
    # =========================
    def _handle_game_answer(
        self,
        text: str,
        user_id: str,
        group_id: str,
        display_name: str,
        theme: str,
    ):
        game = self.active_games.get(group_id)
        if not game:
            self.user_states[user_id] = self.STATE_IDLE
            return TextMessage(text="اللعبة انتهت")

        try:
            if hasattr(game, "set_theme"):
                game.set_theme(theme)

            result = game.check_answer(text, user_id, display_name)

            if isinstance(result, TextMessage):
                return result

            if not isinstance(result, dict):
                return TextMessage(text="⚠️ رد غير صالح من اللعبة")

            points = result.get("points", 0)
            if points:
                self.db.update_user_points(
                    user_id,
                    points,
                    points > 0,
                    getattr(game, "game_name", "unknown"),
                )

            if result.get("game_over"):
                self.stop_game(group_id)
                self.user_states[user_id] = self.STATE_IDLE

            return (
                result.get("response")
                or TextMessage(text=result.get("message", ""))
            )

        except Exception as e:
            logger.error(f"Game runtime error: {e}", exc_info=True)
            self.stop_game(group_id)
            self.user_states[user_id] = self.STATE_IDLE
            return TextMessage(text="حدث خطأ في اللعبة ❌")

    # =========================
    # Helpers
    # =========================
    def stop_game(self, group_id: str) -> bool:
        return self.active_games.pop(group_id, None) is not None

    def get_active_games_count(self) -> int:
        return len(self.active_games)

    def is_game_active(self, group_id: str) -> bool:
        return group_id in self.active_games
