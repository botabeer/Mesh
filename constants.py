"""
Bot Mesh - Constants & Configuration
Created by: Abeer Aldosari © 2025
"""

import os

# Bot Information
BOT_NAME = "Bot Mesh"
BOT_VERSION = "3.0.0"
BOT_RIGHTS = "تم إنشاء هذا البوت بواسطة عبير الدوسري © 2025"

# LINE Credentials
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')

# Gemini AI Keys (3 keys for fallback)
GEMINI_API_KEY_1 = os.getenv('GEMINI_API_KEY_1')
GEMINI_API_KEY_2 = os.getenv('GEMINI_API_KEY_2')
GEMINI_API_KEY_3 = os.getenv('GEMINI_API_KEY_3')

# Game Settings
ROUNDS_PER_GAME = 5
POINTS_PER_CORRECT_ANSWER = 10
INACTIVITY_DAYS = 7

# Neumorphism Soft Themes (9 Professional Themes)
THEMES = {
    "💜": {
        "name": "Purple Dream",
        "bg": "#E0E5EC",
        "card": "#E0E5EC",
        "primary": "#9F7AEA",
        "secondary": "#B794F4",
        "text": "#44337A",
        "text2": "#6B46C1",
        "shadow1": "#A3B1C6",
        "shadow2": "#FFFFFF",
        "button": "#9F7AEA"
    },
    "💚": {
        "name": "Green Nature",
        "bg": "#E0E5EC",
        "card": "#E0E5EC",
        "primary": "#48BB78",
        "secondary": "#68D391",
        "text": "#234E52",
        "text2": "#2C7A7B",
        "shadow1": "#A3B1C6",
        "shadow2": "#FFFFFF",
        "button": "#48BB78"
    },
    "🤍": {
        "name": "Clean White",
        "bg": "#E0E5EC",
        "card": "#E0E5EC",
        "primary": "#667EEA",
        "secondary": "#7F9CF5",
        "text": "#2D3748",
        "text2": "#718096",
        "shadow1": "#A3B1C6",
        "shadow2": "#FFFFFF",
        "button": "#667EEA"
    },
    "🖤": {
        "name": "Dark Mode",
        "bg": "#2D3748",
        "card": "#3A4556",
        "primary": "#667EEA",
        "secondary": "#7F9CF5",
        "text": "#E2E8F0",
        "text2": "#CBD5E0",
        "shadow1": "#1A202C",
        "shadow2": "#414D5F",
        "button": "#667EEA"
    },
    "💙": {
        "name": "Ocean Blue",
        "bg": "#E0E5EC",
        "card": "#E0E5EC",
        "primary": "#3182CE",
        "secondary": "#4299E1",
        "text": "#2C5282",
        "text2": "#2B6CB0",
        "shadow1": "#A3B1C6",
        "shadow2": "#FFFFFF",
        "button": "#3182CE"
    },
    "🩶": {
        "name": "Silver Gray",
        "bg": "#E0E5EC",
        "card": "#E0E5EC",
        "primary": "#718096",
        "secondary": "#A0AEC0",
        "text": "#2D3748",
        "text2": "#4A5568",
        "shadow1": "#A3B1C6",
        "shadow2": "#FFFFFF",
        "button": "#718096"
    },
    "🩷": {
        "name": "Pink Blossom",
        "bg": "#E0E5EC",
        "card": "#E0E5EC",
        "primary": "#D53F8C",
        "secondary": "#ED64A6",
        "text": "#702459",
        "text2": "#97266D",
        "shadow1": "#A3B1C6",
        "shadow2": "#FFFFFF",
        "button": "#D53F8C"
    },
    "🧡": {
        "name": "Sunset Orange",
        "bg": "#E0E5EC",
        "card": "#E0E5EC",
        "primary": "#DD6B20",
        "secondary": "#ED8936",
        "text": "#7C2D12",
        "text2": "#C05621",
        "shadow1": "#A3B1C6",
        "shadow2": "#FFFFFF",
        "button": "#DD6B20"
    },
    "🤎": {
        "name": "Earth Brown",
        "bg": "#E0E5EC",
        "card": "#E0E5EC",
        "primary": "#8B4513",
        "secondary": "#A0522D",
        "text": "#5C2E00",
        "text2": "#7A4F1D",
        "shadow1": "#A3B1C6",
        "shadow2": "#FFFFFF",
        "button": "#8B4513"
    }
}

DEFAULT_THEME = "💜"

# Available Games
GAME_LIST = {
    "IQ": {"icon": "🧠", "label": "ذكاء", "ai_enabled": True},
    "رياضيات": {"icon": "🔢", "label": "رياضيات", "ai_enabled": True},
    "لون الكلمة": {"icon": "🎨", "label": "لون", "ai_enabled": False},
    "كلمة مبعثرة": {"icon": "🔤", "label": "ترتيب", "ai_enabled": False},
    "كتابة سريعة": {"icon": "⚡", "label": "أسرع", "ai_enabled": False},
    "عكس": {"icon": "↔️", "label": "ضد", "ai_enabled": True},
    "حروف وكلمات": {"icon": "🔠", "label": "تكوين", "ai_enabled": False},
    "أغنية": {"icon": "🎵", "label": "أغنية", "ai_enabled": False},
    "إنسان حيوان نبات": {"icon": "🌍", "label": "لعبة", "ai_enabled": False},
    "سلسلة كلمات": {"icon": "🔗", "label": "سلسلة", "ai_enabled": False},
    "تخمين": {"icon": "🔮", "label": "خمّن", "ai_enabled": False},
    "توافق": {"icon": "💕", "label": "توافق", "ai_enabled": False}
}

# Fixed Buttons (Always visible)
FIXED_BUTTONS = {
    "home": {"label": "🏠 بداية", "text": "بداية"},
    "games": {"label": "🎮 ألعاب", "text": "مساعدة"},
    "points": {"label": "⭐ نقاطي", "text": "نقاطي"},
    "leaderboard": {"label": "🏆 صدارة", "text": "صدارة"},
    "stop": {"label": "⛔ إيقاف", "text": "إيقاف"}
}

# Arabic Character Normalization
ARABIC_NORMALIZE = {
    'أ': 'ا', 'إ': 'ا', 'آ': 'ا',
    'ى': 'ي', 'ة': 'ه'
}

def normalize_arabic(text):
    """Normalize Arabic text for comparison"""
    text = text.strip().lower()
    for old, new in ARABIC_NORMALIZE.items():
        text = text.replace(old, new)
    return text

def get_username(profile):
    """Extract username from LINE profile safely"""
    try:
        name = profile.display_name if hasattr(profile, 'display_name') else None
        if not name or name.strip() == "":
            return "مستخدم"
        return name.strip()
    except:
        return "مستخدم"

def validate_env():
    """Validate required environment variables"""
    required = ['LINE_CHANNEL_SECRET', 'LINE_CHANNEL_ACCESS_TOKEN']
    missing = [var for var in required if not os.getenv(var)]
    
    if missing:
        raise ValueError(f"❌ Missing environment variables: {', '.join(missing)}")
    
    # Check AI keys
    ai_keys = [GEMINI_API_KEY_1, GEMINI_API_KEY_2, GEMINI_API_KEY_3]
    active_keys = [k for k in ai_keys if k]
    
    if not active_keys:
        print("⚠️ No Gemini AI keys found - AI features will use fallback mode")
    else:
        print(f"✅ {len(active_keys)} Gemini AI key(s) available")
    
    return True
