#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

print("=" * 60)
print("اختبار شامل لبوت Bot Mesh")
print("=" * 60)

# 1. اختبار استيراد المكتبات
print("\n1. اختبار المكتبات الاساسية...")
try:
    import flask
    print("   ✓ Flask")
    from linebot.v3 import WebhookHandler
    print("   ✓ LINE Bot SDK v3")
    from linebot.v3.messaging import Configuration, MessagingApi
    print("   ✓ LINE Messaging API")
    import sqlite3
    print("   ✓ SQLite3")
    from apscheduler.schedulers.blocking import BlockingScheduler
    print("   ✓ APScheduler")
    print("   ✓ جميع المكتبات موجودة")
except ImportError as e:
    print(f"   ✗ خطأ في المكتبات: {e}")
    sys.exit(1)

# 2. اختبار استيراد ملفات المشروع
print("\n2. اختبار ملفات المشروع...")
try:
    from config import Config
    print("   ✓ config.py")
    from database import Database
    print("   ✓ database.py")
    from game_manager import GameManager
    print("   ✓ game_manager.py")
    from text_manager import TextManager
    print("   ✓ text_manager.py")
    from ui import UI
    print("   ✓ ui.py")
    print("   ✓ جميع الملفات موجودة")
except ImportError as e:
    print(f"   ✗ خطأ في استيراد الملفات: {e}")
    sys.exit(1)

# 3. اختبار قاعدة البيانات
print("\n3. اختبار قاعدة البيانات...")
try:
    db = Database(":memory:")
    user_id = "test_user_123"
    
    # تسجيل مستخدم
    db.register_user(user_id, "اختبار")
    user = db.get_user(user_id)
    assert user is not None, "فشل تسجيل المستخدم"
    assert user['name'] == "اختبار", "خطأ في اسم المستخدم"
    print("   ✓ تسجيل المستخدم")
    
    # اضافة نقاط
    db.add_points(user_id, 10)
    user = db.get_user(user_id)
    assert user['points'] == 10, "خطأ في اضافة النقاط"
    print("   ✓ اضافة النقاط")
    
    # الالعاب والفوز
    db.increment_games(user_id)
    db.increment_wins(user_id)
    user = db.get_user(user_id)
    assert user['games'] == 1, "خطأ في عدد الالعاب"
    assert user['wins'] == 1, "خطأ في عدد الفوز"
    assert user['streak'] == 1, "خطأ في السلسلة"
    print("   ✓ احصائيات اللعب")
    
    # الانجازات
    achievements = db.check_achievements(user_id)
    assert len(achievements) > 0, "خطأ في الانجازات"
    print("   ✓ نظام الانجازات")
    
    print("   ✓ قاعدة البيانات تعمل بشكل صحيح")
except Exception as e:
    print(f"   ✗ خطأ في قاعدة البيانات: {e}")
    sys.exit(1)

# 4. اختبار التطبيع
print("\n4. اختبار تطبيع النصوص...")
try:
    assert Config.normalize("أَحْمَد") == "احمد"
    assert Config.normalize("إبراهيم") == "ابراهيم"
    assert Config.normalize("مُحَمَّد") == "محمد"
    assert Config.normalize("قِطَّة") == "قطه"
    print("   ✓ تطبيع النصوص يعمل بشكل صحيح")
except AssertionError:
    print("   ✗ خطأ في تطبيع النصوص")
    sys.exit(1)

# 5. اختبار الالعاب
print("\n5. اختبار الالعاب...")
try:
    db = Database(":memory:")
    
    # لعبة الذكاء
    from games.iq import IQGame
    game = IQGame(db)
    question = game.get_question()
    assert question is not None, "فشل في انشاء سؤال الذكاء"
    print("   ✓ لعبة الذكاء")
    
    # لعبة الرياضيات
    from games.math import MathGame
    game = MathGame(db)
    question = game.get_question()
    assert question is not None, "فشل في انشاء سؤال الرياضيات"
    print("   ✓ لعبة الرياضيات")
    
    # لعبة خمن
    from games.guess import GuessGame
    game = GuessGame(db)
    question = game.get_question()
    assert question is not None, "فشل في انشاء سؤال خمن"
    print("   ✓ لعبة خمن")
    
    # لعبة ترتيب
    from games.scramble import ScrambleGame
    game = ScrambleGame(db)
    question = game.get_question()
    assert question is not None, "فشل في انشاء سؤال ترتيب"
    print("   ✓ لعبة ترتيب")
    
    # لعبة الاضداد
    from games.opposite import OppositeGame
    game = OppositeGame(db)
    question = game.get_question()
    assert question is not None, "فشل في انشاء سؤال الاضداد"
    print("   ✓ لعبة الاضداد")
    
    # لعبة المافيا
    from games.mafia import MafiaGame
    game = MafiaGame(db)
    result = game.start("test_user")
    assert result is not None, "فشل في بدء لعبة المافيا"
    print("   ✓ لعبة المافيا")
    
    print("   ✓ جميع الالعاب تعمل بشكل صحيح")
