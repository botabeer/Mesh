"""
🎮 Bot Mesh v7.0 - Game Loader (PRODUCTION FIXED)
"""

import os
import importlib
import logging
from typing import Dict, List

logger = logging.getLogger(__name__)


class GameLoader:
    GAME_MAPPING = {
        "ذكاء": "iq_game",
        "رياضيات": "math_game",
        "سرعة": "fast_typing_game",
        "كلمات": "scramble_word_game",
        "ألوان": "word_color_game",
        "أضداد": "opposite_game",
        "سلسلة": "chain_words_game",
        "تخمين": "guess_game",
        "أغنية": "song_game",
        "تكوين": "letters_words_game",
        "توافق": "compatibility_game",
        "إنسان حيوان": "human_animal_plant_game"
    }

    def __init__(self, games_path: str = "games"):
        self.games_path = games_path
        self.loaded_games: Dict[str, type] = {}
        self.failed_games: List[str] = []
        self.load_all_games()

    def load_all_games(self):
        self.loaded_games.clear()
        self.failed_games.clear()

        if not os.path.exists(self.games_path):
            logger.error(f"❌ مجلد الألعاب غير موجود: {self.games_path}")
            return

        success = 0

        for arabic_name, file_name in self.GAME_MAPPING.items():
            try:
                module_path = f"{self.games_path}.{file_name}"
                module = importlib.import_module(module_path)

                game_class = None

                if hasattr(module, "Game"):
                    game_class = getattr(module, "Game")

                if not game_class:
                    for attr in dir(module):
                        if attr.endswith("Game"):
                            obj = getattr(module, attr)
                            if callable(obj):
                                game_class = obj
                                break

                if game_class:
                    self.loaded_games[arabic_name] = game_class
                    success += 1
                    logger.info(f"✅ تم تحميل: {arabic_name}")
                else:
                    self.failed_games.append(arabic_name)
                    logger.warning(f"⚠️ لا يوجد كلاس في {file_name}.py")

            except Exception as e:
                logger.error(f"❌ فشل تحميل {arabic_name}: {e}")
                self.failed_games.append(arabic_name)

        logger.info(f"🎮 تم تحميل {success}/{len(self.GAME_MAPPING)}")

    def create_game(self, arabic_name: str):
        if arabic_name not in self.loaded_games:
            return None

        try:
            game_class = self.loaded_games[arabic_name]
            try:
                return game_class()
            except TypeError:
                return game_class(line_bot_api=None)
        except Exception as e:
            logger.error(f"❌ خطأ إنشاء اللعبة {arabic_name}: {e}")
            return None

    def get_available_games(self):
        return list(self.loaded_games.keys())


# ✅ كائن جاهز للاستيراد من app.py
game_loader = GameLoader()
