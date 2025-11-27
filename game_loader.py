"""
🎮 Bot Mesh v7.0 - Game Loader (النسخة المحسّنة)
تحميل الألعاب تلقائياً من مجلد games/
Created by: Abeer Aldosari © 2025
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
        
        # تحديد مسار مجلد games
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.games_dir = os.path.join(current_dir, 'games')
        
        # التحقق من وجود المجلد
        if not os.path.exists(self.games_dir):
            logger.error(f"❌ مجلد games/ غير موجود في: {self.games_dir}")
            # محاولة إنشاء المجلد
            try:
                os.makedirs(self.games_dir)
                logger.info(f"✅ تم إنشاء مجلد games/ في: {self.games_dir}")
            except Exception as e:
                logger.error(f"❌ فشل إنشاء المجلد: {e}")
                return

        # إضافة مجلد games للمسار
        if self.games_dir not in sys.path:
            sys.path.insert(0, self.games_dir)

        # تحميل الألعاب
        self._load_games()

        if len(self.games) > 0:
            logger.info(f"✅ تم تحميل {len(self.games)} لعبة بنجاح")
        else:
            logger.warning("⚠️ لم يتم تحميل أي لعبة!")

    def _load_games(self):
        """تحميل جميع الألعاب من مجلد games/"""
        
        # خريطة الألعاب (اسم الملف ← اسم اللعبة في القائمة)
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
            "human_animal_plant_game": "إنسان حيوان",
            "compatibility_game": "توافق",
            "scramble_word_game": "كلمات"
        }

        for file_name, game_name in game_mapping.items():
            try:
                # استيراد الوحدة
                module = importlib.import_module(file_name)

                # البحث عن كلاس اللعبة
                game_class_found = False
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    # تحقق من أن الكلاس يحتوي على الميثودات المطلوبة
                    if (hasattr(obj, 'start_game') or hasattr(obj, 'start')) and \
                       (hasattr(obj, 'check_answer')) and \
                       ('Game' in name):
                        
                        self.games[game_name] = obj
                        logger.info(f"  ✓ {game_name} ({name})")
                        game_class_found = True
                        break
                
                if not game_class_found:
                    logger.warning(f"  ⚠️ {game_name}: لم يتم العثور على كلاس مناسب")

            except ModuleNotFoundError:
                logger.warning(f"  ⚠️ {game_name}: الملف {file_name}.py غير موجود")
            except Exception as e:
                logger.error(f"  ✗ فشل تحميل {game_name}: {type(e).__name__}: {e}")

    def create_game(self, game_name: str, line_bot_api=None):
        """
        إنشاء نسخة من اللعبة
        
        Args:
            game_name: اسم اللعبة (مثل "ذكاء")
            line_bot_api: واجهة LINE Bot API (اختياري)
        
        Returns:
            game_instance أو None
        """
        if game_name not in self.games:
            logger.warning(f"⚠️ لعبة '{game_name}' غير موجودة")
            logger.info(f"الألعاب المتاحة: {', '.join(self.games.keys())}")
            return None
        
        try:
            GameClass = self.games[game_name]
            
            # محاولة إنشاء اللعبة مع line_bot_api
            try:
                if line_bot_api:
                    return GameClass(line_bot_api)
                else:
                    return GameClass()
            except TypeError:
                # إذا فشل، حاول بدون معاملات
                try:
                    return GameClass()
                except:
                    logger.error(f"❌ فشل إنشاء {game_name} بدون معاملات")
                    return None
                
        except Exception as e:
            logger.error(f"❌ خطأ في إنشاء لعبة {game_name}: {type(e).__name__}: {e}")
            return None

    def get_available_games(self) -> list:
        """الحصول على قائمة الألعاب المتاحة"""
        return list(self.games.keys())
    
    def get_game_info(self, game_name: str) -> dict:
        """الحصول على معلومات اللعبة"""
        if game_name not in self.games:
            return None
        
        try:
            GameClass = self.games[game_name]
            # محاولة الحصول على معلومات من الكلاس
            if hasattr(GameClass, 'get_game_info'):
                try:
                    temp_game = GameClass()
                    return temp_game.get_game_info()
                except:
                    pass
            
            return {
                "name": game_name,
                "available": True,
                "class": GameClass.__name__
            }
        except Exception as e:
            logger.error(f"❌ خطأ في الحصول على معلومات {game_name}: {e}")
            return {
                "name": game_name,
                "available": False,
                "error": str(e)
            }

    def reload_games(self):
        """إعادة تحميل جميع الألعاب"""
        logger.info("🔄 إعادة تحميل الألعاب...")
        self.games.clear()
        self._load_games()
        logger.info(f"✅ تم إعادة تحميل {len(self.games)} لعبة")
