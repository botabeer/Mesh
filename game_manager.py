import importlib
import logging

logger = logging.getLogger(__name__)

class GameManager:
    def __init__(self, db):
        self.db = db
        self.game_mappings = {
            "خمن": ("games.guess", "GuessGame"),
            "ذكاء": ("games.iq", "IqGame"),
            "ترتيب": ("games.scramble", "ScrambleGame"),
            "رياضيات": ("games.math", "MathGame"),
            "اسرع": ("games.fast_typing", "FastTypingGame"),
            "ضد": ("games.opposite", "OppositeGame"),
            "لعبه": ("games.human_animal", "HumanAnimalGame"),
            "سلسله": ("games.chain_words", "ChainWordsGame"),
            "اغنيه": ("games.song", "SongGame"),
            "تكوين": ("games.letters_words", "LettersWordsGame"),
            "لون": ("games.word_color", "WordColorGame"),
            "حرف": ("games.letters", "LettersGame")
            "مافيا": ("games.mafia", "MafiaGame")
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
            return None, False
        
        correct = game.check_answer(answer)
        
        if correct:
            game.score += 1
            self.db.add_points(user_id, 1)
            game.current_q += 1
            
            if game.current_q >= game.total_q:
                score = game.score
                total = game.total_q
                game_name = game.game_name
                
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
                }, True
        
        return None, correct
    
    def next_question(self, user_id):
        game = self.db.get_game_progress(user_id)
        if game:
            return game.get_question()
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
