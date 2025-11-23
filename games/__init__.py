"""
Bot Mesh - Games Module
Created by: Abeer Aldosari © 2025

هذا الملف يقوم بتحميل جميع الألعاب تلقائياً
"""
import os
import glob
import importlib
import logging

logger = logging.getLogger(__name__)

# استيراد BaseGame أولاً
from .base_game import BaseGame

# الحصول على مسار المجلد الحالي
current_dir = os.path.dirname(__file__)

# البحث عن جميع الملفات المنتهية بـ _game.py
game_files = glob.glob(os.path.join(current_dir, '*_game.py'))

# استيراد جميع الألعاب تلقائياً
for game_file in game_files:
    # استخراج اسم الملف بدون المسار والامتداد
    module_name = os.path.basename(game_file)[:-3]
    
    # تجاهل base_game
    if module_name == 'base_game':
        continue
    
    try:
        # استيراد الموديول
        module = importlib.import_module(f'.{module_name}', package='games')
        
        # استيراد جميع الكلاسات من الموديول
        for item_name in dir(module):
            item = getattr(module, item_name)
            # التحقق من أنها كلاس وليست BaseGame نفسها
            if (isinstance(item, type) and 
                issubclass(item, BaseGame) and 
                item != BaseGame):
                # إضافة الكلاس إلى namespace الحالي
                globals()[item_name] = item
                logger.info(f"✅ Game class loaded: {item_name}")
    except Exception as e:
        logger.error(f"❌ Failed to load game from {module_name}: {e}")

# تصدير BaseGame والكلاسات المحملة
__all__ = ['BaseGame'] + [name for name in globals() if name.endswith('Game') and name != 'BaseGame']

logger.info(f"✅ Total game classes available: {len(__all__) - 1}")
