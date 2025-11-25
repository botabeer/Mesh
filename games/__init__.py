"""
Bot Mesh - Games Package
Created by: Abeer Aldosari © 2025

This package contains all game modules for Bot Mesh.
Each game inherits from BaseGame and implements:
- next_question(): Generate next question
- check_answer(): Validate user answer
"""

from games.base_game import BaseGame

__all__ = ['BaseGame']
__version__ = '3.0.0'
__author__ = 'Abeer Aldosari'
