# games/__init__.py
"""
مجموعة ألعاب LINE Bot التفاعلية
15 لعبة متنوعة مع دعم AI
"""

from .iq_game import IQGame
from .word_color_game import WordColorGame
from .chain_words_game import ChainWordsGame
from .scramble_word_game import ScrambleWordGameAdvanced
from .letters_words_game import LettersWordsGame
from .fast_typing_game import FastTypingGame
from .human_animal_plant_game import HumanAnimalPlantGame
from .guess_game import GuessGame
from .compatibility_game import CompatibilityGame
from .math_game import MathGame
from .memory_game import MemoryGame
from .riddle_game import RiddleGame
from .opposite_game import OppositeGame
from .emoji_game import EmojiGame
from .song_game import SongGame

__all__ = [
    'IQGame',
    'WordColorGame',
    'ChainWordsGame',
    'ScrambleWordGameAdvanced',  # النسخة الجديدة
    'LettersWordsGame',
    'FastTypingGame',
    'HumanAnimalPlantGame',
    'GuessGame',
    'CompatibilityGame',
    'MathGame',
    'MemoryGame',
    'RiddleGame',
    'OppositeGame',
    'EmojiGame',
    'SongGame'
]
