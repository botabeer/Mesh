import logging
from typing import Optional, Dict
from linebot.v3.messaging import TextMessage

logger = logging.getLogger(__name__)

class GameEngine:
    STATE_IDLE = "idle"
    STATE_WAITING_NAME = "waiting_name"
    STATE_IN_GAME = "in_game"

    def __init__(self, messaging_api, database):
        self.messaging_api = messaging_api
        self.db = database
        self.active_games = {}
        self.waiting_for_name = {}
        self.user_states = {}
        self.games = self._load_all_games()

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
        for game_name, (module_name, class_name) in game_mappings.items():
            game_class = self._load_game(module_name, class_name)
            if game_class:
                games[game_name] = game_class
        return games

    def _load_game(self, module_name: str, class_name: str):
        try:
            module = __import__(f"games.{module_name}", fromlist=[class_name])
            return getattr(module, class_name)
        except Exception as e:
            logger.error(f"Failed to load {class_name}: {e}")
            return None

    def set_waiting_for_name(self, user_id: str, waiting: bool):
        if waiting:
            self.waiting_for_name[user_id] = True
            self.user_states[user_id] = self.STATE_WAITING_NAME
        else:
            self.waiting_for_name.pop(user_id, None)
            self.user_states[user_id] = self.STATE_IDLE

    def is_waiting_for_name(self, user_id: str) -> bool:
        return self.waiting_for_name.get(user_id, False)

    def get_user_state(self, user_id: str) -> str:
        return self.user_states.get(user_id, self.STATE_IDLE)

    def process_message(self, text: str, user_id: str, group_id: str, display_name: str, is_registered: bool):
        text = text.strip()
        state = self.get_user_state(user_id)
        if group_id in self.active_games:
            return self._handle_game_answer(text, user_id, group_id, display_name)
        return self._handle_game_start(text, user_id, group_id, is_registered)

    def _handle_game_start(self, text: str, user_id: str, group_id: str, is_registered: bool):
        if text in self.games:
            if not is_registered and text != "توافق":
                return TextMessage(text="يجب التسجيل أولاً\nاكتب: تسجيل")
            return self._start_game(text, user_id, group_id)
        text_games = ["سؤال", "منشن", "تحدي", "اعتراف", "موقف", "اقتباس"]
        if text in text_games:
            return self._start_text_game(text)
        return None

    def _start_game(self, game_name: str, user_id: str, group_id: str):
        GameClass = self.games.get(game_name)
        if not GameClass:
            return TextMessage(text="اللعبة غير متوفرة")
        try:
            game = GameClass(self.messaging_api)
            if hasattr(game, "set_database"):
                game.set_database(self.db)
            self.active_games[group_id] = game
            self.user_states[user_id] = self.STATE_IN_GAME
            result = game.start_game()
            return result if result else TextMessage(text="بدأت اللعبة")
        except Exception as e:
            logger.error(f"Error starting game {game_name}: {e}", exc_info=True)
            return TextMessage(text="فشل بدء اللعبة\nحاول مرة أخرى")

    def _start_text_game(self, game_name: str):
        import random
        files = {
            "سؤال": "questions.txt",
            "منشن": "mentions.txt",
            "تحدي": "challenges.txt",
            "اعتراف": "confessions.txt",
            "موقف": "situations.txt",
            "اقتباس": "quotes.txt",
        }
        try:
            filepath = f"games/{files[game_name]}"
            with open(filepath, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f if line.strip()]
            if lines:
                return TextMessage(text=random.choice(lines))
            return TextMessage(text="لا توجد محتوى متاح")
        except FileNotFoundError:
            logger.error(f"File not found: {filepath}")
            return TextMessage(text="فشل تحميل اللعبة")
        except Exception as e:
            logger.error(f"Error in text game {game_name}: {e}")
            return TextMessage(text="حدث خطأ")

    def _handle_game_answer(self, text: str, user_id: str, group_id: str, display_name: str):
        game = self.active_games.get(group_id)
        if not game:
            return TextMessage(text="اللعبة انتهت")
        try:
            result = game.check_answer(text, user_id, display_name)
            if result is None:
                return None
            if isinstance(result, TextMessage):
                return result
            if not isinstance(result, dict):
                return None
            points = result.get("points", 0)
            if points > 0:
                game_type = getattr(game, 'game_name', 'unknown')
                self.db.update_user_points(user_id, points, points > 0, game_type)
            if result.get("game_over"):
                del self.active_games[group_id]
                self.user_states[user_id] = self.STATE_IDLE
            response = result.get("response")
            if response:
                return response
            message = result.get("message", "")
            return TextMessage(text=message) if message else None
        except Exception as e:
            logger.error(f"Game error: {e}", exc_info=True)
            self.active_games.pop(group_id, None)
            self.user_states[user_id] = self.STATE_IDLE
            return TextMessage(text="حدث خطأ في اللعبة")

    def stop_game(self, group_id: str) -> bool:
        if group_id in self.active_games:
            del self.active_games[group_id]
            return True
        return False

    def get_active_games_count(self) -> int:
        return len(self.active_games)

    def is_game_active(self, group_id: str) -> bool:
        return group_id in self.active_games
