import importlib
import logging
from typing import Dict, Optional, List

logger = logging.getLogger(__name__)

class GameLoader:
    """محمّل الألعاب المبسط"""
    
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
    
    def __init__(self):
        self.loaded: Dict[str, type] = {}  # ✅ التعريف الصحيح
        self.active_sessions: Dict[str, object] = {}
        self._load_all_games()
    
    def _load_all_games(self):
        """تحميل الألعاب"""
        logger.info("🎮 جاري تحميل الألعاب...")
        
        for arabic_name, file_name in self.GAME_MAPPING.items():
            try:
                module = importlib.import_module(f"games.{file_name}")
                
                # البحث عن Game class
                game_class = None
                if hasattr(module, "Game"):
                    game_class = module.Game
                else:
                    for attr_name in dir(module):
                        if attr_name.endswith("Game") and not attr_name.startswith("_"):
                            attr = getattr(module, attr_name)
                            if isinstance(attr, type):
                                game_class = attr
                                break
                
                if game_class:
                    self.loaded[arabic_name] = game_class
                    logger.info(f"  ✅ {arabic_name} ({file_name})")
                else:
                    logger.warning(f"  ⚠️ {arabic_name} - لم يتم العثور على Game class")
                    
            except Exception as e:
                logger.error(f"  ❌ {arabic_name} - خطأ: {e}")
        
        logger.info(f"✅ تم تحميل {len(self.loaded)}/{len(self.GAME_MAPPING)} لعبة")
    
    def start_game(self, user_id: str, game_name: str):
        """بدء لعبة"""
        if game_name not in self.loaded:
            logger.warning(f"⚠️ اللعبة '{game_name}' غير موجودة")
            return None
        
        try:
            # إنهاء اللعبة السابقة إن وجدت
            if user_id in self.active_sessions:
                self.end_game(user_id)
            
            GameClass = self.loaded[game_name]
            
            # محاولة إنشاء نسخة من اللعبة
            try:
                game = GameClass()
            except TypeError:
                # بعض الألعاب تحتاج line_bot_api
                game = GameClass(line_bot_api=None)
            
            self.active_sessions[user_id] = game
            
            # بدء اللعبة
            if hasattr(game, 'start_game'):
                response = game.start_game()
            elif hasattr(game, 'start'):
                response = game.start()
            else:
                raise AttributeError("اللعبة لا تحتوي على start() أو start_game()")
            
            logger.info(f"🎮 {user_id} بدأ لعبة {game_name}")
            return response
            
        except Exception as e:
            logger.error(f"❌ خطأ في بدء اللعبة {game_name}: {e}", exc_info=True)
            if user_id in self.active_sessions:
                del self.active_sessions[user_id]
            return None
    
    def get_game(self, user_id: str):
        """الحصول على اللعبة النشطة للمستخدم"""
        return self.active_sessions.get(user_id)
    
    def has_active_game(self, user_id: str) -> bool:
        """التحقق من وجود لعبة نشطة"""
        return user_id in self.active_sessions
    
    def end_game(self, user_id: str):
        """إنهاء اللعبة"""
        if user_id in self.active_sessions:
            del self.active_sessions[user_id]
            logger.info(f"🛑 {user_id} أنهى اللعبة")
    
    def get_available_games(self) -> List[str]:
        """قائمة الألعاب المتاحة"""
        return list(self.loaded.keys())
    
    def get_stats(self) -> Dict:
        """إحصائيات محمّل الألعاب"""
        return {
            'total_games': len(self.GAME_MAPPING),
            'loaded_games': len(self.loaded),
            'active_sessions': len(self.active_sessions),
            'available_games': list(self.loaded.keys())
        }
