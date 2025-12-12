import logging
import random
from typing import Dict, Any, Optional
from linebot.v3.messaging import TextMessage
from database import Database
from config import Config

logger = logging.getLogger(__name__)

class TextGame:
    def __init__(self, file_name: Optional[str], game_name: str):
        self.game_name = game_name
        self.items = self._load_items(file_name) if file_name else []
        if not self.items:
            self.items = [f"{game_name} - لا يوجد محتوى"]
        random.shuffle(self.items)
        self.used_items = []
        self.game_active = False
        self.current_round = 1
        self.max_rounds = 5

    def _load_items(self, file_name: str) -> list:
        try:
            with open(f"games/{file_name}", "r", encoding="utf-8") as f:
                return [line.strip() for line in f if line.strip()]
        except Exception as e:
            logger.error(f"فشل تحميل {file_name}: {e}")
            return []

    def start_game(self) -> TextMessage:
        self.game_active = True
        self.current_round = 1
        return self.get_question()

    def _pick_item(self) -> str:
        available = [x for x in self.items if x not in self.used_items]
        if not available:
            self.used_items.clear()
            available = self.items.copy()
        item = random.choice(available)
        self.used_items.append(item)
        return item

    def get_question(self) -> TextMessage:
        question = self._pick_item()
        return TextMessage(text=f"{self.game_name} - جولة {self.current_round}: {question}")

    def check_answer(self, answer: str, user_id: str, username: str) -> Dict[str, Any]:
        points = 1
        self.current_round += 1
        game_over = self.current_round > self.max_rounds
        return {"message": None, "points": points, "game_over": game_over}

class GameManager:
    def __init__(self, db: Database):
        self.db = db
        self.active_games: Dict[str, Any] = {}
        self.game_sessions: Dict[str, dict] = {}

        from games.iq_game import IqGame
        from games.guess_game import GuessGame
        from games.opposite_game import OppositeGame
        from games.scramble_word_game import ScrambleWordGame
        from games.math_game import MathGame
        from games.song_game import SongGame
        from games.word_color_game import WordColorGame
        from games.letters_words_game import LettersWordsGame
        from games.human_animal_plant_game import HumanAnimalPlantGame
        from games.chain_words_game import ChainWordsGame
        from games.fast_typing_game import FastTypingGame
        from games.compatibility_game import CompatibilityGame
        from games.mafia_game import MafiaGame

        self.text_games_files = {
            "سؤال": "questions.txt",
            "منشن": "mentions.txt",
            "تحدي": "challenges.txt",
            "اعتراف": "confessions.txt",
            "موقف": "situations.txt",
            "اقتباس": "quotes.txt"
        }

        self.games = {
            "ذكاء": IqGame,
            "خمن": GuessGame,
            "ضد": OppositeGame,
            "ترتيب": ScrambleWordGame,
            "رياضيات": MathGame,
            "اغنيه": SongGame,
            "لون": WordColorGame,
            "تكوين": LettersWordsGame,
            "لعبة": HumanAnimalPlantGame,
            "سلسلة": ChainWordsGame,
            "اسرع": FastTypingGame,
            "توافق": CompatibilityGame,
            "مافيا": MafiaGame
        }

        for k, f in self.text_games_files.items():
            self.games[k] = lambda f=f, k=k: TextGame(f, k)

    def start_game(self, context_id: str, game_name: str, user_id: str) -> TextMessage:
        if game_name not in self.games:
            return TextMessage(text="اللعبة غير موجودة")

        GameClass = self.games[game_name]
        game = GameClass() if callable(GameClass) else GameClass(None)
        self.active_games[context_id] = game

        session_id = self.db.create_session(user_id, game_name)
        self.game_sessions[context_id] = {
            "session_id": session_id,
            "user_id": user_id,
            "game_name": game_name
        }

        return game.start_game()

    def process_message(self, context_id: str, user_id: str, username: str, text: str) -> Optional[TextMessage]:
        if context_id not in self.active_games:
            return None

        game = self.active_games[context_id]
        result = game.check_answer(text, user_id, username)
        if result is None:
            return None

        points = result.get("points", 0)
        game_over = result.get("game_over", False)

        sess = self.game_sessions.get(context_id)
        if sess:
            if points > 0:
                self.db.add_points(user_id, points)
            if game_over:
                self.db.complete_session(sess["session_id"], points)
                self.active_games.pop(context_id, None)
                self.game_sessions.pop(context_id, None)

        if not game_over:
            return game.get_question()
        else:
            return TextMessage(text=f"انتهت اللعبة - نقاطك: {points}")

    def stop_game(self, context_id: str):
        self.active_games.pop(context_id, None)
        self.game_sessions.pop(context_id, None)

    def get_active_count(self) -> int:
        return len(self.active_games)
