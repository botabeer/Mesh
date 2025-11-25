"""
Bot Mesh v6.1 - Game Loader
Automatic game loading from games/ folder
"""

import os
import sys
import importlib
import inspect
import logging

logger = logging.getLogger(__name__)

# إضافة مجلد games للمسار
games_dir = os.path.dirname(os.path.abspath(__file__))
if games_dir not in sys.path:
    sys.path.insert(0, games_dir)

def load_games():
    """تحميل جميع الألعاب من مجلد games/"""
    games = {}
    
    # البحث عن جميع ملفات Python في المجلد
    for filename in os.listdir(games_dir):
        if filename.endswith('.py') and filename not in ['__init__.py', 'game_loader.py', 'base_game.py']:
            module_name = filename[:-3]
            
            try:
                # استيراد الوحدة
                module = importlib.import_module(module_name)
                
                # البحث عن class اللعبة
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    # تحقق من أن الكلاس يحتوي على الدوال المطلوبة
                    if (hasattr(obj, 'start') and 
                        hasattr(obj, 'check_answer') and
                        hasattr(obj, 'generate_question') and
                        obj.__module__ == module.__name__):
                        
                        # استخراج اسم اللعبة من اسم الكلاس
                        game_name = extract_game_name(name)
                        games[game_name] = obj
                        logger.info(f"✅ تم تحميل: {game_name} ({name})")
                        break
            
            except Exception as e:
                logger.error(f"❌ فشل تحميل {module_name}: {e}")
    
    logger.info(f"📦 إجمالي الألعاب المحملة: {len(games)}")
    return games

def extract_game_name(class_name):
    """استخراج اسم اللعبة من اسم الكلاس"""
    # خريطة أسماء الكلاسات إلى أسماء الألعاب
    name_map = {
        'IqGame': 'ذكاء',
        'IQGame': 'ذكاء',
        'MathGame': 'رياضيات',
        'ColorGame': 'ألوان',
        'WordColorGame': 'ألوان',
        'SpeedGame': 'سرعة',
        'FastTypingGame': 'سرعة',
        'WordsGame': 'كلمات',
        'ScrambleWordGame': 'كلمات',
        'LettersWordsGame': 'كلمات',
        'SongGame': 'أغاني',
        'OppositeGame': 'أضداد',
        'GuessGame': 'تخمين',
        'ChainWordsGame': 'سلسلة',
        'HumanAnimalPlantGame': 'إنسان حيوان',
        'CompatibilityGame': 'توافق'
    }
    
    # إذا كان الاسم في الخريطة
    if class_name in name_map:
        return name_map[class_name]
    
    # محاولة استخراج الاسم تلقائياً
    # IqGame -> iq
    name = class_name.replace('Game', '').lower()
    return name
