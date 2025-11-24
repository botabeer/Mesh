"""
Bot Mesh - Games Module (Fixed - No Relative Imports)
Created by: Abeer Aldosari © 2025
"""
import logging
import sys
import os

# إضافة مسار المشروع لـ sys.path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

logger = logging.getLogger(__name__)

# استيراد BaseGame أولاً بدون relative import
from games.base_game import BaseGame

# استيراد جميع الألعاب
try:
    from games.iq_game import IqGame
    logger.info("✅ IqGame loaded")
except Exception as e:
    logger.error(f"❌ Failed to load IqGame: {e}")
    IqGame = None

try:
    from games.math_game import MathGame
    logger.info("✅ MathGame loaded")
except Exception as e:
    logger.error(f"❌ Failed to load MathGame: {e}")
    MathGame = None

try:
    from games.word_color_game import WordColorGame
    logger.info("✅ WordColorGame loaded")
except Exception as e:
    logger.error(f"❌ Failed to load WordColorGame: {e}")
    WordColorGame = None

try:
    from games.scramble_word_game import ScrambleWordGame
    logger.info("✅ ScrambleWordGame loaded")
except Exception as e:
    logger.error(f"❌ Failed to load ScrambleWordGame: {e}")
    ScrambleWordGame = None

try:
    from games.fast_typing_game import FastTypingGame
    logger.info("✅ FastTypingGame loaded")
except Exception as e:
    logger.error(f"❌ Failed to load FastTypingGame: {e}")
    FastTypingGame = None

try:
    from games.opposite_game import OppositeGame
    logger.info("✅ OppositeGame loaded")
except Exception as e:
    logger.error(f"❌ Failed to load OppositeGame: {e}")
    OppositeGame = None

try:
    from games.letters_words_game import LettersWordsGame
    logger.info("✅ LettersWordsGame loaded")
except Exception as e:
    logger.error(f"❌ Failed to load LettersWordsGame: {e}")
    LettersWordsGame = None

try:
    from games.song_game import SongGame
    logger.info("✅ SongGame loaded")
except Exception as e:
    logger.error(f"❌ Failed to load SongGame: {e}")
    SongGame = None

try:
    from games.human_animal_plant_game import HumanAnimalPlantGame
    logger.info("✅ HumanAnimalPlantGame loaded")
except Exception as e:
    logger.error(f"❌ Failed to load HumanAnimalPlantGame: {e}")
    HumanAnimalPlantGame = None

try:
    from games.chain_words_game import ChainWordsGame
    logger.info("✅ ChainWordsGame loaded")
except Exception as e:
    logger.error(f"❌ Failed to load ChainWordsGame: {e}")
    ChainWordsGame = None

try:
    from games.guess_game import GuessGame
    logger.info("✅ GuessGame loaded")
except Exception as e:
    logger.error(f"❌ Failed to load GuessGame: {e}")
    GuessGame = None

try:
    from games.compatibility_game import CompatibilityGame
    logger.info("✅ CompatibilityGame loaded")
except Exception as e:
    logger.error(f"❌ Failed to load CompatibilityGame: {e}")
    CompatibilityGame = None

# Export all games that loaded successfully
__all__ = [
    'BaseGame',
    'IqGame',
    'MathGame',
    'WordColorGame',
    'ScrambleWordGame',
    'FastTypingGame',
    'OppositeGame',
    'LettersWordsGame',
    'SongGame',
    'HumanAnimalPlantGame',
    'ChainWordsGame',
    'GuessGame',
    'CompatibilityGame'
]

# Count successfully loaded games
loaded_games = sum(1 for game in __all__[1:] if globals().get(game) is not None)
logger.info(f"📊 Successfully loaded {loaded_games}/{len(__all__)-1} game classes")
