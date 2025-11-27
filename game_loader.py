"""
🎮 Bot Mesh v7.0 - Game Loader (PRODUCTION FIXED)
نظام تحميل الألعاب - نسخة مُصلحة للإنتاج
Created by: Abeer Aldosari © 2025
"""

import os
import importlib
import logging
from typing import Dict, Optional, List

logger = logging.getLogger(__name__)


class GameLoader:
    """محمّل الألعاب - نسخة الإنتاج المُصلحة"""

    # خريطة الأسماء العربية إلى ملفات الألعاب
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
        
        # تحميل الألعاب عند التهيئة
        self.load_all_games()

    def load_all_games(self):
        """تحميل جميع الألعاب المتاحة"""
        self.loaded_games.clear()
        self.failed_games.clear()
        
        if not os.path.exists(self.games_path):
            logger.error(f"❌ مجلد الألعاب غير موجود: {self.games_path}")
            return
        
        success_count = 0
        
        for arabic_name, file_name in self.GAME_MAPPING.items():
            try:
                # محاولة تحميل الوحدة
                module_path = f"{self.games_path}.{file_name}"
                module = importlib.import_module(module_path)
                
                # البحث عن كلاس Game (النمط الموحد)
                game_class = None
                
                # محاولة 1: البحث عن "Game"
                if hasattr(module, "Game"):
                    game_class = getattr(module, "Game")
                
                # محاولة 2: البحث عن أي كلاس ينتهي بـ "Game"
                if not game_class:
                    for attr_name in dir(module):
                        if attr_name.endswith("Game") and not attr_name.startswith("_"):
                            potential_class = getattr(module, attr_name)
                            if callable(potential_class):
                                game_class = potential_class
                                break
                
                if game_class and callable(game_class):
                    self.loaded_games[arabic_name] = game_class
                    success_count += 1
                    logger.info(f"✅ تم تحميل لعبة: {arabic_name}")
                else:
                    logger.warning(f"⚠️ لا يوجد كلاس Game في {file_name}.py")
                    self.failed_games.append(arabic_name)
                    
            except ImportError as e:
                logger.error(f"❌ فشل استيراد لعبة {arabic_name}: {e}")
                self.failed_games.append(arabic_name)
            except Exception as e:
                logger.error(f"❌ خطأ غير متوقع في تحميل {arabic_name}: {e}")
                self.failed_games.append(arabic_name)
        
        logger.info(f"🎮 تم تحميل {success_count}/{len(self.GAME_MAPPING)} لعبة بنجاح")
        
        if self.failed_games:
            logger.warning(f"⚠️ فشل تحميل: {', '.join(self.failed_games)}")

    def create_game(self, arabic_name: str):
        """
        إنشاء نسخة من اللعبة
        
        Args:
            arabic_name: الاسم العربي للعبة
            
        Returns:
            نسخة من اللعبة أو None في حالة الفشل
        """
        if arabic_name not in self.loaded_games:
            logger.warning(f"⚠️ اللعبة '{arabic_name}' غير متاحة")
            return None
        
        try:
            game_class = self.loaded_games[arabic_name]
            
            # إنشاء اللعبة بدون معاملات (النظام الجديد)
            try:
                game_instance = game_class()
                logger.info(f"🎮 تم إنشاء نسخة من لعبة: {arabic_name}")
                return game_instance
            except TypeError:
                # محاولة مع line_bot_api=None (للتوافق مع الألعاب القديمة)
                try:
                    game_instance = game_class(line_bot_api=None)
                    logger.info(f"🎮 تم إنشاء نسخة من لعبة (وضع التوافق): {arabic_name}")
                    return game_instance
                except:
                    logger.error(f"❌ فشل إنشاء لعبة {arabic_name}")
                    return None
            
        except Exception as e:
            logger.error(f"❌ خطأ في إنشاء لعبة {arabic_name}: {e}")
            return None

    def get_available_games(self) -> List[str]:
        """الحصول على قائمة الألعاب المتاحة"""
        return list(self.loaded_games.keys())

    def get_game_count(self) -> int:
        """عدد الألعاب المحملة"""
        return len(self.loaded_games)

    def is_game_available(self, arabic_name: str) -> bool:
        """التحقق من توفر لعبة معينة"""
        return arabic_name in self.loaded_games

    def get_loader_stats(self) -> Dict:
        """إحصائيات محمّل الألعاب"""
        return {
            "total_games": len(self.GAME_MAPPING),
            "loaded_games": len(self.loaded_games),
            "failed_games": len(self.failed_games),
            "success_rate": f"{(len(self.loaded_games) / len(self.GAME_MAPPING) * 100):.1f}%",
            "available_games": self.get_available_games(),
            "failed_list": self.failed_games
        }
