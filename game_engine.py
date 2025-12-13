import logging
import random
from typing import Optional, Dict, Any

from linebot.models import TextSendMessage

logger = logging.getLogger(__name__)


class GameEngine:
    """
    GameEngine مسؤول فقط عن:
    - منطق الألعاب
    - إدارة حالة الألعاب
    - التسجيل
    لا يقوم بأي إرسال مباشر
    """

    def __init__(self, db):
        self.db = db

        # group_id -> game_instance
        self.active_games: Dict[str, Any] = {}

        # user_id set
        self.waiting_for_name = set()

        # تحميل الألعاب
        self.games = self._load_games()

        # تحميل الألعاب النصية مرة واحدة
        self.text_games = self._load_text_games()

    # ======================================================
    # Public API
    # ======================================================

    def set_waiting_for_name(self, user_id: str, waiting: bool):
        if waiting:
            self.waiting_for_name.add(user_id)
        else:
            self.waiting_for_name.discard(user_id)

    def process_message(
        self,
        text: str,
        user_id: str,
        group_id: str,
        display_name: str,
        is_registered: bool
    ) -> Optional[TextSendMessage]:

        text = text.strip()
        logger.info(f"GameEngine: {text} | user={user_id} group={group_id}")

        # تسجيل اسم
        if user_id in self.waiting_for_name:
            return self._handle_registration(text, user_id)

        # إجابة داخل لعبة
        if group_id in self.active_games:
            return self._handle_game_answer(text, user_id, group_id, display_name)

        # أمر جديد
        return self._handle_command(text, user_id, group_id, display_name, is_registered)

    def stop_game(self, group_id: str) -> bool:
        if group_id in self.active_games:
            del self.active_games[group_id]
            logger.info(f"Game stopped | group={group_id}")
            return True
        return False

    # ======================================================
    # Registration
    # ======================================================

    def _handle_registration(self, text: str, user_id: str) -> TextSendMessage:
        name = text.strip()

        if not (2 <= len(name) <= 20):
            return TextSendMessage(text="الاسم يجب أن يكون بين 2 و 20 حرف")

        self.db.register_or_update_user(user_id, name)
        self.waiting_for_name.discard(user_id)

        logger.info(f"User registered | user={user_id} name={name}")
        return TextSendMessage(text=f"تم التسجيل بنجاح\nالاسم: {name}")

    # ======================================================
    # Commands
    # ======================================================

    def _handle_command(
        self,
        text: str,
        user_id: str,
        group_id: str,
        display_name: str,
        is_registered: bool
    ) -> Optional[TextSendMessage]:

        # ألعاب نصية
        if text in self.text_games:
            if not is_registered:
                return TextSendMessage(text="يجب التسجيل أولاً\nاكتب: تسجيل")
            return TextSendMessage(text=random.choice(self.text_games[text]))

        # ألعاب تفاعلية
        if text in self.games:
            if not is_registered:
                return TextSendMessage(text="يجب التسجيل أولاً\nاكتب: تسجيل")
            return self._start_game(text, group_id)

        return None

    # ======================================================
    # Games
    # ======================================================

    def _start_game(self, game_name: str, group_id: str) -> TextSendMessage:
        GameClass = self.games.get(game_name)
        if not GameClass:
            return TextSendMessage(text="اللعبة غير متوفرة")

        try:
            game = GameClass()
            if hasattr(game, "set_database"):
                game.set_database(self.db)

            self.active_games[group_id] = game

            start_message = game.start_game()
            logger.info(f"Game started | {game_name} group={group_id}")

            return start_message or TextSendMessage(text="بدأت اللعبة")

        except Exception as e:
            logger.error(f"Start game error: {e}", exc_info=True)
            self.active_games.pop(group_id, None)
            return TextSendMessage(text="فشل بدء اللعبة")

    def _handle_game_answer(
        self,
        text: str,
        user_id: str,
        group_id: str,
        display_name: str
    ) -> Optional[TextSendMessage]:

        game = self.active_games.get(group_id)
        if not game:
            return None

        try:
            result = game.check_answer(text, user_id, display_name)

            if not result:
                return None

            # تحديث النقاط
            points = result.get("points", 0)
            if points > 0:
                self.db.update_user_points(user_id, points, True, "game")

            # إنهاء اللعبة
            if result.get("game_over"):
                self.active_games.pop(group_id, None)
                logger.info(f"Game ended | group={group_id}")

            return result.get("response") or TextSendMessage(
                text=result.get("message", "")
            )

        except Exception as e:
            logger.error(f"Game runtime error: {e}", exc_info=True)
            self.active_games.pop(group_id, None)
            return TextSendMessage(text="حدث خطأ في اللعبة")

    # ======================================================
    # Loaders
    # ======================================================

    def _load_games(self) -> Dict[str, Any]:
        games = {}

        mapping = {
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

        for name, (module, cls) in mapping.items():
            try:
                mod = __import__(f"games.{module}", fromlist=[cls])
                games[name] = getattr(mod, cls)
            except Exception as e:
                logger.error(f"Failed loading game {name}: {e}")

        return games

    def _load_text_games(self) -> Dict[str, list]:
        files = {
            "سؤال": "questions.txt",
            "منشن": "mentions.txt",
            "تحدي": "challenges.txt",
            "اعتراف": "confessions.txt",
            "موقف": "situations.txt",
            "اقتباس": "quotes.txt",
        }

        data = {}
        for key, file in files.items():
            try:
                with open(f"games/{file}", "r", encoding="utf-8") as f:
                    data[key] = [l.strip() for l in f if l.strip()]
            except Exception as e:
                logger.error(f"Failed loading text game {key}: {e}")
                data[key] = ["اللعبة غير متوفرة حالياً"]

        return data
