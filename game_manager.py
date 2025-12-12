"""
Bot Mesh Game Manager Module
نظام إدارة الألعاب المحسّن
Created by: Abeer Aldosari - 2025
"""

import logging
from typing import Dict, Optional
from linebot.v3.messaging import TextMessage
from config import Config
from ui_builder import UIBuilder

logger = logging.getLogger(__name__)

class GameManager:
    """مدير الألعاب الذكي"""
    
    def __init__(self, db):
        self.db = db
        self.ui = UIBuilder()
        self.active_games = {}
        self.game_sessions = {}
        self.games = self._load_games()
        logger.info(f"تم تحميل {len(self.games)} لعبة")
    
    def _load_games(self) -> Dict:
        """تحميل جميع الألعاب ديناميكياً"""
        games = {}
        
        try:
            from games.iq_game import IqGame
            from games.roulette_game import RouletteGame
            from games.word_color_game import WordColorGame
            from games.scramble_word_game import ScrambleWordGame
            from games.fast_typing_game import FastTypingGame
            from games.opposite_game import OppositeGame
            from games.letters_words_game import LettersWordsGame
            from games.song_game import SongGame
            from games.human_animal_plant_game import HumanAnimalPlantGame
            from games.chain_words_game import ChainWordsGame
            from games.guess_game import GuessGame
            from games.compatibility_game import CompatibilitySystem
            from games.math_game import MathGame
            from games.mafia_game import MafiaGame
            
            games = {
                "ذكاء": IqGame,
                "روليت": RouletteGame,
                "لون": WordColorGame,
                "ترتيب": ScrambleWordGame,
                "اسرع": FastTypingGame,
                "ضد": OppositeGame,
                "تكوين": LettersWordsGame,
                "اغنيه": SongGame,
                "لعبة": HumanAnimalPlantGame,
                "سلسلة": ChainWordsGame,
                "خمن": GuessGame,
                "توافق": CompatibilitySystem,
                "رياضيات": MathGame,
                "مافيا": MafiaGame
            }
            
            logger.info(f"تم تحميل {len(games)} لعبة بنجاح")
            
        except Exception as e:
            logger.error(f"خطأ في تحميل الألعاب: {e}", exc_info=True)
        
        return games
    
    def get_active_count(self) -> int:
        """عدد الألعاب النشطة"""
        return len(self.active_games)
    
    def get_total_games(self) -> int:
        """عدد الألعاب الكلي"""
        return len(self.games)
    
    def is_game_active(self, context_id: str) -> bool:
        """التحقق من وجود لعبة نشطة"""
        return context_id in self.active_games
    
    def get_active_game(self, context_id: str):
        """الحصول على اللعبة النشطة"""
        return self.active_games.get(context_id)
    
    def stop_game(self, context_id: str) -> Optional[str]:
        """إيقاف لعبة نشطة"""
        if context_id in self.active_games:
            game = self.active_games[context_id]
            game_name = game.game_name
            
            del self.active_games[context_id]
            self.game_sessions.pop(context_id, None)
            
            logger.info(f"تم إيقاف لعبة {game_name} في السياق {context_id}")
            return game_name
        
        return None
    
    def start_game(self, context_id: str, game_name: str, user_id: str, 
                   username: str, is_registered: bool, theme: str, 
                   source_type: str) -> Optional[Dict]:
        """بدء لعبة جديدة"""
        
        if game_name not in self.games:
            logger.warning(f"لعبة غير موجودة: {game_name}")
            return None
        
        game_config = Config.get_game_config(game_name)
        
        if not game_config.get('no_registration') and not is_registered:
            return {
                'messages': [TextMessage(text="يجب التسجيل اولا\nاكتب: انضم")],
                'points': 0
            }
        
        if game_config.get('group_only') and source_type not in ["group", "room"]:
            return {
                'messages': [TextMessage(text="هذه اللعبة للمجموعات فقط")],
                'points': 0
            }
        
        try:
            GameClass = self.games[game_name]
            game = GameClass(None)
            
            if hasattr(game, 'set_theme'):
                game.set_theme(theme)
            
            if hasattr(game, 'set_database'):
                game.set_database(self.db)
            
            self.active_games[context_id] = game
            
            if not game_config.get('no_registration'):
                session_id = self.db.create_session(user_id, game_name)
                self.game_sessions[context_id] = {
                    'session_id': session_id,
                    'user_id': user_id,
                    'game_name': game_name
                }
            
            question = game.start_game()
            
            logger.info(f"تم بدء لعبة {game_name} للمستخدم {username}")
            
            return {
                'messages': [question],
                'points': 0
            }
            
        except Exception as e:
            logger.error(f"خطأ في بدء اللعبة {game_name}: {e}", exc_info=True)
            return {
                'messages': [TextMessage(text="حدث خطأ في بدء اللعبة")],
                'points': 0
            }
    
    def process_message(self, context_id: str, user_id: str, username: str,
                       text: str, is_registered: bool, theme: str, 
                       source_type: str) -> Optional[Dict]:
        """معالجة رسالة المستخدم"""
        
        normalized = Config.normalize(text)
        
        if normalized in self.games:
            return self.start_game(
                context_id, normalized, user_id, username,
                is_registered, theme, source_type
            )
        
        if context_id in self.active_games:
            game = self.active_games[context_id]
            
            try:
                result = game.check_answer(text, user_id, username)
                
                if result:
                    points = result.get('points', 0)
                    messages = []
                    
                    if result.get('message'):
                        messages.append(TextMessage(text=result['message']))
                    
                    if result.get('game_over'):
                        if context_id in self.game_sessions:
                            session = self.game_sessions[context_id]
                            self.db.complete_session(session['session_id'], points)
                            del self.game_sessions[context_id]
                        
                        del self.active_games[context_id]
                        
                        if points > 0 and is_registered:
                            self.db.record_game_stat(user_id, game.game_name, points, True)
                        
                        logger.info(f"انتهت لعبة {game.game_name} - النقاط: {points}")
                    
                    elif result.get('response'):
                        messages.append(result['response'])
                    
                    return {
                        'messages': messages,
                        'points': points
                    }
                
            except Exception as e:
                logger.error(f"خطأ في معالجة الإجابة: {e}", exc_info=True)
                return None
        
        return None
    
    def get_game_info(self, context_id: str) -> Optional[Dict]:
        """الحصول على معلومات اللعبة النشطة"""
        if context_id in self.active_games:
            game = self.active_games[context_id]
            if hasattr(game, 'get_game_info'):
                return game.get_game_info()
        return None
    
    def cleanup_inactive_games(self, timeout_minutes: int = 30):
        """تنظيف الألعاب غير النشطة"""
        from datetime import datetime, timedelta
        
        cutoff_time = datetime.now() - timedelta(minutes=timeout_minutes)
        contexts_to_remove = []
        
        for context_id, game in self.active_games.items():
            if hasattr(game, 'game_start_time') and game.game_start_time:
                if game.game_start_time < cutoff_time:
                    contexts_to_remove.append(context_id)
        
        for context_id in contexts_to_remove:
            self.stop_game(context_id)
        
        if contexts_to_remove:
            logger.info(f"تم تنظيف {len(contexts_to_remove)} لعبة غير نشطة")
