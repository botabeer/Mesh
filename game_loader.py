"""
Bot Mesh v10.0 - Enhanced Game Loader
Created by: Abeer Aldosari © 2025
"""

import importlib
import logging
import inspect
from typing import Dict, Optional, List, Any
from datetime import datetime, timedelta
from threading import Lock

logger = logging.getLogger(__name__)

class GameSession:
    """تمثيل جلسة لعبة مع metadata"""
    
    def __init__(self, game_instance, user_id: str, game_name: str):
        self.game = game_instance
        self.user_id = user_id
        self.game_name = game_name
        self.started_at = datetime.now()
        self.last_activity = datetime.now()
    
    def update_activity(self):
        """تحديث آخر نشاط"""
        self.last_activity = datetime.now()
    
    def is_expired(self, timeout_minutes: int = 30) -> bool:
        """التحقق من انتهاء الصلاحية"""
        return (datetime.now() - self.last_activity) > timedelta(minutes=timeout_minutes)
    
    def get_duration(self) -> float:
        """الحصول على مدة اللعبة بالثواني"""
        return (datetime.now() - self.started_at).total_seconds()


class GameLoader:
    """محمّل الألعاب المحسّن"""
    
    # خريطة الألعاب (الاسم العربي -> اسم الملف)
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
    
    def __init__(self, auto_cleanup: bool = True, session_timeout: int = 30):
        self.loaded: Dict[str, type] = {}
        self.active_sessions: Dict[str, GameSession] = {}
        self.session_timeout = session_timeout
        self.auto_cleanup = auto_cleanup
        self.lock = Lock()
        
        self.stats = {
            'games_started': 0,
            'games_completed': 0,
            'games_failed': 0,
            'load_errors': 0
        }
        
        self._load_all_games()
        
        logger.info(f"✅ GameLoader initialized: {len(self.loaded)}/{len(self.GAME_MAPPING)} games loaded")
    
    def _load_all_games(self):
        """تحميل الألعاب بشكل آمن"""
        logger.info("🎮 Loading games...")
        
        for arabic_name, file_name in self.GAME_MAPPING.items():
            try:
                module = importlib.import_module(f"games.{file_name}")
                game_class = self._find_game_class(module)
                
                if game_class:
                    if self._validate_game_class(game_class):
                        self.loaded[arabic_name] = game_class
                        logger.info(f"  ✅ {arabic_name} ({file_name})")
                    else:
                        logger.warning(f"  ⚠️ {arabic_name} - validation failed")
                        self.stats['load_errors'] += 1
                else:
                    logger.warning(f"  ⚠️ {arabic_name} - no Game class found")
                    self.stats['load_errors'] += 1
                    
            except Exception as e:
                logger.error(f"  ❌ {arabic_name} - error: {e}")
                self.stats['load_errors'] += 1
        
        logger.info(f"✅ Loaded {len(self.loaded)}/{len(self.GAME_MAPPING)} games successfully")
    
    def _find_game_class(self, module) -> Optional[type]:
        """البحث عن Game class في الموديول"""
        if hasattr(module, "Game"):
            return module.Game
        
        for attr_name in dir(module):
            if attr_name.endswith("Game") and not attr_name.startswith("_"):
                attr = getattr(module, attr_name)
                if isinstance(attr, type):
                    return attr
        
        return None
    
    def _validate_game_class(self, game_class: type) -> bool:
        """التحقق من صحة Game class"""
        try:
            required_methods = ['start', 'check_answer']
            for method in required_methods:
                if not hasattr(game_class, method):
                    logger.warning(f"Missing method: {method}")
                    return False
            return True
        except Exception as e:
            logger.error(f"Validation error: {e}")
            return False
    
    def _create_game_instance(self, game_class: type) -> Optional[Any]:
        """إنشاء نسخة من اللعبة بطريقة آمنة"""
        try:
            sig = inspect.signature(game_class.__init__)
            params = list(sig.parameters.keys())
            params = [p for p in params if p != 'self']
            
            if not params:
                return game_class()
            elif 'line_bot_api' in params:
                return game_class(line_bot_api=None)
            else:
                try:
                    return game_class()
                except TypeError:
                    return game_class(line_bot_api=None)
        
        except Exception as e:
            logger.error(f"Error creating game instance: {e}")
            return None
    
    def start_game(self, user_id: str, game_name: str) -> Optional[Any]:
        """بدء لعبة جديدة"""
        with self.lock:
            if game_name not in self.loaded:
                logger.warning(f"⚠️ Game not found: {game_name}")
                return None
            
            try:
                if user_id in self.active_sessions:
                    self.end_game(user_id)
                
                GameClass = self.loaded[game_name]
                game = self._create_game_instance(GameClass)
                
                if not game:
                    logger.error(f"❌ Failed to create game instance: {game_name}")
                    self.stats['games_failed'] += 1
                    return None
                
                if hasattr(game, 'start_game'):
                    response = game.start_game()
                elif hasattr(game, 'start'):
                    response = game.start()
                else:
                    raise AttributeError("No start method found")
                
                session = GameSession(game, user_id, game_name)
                self.active_sessions[user_id] = session
                
                self.stats['games_started'] += 1
                
                logger.info(f"🎮 {user_id[:8]}... started {game_name}")
                return response
                
            except Exception as e:
                logger.error(f"❌ Error starting game {game_name}: {e}", exc_info=True)
                self.stats['games_failed'] += 1
                
                if user_id in self.active_sessions:
                    del self.active_sessions[user_id]
                
                return None
    
    def get_game(self, user_id: str) -> Optional[Any]:
        """الحصول على اللعبة النشطة"""
        session = self.active_sessions.get(user_id)
        if session:
            session.update_activity()
            return session.game
        return None
    
    def has_active_game(self, user_id: str) -> bool:
        """التحقق من وجود لعبة نشطة"""
        return user_id in self.active_sessions
    
    def end_game(self, user_id: str, completed: bool = False):
        """إنهاء اللعبة"""
        with self.lock:
            if user_id in self.active_sessions:
                session = self.active_sessions[user_id]
                duration = session.get_duration()
                
                if completed:
                    self.stats['games_completed'] += 1
                
                del self.active_sessions[user_id]
                
                logger.info(
                    f"🛑 {user_id[:8]}... ended {session.game_name} "
                    f"(duration: {duration:.1f}s, completed: {completed})"
                )
    
    def cleanup_expired_sessions(self):
        """تنظيف الجلسات المنتهية"""
        if not self.auto_cleanup:
            return
        
        with self.lock:
            expired = []
            
            for user_id, session in self.active_sessions.items():
                if session.is_expired(self.session_timeout):
                    expired.append(user_id)
            
            for user_id in expired:
                logger.info(f"🧹 Cleaning expired session: {user_id[:8]}...")
                self.end_game(user_id, completed=False)
            
            if expired:
                logger.info(f"🧹 Cleaned {len(expired)} expired sessions")
    
    def get_available_games(self) -> List[str]:
        """الحصول على قائمة الألعاب المتاحة"""
        return list(self.loaded.keys())
    
    def get_stats(self) -> Dict:
        """الحصول على إحصائيات"""
        with self.lock:
            return {
                'total_games': len(self.GAME_MAPPING),
                'loaded_games': len(self.loaded),
                'load_errors': self.stats['load_errors'],
                'active_sessions': len(self.active_sessions),
                'games_started': self.stats['games_started'],
                'games_completed': self.stats['games_completed'],
                'games_failed': self.stats['games_failed'],
                'available_games': self.get_available_games(),
                'success_rate': (
                    self.stats['games_completed'] / self.stats['games_started'] * 100
                    if self.stats['games_started'] > 0 else 0
                )
            }
    
    def get_session_info(self, user_id: str) -> Optional[Dict]:
        """الحصول على معلومات الجلسة"""
        session = self.active_sessions.get(user_id)
        if session:
            return {
                'game_name': session.game_name,
                'started_at': session.started_at.isoformat(),
                'duration': session.get_duration(),
                'last_activity': session.last_activity.isoformat()
            }
        return None
