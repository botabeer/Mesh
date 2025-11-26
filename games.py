"""
🎮 Bot Mesh v8.0 - Game Loader
Created by: Abeer Aldosari © 2025

✅ تحميل ديناميكي للألعاب
✅ إدارة الجلسات النشطة
✅ دعم 12 لعبة
"""

import os
import importlib
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)

class Games:
    """محمّل الألعاب الديناميكي"""
    
    # ربط الأسماء العربية بملفات الألعاب
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
        "إنسان حيوان": "human_animal_plant_game",
        "توافق": "compatibility_game"
    }
    
    def __init__(self, games_path="games"):
        """
        تهيئة المحمّل
        
        Args:
            games_path: مسار مجلد الألعاب
        """
        self.games_path = games_path
        self.loaded: Dict[str, type] = {}
        self.active_sessions: Dict[str, object] = {}
        self.failed: list = []
        
        # تحميل جميع الألعاب
        self.load_all()
    
    def load_all(self):
        """تحميل جميع الألعاب من المجلد"""
        logger.info("🎮 Loading games...")
        
        for arabic_name, file_name in self.GAME_MAPPING.items():
            try:
                # استيراد الملف
                module_path = f"{self.games_path}.{file_name}"
                module = importlib.import_module(module_path)
                
                # البحث عن كلاس Game
                game_class = None
                
                if hasattr(module, "Game"):
                    game_class = module.Game
                else:
                    # البحث عن أي كلاس ينتهي بـ Game
                    for attr in dir(module):
                        if attr.endswith("Game") and not attr.startswith("_"):
                            game_class = getattr(module, attr)
                            break
                
                if game_class:
                    self.loaded[arabic_name] = game_class
                    logger.info(f"  ✅ {arabic_name}")
                else:
                    self.failed.append(arabic_name)
                    logger.warning(f"  ⚠️ {arabic_name} - No Game class found")
                    
            except Exception as e:
                self.failed.append(arabic_name)
                logger.error(f"  ❌ {arabic_name} - {e}")
        
        logger.info(f"✅ Loaded {len(self.loaded)}/{len(self.GAME_MAPPING)} games")
        
        if self.failed:
            logger.warning(f"⚠️ Failed: {', '.join(self.failed)}")
    
    def start_game(self, user_id: str, game_name: str):
        """
        بدء لعبة جديدة
        
        Args:
            user_id: معرف المستخدم
            game_name: اسم اللعبة بالعربي
        
        Returns:
            رسالة Flex أو None
        """
        # التحقق من وجود اللعبة
        if game_name not in self.loaded:
            logger.warning(f"Game not found: {game_name}")
            return None
        
        try:
            # إنهاء اللعبة السابقة إن وجدت
            if user_id in self.active_sessions:
                self.end_game(user_id)
            
            # إنشاء نسخة جديدة من اللعبة
            GameClass = self.loaded[game_name]
            
            # محاولة إنشاء اللعبة (مع أو بدون line_bot_api)
            try:
                game = GameClass()
            except TypeError:
                # بعض الألعاب تحتاج line_bot_api
                game = GameClass(line_bot_api=None)
            
            # حفظ الجلسة
            self.active_sessions[user_id] = game
            
            # بدء اللعبة
            response = game.start()
            
            logger.info(f"🎮 {user_id} started {game_name}")
            return response
            
        except Exception as e:
            logger.error(f"❌ Error starting game {game_name}: {e}", exc_info=True)
            return None
    
    def get_game(self, user_id: str) -> Optional[object]:
        """
        الحصول على اللعبة النشطة
        
        Args:
            user_id: معرف المستخدم
        
        Returns:
            كائن اللعبة أو None
        """
        return self.active_sessions.get(user_id)
    
    def has_active_game(self, user_id: str) -> bool:
        """
        التحقق من وجود لعبة نشطة
        
        Args:
            user_id: معرف المستخدم
        
        Returns:
            True إذا كانت هناك لعبة نشطة
        """
        return user_id in self.active_sessions
    
    def end_game(self, user_id: str):
        """
        إنهاء اللعبة النشطة
        
        Args:
            user_id: معرف المستخدم
        """
        if user_id in self.active_sessions:
            game = self.active_sessions[user_id]
            game_name = game.game_name if hasattr(game, 'game_name') else 'Unknown'
            
            del self.active_sessions[user_id]
            logger.info(f"🛑 {user_id} ended {game_name}")
    
    def get_available_games(self) -> list:
        """
        الحصول على قائمة الألعاب المتاحة
        
        Returns:
            قائمة أسماء الألعاب بالعربي
        """
        return list(self.loaded.keys())
    
    def get_stats(self) -> dict:
        """
        الحصول على إحصائيات المحمّل
        
        Returns:
            dict مع معلومات الإحصائيات
        """
        return {
            'total_games': len(self.GAME_MAPPING),
            'loaded_games': len(self.loaded),
            'failed_games': len(self.failed),
            'active_sessions': len(self.active_sessions),
            'available_games': list(self.loaded.keys()),
            'failed_list': self.failed
        }
