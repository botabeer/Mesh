import logging
from linebot.models import TextSendMessage

logger = logging.getLogger(__name__)

class GameEngine:
    STATE_IDLE = "idle"
    STATE_WAITING_NAME = "waiting_name"

    def __init__(self, line_bot_api, db):
        self.line_bot_api = line_bot_api
        self.db = db
        self.active_games = {}
        self.waiting_for_name = set()

        # Load all games that need line_bot_api
        self.games = {
            "ذكاء": self._load_game("iq_game", "IqGame"),
            "خمن": self._load_game("guess_game", "GuessGame"),
            "ضد": self._load_game("opposite_game", "OppositeGame"),
            "ترتيب": self._load_game("scramble_word_game", "ScrambleWordGame"),
            "رياضيات": self._load_game("math_game", "MathGame"),
            "اغنيه": self._load_game("song_game", "SongGame"),
            "لون": self._load_game("word_color_game", "WordColorGame"),
            "تكوين": self._load_game("letters_words_game", "LettersWordsGame"),
            "لعبة": self._load_game("human_animal_plant_game", "HumanAnimalPlantGame"),
            "سلسلة": self._load_game("chain_words_game", "ChainWordsGame"),
            "اسرع": self._load_game("fast_typing_game", "FastTypingGame"),
            "توافق": self._load_game("compatibility_game", "CompatibilityGame"),
            "مافيا": self._load_game("mafia_game", "MafiaGame"),
        }
        self.text_games = ["سؤال", "منشن", "تحدي", "اعتراف", "موقف", "اقتباس"]

    def set_waiting_for_name(self, user_id, waiting):
        if waiting:
            self.waiting_for_name.add(user_id)
        else:
            self.waiting_for_name.discard(user_id)

    def process_message(self, text, user_id, group_id, display_name, is_registered):
        text = text.strip()
        logger.info(f"GameEngine: {text} | user={user_id} group={group_id}")

        if user_id in self.waiting_for_name:
            return self._handle_registration(text, user_id)
        if group_id in self.active_games:
            return self._handle_game_answer(text, user_id, group_id, display_name)
        return self._handle_command(text, user_id, group_id, display_name, is_registered)

    def _handle_registration(self, text, user_id):
        name = text.strip()
        if len(name) < 2 or len(name) > 20:
            return TextSendMessage(text="الاسم يجب ان يكون بين 2 و 20 حرف")
        self.db.register_or_update_user(user_id, name)
        self.waiting_for_name.discard(user_id)
        logger.info(f"User registered | user={user_id} name={name}")
        return TextSendMessage(text=f"تم التسجيل بنجاح\nالاسم: {name}")

    def _handle_command(self, text, user_id, group_id, display_name, is_registered):
        if text in self.games or text in self.text_games:
            if not is_registered:
                return TextSendMessage(text="يجب التسجيل اولا\nاكتب: تسجيل")
            return self._start_game(text, user_id, group_id)
        return None

    def _start_game(self, game_name, user_id, group_id):
        if game_name in self.text_games:
            return self._start_text_game(game_name)

        GameClass = self.games.get(game_name)
        if not GameClass:
            return TextSendMessage(text="اللعبة غير متوفرة")
        try:
            game = GameClass(self.line_bot_api)
            if hasattr(game, "set_database"):
                game.set_database(self.db)
            self.active_games[group_id] = game
            result = game.start_game()
            logger.info(f"Game started | {game_name} group={group_id}")
            return result if result else TextSendMessage(text="بدأت اللعبة")
        except Exception as e:
            logger.error(f"Start game error: {e}", exc_info=True)
            return TextSendMessage(text="فشل بدء اللعبة")

    def _start_text_game(self, game_name):
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
            with open(f"games/{files[game_name]}", "r", encoding="utf-8") as f:
                lines = [l.strip() for l in f if l.strip()]
            return TextSendMessage(text=random.choice(lines))
        except Exception as e:
            logger.error(f"Text game error: {e}")
            return TextSendMessage(text="فشل تحميل اللعبة")

    def _handle_game_answer(self, text, user_id, group_id, display_name):
        game = self.active_games.get(group_id)
        if not game:
            return TextSendMessage(text="اللعبة انتهت")
        try:
            result = game.check_answer(text, user_id, display_name)
            if result is None:
                return None
            if isinstance(result, TextSendMessage):
                return result
            if not isinstance(result, dict):
                return None
            points = result.get("points", 0)
            if points > 0:
                self.db.update_user_points(user_id, points, points > 0, "game")
            if result.get("game_over"):
                del self.active_games[group_id]
                logger.info(f"Game ended | group={group_id}")
            return result.get("response") or TextSendMessage(text=result.get("message", ""))
        except Exception as e:
            logger.error(f"Game error: {e}", exc_info=True)
            self.active_games.pop(group_id, None)
            return TextSendMessage(text="حدث خطأ في اللعبة")

    def stop_game(self, group_id):
        if group_id in self.active_games:
            del self.active_games[group_id]
            logger.info(f"Game stopped | group={group_id}")
            return True
        return False

    def _load_game(self, module_name, class_name):
        try:
            module = __import__(f"games.{module_name}", fromlist=[class_name])
            return getattr(module, class_name)
        except Exception as e:
            logger.error(f"Failed to load {class_name}: {e}")
            return None
