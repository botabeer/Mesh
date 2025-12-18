import importlib
import logging

logger = logging.getLogger(__name__)

class GameManager:
    def __init__(self, db):
        self.db = db
        self.game_mappings = {
            "خمن": ("games.guess", "GuessGame"),
            "ذكاء": ("games.iq", "IQGame"),
            "ترتيب": ("games.scramble", "ScrambleGame"),
            "رياضيات": ("games.math", "MathGame"),
            "اسرع": ("games.fast_typing", "FastTypingGame"),
            "ضد": ("games.opposite", "OppositeGame"),
            "اضداد": ("games.opposite", "OppositeGame"),
            "لعبه": ("games.human_animal", "HumanAnimalGame"),
            "لعبة": ("games.human_animal", "HumanAnimalGame"),
            "سلسله": ("games.chain_words", "ChainWordsGame"),
            "سلسلة": ("games.chain_words", "ChainWordsGame"),
            "اغنيه": ("games.song", "SongGame"),
            "اغنية": ("games.song", "SongGame"),
            "تكوين": ("games.letters_words", "LettersWordsGame"),
            "لون": ("games.word_color", "WordColorGame"),
            "حرف": ("games.letters_words", "LettersWordsGame"),
            "مافيا": ("games.mafia", "MafiaGame"),
            "توافق": ("games.compatibility", "CompatibilityGame")
        }
    
    def start_game(self, user_id, game_cmd, theme="light"):
        if game_cmd not in self.game_mappings:
            return None
        
        module_name, class_name = self.game_mappings[game_cmd]
        try:
            module = importlib.import_module(module_name)
            game_class = getattr(module, class_name)
            game = game_class(self.db, theme)
            self.db.set_game_progress(user_id, game)
            return game.start(user_id)
        except Exception as e:
            logger.error(f"Error starting game {game_cmd}: {e}")
            return None
    
    def process_answer(self, user_id, answer):
        game = self.db.get_game_progress(user_id)
        if not game:
            return None, None
        
        result = game.check(answer, user_id)
        
        if result is None:
            score = game.score
            total = game.total_q
            game_name = game.game_name
            self.db.add_points(user_id, score)
            self.db.increment_games(user_id)
            
            if score == total:
                self.db.increment_wins(user_id)
            else:
                self.db.reset_streak(user_id)
            
            self.db.add_game_played(user_id, game_name)
            achievements = self.db.check_achievements(user_id)
            self.db.clear_game_progress(user_id)
            
            return {
                "finished": True,
                "score": score,
                "total": total,
                "game_name": game_name,
                "achievements": achievements
            }, None
        
        if isinstance(result, dict):
            if result.get("game_over"):
                self.db.clear_game_progress(user_id)
                return result, None
            return result.get("response"), result.get("skip", False)
        
        question, correct = result
        return question, correct
    
    def get_hint(self, user_id):
        game = self.db.get_game_progress(user_id)
        if game and hasattr(game, 'get_hint'):
            return game.get_hint()
        return None
    
    def reveal_answer(self, user_id):
        game = self.db.get_game_progress(user_id)
        if game and hasattr(game, 'reveal_answer'):
            return game.reveal_answer()
        return None
    
    def stop_game(self, user_id):
        game = self.db.get_game_progress(user_id)
        if game:
            score = game.score
            self.db.add_points(user_id, score)
            self.db.reset_streak(user_id)
            self.db.clear_game_progress(user_id)
            return score
        return 0
    
    def count_active(self):
        return len(self.db._game_progress)
