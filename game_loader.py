"""
Bot Mesh v7.0 - Game Loader
تحميل الألعاب تلقائياً بأسماء عربية رسمية
"""

import os
import sys
import importlib
import inspect
import logging

logger = logging.getLogger(__name__)

class GameLoader:

    def __init__(self):
        self.games = {}

        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.games_dir = os.path.join(current_dir, 'games')

        if not os.path.exists(self.games_dir):
            logger.error("مجلد games غير موجود")
            return

        if self.games_dir not in sys.path:
            sys.path.insert(0, self.games_dir)

        self._load_games()

        if not self.games:
            logger.warning("لم يتم تحميل أي لعبة")

    def _load_games(self):

        game_mapping = {
            "iq_game": "ذكاء",
            "math_game": "رياضيات",
            "fast_typing_game": "سرعة",
            "letters_words_game": "تكوين",
            "word_color_game": "ألوان",
            "opposite_game": "أضداد",
            "chain_words_game": "سلسلة",
            "guess_game": "تخمين",
            "song_game": "أغنية",
            "scramble_word_game": "كلمات",
            "human_animal_plant_game": "لعبة",
            "compatibility_game": "توافق"
        }

        for file_name, game_name in game_mapping.items():
            try:
                module = importlib.import_module(file_name)

                for name, obj in inspect.getmembers(module, inspect.isclass):

                    if (
                        hasattr(obj, 'start') and
                        hasattr(obj, 'get_question') and
                        hasattr(obj, 'check_answer')
                    ):
                        self.games[game_name] = obj
                        logger.info(f"تم تحميل اللعبة: {game_name}")
                        break

            except Exception as e:
                logger.warning(f"{game_name}: الملف غير موجود أو به خطأ")

    def create_game(self, game_name):

        if game_name not in self.games:
            logger.warning(f"اللعبة غير موجودة: {game_name}")
            return None

        try:
            GameClass = self.games[game_name]
            return GameClass()
        except Exception as e:
            logger.error(f"خطأ في إنشاء اللعبة {game_name}")
            return None
