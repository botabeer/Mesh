# -*- coding: utf-8 -*-
import os

# اسم البوت
BOT_NAME = "Bot Mesh"

# الأزرار الثابتة
FIXED_BUTTONS = ["Home", "Games", "Info"]

# الثيمات
THEMES = ["💜", "💚", "🤍", "🖤", "💙", "🩶", "🩷", "🧡", "🤎"]

# مفاتيح Gemini API
GEMINI_KEYS = [
    os.getenv("GEMINI_API_KEY_1"),
    os.getenv("GEMINI_API_KEY_2"),
    os.getenv("GEMINI_API_KEY_3")
]

# دالة لجلب اسم المستخدم فقط
def get_username(user_profile):
    """جلب اسم المستخدم من LINE بدون ID"""
    try:
        return user_profile.display_name
    except:
        return "مستخدم"

# الحقوق
BOT_RIGHTS = "تم إنشاء هذا البوت بواسطة عبير الدوسري @ 2025"
