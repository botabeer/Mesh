"""
Bot Mesh - Constants & Configuration
تم إنشاء هذا البوت بواسطة عبير الدوسري © 2025
"""

import os

# ============================================================================
# Bot Information
# ============================================================================
BOT_NAME = "Bot Mesh"
BOT_VERSION = "3.0.0"
BOT_RIGHTS = "Bot Mesh © 2025 — تم إنشاء هذا البوت بواسطة عبير الدوسري"

# ============================================================================
# LINE Credentials
# ============================================================================
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')

# ============================================================================
# Gemini AI Keys (Optional - 3 keys for fallback)
# ============================================================================
GEMINI_API_KEY_1 = os.getenv('GEMINI_API_KEY_1')
GEMINI_API_KEY_2 = os.getenv('GEMINI_API_KEY_2')
GEMINI_API_KEY_3 = os.getenv('GEMINI_API_KEY_3')

# ============================================================================
# Game Settings
# ============================================================================
ROUNDS_PER_GAME = 5
POINTS_PER_CORRECT_ANSWER = 10
INACTIVITY_DAYS = 7

# ============================================================================
# Themes (9 Professional Themes - NO GROUPS - Ordered List)
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
        "button": "#4299E1"
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
        "button": "#667EEA"
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
        "button": "#4A5568"
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
        "button": "#2B6CB0"
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
        "button": "#805AD5"
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
        "button": "#B83280"
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
        "button": "#38A169"
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
        "button": "#C05621"
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
        "button": "#744210"
    }
}

DEFAULT_THEME = "أبيض"

# ============================================================================
# Available Games (ORDERED LIST - NO EMOJI - WITH ▫️)
# ============================================================================
GAME_LIST = {
    "سرعة": {"label": "▫️ سرعة", "file": "fast_typing_game"},
    "ذكاء": {"label": "▫️ ذكاء", "file": "iq_game"},
    "لعبة": {"label": "▫️ لعبة", "file": "human_animal_plant_game"},
    "أغنية": {"label": "▫️ أغنية", "file": "song_game"},
    "خمن": {"label": "▫️ خمن", "file": "guess_game"},
    "سلسلة": {"label": "▫️ سلسلة", "file": "chain_words_game"},
    "ترتيب": {"label": "▫️ ترتيب", "file": "scramble_word_game"},
    "تكوين": {"label": "▫️ تكوين", "file": "letters_words_game"},
    "ضد": {"label": "▫️ ضد", "file": "opposite_game"},
    "لون": {"label": "▫️ لون", "file": "word_color_game"},
    "رياضيات": {"label": "▫️ رياضيات", "file": "math_game"},
    "توافق": {"label": "▫️ توافق", "file": "compatibility_game"}  # Always last
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
    
    # Check AI keys
    ai_keys = [GEMINI_API_KEY_1, GEMINI_API_KEY_2, GEMINI_API_KEY_3]
    active_keys = [k for k in ai_keys if k]
    
    if not active_keys:
        print("⚠️ No Gemini AI keys found - AI features will use fallback mode")
    else:
        print(f"✅ {len(active_keys)} Gemini AI key(s) available")
    
    return True
