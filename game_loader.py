# game_loader.py
"""
🎮 Bot Mesh v7.0 - Game Loader (PRODUCTION FIXED)
Created by: Abeer Aldosari © 2025
"""

import os
import importlib
import logging
from typing import Dict, List

logger = logging.getLogger(__name__)


class GameLoader:
    """محمّل الألعاب"""

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

    def __init__(self, games_path="games"):
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

        for arabic_name, file_name in self.GAME_MAPPING.items():
            try:
                module_path = f"{self.games_path}.{file_name}"
                module = importlib.import_module(module_path)

                game_class = None
                if hasattr(module, "Game"):
                    game_class = module.Game
                else:
                    for attr in dir(module):
                        if attr.endswith("Game"):
                            game_class = getattr(module, attr)
                            break

                if game_class:
                    self.loaded_games[arabic_name] = game_class
                    logger.info(f"✅ تم تحميل: {arabic_name}")
                else:
                    self.failed_games.append(arabic_name)

            except Exception as e:
                logger.error(f"❌ فشل تحميل {arabic_name}: {e}")
                self.failed_games.append(arabic_name)

        logger.info(f"🎮 تم تحميل {len(self.loaded_games)}/{len(self.GAME_MAPPING)}")

    def create_game(self, arabic_name: str):
        if arabic_name not in self.loaded_games:
            return None

        try:
            return self.loaded_games[arabic_name]()
        except TypeError:
            try:
                return self.loaded_games[arabic_name](line_bot_api=None)
            except:
                return None

    def get_available_games(self) -> List[str]:
        return list(self.loaded_games.keys())

    def get_loader_stats(self):
        return {
            "total": len(self.GAME_MAPPING),
            "loaded": len(self.loaded_games),
            "failed": len(self.failed_games)
        }
