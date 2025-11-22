"""Bot Mesh - Games Package | Abeer Aldosari © 2025"""
import os,sys,logging,importlib

__version__='2.0.0'
__author__='Abeer Aldosari'
__all__=[]

logger=logging.getLogger(__name__)
current_dir=os.path.dirname(__file__)

# Load base game first
try:
    from .base_game import BaseGame
    __all__.append('BaseGame')
except ImportError as e:
    logger.error(f"❌ BaseGame: {e}")
    sys.exit(1)

# Auto-load all game files
for f in os.listdir(current_dir):
    if f.endswith("_game.py")and f!="base_game.py":
        m=f[:-3]
        try:
            module=importlib.import_module(f".{m}",package=__name__)
            __all__.append(m)
            logger.debug(f"✅ {m}")
        except Exception as e:
            logger.warning(f"⚠️ {m}: {e}")

logger.info(f"📦 Loaded: {len(__all__)} modules")
