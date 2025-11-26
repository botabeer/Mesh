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
    مسؤول عن تحميل الألعاب من مجلد games/
    وربطها مع الأسماء العربية الرسمية
    """

    # خريطة الأسماء العربية إلى أسماء الملفات
    ARABIC_GAME_MAP = {
        "تخمين": "guess",
        "ذكاء": "iq",
        "رياضيات": "math",
        "سرعة": "speed",
        "سلسلة": "sequence",
        "ترتيب": "order",
        "تكوين": "compose",
        "كلمة ولون": "word_color",
        "أضداد": "opposites",
        "أغنية": "song",
        "لعبة": "play",
        "توافق": "match"
    }

    def __init__(self, games_path: str = "games"):
        self.games_path = games_path
        self.games = {}
        self.load_games()

    # ------------------------------------------------------------------

    def load_games(self):
        """
        تحميل جميع الألعاب من مجلد games
        """
        self.games.clear()

        if not os.path.exists(self.games_path):
            logger.error(f"❌ مجلد الألعاب غير موجود: {self.games_path}")
            return

        for arabic_name, file_name in self.ARABIC_GAME_MAP.items():
            try:
                module_path = f"{self.games_path}.{file_name}"
                module = importlib.import_module(module_path)

                if hasattr(module, "Game"):
                    self.games[arabic_name] = module.Game
                    logger.info(f"✅ تم تحميل لعبة: {arabic_name}")
                else:
                    logger.warning(f"⚠️ لا يوجد كلاس Game في {file_name}.py")

            except Exception as e:
                logger.error(f"❌ فشل تحميل لعبة {arabic_name}: {e}")

        logger.info(f"🎮 عدد الألعاب المحملة: {len(self.games)}")

    # ------------------------------------------------------------------

    def create_game(self, arabic_name: str):
        """
        إنشاء كائن لعبة بناءً على الاسم العربي
        """
        game_class = self.games.get(arabic_name)

        if not game_class:
            logger.warning(f"⚠️ لعبة غير موجودة: {arabic_name}")
            return None

        try:
            return game_class()
        except Exception as e:
            logger.error(f"❌ خطأ في إنشاء اللعبة {arabic_name}: {e}")
            return None

    # ------------------------------------------------------------------

    def get_available_games(self):
        """
        إرجاع قائمة الألعاب المتاحة بالأسماء العربية
        """
        return list(self.games.keys())
