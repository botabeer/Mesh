"""
🎮 Bot Mesh v7.0 - Game Loader
تحميل الألعاب تلقائياً من ملفاتها الصحيحة
"""

import os
import sys
import importlib
import inspect
import logging

logger = logging.getLogger(__name__)


class GameLoader:
    """محمّل الألعاب التلقائي"""

    def __init__(self):
        """تهيئة المحمّل"""
        self.games = {}
        self.games_dir = os.path.dirname(__file__)

        # إضافة مجلد games للمسار
        if self.games_dir not in sys.path:
            sys.path.insert(0, self.games_dir)

        # تحميل الألعاب
        self._load_games()

        logger.info(f"✅ تم تحميل {len(self.games)} لعبة")

    def _load_games(self):
        """تحميل جميع الألعاب من مجلد games/"""
        if not os.path.exists(self.games_dir):
            logger.warning(f"❌ مجلد {self.games_dir} غير موجود")
            return

        # ✅ ربط مباشر مع ملفاتك الحقيقية
        game_mapping = {
            "iq_game": "ذكاء",
            "math_game": "رياضيات",
            "fast_typing_game": "سرعة",
            "letters_words_game": "كلمات",
            "word_color_game": "ألوان",
            "opposite_game": "أضداد",
            "chain_words_game": "سلسلة",
            "guess_game": "تخمين",
            "song_game": "أغنية",
            "human_animal_plant_game": "إنسان حيوان",
            "compatibility_game": "توافق",
            "scramble_word_game": "تكوين"
        }

        for file_name, game_name in game_mapping.items():
            try:
                module = importlib.import_module(file_name)

                for name, obj in inspect.getmembers(module, inspect.isclass):
                    if hasattr(obj, "start") and hasattr(obj, "check_answer"):
                        self.games[game_name] = obj
                        logger.info(f"  ✓ {game_name}")
                        break

            except Exception as e:
                logger.error(f"  ✗ فشل تحميل {game_name}: {e}")

    def create_game(self, game_name: str):
        """إنشاء نسخة من اللعبة"""
        if game_name in self.games:
            try:
                GameClass = self.games[game_name]
                return GameClass()
            except Exception as e:
                logger.error(f"❌ خطأ في إنشاء لعبة {game_name}: {e}")
                return None

        logger.warning(f"⚠️ لعبة '{game_name}' غير موجودة")
        return None

    def get_available_games(self) -> list:
        """الحصول على قائمة الألعاب المتاحة"""
        return list(self.games.keys())
