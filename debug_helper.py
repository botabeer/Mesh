# -*- coding: utf-8 -*-
"""
Bot Mesh - Debug Helper & Error Diagnostics
Created by: Abeer Aldosari © 2025
"""

import os
import sys
import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler

class BotDebugger:
    """نظام مراقبة وتشخيص شامل للبوت"""
    
    def __init__(self, log_file="bot_mesh_debug.log"):
        self.log_file = log_file
        self.setup_logging()
        self.errors_log = []
        self.warnings_log = []
        
    def setup_logging(self):
        """إعداد نظام تسجيل متقدم"""
        # إنشاء logger رئيسي
        self.logger = logging.getLogger('BotMeshDebug')
        self.logger.setLevel(logging.DEBUG)
        
        # تنسيق الرسائل
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # معالج الملفات (يحفظ آخر 5MB)
        file_handler = RotatingFileHandler(
            self.log_file, 
            maxBytes=5*1024*1024,  # 5MB
            backupCount=3,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        
        # معالج Console
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
    def check_environment(self):
        """فحص المتغيرات البيئية"""
        self.logger.info("=" * 60)
        self.logger.info("🔍 فحص المتغيرات البيئية")
        self.logger.info("=" * 60)
        
        required_vars = {
            'LINE_CHANNEL_SECRET': os.getenv('LINE_CHANNEL_SECRET'),
            'LINE_CHANNEL_ACCESS_TOKEN': os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
        }
        
        optional_vars = {
            'GEMINI_API_KEY_1': os.getenv('GEMINI_API_KEY_1'),
            'GEMINI_API_KEY_2': os.getenv('GEMINI_API_KEY_2'),
            'GEMINI_API_KEY_3': os.getenv('GEMINI_API_KEY_3'),
            'PORT': os.getenv('PORT', '10000')
        }
        
        all_good = True
        
        # فحص المتغيرات المطلوبة
        for var_name, var_value in required_vars.items():
            if not var_value:
                self.logger.error(f"❌ {var_name} مفقود!")
                self.errors_log.append(f"{var_name} غير موجود")
                all_good = False
            else:
                masked_value = var_value[:8] + "..." if len(var_value) > 8 else "***"
                self.logger.info(f"✅ {var_name}: {masked_value}")
        
        # فحص المتغيرات الاختيارية
        for var_name, var_value in optional_vars.items():
            if var_value:
                if var_name.startswith('GEMINI'):
                    masked_value = var_value[:8] + "..."
                else:
                    masked_value = var_value
                self.logger.info(f"✅ {var_name}: {masked_value}")
            else:
                self.logger.warning(f"⚠️ {var_name}: غير موجود (اختياري)")
                self.warnings_log.append(f"{var_name} غير موجود")
        
        return all_good
    
    def check_imports(self):
        """فحص المكتبات المطلوبة"""
        self.logger.info("=" * 60)
        self.logger.info("📦 فحص المكتبات المطلوبة")
        self.logger.info("=" * 60)
        
        required_packages = [
            ('flask', 'Flask'),
            ('linebot', 'LINE Bot SDK'),
            ('dotenv', 'python-dotenv'),
        ]
        
        optional_packages = [
            ('google.generativeai', 'Gemini AI'),
            ('redis', 'Redis'),
        ]
        
        all_good = True
        
        # فحص المكتبات المطلوبة
        for package, display_name in required_packages:
            try:
                __import__(package)
                self.logger.info(f"✅ {display_name} متوفر")
            except ImportError:
                self.logger.error(f"❌ {display_name} مفقود! قم بتثبيت: pip install {package}")
                self.errors_log.append(f"مكتبة {display_name} غير مثبتة")
                all_good = False
        
        # فحص المكتبات الاختيارية
        for package, display_name in optional_packages:
            try:
                __import__(package)
                self.logger.info(f"✅ {display_name} متوفر")
            except ImportError:
                self.logger.warning(f"⚠️ {display_name} غير متوفر (اختياري)")
                self.warnings_log.append(f"مكتبة {display_name} غير مثبتة")
        
        return all_good
    
    def check_files_structure(self):
        """فحص هيكل الملفات"""
        self.logger.info("=" * 60)
        self.logger.info("📁 فحص هيكل الملفات")
        self.logger.info("=" * 60)
        
        required_files = [
            'app.py',
            'config.py',
            'theme_styles.py',
            'ui_builder.py',
            'requirements.txt'
        ]
        
        required_dirs = [
            'games',
        ]
        
        all_good = True
        
        # فحص الملفات
        for file in required_files:
            if os.path.exists(file):
                size = os.path.getsize(file)
                self.logger.info(f"✅ {file} ({size} bytes)")
            else:
                self.logger.error(f"❌ {file} مفقود!")
                self.errors_log.append(f"ملف {file} غير موجود")
                all_good = False
        
        # فحص المجلدات
        for directory in required_dirs:
            if os.path.isdir(directory):
                files_count = len([f for f in os.listdir(directory) if f.endswith('.py')])
                self.logger.info(f"✅ {directory}/ ({files_count} ملف)")
            else:
                self.logger.error(f"❌ {directory}/ مفقود!")
                self.errors_log.append(f"مجلد {directory} غير موجود")
                all_good = False
        
        return all_good
    
    def check_games_loading(self):
        """فحص تحميل الألعاب"""
        self.logger.info("=" * 60)
        self.logger.info("🎮 فحص تحميل الألعاب")
        self.logger.info("=" * 60)
        
        games_list = [
            "IQ", "رياضيات", "لون الكلمة", "كلمة مبعثرة",
            "كتابة سريعة", "عكس", "حروف وكلمات", "أغنية",
            "إنسان حيوان نبات", "سلسلة كلمات", "تخمين", "توافق"
        ]
        
        game_modules = {
            "IQ": "games.iq_game",
            "رياضيات": "games.math_game",
            "لون الكلمة": "games.word_color_game",
            "كلمة مبعثرة": "games.scramble_word_game",
            "كتابة سريعة": "games.fast_typing_game",
            "عكس": "games.opposite_game",
            "حروف وكلمات": "games.letters_words_game",
            "أغنية": "games.song_game",
            "إنسان حيوان نبات": "games.human_animal_plant_game",
            "سلسلة كلمات": "games.chain_words_game",
            "تخمين": "games.guess_game",
            "توافق": "games.compatibility_game"
        }
        
        loaded_count = 0
        
        for game_name, module_path in game_modules.items():
            try:
                __import__(module_path)
                self.logger.info(f"✅ {game_name} ({module_path})")
                loaded_count += 1
            except ImportError as e:
                self.logger.error(f"❌ {game_name} فشل التحميل: {str(e)}")
                self.errors_log.append(f"لعبة {game_name} فشل تحميلها")
            except Exception as e:
                self.logger.error(f"❌ {game_name} خطأ غير متوقع: {str(e)}")
                self.errors_log.append(f"لعبة {game_name} خطأ في التحميل")
        
        self.logger.info(f"📊 تم تحميل {loaded_count}/{len(game_modules)} لعبة")
        
        return loaded_count > 0
    
    def check_config_validation(self):
        """فحص ملف الإعدادات"""
        self.logger.info("=" * 60)
        self.logger.info("⚙️ فحص ملف الإعدادات")
        self.logger.info("=" * 60)
        
        try:
            from config import (
                BOT_NAME, BOT_VERSION, LINE_CHANNEL_SECRET,
                LINE_CHANNEL_ACCESS_TOKEN, GEMINI_API_KEYS,
                AI_ENABLED, BOT_SETTINGS, GAMES_LIST
            )
            
            self.logger.info(f"✅ BOT_NAME: {BOT_NAME}")
            self.logger.info(f"✅ BOT_VERSION: {BOT_VERSION}")
            self.logger.info(f"✅ AI_ENABLED: {AI_ENABLED}")
            self.logger.info(f"✅ GEMINI_KEYS: {len(GEMINI_API_KEYS)} مفاتيح")
            self.logger.info(f"✅ GAMES_LIST: {len(GAMES_LIST)} لعبة")
            self.logger.info(f"✅ Silent Mode: {'مفعل' if BOT_SETTINGS.get('silent_mode') else 'معطل'}")
            self.logger.info(f"✅ Registered Only: {'نعم' if BOT_SETTINGS.get('registered_users_only') else 'لا'}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ خطأ في config.py: {str(e)}")
            self.errors_log.append(f"خطأ في config.py: {str(e)}")
            return False
    
    def test_line_connection(self):
        """اختبار الاتصال بـ LINE"""
        self.logger.info("=" * 60)
        self.logger.info("🔗 اختبار الاتصال بـ LINE")
        self.logger.info("=" * 60)
        
        try:
            from linebot.v3.messaging import Configuration, ApiClient, MessagingApi
            from config import LINE_CHANNEL_ACCESS_TOKEN
            
            configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)
            
            with ApiClient(configuration) as api_client:
                line_bot_api = MessagingApi(api_client)
                # محاولة الاتصال البسيطة
                self.logger.info("✅ تم إنشاء كائن LINE API بنجاح")
                return True
                
        except Exception as e:
            self.logger.error(f"❌ فشل الاتصال بـ LINE: {str(e)}")
            self.errors_log.append(f"فشل الاتصال بـ LINE: {str(e)}")
            return False
    
    def generate_report(self):
        """توليد تقرير شامل"""
        self.logger.info("=" * 60)
        self.logger.info("📋 ملخص التشخيص")
        self.logger.info("=" * 60)
        
        if self.errors_log:
            self.logger.error(f"❌ عدد الأخطاء: {len(self.errors_log)}")
            for i, error in enumerate(self.errors_log, 1):
                self.logger.error(f"   {i}. {error}")
        else:
            self.logger.info("✅ لا توجد أخطاء حرجة")
        
        if self.warnings_log:
            self.logger.warning(f"⚠️ عدد التحذيرات: {len(self.warnings_log)}")
            for i, warning in enumerate(self.warnings_log, 1):
                self.logger.warning(f"   {i}. {warning}")
        else:
            self.logger.info("✅ لا توجد تحذيرات")
        
        self.logger.info("=" * 60)
        
        if not self.errors_log:
            self.logger.info("🎉 البوت جاهز للعمل!")
            return True
        else:
            self.logger.error("⚠️ يرجى إصلاح الأخطاء أعلاه قبل تشغيل البوت")
            return False
    
    def run_full_diagnosis(self):
        """تشغيل كامل الفحوصات"""
        self.logger.info("")
        self.logger.info("🔬 بدء التشخيص الشامل للبوت")
        self.logger.info(f"⏰ الوقت: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.logger.info("")
        
        checks = [
            ("المتغيرات البيئية", self.check_environment),
            ("المكتبات المطلوبة", self.check_imports),
            ("هيكل الملفات", self.check_files_structure),
            ("ملف الإعدادات", self.check_config_validation),
            ("تحميل الألعاب", self.check_games_loading),
            ("الاتصال بـ LINE", self.test_line_connection),
        ]
        
        results = {}
        for check_name, check_func in checks:
            try:
                results[check_name] = check_func()
            except Exception as e:
                self.logger.error(f"❌ خطأ في فحص {check_name}: {str(e)}")
                results[check_name] = False
                self.errors_log.append(f"خطأ في فحص {check_name}")
        
        # توليد التقرير النهائي
        return self.generate_report()


def run_debug():
    """تشغيل التشخيص من سطر الأوامر"""
    debugger = BotDebugger()
    success = debugger.run_full_diagnosis()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ التشخيص اكتمل بنجاح - البوت جاهز للتشغيل")
        print(f"📝 سجل الأخطاء محفوظ في: {debugger.log_file}")
        sys.exit(0)
    else:
        print("❌ التشخيص وجد أخطاء - يرجى إصلاحها")
        print(f"📝 راجع السجل في: {debugger.log_file}")
        sys.exit(1)


if __name__ == "__main__":
    run_debug()
