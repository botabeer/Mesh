# -*- coding: utf-8 -*-
"""
Bot Mesh - Complete Configuration File
Created by: Abeer Aldosari © 2025
"""
import os
from dotenv import load_dotenv

# =============================================================================
# تحميل المتغيرات البيئية من .env
# =============================================================================
load_dotenv()

# =============================================================================
# Bot Info
# =============================================================================
BOT_NAME = "Bot Mesh"
BOT_VERSION = "2.0.0"
BOT_RIGHTS = "تم إنشاء هذا البوت بواسطة عبير الدوسري © 2025"

# =============================================================================
# LINE Bot Configuration
# =============================================================================
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')

if not LINE_CHANNEL_SECRET or not LINE_CHANNEL_ACCESS_TOKEN:
    raise ValueError("❌ Missing required LINE credentials in .env file!")

# =============================================================================
# AI Configuration
# =============================================================================
GEMINI_API_KEYS = [
    os.getenv("GEMINI_API_KEY_1", ''),
    os.getenv("GEMINI_API_KEY_2", ''),
    os.getenv("GEMINI_API_KEY_3", '')
]
AI_ENABLED = any(GEMINI_API_KEYS)

# =============================================================================
# Points System
# =============================================================================
POINTS_PER_CORRECT = 10
POINTS_PER_WIN = 5
POINTS_PER_HINT = -2

# =============================================================================
# Game Defaults
# =============================================================================
DEFAULT_ROUNDS = 5
DEFAULT_TIME_LIMIT = 30  # بالثواني

# =============================================================================
# Themes
# =============================================================================
THEMES = {
    "white": {"bg": "#F8F9FA", "card": "#FFFFFF", "primary": "#667EEA", "text": "#2D3748", "text2": "#718096", "shadow": "rgba(0,0,0,0.1)"},
    "dark": {"bg": "#1A202C", "card": "#2D3748", "primary": "#667EEA", "text": "#F7FAFC", "text2": "#CBD5E0", "shadow": "rgba(0,0,0,0.3)"},
    "blue": {"bg": "#EBF4FF", "card": "#FFFFFF", "primary": "#3182CE", "text": "#2C5282", "text2": "#4299E1", "shadow": "rgba(49,130,206,0.1)"},
    "green": {"bg": "#F0FFF4", "card": "#FFFFFF", "primary": "#48BB78", "text": "#276749", "text2": "#68D391", "shadow": "rgba(72,187,120,0.1)"},
    "purple": {"bg": "#FAF5FF", "card": "#FFFFFF", "primary": "#9F7AEA", "text": "#553C9A", "text2": "#B794F4", "shadow": "rgba(159,122,234,0.1)"},
    "pink": {"bg": "#FFF5F7", "card": "#FFFFFF", "primary": "#ED64A6", "text": "#97266D", "text2": "#F687B3", "shadow": "rgba(237,100,166,0.1)"},
    "black": {"bg": "#1A202C", "card": "#2D3748", "primary": "#667EEA", "text": "#E2E8F0", "text2": "#CBD5E0"},
    "orange": {"bg": "#FFFAF0", "card": "#FEEBC8", "primary": "#DD6B20", "text": "#7C2D12", "text2": "#C05621"},
    "brown": {"bg": "#F7F3EF", "card": "#EDE0D4", "primary": "#8B4513", "text": "#5C2E00", "text2": "#7A4F1D"},
    "gray": {"bg": "#F7FAFC", "card": "#EDF2F7", "primary": "#718096", "text": "#2D3748", "text2": "#4A5568"}
}
DEFAULT_THEME = "white"

THEME_EMOJI_MAP = {
    "💜": "purple", "💚": "green", "🤍": "white", "🖤": "black",
    "💙": "blue", "🩶": "gray", "🩷": "pink", "🧡": "orange", "🤎": "brown"
}

# =============================================================================
# Bot Behavior Settings
# =============================================================================
BOT_SETTINGS = {
    "silent_mode": True,
    "registered_users_only": True,
    "command_only": True,
    "allow_game_responses": True,
    "send_welcome_message": False,
    "send_goodbye_message": False,
    "log_activities": True,
    "max_active_games": 10,
    "game_timeout_minutes": 30
}

# =============================================================================
# User Management
# =============================================================================
REGISTERED_USERS_FILE = 'registered_users.json'
ADMIN_USER_ID = os.getenv('ADMIN_USER_ID', '')
DEFAULT_REGISTERED_USERS = []

# =============================================================================
# Fixed Buttons
# =============================================================================
FIXED_BUTTONS = ["Home", "Games", "Info"]

