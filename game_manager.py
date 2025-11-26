"""
🎮 Bot Mesh v6.0 - Smart Game Manager
Created by: Abeer Aldosari © 2025

نظام إدارة ألعاب ذكي مع:
- تحميل تلقائي للألعاب
- إدارة الجلسات
- تنظيف تلقائي
"""

import os
import sys
import logging
import importlib
import inspect
from datetime import datetime, timedelta
from typing import Dict, Optional, Any

logger = logging.getLogger(__name__)

class GameManager:
    """مدير الألعاب المركزي"""
    
    def __init__(self, gemini_helper=None):
        """تهيئة المدير"""
        self.gemini = gemini_helper
        self.available_games = {}
        self.active_sessions = {}  # {user_id: game_instance}
        
        # تحميل الألعاب
        self._load_games()
        
        logger.info(f"✅ تم تحميل {len(self.available_games)} لعبة")
    
    def _load_games(self):
        """تحميل جميع الألعاب من مجلد games/"""
        games_dir = os.path.join(os.path.dirname(__file__), 'games')
        
        if not os.path.exists(games_dir):
            logger.warning("❌ مجلد games/ غير موجود")
            return
        
        # إضافة مجلد games للمسار
        if games_dir not in sys.path:
            sys.path.insert(0, games_dir)
        
        # قائمة الألعاب المعروفة
        game_files = {
            'iq_game': 'ذكاء',
            'math_game': 'رياضيات',
            'fast_typing_game': 'سرعة',
            'scramble_word_game': 'كلمات',
            'word_color_game': 'ألوان',
            'opposite_game': 'أضداد',
            'chain_words_game': 'سلسلة',
            'guess_game': 'تخمين',
            'letters_words_game': 'تكوين',
            'song_game': 'أغنية',
            'human_animal_plant_game': 'إنسان حيوان',
            'compatibility_game': 'توافق'
        }
        
        for file_name, game_name in game_files.items():
            try:
                # استيراد الوحدة
                module = importlib.import_module(file_name)
                
                # البحث عن كلاس اللعبة
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    if 'Game' in name and hasattr(obj, 'start_game'):
                        self.available_games[game_name] = obj
                        logger.info(f"  ✓ {game_name}")
                        break
                
            except Exception as e:
                logger.error(f"  ✗ فشل تحميل {game_name}: {e}")
    
    def start_game(self, user_id: str, game_name: str) -> Optional[Any]:
        """بدء لعبة جديدة"""
        # إنهاء اللعبة السابقة إن وجدت
        if user_id in self.active_sessions:
            self.end_game(user_id)
        
        # التحقق من وجود اللعبة
        if game_name not in self.available_games:
            logger.warning(f"⚠️ لعبة غير موجودة: {game_name}")
            return None
        
        try:
            # إنشاء نسخة جديدة من اللعبة
            GameClass = self.available_games[game_name]
            
            # تمرير Gemini helper إذا كانت اللعبة تدعم AI
            if self.gemini:
                game = GameClass(gemini_helper=self.gemini)
            else:
                game = GameClass()
            
            # حفظ الجلسة
            self.active_sessions[user_id] = {
                'game': game,
                'name': game_name,
                'started_at': datetime.now()
            }
            
            # بدء اللعبة
            game.start_game()
            
            logger.info(f"🎮 بدأ {user_id} لعبة {game_name}")
            return game
            
        except Exception as e:
            logger.error(f"❌ خطأ في بدء اللعبة: {e}", exc_info=True)
            return None
    
    def has_active_game(self, user_id: str) -> bool:
        """التحقق من وجود لعبة نشطة"""
        return user_id in self.active_sessions
    
    def get_game(self, user_id: str) -> Optional[Any]:
        """الحصول على اللعبة النشطة"""
        session = self.active_sessions.get(user_id)
        return session['game'] if session else None
    
    def process_answer(self, user_id: str, answer: str, username: str) -> Dict[str, Any]:
        """معالجة إجابة اللاعب"""
        game = self.get_game(user_id)
        
        if not game:
            return {
                'valid': False,
                'message': "لا توجد لعبة نشطة"
            }
        
        try:
            # التحقق من الإجابة
            result = game.check_answer(answer, user_id, username)
            
            if not result:
                return {
                    'valid': False,
                    'message': "حدث خطأ في التحقق"
                }
            
            # إذا انتهت اللعبة
            if result.get('game_over'):
                session = self.active_sessions[user_id]
                result['game_name'] = session['name']
                result['total_points'] = game.scores.get(user_id, {}).get('points', 0)
            
            # إذا كانت إجابة صحيحة
            elif result.get('points', 0) > 0:
                result['correct'] = True
                result['points_earned'] = result['points']
                
                # الحصول على السؤال التالي
                if hasattr(game, 'get_question'):
                    next_q = game.get_question()
                    result['next_question'] = next_q
            
            return result
            
        except Exception as e:
            logger.error(f"❌ خطأ في معالجة الإجابة: {e}", exc_info=True)
            return {
                'valid': False,
                'message': "حدث خطأ في معالجة إجابتك"
            }
    
    def end_game(self, user_id: str):
        """إنهاء اللعبة"""
        if user_id in self.active_sessions:
            session = self.active_sessions[user_id]
            logger.info(f"🛑 انتهت لعبة {session['name']} لـ {user_id}")
            del self.active_sessions[user_id]
    
    def cleanup_expired_sessions(self, max_minutes: int = 30):
        """تنظيف الجلسات المنتهية"""
        now = datetime.now()
        expired = []
        
        for user_id, session in self.active_sessions.items():
            elapsed = (now - session['started_at']).total_seconds() / 60
            if elapsed > max_minutes:
                expired.append(user_id)
        
        for user_id in expired:
            self.end_game(user_id)
        
        if expired:
            logger.info(f"🧹 تم حذف {len(expired)} جلسات منتهية")
    
    def get_stats(self) -> Dict[str, Any]:
        """الحصول على إحصائيات"""
        return {
            'available_games': len(self.available_games),
            'active_sessions': len(self.active_sessions),
            'game_names': list(self.available_games.keys())
        }
