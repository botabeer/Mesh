"""
Bot Mesh v7.0 - Game Loader
تم إنشاء هذا البوت بواسطة عبير الدوسري © 2025
"""

import os
import importlib
import logging

logger = logging.getLogger(__name__)


class GameLoader:
    """
    مدير تحميل الألعاب من مجلد games/
    مع ربط الأسماء العربية بالملفات البرمجية
    """

    # خريطة الأسماء العربية -> أسماء الملفات داخل مجلد games
    GAME_MAP = {
        "تخمين": "guess_game",
        "ذكاء": "iq_game",
        "رياضيات": "math_game",
        "سرعة": "speed_game",
        "سلسلة": "sequence_game",
        "ترتيب": "order_game",
        "تكوين": "build_game",
        "كلمة ولون": "word_color_game",
        "أضداد": "opposites_game",
        "أغنية": "song_game",
        "لعبة": "general_game",
        "توافق": "match_game"
    }

    def __init__(self, games_folder="games"):
        self.games_folder = games_folder
        self.games = {}
        self.load_games()

    # --------------------------------------------------
    # تحميل جميع الألعاب عند بدء التشغيل
    # --------------------------------------------------
    def load_games(self):
        if not os.path.exists(self.games_folder):
            logger.warning(f"مجلد الألعاب غير موجود: {self.games_folder}")
            return

        for arabic_name, file_name in self.GAME_MAP.items():
            try:
                module_path = f"{self.games_folder}.{file_name}"
                module = importlib.import_module(module_path)

                if hasattr(module, "Game"):
                    self.games[arabic_name] = module.Game
                    logger.info(f"تم تحميل اللعبة: {arabic_name}")
                else:
                    logger.warning(f"الملف {file_name} لا يحتوي على Game class")

            except Exception as e:
                logger.error(f"فشل تحميل اللعبة {arabic_name}: {e}")

    # --------------------------------------------------
    # إنشاء كائن لعبة جديد حسب الاسم العربي
    # --------------------------------------------------
    def create_game(self, arabic_name):
        game_class = self.games.get(arabic_name)

        if not game_class:
            logger.warning(f"لعبة غير مسجلة: {arabic_name}")
            return None

        try:
            return game_class()
        except Exception as e:
            logger.error(f"خطأ في إنشاء اللعبة {arabic_name}: {e}")
            return None

    # --------------------------------------------------
    # إرجاع قائمة الألعاب المتاحة
    # --------------------------------------------------
    def list_games(self):
        return list(self.games.keys())