# =============================================================================
# Available Commands
# =============================================================================
BOT_COMMANDS = {
    "ابدأ": "بدء لعبة جديدة",
    "لعبة": "اختيار لعبة محددة",
    "نقاطي": "عرض النقاط",
    "تصنيف": "عرض التصنيف العام",
    "توقف": "إيقاف اللعبة الحالية",
    "مساعدة": "عرض المساعدة",
    "لمح": "الحصول على تلميح",
    "جاوب": "كشف الإجابة والانتقال للسؤال التالي",
    "ثيم": "تغيير ثيم اللعبة"
}

# =============================================================================
# Games List
# =============================================================================
GAMES_LIST = {
    "IQ": {"name": "لعبة الذكاء", "emoji": "🧠", "rounds": 5},
    "رياضيات": {"name": "لعبة الرياضيات", "emoji": "🔢", "rounds": 5},
    "لون الكلمة": {"name": "الكلمة واللون", "emoji": "🎨", "rounds": 10},
    "كلمة مبعثرة": {"name": "ترتيب الحروف", "emoji": "🔤", "rounds": 10},
    "كتابة سريعة": {"name": "الكتابة السريعة", "emoji": "⚡", "rounds": 5},
    "عكس": {"name": "ضد الكلمة", "emoji": "↔️", "rounds": 10},
    "حروف وكلمات": {"name": "تكوين الكلمات", "emoji": "📝", "rounds": 5},
    "أغنية": {"name": "تخمين الأغنية", "emoji": "🎵", "rounds": 5},
    "إنسان حيوان نبات": {"name": "إنسان حيوان نبات", "emoji": "🌍", "rounds": 5},
    "سلسلة كلمات": {"name": "سلسلة الكلمات", "emoji": "🔗", "rounds": 5},
    "تخمين": {"name": "لعبة التخمين", "emoji": "🔮", "rounds": 5},
    "توافق": {"name": "لعبة التوافق", "emoji": "💕", "rounds": 1}
}

# =============================================================================
# Response Messages
# =============================================================================
MESSAGES = {
    "welcome": "مرحبًا بك في Bot Mesh! 🤖",
    "not_registered": "⚠️ يجب التسجيل أولاً باستخدام زر 'انضم'",
    "choose_game": "اختر لعبة من القائمة:",
    "game_started": "🎮 بدأت اللعبة! حظاً موفقاً",
    "game_stopped": "⏹️ تم إيقاف اللعبة",
    "game_ended": "🏁 انتهت اللعبة",
    "invalid_command": "❌ أمر غير صحيح",
    "help_message": """
🎮 **أوامر البوت**

• ابدأ - بدء لعبة عشوائية
• لعبة - اختيار لعبة محددة
• نقاطي - عرض نقاطك
• تصنيف - عرض التصنيف
• توقف - إيقاف اللعبة
• ثيم - تغيير الثيم
• لمح - تلميح
• جاوب - كشف الإجابة

**أثناء اللعبة:**
• اكتب إجابتك مباشرة
• لمح - للحصول على تلميح
• جاوب - للانتقال للسؤال التالي
"""
}

# =============================================================================
# Logging Configuration
# =============================================================================
LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"standard": {"format": '%(asctime)s - %(name)s - %(levelname)s - %(message)s'}},
    "handlers": {
        "console": {"class": "logging.StreamHandler", "level": "INFO", "formatter": "standard", "stream": "ext://sys.stdout"},
        "file": {"class": "logging.FileHandler", "level": "INFO", "formatter": "standard", "filename": "bot.log", "mode": "a"}
    },
    "loggers": {"": {"handlers": ["console", "file"], "level": "INFO", "propagate": True}}
}

# =============================================================================
# Validation
# =============================================================================
def validate_config():
    errors = []
    if not LINE_CHANNEL_SECRET:
        errors.append("LINE_CHANNEL_SECRET is missing")
    if not LINE_CHANNEL_ACCESS_TOKEN:
        errors.append("LINE_CHANNEL_ACCESS_TOKEN is missing")
    if errors:
        error_msg = "\n".join([f"❌ {err}" for err in errors])
        raise ValueError(f"Configuration errors:\n{error_msg}")
    return True

validate_config()

print("✅ Configuration loaded successfully!")
print(f"✅ AI Features: {'Enabled' if AI_ENABLED else 'Disabled'}")
print(f"✅ Silent Mode: {'On' if BOT_SETTINGS['silent_mode'] else 'Off'}")
print(f"✅ Registered Users Only: {'Yes' if BOT_SETTINGS['registered_users_only'] else 'No'}")
print(f"✅ Available Games: {len(GAMES_LIST)}")
print(f"✅ Available Themes: {len(THEMES)}")
