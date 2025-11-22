"""
Bot Mesh - Games Package
Created by: Abeer Aldosari © 2025
"""
import os
import logging
import importlib

__version__ = '2.0.0'
__author__ = 'Abeer Aldosari'
__all__ = []

logger = logging.getLogger(__name__)
current_dir = os.path.dirname(__file__)

# Load base game
try:
    from .base_game import BaseGame
    __all__.append('BaseGame')
except ImportError as e:
    logger.error(f"❌ BaseGame: {e}")

# Auto-load all games
for f in os.listdir(current_dir):
    if f.endswith("_game.py") and f != "base_game.py":
        module_name = f[:-3]
        try:
            module = importlib.import_module(f".{module_name}", package=__name__)
            __all__.append(module_name)
            logger.debug(f"✅ {module_name}")
        except Exception as e:
            logger.warning(f"⚠️ {module_name}: {e}")

logger.info(f"📦 Games loaded: {len(__all__)}")
