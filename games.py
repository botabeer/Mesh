"""
🎮 Bot Mesh v8.0 - Game Loader (Fixed & Enhanced)
محمّل الألعاب الديناميكي المحسّن
Created by: Abeer Aldosari © 2025

✅ Fixed class name: GameLoader
✅ Better error handling
✅ Session management
✅ Memory optimization
"""

import os
import importlib
import logging
from typing import Dict, Optional, List

logger = logging.getLogger(__name__)


class GameLoader:
    """محمّل الألعاب الديناميكي المحسّن"""
    
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
        "لعبة": "general_game",
        "توافق": "compatibility_game"
    }
    
    def __init__(self, games_path: str = "games"):
        """
        تهيئة المحمّل
        
        Args:
            games_path: مسار مجلد الألعاب
        """
        self.games_path = games_path
        self.loaded: Dict[str, type] = {}
        self.active_sessions: Dict[str, object] = {}
        self.failed: List[str] = []
        
        # تحميل جميع الألعاب
        self._load_all_games()
    
    def _load_all_games(self):
        """تحميل جميع الألعاب من المجلد"""
        logger.info("🎮 Loading games...")
        
        for arabic_name, file_name in self.GAME_MAPPING.items():
            try:
                # استيراد الملف
                module_path = f"{self.games_path}.{file_name}"
                module = importlib.import_module(module_path)
                
                # البحث عن كلاس Game
                game_class = self._find_game_class(module)
                
                if game_class:
                    self.loaded[arabic_name] = game_class
                    logger.info(f"  ✅ {arabic_name} ({game_class.__name__})")
                else:
                    self.failed.append(arabic_name)
                    logger.warning(f"  ⚠️ {arabic_name} - No Game class found")
                    
            except Exception as e:
                self.failed.append(arabic_name)
                logger.error(f"  ❌ {arabic_name} - {e}")
        
        logger.info(f"✅ Loaded {len(self.loaded)}/{len(self.GAME_MAPPING)} games")
        
        if self.failed:
            logger.warning(f"⚠️ Failed to load: {', '.join(self.failed)}")
    
    def _find_game_class(self, module):
        """البحث عن كلاس اللعبة في الموديول"""
        # محاولة 1: كلاس "Game"
        if hasattr(module, "Game"):
            return module.Game
        
        # محاولة 2: البحث عن أي كلاس ينتهي بـ "Game"
        for attr_name in dir(module):
            if attr_name.endswith("Game") and not attr_name.startswith("_"):
                attr = getattr(module, attr_name)
                if isinstance(attr, type):  # تأكد أنه كلاس
                    return attr
        
        return None
    
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
            logger.warning(f"❌ Game not found: {game_name}")
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
            # حذف الجلسة الفاشلة
            if user_id in self.active_sessions:
                del self.active_sessions[user_id]
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
            game_name = getattr(game, 'game_name', 'Unknown')
            
            del self.active_sessions[user_id]
            logger.info(f"🛑 {user_id} ended {game_name}")
    
    def get_available_games(self) -> List[str]:
        """
        الحصول على قائمة الألعاب المتاحة
        
        Returns:
            قائمة أسماء الألعاب بالعربي
        """
        return list(self.loaded.keys())
    
    def cleanup_inactive_sessions(self, timeout_minutes: int = 30):
        """
        تنظيف الجلسات غير النشطة (للاستخدام المستقبلي)
        
        Args:
            timeout_minutes: مدة عدم النشاط بالدقائق
        """
        # TODO: إضافة timestamp لكل جلسة وحذف القديمة
        pass
    
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
