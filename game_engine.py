import logging
from typing import Optional, Dict, Any
from linebot.v3.messaging import TextMessage

logger = logging.getLogger(__name__)

class GameEngine:
    """محرك الألعاب المحسّن"""
    
    # الحالات
    STATE_IDLE = "idle"
    STATE_WAITING_NAME = "waiting_name"
    STATE_IN_GAME = "in_game"
    
    def __init__(self, messaging_api, database):
        self.messaging_api = messaging_api
        self.db = database
        self.active_games = {}
        self.waiting_for_name = {}  # تغيير من set إلى dict
        self.user_states = {}
        
        # تحميل الألعاب
        self.games = self._load_all_games()
    
    def _load_all_games(self) -> Dict:
        """تحميل جميع الألعاب"""
        games = {}
        
        game_mappings = {
            "ذكاء": ("iq_game", "IqGame"),
            "خمن": ("guess_game", "GuessGame"),
            "ضد": ("opposite_game", "OppositeGame"),
            "ترتيب": ("scramble_word_game", "ScrambleWordGame"),
            "رياضيات": ("math_game", "MathGame"),
            "اغنيه": ("song_game", "SongGame"),
            "لون": ("word_color_game", "WordColorGame"),
            "تكوين": ("letters_words_game", "LettersWordsGame"),
            "لعبة": ("human_animal_plant_game", "HumanAnimalPlantGame"),
            "سلسلة": ("chain_words_game", "ChainWordsGame"),
            "اسرع": ("fast_typing_game", "FastTypingGame"),
            "توافق": ("compatibility_game", "CompatibilityGame"),
            "مافيا": ("mafia_game", "MafiaGame"),
        }
        
        for game_name, (module_name, class_name) in game_mappings.items():
            game_class = self._load_game(module_name, class_name)
            if game_class:
                games[game_name] = game_class
        
        return games
    
    def _load_game(self, module_name: str, class_name: str):
        """تحميل لعبة واحدة"""
        try:
            module = __import__(f"games.{module_name}", fromlist=[class_name])
            return getattr(module, class_name)
        except Exception as e:
            logger.error(f"Failed to load {class_name}: {e}")
            return None
    
    def set_waiting_for_name(self, user_id: str, waiting: bool):
        """تعيين حالة انتظار الاسم"""
        if waiting:
            self.waiting_for_name[user_id] = True
            self.user_states[user_id] = self.STATE_WAITING_NAME
        else:
            self.waiting_for_name.pop(user_id, None)
            self.user_states[user_id] = self.STATE_IDLE
    
    def is_waiting_for_name(self, user_id: str) -> bool:
        """التحقق من حالة انتظار الاسم"""
        return self.waiting_for_name.get(user_id, False)
    
    def get_user_state(self, user_id: str) -> str:
        """الحصول على حالة المستخدم"""
        return self.user_states.get(user_id, self.STATE_IDLE)
    
    def process_message(self, text: str, user_id: str, group_id: str, 
                       display_name: str, is_registered: bool):
        """معالجة الرسالة"""
        text = text.strip()
        logger.info(f"Processing: {text} | user={user_id} | registered={is_registered}")
        
        # التحقق من حالة المستخدم
        state = self.get_user_state(user_id)
        
        # معالجة الألعاب النشطة
        if group_id in self.active_games:
            return self._handle_game_answer(text, user_id, group_id, display_name)
        
        # معالجة بدء لعبة جديدة
        return self._handle_game_start(text, user_id, group_id, is_registered)
    
    def _handle_game_start(self, text: str, user_id: str, group_id: str, is_registered: bool):
        """معالجة بدء لعبة جديدة"""
        # التحقق من التسجيل للألعاب التي تتطلب نقاط
        if text in self.games:
            if not is_registered and text != "توافق":
                return TextMessage(text="يجب التسجيل أولاً\nاكتب: تسجيل")
            
            return self._start_game(text, user_id, group_id)
        
        # الألعاب النصية (لا تتطلب تسجيل)
        text_games = ["سؤال", "منشن", "تحدي", "اعتراف", "موقف", "اقتباس"]
        if text in text_games:
            return self._start_text_game(text)
        
        return None
    
    def _start_game(self, game_name: str, user_id: str, group_id: str):
        """بدء لعبة"""
        GameClass = self.games.get(game_name)
        
        if not GameClass:
            return TextMessage(text="اللعبة غير متوفرة")
        
        try:
            # إنشاء مثيل اللعبة
            game = GameClass(self.messaging_api)
            
            # تعيين قاعدة البيانات إن كانت اللعبة تدعم ذلك
            if hasattr(game, "set_database"):
                game.set_database(self.db)
            
            # حفظ اللعبة النشطة
            self.active_games[group_id] = game
            self.user_states[user_id] = self.STATE_IN_GAME
            
            # بدء اللعبة
            result = game.start_game()
            
            logger.info(f"Game started: {game_name} | group={group_id}")
            
            return result if result else TextMessage(text="بدأت اللعبة")
        
        except Exception as e:
            logger.error(f"Error starting game {game_name}: {e}", exc_info=True)
            return TextMessage(text="فشل بدء اللعبة\nحاول مرة أخرى")
    
    def _start_text_game(self, game_name: str):
        """بدء لعبة نصية (بدون نقاط)"""
        import random
        
        files = {
            "سؤال": "questions.txt",
            "منشن": "mentions.txt",
            "تحدي": "challenges.txt",
            "اعتراف": "confessions.txt",
            "موقف": "situations.txt",
            "اقتباس": "quotes.txt",
        }
        
        try:
            filepath = f"games/{files[game_name]}"
            with open(filepath, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f if line.strip()]
            
            if lines:
                return TextMessage(text=random.choice(lines))
            else:
                return TextMessage(text="لا توجد محتوى متاح")
        
        except FileNotFoundError:
            logger.error(f"File not found: {filepath}")
            return TextMessage(text="فشل تحميل اللعبة")
        
        except Exception as e:
            logger.error(f"Error in text game {game_name}: {e}")
            return TextMessage(text="حدث خطأ")
    
    def _handle_game_answer(self, text: str, user_id: str, group_id: str, display_name: str):
        """معالجة إجابة اللعبة"""
        game = self.active_games.get(group_id)
        
        if not game:
            return TextMessage(text="اللعبة انتهت")
        
        try:
            # التحقق من الإجابة
            result = game.check_answer(text, user_id, display_name)
            
            if result is None:
                return None
            
            # رسالة نصية بسيطة
            if isinstance(result, TextMessage):
                return result
            
            # نتيجة بتفاصيل
            if not isinstance(result, dict):
                return None
            
            # تحديث النقاط إن وجدت
            points = result.get("points", 0)
            if points > 0:
                game_type = getattr(game, 'game_name', 'unknown')
                self.db.update_user_points(user_id, points, points > 0, game_type)
            
            # انتهاء اللعبة
            if result.get("game_over"):
                del self.active_games[group_id]
                self.user_states[user_id] = self.STATE_IDLE
                logger.info(f"Game ended | group={group_id}")
            
            # إرجاع الرد
            response = result.get("response")
            if response:
                return response
            
            message = result.get("message", "")
            return TextMessage(text=message) if message else None
        
        except Exception as e:
            logger.error(f"Game error: {e}", exc_info=True)
            self.active_games.pop(group_id, None)
            self.user_states[user_id] = self.STATE_IDLE
            return TextMessage(text="حدث خطأ في اللعبة")
    
    def stop_game(self, group_id: str) -> bool:
        """إيقاف اللعبة"""
        if group_id in self.active_games:
            del self.active_games[group_id]
            logger.info(f"Game manually stopped | group={group_id}")
            return True
        return False
    
    def get_active_games_count(self) -> int:
        """عدد الألعاب النشطة"""
        return len(self.active_games)
    
    def is_game_active(self, group_id: str) -> bool:
        """التحقق من وجود لعبة نشطة"""
        return group_id in self.active_games
