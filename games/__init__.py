"""
games/__init__.py - تصدير الألعاب
"""

from .base_game import BaseGame
from .letters_game import LettersGame
from .fast_game import FastGame
from .scramble_game import ScrambleGame
from .chain_game import ChainGame
from .iq_game import IQGame

__all__ = [
    'BaseGame',
    'LettersGame',
    'FastGame',
    'ScrambleGame',
    'ChainGame',
    'IQGame'
]
