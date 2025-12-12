import logging
from typing import Dict, Optional
from linebot.v3.messaging import TextMessage
from config import Config

logger = logging.getLogger(__name__)


class GameManager:
    """مدير الألعاب المركزي"""

    def __init__(self, db):
        self.db = db
        self.active_games: Dict[str, object] = {}
        self.game_sessions: Dict[str, dict] = {}
        self.games = self._load_games()
        logger.info(f"تم تحميل {len(self.games)} لعبة")

    def _load_games(self) -> Dict[str, type]:
        """تحميل الألعاب"""
        try:
            from games.iq_game import IqGame
            from games.guess_game import GuessGame
            from games.opposite_game import OppositeGame
            from games.scramble_word_game import ScrambleWordGame
            from games.math_game import MathGame
            from games.compatibility_game import CompatibilityGame
            from games.song_game import SongGame
            from games.word_color_game import WordColorGame
            from games.letters_words_game import LettersWordsGame
            from games.human_animal_plant_game import HumanAnimalPlantGame
            from games.chain_words_game import ChainWordsGame
            from games.fast_typing_game import FastTypingGame
            from games.roulette_game import RouletteGame
            
            return {
                "ذكاء": IqGame,
                "خمن": GuessGame,
                "ضد": OppositeGame,
                "ترتيب": ScrambleWordGame,
                "رياضيات": MathGame,
                "توافق": CompatibilityGame,
                "اغنيه": SongGame,
                "لون": WordColorGame,
                "تكوين": LettersWordsGame,
                "لعبة": HumanAnimalPlantGame,
                "سلسلة": ChainWordsGame,
                "اسرع": FastTypingGame,
                "روليت": RouletteGame
            }
        except Exception as e:
            logger.error(f"خطأ في تحميل الألعاب: {e}", exc_info=True)
            return {}

    def get_active_count(self) -> int:
        """عدد الألعاب النشطة"""
        return len(self.active_games)

    def get_total_games(self) -> int:
        """إجمالي الألعاب"""
        return len(self.games)

    def is_game_active(self, context_id: str) -> bool:
        """التحقق من وجود لعبة نشطة"""
        return context_id in self.active_games

    def stop_game(self, context_id: str) -> Optional[str]:
        """إيقاف لعبة نشطة"""
        game = self.active_games.pop(context_id, None)
        self.game_sessions.pop(context_id, None)
        
        if game:
            logger.info(f"تم إيقاف لعبة {game.game_name}")
            return game.game_name
        
        return None

    def start_game(self, context_id: str, game_name: str, user_id: str,
                   username: str, is_registered: bool, theme: str,
                   source_type: str) -> Optional[Dict]:
        """بدء لعبة جديدة"""
        if game_name not in self.games:
            return {"messages": [TextMessage(text="اللعبة غير موجودة")], "points": 0}
        
        config = Config.get_game_config(game_name)
        
        if config.get("requires_registration") and not is_registered:
            return {"messages": [TextMessage(text="يجب التسجيل اولا\nاكتب: انضم")], "points": 0}
        
        if config.get("group_only") and source_type not in ("group", "room"):
            return {"messages": [TextMessage(text="هذه اللعبة للمجموعات فقط")], "points": 0}
        
        try:
            GameClass = self.games[game_name]
            game = GameClass(None)
            
            if hasattr(game, "set_theme"):
                game.set_theme(theme)
            
            if hasattr(game, "set_database"):
                game.set_database(self.db)
            
            self.active_games[context_id] = game
            
            if config.get("requires_registration"):
                session_id = self.db.create_session(user_id, game_name)
                self.game_sessions[context_id] = {
                    "session_id": session_id,
                    "user_id": user_id,
                    "game_name": game_name
                }
            
            question = game.start_game()
            logger.info(f"تم بدء لعبة {game_name}")
            
            return {"messages": [question], "points": 0}
        
        except Exception as e:
            logger.error(f"خطأ في بدء اللعبة: {e}", exc_info=True)
            return {"messages": [TextMessage(text="حدث خطأ في بدء اللعبة")], "points": 0}

    def process_message(self, context_id: str, user_id: str, username: str,
                        text: str, is_registered: bool, theme: str,
                        source_type: str) -> Optional[Dict]:
        """معالجة رسالة المستخدم"""
        normalized = Config.normalize(text)
        
        if normalized in self.games:
            return self.start_game(context_id, normalized, user_id, username,
                                   is_registered, theme, source_type)
        
        if context_id not in self.active_games:
            return None
        
        game = self.active_games[context_id]
        
        try:
            result = game.check_answer(text, user_id, username)
            if not result:
                return None
            
            messages = []
            points = result.get("points", 0)
            
            if result.get("message"):
                messages.append(TextMessage(text=result["message"]))
            
            if result.get("game_over"):
                session = self.game_sessions.pop(context_id, None)
                self.active_games.pop(context_id, None)
                
                if session:
                    self.db.complete_session(session["session_id"], points)
                
                if points > 0 and is_registered:
                    self.db.record_game_stat(user_id, game.game_name, points, True)
                
                logger.info(f"انتهت لعبة {game.game_name} - النقاط: {points}")
            
            elif result.get("response"):
                messages.append(result["response"])
            
            return {"messages": messages, "points": points}
        
        except Exception as e:
            logger.error(f"خطأ في معالجة الإجابة: {e}", exc_info=True)
            return None
