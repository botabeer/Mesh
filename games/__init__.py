"""
Bot Mesh - Games Package
Created by: Abeer Aldosari © 2025

هذا الملف يجعل مجلد games حزمة Python ويحمّل كل الألعاب تلقائياً
"""

import os
import importlib

__version__ = '1.0.0'
__author__ = 'Abeer Aldosari'
__all__ = []

# مسار المجلد الحالي
current_dir = os.path.dirname(__file__)

# البحث عن جميع ملفات الألعاب (تبدأ وتنتهي بـ _game.py)
for filename in os.listdir(current_dir):
    if filename.endswith("_game.py") and not filename.startswith("__"):
        module_name = filename[:-3]  # إزالة ".py"
        try:
            module = importlib.import_module(f".{module_name}", package=__name__)
            __all__.append(module_name)
        except Exception as e:
            print(f"⚠️ فشل تحميل اللعبة {module_name}: {e}")

# الآن يمكن استيراد كل الألعاب هكذا:
# from games import iq_game, word_color_game, ...
