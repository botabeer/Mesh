"""
Bot Mesh - Games Package
Created by: Abeer Aldosari © 2025

هذا الملف يقوم بتحميل جميع الألعاب تلقائياً
"""
import os
import logging
import importlib

logger = logging.getLogger(__name__)

# تصدير اللعبة الأساسية
from .base_game import BaseGame

__version__ = '2.0.0'
__author__ = 'Abeer Aldosari'
__all__ = ['BaseGame']

# المجلد الحالي
current_dir = os.path.dirname(__file__)

# تحميل جميع الألعاب تلقائياً
for filename in os.listdir(current_dir):
    if filename.endswith('_game.py') and filename != 'base_game.py':
        module_name = filename[:-3]  # إزالة .py
        
        try:
            # استيراد الموديول
            module = importlib.import_module(f'.{module_name}', package=__name__)
            
            # إضافة إلى __all__
            __all__.append(module_name)
            
            # تصدير الكلاسات
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if (isinstance(attr, type) and 
                    issubclass(attr, BaseGame) and 
                    attr is not BaseGame):
                    globals()[attr_name] = attr
                    __all__.append(attr_name)
                    logger.info(f"✅ تم تحميل: {attr_name}")
        
        except Exception as e:
            logger.warning(f"⚠️ فشل تحميل {module_name}: {e}")

logger.info(f"📦 تم تحميل {len(__all__)} عنصر من مجلد الألعاب")
