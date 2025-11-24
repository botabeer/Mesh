# -*- coding: utf-8 -*-
"""
Bot Mesh - Enhanced Debug & Diagnostics System
Created by: Abeer Aldosari © 2025
نظام تشخيص شامل مع الحفاظ على جميع القواعد الثابتة
"""

import os
import sys
import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler
import traceback

class BotDiagnostics:
    """نظام تشخيص متقدم للبوت"""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.info = []
        self.setup_logging()
        
    def setup_logging(self):
        """إعداد نظام تسجيل محسّن"""
        log_format = '%(asctime)s | %(levelname)-8s | %(message)s'
        
        # File handler
        file_handler = RotatingFileHandler(
            'bot_diagnostics.log',
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        
        # Format
        formatter = logging.Formatter(log_format, datefmt='%Y-%m-%d %H:%M:%S')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Logger
        self.logger = logging.getLogger('BotMeshDiagnostics')
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def log_section(self, title):
        """طباعة عنوان قسم"""
        separator = "=" * 70
        self.logger.info("")
        self.logger.info(separator)
        self.logger.info(f"  {title}")
        self.logger.info(separator)
    
    def check_environment_variables(self):
        """فحص المتغيرات البيئية المطلوبة"""
        self.log_section("🔍 فحص المتغيرات البيئية")
        
        required = {
            'LINE_CHANNEL_SECRET': os.getenv('LINE_CHANNEL_SECRET'),
            'LINE_CHANNEL_ACCESS_TOKEN': os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
        }
        
        optional = {
            'GEMINI_API_KEY_1': os.getenv('GEMINI_API_KEY_1'),
            'GEMINI_API_KEY_2': os.getenv('GEMINI_API_KEY_2'),
            'GEMINI_API_KEY_3': os.getenv('GEMINI_API_KEY_3'),
            'PORT': os.getenv('PORT', '10000')
        }
        
        all_ok = True
        
        # فحص المطلوبة
        for key, value in required.items():
            if not value:
                self.logger.error(f"❌ {key}: مفقود")
                self.errors.append(f"{key} غير موجود في المتغيرات البيئية")
                all_ok = False
            else:
                masked = value[:10] + "..." if len(value) > 10 else "***"
                self.logger.info(f"✅ {key}: {masked}")
                
        # فحص الاختيارية
        for key, value in optional.items():
            if value:
                if 'GEMINI' in key:
                    masked = value[:10] + "..."
                else:
                    masked = value
                self.logger.info(f"✅ {key}: {masked}")
            else:
                self.logger.warning(f"⚠️  {key}: غير موجود (اختياري)")
                self.warnings.append(f"{key} غير متاح")
        
        return all_ok
    
    def check_python_packages(self):
        """فحص المكتبات المطلوبة"""
        self.log_section("📦 فحص المكتبات المثبتة")
        
        required_packages = [
            ('flask', 'Flask'),
            ('linebot', 'LINE Bot SDK'),
            ('dotenv', 'python-dotenv'),
        ]
        
        optional_packages = [
            ('google.generativeai', 'Gemini AI'),
            ('redis', 'Redis'),
            ('apscheduler', 'APScheduler'),
        ]
        
        all_ok = True
        
        for package, name in required_packages:
            try:
                __import__(package)
                self.logger.info(f"✅ {name} - متوفر")
            except ImportError:
                self.logger.error(f"❌ {name} - مفقود")
                self.errors.append(f"مكتبة {name} غير مثبتة")
                all_ok = False
        
        for package, name in optional_packages:
            try:
                __import__(package)
                self.logger.info(f"✅ {name} - متوفر")
            except ImportError:
                self.logger.warning(f"⚠️  {name} - غير متوفر")
                self.warnings.append(f"مكتبة {name} غير مثبتة")
        
        return all_ok
    
    def check_file_structure(self):
        """فحص هيكل الملفات"""
        self.log_section("📁 فحص هيكل الملفات")
        
        required_files = [
            'app.py',
            'config.py',
            'theme_styles.py',
            'ui_builder.py',
            'requirements.txt',
            'runtime.txt'
        ]
        
        required_dirs = ['games']
        
        all_ok = True
        
        for file in required_files:
            if os.path.exists(file):
                size = os.path.getsize(file)
                self.logger.info(f"✅ {file} ({size:,} bytes)")
            else:
                self.logger.error(f"❌ {file} - مفقود")
                self.errors.append(f"ملف {file} غير موجود")
                all_ok = False
        
        for directory in required_dirs:
            if os.path.isdir(directory):
                files = [f for f in os.listdir(directory) if f.endswith('.py')]
                self.logger.info(f"✅ {directory}/ ({len(files)} ملفات)")
                
                # فحص الملفات داخل المجلد
                for game_file in files:
                    if game_file not in ['__init__.py', 'base_game.py']:
                        path = os.path.join(directory, game_file)
                        size = os.path.getsize(path)
                        self.logger.info(f"   - {game_file} ({size:,} bytes)")
            else:
                self.logger.error(f"❌ {directory}/ - مفقود")
                self.errors.append(f"مجلد {directory} غير موجود")
                all_ok = False
        
        return all_ok
    
    def check_config_file(self):
        """فحص ملف الإعدادات"""
        self.log_section("⚙️  فحص ملف الإعدادات")
        
        try:
            sys.path.insert(0, os.getcwd())
            import config
            
            attributes = [
                'BOT_NAME',
                'LINE_CHANNEL_SECRET',
                'LINE_CHANNEL_ACCESS_TOKEN',
                'GEMINI_API_KEYS',
                'AI_ENABLED',
                'BOT_SETTINGS',
                'GAMES_LIST'
            ]
            
            for attr in attributes:
                if hasattr(config, attr):
                    value = getattr(config, attr)
                    if isinstance(value, (str, int, bool)):
                        self.logger.info(f"✅ {attr}: {value}")
                    elif isinstance(value, list):
                        self.logger.info(f"✅ {attr}: قائمة ({len(value)} عناصر)")
                    elif isinstance(value, dict):
                        self.logger.info(f"✅ {attr}: قاموس ({len(value)} مفاتيح)")
                    else:
                        self.logger.info(f"✅ {attr}: موجود")
                else:
                    self.logger.error(f"❌ {attr}: مفقود")
                    self.errors.append(f"متغير {attr} غير موجود في config.py")
            
            # فحص القواعد الثابتة
            if hasattr(config, 'BOT_SETTINGS'):
                settings = config.BOT_SETTINGS
                self.logger.info("")
                self.logger.info("📋 القواعد الثابتة:")
                self.logger.info(f"   - Silent Mode: {settings.get('silent_mode', 'غير محدد')}")
                self.logger.info(f"   - Registered Only: {settings.get('registered_users_only', 'غير محدد')}")
                self.logger.info(f"   - Auto Delete Days: {settings.get('auto_delete_after_days', 'غير محدد')}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ خطأ في تحميل config.py: {str(e)}")
            self.logger.error(traceback.format_exc())
            self.errors.append(f"فشل تحميل config.py: {str(e)}")
            return False
    
    def check_games_loading(self):
        """فحص تحميل الألعاب"""
        self.log_section("🎮 فحص الألعاب")
        
        games_map = {
            "IQ": "iq_game.py",
            "رياضيات": "math_game.py",
            "لون الكلمة": "word_color_game.py",
            "كلمة مبعثرة": "scramble_word_game.py",
            "كتابة سريعة": "fast_typing_game.py",
            "عكس": "opposite_game.py",
            "حروف وكلمات": "letters_words_game.py",
            "أغنية": "song_game.py",
            "إنسان حيوان نبات": "human_animal_plant_game.py",
            "سلسلة كلمات": "chain_words_game.py",
            "تخمين": "guess_game.py",
            "توافق": "compatibility_game.py"
        }
        
        loaded_count = 0
        
        for game_name, file_name in games_map.items():
            file_path = os.path.join('games', file_name)
            
            if os.path.exists(file_path):
                try:
                    module_name = file_name[:-3]
                    module = __import__(f'games.{module_name}', fromlist=['*'])
                    
                    # البحث عن الكلاس
                    class_found = False
                    for attr_name in dir(module):
                        attr = getattr(module, attr_name)
                        if isinstance(attr, type) and attr_name.endswith('Game'):
                            self.logger.info(f"✅ {game_name} ({attr_name}) - محمل")
                            loaded_count += 1
                            class_found = True
                            break
                    
                    if not class_found:
                        self.logger.warning(f"⚠️  {game_name} - الملف موجود لكن الكلاس غير موجود")
                        self.warnings.append(f"لعبة {game_name} - كلاس غير موجود")
                        
                except Exception as e:
                    self.logger.error(f"❌ {game_name} - فشل التحميل: {str(e)}")
                    self.errors.append(f"فشل تحميل لعبة {game_name}: {str(e)}")
            else:
                self.logger.error(f"❌ {game_name} - الملف مفقود ({file_name})")
                self.errors.append(f"ملف لعبة {game_name} غير موجود")
        
        self.logger.info(f"\n📊 تم تحميل {loaded_count}/{len(games_map)} لعبة")
        
        return loaded_count > 0
    
    def test_line_imports(self):
        """اختبار استيراد مكتبات LINE"""
        self.log_section("🔗 اختبار LINE SDK")
        
        try:
            from linebot.v3 import WebhookHandler
            from linebot.v3.messaging import Configuration, ApiClient, MessagingApi
            from linebot.v3.webhooks import MessageEvent, TextMessageContent
            
            self.logger.info("✅ WebhookHandler - متاح")
            self.logger.info("✅ Configuration - متاح")
            self.logger.info("✅ MessagingApi - متاح")
            self.logger.info("✅ MessageEvent - متاح")
            
            # اختبار إنشاء Configuration
            token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', 'test')
            config = Configuration(access_token=token)
            self.logger.info("✅ Configuration object - تم الإنشاء")
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ فشل استيراد LINE SDK: {str(e)}")
            self.logger.error(traceback.format_exc())
            self.errors.append(f"مشكلة في LINE SDK: {str(e)}")
            return False
    
    def check_ui_builder(self):
        """فحص ui_builder.py"""
        self.log_section("🎨 فحص UI Builder")
        
        try:
            from ui_builder import UIBuilder
            
            # اختبار الدوال
            methods = ['build_home', 'build_games_menu', 'build_info', 
                      'build_my_points', 'build_leaderboard']
            
            for method in methods:
                if hasattr(UIBuilder, method):
                    self.logger.info(f"✅ {method} - موجود")
                else:
                    self.logger.error(f"❌ {method} - مفقود")
                    self.errors.append(f"دالة {method} غير موجودة في UIBuilder")
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ فشل تحميل UIBuilder: {str(e)}")
            self.logger.error(traceback.format_exc())
            self.errors.append(f"مشكلة في UIBuilder: {str(e)}")
            return False
    
    def generate_report(self):
        """توليد تقرير نهائي"""
        self.log_section("📋 تقرير التشخيص النهائي")
        
        # الأخطاء
        if self.errors:
            self.logger.error(f"\n🚨 عدد الأخطاء الحرجة: {len(self.errors)}")
            for i, error in enumerate(self.errors, 1):
                self.logger.error(f"   {i}. {error}")
        else:
            self.logger.info("\n✅ لا توجد أخطاء حرجة")
        
        # التحذيرات
        if self.warnings:
            self.logger.warning(f"\n⚠️  عدد التحذيرات: {len(self.warnings)}")
            for i, warning in enumerate(self.warnings, 1):
                self.logger.warning(f"   {i}. {warning}")
        else:
            self.logger.info("\n✅ لا توجد تحذيرات")
        
        # الخلاصة
        self.logger.info("\n" + "=" * 70)
        if not self.errors:
            self.logger.info("🎉 البوت جاهز للتشغيل!")
            self.logger.info("✅ جميع الفحوصات نجحت")
            return True
        else:
            self.logger.error("⚠️  البوت غير جاهز - يرجى إصلاح الأخطاء أعلاه")
            return False
    
    def run_full_check(self):
        """تشغيل كامل الفحوصات"""
        self.logger.info("\n" + "=" * 70)
        self.logger.info("🔬 بدء التشخيص الشامل للبوت")
        self.logger.info(f"⏰ الوقت: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.logger.info("=" * 70)
        
        checks = [
            ("المتغيرات البيئية", self.check_environment_variables),
            ("المكتبات المطلوبة", self.check_python_packages),
            ("هيكل الملفات", self.check_file_structure),
            ("ملف الإعدادات", self.check_config_file),
            ("LINE SDK", self.test_line_imports),
            ("UI Builder", self.check_ui_builder),
            ("الألعاب", self.check_games_loading),
        ]
        
        results = {}
        for check_name, check_func in checks:
            try:
                results[check_name] = check_func()
            except Exception as e:
                self.logger.error(f"❌ خطأ في فحص {check_name}: {str(e)}")
                self.logger.error(traceback.format_exc())
                results[check_name] = False
                self.errors.append(f"خطأ في فحص {check_name}")
        
        return self.generate_report()


def main():
    """تشغيل التشخيص"""
    diagnostics = BotDiagnostics()
    success = diagnostics.run_full_check()
    
    print("\n" + "=" * 70)
    if success:
        print("✅ التشخيص اكتمل بنجاح")
        print("🚀 يمكنك الآن تشغيل البوت بأمان")
        print("📝 السجل محفوظ في: bot_diagnostics.log")
        sys.exit(0)
    else:
        print("❌ وجدت أخطاء - يرجى مراجعة السجل")
        print("📝 السجل محفوظ في: bot_diagnostics.log")
        sys.exit(1)


if __name__ == "__main__":
    main()
