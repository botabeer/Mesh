"""
Bot Mesh - Smart Game Loader (Automatic)
Created by: Abeer Aldosari © 2025
Automatically loads all games in the games folder without worrying about class names.
"""

import os
import logging
import importlib
import inspect

# إعداد اللوج
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# استيراد اللعبة الأساسية
from .base_game import BaseGame

# مجلد الألعاب
games_dir = os.path.dirname(__file__)

# قائمة الألعاب الصالحة
games_list = []
invalid_modules = []

# مسح كل ملفات بايثون في مجلد الألعاب
for filename in os.listdir(games_dir):
    if filename.endswith(".py") and filename not in ["__init__.py", "base_game.py", "game_loader.py"]:
        module_name = filename[:-3]
        try:
            module = importlib.import_module(f".{module_name}", package=__package__)
            found_game = False
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if issubclass(obj, BaseGame) and obj.__module__ == module.__name__:
                    games_list.append(obj)
                    logger.info(f"✅ Loaded game: {obj.__name__}")
                    found_game = True
            if not found_game:
                invalid_modules.append(module_name)
                logger.warning(f"⚠️ Module '{module_name}' does not contain a valid BaseGame class")
        except Exception as e:
            invalid_modules.append(module_name)
            logger.error(f"❌ Failed to import module '{module_name}': {e}")

__version__ = "2.0.0"

# ملخص الألعاب
logger.info(f"📊 Total valid games loaded: {len(games_list)}")
if invalid_modules:
    logger.warning(f"⚠️ Modules with issues: {', '.join(invalid_modules)}")
else:
    logger.info("🎉 All game modules loaded successfully")
