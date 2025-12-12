import logging
from typing import Dict, Optional
from linebot.v3.messaging import TextMessage
from config import Config

logger = logging.getLogger(__name__)


class GameManager:
    """إدارة الألعاب وتشغيلها ومتابعة الجلسات والنتائج."""

    def __init__(self, db):
        self.db = db
        self.active_games: Dict[str, object] = {}  # context_id -> game instance
        self.game_sessions: Dict[str, dict] = {}   # context_id -> session info
        self.games = self._load_games()
        logger.info(f"Loaded {len(self.games)} games")

    # ----------------------------------------------------------------------
    def _load_games(self) -> Dict[str, type]:
        """تحميل جميع الألعاب من ملفاتها الخاصة."""
        try:
            from games.iq_game import IqGame
            from games.guess_game import GuessGame
            from games.opposite_game import OppositeGame
            from games.scramble_word_game import ScrambleWordGame
            from games.math_game import MathGame
            from games.song_game import SongGame
            from games.word_color_game import WordColorGame
            from games.letters_words_game import LettersWordsGame
            from games.human_animal_plant_game import HumanAnimalPlantGame
            from games.chain_words_game import ChainWordsGame
            from games.fast_typing_game import FastTypingGame

            from text_games import QuestionGame, MentionGame, ChallengeGame, ConfessionGame
            from games.compatibility_game import CompatibilityGame
            from games.mafia_game import MafiaGame

            return {
                "ذكاء": IqGame,
                "خمن": GuessGame,
                "ضد": OppositeGame,
                "ترتيب": ScrambleWordGame,
                "رياضيات": MathGame,
                "اغنيه": SongGame,
                "لون": WordColorGame,
                "تكوين": LettersWordsGame,
                "لعبة": HumanAnimalPlantGame,
                "سلسلة": ChainWordsGame,
                "اسرع": FastTypingGame,

                "سؤال": QuestionGame,
                "منشن": MentionGame,
                "تحدي": ChallengeGame,
                "اعتراف": ConfessionGame,
                "توافق": CompatibilityGame,
                "مافيا": MafiaGame,
            }

        except Exception as e:
            logger.error(f"Error loading games: {e}", exc_info=True)
            return {}

    # ----------------------------------------------------------------------
    def get_active_count(self) -> int:
        """عدد الألعاب النشطة حاليًا."""
        return len(self.active_games)

    # ----------------------------------------------------------------------
    def is_game_active(self, context_id: str) -> bool:
        """التحقق مما إذا كانت هناك لعبة نشطة في السياق المحدد."""
        return context_id in self.active_games

    # ----------------------------------------------------------------------
    def stop_game(self, context_id: str) -> Optional[str]:
        """إيقاف اللعبة النشطة في السياق وإزالة الجلسة."""
        game = self.active_games.pop(context_id, None)
        self.game_sessions.pop(context_id, None)
        if game:
            logger.info(f"Stopped game {game.game_name}")
            return game.game_name
        return None

    # ----------------------------------------------------------------------
    def start_game(self, context_id: str, game_name: str, user_id: str,
                   username: str, is_registered: bool, theme: str,
                   source_type: str) -> dict:
        """بدء لعبة جديدة حسب الاسم والسياق."""
        if game_name not in self.games:
            return {"messages": [TextMessage(text="اللعبة غير موجودة")], "points": 0}

        is_point_game = game_name in Config.POINT_GAMES
        is_fun_game = game_name in Config.FUN_GAMES

        # التحقق من التسجيل للألعاب بالنقاط
        if is_point_game and not is_registered:
            return {"messages": [TextMessage(text="يجب التسجيل اولا\nاكتب: انضم")], "points": 0}

        # التحقق من قيود الألعاب الجماعية
        if is_fun_game:
            game_cfg = Config.FUN_GAMES.get(game_name, {})
            if game_cfg.get("group_only") and source_type not in ("group", "room"):
                return {"messages": [TextMessage(text="هذه اللعبة للمجموعات فقط")], "points": 0}

        try:
            GameClass = self.games[game_name]
            game = GameClass(None)

            if hasattr(game, "set_theme"):
                game.set_theme(theme)
            if hasattr(game, "set_database"):
                game.set_database(self.db)

            self.active_games[context_id] = game

            # إنشاء جلسة للألعاب بالنقاط
            if is_point_game:
                session_id = self.db.create_session(user_id, game_name)
                self.game_sessions[context_id] = {
                    "session_id": session_id,
                    "user_id": user_id,
                    "game_name": game_name
                }

            q = game.start_game()
            logger.info(f"Started game {game_name} for {user_id}")
            return {"messages": [q], "points": 0}

        except Exception as e:
            logger.error(f"Error starting game {game_name}: {e}", exc_info=True)
            return {"messages": [TextMessage(text="خطأ في بدء اللعبة")], "points": 0}

    # ----------------------------------------------------------------------
    def process_message(self, context_id: str, user_id: str, username: str,
                        text: str, is_registered: bool, theme: str,
                        source_type: str) -> Optional[dict]:
        """معالجة الرسائل الواردة وتشغيل الألعاب أو التحقق من الإجابات."""
        norm = Config.normalize(text)

        # بدء اللعبة مباشرة إذا كان النص اسم لعبة
        if norm in self.games:
            return self.start_game(context_id, norm, user_id, username,
                                   is_registered, theme, source_type)

        # إذا لا توجد لعبة نشطة في السياق
        if context_id not in self.active_games:
            return None

        game = self.active_games[context_id]

        try:
            result = game.check_answer(text, user_id, username)
            if not result:
                return None

            msgs = []
            pts = result.get("points", 0)

            if result.get("message"):
                msgs.append(TextMessage(text=result["message"]))
            if result.get("response"):
                msgs.append(result["response"])

            # إنهاء اللعبة إذا انتهت
            if result.get("game_over"):
                sess = self.game_sessions.pop(context_id, None)
                self.active_games.pop(context_id, None)

                if sess:
                    self.db.complete_session(sess["session_id"], pts)

                if pts > 0 and is_registered:
                    self.db.record_game_stat(user_id, game.game_name, pts, True)

                logger.info(f"Game finished: {game.game_name}, User={user_id}, Points={pts}")

            return {"messages": msgs, "points": pts}

        except Exception as e:
            logger.error(f"Error processing answer in {game.game_name}: {e}", exc_info=True)
            return None
