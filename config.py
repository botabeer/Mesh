# -*- coding: utf-8 -*-
"""
Bot Mesh - Configuration File
Created by: Abeer Aldosari © 2025
"""
import os
from dotenv import load_dotenv

load_dotenv()

# =============================================================================
# Bot Information
# =============================================================================
BOT_NAME = "Bot Mesh"
BOT_VERSION = "2.0.0"
BOT_RIGHTS = "تم إنشاء هذا البوت بواسطة عبير الدوسري © 2025"

# =============================================================================
# LINE Bot Credentials
# =============================================================================
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')

if not LINE_CHANNEL_SECRET or not LINE_CHANNEL_ACCESS_TOKEN:
    raise ValueError("❌ Missing LINE credentials! Check .env file")

# =============================================================================
# Gemini AI Configuration
# =============================================================================
GEMINI_API_KEYS = [
    os.getenv("GEMINI_API_KEY_1", ''),
    os.getenv("GEMINI_API_KEY_2", ''),
    os.getenv("GEMINI_API_KEY_3", '')
]
GEMINI_API_KEYS = [key for key in GEMINI_API_KEYS if key]
AI_ENABLED = len(GEMINI_API_KEYS) > 0

# =============================================================================
# Points System
# =============================================================================
POINTS_PER_CORRECT = 10
POINTS_PER_HINT = -2
POINTS_PER_SKIP = -1

# =============================================================================
# Game Settings
# =============================================================================
DEFAULT_ROUNDS = 5
DEFAULT_TIME_LIMIT = 30

# =============================================================================
# Theme System (LINE Compatible)
# =============================================================================
THEMES = {
    "💜": {"name": "purple", "color": "#9F7AEA"},
    "💚": {"name": "green", "color": "#48BB78"},
    "🤍": {"name": "white", "color": "#CBD5E0"},
    "🖤": {"name": "black", "color": "#2D3748"},
    "💙": {"name": "blue", "color": "#3182CE"},
    "🩶": {"name": "gray", "color": "#718096"},
    "🩷": {"name": "pink", "color": "#ED64A6"},
    "🧡": {"name": "orange", "color": "#DD6B20"},
    "🤎": {"name": "brown", "color": "#8B4513"}
}
DEFAULT_THEME = "💜"

# =============================================================================
# Fixed Buttons (Always Visible)
# =============================================================================
FIXED_BUTTONS = ["Home", "Games", "Info"]

# =============================================================================
# Available Games
# =============================================================================
GAMES_LIST = {
    "IQ": {"name": "لعبة الذكاء", "emoji": "🧠"},
    "رياضيات": {"name": "لعبة الرياضيات", "emoji": "🔢"},
    "لون الكلمة": {"name": "الكلمة واللون", "emoji": "🎨"},
    "كلمة مبعثرة": {"name": "ترتيب الحروف", "emoji": "🔤"},
    "كتابة سريعة": {"name": "الكتابة السريعة", "emoji": "⚡"},
    "عكس": {"name": "ضد الكلمة", "emoji": "↔️"},
    "حروف وكلمات": {"name": "تكوين الكلمات", "emoji": "📝"},
    "أغنية": {"name": "تخمين الأغنية", "emoji": "🎵"},
    "إنسان حيوان نبات": {"name": "إنسان حيوان نبات", "emoji": "🌍"},
    "سلسلة كلمات": {"name": "سلسلة الكلمات", "emoji": "🔗"},
    "تخمين": {"name": "لعبة التخمين", "emoji": "🔮"},
    "توافق": {"name": "لعبة التوافق", "emoji": "💕"}
}

# =============================================================================
# Bot Behavior
# =============================================================================
BOT_SETTINGS = {
    "silent_mode": True,
    "registered_users_only": True,
    "auto_delete_after_days": 7,
    "max_active_games": 10
}

# =============================================================================
# Data Storage
# =============================================================================
REGISTERED_USERS_FILE = 'registered_users.json'
ADMIN_USER_ID = os.getenv('ADMIN_USER_ID', '')

# =============================================================================
# Validation
# =============================================================================
def validate_config():
    """Validate configuration on startup"""
    errors = []
    
    if not LINE_CHANNEL_SECRET:
        errors.append("LINE_CHANNEL_SECRET is missing")
    if not LINE_CHANNEL_ACCESS_TOKEN:
        errors.append("LINE_CHANNEL_ACCESS_TOKEN is missing")
    
    if errors:
        raise ValueError(f"Configuration errors:\n" + "\n".join([f"❌ {e}" for e in errors]))
    
    return True

validate_config()

print("✅ Configuration loaded successfully!")
print(f"✅ AI Features: {'Enabled' if AI_ENABLED else 'Disabled'}")
print(f"✅ AI Keys Available: {len(GEMINI_API_KEYS)}")
print(f"✅ Available Games: {len(GAMES_LIST)}")
print(f"✅ Available Themes: {len(THEMES)}")
