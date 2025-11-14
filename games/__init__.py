# games/__init__.py

from .scramble_word_game import ScrambleWordGameAdvanced
from .chain_words_game import ChainWordsGame
from .clean_hidden_chars import clean_hidden_chars
from .compatibility_game import CompatibilityGame
from .differences_game import DifferencesGame
from .emoji_game import EmojiGame
from .fast_typing_game import FastTypingGame
from .guess_game import GuessGame
from .human_animal_plant_game import HumanAnimalPlantGame
from .iq_game import IQGame
from .letters_words_game import LettersWordsGame
from .make_words import MakeWordsGame
from .math_game import MathGame
from .memory_game import MemoryGame
from .multi_games import MultiGames
from .multi_games_extended import MultiGamesExtended
from .name_compatibility import NameCompatibility
from .opposite_game import OppositeGame
from .riddle_game import RiddleGame
from .scramble_word_game import ScrambleWordGameAdvanced
from .song_game import SongGame
from .word_color_game import WordColorGame

__all__ = [
    "ScrambleWordGameAdvanced",
    "ChainWordsGame",
    "clean_hidden_chars",
    "CompatibilityGame",
    "DifferencesGame",
    "EmojiGame",
    "FastTypingGame",
    "GuessGame",
    "HumanAnimalPlantGame",
    "IQGame",
    "LettersWordsGame",
    "MakeWordsGame",
    "MathGame",
    "MemoryGame",
    "MultiGames",
    "MultiGamesExtended",
    "NameCompatibility",
    "OppositeGame",
    "RiddleGame",
    "SongGame",
    "WordColorGame"
]
