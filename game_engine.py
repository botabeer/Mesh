import logging
from typing import Any, Dict
from linebot.models import TextSendMessage
from ui_builder import UIBuilder

logger = logging.getLogger(__name__)

class GameEngine:
    STATE_IDLE = "idle"
    STATE_MENU = "menu"
    STATE_WAITING_NAME = "waiting_name"
    STATE_IN_GAME = "in_game"

    def __init__(self, line_bot_api, db):
        self.line_bot_api = line_bot_api
        self.db = db
        self.ui = UIBuilder()
        self.session_states: Dict[str, str] = {}
        self.active_games: Dict[str, Any] = {}
        
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

    def process_message(self, text: str, user_id: str, group_id: str, display_name: str):
        text = text.strip()
        normalized = text.lower()
        state = self.session_states.get(group_id, self.STATE_IDLE)
        user_data = self.db.get_user(user_id)

        if state == self.STATE_WAITING_NAME:
            return self._handle_registration(text, user_id)

        if state == self.STATE_IN_GAME:
            return self._handle_game_answer(text, user_id, group_id, display_name)

        return self._handle_command(normalized, text, user_id, group_id, display_name, user_data)

    def _handle_command(self, normalized, original, user_id, group_id, display_name, user_data):
        is_registered = user_data is not None

        if normalized in ["بداية", "start"]:
            self.session_states[group_id] = self.STATE_MENU
            points = user_data["points"] if user_data else 0
            return self.ui.welcome_card(display_name, is_registered, points)

        if normalized in ["مساعدة", "help"]:
            return self.ui.help_card()

        if normalized in ["العاب", "ألعاب", "games"]:
            return self.ui.games_menu_card()

        if normalized in ["تسجيل", "register"]:
            self.session_states[group_id] = self.STATE_WAITING_NAME
            if is_registered:
                return TextSendMessage(text=f"انت مسجل باسم: {user_data['name']}\n\nاكتب الاسم الجديد:")
            return TextSendMessage(text="اكتب اسمك للتسجيل:")

        if normalized in ["نقاطي", "احصائياتي", "stats"]:
            if not is_registered:
                return TextSendMessage(text="يجب التسجيل اولا\nاكتب: تسجيل")
            return self.ui.stats_card(display_name, user_data)

        if normalized in ["الصدارة", "المتصدرين", "top"]:
            leaders = self.db.get_leaderboard(20)
            return self.ui.leaderboard_card(leaders)

        if normalized in ["ايقاف", "stop", "انهاء"]:
            if group_id in self.active_games:
                del self.active_games[group_id]
                self.session_states[group_id] = self.STATE_MENU
                return TextSendMessage(text="تم ايقاف اللعبة")
            return TextSendMessage(text="لا توجد لعبة نشطة")

        if original in self.games or original in self.text_games:
            if not is_registered:
                return TextSendMessage(text="يجب التسجيل اولا\nاكتب: تسجيل")
            self.session_states[group_id] = self.STATE_IN_GAME
            return self._start_game(original, user_id, group_id)

        return TextSendMessage(text="اكتب 'بداية' للبدء")

    def _handle_registration(self, text: str, user_id: str):
        name = text.strip()
        if len(name) < 2 or len(name) > 20:
            return TextSendMessage(text="الاسم يجب أن يكون بين 2 و 20 حرف")

        self.db.create_user(user_id, name)
        self.db.update_user(user_id, is_registered=1)
        self.session_states[user_id] = self.STATE_MENU
        return self.ui.registration_success(name, 0, "light")

    def _start_game(self, game_name: str, user_id: str, group_id: str):
        if game_name in self.text_games:
            return self._start_text_game(game_name)

        GameClass = self.games.get(game_name)
        if not GameClass:
            return TextSendMessage(text="اللعبة غير متوفرة")

        try:
            game = GameClass(self.line_bot_api)
            game.set_database(self.db)
            self.active_games[group_id] = game
            return game.start_game()
        except Exception as e:
            logger.error(f"Start game error: {e}", exc_info=True)
            self.session_states[group_id] = self.STATE_MENU
            return TextSendMessage(text="فشل بدء اللعبة")

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
            with open(f"games/{files[game_name]}", "r", encoding="utf-8") as f:
                lines = [l.strip() for l in f if l.strip()]
            return TextSendMessage(text=random.choice(lines))
        except Exception as e:
            logger.error(f"Text game error: {e}")
            return TextSendMessage(text="فشل تحميل اللعبة")

    def _handle_game_answer(self, text: str, user_id: str, group_id: str, display_name: str):
        game = self.active_games.get(group_id)
        if not game:
            self.session_states[group_id] = self.STATE_MENU
            return TextSendMessage(text="اللعبة انتهت")

        try:
            result = game.check_answer(text, user_id, display_name)
            if isinstance(result, TextSendMessage):
                return result
            if not isinstance(result, dict):
                return None

            points = result.get("points", 0)
            if points > 0:
                self.db.add_points(user_id, points)

            if result.get("game_over"):
                del self.active_games[group_id]
                self.session_states[group_id] = self.STATE_MENU

            return result.get("response") or TextSendMessage(text=result.get("message", ""))

        except Exception as e:
            logger.error(f"Game error: {e}", exc_info=True)
            self.active_games.pop(group_id, None)
            self.session_states[group_id] = self.STATE_MENU
            return TextSendMessage(text="حدث خطأ في اللعبة")

    def _load_game(self, module_name: str, class_name: str):
        try:
            module = __import__(f"games.{module_name}", fromlist=[class_name])
            return getattr(module, class_name)
        except Exception as e:
            logger.error(f"Failed to load {class_name}: {e}")
            return None
