"""
Bot Mesh - Games Package
Created by: Abeer Aldosari © 2025

هذا الملف يجعل مجلد games حزمة Python ويحمّل كل الألعاب تلقائياً
"""
import os
import sys
import logging
import importlib

__version__ = '2.0.0'
__author__ = 'Abeer Aldosari'
__all__ = []

logger = logging.getLogger(__name__)

# مسار المجلد الحالي
current_dir = os.path.dirname(__file__)

# تأكد من وجود base_game أولاً
try:
    from .base_game import BaseGame
    __all__.append('BaseGame')
except ImportError as e:
    logger.error(f"❌ Failed to load BaseGame: {e}")
    sys.exit(1)

# البحث عن جميع ملفات الألعاب
for filename in os.listdir(current_dir):
    if filename.endswith("_game.py") and filename != "base_game.py":
        module_name = filename[:-3]
        try:
            module = importlib.import_module(f".{module_name}", package=__name__)
            __all__.append(module_name)
            logger.debug(f"✅ Loaded game module: {module_name}")
        except Exception as e:
            logger.warning(f"⚠️ Failed to load {module_name}: {e}")

logger.info(f"📦 Games package loaded: {len(__all__)} modules")
