# games/__init__.py
"""
مجموعة ألعاب LINE Bot التفاعلية
15 لعبة متنوعة مع دعم AI
"""

from .iq_game import IQGame
from .word_color_game import WordColorGame
from .chain_words_game import ChainWordsGame
from .scramble_word_game import ScrambleWordGame
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
    'ScrambleWordGame',
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


# utils/__init__.py
"""
أدوات مساعدة للبوت
"""

from .helpers import (
    get_user_profile_safe,
    normalize_text,
    check_rate_limit,
    cleanup_old_games
)

from .database import (
    init_db,
    update_user_points,
    get_user_stats,
    get_leaderboard
)

from .ui_components import (
    get_games_quick_reply,
    get_winner_announcement,
    get_help_message,
    get_welcome_message,
    get_stats_message,
    get_leaderboard_message,
    get_join_message
)

from .gemini_config import (
    USE_AI,
    get_gemini_api_key,
    switch_gemini_key
)

__all__ = [
    'get_user_profile_safe',
    'normalize_text',
    'check_rate_limit',
    'cleanup_old_games',
    'init_db',
    'update_user_points',
    'get_user_stats',
    'get_leaderboard',
    'get_games_quick_reply',
    'get_winner_announcement',
    'get_help_message',
    'get_welcome_message',
    'get_stats_message',
    'get_leaderboard_message',
    'get_join_message',
    'USE_AI',
    'get_gemini_api_key',
    'switch_gemini_key'
]