except Exception as e:
    print(f"   ✗ خطأ في الالعاب: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 6. اختبار مدير الالعاب
print("\n6. اختبار مدير الالعاب...")
try:
    db = Database(":memory:")
    db.register_user("test_user", "اختبار")
    game_mgr = GameManager(db)
    
    # بدء لعبة
    question = game_mgr.start_game("test_user", "ذكاء")
    assert question is not None, "فشل في بدء اللعبة"
    print("   ✓ بدء اللعبة")
    
    # ايقاف لعبة
    score = game_mgr.stop_game("test_user")
    assert isinstance(score, int), "خطأ في ايقاف اللعبة"
    print("   ✓ ايقاف اللعبة")
    
    print("   ✓ مدير الالعاب يعمل بشكل صحيح")
except Exception as e:
    print(f"   ✗ خطأ في مدير الالعاب: {e}")
    sys.exit(1)

# 7. اختبار مدير المحتوى
print("\n7. اختبار مدير المحتوى...")
try:
    text_mgr = TextManager()
    
    # اختبار الاوامر
    commands = ["تحدي", "اعتراف", "منشن", "سؤال", "حكمه", "موقف"]
    for cmd in commands:
        content = text_mgr.get_content(cmd)
        assert content is not None, f"فشل في الحصول على محتوى {cmd}"
    
    print("   ✓ مدير المحتوى يعمل بشكل صحيح")
except Exception as e:
    print(f"   ✗ خطأ في مدير المحتوى: {e}")
    sys.exit(1)

# 8. اختبار واجهة المستخدم
print("\n8. اختبار واجهة المستخدم...")
try:
    db = Database(":memory:")
    db.register_user("test_user", "اختبار")
    user = db.get_user("test_user")
    
    # اختبار الشاشات
    message = UI.registration_success("اختبار", "light")
    assert message is not None, "فشل في شاشة التسجيل"
    
    message = UI.main_menu(user, db)
    assert message is not None, "فشل في القائمة الرئيسية"
    
    message = UI.games_list("light")
    assert message is not None, "فشل في قائمة الالعاب"
    
    message = UI.user_stats(user)
    assert message is not None, "فشل في احصائيات المستخدم"
    
    print("   ✓ واجهة المستخدم تعمل بشكل صحيح")
except Exception as e:
    print(f"   ✗ خطأ في واجهة المستخدم: {e}")
    sys.exit(1)

# 9. اختبار متغيرات البيئة
print("\n9. اختبار متغيرات البيئة...")
warnings = []
if not Config.LINE_CHANNEL_SECRET:
    warnings.append("LINE_CHANNEL_SECRET غير موجود")
if not Config.LINE_CHANNEL_ACCESS_TOKEN:
    warnings.append("LINE_CHANNEL_ACCESS_TOKEN غير موجود")

if warnings:
    print("   ! تحذيرات:")
    for warning in warnings:
        print(f"     - {warning}")
    print("   ! تأكد من اعداد ملف .env للتشغيل الفعلي")
else:
    print("   ✓ جميع المتغيرات موجودة")

# النتيجة النهائية
print("\n" + "=" * 60)
print("النتيجة: جميع الاختبارات نجحت!")
print("=" * 60)
print("\nالبوت جاهز للعمل!")
print("\nللتشغيل:")
print("  - تطوير: python app.py")
print("  - انتاج: gunicorn -c gunicorn_config.py app:app")
print("\nلا تنسى اعداد ملف .env بمعلومات LINE Bot")
print("=" * 60)
