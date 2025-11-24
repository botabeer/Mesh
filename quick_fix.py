# -*- coding: utf-8 -*-
"""
Bot Mesh - Quick Fix Tool
Created by: Abeer Aldosari © 2025
أداة إصلاح سريعة للمشاكل الشائعة
"""

import os
import sys

class QuickFix:
    """أداة إصلاح سريعة"""
    
    def __init__(self):
        self.fixes_applied = []
    
    def fix_env_file(self):
        """التحقق من وجود ملف .env"""
        print("🔧 فحص ملف .env...")
        
        if not os.path.exists('.env'):
            print("❌ ملف .env غير موجود")
            print("\n📝 قم بإنشاء ملف .env بالمحتوى التالي:")
            print("""
LINE_CHANNEL_SECRET=your_channel_secret_here
LINE_CHANNEL_ACCESS_TOKEN=your_access_token_here
GEMINI_API_KEY_1=your_gemini_key_here
PORT=10000
            """)
            return False
        else:
            print("✅ ملف .env موجود")
            
            # قراءة المحتوى
            with open('.env', 'r') as f:
                content = f.read()
            
            # التحقق من المتغيرات المطلوبة
            required = ['LINE_CHANNEL_SECRET', 'LINE_CHANNEL_ACCESS_TOKEN']
            missing = []
            
            for var in required:
                if var not in content or f'{var}=' in content and content.split(f'{var}=')[1].split('\n')[0].strip() == '':
                    missing.append(var)
            
            if missing:
                print(f"⚠️  المتغيرات التالية مفقودة أو فارغة: {', '.join(missing)}")
                return False
            
            print("✅ جميع المتغيرات المطلوبة موجودة")
            return True
    
    def fix_games_init(self):
        """إصلاح ملف __init__.py في مجلد games"""
        print("\n🔧 فحص games/__init__.py...")
        
        games_init = 'games/__init__.py'
        
        if not os.path.exists('games'):
            print("❌ مجلد games غير موجود")
            return False
        
        if not os.path.exists(games_init):
            print("⚠️  ملف __init__.py غير موجود - سيتم إنشاؤه")
            
            content = '''"""
Bot Mesh - Games Package
Created by: Abeer Aldosari © 2025
"""

from .iq_game import IqGame
from .math_game import MathGame
from .word_color_game import WordColorGame
from .scramble_word_game import ScrambleWordGame
from .fast_typing_game import FastTypingGame
from .opposite_game import OppositeGame
from .letters_words_game import LettersWordsGame
from .song_game import SongGame
from .human_animal_plant_game import HumanAnimalPlantGame
from .chain_words_game import ChainWordsGame
from .guess_game import GuessGame
from .compatibility_game import CompatibilityGame

__all__ = [
    'IqGame',
    'MathGame',
    'WordColorGame',
    'ScrambleWordGame',
    'FastTypingGame',
    'OppositeGame',
    'LettersWordsGame',
    'SongGame',
    'HumanAnimalPlantGame',
    'ChainWordsGame',
    'GuessGame',
    'CompatibilityGame'
]
'''
            
            with open(games_init, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ تم إنشاء __init__.py")
            self.fixes_applied.append("إنشاء games/__init__.py")
            return True
        else:
            print("✅ ملف __init__.py موجود")
            return True
    
    def check_port_availability(self):
        """التحقق من توفر المنفذ"""
        print("\n🔧 فحص المنفذ...")
        
        import socket
        port = int(os.getenv('PORT', 10000))
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('127.0.0.1', port))
            sock.close()
            
            if result == 0:
                print(f"⚠️  المنفذ {port} مستخدم بالفعل")
                print(f"💡 جرب تغيير PORT في ملف .env إلى منفذ آخر (مثل {port + 1})")
                return False
            else:
                print(f"✅ المنفذ {port} متاح")
                return True
        except Exception as e:
            print(f"⚠️  لم نتمكن من فحص المنفذ: {e}")
            return True
    
    def check_python_version(self):
        """التحقق من إصدار Python"""
        print("\n🔧 فحص إصدار Python...")
        
        version = sys.version_info
        print(f"📌 إصدار Python الحالي: {version.major}.{version.minor}.{version.micro}")
        
        if version.major < 3 or (version.major == 3 and version.minor < 11):
            print("⚠️  يتطلب البوت Python 3.11 أو أحدث")
            print(f"💡 الإصدار الحالي: {version.major}.{version.minor}.{version.micro}")
            return False
        
        print("✅ إصدار Python مناسب")
        return True
    
    def verify_imports(self):
        """التحقق من الاستيرادات الأساسية"""
        print("\n🔧 فحص الاستيرادات الأساسية...")
        
        imports = [
            ('flask', 'Flask'),
            ('linebot.v3', 'LINE Bot SDK'),
            ('dotenv', 'python-dotenv'),
        ]
        
        all_ok = True
        for module, name in imports:
            try:
                __import__(module)
                print(f"✅ {name}")
            except ImportError:
                print(f"❌ {name} - غير مثبت")
                print(f"   قم بتشغيل: pip install {module}")
                all_ok = False
        
        return all_ok
    
    def run_all_fixes(self):
        """تشغيل جميع الإصلاحات"""
        print("=" * 70)
        print("🔧 أداة الإصلاح السريع لـ Bot Mesh")
        print("=" * 70)
        
        checks = [
            ("إصدار Python", self.check_python_version),
            ("الاستيرادات", self.verify_imports),
            ("ملف .env", self.fix_env_file),
            ("games/__init__.py", self.fix_games_init),
            ("المنفذ", self.check_port_availability),
        ]
        
        results = {}
        for name, func in checks:
            try:
                results[name] = func()
            except Exception as e:
                print(f"❌ خطأ في {name}: {e}")
                results[name] = False
        
        print("\n" + "=" * 70)
        print("📊 ملخص الإصلاحات:")
        print("=" * 70)
        
        passed = sum(1 for v in results.values() if v)
        total = len(results)
        
        for name, result in results.items():
            status = "✅" if result else "❌"
            print(f"{status} {name}")
        
        print(f"\n📈 النتيجة: {passed}/{total} فحص نجح")
        
        if self.fixes_applied:
            print("\n🔧 الإصلاحات المطبقة:")
            for fix in self.fixes_applied:
                print(f"   ✓ {fix}")
        
        print("\n" + "=" * 70)
        
        if passed == total:
            print("🎉 جميع الفحوصات نجحت!")
            print("🚀 يمكنك الآن تشغيل البوت")
            print("\n📝 للتشغيل:")
            print("   python app.py")
        else:
            print("⚠️  بعض الفحوصات فشلت")
            print("📝 يرجى إصلاح المشاكل أعلاه ثم المحاولة مرة أخرى")
        
        print("=" * 70)


def main():
    fixer = QuickFix()
    fixer.run_all_fixes()


if __name__ == "__main__":
    main()
