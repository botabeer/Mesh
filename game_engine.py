# ========================================
# game_engine.py
# ========================================

import logging
from typing import Dict, Optional
from linebot.v3.messaging import TextMessage

logger = logging.getLogger(__name__)


class GameEngine:
    """Production-ready Game Engine"""

    STATE_IDLE = "idle"
    STATE_WAITING_NAME = "waiting_name"
    STATE_IN_GAME = "in_game"

    def __init__(self, messaging_api, database):
        self.messaging_api = messaging_api
        self.db = database

        self.active_games: Dict[str, Dict] = {}
        self.user_states: Dict[str, str] = {}
        self.waiting_for_name = set()

        self.games = self._load_all_games()

    # ------------------------------------
    # Load Games
    # ------------------------------------
    def _load_all_games(self) -> Dict:
        mappings = {
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

        games = {}
        for name, (module, cls) in mappings.items():
            try:
                mod = __import__(f"games.{module}", fromlist=[cls])
                games[name] = getattr(mod, cls)
            except Exception:
                logger.error(f"Failed to load game: {cls}", exc_info=True)

        return games

    # ------------------------------------
    # State Helpers
    # ------------------------------------
    def get_user_state(self, user_id: str) -> str:
        return self.user_states.get(user_id, self.STATE_IDLE)

    def set_user_state(self, user_id: str, state: str):
        self.user_states[user_id] = state

    # ------------------------------------
    # Message Router
    # ------------------------------------
    def process_message(
        self,
        text: str,
        user_id: str,
        group_id: str,
        display_name: str,
        is_registered: bool
    ):
        text = text.strip()
        state = self.get_user_state(user_id)

        logger.info(
            f"MSG [{group_id}] {user_id} | {state} | {text}"
        )

        if state == self.STATE_WAITING_NAME:
            return self._handle_registration(text, user_id)

        if group_id in self.active_games:
            return self._handle_game_answer(
                text, user_id, group_id, display_name
            )

        return self._handle_game_start(
            text, user_id, group_id, is_registered
        )

    # ------------------------------------
    # Registration
    # ------------------------------------
    def _handle_registration(self, text: str, user_id: str):
        name = text.strip()

        if not (2 <= len(name) <= 20):
            return TextMessage(text="الاسم يجب أن يكون بين 2 و 20 حرف")

        if self.db.register_or_update_user(user_id, name):
            self.set_user_state(user_id, self.STATE_IDLE)
            return TextMessage(
                text=f"تم التسجيل بنجاح\n\nالاسم: {name}"
            )

        return TextMessage(text="فشل التسجيل، حاول مرة أخرى")

    # ------------------------------------
    # Game Start
    # ------------------------------------
    def _handle_game_start(
        self,
        text: str,
        user_id: str,
        group_id: str,
        is_registered: bool
    ):
        if text not in self.games:
            return None

        if not is_registered and text != "توافق":
            return TextMessage(text="يجب التسجيل أولاً")

        return self._start_game(text, user_id, group_id)

    def _start_game(self, game_name: str, user_id: str, group_id: str):
        GameClass = self.games.get(game_name)
        if not GameClass:
            return TextMessage(text="اللعبة غير متوفرة")

        try:
            game = GameClass(self.messaging_api)

            if hasattr(game, "set_database"):
                game.set_database(self.db)

            self.active_games[group_id] = {
                "game": game,
                "owner": user_id
            }

            self.set_user_state(user_id, self.STATE_IN_GAME)

            response = game.start_game()
            return response or TextMessage(text="بدأت اللعبة")

        except Exception:
            logger.error("Game start failed", exc_info=True)
            self.active_games.pop(group_id, None)
            self.set_user_state(user_id, self.STATE_IDLE)
            return TextMessage(text="فشل بدء اللعبة")

    # ------------------------------------
    # Game Answer
    # ------------------------------------
    def _handle_game_answer(
        self,
        text: str,
        user_id: str,
        group_id: str,
        display_name: str
    ):
        data = self.active_games.get(group_id)
        if not data:
            return None

        game = data["game"]

        try:
            result = game.check_answer(text, user_id, display_name)

            if not result:
                return None

            if isinstance(result, TextMessage):
                return result

            points = result.get("points", 0)
            if points > 0:
                self.db.update_user_points(
                    user_id,
                    points,
                    True,
                    getattr(game, "game_name", "unknown")
                )

            if result.get("game_over"):
                self.active_games.pop(group_id, None)
                self.set_user_state(user_id, self.STATE_IDLE)

            return result.get("response") or (
                TextMessage(text=result.get("message"))
                if result.get("message") else None
            )

        except Exception:
            logger.error("Game runtime error", exc_info=True)
            self.active_games.pop(group_id, None)
            self.set_user_state(user_id, self.STATE_IDLE)
            return TextMessage(text="حدث خطأ في اللعبة")

    # ------------------------------------
    # Utils
    # ------------------------------------
    def stop_game(self, group_id: str) -> bool:
        if group_id in self.active_games:
            self.active_games.pop(group_id, None)
            return True
        return False

    def is_game_active(self, group_id: str) -> bool:
        return group_id in self.active_games

    def active_games_count(self) -> int:
        return len(self.active_games)
