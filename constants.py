"""
Bot Mesh - Constants & Configuration v3.2
تم إنشاء هذا البوت بواسطة عبير الدوسري © 2025
"""

import os

# ============================================================================
# Bot Information
# ============================================================================
BOT_NAME = "Bot Mesh"
BOT_VERSION = "3.2.0"
BOT_RIGHTS = "Bot Mesh © 2025 — تم إنشاء هذا البوت بواسطة عبير الدوسري"

# ============================================================================
# LINE Credentials
# ============================================================================
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')

# ============================================================================
# Game Settings
# ============================================================================
ROUNDS_PER_GAME = 5
POINTS_PER_CORRECT_ANSWER = 10
INACTIVITY_DAYS = 7

# ============================================================================
# Themes (9 Professional Themes - Ordered List)
# ============================================================================
THEMES = {
    "أبيض": {
        "name": "أبيض",
        "bg": "#F7FAFC",
        "card": "#FFFFFF",
        "primary": "#4299E1",
        "secondary": "#63B3ED",
        "text": "#2D3748",
        "text2": "#718096",
        "shadow1": "#E2E8F0",
        "shadow2": "#FFFFFF",
        "button": "#4299E1",
        "success": "#48BB78",
        "error": "#EF4444"
    },
    "أسود": {
        "name": "أسود",
        "bg": "#1A202C",
        "card": "#2D3748",
        "primary": "#667EEA",
        "secondary": "#7F9CF5",
        "text": "#F7FAFC",
        "text2": "#CBD5E0",
        "shadow1": "#4A5568",
        "shadow2": "#414D5F",
        "button": "#667EEA",
        "success": "#48BB78",
        "error": "#EF4444"
    },
    "رمادي": {
        "name": "رمادي",
        "bg": "#F7FAFC",
        "card": "#FFFFFF",
        "primary": "#4A5568",
        "secondary": "#718096",
        "text": "#2D3748",
        "text2": "#718096",
        "shadow1": "#E2E8F0",
        "shadow2": "#FFFFFF",
        "button": "#4A5568",
        "success": "#48BB78",
        "error": "#EF4444"
    },
    "أزرق": {
        "name": "أزرق",
        "bg": "#EBF8FF",
        "card": "#FFFFFF",
        "primary": "#2B6CB0",
        "secondary": "#3182CE",
        "text": "#2C5282",
        "text2": "#2B6CB0",
        "shadow1": "#BEE3F8",
        "shadow2": "#FFFFFF",
        "button": "#2B6CB0",
        "success": "#48BB78",
        "error": "#EF4444"
    },
    "بنفسجي": {
        "name": "بنفسجي",
        "bg": "#FAF5FF",
        "card": "#FFFFFF",
        "primary": "#805AD5",
        "secondary": "#9F7AEA",
        "text": "#5B21B6",
        "text2": "#7C3AED",
        "shadow1": "#DDD6FE",
        "shadow2": "#FFFFFF",
        "button": "#805AD5",
        "success": "#48BB78",
        "error": "#EF4444"
    },
    "وردي": {
        "name": "وردي",
        "bg": "#FFF5F7",
        "card": "#FFFFFF",
        "primary": "#B83280",
        "secondary": "#D53F8C",
        "text": "#702459",
        "text2": "#97266D",
        "shadow1": "#FED7E2",
        "shadow2": "#FFFFFF",
        "button": "#B83280",
        "success": "#48BB78",
        "error": "#EF4444"
    },
    "أخضر": {
        "name": "أخضر",
        "bg": "#F0FDF4",
        "card": "#FFFFFF",
        "primary": "#38A169",
        "secondary": "#48BB78",
        "text": "#064E3B",
        "text2": "#065F46",
        "shadow1": "#A7F3D0",
        "shadow2": "#FFFFFF",
        "button": "#38A169",
        "success": "#48BB78",
        "error": "#EF4444"
    },
    "برتقالي": {
        "name": "برتقالي",
        "bg": "#FFFAF0",
        "card": "#FFFFFF",
        "primary": "#C05621",
        "secondary": "#DD6B20",
        "text": "#7C2D12",
        "text2": "#9C4221",
        "shadow1": "#FEEBC8",
        "shadow2": "#FFFFFF",
        "button": "#C05621",
        "success": "#48BB78",
        "error": "#EF4444"
    },
    "بني": {
        "name": "بني",
        "bg": "#FEFCF9",
        "card": "#FFFFFF",
        "primary": "#744210",
        "secondary": "#8B4513",
        "text": "#5C2E00",
        "text2": "#7A4F1D",
        "shadow1": "#E6D5C3",
        "shadow2": "#FFFFFF",
        "button": "#744210",
        "success": "#48BB78",
        "error": "#EF4444"
    }
}

DEFAULT_THEME = "أبيض"

# ============================================================================
# Available Games (ORDERED LIST - WITH ICONS)
# ============================================================================
GAME_LIST = {
    "كتابة سريعة": {"label": "سرعة", "icon": "⚡"},
    "IQ": {"label": "ذكاء", "icon": "🧠"},
    "إنسان حيوان نبات": {"label": "لعبة", "icon": "🎯"},
    "أغنية": {"label": "أغنية", "icon": "🎵"},
    "تخمين": {"label": "خمن", "icon": "🔮"},
    "سلسلة كلمات": {"label": "سلسلة", "icon": "🔗"},
    "كلمة مبعثرة": {"label": "ترتيب", "icon": "🔤"},
    "حروف وكلمات": {"label": "تكوين", "icon": "📝"},
    "عكس": {"label": "ضد", "icon": "↔️"},
    "لون الكلمة": {"label": "لون", "icon": "🎨"},
    "رياضيات": {"label": "رياضيات", "icon": "🔢"},
    "توافق": {"label": "توافق", "icon": "🖤"}
}

# ============================================================================
# Fixed Buttons
# ============================================================================
FIXED_BUTTONS = {
    "home": {"label": "🏠 البداية", "text": "بداية"},
    "games": {"label": "🎮 الألعاب", "text": "مساعدة"},
    "points": {"label": "⭐ نقاطي", "text": "نقاطي"},
    "leaderboard": {"label": "🏆 الصدارة", "text": "صدارة"},
    "stop": {"label": "⛔ إيقاف", "text": "إيقاف"}
}

# ============================================================================
# Helper Functions
# ============================================================================
def normalize_arabic(text):
    """Normalize Arabic text for comparison"""
    ARABIC_NORMALIZE = {
        'أ': 'ا', 'إ': 'ا', 'آ': 'ا',
        'ى': 'ي', 'ة': 'ه'
    }
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
    
    return True
