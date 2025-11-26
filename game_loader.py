"""
🎮 Bot Mesh v7.0 - Enhanced Game Loader (FIXED)
نظام تحميل الألعاب الذكي والمحسّن
Created by: Abeer Aldosari © 2025
"""

import os
import importlib
import logging
from typing import Dict, Optional, List

logger = logging.getLogger(__name__)


class GameLoader:
    """
    محمّل الألعاب المحسّن - نسخة مُصلحة
    - تحميل تلقائي ذكي
    - معالجة أخطاء شاملة
    - دعم أسماء عربية
    """

    # خريطة الأسماء العربية إلى أسماء ملفات الألعاب (الأسماء الصحيحة)
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
        "ترتيب": "order_game",
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
                
                # البحث عن كلاس Game
                if hasattr(module, "Game"):
                    game_class = getattr(module, "Game")
                    
                    # التحقق من أن الكلاس قابل للاستدعاء
                    if callable(game_class):
                        self.loaded_games[arabic_name] = game_class
                        success_count += 1
                        logger.info(f"✅ تم تحميل لعبة: {arabic_name}")
                    else:
                        logger.warning(f"⚠️ Game في {file_name}.py ليس كلاساً قابلاً للاستدعاء")
                        self.failed_games.append(arabic_name)
                else:
                    logger.warning(f"⚠️ لا يوجد كلاس Game في {file_name}.py")
                    self.failed_games.append(arabic_name)
                    
            except ImportError as e:
                logger.error(f"❌ فشل استيراد لعبة {arabic_name}: {e}")
                self.failed_games.append(arabic_name)
            except Exception as e:
                logger.error(f"❌ خطأ غير متوقع في تحميل {arabic_name}: {e}")
                self.failed_games.append(arabic_name)
        
        logger.info(f"🎮 تم تحميل {success_count} لعبة بنجاح")
        
        if self.failed_games:
            logger.warning(f"⚠️ فشل تحميل {len(self.failed_games)} لعبة: {', '.join(self.failed_games)}")

    def create_game(self, arabic_name: str):
        """
        إنشاء نسخة من اللعبة
        
        Args:
            arabic_name: الاسم العربي للعبة
            
        Returns:
            نسخة من اللعبة أو None في حالة الفشل
        """
        # التحقق من أن اللعبة محملة
        if arabic_name not in self.loaded_games:
            logger.warning(f"⚠️ اللعبة '{arabic_name}' غير متاحة")
            return None
        
        try:
            game_class = self.loaded_games[arabic_name]
            game_instance = game_class()
            
            logger.info(f"🎮 تم إنشاء نسخة من لعبة: {arabic_name}")
            return game_instance
            
        except Exception as e:
            logger.error(f"❌ خطأ في إنشاء لعبة {arabic_name}: {e}")
            return None

    def get_available_games(self) -> List[str]:
        """
        الحصول على قائمة الألعاب المتاحة
        
        Returns:
            قائمة بالأسماء العربية للألعاب المحملة
        """
        return list(self.loaded_games.keys())

    def get_game_count(self) -> int:
        """عدد الألعاب المحملة"""
        return len(self.loaded_games)

    def is_game_available(self, arabic_name: str) -> bool:
        """التحقق من توفر لعبة معينة"""
        return arabic_name in self.loaded_games

    def reload_game(self, arabic_name: str) -> bool:
        """
        إعادة تحميل لعبة معينة
        
        Args:
            arabic_name: الاسم العربي للعبة
            
        Returns:
            True إذا نجحت إعادة التحميل
        """
        if arabic_name not in self.GAME_MAPPING:
            logger.warning(f"⚠️ اللعبة '{arabic_name}' غير موجودة في الخريطة")
            return False
        
        file_name = self.GAME_MAPPING[arabic_name]
        
        try:
            # إعادة تحميل الوحدة
            module_path = f"{self.games_path}.{file_name}"
            
            # حذف من الذاكرة إذا كانت محملة
            if module_path in importlib.sys.modules:
                importlib.reload(importlib.sys.modules[module_path])
            else:
                importlib.import_module(module_path)
            
            module = importlib.sys.modules[module_path]
            
            if hasattr(module, "Game"):
                game_class = getattr(module, "Game")
                self.loaded_games[arabic_name] = game_class
                
                # إزالة من قائمة الفاشلة إذا كانت موجودة
                if arabic_name in self.failed_games:
                    self.failed_games.remove(arabic_name)
                
                logger.info(f"✅ تم إعادة تحميل لعبة: {arabic_name}")
                return True
            else:
                logger.warning(f"⚠️ لا يوجد كلاس Game في {file_name}.py")
                return False
                
        except Exception as e:
            logger.error(f"❌ فشلت إعادة تحميل {arabic_name}: {e}")
            return False

    def get_game_info(self, arabic_name: str) -> Optional[Dict]:
        """
        الحصول على معلومات لعبة
        
        Args:
            arabic_name: الاسم العربي للعبة
            
        Returns:
            معلومات اللعبة أو None
        """
        if not self.is_game_available(arabic_name):
            return None
        
        try:
            game = self.create_game(arabic_name)
            if game and hasattr(game, 'get_game_info'):
                return game.get_game_info()
            return None
        except Exception as e:
            logger.error(f"❌ خطأ في الحصول على معلومات {arabic_name}: {e}")
            return None

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
