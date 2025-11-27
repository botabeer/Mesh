"""
Game Loader - Bot Mesh v9.0 (Simplified)
"""

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
        self.loaded: Dict[str, type] = {}
        self.active_sessions: Dict[str, object] = {}
        self._load_all_games()
    
    def _load_all_games(self):
        """تحميل الألعاب"""
        logger.info("Loading games...")
        
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
                    logger.info(f"  ✅ {arabic_name}")
                else:
                    logger.warning(f"  ⚠️ {arabic_name} - No Game class")
                    
            except Exception as e:
                logger.error(f"  ❌ {arabic_name} - {e}")
        
        logger.info(f"✅ Loaded {len(self.loaded)}/{len(self.GAME_MAPPING)} games")
    
    def start_game(self, user_id: str, game_name: str):
        """بدء لعبة"""
        if game_name not in self.loaded:
            return None
        
        try:
            if user_id in self.active_sessions:
                self.end_game(user_id)
            
            GameClass = self.loaded[game_name]
            
            try:
                game = GameClass()
            except TypeError:
                game = GameClass(line_bot_api=None)
            
            self.active_sessions[user_id] = game
            response = game.start()
            
            logger.info(f"🎮 {user_id} started {game_name}")
            return response
            
        except Exception as e:
            logger.error(f"❌ Error starting game {game_name}: {e}")
            if user_id in self.active_sessions:
                del self.active_sessions[user_id]
            return None
    
    def get_game(self, user_id: str):
        return self.active_sessions.get(user_id)
    
    def has_active_game(self, user_id: str) -> bool:
        return user_id in self.active_sessions
    
    def end_game(self, user_id: str):
        if user_id in self.active_sessions:
            del self.active_sessions[user_id]
            logger.info(f"🛑 {user_id} ended game")
    
    def get_available_games(self) -> List[str]:
        return list(self.loaded.keys())
